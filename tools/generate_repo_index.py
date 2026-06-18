#!/usr/bin/env python3
"""Regenerate the repo navigation index from marketplace registry surfaces."""

from __future__ import annotations

import json
from pathlib import Path

from marketplace_utils import MARKETPLACE_PATH, REPO_INDEX_PATH, load_json


ROOT = Path(__file__).resolve().parents[1]
REPO_WORKER_BASE_ENTRY = {
    "name": "repo-worker-base",
    "plugin_root": "codex-marketplace/plugins/repo-worker-base",
    "plugin_manifest": "codex-marketplace/plugins/repo-worker-base/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/repo-worker-base/SOURCE.md",
    "source_ledger": [],
    "license_path": "codex-marketplace/plugins/repo-worker-base/LICENSE",
    "bundle_manifest": None,
    "skills_path": "codex-marketplace/plugins/repo-worker-base/skills",
    "provenance_refs": ["provenance/repo-worker-base.md"],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/repo-worker-base",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}

DOTNET_KIT_ENTRY = {
    "name": "dotnet-kit",
    "plugin_root": "codex-marketplace/plugins/dotnet-kit",
    "plugin_manifest": "codex-marketplace/plugins/dotnet-kit/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/dotnet-kit/SOURCE.md",
    "source_ledger": [
        "sources/first_party/skills/dotnet-kit/decisions.json",
        "sources/first_party/skills/dotnet-kit/decisions.md",
        "sources/first_party/skills/dotnet-kit/intake.json",
    ],
    "license_path": "codex-marketplace/plugins/dotnet-kit/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/dotnet-kit/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/dotnet-kit/skills",
    "provenance_refs": [
        "provenance/dotnet-claude-kit.md",
        "codex-marketplace/plugins/dotnet-kit/references/source-map.md",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/dotnet-kit",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}

CODEX_CORTEX_ENTRY = {
    "name": "codex-cortex",
    "plugin_root": "codex-marketplace/plugins/codex-cortex",
    "plugin_manifest": "codex-marketplace/plugins/codex-cortex/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/codex-cortex/SOURCE.md",
    "source_ledger": [
        "sources/first_party/skills/codex-cortex/intake.json",
        "sources/first_party/skills/codex-cortex/decisions.json",
        "sources/first_party/skills/codex-cortex/decisions.md",
    ],
    "license_path": "codex-marketplace/plugins/codex-cortex/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/codex-cortex/skills",
    "provenance_refs": [
        "provenance/codex-cortex.md",
        "codex-marketplace/plugins/codex-cortex/references/source-map.md",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/codex-cortex",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}

API_CONTRACTS_PACK_ENTRY = {
    "name": "api-contracts-pack",
    "plugin_root": "codex-marketplace/plugins/api-contracts-pack",
    "plugin_manifest": "codex-marketplace/plugins/api-contracts-pack/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/api-contracts-pack/SOURCE.md",
    "source_ledger": [
        "sources/first_party/skills/codex-cortex/intake.json",
        "sources/first_party/skills/codex-cortex/decisions.json",
        "sources/first_party/skills/codex-cortex/decisions.md",
    ],
    "license_path": "codex-marketplace/plugins/api-contracts-pack/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/api-contracts-pack/skills",
    "provenance_refs": [
        "provenance/codex-cortex.md",
        "codex-marketplace/plugins/api-contracts-pack/references/source-map.md",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/api-contracts-pack",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}

LANGUAGE_PATTERNS_PACK_ENTRY = {
    "name": "language-patterns-pack",
    "plugin_root": "codex-marketplace/plugins/language-patterns-pack",
    "plugin_manifest": "codex-marketplace/plugins/language-patterns-pack/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/language-patterns-pack/SOURCE.md",
    "source_ledger": [
        "sources/first_party/skills/codex-cortex/intake.json",
        "sources/first_party/skills/codex-cortex/decisions.json",
        "sources/first_party/skills/codex-cortex/decisions.md",
    ],
    "license_path": "codex-marketplace/plugins/language-patterns-pack/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/language-patterns-pack/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/language-patterns-pack/skills",
    "provenance_refs": [
        "provenance/codex-cortex.md",
        "codex-marketplace/plugins/language-patterns-pack/references/source-map.md",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/language-patterns-pack",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}

SUPERPOWERS_PLUS_ENTRY = {
    "name": "superpowers-plus",
    "plugin_root": "codex-marketplace/plugins/superpowers-plus",
    "plugin_manifest": "codex-marketplace/plugins/superpowers-plus/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/superpowers-plus/SOURCE.md",
    "source_ledger": [
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
        "codex-marketplace/plugins/house-skills/skills/linear-superpowers/SKILL.md",
        "sources/first_party/skills/architecture-superpowers/SKILL.md",
    ],
    "license_path": "codex-marketplace/plugins/superpowers-plus/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/superpowers-plus/skills",
    "provenance_refs": [
        "provenance/superpowers-plus.md",
        "codex-marketplace/plugins/superpowers-plus/references/provenance-map.json",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/superpowers-plus",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}


def _normalize_zones(zones: list[dict]) -> list[dict]:
    normalized_zones: list[dict] = []
    for zone in zones:
        if not isinstance(zone, dict):
            normalized_zones.append(zone)
            continue
        if zone.get("name") == "superpowers-marketplace":
            updated_zone = dict(zone)
            updated_zone["name"] = "superpowers-plus-marketplace"
            updated_zone["path"] = "codex-marketplace/plugins/superpowers-plus"
            updated_zone["purpose"] = "Codex-facing projection of the upstream Superpowers release snapshot, renamed to Superpowers+."
            normalized_zones.append(updated_zone)
            continue
        normalized_zones.append(zone)
    return normalized_zones


def build_repo_index() -> dict:
    marketplace = load_json(MARKETPLACE_PATH)
    repo_index = load_json(REPO_INDEX_PATH)
    registry_plugins = {plugin["name"]: plugin for plugin in marketplace.get("plugins", [])}

    current_plugins = {entry["name"]: entry for entry in repo_index.get("marketplace_plugins", [])}
    ordered_plugins: list[dict] = []
    for plugin in marketplace.get("plugins", []):
        name = plugin.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("marketplace registry contains a malformed plugin name")

        if name == "dotnet-kit":
            ordered_plugins.append(dict(DOTNET_KIT_ENTRY))
            continue
        if name == "codex-cortex":
            ordered_plugins.append(dict(CODEX_CORTEX_ENTRY))
            continue
        if name == "api-contracts-pack":
            ordered_plugins.append(dict(API_CONTRACTS_PACK_ENTRY))
            continue
        if name == "language-patterns-pack":
            ordered_plugins.append(dict(LANGUAGE_PATTERNS_PACK_ENTRY))
            continue
        if name == "repo-worker-base":
            ordered_plugins.append(dict(REPO_WORKER_BASE_ENTRY))
            continue
        if name == "superpowers-plus":
            ordered_plugins.append(dict(SUPERPOWERS_PLUS_ENTRY))
            continue
        if name in current_plugins:
            ordered_plugins.append(current_plugins[name])
            continue
        raise ValueError(f"repo-index generator does not know how to synthesize marketplace plugin {name}")

    repo_index["marketplace_plugins"] = ordered_plugins
    repo_index["zones"] = _normalize_zones(list(repo_index.get("zones", [])))
    validation = dict(repo_index.get("validation", {}))
    validation["repo_index_generate"] = "py -3 tools/generate_repo_index.py"
    repo_index["validation"] = validation
    return repo_index


def main() -> int:
    repo_index = build_repo_index()
    rendered = json.dumps(repo_index, indent=2, ensure_ascii=False)
    REPO_INDEX_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(f"Wrote {REPO_INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
