#!/usr/bin/env python3
"""Generate deterministic pack bundle manifests.

This tool writes the bundle-manifest.json surfaces for the selected pack set.
The editable registry lives in `codex-marketplace/custody-pack-registry.json`
so both projection-lane packs and mega packs can be regenerated from one
source of truth instead of being hand-edited.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_json

PACK_REGISTRY_PATH = ROOT / "codex-marketplace/custody-pack-registry.json"


def _entry(
    canonical_name: str,
    *,
    source_category: str,
    source_family: str,
    canonical_source_path: str,
    local_path: str,
    content_mode: str = "verbatim",
    provenance_note: str,
    adaptation_overlay_path: str | None = None,
    adaptation_note: str | None = None,
    source_path: str | None = None,
    source_author: str | None = None,
    source_license: str | None = None,
    source_repo: str | None = None,
    adapted_author: str | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "canonical_name": canonical_name,
        "source_category": source_category,
        "content_mode": content_mode,
        "source_family": source_family,
        "canonical_source_path": canonical_source_path,
        "local_path": local_path,
        "provenance_note": provenance_note,
    }
    if source_path is not None:
        entry["source_path"] = source_path
    if source_author is not None:
        entry["source_author"] = source_author
    if source_license is not None:
        entry["source_license"] = source_license
    if source_repo is not None:
        entry["source_repo"] = source_repo
    if adapted_author is not None:
        entry["adapted_author"] = adapted_author
    if adaptation_overlay_path is not None:
        entry["adaptation_overlay_path"] = adaptation_overlay_path
    if adaptation_note is not None:
        entry["adaptation_note"] = adaptation_note
    if content_mode == "verbatim":
        entry["copy_expectation"] = "byte_identical"
    elif content_mode == "normalised":
        entry["copy_expectation"] = "normalised_from_source"
    else:
        entry["copy_expectation"] = "adapted_from_source"
    return entry


def _repo_index(plugin_root: str, *, agents_md: str | None = None) -> dict[str, Any]:
    return {
        "source_md": f"{plugin_root}/SOURCE.md",
        "bundle_manifest": f"{plugin_root}/references/bundle-manifest.json",
        "skills_path": f"{plugin_root}/skills",
        "agents_md": agents_md,
        "registry_alignment": {
            "status": "aligned",
            "note": None,
        },
    }


def load_pack_registry() -> list[dict[str, Any]]:
    registry = load_json(PACK_REGISTRY_PATH)
    if registry.get("schema_version") != 1:
        raise ValueError(f"{PACK_REGISTRY_PATH}: schema_version must be 1")
    packs = registry.get("packs")
    if not isinstance(packs, list) or not packs:
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must be a non-empty list")
    normalized = [pack for pack in packs if isinstance(pack, dict)]
    if len(normalized) != len(packs):
        raise ValueError(f"{PACK_REGISTRY_PATH}: packs must contain objects")
    return normalized


PACKS = [pack for pack in load_pack_registry() if not pack.get("is_mega_pack")]
OPTIONAL_MANIFEST_FIELDS = (
    "marketplace_root",
    "canonical_source_roots",
    "source_of_truth",
    "projection_policy",
)


def _bundle_manifest(pack: dict[str, Any]) -> dict[str, Any]:
    entries = sorted(pack["entries"], key=lambda item: item["canonical_name"])
    source_families = sorted({entry["source_family"] for entry in entries})
    manifest: dict[str, Any] = {
        "bundle_name": pack["bundle_name"],
        "bundle_version": pack["bundle_version"],
        "bundle_type": pack["bundle_type"],
        "marketplace_root": ".agents/plugins/marketplace.json",
        "plugin_root": pack["plugin_root"],
        "is_mega_pack": pack["is_mega_pack"],
        "source_families": source_families,
        "notes": pack["notes"],
        "provenance_refs": pack["provenance_refs"],
        "plugin_author": "Harley Bartles",
        "plugin_license": "MIT",
        "entries": entries,
    }
    for field_name in OPTIONAL_MANIFEST_FIELDS:
        value = pack.get(field_name)
        if value is not None:
            manifest[field_name] = value
    if not pack.get("is_mega_pack"):
        manifest["repo_index"] = _repo_index(
            pack["plugin_root"],
        )
    if pack.get("mega_pack_for") is not None:
        manifest["mega_pack_for"] = pack["mega_pack_for"]
    return manifest


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def generate(*, write: bool) -> None:
    for pack in PACKS:
        manifest = _bundle_manifest(pack)
        manifest_path = ROOT / pack["plugin_root"] / "references" / "bundle-manifest.json"
        if write:
            _write_manifest(manifest_path, manifest)
            print(f"WROTE {manifest_path.relative_to(ROOT)}")
            continue
        if not manifest_path.exists():
            raise FileNotFoundError(manifest_path)
        current = json.loads(manifest_path.read_text(encoding="utf-8"))
        if current != manifest:
            raise ValueError(f"{manifest_path.relative_to(ROOT)} is stale; run py -3 tools/generate_pack_manifests.py")
        print(f"OK   {manifest_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the selected pack bundle manifests")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    generate(write=not args.check)
    if args.check:
        print("OK pack manifests: current")
    else:
        print("OK pack manifests: generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
