#!/usr/bin/env python3
"""Regenerate the repo navigation index from marketplace registry surfaces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from marketplace_utils import MARKETPLACE_PATH, MARKETPLACE_PLUGIN_SPECS, REPO_INDEX_PATH, load_json


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
        "sources/first_party/skills/ecc-superpowers/SKILL.md",
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

SUPERPOWERS_ECC_ENTRY = {
    "name": "superpowers-ecc",
    "plugin_root": "codex-marketplace/plugins/superpowers-ecc",
    "plugin_manifest": "codex-marketplace/plugins/superpowers-ecc/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/superpowers-ecc/SOURCE.md",
    "source_ledger": [
        "sources/third_party/ecc/upstream/LICENSE",
        "sources/third_party/ecc/upstream/source-custody.md",
    ],
    "license_path": "codex-marketplace/plugins/superpowers-ecc/LICENSE",
    "bundle_manifest": "codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json",
    "skills_path": "codex-marketplace/plugins/superpowers-ecc/skills",
    "provenance_refs": [
        "provenance/superpowers-ecc.md",
        "codex-marketplace/plugins/superpowers-ecc/references/source-map.md",
    ],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/superpowers-ecc",
    "registry_alignment": {
        "status": "aligned",
        "note": None,
    },
}


def _bundle_manifest_path(plugin_root: str) -> Path:
    return ROOT / plugin_root / "references" / "bundle-manifest.json"


def _load_bundle_manifest(plugin_root: str) -> dict[str, Any] | None:
    path = _bundle_manifest_path(plugin_root)
    if not path.exists():
        return None
    bundle_manifest = load_json(path)
    if not isinstance(bundle_manifest, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return bundle_manifest


def _plugin_manifest_path(plugin_manifest: Path) -> str:
    return plugin_manifest.relative_to(ROOT).as_posix()


def _default_skills_path(plugin_root: str, plugin_manifest: dict[str, Any]) -> str:
    skills = plugin_manifest.get("skills")
    if not isinstance(skills, str) or not skills.strip():
        raise ValueError(f"{plugin_root} plugin manifest is missing a skills path")
    return (Path(plugin_root) / Path(skills)).as_posix()


def _metadata_driven_plugin_entry(
    plugin: dict[str, Any],
    *,
    current_entry: dict[str, Any] | None,
    plugin_manifest: dict[str, Any],
    bundle_manifest: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if bundle_manifest is None:
        return None
    repo_index = bundle_manifest.get("repo_index")
    if not isinstance(repo_index, dict):
        return None

    plugin_root = plugin["plugin_root"]
    entry = dict(current_entry or {})
    entry["name"] = plugin["name"]
    entry["plugin_root"] = plugin_root
    entry["plugin_manifest"] = _plugin_manifest_path(plugin["manifest_path"])
    entry["source_md"] = repo_index.get("source_md") or entry.get("source_md") or f"{plugin_root}/SOURCE.md"
    entry["source_ledger"] = list(repo_index.get("source_ledger", entry.get("source_ledger", [])))
    entry["license_path"] = repo_index.get("license_path") or entry.get("license_path") or f"{plugin_root}/LICENSE"
    entry["bundle_manifest"] = repo_index.get("bundle_manifest") or f"{plugin_root}/references/bundle-manifest.json"
    entry["skills_path"] = repo_index.get("skills_path") or entry.get("skills_path") or _default_skills_path(
        plugin_root, plugin_manifest
    )
    entry["provenance_refs"] = list(repo_index.get("provenance_refs", entry.get("provenance_refs", [])))
    entry["agents_md"] = repo_index.get("agents_md", entry.get("agents_md"))
    entry["registry_path"] = plugin["registry_path"]
    entry["registry_alignment"] = dict(
        repo_index.get(
            "registry_alignment",
            entry.get("registry_alignment", {"status": "aligned", "note": None}),
        )
    )
    return entry


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
    plugin_specs_by_name = {spec["name"]: spec for spec in MARKETPLACE_PLUGIN_SPECS}

    current_plugins = {entry["name"]: entry for entry in repo_index.get("marketplace_plugins", [])}
    ordered_plugins: list[dict] = []
    for plugin in marketplace.get("plugins", []):
        name = plugin.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError("marketplace registry contains a malformed plugin name")

        if name in current_plugins:
            spec = plugin_specs_by_name.get(name)
            if spec is None:
                raise ValueError(f"repo-index generator does not know how to synthesize marketplace plugin {name}")
            plugin_manifest = load_json(spec["manifest_path"])
            if not isinstance(plugin_manifest, dict):
                raise ValueError(f"{spec['manifest_path']} must contain a JSON object")
            bundle_manifest = _load_bundle_manifest(spec["plugin_root"])
            metadata_entry = _metadata_driven_plugin_entry(
                spec,
                current_entry=current_plugins[name],
                plugin_manifest=plugin_manifest,
                bundle_manifest=bundle_manifest,
            )
            ordered_plugins.append(metadata_entry or current_plugins[name])
            continue
        spec = plugin_specs_by_name.get(name)
        if spec is None:
            raise ValueError(f"repo-index generator does not know how to synthesize marketplace plugin {name}")
        plugin_manifest = load_json(spec["manifest_path"])
        if not isinstance(plugin_manifest, dict):
            raise ValueError(f"{spec['manifest_path']} must contain a JSON object")
        bundle_manifest = _load_bundle_manifest(spec["plugin_root"])
        metadata_entry = _metadata_driven_plugin_entry(
            spec,
            current_entry=None,
            plugin_manifest=plugin_manifest,
            bundle_manifest=bundle_manifest,
        )
        if metadata_entry is None:
            raise ValueError(f"repo-index generator does not know how to synthesize marketplace plugin {name}")
        ordered_plugins.append(metadata_entry)

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
