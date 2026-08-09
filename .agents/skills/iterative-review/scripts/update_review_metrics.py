#!/usr/bin/env python3
"""Safely update review-metrics.json from the command line. (mutating)

This script exists to avoid the editor-buffer race that happens when the
`write` tool and the iterative-review scripts both touch `review-metrics.json`.
It reads the current file, applies the requested patch, and writes it back
without opening it in the IDE.

Contract:
- --help   prints usage and exits 0
- --check  reports whether the script is in a runnable state and exits 0
- --apply  applies the patch to review-metrics.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    # Strip a UTF-8 BOM if present so json.loads is happy.
    if text.startswith("\ufeff"):
        text = text[1:]
    return json.loads(text)


def _save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _merge(base: dict, patch: dict) -> dict:
    """Shallow merge patch into base, then recurse for dict values."""
    for key, value in patch.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            base[key] = _merge(base[key], value)
        else:
            base[key] = value
    return base


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Patch review-metrics.json safely. (mutating)")
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--apply", action="store_true", help="apply the patch to the metrics file")
    parser.add_argument("--metrics", help="Path to review-metrics.json")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--patch-file", help="JSON file containing the patch to apply")
    group.add_argument("--patch", help="JSON string containing the patch to apply")
    args = parser.parse_args(argv)

    if args.check:
        print("update_review_metrics.py is ready")
        return 0

    if not args.apply:
        print("--apply is required to modify review-metrics.json", file=sys.stderr)
        return 2

    if not args.patch_file and not args.patch:
        print("--patch-file or --patch is required with --apply", file=sys.stderr)
        return 2

    metrics_path = Path(args.metrics)
    if not metrics_path.is_file():
        print(f"ERROR: metrics file not found: {metrics_path}", file=sys.stderr)
        return 1

    patch_text = Path(args.patch_file).read_text(encoding="utf-8-sig") if args.patch_file else args.patch
    try:
        patch = json.loads(patch_text)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid patch JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(patch, dict):
        print("ERROR: patch must be a JSON object", file=sys.stderr)
        return 1

    data = _load(metrics_path)
    data = _merge(data, patch)
    _save(metrics_path, data)
    print(f"OK: updated {metrics_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
