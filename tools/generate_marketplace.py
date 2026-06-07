#!/usr/bin/env python3
"""Generate the local Codex marketplace registry export."""

from __future__ import annotations

import json

from marketplace_utils import (
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    PLUGIN_MANIFEST_PATH,
    MARKETPLACE_FAMILY_PACK_PLUGIN_MANIFEST_PATH,
    SOURCE_DECISIONS_JSON_PATH,
    SOURCE_INTAKE_JSON_PATH,
    build_marketplace_manifest,
    load_json,
)


def main() -> int:
    decisions = load_json(SOURCE_DECISIONS_JSON_PATH)
    intake = load_json(SOURCE_INTAKE_JSON_PATH)
    plugin_manifest = load_json(PLUGIN_MANIFEST_PATH)
    marketplace_family_pack_manifest = load_json(MARKETPLACE_FAMILY_PACK_PLUGIN_MANIFEST_PATH)

    imported_records = [
        record
        for record in decisions
        if record.get("source_id") and record.get("import_state", "imported") == "imported"
    ]
    if not imported_records:
        raise ValueError("No imported House Skills records found in the source ledger")

    if not intake.get("imports"):
        raise ValueError("sources/house-skills/intake.json does not contain imports")

    expected = build_marketplace_manifest([plugin_manifest, marketplace_family_pack_manifest])
    if expected != EXPECTED_MARKETPLACE:
        raise ValueError("Unexpected marketplace manifest shape")

    MARKETPLACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MARKETPLACE_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(expected, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {MARKETPLACE_PATH.relative_to(MARKETPLACE_PATH.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
