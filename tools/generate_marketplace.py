#!/usr/bin/env python3
"""Generate the local Codex marketplace registry export."""

from __future__ import annotations

import json

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    SOURCE_DECISIONS_JSON_PATH,
    SOURCE_INTAKE_JSON_PATH,
    build_marketplace_manifest,
    load_json,
)


def main() -> int:
    decisions = load_json(SOURCE_DECISIONS_JSON_PATH)
    intake = load_json(SOURCE_INTAKE_JSON_PATH)
    plugin_manifests = [load_json(spec["manifest_path"]) for spec in MARKETPLACE_PLUGIN_SPECS]

    imported_records = [
        record
        for record in decisions
        if record.get("source_id") and record.get("import_state", "imported") == "imported"
    ]
    if not imported_records:
        raise ValueError("No imported House Skills records found in the source ledger")

    if not intake.get("imports"):
        raise ValueError("sources/first_party/skills/house-skills/intake.json does not contain imports")

    expected = build_marketplace_manifest(plugin_manifests)
    if expected != EXPECTED_MARKETPLACE:
        raise ValueError("Unexpected marketplace manifest shape")

    MARKETPLACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MARKETPLACE_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(expected, handle, indent=2)
        handle.write("\n")

    CODEX_MARKETPLACE_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CODEX_MARKETPLACE_MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(expected, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {MARKETPLACE_PATH.relative_to(MARKETPLACE_PATH.parents[2])}")
    print(f"Wrote {CODEX_MARKETPLACE_MANIFEST_PATH.relative_to(CODEX_MARKETPLACE_MANIFEST_PATH.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
