#!/usr/bin/env python3
"""Generate provenance-map.json files from bundle manifests.

Reads each plugin's ``references/bundle-manifest.json`` and derives a
``references/provenance-map.json`` that splits the manifest entries into
``source_backed_projections`` and ``adapted_projections`` lanes.

Use ``--check`` to validate that committed provenance maps are current
without writing.  The check exits non-zero on drift.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_plugin_root_inventory, load_json

SKIP_CONTENT_MODES = {"blocked", "skipped"}


def _classify_entry(entry: dict[str, Any]) -> str | None:
    """Return the provenance lane for *entry* or ``None`` to skip."""
    content_mode = entry.get("content_mode")
    if content_mode in SKIP_CONTENT_MODES:
        return None
    if content_mode in ("normalised", "adapted"):
        return "adapted"
    source_category = entry.get("source_category")
    if source_category == "first_party" or content_mode == "verbatim":
        return "source_backed"
    # Warn about unknown content_mode to avoid silent drift
    canonical_name = entry.get("canonical_name", "<unknown>")
    print(f"WARNING: entry {canonical_name} has unknown content_mode: {content_mode}, skipping provenance map")
    return None


def _project_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Project a manifest entry into the provenance-map subset."""
    projected: dict[str, Any] = {
        "canonical_name": entry.get("canonical_name"),
        "source_category": entry.get("source_category"),
        "content_mode": entry.get("content_mode"),
        "canonical_source_path": entry.get("canonical_source_path"),
        "local_path": entry.get("local_path"),
    }
    adaptation_overlay_path = entry.get("adaptation_overlay_path")
    if adaptation_overlay_path:
        projected["adaptation_overlay_path"] = adaptation_overlay_path
    return projected


def generate_provenance_map(manifest: dict[str, Any]) -> dict[str, Any]:
    """Build the provenance-map payload from a bundle manifest."""
    source_backed: list[dict[str, Any]] = []
    adapted: list[dict[str, Any]] = []

    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        return {"source_backed_projections": [], "adapted_projections": []}

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        lane = _classify_entry(entry)
        if lane is None:
            continue
        projected = _project_entry(entry)
        if lane == "source_backed":
            source_backed.append(projected)
        else:
            adapted.append(projected)

    source_backed.sort(key=lambda e: e.get("canonical_name") or "")
    adapted.sort(key=lambda e: e.get("canonical_name") or "")

    return {
        "source_backed_projections": source_backed,
        "adapted_projections": adapted,
    }


def _serialize(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def run(*, write: bool) -> int:
    inventory = load_plugin_root_inventory()
    stale: list[str] = []
    current: list[str] = []
    written: list[str] = []

    for spec in inventory:
        plugin_root = ROOT / spec["plugin_root"]
        manifest_path = plugin_root / "references" / "bundle-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = load_json(manifest_path)
        if not isinstance(manifest, dict) or not isinstance(manifest.get("entries"), list):
            print(f"SKIP {spec['name']}: manifest has no entries[]")
            continue

        provenance_map = generate_provenance_map(manifest)
        output_path = plugin_root / "references" / "provenance-map.json"
        serialized = _serialize(provenance_map)

        if write:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(serialized, encoding="utf-8", newline="\n")
            written.append(str(output_path.relative_to(ROOT)))
            print(f"WROTE {output_path.relative_to(ROOT)}")
        else:
            if not output_path.exists():
                stale.append(str(output_path.relative_to(ROOT)))
                print(f"STALE {output_path.relative_to(ROOT)} (missing)")
                continue
            existing = output_path.read_text(encoding="utf-8")
            if existing != serialized:
                stale.append(str(output_path.relative_to(ROOT)))
                print(f"STALE {output_path.relative_to(ROOT)} (drift)")
            else:
                current.append(str(output_path.relative_to(ROOT)))
                print(f"OK    {output_path.relative_to(ROOT)}")

    if write:
        print(f"\nOK provenance maps: {len(written)} file(s) written")
    else:
        if stale:
            print(f"\nFAIL provenance maps: {len(stale)} stale file(s):")
            for path in stale:
                print(f"  {path}")
            print("Run: py -3 tools/generate_provenance_maps.py")
            return 1
        print(f"\nOK provenance maps: {len(current)} file(s) current")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate provenance-map.json files")
    parser.add_argument("--check", action="store_true", help="validate without writing; fail on drift")
    args = parser.parse_args()
    return run(write=not args.check)


if __name__ == "__main__":
    raise SystemExit(main())
