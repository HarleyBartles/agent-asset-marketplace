#!/usr/bin/env python3
"""Copy completed plans to verified off-repo cold storage without deleting Git files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    return env


def _worktree_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip()).resolve()


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1]).resolve()
    raise RuntimeError("could not determine the main repository root")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _inventory(source: Path) -> list[dict[str, str]]:
    return [
        {"path": path.relative_to(source).as_posix(), "sha256": _sha256(path)}
        for path in sorted(source.rglob("*"))
        if path.is_file()
    ]


def _manifest_path(archive: Path) -> Path:
    return archive / "manifest.json"


def _expected_manifest(source: Path) -> dict[str, object]:
    return {"schema_version": 1, "source": ".agents/plans/completed", "files": _inventory(source)}


def _read_manifest(archive: Path) -> dict[str, object] | None:
    path = _manifest_path(archive)
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _matches(source: Path, archive: Path) -> bool:
    expected = _expected_manifest(source)
    if _read_manifest(archive) != expected:
        return False
    return all(
        (archive / item["path"]).is_file()
        and _sha256(archive / item["path"]) == item["sha256"]
        for item in expected["files"]
    )


def _archive_matches_manifest(archive: Path) -> bool:
    manifest = _read_manifest(archive)
    files = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(files, list):
        return False
    return all(
        isinstance(item, dict)
        and isinstance(item.get("path"), str)
        and isinstance(item.get("sha256"), str)
        and (archive / item["path"]).is_file()
        and _sha256(archive / item["path"]) == item["sha256"]
        for item in files
    )


def _apply(source: Path, archive: Path) -> None:
    expected = _expected_manifest(source)
    archive.mkdir(parents=True, exist_ok=True)
    for item in expected["files"]:
        target = archive / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / item["path"], target)
    _manifest_path(archive).write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    root = _worktree_root()
    main_root = _main_repo_root()
    default_source = root / ".agents" / "plans" / "completed"
    default_archive = main_root.parent / "_agent-scratch" / main_root.name / "archive" / "completed-plans"
    parser = argparse.ArgumentParser(
        description=(
            "Copy completed plans to verified off-repo cold storage. "
            "(mixed: supports --check and --apply)"
        )
    )
    parser.add_argument("--source", type=Path, default=default_source)
    parser.add_argument("--archive", type=Path, default=default_archive)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="verify copy and manifest without writing (default)",
    )
    mode.add_argument("--apply", action="store_true", help="copy plans and write manifest; never deletes source files")
    args = parser.parse_args(argv)
    source = args.source.resolve()
    archive = args.archive.resolve()
    if args.apply:
        if not source.is_dir():
            print(f"ERROR: completed-plan source is missing: {source}")
            return 1
        _apply(source, archive)
    matched = _matches(source, archive) if source.is_dir() else _archive_matches_manifest(archive)
    if not matched:
        print(f"DRIFT: archive does not match source: {archive}")
        return 1
    count = len(_inventory(source)) if source.is_dir() else len(_read_manifest(archive)["files"])
    print(f"OK: {count} completed plan file(s) verified at {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
