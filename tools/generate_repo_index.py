#!/usr/bin/env python3
"""Generate or validate the repo navigation index from marketplace surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import (
    MARKETPLACE_PLUGIN_SPECS,
    REPO_INDEX_PATH,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO_INDEX: dict[str, Any] = {
    "schema_version": 1,
    "repo_name": "agent-asset-marketplace",
    "description": (
        "Navigation metadata for the agent asset marketplace. "
        "This file is an index of repo zones and marketplace plugin packs, "
        "not the source of truth itself."
    ),
    "marketplace_root_inventory_path": "codex-marketplace/plugin-roots.json",
    "marketplace_registry_path": ".agents/plugins/marketplace.json",
    "codex_marketplace_manifest_path": "codex-marketplace/manifest.json",
    "validation": {
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "repo_index_generate": "py -3 tools/generate_repo_index.py --apply",
        "marketplace_generate": "py -3 tools/generate_marketplace.py --apply",
        "marketplace_check": "py -3 tools/generate_marketplace.py --check",
        "repo_index_check": "py -3 tools/generate_repo_index.py --check",
    },
    "zones": [
        {
            "name": "runtime-registry",
            "path": ".agents/plugins",
            "purpose": "Runtime-facing plugin registry consumed by Codex tooling.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": None,
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "codex-marketplace-root",
            "path": "codex-marketplace",
            "purpose": "Codex marketplace source root and export manifest surface.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": ".devin/rules/codex-marketplace.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "marketplace-root-inventory",
            "path": "codex-marketplace/plugin-roots.json",
            "purpose": "Editable active marketplace plugin root inventory for manifest and validator generation.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": None,
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "codex-marketplace-plugins",
            "path": "codex-marketplace/plugins",
            "purpose": "Protected active Codex marketplace plugin pack roots and their packaging metadata.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": ".devin/rules/codex-plugins.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "provenance",
            "path": "provenance",
            "purpose": "Retained provenance notes, trust records, and custody evidence.",
            "surface_kind": "provenance",
            "nearest_scoped_agents_md": ".devin/rules/provenance.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "docs-unslop-profile",
            "path": ".agents/docs/unslop/profile.md",
            "purpose": "Canonical repo unslop profile for anti-slop custody and discovery.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".devin/rules/docs.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-plans",
            "path": ".agents/plans",
            "purpose": "Superpowers plan drafts and execution plans.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".devin/rules/plans.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-specs",
            "path": ".agents/specs",
            "purpose": "Superpowers design specs. Specs are repo-resident, tracked, and indexed alongside plans.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".agents/runbooks/design.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "tools",
            "path": "tools",
            "purpose": "Repository validation and generation scripts.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".devin/rules/tools.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
    ],
}


def _plugin_entry(spec: dict[str, Any]) -> dict[str, Any]:
    plugin_root = spec["plugin_root"]
    return {
        "name": spec["name"],
        "category": spec["category"],
        "plugin_root": plugin_root,
        "plugin_manifest": f"{plugin_root}/.codex-plugin/plugin.json",
        "source_md": f"{plugin_root}/SOURCE.md",
        "bundle_manifest": f"{plugin_root}/references/bundle-manifest.json",
        "skills_path": f"{plugin_root}/skills",
        "agents_md": None,
        "registry_path": spec["registry_path"],
        "registry_alignment": {
            "status": "aligned",
            "note": None,
        },
    }


def build_repo_index() -> dict[str, Any]:
    repo_index = dict(DEFAULT_REPO_INDEX)
    repo_index["marketplace_plugins"] = [_plugin_entry(spec) for spec in MARKETPLACE_PLUGIN_SPECS]
    return repo_index


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the repo index. (mixed)")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--apply", action="store_true", help="write the repo index")
    args = parser.parse_args(argv)

    repo_index = build_repo_index()
    rendered = json.dumps(repo_index, indent=2, ensure_ascii=False) + "\n"

    if args.apply:
        _write_json(REPO_INDEX_PATH, repo_index)
        print(f"Wrote {REPO_INDEX_PATH.relative_to(ROOT)}")
        print("OK repo index: generated")
        return 0

    if not REPO_INDEX_PATH.exists():
        raise FileNotFoundError(REPO_INDEX_PATH)
    current = REPO_INDEX_PATH.read_text(encoding="utf-8")
    if current != rendered:
        stale_path = REPO_INDEX_PATH.relative_to(ROOT)
        raise ValueError(f"{stale_path} is stale; run py -3 tools/generate_repo_index.py --apply")
    print(f"OK {REPO_INDEX_PATH.relative_to(ROOT)}")
    print("OK repo index: current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
