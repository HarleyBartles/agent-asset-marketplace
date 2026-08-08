#!/usr/bin/env python3
"""Generate the local Codex marketplace registry export."""

from __future__ import annotations

import argparse
import json

from marketplace_utils import (
    ROOT,
    CODEX_MARKETPLACE_MANIFEST_PATH,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    build_marketplace_manifest,
    load_json,
)


def _render_manifest(manifest: dict) -> str:
    return json.dumps(manifest, indent=2) + "\n"


def _check_freshness(path, expected_text: str) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    current_text = path.read_text(encoding="utf-8")
    if current_text != expected_text:
        raise ValueError(f"{path.relative_to(ROOT)} is stale; run py -3 tools/generate_marketplace.py --apply")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the Codex marketplace export. (mixed)")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--apply", action="store_true", help="write the marketplace manifest")
    args = parser.parse_args(argv)

    plugin_manifests = [load_json(spec["manifest_path"]) for spec in MARKETPLACE_PLUGIN_SPECS]

    expected = build_marketplace_manifest(plugin_manifests)
    if expected != EXPECTED_MARKETPLACE:
        raise ValueError("Unexpected marketplace manifest shape")

    rendered = _render_manifest(expected)
    if args.apply:
        MARKETPLACE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with MARKETPLACE_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)

        CODEX_MARKETPLACE_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CODEX_MARKETPLACE_MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)

        print(f"Wrote {MARKETPLACE_PATH.relative_to(ROOT)}")
        print(f"Wrote {CODEX_MARKETPLACE_MANIFEST_PATH.relative_to(ROOT)}")
        return 0

    _check_freshness(MARKETPLACE_PATH, rendered)
    _check_freshness(CODEX_MARKETPLACE_MANIFEST_PATH, rendered)
    print(f"OK {MARKETPLACE_PATH.relative_to(ROOT)}")
    print(f"OK {CODEX_MARKETPLACE_MANIFEST_PATH.relative_to(ROOT)}")
    print("OK marketplace: .agents/plugins/marketplace.json and codex-marketplace/manifest.json are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
