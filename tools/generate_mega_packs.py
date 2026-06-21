#!/usr/bin/env python3
"""Generate mega-pack manifests from the union of plugin entries by custody root."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_plugin_root_inventory, load_json

REGISTRY_PATH = ROOT / "codex-marketplace/custody-mega-pack-registry.json"
SKIP_CONTENT_MODES = {"blocked", "skipped"}


def load_mega_pack_registry() -> list[dict[str, Any]]:
    registry = load_json(REGISTRY_PATH)
    if registry.get("schema_version") != 1:
        raise ValueError(f"{REGISTRY_PATH}: schema_version must be 1")
    mappings = registry.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError(f"{REGISTRY_PATH}: mappings must be a non-empty list")
    return mappings


def load_plugin_manifest(plugin_root: Path) -> dict[str, Any] | None:
    manifest_path = plugin_root / "references" / "bundle-manifest.json"
    if not manifest_path.exists():
        return None
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        return None
    if "entries" not in manifest:
        return None
    return manifest


def collect_entries_by_family(plugin_manifests: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Collect all active entries from all plugin manifests, grouped by source_family."""
    by_family: dict[str, list[dict[str, Any]]] = {}
    for manifest in plugin_manifests:
        entries = manifest.get("entries", [])
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("content_mode") in SKIP_CONTENT_MODES:
                continue
            family = entry.get("source_family")
            if not family:
                continue
            by_family.setdefault(family, []).append(entry)
    return by_family


def generate_mega_pack_manifest(
    *, mega_pack_name: str, mega_pack_root: str, source_family: str, entries: list[dict[str, Any]],
    existing_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a mega-pack manifest from collected entries.

    If ``existing_manifest`` is provided, entries from it that have a
    *different* ``source_family`` than ``source_family`` are preserved
    as curated cross-family projections (e.g. first-party skills projected
    into the superpowers-plus mega-pack).  Entries with the matching
    ``source_family`` are fully replaced by the generated set.
    """
    # Deduplicate generated entries by canonical_name
    seen: dict[str, dict[str, Any]] = {}
    for entry in entries:
        name = entry.get("canonical_name")
        if not name:
            continue
        if name not in seen:
            mega_entry = dict(entry)
            mega_entry["local_path"] = f"skills/{name}"
            seen[name] = mega_entry

    # Preserve curated cross-family entries from the existing manifest
    curated_families: set[str] = set()
    if existing_manifest is not None:
        for entry in existing_manifest.get("entries", []):
            if not isinstance(entry, dict):
                continue
            ef = entry.get("source_family")
            if ef and ef != source_family and entry.get("content_mode") not in SKIP_CONTENT_MODES:
                name = entry.get("canonical_name")
                if name and name not in seen:
                    mega_entry = dict(entry)
                    mega_entry["local_path"] = f"skills/{name}"
                    seen[name] = mega_entry
                    curated_families.add(ef)

    all_families = sorted([source_family] + list(curated_families))
    return {
        "bundle_name": mega_pack_name,
        "bundle_version": "1.0.0",
        "bundle_type": "projection-lane",
        "plugin_root": mega_pack_root,
        "is_mega_pack": True,
        "mega_pack_for": source_family,
        "source_families": all_families,
        "entries": sorted(seen.values(), key=lambda e: e["canonical_name"]),
        "notes": [
            f"Auto-generated mega-pack manifest for the {source_family} custody root.",
            "Curated cross-family entries are preserved from the prior manifest.",
            "Regenerate with: py -3 tools/generate_mega_packs.py",
        ],
        "plugin_author": "Harley Bartles",
        "plugin_license": "MIT",
    }


def generate_all_mega_packs(*, write: bool) -> None:
    registry = load_mega_pack_registry()
    inventory = load_plugin_root_inventory()

    # Load ALL plugin manifests (including mega-packs) so that entries
    # declared directly in a mega-pack's own manifest are preserved when
    # that mega-pack is regenerated.  Mega-pack entries are still
    # deduplicated by canonical_name in generate_mega_pack_manifest.
    plugin_manifests: list[dict[str, Any]] = []
    for spec in inventory:
        plugin_root = ROOT / spec["plugin_root"]
        manifest = load_plugin_manifest(plugin_root)
        if manifest is None:
            continue
        plugin_manifests.append(manifest)

    by_family = collect_entries_by_family(plugin_manifests)

    for mapping in registry:
        family = mapping["source_family"]
        mega_name = mapping["mega_pack"]
        mega_root = mapping["mega_pack_root"]
        entries = by_family.get(family, [])
        if not entries:
            # No normalized entries for this family yet (topical plugins
            # still use legacy shapes).  Skip — do not clobber the existing
            # manifest with an empty generated one.
            print(f"SKIP {mega_name}: no normalized entries for family '{family}' yet")
            continue
        manifest_path = ROOT / mega_root / "references" / "bundle-manifest.json"
        existing_manifest: dict[str, Any] | None = None
        if manifest_path.exists():
            try:
                existing_manifest = load_json(manifest_path)
            except Exception:
                existing_manifest = None
        manifest = generate_mega_pack_manifest(
            mega_pack_name=mega_name,
            mega_pack_root=mega_root,
            source_family=family,
            entries=entries,
            existing_manifest=existing_manifest,
        )
        if write:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            with manifest_path.open("w", encoding="utf-8", newline="\n") as f:
                json.dump(manifest, f, indent=2)
                f.write("\n")
            print(f"Wrote {manifest_path.relative_to(ROOT)}")
        else:
            if not manifest_path.exists():
                raise FileNotFoundError(f"mega-pack manifest missing: {manifest_path}")
            existing = load_json(manifest_path)
            if existing != manifest:
                raise ValueError(
                    f"mega-pack manifest stale: {manifest_path}\n"
                    f"Run: py -3 tools/generate_mega_packs.py"
                )
            print(f"OK mega-pack manifest current: {manifest_path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate mega-pack manifests")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()
    generate_all_mega_packs(write=not args.check)
    if args.check:
        print("OK mega-packs: all mega-pack manifests validated")
    else:
        print("OK mega-packs: all mega-pack manifests generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
