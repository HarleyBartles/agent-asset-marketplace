#!/usr/bin/env python3
"""Materialize Codex marketplace projections from bundle-manifests."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_plugin_root_inventory, load_json
from skill_overlay_materializer import apply_overlay_tree, stage_overlay_tree

VALID_SOURCE_CATEGORIES = {"first_party", "third_party"}
VALID_CONTENT_MODES = {"verbatim", "normalised", "adapted"}


def _find_bundle_manifest(plugin_root: Path) -> Path | None:
    candidate = plugin_root / "references" / "bundle-manifest.json"
    return candidate if candidate.exists() else None


def _load_bundle_manifest(plugin_root: Path) -> dict[str, Any] | None:
    manifest_path = _find_bundle_manifest(plugin_root)
    if manifest_path is None:
        return None
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{manifest_path} must contain a JSON object")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return None  # Not a projection-lane plugin (e.g. legacy skills[] shape)
    # Distinguish new-schema entries (canonical_name + source_category) from
    # legacy entries (snapshot_path, no canonical_name). Only process new-schema
    # plugins; legacy-schema plugins are migrated separately.
    if entries:
        first = entries[0]
        if not isinstance(first, dict) or "canonical_name" not in first:
            return None  # Legacy schema — skip until migrated
    return manifest


def _validate_entry(entry: dict[str, Any]) -> None:
    canonical_name = entry.get("canonical_name")
    if not isinstance(canonical_name, str) or not canonical_name:
        raise ValueError(f"entry missing canonical_name: {entry}")
    source_category = entry.get("source_category")
    if source_category not in VALID_SOURCE_CATEGORIES:
        raise ValueError(f"entry {canonical_name} invalid source_category: {source_category}")
    content_mode = entry.get("content_mode")
    if content_mode not in VALID_CONTENT_MODES:
        raise ValueError(f"entry {canonical_name} invalid content_mode: {content_mode}")
    for field in ("canonical_source_path", "local_path"):
        if not isinstance(entry.get(field), str) or not entry[field]:
            raise ValueError(f"entry {canonical_name} missing {field}")
    overlay_path = entry.get("adaptation_overlay_path")
    if source_category == "first_party":
        if content_mode != "verbatim":
            raise ValueError(f"first-party entry {canonical_name} must be verbatim (fix the source, don't adapt)")
        if overlay_path is not None:
            raise ValueError(f"first-party verbatim entry {canonical_name} must not declare adaptation_overlay_path")
    else:  # third_party
        if content_mode == "verbatim":
            if overlay_path is not None:
                raise ValueError(f"verbatim entry {canonical_name} must not declare adaptation_overlay_path")
        else:  # normalised or adapted
            if not isinstance(overlay_path, str) or not overlay_path:
                raise ValueError(f"third-party {content_mode} entry {canonical_name} requires adaptation_overlay_path")


def _materialize_entry(entry: dict[str, Any], plugin_root: Path, *, write: bool) -> None:
    source_root = (ROOT / str(entry["canonical_source_path"])).resolve()
    destination_root = (plugin_root / str(entry["local_path"])).resolve()
    overlay_path = entry.get("adaptation_overlay_path")
    overlay_root = (ROOT / overlay_path).resolve() if overlay_path else None

    if write:
        apply_overlay_tree(source_root, overlay_root, destination_root)
        return

    # check mode: stage reconstruction and compare
    if not destination_root.exists():
        raise FileNotFoundError(f"projection missing for {entry['canonical_name']}: {destination_root}")
    expected_root, tempdir = stage_overlay_tree(source_root, overlay_root)
    try:
        expected_files = sorted(p.relative_to(expected_root).as_posix() for p in expected_root.rglob("*") if p.is_file())
        actual_files = sorted(p.relative_to(destination_root).as_posix() for p in destination_root.rglob("*") if p.is_file())
        if expected_files != actual_files:
            raise ValueError(f"projection mismatch for {entry['canonical_name']}: file inventory differs")
        for rel in expected_files:
            if (expected_root / rel).read_bytes() != (destination_root / rel).read_bytes():
                raise ValueError(f"projection mismatch for {entry['canonical_name']}: content differs at {rel}")
    finally:
        tempdir.cleanup()


def reconcile_projection(*, write: bool, plugin_name: str | None = None) -> None:
    inventory = load_plugin_root_inventory()
    for spec in inventory:
        if plugin_name and spec["name"] != plugin_name:
            continue
        plugin_root = ROOT / spec["plugin_root"]
        manifest = _load_bundle_manifest(plugin_root)
        if manifest is None:
            continue  # Not a projection-lane plugin
        entries = manifest["entries"]
        if not entries:
            raise ValueError(f"{spec['name']} bundle-manifest entries must be non-empty")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"{spec['name']} bundle-manifest entry must be an object")
            _validate_entry(entry)
            _materialize_entry(entry, plugin_root, write=write)


def main() -> int:
    parser = argparse.ArgumentParser(description="Materialize or validate Codex projections from bundle-manifests")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--plugin", help="target one plugin by name")
    args = parser.parse_args()
    reconcile_projection(write=not args.check, plugin_name=args.plugin)
    if args.check:
        print("OK projection: all projection-lane plugins validated")
    else:
        print("OK projection: all projection-lane plugins materialized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
