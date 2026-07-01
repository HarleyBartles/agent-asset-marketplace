#!/usr/bin/env python3
"""Regenerate the repo navigation index from marketplace registry surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from marketplace_utils import MARKETPLACE_PATH, MARKETPLACE_PLUGIN_SPECS, REPO_INDEX_PATH, load_json
from superpowers_source import superpowers_source_ledger, superpowers_source_root, superpowers_source_tag


ROOT = Path(__file__).resolve().parents[1]
REPO_WORKER_PACK_ENTRY = {
    "name": "repo-worker-pack",
    "plugin_root": "codex-marketplace/plugins/repo-worker-pack",
    "plugin_manifest": "codex-marketplace/plugins/repo-worker-pack/.codex-plugin/plugin.json",
    "source_md": "codex-marketplace/plugins/repo-worker-pack/SOURCE.md",
    "source_ledger": [],
    "license_path": "codex-marketplace/plugins/repo-worker-pack/LICENSE",
    "bundle_manifest": None,
    "skills_path": "codex-marketplace/plugins/repo-worker-pack/skills",
    "provenance_refs": ["provenance/repo-worker-pack.md"],
    "agents_md": None,
    "registry_path": "./codex-marketplace/plugins/repo-worker-pack",
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
        "provenance/dotnet-kit-governance/decisions.json",
        "provenance/dotnet-kit-governance/decisions.md",
        "provenance/dotnet-kit-governance/intake.json",
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
        "provenance/codex-cortex-governance/intake.json",
        "provenance/codex-cortex-governance/decisions.json",
        "provenance/codex-cortex-governance/decisions.md",
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
        "provenance/codex-cortex-governance/intake.json",
        "provenance/codex-cortex-governance/decisions.json",
        "provenance/codex-cortex-governance/decisions.md",
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
        "provenance/codex-cortex-governance/intake.json",
        "provenance/codex-cortex-governance/decisions.json",
        "provenance/codex-cortex-governance/decisions.md",
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
        *superpowers_source_ledger(),
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


def _synthetic_plugin_spec(name: str, *, current_entry: dict[str, Any], category: str | None = None) -> dict[str, Any]:
    plugin_root = current_entry.get("plugin_root") or f"codex-marketplace/plugins/{name}"
    manifest_path = current_entry.get("plugin_manifest") or f"{plugin_root}/.codex-plugin/plugin.json"
    registry_path = current_entry.get("registry_path") or f"./{plugin_root}"
    return {
        "name": name,
        "category": category or "Productivity",
        "registry_path": registry_path,
        "plugin_root": plugin_root,
        "manifest_path": ROOT / manifest_path,
    }


def _generic_plugin_entry(plugin: dict[str, Any], *, spec: dict[str, Any], current_entry: dict[str, Any] | None) -> dict[str, Any]:
    plugin_root = spec["plugin_root"]
    manifest_path = _plugin_manifest_path(spec["manifest_path"])
    entry = dict(current_entry or {})
    entry["name"] = spec["name"]
    entry["plugin_root"] = plugin_root
    entry["plugin_manifest"] = manifest_path
    entry["source_md"] = entry.get("source_md") or f"{plugin_root}/SOURCE.md"
    entry["source_ledger"] = list(entry.get("source_ledger", []))
    entry["license_path"] = entry.get("license_path") or f"{plugin_root}/LICENSE"
    entry["bundle_manifest"] = entry.get("bundle_manifest") or f"{plugin_root}/references/bundle-manifest.json"
    entry["skills_path"] = entry.get("skills_path") or f"{plugin_root}/skills"
    entry["provenance_refs"] = list(entry.get("provenance_refs", []))
    entry["agents_md"] = entry.get("agents_md")
    if spec["name"] == "superpowers-plus":
        entry["source_ledger"] = superpowers_source_ledger()
    entry["registry_path"] = spec.get("registry_path") or plugin.get("source", {}).get("path") or f"./{plugin_root}"
    entry["registry_alignment"] = dict(entry.get("registry_alignment", {"status": "aligned", "note": None}))
    return entry


def _normalize_zones(zones: list[dict]) -> list[dict]:
    normalized_zones: list[dict] = []
    superpowers_root = superpowers_source_root().relative_to(ROOT).as_posix()
    superpowers_version = superpowers_source_tag()
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
        if zone.get("name") == "superpowers-custody":
            updated_zone = dict(zone)
            updated_zone["path"] = superpowers_root
            updated_zone["purpose"] = (
                f"Retained third-party source custody for the upstream obra/superpowers {superpowers_version} release snapshot."
            )
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
                spec = _synthetic_plugin_spec(name, current_entry=current_plugins[name], category=plugin.get("category"))
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
            ordered_plugins.append(metadata_entry or _generic_plugin_entry(plugin, spec=spec, current_entry=current_plugins[name]))
            continue
        spec = plugin_specs_by_name.get(name)
        if spec is None:
            spec = _synthetic_plugin_spec(name, current_entry=current_plugins.get(name, {}), category=plugin.get("category"))
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
            metadata_entry = _generic_plugin_entry(plugin, spec=spec, current_entry=current_plugins.get(name))
        ordered_plugins.append(metadata_entry)

    repo_index["marketplace_plugins"] = ordered_plugins
    repo_index["zones"] = _normalize_zones(list(repo_index.get("zones", [])))
    validation = dict(repo_index.get("validation", {}))
    validation["marketplace_generate"] = "py -3 tools/generate_marketplace.py"
    validation["marketplace_check"] = "py -3 tools/generate_marketplace.py --check"
    validation["repo_index_generate"] = "py -3 tools/generate_repo_index.py"
    validation["repo_index_check"] = "py -3 tools/generate_repo_index.py --check"
    repo_index["validation"] = validation
    return repo_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or validate the repo navigation index")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    args = parser.parse_args()

    repo_index = build_repo_index()
    rendered = json.dumps(repo_index, indent=2, ensure_ascii=False)
    rendered += "\n"

    if args.check:
        if not REPO_INDEX_PATH.exists():
            raise FileNotFoundError(REPO_INDEX_PATH)
        current = REPO_INDEX_PATH.read_text(encoding="utf-8")
        if current != rendered:
            raise ValueError(f"{REPO_INDEX_PATH.relative_to(ROOT)} is stale; run py -3 tools/generate_repo_index.py")
        print(f"OK {REPO_INDEX_PATH.relative_to(ROOT)}")
        print("OK repo-index: repo-index/repo-index.json is current")
        return 0

    with REPO_INDEX_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(rendered)
    print(f"Wrote {REPO_INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
