#!/usr/bin/env python3
"""Generate the Adventures Pack bundle manifest from the checked-in source surface.

This keeps the project-scoped Adventures projection on the same deterministic
regen path as the rest of the marketplace surfaces.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, load_json

MANIFEST_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/references/bundle-manifest.json"
SOURCE_MD_PATH = ROOT / "codex-marketplace/plugins/adventures-pack/SOURCE.md"


def _render_manifest(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2) + "\n"


def build_expected_manifest() -> dict[str, Any]:
    if not SOURCE_MD_PATH.exists():
        raise FileNotFoundError(SOURCE_MD_PATH)
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(MANIFEST_PATH)

    manifest = load_json(MANIFEST_PATH)
    if not isinstance(manifest, dict):
        raise ValueError(f"{MANIFEST_PATH} must contain a JSON object")

    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{MANIFEST_PATH} must contain a non-empty entries list")

    expected = dict(manifest)
    expected["entries"] = entries
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the Adventures Pack bundle manifest")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()

    expected = build_expected_manifest()
    rendered = _render_manifest(expected)

    if args.check:
        current = MANIFEST_PATH.read_text(encoding="utf-8")
        if current != rendered:
            raise ValueError(f"{MANIFEST_PATH.relative_to(ROOT)} is stale; run py -3 tools/generate_adventures_pack_manifest.py")
        print(f"OK {MANIFEST_PATH.relative_to(ROOT)}")
        return 0

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
