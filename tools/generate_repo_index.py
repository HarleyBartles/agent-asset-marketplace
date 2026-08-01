#!/usr/bin/env python3
"""Regenerate the repo navigation index from marketplace registry surfaces."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from marketplace_utils import MARKETPLACE_PATH, MARKETPLACE_PLUGIN_SPECS, REPO_INDEX_PATH, load_json
from superpowers_source import superpowers_source_root, superpowers_source_tag


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPO_INDEX = {
    "schema_version": 1,
    "repo_name": "agent-asset-marketplace",
    "description": "Navigation metadata for the agent asset marketplace. This file is an index of repo zones and marketplace plugin packs, not the source of truth itself.",
    "marketplace_root_inventory_path": "codex-marketplace/plugin-roots.json",
    "marketplace_registry_path": ".agents/plugins/marketplace.json",
    "codex_marketplace_manifest_path": "codex-marketplace/manifest.json",
    "validation": {
        "marketplace": "py -3 tools/validate_marketplace.py",
        "repo_index": "py -3 tools/validate_repo_index.py",
        "repo_index_generate": "py -3 tools/generate_repo_index.py",
        "marketplace_generate": "py -3 tools/generate_marketplace.py",
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
            "nearest_scoped_agents_md": "codex-marketplace/AGENTS.md",
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
            "purpose": "Protected active Codex marketplace plugin pack roots and their packaging metadata, including the api-contracts-pack projection for api-design-patterns and openapi-specification plus the security-pack projection for secure-coding-practices, owasp-top-10, security-testing-patterns, and threat-modeling-techniques.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": "codex-marketplace/plugins/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "frontend-pack",
            "path": "codex-marketplace/plugins/frontend-pack",
            "purpose": "Browser frontend implementation guidance with shared architecture, DOM UI, React-hosted 3D, and frontend QA surfaces.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": "codex-marketplace/plugins/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-plus-marketplace",
            "path": "codex-marketplace/plugins/superpowers-plus",
            "purpose": "Codex-facing projection of the upstream Superpowers release snapshot, renamed to Superpowers+.",
            "surface_kind": "runtime-facing",
            "nearest_scoped_agents_md": "codex-marketplace/plugins/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
                "tools/project_skills.py",
            ],
        },
        {
            "name": "third-party-custody",
            "path": "sources/third_party",
            "purpose": "Third-party source custody for the retained unslop, superpowers, and feature-sliced upstream snapshots. The custody expectation is the upstream skill tree only; non-skill upstream scaffolding stays out unless a projection or validator explicitly requires it. The unslop engine is projected into the unslop-plus combined-source plugin.",
            "surface_kind": "vendored",
            "nearest_scoped_agents_md": "sources/third_party/AGENTS.md",
            "guidance_scope": "repo-owned-guidance",
            "notes": "Nested upstream AGENTS.md files remain third-party package instructions, not repository doctrine.",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
                "tools/validate_marketplace.py",
            ],
        },
        {
            "name": "superpowers-custody",
            "path": "sources/third_party/superpowers/obra-superpowers/v6.2.0",
            "purpose": (
                "Retained third-party source custody for the upstream obra/superpowers v6.2.0 "
                "release snapshot. The custody expectation is the upstream skill tree, with "
                "broader snapshot files kept only when the active projection or update tooling "
                "still requires them."
            ),
            "surface_kind": "vendored",
            "nearest_scoped_agents_md": "sources/third_party/AGENTS.md",
            "guidance_scope": "repo-owned-guidance",
            "notes": "Nested upstream AGENTS.md files remain third-party package instructions, not repository doctrine.",
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
            "nearest_scoped_agents_md": "provenance/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "docs-unslop-profile",
            "path": "docs/unslop/profile.md",
            "purpose": "Canonical repo unslop profile for anti-slop custody and discovery.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": "docs/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-plans",
            "path": ".agents/plans",
            "purpose": "Superpowers plan drafts and execution plans. Local guidance here reminds workers to check off completed steps before final publication and to explain intentionally open plans inside the plan itself.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".agents/plans/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "superpowers-specs",
            "path": ".agents/specs",
            "purpose": "Superpowers design specs. Specs are repo-resident, tracked, and indexed alongside plans.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": ".agents/guides/design-guide.md",
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
        {
            "name": "tools",
            "path": "tools",
            "purpose": "Repository validation and generation scripts.",
            "surface_kind": "hand-authored",
            "nearest_scoped_agents_md": "tools/AGENTS.md",
            "key_validation_scripts": [
                "tools/validate_marketplace.py",
                "tools/validate_repo_index.py",
                "tools/generate_marketplace.py",
            ],
        },
        {
            "name": "repo-index",
            "path": "repo-index",
            "purpose": "Navigation metadata for repo traversal and future corpus preparation.",
            "surface_kind": "generated",
            "nearest_scoped_agents_md": None,
            "key_validation_scripts": [
                "tools/validate_repo_index.py",
            ],
        },
    ],
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
    entry["bundle_manifest"] = repo_index.get("bundle_manifest") or f"{plugin_root}/references/bundle-manifest.json"
    entry["skills_path"] = (
        repo_index.get("skills_path") or entry.get("skills_path") or _default_skills_path(plugin_root, plugin_manifest)
    )
    entry["agents_md"] = repo_index.get("agents_md", entry.get("agents_md"))
    entry["registry_path"] = plugin["registry_path"]
    entry["registry_alignment"] = dict(
        repo_index.get(
            "registry_alignment",
            entry.get("registry_alignment", {"status": "aligned", "note": None}),
        )
    )
    for field_name in ("source_ledger", "license_path", "license_reference", "provenance_refs"):
        entry.pop(field_name, None)
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


def _generic_plugin_entry(
    plugin: dict[str, Any], *, spec: dict[str, Any], current_entry: dict[str, Any] | None
) -> dict[str, Any]:
    plugin_root = spec["plugin_root"]
    manifest_path = _plugin_manifest_path(spec["manifest_path"])
    entry = dict(current_entry or {})
    entry["name"] = spec["name"]
    entry["plugin_root"] = plugin_root
    entry["plugin_manifest"] = manifest_path
    entry["source_md"] = entry.get("source_md") or f"{plugin_root}/SOURCE.md"
    entry["bundle_manifest"] = entry.get("bundle_manifest") or f"{plugin_root}/references/bundle-manifest.json"
    entry["skills_path"] = entry.get("skills_path") or f"{plugin_root}/skills"
    entry["agents_md"] = entry.get("agents_md")
    entry["registry_path"] = spec.get("registry_path") or plugin.get("source", {}).get("path") or f"./{plugin_root}"
    entry["registry_alignment"] = dict(entry.get("registry_alignment", {"status": "aligned", "note": None}))
    for field_name in ("source_ledger", "license_path", "license_reference", "provenance_refs"):
        entry.pop(field_name, None)
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
            updated_zone["purpose"] = (
                "Codex-facing projection of the upstream Superpowers release snapshot, renamed to Superpowers+."
            )
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
        if zone.get("name") == "docs-superpowers-plans":
            updated_zone = dict(zone)
            updated_zone["name"] = "superpowers-plans"
            updated_zone["path"] = ".agents/plans"
            updated_zone["nearest_scoped_agents_md"] = ".agents/plans/AGENTS.md"
            normalized_zones.append(updated_zone)
            continue
        if zone.get("name") == "superpowers-plans":
            updated_zone = dict(zone)
            updated_zone["path"] = ".agents/plans"
            updated_zone["nearest_scoped_agents_md"] = ".agents/plans/AGENTS.md"
            normalized_zones.append(updated_zone)
            continue
        if zone.get("name") == "superpowers-specs":
            updated_zone = dict(zone)
            updated_zone["path"] = ".agents/specs"
            normalized_zones.append(updated_zone)
            continue
        if zone.get("name") == "third-party-custody":
            updated_zone = dict(zone)
            updated_zone["purpose"] = (
                "Third-party source custody for the retained unslop, superpowers, and feature-sliced upstream snapshots. "
                "The custody expectation is the upstream skill tree only; non-skill upstream scaffolding stays out unless a projection or validator explicitly requires it. "
                "The unslop engine is projected into the unslop-plus combined-source plugin."
            )
            normalized_zones.append(updated_zone)
            continue
        normalized_zones.append(zone)
    agents_md_replacements = {
        "codex-marketplace/AGENTS.md": ".devin/rules/codex-marketplace.md",
        "codex-marketplace/plugins/AGENTS.md": ".devin/rules/codex-plugins.md",
        "sources/third_party/AGENTS.md": ".devin/rules/third-party.md",
        "provenance/AGENTS.md": ".devin/rules/provenance.md",
        "docs/AGENTS.md": ".devin/rules/docs.md",
        ".agents/plans/AGENTS.md": ".devin/rules/plans.md",
        "tools/AGENTS.md": ".devin/rules/tools.md",
    }
    for zone in normalized_zones:
        if isinstance(zone, dict):
            nearest = zone.get("nearest_scoped_agents_md")
            if nearest in agents_md_replacements:
                zone["nearest_scoped_agents_md"] = agents_md_replacements[nearest]
    return normalized_zones


def build_repo_index() -> dict:
    marketplace = load_json(MARKETPLACE_PATH)
    if REPO_INDEX_PATH.exists():
        repo_index = load_json(REPO_INDEX_PATH)
        if not isinstance(repo_index, dict) or repo_index.get("schema_version") != 1:
            repo_index = deepcopy(DEFAULT_REPO_INDEX)
    else:
        repo_index = deepcopy(DEFAULT_REPO_INDEX)
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
                spec = _synthetic_plugin_spec(
                    name, current_entry=current_plugins[name], category=plugin.get("category")
                )
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
            ordered_plugins.append(
                metadata_entry or _generic_plugin_entry(plugin, spec=spec, current_entry=current_plugins[name])
            )
            continue
        spec = plugin_specs_by_name.get(name)
        if spec is None:
            spec = _synthetic_plugin_spec(
                name, current_entry=current_plugins.get(name, {}), category=plugin.get("category")
            )
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
    validation.pop("generated_drift", None)

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
