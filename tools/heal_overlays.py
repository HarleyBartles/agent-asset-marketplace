#!/usr/bin/env python3
"""Self-heal overlay.yaml line edits when source content shifts.

When source files are normalized (e.g. CRLF→LF, trailing whitespace stripped),
the ``expected_lines`` in overlay.yaml files may no longer match at the
recorded line numbers. This tool searches for the expected content at the
original line range first, then scans the rest of the source file. If the
content is found at a different location (or with minor whitespace
differences), the overlay is updated in place.

Usage:
    py -3 tools/heal_overlays.py            # heal all overlays
    py -3 tools/heal_overlays.py --check    # report drift without writing
    py -3 tools/heal_overlays.py --overlay adapters/codex/.../overlay.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ADAPTERS_ROOT = ROOT / "adapters"
OVERLAY_FILENAME = "overlay.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _save_yaml(path: Path, data: dict[str, Any]) -> None:
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=4096)
    path.write_text(text, encoding="utf-8", newline="\n")


def _find_content(
    source_lines: list[str],
    expected: list[str],
    original_start: int,
) -> tuple[int, int] | None:
    """Search for ``expected`` line sequence in ``source_lines``.

    Returns the 1-based (start, end) line range if found, else None.
    Tries the original location first, then scans the full file.
    """
    if not expected:
        return None

    needle = [line.rstrip() for line in expected]
    haystack = [line.rstrip() for line in source_lines]

    # Try original location first (1-based to 0-based)
    orig_start_0 = original_start - 1
    orig_end_0 = orig_start_0 + len(needle)
    if orig_end_0 <= len(haystack):
        if haystack[orig_start_0:orig_end_0] == needle:
            return (original_start, original_start + len(needle) - 1)

    # Scan full file for the sequence
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i : i + len(needle)] == needle:
            return (i + 1, i + len(needle))

    return None


def _heal_overlay(
    overlay_path: Path,
    source_root: Path,
    *,
    write: bool,
) -> list[str]:
    """Heal a single overlay.yaml. Returns a list of human-readable changes."""
    spec = _load_yaml(overlay_path)
    changes: list[str] = []
    edits = spec.get("edits", [])
    if not edits:
        return changes

    healed_edits: list[dict[str, Any]] = []
    edits_by_path: dict[str, list[dict[str, Any]]] = {}
    for edit in edits:
        edits_by_path.setdefault(edit["path"], []).append(edit)

    for rel_path, file_edits in edits_by_path.items():
        source_file = source_root / rel_path
        if not source_file.exists():
            changes.append(f"  WARNING: source file missing: {rel_path}")
            healed_edits.extend(file_edits)
            continue

        source_lines = source_file.read_text(encoding="utf-8").splitlines()

        for edit in file_edits:
            op = edit.get("op", "replace")
            if op in {"insert_before", "insert_after"}:
                # Anchor-based edits: heal the anchor line
                anchor = edit.get("anchor", "")
                line = edit.get("line", 0)
                healed = dict(edit)

                # Try original line first
                if 0 < line <= len(source_lines):
                    if source_lines[line - 1].rstrip() == anchor.rstrip():
                        # Exact match at original line — check if anchor needs whitespace update
                        if source_lines[line - 1] != anchor:
                            healed["anchor"] = source_lines[line - 1]
                            changes.append(
                                f"  {rel_path}:{line} anchor whitespace healed"
                            )
                        healed_edits.append(healed)
                        continue

                # Search for anchor in full file
                anchor_stripped = anchor.rstrip()
                found = False
                for i, src_line in enumerate(source_lines):
                    if src_line.rstrip() == anchor_stripped:
                        healed["line"] = i + 1
                        if src_line != anchor:
                            healed["anchor"] = src_line
                        changes.append(
                            f"  {rel_path} insert anchor moved {line}→{i+1}"
                        )
                        found = True
                        break

                if not found:
                    changes.append(f"  {rel_path} insert anchor NOT FOUND")
                healed_edits.append(healed)
                continue

            # replace / delete edits
            start_line = edit.get("start_line", 0)
            end_line = edit.get("end_line", 0)
            expected_lines = edit.get("expected_lines", [])
            healed = dict(edit)

            if not expected_lines:
                healed_edits.append(healed)
                continue

            # Check if expected_lines match at original location (exact)
            orig_start_0 = start_line - 1
            orig_end_0 = end_line
            if orig_end_0 <= len(source_lines):
                orig_slice = source_lines[orig_start_0:orig_end_0]
                if orig_slice == expected_lines:
                    # Exact match — no healing needed
                    healed_edits.append(healed)
                    continue

            # Search for content (whitespace-insensitive)
            found = _find_content(source_lines, expected_lines, start_line)
            if found is None:
                changes.append(
                    f"  {rel_path} {start_line}-{end_line} content NOT FOUND — manual fix needed"
                )
                healed_edits.append(healed)
                continue

            new_start, new_end = found
            # Get the exact source lines at the found location (with original whitespace)
            exact_lines = source_lines[new_start - 1 : new_end]

            if new_start != start_line or new_end != end_line:
                changes.append(
                    f"  {rel_path} lines healed {start_line}-{end_line}→{new_start}-{new_end}"
                )
                healed["start_line"] = new_start
                healed["end_line"] = new_end

            # Update expected_lines to exact source content (handles whitespace normalization)
            if exact_lines != expected_lines:
                healed["expected_lines"] = exact_lines
                if new_start == start_line and new_end == end_line:
                    changes.append(
                        f"  {rel_path}:{start_line} expected_lines whitespace healed"
                    )

            # Check if the edit is now a no-op (replace with identical content)
            replace_lines = edit.get("replace_lines", [])
            if op == "replace" and replace_lines == exact_lines:
                changes.append(
                    f"  {rel_path}:{new_start} replace is now a no-op — removing"
                )
                continue  # Skip this edit entirely

            healed_edits.append(healed)

    if changes:
        spec["edits"] = healed_edits
        if write:
            _save_yaml(overlay_path, spec)

    return changes


def _discover_overlays() -> list[tuple[Path, Path]]:
    """Discover all overlay.yaml files and their source roots.

    Returns list of (overlay_path, source_root) pairs.
    """
    results: list[tuple[Path, Path]] = []
    for overlay_path in sorted(ADAPTERS_ROOT.rglob(OVERLAY_FILENAME)):
        spec = _load_yaml(overlay_path)
        metadata = spec.get("metadata", {})
        source_category = metadata.get("source_category", "")
        if source_category != "third_party":
            continue

        # Find the source root from the bundle manifest
        # The overlay's metadata has adaptation_overlay and projection_plugin
        # We need to find the matching bundle manifest entry to get canonical_source_path
        overlay_rel = overlay_path.relative_to(ROOT).as_posix()
        source_root = _find_source_root_for_overlay(overlay_rel)
        if source_root is None:
            # Try to infer from the overlay directory structure
            # adapters/codex/<pack>/<skill>/overlay.yaml
            # source is typically sources/third_party/<upstream>/upstream/skills/<skill>
            parts = overlay_path.relative_to(ADAPTERS_ROOT).parts
            if len(parts) >= 3:
                skill_name = parts[-2]
                # Search for this skill in third_party sources
                for candidate in (ROOT / "sources/third_party").rglob(f"skills/{skill_name}"):
                    if candidate.is_dir():
                        source_root = candidate
                        break

        if source_root is None:
            print(f"  WARNING: could not find source root for {overlay_rel}")
            continue

        results.append((overlay_path, source_root))

    return results


def _find_source_root_for_overlay(overlay_rel: str) -> Path | None:
    """Find the source root for an overlay by searching bundle manifests."""
    for manifest_path in (ROOT / "codex-marketplace/plugins").rglob("bundle-manifest.json"):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for entry in manifest.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("adaptation_overlay_path") == overlay_rel:
                csp = entry.get("canonical_source_path")
                if csp:
                    source_root = ROOT / csp
                    if source_root.is_dir():
                        return source_root
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Self-heal overlay.yaml line edits when source content shifts")
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    parser.add_argument("--overlay", type=str, help="heal a specific overlay.yaml (relative path)")
    args = parser.parse_args()

    write = not args.check

    if args.overlay:
        overlay_path = ROOT / args.overlay
        if not overlay_path.exists():
            print(f"ERROR: overlay not found: {overlay_path}")
            return 1
        source_root = _find_source_root_for_overlay(args.overlay)
        if source_root is None:
            # Try inference
            parts = overlay_path.relative_to(ADAPTERS_ROOT).parts
            if len(parts) >= 3:
                skill_name = parts[-2]
                for candidate in (ROOT / "sources/third_party").rglob(f"skills/{skill_name}"):
                    if candidate.is_dir():
                        source_root = candidate
                        break
        if source_root is None:
            print(f"ERROR: could not find source root for {args.overlay}")
            return 1
        overlays = [(overlay_path, source_root)]
    else:
        overlays = _discover_overlays()

    total_changes = 0
    for overlay_path, source_root in overlays:
        overlay_rel = overlay_path.relative_to(ROOT).as_posix()
        changes = _heal_overlay(overlay_path, source_root, write=write)
        if changes:
            total_changes += len(changes)
            print(f"\n{overlay_rel}:")
            for change in changes:
                print(change)

    if total_changes == 0:
        print("OK all overlays healthy")
        return 0

    mode = "healed" if write else "would heal"
    print(f"\n{total_changes} change(s) {mode} across {len(overlays)} overlay(s)")
    return 0 if write else 1


if __name__ == "__main__":
    raise SystemExit(main())
