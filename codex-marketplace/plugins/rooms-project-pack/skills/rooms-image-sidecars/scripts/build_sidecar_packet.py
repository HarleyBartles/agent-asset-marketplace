#!/usr/bin/env python3
"""Build a Rooms image sidecar packet from ordered images and sidecar files.

This helper does not analyze images. It packages GPT-authored semantic sidecars
with raw ordered images, hashes, and a starter manifest.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import re
import shutil
import tempfile
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def image_dimensions(path: Path) -> tuple[int | None, int | None]:
    data = path.read_bytes()[:32]
    suffix = path.suffix.lower()
    if suffix == ".png" and len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if suffix == ".gif" and len(data) >= 10 and data[:6] in {b"GIF87a", b"GIF89a"}:
        return int.from_bytes(data[6:8], "little"), int.from_bytes(data[8:10], "little")
    return None, None


def iter_images(input_dir: Path) -> list[Path]:
    images = [p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
    def natural_key(path: Path) -> list[object]:
        parts = re.split(r"(\d+)", path.name.casefold())
        return [int(part) if part.isdigit() else part for part in parts]

    return sorted(images, key=natural_key)


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_optional(src: Path | None, dst: Path) -> None:
    if src is not None:
        shutil.copy2(src, dst)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Rooms image sidecar packet")
    parser.add_argument("--input-dir", required=True, type=Path, help="Folder containing image files")
    parser.add_argument("--sidecar", required=True, type=Path, help="semantic_sidecar.json")
    parser.add_argument("--sidecar-md", type=Path, help="semantic_sidecar.md")
    parser.add_argument("--readme", type=Path, help="README_FOR_ALBERT.md")
    parser.add_argument("--batch-intake", type=Path, help="batch.intake.json")
    parser.add_argument("--observation-csv", type=Path, help="image_observation_table.csv")
    parser.add_argument("--conversation-csv", type=Path, help="conversation_candidates.csv or conversation_promotion_companion.csv")
    parser.add_argument("--db-companion-dir", type=Path, help="Folder of DB promotion companion CSVs to copy into db_promotion_companion/")
    parser.add_argument("--output", required=True, type=Path, help="Output .zip path")
    args = parser.parse_args(argv)

    input_dir = args.input_dir.resolve()
    if not input_dir.is_dir():
        print(f"input dir not found: {input_dir}", file=sys.stderr)
        return 2
    if not args.sidecar.is_file():
        print(f"semantic sidecar not found: {args.sidecar}", file=sys.stderr)
        return 2

    images = iter_images(input_dir)
    if not images:
        print("no supported image files found", file=sys.stderr)
        return 2

    sidecar = load_json(args.sidecar)
    expected_count = sidecar.get("source_batch", {}).get("expected_image_count")
    if expected_count is not None and int(expected_count) != len(images):
        print(f"warning: expected {expected_count} images but found {len(images)}", file=sys.stderr)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{args.output.stem}_", dir=args.output.parent) as tmp_dir:
        work_dir = Path(tmp_dir)
        (work_dir / "raw").mkdir(parents=True)
        (work_dir / "db_promotion_companion").mkdir(parents=True)

        manifest_entries: list[dict[str, Any]] = []
        for seq, image in enumerate(images, start=1):
            target_name = f"{seq:03d}__{image.name}"
            target = work_dir / "raw" / target_name
            shutil.copy2(image, target)
            width, height = image_dimensions(image)
            manifest_entries.append(
                {
                    "image_seq": seq,
                    "original_filename": image.name,
                    "packet_filename": f"raw/{target_name}",
                    "byte_size": image.stat().st_size,
                    "content_hash": sha256_file(image),
                    "mime_type": mimetypes.guess_type(image.name)[0] or "application/octet-stream",
                    "width": width,
                    "height": height,
                }
            )

        starter_manifest = {
            "manifest_type": "rooms_image_sidecar_packet_manifest",
            "generated_at": utc_now(),
            "image_count": len(manifest_entries),
            "sidecar_type": sidecar.get("sidecar_type", "unknown"),
            "sidecar_status": sidecar.get("status", "unknown"),
            "truth_boundary": sidecar.get("truth_boundary", "starter guidance only"),
            "images": manifest_entries,
        }
        write_json(work_dir / "starter_manifest.json", starter_manifest)

        copy_optional(args.sidecar, work_dir / "semantic_sidecar.json")
        copy_optional(args.sidecar_md, work_dir / "semantic_sidecar.md")
        copy_optional(args.readme, work_dir / "README_FOR_ALBERT.md")
        copy_optional(args.batch_intake, work_dir / "batch.intake.json")
        copy_optional(args.observation_csv, work_dir / "image_observation_table.csv")
        copy_optional(args.conversation_csv, work_dir / "conversation_candidates.csv")
        if args.db_companion_dir is not None:
            if not args.db_companion_dir.is_dir():
                print(f"db companion dir not found: {args.db_companion_dir}", file=sys.stderr)
                return 2
            for companion in sorted(args.db_companion_dir.iterdir()):
                if companion.is_file():
                    shutil.copy2(companion, work_dir / "db_promotion_companion" / companion.name)

        if args.observation_csv is None:
            with (work_dir / "image_observation_table.csv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["image_seq", "filename", "notes"])
                writer.writeheader()
                for entry in manifest_entries:
                    writer.writerow({"image_seq": entry["image_seq"], "filename": entry["packet_filename"], "notes": "see semantic_sidecar.json"})

        if args.output.exists():
            args.output.unlink()
        with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(work_dir.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(work_dir).as_posix())

    print(f"wrote {args.output} with {len(manifest_entries)} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
