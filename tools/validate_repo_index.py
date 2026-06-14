#!/usr/bin/env python3
"""Validate the repo navigation index against the current marketplace surfaces."""

from __future__ import annotations

from pathlib import Path

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    PROTECTED_MARKETPLACE_PLUGIN_NAMES,
    PLUGIN_ROOT_INVENTORY_PATH,
    REPO_INDEX_PATH,
    load_json,
)


ROOT = Path(__file__).resolve().parents[1]


def check_path_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    print(f"OK path: {path.relative_to(ROOT)}")


def check_json(path: Path) -> dict:
    data = load_json(path)
    print(f"OK json: {path.relative_to(ROOT)}")
    return data


def check_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"{path} is empty")
    print(f"OK text: {path.relative_to(ROOT)}")
    return text


def _resolved_path(relative_path: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ValueError("expected a non-empty relative path string")
    return ROOT / Path(relative_path)


def _validate_required_string_field(entry: dict, field: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"repo index entry is missing required field: {field}")
    return value


def _validate_optional_string_field(entry: dict, field: str) -> str | None:
    value = entry.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"repo index entry field {field} must be a non-empty string or null")
    return value


def _validate_optional_list_field(entry: dict, field: str) -> list[str]:
    value = entry.get(field, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"repo index entry field {field} must be a list")
    paths: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"repo index entry field {field} must contain only non-empty strings")
        paths.append(item)
    return paths


def validate_repo_index() -> dict:
    repo_index = check_json(REPO_INDEX_PATH)

    schema_version = repo_index.get("schema_version")
    if schema_version != 1:
        raise ValueError("repo-index schema_version must be 1")
    if repo_index.get("marketplace_root_inventory_path") != "codex-marketplace/plugin-roots.json":
        raise ValueError("repo-index marketplace_root_inventory_path mismatch")

    zones = repo_index.get("zones")
    if not isinstance(zones, list) or not zones:
        raise ValueError("repo-index zones must be a non-empty list")

    marketplace_plugins = repo_index.get("marketplace_plugins")
    if not isinstance(marketplace_plugins, list) or not marketplace_plugins:
        raise ValueError("repo-index marketplace_plugins must be a non-empty list")

    if repo_index.get("marketplace_registry_path") != ".agents/plugins/marketplace.json":
        raise ValueError("repo-index marketplace_registry_path mismatch")
    if repo_index.get("codex_marketplace_manifest_path") != "codex-marketplace/manifest.json":
        raise ValueError("repo-index codex_marketplace_manifest_path mismatch")

    validation = repo_index.get("validation")
    if not isinstance(validation, dict):
        raise ValueError("repo-index validation block is missing")
    if validation.get("marketplace") != "py -3 tools/validate_marketplace.py":
        raise ValueError("repo-index marketplace validation command mismatch")
    if validation.get("repo_index") != "py -3 tools/validate_repo_index.py":
        raise ValueError("repo-index repo_index validation command mismatch")
    if validation.get("skill_zips_update") != "py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>":
        raise ValueError("repo-index skill_zips_update command mismatch")
    if validation.get("skill_zips_full_regeneration") != "py -3 tools/update_skill_artifacts.py --all":
        raise ValueError("repo-index skill_zips_full_regeneration command mismatch")
    if validation.get("skill_zips_check") != "py -3 tools/validate_skill_zips.py":
        raise ValueError("repo-index skill_zips_check command mismatch")
    if validation.get("generated_drift") != "py -3 tools/validate_generated_drift.py --base origin/main":
        raise ValueError("repo-index generated_drift command mismatch")

    check_path_exists(PLUGIN_ROOT_INVENTORY_PATH)

    seen_zone_names: set[str] = set()
    seen_zone_paths: set[str] = set()
    for zone in zones:
        if not isinstance(zone, dict):
            raise ValueError("repo-index zones must contain objects")
        zone_name = _validate_required_string_field(zone, "name")
        zone_path = _validate_required_string_field(zone, "path")
        surface_kind = _validate_required_string_field(zone, "surface_kind")
        if surface_kind not in {"hand-authored", "generated", "vendored", "provenance", "runtime-facing"}:
            raise ValueError(f"repo-index zone {zone_name} has an unsupported surface_kind")
        if zone_name in seen_zone_names:
            raise ValueError(f"repo-index zone name is duplicated: {zone_name}")
        if zone_path in seen_zone_paths:
            raise ValueError(f"repo-index zone path is duplicated: {zone_path}")
        seen_zone_names.add(zone_name)
        seen_zone_paths.add(zone_path)

        zone_fs_path = _resolved_path(zone_path)
        check_path_exists(zone_fs_path)

        agents_md = _validate_optional_string_field(zone, "nearest_scoped_agents_md")
        if agents_md is not None:
            agents_path = _resolved_path(agents_md)
            check_path_exists(agents_path)
            if zone_path == "sources/third_party":
                guidance_scope = zone.get("guidance_scope")
                if guidance_scope != "repo-owned-guidance":
                    raise ValueError(
                        "sources/third_party zone must state that its scoped AGENTS guidance is repo-owned"
                    )

        scripts = _validate_optional_list_field(zone, "key_validation_scripts")
        for script in scripts:
            check_path_exists(_resolved_path(script))

    registry = check_json(MARKETPLACE_PATH)
    codex_manifest = check_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    if registry != codex_manifest:
        raise ValueError(".agents/plugins/marketplace.json does not match codex-marketplace/manifest.json")

    registry_plugins = {plugin["name"]: plugin for plugin in registry.get("plugins", [])}
    spec_by_name = {spec["name"]: spec for spec in MARKETPLACE_PLUGIN_SPECS}

    if set(registry_plugins) != set(spec_by_name):
        raise ValueError("repo-index marketplace plugins do not match the current marketplace registry")
    registry_plugin_names = [plugin.get("name") for plugin in registry.get("plugins", [])]
    if registry_plugin_names != list(PROTECTED_MARKETPLACE_PLUGIN_NAMES):
        raise ValueError("repo-index marketplace registry order does not match the protected marketplace shape")

    seen_plugin_names: set[str] = set()
    for entry in marketplace_plugins:
        if not isinstance(entry, dict):
            raise ValueError("repo-index marketplace_plugins must contain objects")

        name = _validate_required_string_field(entry, "name")
        if name in seen_plugin_names:
            raise ValueError(f"repo-index marketplace plugin is duplicated: {name}")
        seen_plugin_names.add(name)

        plugin_root = _validate_required_string_field(entry, "plugin_root")
        plugin_manifest = _validate_required_string_field(entry, "plugin_manifest")
        registry_path = _validate_required_string_field(entry, "registry_path")
        registry_alignment = entry.get("registry_alignment")
        if not isinstance(registry_alignment, dict):
            raise ValueError(f"repo-index marketplace plugin {name} is missing registry_alignment")
        alignment_status = registry_alignment.get("status")
        alignment_note = registry_alignment.get("note")
        if alignment_status not in {"aligned", "intentional-delta"}:
            raise ValueError(f"repo-index marketplace plugin {name} has an unsupported registry_alignment status")
        if alignment_status == "intentional-delta" and not isinstance(alignment_note, str) and alignment_note is not None:
            raise ValueError(f"repo-index marketplace plugin {name} needs a textual registry_alignment note")
        if alignment_status == "intentional-delta" and not alignment_note:
            raise ValueError(f"repo-index marketplace plugin {name} needs a registry_alignment note")

        check_path_exists(_resolved_path(plugin_root))
        check_path_exists(_resolved_path(plugin_manifest))

        plugin_manifest_json = check_json(_resolved_path(plugin_manifest))
        if plugin_manifest_json.get("name") != name:
            raise ValueError(f"repo-index marketplace plugin {name} manifest name mismatch")

        plugin_spec = spec_by_name.get(name)
        registry_plugin = registry_plugins.get(name)
        if plugin_spec is None or registry_plugin is None:
            raise ValueError(f"repo-index marketplace plugin {name} is not present in the current marketplace registry")

        if alignment_status == "aligned":
            if registry_plugin.get("source", {}).get("path") != registry_path:
                raise ValueError(f"repo-index marketplace plugin {name} registry path mismatch")
            if registry_plugin.get("source", {}).get("source") != "local":
                raise ValueError(f"repo-index marketplace plugin {name} registry source kind mismatch")
        else:
            if not alignment_note:
                raise ValueError(f"repo-index marketplace plugin {name} needs an intentional-delta explanation")

        source_md = _validate_optional_string_field(entry, "source_md")
        source_ledger = _validate_optional_list_field(entry, "source_ledger")
        if source_md is None and not source_ledger:
            raise ValueError(f"repo-index marketplace plugin {name} needs source_md or source_ledger")
        if source_md is not None:
            check_path_exists(_resolved_path(source_md))
        for source_path in source_ledger:
            check_path_exists(_resolved_path(source_path))

        license_path = _validate_optional_string_field(entry, "license_path")
        license_reference = _validate_optional_string_field(entry, "license_reference")
        if license_path is None and license_reference is None:
            raise ValueError(f"repo-index marketplace plugin {name} needs license_path or license_reference")
        if license_path is not None:
            check_path_exists(_resolved_path(license_path))

        bundle_manifest = _validate_optional_string_field(entry, "bundle_manifest")
        if bundle_manifest is not None:
            check_path_exists(_resolved_path(bundle_manifest))

        skills_path = _validate_optional_string_field(entry, "skills_path")
        manifest_skills = plugin_manifest_json.get("skills")
        if manifest_skills is not None and not skills_path:
            raise ValueError(f"repo-index marketplace plugin {name} is missing skills_path")
        if skills_path is not None:
            check_path_exists(_resolved_path(skills_path))
            if not isinstance(manifest_skills, str):
                raise ValueError(f"repo-index marketplace plugin {name} manifest skills path mismatch")
            expected_skills_path = (ROOT / Path(plugin_root) / Path(manifest_skills)).resolve()
            actual_skills_path = _resolved_path(skills_path).resolve()
            if actual_skills_path != expected_skills_path:
                raise ValueError(f"repo-index marketplace plugin {name} skills_path mismatch")

        provenance_refs = _validate_optional_list_field(entry, "provenance_refs")
        for reference in provenance_refs:
            check_path_exists(_resolved_path(reference))

        agents_md = _validate_optional_string_field(entry, "agents_md")
        if agents_md is not None:
            check_path_exists(_resolved_path(agents_md))

    if seen_plugin_names != set(registry_plugins):
        raise ValueError("repo-index marketplace plugin list does not match the current marketplace registry")
    if [entry.get("name") for entry in marketplace_plugins] != list(PROTECTED_MARKETPLACE_PLUGIN_NAMES):
        raise ValueError("repo-index marketplace plugin order does not match the protected marketplace shape")

    third_party_agents = ROOT / "sources/third_party/AGENTS.md"
    third_party_guidance = check_text(third_party_agents)
    normalized_third_party_guidance = " ".join(third_party_guidance.split())
    if "third-party source custody" not in normalized_third_party_guidance or "not repository doctrine" not in normalized_third_party_guidance:
        raise ValueError("sources/third_party/AGENTS.md must clearly distinguish repo-owned guidance from third-party instructions")

    print("Repo index validation passed.")
    return repo_index


def main() -> int:
    validate_repo_index()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
