#!/usr/bin/env python3
"""Materialize the Superpowers+ marketplace projection from custody plus overlays."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from marketplace_utils import load_json
from skill_overlay_materializer import apply_overlay_tree, stage_overlay_tree


ROOT = Path(__file__).resolve().parents[1]
BUNDLE_MANIFEST_PATH = ROOT / "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json"
PROJECTION_ROOT = ROOT / "codex-marketplace/plugins/superpowers-plus"


def _load_bundle_manifest() -> dict[str, Any]:
    if not BUNDLE_MANIFEST_PATH.exists():
        raise FileNotFoundError(BUNDLE_MANIFEST_PATH)
    bundle_manifest = load_json(BUNDLE_MANIFEST_PATH)
    if not isinstance(bundle_manifest, dict):
        raise ValueError(f"{BUNDLE_MANIFEST_PATH} must contain a JSON object")
    return bundle_manifest


def _entry_overlay_root(entry: dict[str, Any]) -> Path | None:
    overlay_path = entry.get("adaptation_overlay_path")
    if overlay_path is None:
        return None
    if not isinstance(overlay_path, str) or not overlay_path.strip():
        raise ValueError(f"superpowers-plus entry {entry.get('canonical_name')} has an invalid adaptation_overlay_path")
    overlay_root = (ROOT / overlay_path).resolve()
    if not overlay_root.exists():
        raise FileNotFoundError(overlay_root)
    return overlay_root


def _validate_entry(entry: dict[str, Any]) -> None:
    canonical_name = entry.get("canonical_name")
    if not isinstance(canonical_name, str) or not canonical_name:
        raise ValueError("superpowers-plus bundle manifest entry is missing canonical_name")
    source_category = entry.get("source_category")
    content_mode = entry.get("content_mode")
    canonical_source_path = entry.get("canonical_source_path")
    local_path = entry.get("local_path")

    if source_category not in {"first_party", "third_party"}:
        raise ValueError(f"superpowers-plus entry {canonical_name} has an invalid source_category")
    if content_mode not in {"verbatim", "adapted"}:
        raise ValueError(f"superpowers-plus entry {canonical_name} has an invalid content_mode")
    if not isinstance(canonical_source_path, str) or not canonical_source_path:
        raise ValueError(f"superpowers-plus entry {canonical_name} is missing canonical_source_path")
    if not isinstance(local_path, str) or not local_path:
        raise ValueError(f"superpowers-plus entry {canonical_name} is missing local_path")

    overlay_root = _entry_overlay_root(entry)
    if source_category == "third_party" and content_mode == "adapted":
        if overlay_root is None:
            raise ValueError(f"superpowers-plus adapted entry {canonical_name} requires adaptation_overlay_path")
    elif overlay_root is not None:
        raise ValueError(f"superpowers-plus verbatim entry {canonical_name} must not declare adaptation_overlay_path")


def _materialize_entry(entry: dict[str, Any], *, write: bool) -> None:
    source_root = (ROOT / str(entry["canonical_source_path"])).resolve()
    destination_root = (PROJECTION_ROOT / str(entry["local_path"])).resolve()
    overlay_root = _entry_overlay_root(entry)
    if write:
        apply_overlay_tree(source_root, overlay_root, destination_root)
        return

    expected_root, tempdir = stage_overlay_tree(source_root, overlay_root)
    try:
        if not destination_root.exists():
            raise FileNotFoundError(destination_root)
        expected_files = sorted(path.relative_to(expected_root).as_posix() for path in expected_root.rglob("*") if path.is_file())
        actual_files = sorted(path.relative_to(destination_root).as_posix() for path in destination_root.rglob("*") if path.is_file())
        if expected_files != actual_files:
            raise ValueError(
                f"superpowers-plus projection mismatch for {entry['canonical_name']}: file inventory differs from reconstruction"
            )
        for rel_path in expected_files:
            expected_bytes = (expected_root / rel_path).read_bytes()
            actual_bytes = (destination_root / rel_path).read_bytes()
            if expected_bytes != actual_bytes:
                raise ValueError(
                    f"superpowers-plus projection mismatch for {entry['canonical_name']}: file content differs at {rel_path}"
                )
    finally:
        tempdir.cleanup()


def reconcile_superpowers_projection(*, write: bool) -> None:
    bundle_manifest = _load_bundle_manifest()
    entries = bundle_manifest.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError("superpowers-plus bundle manifest entries must be a non-empty list")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("superpowers-plus bundle manifest entries must contain objects")
        _validate_entry(entry)
        _materialize_entry(entry, write=write)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize or validate the Superpowers+ Codex projection")
    parser.add_argument("--check", action="store_true", help="validate the current projection without writing")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    reconcile_superpowers_projection(write=not args.check)
    if args.check:
        print("OK superpowers-plus projection: codex-marketplace/plugins/superpowers-plus/skills")
    else:
        print("OK superpowers-plus projection materialized: codex-marketplace/plugins/superpowers-plus/skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
