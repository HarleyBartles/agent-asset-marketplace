#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

from pathlib import Path
import sys

from marketplace_utils import (
    BUNDLE_MANIFEST_PATH,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    PLUGIN_README_PATH,
    PLUGIN_SKILL_PATH,
    PROVENANCE_PATH,
    SOURCE_DECISIONS_JSON_PATH,
    SOURCE_DECISIONS_MD_PATH,
    SOURCE_INTAKE_JSON_PATH,
    SOURCE_MAP_PATH,
    build_marketplace_manifest,
    load_json,
    normalize_decision_record,
    normalize_decision_row,
    parse_top_markdown_table,
)


ROOT = Path(__file__).resolve().parents[1]


def check_json(path: Path) -> dict:
    data = load_json(path)
    print(f"OK json: {path.relative_to(ROOT)}")
    return data


def check_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"{path} is empty")
    print(f"OK text: {path.relative_to(ROOT)}")
    return content


def check_path_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    print(f"OK path: {path.relative_to(ROOT)}")


def validate_decisions(decisions: list[dict], decisions_md_rows: list[dict[str, str]], decisions_md_text: str) -> None:
    normalized_json = [
        _decision_structure(normalize_decision_record(row))
        for row in decisions
        if row.get("source_id") and row.get("source_id") != "global.mark-19.source-import-boundary"
    ]
    normalized_md = [
        _decision_structure(normalize_decision_row(row))
        for row in decisions_md_rows
        if row.get("source_id") and row.get("source_id") != "global.mark-19.source-import-boundary"
    ]
    if normalized_json != normalized_md:
        raise ValueError("sources/house-skills/decisions.md does not match sources/house-skills/decisions.json")

    boundary = next((row for row in decisions if row.get("id") == "global.mark-19.source-import-boundary"), None)
    if boundary is None:
        raise ValueError("sources/house-skills/decisions.json is missing the MARK-19 boundary row")
    if boundary.get("import_state") != "source-import-boundary":
        raise ValueError("sources/house-skills/decisions.json has an invalid MARK-19 boundary state")
    if "global.mark-19.source-import-boundary" not in decisions_md_text:
        raise ValueError("sources/house-skills/decisions.md is missing the MARK-19 boundary row")
    if "MARK-19 imports exactly six reviewed core generic buster source records" not in decisions_md_text:
        raise ValueError("sources/house-skills/decisions.md is missing the MARK-19 boundary description")


def _decision_structure(record: dict[str, object]) -> dict[str, object]:
    keys = ("issue", "source_id", "source_path", "public_name", "provenance_name", "import_state", "scope")
    return {key: record.get(key, "") for key in keys}


def validate_marketplace_registry(registry: dict, plugin_manifests: list[dict]) -> None:
    expected = build_marketplace_manifest(plugin_manifests)
    if registry != expected:
        raise ValueError(".agents/plugins/marketplace.json does not match the generated marketplace manifest")

    if registry.get("name") != EXPECTED_MARKETPLACE["name"]:
        raise ValueError("Marketplace registry name mismatch")
    if registry.get("interface", {}).get("displayName") != EXPECTED_MARKETPLACE["interface"]["displayName"]:
        raise ValueError("Marketplace registry display name mismatch")

    plugins_by_name = {plugin.get("name"): plugin for plugin in registry.get("plugins", [])}
    expected_plugins = {spec["name"]: spec["registry_path"] for spec in MARKETPLACE_PLUGIN_SPECS}
    for name, path in expected_plugins.items():
        plugin = plugins_by_name.get(name)
        if not plugin:
            raise ValueError(f"Marketplace registry is missing the {name} plugin entry")
        if plugin.get("source", {}).get("path") != path:
            raise ValueError(f"Marketplace registry {name} plugin path mismatch")
        if plugin.get("source", {}).get("source") != "local":
            raise ValueError(f"Marketplace registry {name} plugin source kind mismatch")
        if plugin.get("policy", {}).get("installation") != "AVAILABLE":
            raise ValueError(f"Marketplace registry {name} installation policy mismatch")
        if plugin.get("policy", {}).get("authentication") != "ON_INSTALL":
            raise ValueError(f"Marketplace registry {name} authentication policy mismatch")
        if plugin.get("category") != "Productivity":
            raise ValueError(f"Marketplace registry {name} category mismatch")


def validate_plugin_manifest(plugin_manifest: dict, plugin_name: str, plugin_root: str) -> None:
    if plugin_manifest.get("name") != plugin_name:
        raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json name mismatch")
    if plugin_manifest.get("interface", {}).get("category") != "Productivity":
        raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json category mismatch")
    for key in ("composerIcon", "logo"):
        relative = plugin_manifest.get("interface", {}).get(key)
        if relative != "./assets/icon.svg":
            raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json {key} path mismatch")
    check_path_exists(ROOT / plugin_root / "assets/icon.svg")
    skills_path = plugin_manifest.get("skills")
    if skills_path:
        if not isinstance(skills_path, str):
            raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json skills path must be a string")
        check_path_exists(ROOT / plugin_root / skills_path)


def validate_bundle_manifest(bundle_manifest: dict, intake: dict) -> None:
    if bundle_manifest.get("bundle_name") != "house-skills":
        raise ValueError("bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError("bundle manifest bundle_version mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "plugins/house-skills":
        raise ValueError("bundle manifest plugin_root mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "sources/house-skills/decisions.json",
        "sources/house-skills/decisions.md",
        "sources/house-skills/intake.json",
        "provenance/house-skills.md",
    ]:
        raise ValueError("bundle manifest source_of_truth mismatch")

    imports = intake.get("imports", [])
    projected_imports = [
        record
        for record in imports
        if record.get("import_state") == "imported" and record.get("issue") == "MARK-30"
    ]
    imported_by_id = {record["source_id"]: record for record in projected_imports}
    components = bundle_manifest.get("components", [])
    if len(components) != len(imported_by_id):
        raise ValueError("bundle manifest component count does not match imported ledger records")

    projected_order = [record["source_id"] for record in projected_imports]
    component_order: list[str] = []
    for component in components:
        source_id = component.get("installed_source_skill_id")
        if source_id not in imported_by_id:
            raise ValueError(f"bundle manifest component {source_id!r} is not present in sources/house-skills/intake.json")
        source_row = imported_by_id[source_id]
        if component.get("source_path") != source_row.get("source_path"):
            raise ValueError(f"bundle manifest source path mismatch for {source_id}")
        expected_canonical_name = source_id.rsplit("-v", 1)[0]
        expected_component_version = f"v{source_id.rsplit('-v', 1)[1]}"
        if component.get("canonical_name") != expected_canonical_name:
            raise ValueError(f"bundle manifest canonical name mismatch for {source_id}")
        if component.get("component_version") != expected_component_version:
            raise ValueError(f"bundle manifest component version mismatch for {source_id}")
        if component.get("import_status") != source_row.get("import_state"):
            raise ValueError(f"bundle manifest import status mismatch for {source_id}")
        check_path_exists(ROOT / component["source_path"])
        component_order.append(source_id)

    if component_order != projected_order:
        raise ValueError("bundle manifest component ordering does not match the source ledger projection")

    for source_path in bundle_manifest.get("source_of_truth", []):
        check_path_exists(ROOT / source_path)


def validate_source_map(text: str) -> None:
    for needle in (
        ".agents/plugins/marketplace.json",
        "plugins/house-skills/.codex-plugin/plugin.json",
        "plugins/house-skills/skills/house-skills/references/bundle-manifest.json",
        "sources/house-skills/decisions.json",
        "sources/house-skills/decisions.md",
        "sources/house-skills/intake.json",
    ):
        if needle not in text:
            raise ValueError(f"source map is missing {needle}")


def main() -> int:
    decisions = check_json(SOURCE_DECISIONS_JSON_PATH)
    intake = check_json(SOURCE_INTAKE_JSON_PATH)
    plugin_manifests: list[dict] = []
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec["name"], spec["plugin_root"])
        plugin_manifests.append(plugin_manifest)
    registry = check_json(MARKETPLACE_PATH)
    bundle_manifest = check_json(BUNDLE_MANIFEST_PATH)
    decisions_md_text = check_text(SOURCE_DECISIONS_MD_PATH)
    decision_rows = parse_top_markdown_table(SOURCE_DECISIONS_MD_PATH)

    validate_decisions(decisions, decision_rows, decisions_md_text)
    validate_marketplace_registry(registry, plugin_manifests)
    validate_bundle_manifest(bundle_manifest, intake)

    source_map = check_text(SOURCE_MAP_PATH)
    validate_source_map(source_map)
    check_text(ROOT / "codex-marketplace/README.md")
    check_text(ROOT / "codex-marketplace/plugins/README.md")
    check_text(ROOT / "provenance/MARK-46-activity-log.md")
    check_text(PLUGIN_README_PATH)
    check_text(PLUGIN_SKILL_PATH)
    check_text(PROVENANCE_PATH)

    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
