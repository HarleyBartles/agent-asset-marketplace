#!/usr/bin/env python3
"""Generate source-map.md files from bundle manifests.

Reads each plugin's ``references/bundle-manifest.json`` and derives a
``references/source-map.md`` markdown table from the manifest entries.

Use ``--check`` to validate that committed source maps are current
without writing.  The check exits non-zero on drift.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_plugin_root_inventory, load_json

SKIP_CONTENT_MODES = {"blocked", "skipped"}

COLUMNS = ("Skill", "Source category", "Content mode", "Canonical source path", "Local path", "Notes")


def _format_cell(value: Any) -> str:
    """Format a cell value, wrapping non-empty strings in backticks."""
    if value is None:
        return ""
    text = str(value)
    if not text:
        return ""
    return f"`{text}`"


def _entry_notes(entry: dict[str, Any]) -> str:
    """Build the Notes column from optional manifest fields."""
    parts: list[str] = []
    provenance_note = entry.get("provenance_note")
    if provenance_note:
        parts.append(provenance_note)
    adaptation_note = entry.get("adaptation_note")
    if adaptation_note:
        parts.append(f"Adaptation: {adaptation_note}")
    return " ".join(parts)


def _full_local_path(plugin_root: str, local_path: str | None) -> str | None:
    """Resolve a relative local_path to a full repo-relative path."""
    if not local_path:
        return None
    return f"{plugin_root}/{local_path}"


def generate_source_map(manifest: dict[str, Any], plugin_root: str) -> str:
    """Build the source-map.md content from a bundle manifest."""
    bundle_name = manifest.get("bundle_name", plugin_root)
    manifest_ref = f"{plugin_root}/references/bundle-manifest.json"

    title = bundle_name.replace("-", " ").replace("_", " ").title()
    if not title.endswith(" Source Map"):
        title = f"{title} Source Map"

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated from `{manifest_ref}`.")
    lines.append("")

    entries = manifest.get("entries", [])
    if not isinstance(entries, list):
        entries = []

    rows: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        content_mode = entry.get("content_mode")
        if content_mode in SKIP_CONTENT_MODES:
            continue
        canonical_name = entry.get("canonical_name", "")
        source_category = entry.get("source_category", "")
        canonical_source_path = entry.get("canonical_source_path")
        local_path = _full_local_path(plugin_root, entry.get("local_path"))
        notes = _entry_notes(entry)
        rows.append({
            "Skill": canonical_name,
            "Source category": source_category,
            "Content mode": content_mode or "",
            "Canonical source path": canonical_source_path or "",
            "Local path": local_path or "",
            "Notes": notes,
        })

    rows.sort(key=lambda r: r["Skill"])

    # Table header
    header_cells = " | ".join(COLUMNS)
    separator_cells = " | ".join("---" for _ in COLUMNS)
    lines.append(f"| {header_cells} |")
    lines.append(f"| {separator_cells} |")

    for row in rows:
        cells = [
            row["Skill"],
            row["Source category"],
            row["Content mode"],
            _format_cell(row["Canonical source path"]),
            _format_cell(row["Local path"]),
            row["Notes"],
        ]
        lines.append("| " + " | ".join(cells) + " |")

    lines.append("")
    return "\n".join(lines)


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

        source_map = generate_source_map(manifest, spec["plugin_root"])
        output_path = plugin_root / "references" / "source-map.md"

        if write:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(source_map, encoding="utf-8", newline="\n")
            written.append(str(output_path.relative_to(ROOT)))
            print(f"WROTE {output_path.relative_to(ROOT)}")
        else:
            if not output_path.exists():
                stale.append(str(output_path.relative_to(ROOT)))
                print(f"STALE {output_path.relative_to(ROOT)} (missing)")
                continue
            existing = output_path.read_text(encoding="utf-8")
            if existing != source_map:
                stale.append(str(output_path.relative_to(ROOT)))
                print(f"STALE {output_path.relative_to(ROOT)} (drift)")
            else:
                current.append(str(output_path.relative_to(ROOT)))
                print(f"OK    {output_path.relative_to(ROOT)}")

    if write:
        print(f"\nOK source maps: {len(written)} file(s) written")
    else:
        if stale:
            print(f"\nFAIL source maps: {len(stale)} stale file(s):")
            for path in stale:
                print(f"  {path}")
            print("Run: py -3 tools/generate_source_maps.py")
            return 1
        print(f"\nOK source maps: {len(current)} file(s) current")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate source-map.md files")
    parser.add_argument("--check", action="store_true", help="validate without writing; fail on drift")
    args = parser.parse_args()
    return run(write=not args.check)


if __name__ == "__main__":
    raise SystemExit(main())
