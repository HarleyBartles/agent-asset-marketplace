#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

import json
import re
from pathlib import Path

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    BUNDLE_MANIFEST_PATH,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    PROTECTED_MARKETPLACE_PLUGIN_NAMES,
    PLUGIN_README_PATH,
    PLUGIN_SKILL_PATH,
    PROVENANCE_PATH,
    PLUGIN_BUNDLE_AGENTS_PATH,
    ADVENTURES_PACK_BUNDLE_MANIFEST_PATH,
    ADVENTURES_PACK_SOURCE_MAP_PATH,
    ADVENTURES_PACK_SKILL_PATH,
    SOURCE_DECISIONS_JSON_PATH,
    SOURCE_DECISIONS_MD_PATH,
    SOURCE_INTAKE_JSON_PATH,
    SOURCE_MAP_PATH,
    PLUGIN_ROOT_INVENTORY_PATH,
    REPO_INDEX_PATH,
    REPO_INDEX_README_PATH,
    build_marketplace_manifest,
    load_json,
    normalize_decision_record,
    normalize_decision_row,
    parse_top_markdown_table,
)
from validate_repo_index import validate_repo_index
from skill_overlay_materializer import stage_overlay_tree, validate_openai_agent_yaml
from skill_zip_artifacts import validate_skill_markdown_frontmatter, validate_skill_zip_registry


ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SUPERPOWERS_SOURCES = {
    "linear-superpowers": "sources/first_party/core/linear-superpowers",
    "github-superpowers": "sources/first_party/skills/github-superpowers",
    "unslop-superpowers": "sources/first_party/skills/unslop-superpowers",
    "architecture-superpowers": "sources/first_party/skills/architecture-superpowers",
    "ecc-superpowers": "sources/first_party/skills/ecc-superpowers",
}

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".sh",
    ".svg",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".ts",
}
TEXT_FILENAMES = {"SKILL.md", "openai.yaml"}


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


def list_files(root: Path) -> list[Path]:
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def _canonicalize_tree_bytes(path: Path, raw: bytes) -> bytes:
    if path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES:
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return raw


def _split_skill_frontmatter_and_body(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError(f"{path} is missing a closing YAML frontmatter delimiter")
    frontmatter = "".join(lines[1:end_index])
    body = "".join(lines[end_index + 1 :])
    return frontmatter, body


def validate_tree_mirror(source_root: Path, local_root: Path, component_name: str) -> None:
    source_files = list_files(source_root)
    local_files = list_files(local_root)
    if source_files != local_files:
        raise ValueError(f"adventures-pack component {component_name} file inventory mismatch")
    for rel_path in source_files:
        source_bytes = _canonicalize_tree_bytes(source_root / rel_path, (source_root / rel_path).read_bytes())
        local_bytes = _canonicalize_tree_bytes(local_root / rel_path, (local_root / rel_path).read_bytes())
        if source_bytes != local_bytes:
            raise ValueError(f"adventures-pack component {component_name} file content mismatch at {rel_path}")


def validate_tree_reconstruction(source_root: Path, overlay_root: Path | None, local_root: Path, component_name: str) -> None:
    expected_root, tempdir = stage_overlay_tree(source_root, overlay_root)
    try:
        validate_tree_mirror(expected_root, local_root, component_name)
    finally:
        tempdir.cleanup()


def _validate_superpowers_provenance_map(bundle_manifest: dict, plugin_root: str) -> None:
    provenance_map = load_json(ROOT / plugin_root / "references" / "provenance-map.json")
    if not isinstance(provenance_map, dict):
        raise ValueError("superpowers-plus provenance-map.json must contain an object")

    source_backed = provenance_map.get("source_backed_projections", [])
    adapted = provenance_map.get("adapted_projections", [])
    source_only = provenance_map.get("source_only_surfaces", [])
    if not isinstance(source_backed, list) or not isinstance(adapted, list) or not isinstance(source_only, list):
        raise ValueError("superpowers-plus provenance-map.json uses an invalid shape")

    expected_source_backed = {
        entry["canonical_name"]: entry
        for entry in bundle_manifest.get("entries", [])
        if isinstance(entry, dict)
        and entry.get("source_category") == "first_party"
        and entry.get("canonical_name") != "ecc-superpowers"
    }
    expected_adapted = {
        entry["canonical_name"]: entry
        for entry in bundle_manifest.get("entries", [])
        if isinstance(entry, dict)
        and entry.get("content_mode") == "adapted"
        and (entry.get("source_category") == "third_party" or entry.get("canonical_name") == "ecc-superpowers")
    }

    source_backed_by_name = {entry.get("canonical_name"): entry for entry in source_backed if isinstance(entry, dict)}
    adapted_by_name = {entry.get("canonical_name"): entry for entry in adapted if isinstance(entry, dict)}

    if set(source_backed_by_name) != set(expected_source_backed):
        raise ValueError("superpowers-plus provenance-map.json source_backed_projections mismatch")
    if set(adapted_by_name) != set(expected_adapted):
        raise ValueError("superpowers-plus provenance-map.json adapted_projections mismatch")

    for canonical_name, expected_entry in expected_source_backed.items():
        projection = source_backed_by_name[canonical_name]
        if projection.get("content_mode") != "verbatim":
            raise ValueError(f"superpowers-plus provenance-map.json source_backed_projections[{canonical_name}] must be verbatim")
        if projection.get("adaptation_overlay_path") is not None:
            raise ValueError(f"superpowers-plus provenance-map.json source_backed_projections[{canonical_name}] must not declare an overlay")
        if projection.get("local_path") != f"codex-marketplace/plugins/superpowers-plus/skills/{canonical_name}":
            raise ValueError(f"superpowers-plus provenance-map.json source_backed_projections[{canonical_name}] local path mismatch")
        if projection.get("canonical_source_path") != expected_entry.get("canonical_source_path"):
            raise ValueError(f"superpowers-plus provenance-map.json source_backed_projections[{canonical_name}] source path mismatch")
    for canonical_name, expected_entry in expected_adapted.items():
        projection = adapted_by_name[canonical_name]
        expected_overlay = expected_entry.get("adaptation_overlay_path")
        if projection.get("content_mode") != "adapted":
            raise ValueError(f"superpowers-plus provenance-map.json adapted_projections[{canonical_name}] must be adapted")
        if projection.get("adaptation_overlay_path") != expected_overlay:
            raise ValueError(f"superpowers-plus provenance-map.json adapted_projections[{canonical_name}] overlay path mismatch")
        if projection.get("local_path") != f"codex-marketplace/plugins/superpowers-plus/skills/{canonical_name}":
            raise ValueError(f"superpowers-plus provenance-map.json adapted_projections[{canonical_name}] local path mismatch")
        if projection.get("canonical_source_path") != expected_entry.get("canonical_source_path"):
            raise ValueError(f"superpowers-plus provenance-map.json adapted_projections[{canonical_name}] source path mismatch")
        for field_name in ("source_path", "source_author", "source_license", "adapted_author"):
            expected_value = expected_entry.get(field_name)
            if expected_value is not None and projection.get(field_name) != expected_value:
                raise ValueError(
                    f"superpowers-plus provenance-map.json adapted_projections[{canonical_name}] {field_name} mismatch"
                )

    if len(source_only) != 7:
        raise ValueError("superpowers-plus provenance-map.json source_only_surfaces count mismatch")


def _validate_repo_index_metadata(repo_index: dict | None, *, bundle_name: str, plugin_root: str) -> None:
    if repo_index is None:
        return
    if not isinstance(repo_index, dict):
        raise ValueError(f"{bundle_name} bundle manifest repo_index must be a mapping")

    for field_name in ("source_ledger", "provenance_refs"):
        value = repo_index.get(field_name)
        if not isinstance(value, list):
            raise ValueError(f"{bundle_name} bundle manifest repo_index {field_name} must be a list")
        for item in value:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"{bundle_name} bundle manifest repo_index {field_name} must contain nonblank strings")

    agents_md = repo_index.get("agents_md")
    if agents_md is not None and (not isinstance(agents_md, str) or not agents_md.strip()):
        raise ValueError(f"{bundle_name} bundle manifest repo_index agents_md must be a nonblank string or null")

    registry_alignment = repo_index.get("registry_alignment")
    if not isinstance(registry_alignment, dict):
        raise ValueError(f"{bundle_name} bundle manifest repo_index registry_alignment must be a mapping")
    status = registry_alignment.get("status")
    note = registry_alignment.get("note")
    if status not in {"aligned", "intentional-delta"}:
        raise ValueError(f"{bundle_name} bundle manifest repo_index registry_alignment status mismatch")
    if status == "intentional-delta" and not isinstance(note, str):
        raise ValueError(f"{bundle_name} bundle manifest repo_index registry_alignment note must be text")
    if status == "intentional-delta" and not note.strip():
        raise ValueError(f"{bundle_name} bundle manifest repo_index registry_alignment note must be nonblank")

    for field_name in ("source_md", "license_path", "license_reference", "bundle_manifest", "skills_path"):
        value = repo_index.get(field_name)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{bundle_name} bundle manifest repo_index {field_name} must be a nonblank string or null")


def _load_markdown_table_column_values(path: Path, column_name: str) -> list[str]:
    rows = parse_top_markdown_table(path)
    values: list[str] = []
    seen_values: set[str] = set()
    for row in rows:
        value = row.get(column_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{path}: markdown table column {column_name} must contain nonblank strings")
        if value in seen_values:
            raise ValueError(f"{path}: markdown table column {column_name} contains a duplicate value: {value}")
        seen_values.add(value)
        values.append(value)
    if not values:
        raise ValueError(f"{path}: markdown table column {column_name} must contain at least one value")
    return values


def validate_everything_codex_code_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    if bundle_manifest.get("bundle_name") != "everything-codex-code":
        raise ValueError("everything-codex-code bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError("everything-codex-code bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") != "project-scoped-codex-plugin-projection":
        raise ValueError("everything-codex-code bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("everything-codex-code bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/everything-codex-code":
        raise ValueError("everything-codex-code bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_root") != "codex-marketplace/plugins/superpowers-ecc/skills":
        raise ValueError("everything-codex-code bundle manifest canonical_source_root mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json",
        "codex-marketplace/plugins/superpowers-ecc/references/source-map.md",
        "provenance/superpowers-ecc.md",
    ]:
        raise ValueError("everything-codex-code bundle manifest source_of_truth mismatch")
    if bundle_manifest.get("projection_policy") != (
        "Project the ECC workflow skills already selected into superpowers-ecc. Keep this pack mirrored from that marketplace projection rather than upstream ECC custody."
    ):
        raise ValueError("everything-codex-code bundle manifest projection_policy mismatch")

    components = bundle_manifest.get("components", [])
    if not isinstance(components, list) or not components:
        raise ValueError("everything-codex-code bundle manifest components must be a non-empty list")

    skill_dir = ROOT / plugin_root / "skills"
    source_map_path = ROOT / plugin_root / "references" / "source-map.md"
    check_path_exists(skill_dir)
    check_path_exists(source_map_path)
    expected_names = _load_markdown_table_column_values(source_map_path, "Skill")
    actual_skill_names = sorted(path.name for path in skill_dir.iterdir() if path.is_dir())
    if actual_skill_names != sorted(expected_names):
        raise ValueError("everything-codex-code bundle manifest skill directory inventory mismatch")

    seen_names: set[str] = set()
    seen_local_paths: set[str] = set()
    component_names: list[str] = []
    for component in components:
        if not isinstance(component, dict):
            raise ValueError("everything-codex-code bundle manifest components must contain objects")
        canonical_name = component.get("canonical_name")
        source_path = component.get("source_path")
        local_path = component.get("local_path")
        projection_status = component.get("projection_status")
        if not isinstance(canonical_name, str) or not canonical_name:
            raise ValueError("everything-codex-code bundle manifest component is missing canonical_name")
        if canonical_name in seen_names:
            raise ValueError(f"everything-codex-code bundle manifest component is duplicated: {canonical_name}")
        seen_names.add(canonical_name)
        component_names.append(canonical_name)
        if not isinstance(source_path, str) or not source_path:
            raise ValueError(f"everything-codex-code bundle manifest component {canonical_name} is missing source_path")
        if not isinstance(local_path, str) or not local_path:
            raise ValueError(f"everything-codex-code bundle manifest component {canonical_name} is missing local_path")
        if local_path in seen_local_paths:
            raise ValueError(f"everything-codex-code bundle manifest component local path is duplicated: {local_path}")
        seen_local_paths.add(local_path)
        if projection_status != "projected":
            raise ValueError(f"everything-codex-code bundle manifest component {canonical_name} must be projected")

        source_md = ROOT / source_path
        local_md = ROOT / plugin_root / local_path
        check_path_exists(source_md)
        check_path_exists(local_md)
        validate_tree_mirror(source_md.parent, local_md.parent, canonical_name)

    if component_names != expected_names:
        raise ValueError("everything-codex-code bundle manifest components must match the source map selection")

    _validate_repo_index_metadata(bundle_manifest.get("repo_index"), bundle_name="everything-codex-code", plugin_root=plugin_root)


def _validate_projection_entry_provenance(entry: dict, *, bundle_name: str) -> None:
    canonical_name = entry.get("canonical_name")
    if not isinstance(canonical_name, str) or not canonical_name:
        raise ValueError(f"{bundle_name} bundle manifest imported entry is missing canonical_name")

    def require_nonblank(field_name: str) -> None:
        value = entry.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} is missing {field_name}")

    require_nonblank("canonical_source_path")
    require_nonblank("provenance_note")

    content_mode = entry.get("content_mode")
    source_category = entry.get("source_category")
    if content_mode == "verbatim":
        if source_category not in {"first_party", "third_party"}:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has an invalid source_category")
        if entry.get("adaptation_overlay_path") is not None:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} must not declare adaptation_overlay_path")
        if entry.get("adapted_author") is not None:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} must not declare adapted_author")
        for field_name in ("source_path", "source_author", "source_license", "source_repo"):
            if field_name in entry:
                require_nonblank(field_name)
        return

    if content_mode != "adapted":
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has invalid content_mode")
    if not entry.get("adaptation_note"):
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} requires an adaptation note")

    if source_category == "third_party":
        require_nonblank("adaptation_overlay_path")
        require_nonblank("adapted_author")
    elif source_category == "first_party":
        require_nonblank("source_path")
        require_nonblank("source_author")
        require_nonblank("source_license")
        require_nonblank("adapted_author")
    else:
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has an invalid source_category")


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
        raise ValueError("sources/first_party/skills/house-skills/decisions.md does not match sources/first_party/skills/house-skills/decisions.json")

    boundary = next((row for row in decisions if row.get("id") == "global.mark-19.source-import-boundary"), None)
    if boundary is None:
        raise ValueError("sources/first_party/skills/house-skills/decisions.json is missing the MARK-19 boundary row")
    if boundary.get("import_state") != "source-import-boundary":
        raise ValueError("sources/first_party/skills/house-skills/decisions.json has an invalid MARK-19 boundary state")
    if "global.mark-19.source-import-boundary" not in decisions_md_text:
        raise ValueError("sources/first_party/skills/house-skills/decisions.md is missing the MARK-19 boundary row")
    if "MARK-19 imports exactly six reviewed core generic buster source records" not in decisions_md_text:
        raise ValueError("sources/first_party/skills/house-skills/decisions.md is missing the MARK-19 boundary description")


def _decision_structure(record: dict[str, object]) -> dict[str, object]:
    keys = ("issue", "source_id", "source_path", "public_name", "provenance_name", "import_state", "scope")
    return {key: record.get(key, "") for key in keys}


def _resolve_vendor_root(upstream_repo: str, pinned_commit: str) -> Path:
    if upstream_repo == "mshumer/unslop":
        if pinned_commit != "edcb62386d129c65e4395f0cfcc9168eb1ba2148":
            raise ValueError("Unexpected pinned commit for mshumer/unslop vendor snapshot")
        return ROOT / "sources/third_party/unslop/upstream"
    if upstream_repo == "openai/plugins":
        if pinned_commit != "c33199897758cab145bb7fdab1ca8fb1cbd9de50":
            raise ValueError("Unexpected pinned commit for openai/plugins vendor snapshot")
        return ROOT / "sources/third_party/game-studio/upstream"
    if upstream_repo == "codewithmukesh/dotnet-claude-kit":
        if pinned_commit != "9a9a91107596b3ac3ad1d0ad5ec5eef189e74515":
            raise ValueError("Unexpected pinned commit for codewithmukesh/dotnet-claude-kit vendor snapshot")
        return ROOT / "sources/third_party/dotnet-claude-kit/upstream"
    if upstream_repo == "NickCrew/Claude-Cortex":
        if pinned_commit != "7892d00e7cb6adf00144a535103b930c772fb2c0":
            raise ValueError("Unexpected pinned commit for NickCrew/Claude-Cortex vendor snapshot")
        return ROOT / "sources/third_party/codex-cortex/upstream"
    if upstream_repo == "affaan-m/ECC":
        if pinned_commit != "ceca28852e5b31edbbf66ebccc8fd163dd14208e":
            raise ValueError("Unexpected pinned commit for affaan-m/ECC vendor snapshot")
        return ROOT / "sources/third_party/ecc/upstream"
    if upstream_repo == "https://github.com/affaan-m/ECC/tree/main/skills":
        if pinned_commit != "ceca28852e5b31edbbf66ebccc8fd163dd14208e":
            raise ValueError("Unexpected pinned commit for affaan-m/ECC vendor snapshot")
        return ROOT / "sources/third_party/ecc/upstream"
    raise ValueError(f"Unsupported upstream repo in bundle manifest: {upstream_repo}")


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
    actual_plugin_names = [plugin.get("name") for plugin in registry.get("plugins", [])]
    if actual_plugin_names != list(PROTECTED_MARKETPLACE_PLUGIN_NAMES):
        raise ValueError("Marketplace registry plugin order does not match the protected marketplace shape")
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
        spec = next((item for item in MARKETPLACE_PLUGIN_SPECS if item["name"] == name), None)
        if spec is None:
            raise ValueError(f"Marketplace registry {name} has no protected marketplace spec")
        if plugin.get("category") != spec["category"]:
            raise ValueError(f"Marketplace registry {name} category mismatch")


def validate_active_plugin_tree() -> None:
    plugin_root = ROOT / "codex-marketplace/plugins"
    expected_names = sorted(spec["name"] for spec in MARKETPLACE_PLUGIN_SPECS)
    actual_names = sorted(path.name for path in plugin_root.iterdir() if path.is_dir())
    if actual_names != expected_names:
        raise ValueError(
            "codex-marketplace/plugins contains non-protected plugin roots: "
            f"expected {expected_names}, found {actual_names}"
        )


def validate_plugin_manifest(plugin_manifest: dict, spec: dict) -> None:
    plugin_name = spec["name"]
    plugin_root = spec["plugin_root"]
    if plugin_manifest.get("name") != plugin_name:
        raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json name mismatch")
    if plugin_manifest.get("interface", {}).get("category") != spec["category"]:
        raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json category mismatch")
    if plugin_name == "superpowers-plus":
        expected_icons = {
            "composerIcon": "./assets/superpowers-small.svg",
            "logo": "./assets/app-icon.png",
        }
        expected_assets = ("assets/app-icon.png", "assets/superpowers-small.svg")
    else:
        expected_icons = {
            "composerIcon": "./assets/icon.svg",
            "logo": "./assets/icon.svg",
        }
        expected_assets = ("assets/icon.svg",)

    for key, expected in expected_icons.items():
        relative = plugin_manifest.get("interface", {}).get(key)
        if relative != expected:
            raise ValueError(f"{plugin_root}/.codex-plugin/plugin.json {key} path mismatch")
    for asset_path in expected_assets:
        check_path_exists(ROOT / plugin_root / asset_path)
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
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/house-skills":
        raise ValueError("bundle manifest plugin_root mismatch")
    if bundle_manifest.get("bundle_type") != "current-first-party-house-skills-plugin":
        raise ValueError("bundle manifest bundle_type mismatch")
    if bundle_manifest.get("skills_root") != "codex-marketplace/plugins/house-skills/skills":
        raise ValueError("bundle manifest skills_root mismatch")

    control_plane = bundle_manifest.get("control_plane_skill")
    if not isinstance(control_plane, dict):
        raise ValueError("bundle manifest control_plane_skill mismatch")
    if control_plane.get("name") != "house-skills":
        raise ValueError("bundle manifest control plane name mismatch")
    control_plane_path = control_plane.get("path")
    if control_plane_path != "codex-marketplace/plugins/house-skills/skills/house-skills":
        raise ValueError("bundle manifest control plane path mismatch")
    control_plane_root = ROOT / control_plane_path
    check_path_exists(control_plane_root)
    check_path_exists(control_plane_root / "SKILL.md")
    check_path_exists(control_plane_root / "agents" / "openai.yaml")

    skill_dir = ROOT / "codex-marketplace/plugins/house-skills/skills"
    current_skill_dirs = sorted(
        path.name for path in skill_dir.iterdir() if path.is_dir() and path.name != "house-skills"
    )
    if any(re.match(r"^v\d", path.name) for path in skill_dir.rglob("*") if path.is_dir()):
        raise ValueError("house-skills plugin root still contains live versioned subdirectories")

    skills = bundle_manifest.get("skills", [])
    if bundle_manifest.get("skill_count") != len(skills):
        raise ValueError("bundle manifest skill_count mismatch")
    if len(skills) != len(current_skill_dirs):
        raise ValueError("bundle manifest skill inventory count mismatch")

    manifest_names: list[str] = []
    for entry in skills:
        if not isinstance(entry, dict):
            raise ValueError("bundle manifest skills must contain objects")
        name = entry.get("name")
        lane = entry.get("lane")
        path = entry.get("path")
        if not name or not isinstance(name, str):
            raise ValueError("bundle manifest skill entry is missing a name")
        if not lane or not isinstance(lane, str):
            raise ValueError(f"bundle manifest skill {name} is missing a lane")
        if not path or not isinstance(path, str):
            raise ValueError(f"bundle manifest skill {name} is missing a path")
        expected_lane = (
            "Adventures"
            if name.startswith("adventures-")
            else "Rooms"
            if name.startswith("rooms-")
            else "Wild Bunch"
            if name.startswith("wild-bunch-")
            else "Base and control plane"
        )
        if lane != expected_lane:
            raise ValueError(f"bundle manifest skill {name} lane mismatch")
        check_path_exists(ROOT / path)
        skill_root = ROOT / path
        if skill_root.name != name:
            raise ValueError(f"bundle manifest skill {name} path mismatch")
        check_path_exists(skill_root / "SKILL.md")
        check_path_exists(skill_root / "agents" / "openai.yaml")
        manifest_names.append(name)

    if sorted(manifest_names) != current_skill_dirs:
        raise ValueError("bundle manifest skill inventory does not match the live plugin root")

    archive_roots = bundle_manifest.get("archive_roots", [])
    if archive_roots:
        raise ValueError("bundle manifest archive_roots must be absent in the reduced marketplace")

    notes = bundle_manifest.get("notes", [])
    if not isinstance(notes, list) or len(notes) < 1:
        raise ValueError("bundle manifest notes mismatch")


def validate_wild_bunch_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    if bundle_manifest.get("bundle_name") != "wild-bunch-project-pack":
        raise ValueError("wild-bunch-project-pack bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError("wild-bunch-project-pack bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") != "project-scoped-codex-plugin-projection":
        raise ValueError("wild-bunch-project-pack bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("wild-bunch-project-pack bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/wild-bunch-project-pack":
        raise ValueError("wild-bunch-project-pack bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_roots") != [
        "sources/first_party/skills",
        "sources/third_party/game-studio/upstream/skills",
    ]:
        raise ValueError("wild-bunch-project-pack bundle manifest canonical_source_roots mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "sources/first_party/skills/wild-bunch-browser-game/SKILL.md",
        "sources/first_party/skills/wild-bunch-domain-modeling/SKILL.md",
        "sources/first_party/skills/wild-bunch-dotnet-architecture/SKILL.md",
        "sources/first_party/skills/wild-bunch-project-doctrine/SKILL.md",
        "sources/first_party/skills/wild-bunch-worker-verification/SKILL.md",
        "sources/third_party/game-studio/upstream/.codex-plugin/plugin.json",
        "sources/third_party/game-studio/upstream/skills/web-game-foundations/SKILL.md",
    ]:
        raise ValueError("wild-bunch-project-pack bundle manifest source_of_truth mismatch")
    if bundle_manifest.get("projection_policy") != (
        "Project the five hydrated first-party Wild Bunch skills together with the retained browser-game helper skills in a self-contained bundle. Do not depend on another plugin at install time."
    ):
        raise ValueError("wild-bunch-project-pack bundle manifest projection_policy mismatch")

    entries = bundle_manifest.get("entries", [])
    if bundle_manifest.get("candidate_count") != len(entries):
        raise ValueError("wild-bunch-project-pack bundle manifest candidate count mismatch")

    imported_entries = [entry for entry in entries if entry.get("import_status") == "imported"]
    blocked_entries = [entry for entry in entries if entry.get("import_status") == "blocked"]
    if bundle_manifest.get("imported_count") != len(imported_entries):
        raise ValueError("wild-bunch-project-pack bundle manifest imported count mismatch")
    if bundle_manifest.get("blocked_count") != len(blocked_entries):
        raise ValueError("wild-bunch-project-pack bundle manifest blocked count mismatch")
    if bundle_manifest.get("skipped_count") != 0:
        raise ValueError("wild-bunch-project-pack bundle manifest skipped count mismatch")

    skill_dir = ROOT / plugin_root / "skills"
    actual_skill_dirs = sorted(path.name for path in skill_dir.iterdir() if path.is_dir())
    imported_skill_dirs = sorted(
        Path(entry["local_path"]).parts[1]
        for entry in imported_entries
        if isinstance(entry.get("local_path"), str)
        and Path(entry["local_path"]).parts[:1] == ("skills",)
        and len(Path(entry["local_path"]).parts) >= 3
    )
    if actual_skill_dirs != imported_skill_dirs:
        raise ValueError("wild-bunch-project-pack bundle manifest imported skill inventory mismatch")

    for entry in imported_entries:
        canonical_name = entry.get("canonical_name")
        if not canonical_name or not isinstance(canonical_name, str):
            raise ValueError("wild-bunch-project-pack imported entry is missing canonical_name")
        if entry.get("source_category") not in {"first_party", "third_party"}:
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} has an invalid source_category")
        if entry.get("content_mode") != "verbatim":
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} must be verbatim")
        if entry.get("copy_expectation") != "byte_identical":
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} copy expectation mismatch")
        if not entry.get("provenance_note"):
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} needs a provenance note")

        canonical_source_path = entry.get("canonical_source_path")
        local_path = entry.get("local_path")
        if not isinstance(canonical_source_path, str) or not canonical_source_path:
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} is missing canonical_source_path")
        if not isinstance(local_path, str) or not local_path:
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} is missing local_path")
        check_path_exists(ROOT / canonical_source_path)
        check_path_exists(ROOT / plugin_root / local_path)
        if (ROOT / canonical_source_path).read_bytes() != (ROOT / plugin_root / local_path).read_bytes():
            raise ValueError(f"wild-bunch-project-pack entry {canonical_name} drifted from its source copy")

    if len(blocked_entries) != 1:
        raise ValueError("wild-bunch-project-pack bundle manifest must contain one blocked entry")
    blocked = blocked_entries[0]
    if blocked.get("canonical_name") != "agent-browser":
        raise ValueError("wild-bunch-project-pack blocked entry must be agent-browser")
    if blocked.get("local_path") is not None:
        raise ValueError("wild-bunch-project-pack blocked entry must not expose a local path")
    if blocked.get("canonical_source_path") is not None:
        raise ValueError("wild-bunch-project-pack blocked entry must not expose a canonical source path")
    if blocked.get("copy_expectation") != "not_copied":
        raise ValueError("wild-bunch-project-pack blocked entry copy expectation mismatch")
    if not blocked.get("provenance_note"):
        raise ValueError("wild-bunch-project-pack blocked entry needs a provenance note")

    notes = bundle_manifest.get("notes", [])
    if not isinstance(notes, list) or len(notes) < 3:
        raise ValueError("wild-bunch-project-pack bundle manifest notes mismatch")


def normalize_superpowers_projection_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("**", "").lower()).strip()


def _expected_superpowers_projected_plugin(source_plugin: dict) -> dict:
    projected_plugin = json.loads(json.dumps(source_plugin))
    projected_plugin["name"] = "superpowers-plus"
    interface = projected_plugin.get("interface")
    if isinstance(interface, dict):
        interface["displayName"] = "Superpowers+"
    return projected_plugin


def validate_superpowers_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    source_root = ROOT / "sources/third_party/superpowers/obra-superpowers/v5.1.0"
    if bundle_manifest.get("bundle_name") != "superpowers-plus":
        raise ValueError("superpowers-plus bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "5.1.0":
        raise ValueError("superpowers-plus bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") != "third-party-codex-plugin-projection":
        raise ValueError("superpowers-plus bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("superpowers-plus bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/superpowers-plus":
        raise ValueError("superpowers-plus bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_root") != "sources/third_party/superpowers/obra-superpowers/v5.1.0":
        raise ValueError("superpowers-plus bundle manifest canonical_source_root mismatch")
    if bundle_manifest.get("source_tag") != "v5.1.0":
        raise ValueError("superpowers-plus bundle manifest source_tag mismatch")
    if bundle_manifest.get("source_commit") != "f2cbfbefebbfef77321e4c9abc9e949826bea9d7":
        raise ValueError("superpowers-plus bundle manifest source_commit mismatch")
    if bundle_manifest.get("license") != "MIT":
        raise ValueError("superpowers-plus bundle manifest license mismatch")
    if bundle_manifest.get("projection_policy") != (
        "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody."
    ):
        raise ValueError("superpowers-plus bundle manifest projection_policy mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
    ]:
        raise ValueError("superpowers-plus bundle manifest source_of_truth mismatch")

    source_plugin = json.loads((source_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    projected_plugin = json.loads((ROOT / plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    expected_projected_plugin = _expected_superpowers_projected_plugin(source_plugin)
    if expected_projected_plugin != projected_plugin:
        raise ValueError("superpowers-plus projection drift at .codex-plugin/plugin.json")

    for relative_path in (
        "LICENSE",
        "assets/app-icon.png",
        "assets/superpowers-small.svg",
    ):
        source_bytes = (source_root / relative_path).read_bytes()
        projected_bytes = (ROOT / plugin_root / relative_path).read_bytes()
        if source_bytes != projected_bytes:
            raise ValueError(f"superpowers-plus projection drift at {relative_path}")

    entries = bundle_manifest.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError("superpowers-plus bundle manifest entries must be a non-empty list")
    if bundle_manifest.get("candidate_count") != len(entries):
        raise ValueError("superpowers-plus bundle manifest candidate count mismatch")
    if bundle_manifest.get("imported_count") != len(entries):
        raise ValueError("superpowers-plus bundle manifest imported count mismatch")
    if bundle_manifest.get("skipped_count") != 0:
        raise ValueError("superpowers-plus bundle manifest skipped count mismatch")
    if bundle_manifest.get("blocked_count") != 0:
        raise ValueError("superpowers-plus bundle manifest blocked count mismatch")

    support_entries = bundle_manifest.get("excluded", [])
    if not isinstance(support_entries, list) or len(support_entries) != 7:
        raise ValueError("superpowers-plus bundle manifest excluded support surface count mismatch")

    projection_doc = (ROOT / plugin_root / "PROJECTION.md").read_text(encoding="utf-8")
    compatibility_doc = (ROOT / plugin_root / "references" / "codex-marketplace-compatibility.md").read_text(
        encoding="utf-8"
    )
    for needle in (
        "source custody -> projection layer -> installation/export layer",
        "Source custody keeps the retained third-party snapshot verbatim.",
        "Projection layer holds the source-controlled marketplace copy",
        "Installation/export layer is derived from the projection plus overlays",
        "docs/contracts/skill-frontmatter.md",
        "docs/contracts/openai-agent-yaml.md",
    ):
        if needle not in projection_doc:
            raise ValueError(f"superpowers PROJECTION.md is missing the three-layer model text: {needle}")
    for needle in (
        "lives only in the projection layer",
        "Source custody remains a verbatim upstream snapshot",
        "Installation and export artifacts are derived from the projection layer plus overlays",
        "docs/contracts/skill-frontmatter.md",
        "docs/contracts/openai-agent-yaml.md",
    ):
        if needle not in compatibility_doc:
            raise ValueError(
                f"superpowers codex-marketplace-compatibility note is missing the custody split text: {needle}"
            )

    _validate_superpowers_provenance_map(bundle_manifest, plugin_root)
    _validate_repo_index_metadata(bundle_manifest.get("repo_index"), bundle_name="superpowers-plus", plugin_root=plugin_root)

    skill_dir = ROOT / plugin_root / "skills"
    actual_skill_dirs = sorted(path.name for path in skill_dir.iterdir() if path.is_dir())
    imported_skill_dirs = sorted(
        Path(entry["local_path"]).parts[1]
        for entry in entries
        if isinstance(entry.get("local_path"), str)
        and Path(entry["local_path"]).parts[:1] == ("skills",)
        and len(Path(entry["local_path"]).parts) >= 2
    )
    if actual_skill_dirs != imported_skill_dirs:
        raise ValueError("superpowers-plus bundle manifest imported skill inventory mismatch")

    for entry in entries:
        canonical_name = entry.get("canonical_name")
        if not canonical_name or not isinstance(canonical_name, str):
            raise ValueError("superpowers-plus imported entry is missing canonical_name")
        canonical_source_path = entry.get("canonical_source_path")
        source_category = entry.get("source_category")
        if source_category not in {"third_party", "first_party"}:
            raise ValueError(f"superpowers-plus entry {canonical_name} has an invalid source_category")
        if source_category == "first_party":
            expected_source_path = FIRST_PARTY_SUPERPOWERS_SOURCES.get(canonical_name)
            if expected_source_path is None:
                allowed = ", ".join(sorted(FIRST_PARTY_SUPERPOWERS_SOURCES))
                raise ValueError(f"superpowers-plus first-party projections are limited to {allowed}")
            if canonical_source_path != expected_source_path:
                raise ValueError(f"superpowers-plus {canonical_name} first-party source path mismatch")
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "adapted"}:
            raise ValueError(f"superpowers-plus entry {canonical_name} has an invalid content_mode")
        copy_expectation = entry.get("copy_expectation")
        if content_mode == "verbatim":
            if copy_expectation != "byte_identical":
                raise ValueError(f"superpowers-plus entry {canonical_name} copy expectation mismatch")
        elif copy_expectation not in {"adapted_from_source", "documented_adaptation"}:
            raise ValueError(f"superpowers-plus entry {canonical_name} copy expectation mismatch")
        if not entry.get("provenance_note"):
            raise ValueError(f"superpowers-plus entry {canonical_name} needs a provenance note")
        if content_mode == "adapted" and not entry.get("adaptation_note"):
            raise ValueError(f"superpowers-plus entry {canonical_name} needs an adaptation note")
        adaptation_overlay_path = entry.get("adaptation_overlay_path")
        if source_category == "third_party" and content_mode == "adapted":
            expected_overlay_path = f"adaptation-overlays/superpowers-plus/{canonical_name}"
            if adaptation_overlay_path != expected_overlay_path:
                raise ValueError(f"superpowers-plus adapted entry {canonical_name} needs {expected_overlay_path}")
            check_path_exists(ROOT / expected_overlay_path)
        elif adaptation_overlay_path is not None:
            raise ValueError(f"superpowers-plus verbatim entry {canonical_name} must not declare adaptation_overlay_path")

        local_path = entry.get("local_path")
        if not isinstance(canonical_source_path, str) or not canonical_source_path:
            raise ValueError(f"superpowers-plus entry {canonical_name} is missing canonical_source_path")
        if not isinstance(local_path, str) or not local_path:
            raise ValueError(f"superpowers-plus entry {canonical_name} is missing local_path")
        _validate_projection_entry_provenance(entry, bundle_name="superpowers-plus")
        check_path_exists(ROOT / canonical_source_path)
        check_path_exists(ROOT / plugin_root / local_path)
        source_path = ROOT / canonical_source_path
        local_full_path = ROOT / plugin_root / local_path
        validate_skill_markdown_frontmatter(local_full_path)
        if source_path.is_dir():
            if content_mode == "verbatim":
                if canonical_name == "ecc-superpowers":
                    source_skill = source_path / "SKILL.md"
                    projected_skill = local_full_path / "SKILL.md"
                    _, source_body = _split_skill_frontmatter_and_body(source_skill)
                    _, projected_body = _split_skill_frontmatter_and_body(projected_skill)
                    if source_body != projected_body:
                        raise ValueError(f"superpowers-plus entry {canonical_name} drifted from its source copy")
                    source_agent = source_path / "agents" / "openai.yaml"
                    projected_agent = local_full_path / "agents" / "openai.yaml"
                    if source_agent.read_bytes() != projected_agent.read_bytes():
                        raise ValueError(f"superpowers-plus entry {canonical_name} drifted from its source copy")
                else:
                    validate_tree_mirror(source_path, local_full_path, canonical_name)
            else:
                validate_openai_agent_yaml(local_full_path / "agents" / "openai.yaml")
                if adaptation_overlay_path is None:
                    if canonical_name != "ecc-superpowers":
                        raise ValueError(f"superpowers-plus adapted entry {canonical_name} needs an overlay path")
                    source_skill = source_path / "SKILL.md"
                    projected_skill = local_full_path / "SKILL.md"
                    _, source_body = _split_skill_frontmatter_and_body(source_skill)
                    _, projected_body = _split_skill_frontmatter_and_body(projected_skill)
                    if source_body != projected_body:
                        raise ValueError(f"superpowers-plus entry {canonical_name} drifted from its source copy")
                    source_agent = source_path / "agents" / "openai.yaml"
                    projected_agent = local_full_path / "agents" / "openai.yaml"
                    if source_agent.read_bytes() != projected_agent.read_bytes():
                        raise ValueError(f"superpowers-plus entry {canonical_name} drifted from its source copy")
                else:
                    overlay_root = ROOT / adaptation_overlay_path
                    validate_tree_reconstruction(source_path, overlay_root, local_full_path, canonical_name)
        else:
            if content_mode == "verbatim" and source_path.read_bytes() != local_full_path.read_bytes():
                raise ValueError(f"superpowers-plus entry {canonical_name} drifted from its source copy")

    expected_support_paths = {
        ".claude-plugin": "Claude harness metadata",
        ".cursor-plugin": "Cursor harness metadata",
        ".opencode": "OpenCode harness metadata",
        "gemini-extension.json": "Gemini harness metadata",
        "CLAUDE.md": "Claude instructions",
        "GEMINI.md": "Gemini instructions",
        "hooks": "harness hook support",
    }
    support_paths = {}
    for entry in support_entries:
        if not isinstance(entry, dict):
            raise ValueError("superpowers-plus excluded entries must contain objects")
        path = entry.get("path")
        reason = entry.get("reason")
        if not isinstance(path, str) or not path:
            raise ValueError("superpowers-plus excluded entry is missing path")
        if not isinstance(reason, str) or not reason:
            raise ValueError(f"superpowers-plus excluded entry {path} needs a reason")
        support_paths[path] = reason

    if set(support_paths) != set(expected_support_paths):
        raise ValueError("superpowers-plus bundle manifest excluded support surface mismatch")

    for path in expected_support_paths:
        check_path_exists(source_root / path)
        if (ROOT / plugin_root / path).exists():
            raise ValueError(f"superpowers-plus support surface {path} must not be projected")

    for required in (
        ROOT / plugin_root / ".codex-plugin" / "plugin.json",
        ROOT / plugin_root / "LICENSE",
        ROOT / plugin_root / "SOURCE.md",
        ROOT / plugin_root / "PROJECTION.md",
        ROOT / plugin_root / "references" / "codex-marketplace-compatibility.md",
        ROOT / plugin_root / "references" / "bundle-manifest.json",
        ROOT / plugin_root / "references" / "provenance-map.json",
        ROOT / plugin_root / "assets" / "app-icon.png",
        ROOT / plugin_root / "assets" / "superpowers-small.svg",
    ):
        check_path_exists(required)

    actual_top_level = sorted(path.name for path in (ROOT / plugin_root).iterdir())
    allowed_top_level = sorted(
        [
            ".codex-plugin",
            "LICENSE",
            "PROJECTION.md",
            "SOURCE.md",
            "assets",
            "references",
            "skills",
        ]
    )
    if actual_top_level != allowed_top_level:
        raise ValueError("superpowers plugin root contains unexpected top-level content")


def validate_skill_bundle_manifest(
    bundle_manifest: dict,
    *,
    bundle_name: str,
    plugin_root: str,
) -> None:
    if bundle_manifest.get("bundle_name") != bundle_name:
        raise ValueError(f"{bundle_name} bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError(f"{bundle_name} bundle manifest bundle_version mismatch")
    
    # First-party bundles don't require upstream_repo, pinned_commit, source_root
    bundle_type = bundle_manifest.get("bundle_type")
    if bundle_type and "first-party" in bundle_type:
        # First-party bundle validation
        if not bundle_manifest.get("plugin_root"):
            raise ValueError(f"{bundle_name} bundle manifest plugin_root missing")
        if not bundle_manifest.get("skills_root"):
            raise ValueError(f"{bundle_name} bundle manifest skills_root missing")
        return
    
    # Third-party bundle validation requires upstream fields
    upstream_repo = bundle_manifest.get("upstream_repo")
    if not upstream_repo or not isinstance(upstream_repo, str):
        raise ValueError(f"{bundle_name} bundle manifest upstream_repo mismatch")
    pinned_commit = bundle_manifest.get("pinned_commit")
    if not pinned_commit or not isinstance(pinned_commit, str):
        raise ValueError(f"{bundle_name} bundle manifest pinned_commit mismatch")
    source_root = bundle_manifest.get("source_root")
    if not source_root or not isinstance(source_root, str):
        raise ValueError(f"{bundle_name} bundle manifest source_root mismatch")
    vendor_root: Path | None = None
    source_family_roots: dict[str, Path] | None = None

    if bundle_name == "superpowers-ecc":
        check_path_exists(ROOT / "sources/third_party/ecc/upstream/LICENSE")

    if bundle_name == "security-pack" and isinstance(bundle_manifest.get("source_families"), list):
        source_family_roots = {}
        for family in bundle_manifest["source_families"]:
            if not isinstance(family, dict):
                raise ValueError("security-pack bundle manifest source_families must contain objects")
            family_name = family.get("name")
            family_upstream_repo = family.get("upstream_repo")
            family_pinned_commit = family.get("pinned_commit")
            family_source_root = family.get("source_root")
            if not family_name or not isinstance(family_name, str):
                raise ValueError("security-pack bundle manifest source_families entry name mismatch")
            if family_name in source_family_roots:
                raise ValueError("security-pack bundle manifest source_families entry name duplicated")
            if not family_upstream_repo or not isinstance(family_upstream_repo, str):
                raise ValueError("security-pack bundle manifest source_families upstream_repo mismatch")
            if not family_pinned_commit or not isinstance(family_pinned_commit, str):
                raise ValueError("security-pack bundle manifest source_families pinned_commit mismatch")
            if not family_source_root or not isinstance(family_source_root, str):
                raise ValueError("security-pack bundle manifest source_families source_root mismatch")
            family_vendor_root = _resolve_vendor_root(family_upstream_repo, family_pinned_commit)
            resolved_family_root = family_vendor_root / family_source_root
            check_path_exists(resolved_family_root)
            source_family_roots[family_name] = resolved_family_root
        check_path_exists(ROOT / plugin_root / source_root)
    elif bundle_type and "first-party" in bundle_type:
        # First-party bundles don't have vendor roots to validate
        pass
    else:
        vendor_root = _resolve_vendor_root(upstream_repo, pinned_commit)
        check_path_exists(vendor_root / source_root)

    _validate_repo_index_metadata(bundle_manifest.get("repo_index"), bundle_name=bundle_name, plugin_root=plugin_root)

    entries = bundle_manifest.get("entries", [])
    if bundle_manifest.get("candidate_count") != len(entries):
        raise ValueError(f"{bundle_name} bundle manifest candidate count mismatch")

    allowed_statuses = {"imported", "out_of_scope", "blocked"}
    statuses = {entry.get("import_status") for entry in entries}
    if not statuses.issubset(allowed_statuses):
        raise ValueError(f"{bundle_name} bundle manifest contains unrecognized import status values")

    imported_entries = [entry for entry in entries if entry.get("import_status") == "imported"]
    skipped_entries = [entry for entry in entries if entry.get("import_status") == "out_of_scope"]
    blocked_entries = [entry for entry in entries if entry.get("import_status") == "blocked"]
    if len(imported_entries) + len(skipped_entries) + len(blocked_entries) != len(entries):
        raise ValueError(f"{bundle_name} bundle manifest import buckets do not sum to candidate_count")
    if bundle_manifest.get("imported_count") != len(imported_entries):
        raise ValueError(f"{bundle_name} bundle manifest imported count mismatch")
    if bundle_manifest.get("skipped_count") != len(skipped_entries):
        raise ValueError(f"{bundle_name} bundle manifest skipped count mismatch")
    if bundle_manifest.get("blocked_count") != len(blocked_entries):
        raise ValueError(f"{bundle_name} bundle manifest blocked count mismatch")

    skill_dir = ROOT / plugin_root / "skills"
    actual_skill_dirs = [path for path in skill_dir.iterdir() if path.is_dir()]
    imported_skill_dirs = {
        Path(entry["local_path"]).parts[1]
        for entry in imported_entries
        if isinstance(entry.get("local_path"), str)
        and Path(entry["local_path"]).parts[:1] == ("skills",)
        and len(Path(entry["local_path"]).parts) >= 3
    }
    if len(actual_skill_dirs) != len(imported_skill_dirs):
        raise ValueError(f"{bundle_name} bundle manifest imported skill directory count does not match copied skills")

    for entry in imported_entries:
        local_path = entry.get("local_path")
        if not local_path or not isinstance(local_path, str):
            raise ValueError(f"{bundle_name} bundle manifest imported entry is missing a local_path")
        check_path_exists(ROOT / plugin_root / local_path)
        snapshot_path = entry.get("snapshot_path")
        if not snapshot_path or not isinstance(snapshot_path, str):
            raise ValueError(f"{bundle_name} bundle manifest imported entry is missing a snapshot_path")
        if bundle_name == "superpowers-ecc":
            for field in ("source_path", "source_author", "source_license", "source_repo"):
                if not isinstance(entry.get(field), str) or not entry.get(field):
                    raise ValueError(f"{bundle_name} bundle manifest imported entry is missing {field}")
        entry_vendor_root = vendor_root
        if source_family_roots is not None:
            source_family = entry.get("source_family")
            if not source_family or not isinstance(source_family, str):
                raise ValueError(f"{bundle_name} bundle manifest imported entry is missing a source_family")
            entry_vendor_root = source_family_roots.get(source_family)
            if entry_vendor_root is None:
                raise ValueError(
                    f"{bundle_name} bundle manifest imported entry uses an unknown source_family: {source_family}"
                )
        assert entry_vendor_root is not None
        check_path_exists(entry_vendor_root / snapshot_path)
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "adapted"}:
            raise ValueError(f"{bundle_name} bundle manifest imported entry has invalid content_mode")
        if not entry.get("adaptation_note"):
            raise ValueError(f"{bundle_name} bundle manifest imported entry requires an adaptation note")
        if content_mode == "verbatim":
            source_path = entry_vendor_root / snapshot_path
            projected_path = ROOT / plugin_root / local_path
            if bundle_name == "superpowers-ecc":
                _, source_body = _split_skill_frontmatter_and_body(source_path)
                _, projected_body = _split_skill_frontmatter_and_body(projected_path)
                if source_body != projected_body:
                    raise ValueError(
                        f"{bundle_name} bundle manifest imported entry {local_path} drifted from retained snapshot"
                    )
            else:
                source_bytes = source_path.read_bytes()
                projected_bytes = projected_path.read_bytes()
                if source_bytes != projected_bytes:
                    raise ValueError(
                        f"{bundle_name} bundle manifest imported entry {local_path} drifted from retained snapshot"
                    )
        elif content_mode == "adapted" and not entry.get("adaptation_note"):
            raise ValueError(f"{bundle_name} bundle manifest adapted entry requires an adaptation note")

    for entry in skipped_entries + blocked_entries:
        if entry.get("local_path") not in ("", None):
            raise ValueError(f"{bundle_name} bundle manifest skipped/blocked entry should not expose a local path")
        if not entry.get("adaptation_note"):
            raise ValueError(f"{bundle_name} bundle manifest skipped/blocked entry requires an adaptation note")


def validate_project_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    if bundle_manifest.get("bundle_name") != "adventures-pack":
        raise ValueError("adventures-pack bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError("adventures-pack bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") != "project-scoped-codex-plugin-projection":
        raise ValueError("adventures-pack bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("adventures-pack bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/adventures-pack":
        raise ValueError("adventures-pack bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_root") != "codex-marketplace/plugins/house-skills/skills":
        raise ValueError("adventures-pack bundle manifest canonical_source_root mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "sources/first_party/skills/house-skills/decisions.json",
        "sources/first_party/skills/house-skills/decisions.md",
        "sources/first_party/skills/house-skills/intake.json",
        "provenance/house-skills.md",
    ]:
        raise ValueError("adventures-pack bundle manifest source_of_truth mismatch")

    components = bundle_manifest.get("components", [])
    if not isinstance(components, list) or not components:
        raise ValueError("adventures-pack bundle manifest components must be a non-empty list")

    skill_dir = ROOT / plugin_root / "skills"
    check_path_exists(skill_dir / "adventures-pack" / "SKILL.md")

    actual_skill_dirs = [path for path in skill_dir.iterdir() if path.is_dir() and path.name != "adventures-pack"]
    if len(actual_skill_dirs) != len(components):
        raise ValueError("adventures-pack bundle manifest component directory count does not match copied skills")

    adventure_count = 0
    dependency_count = 0
    seen_local_paths: set[str] = set()

    for component in components:
        if not isinstance(component, dict):
            raise ValueError("adventures-pack bundle manifest components must contain objects")
        canonical_name = component.get("canonical_name")
        component_version = component.get("component_version")
        source_path = component.get("source_path")
        local_path = component.get("local_path")
        role = component.get("role")
        projection_status = component.get("projection_status")

        if not canonical_name or not isinstance(canonical_name, str):
            raise ValueError("adventures-pack bundle manifest component is missing canonical_name")
        if not component_version or not isinstance(component_version, str):
            raise ValueError(f"adventures-pack bundle manifest component {canonical_name} is missing component_version")
        if not source_path or not isinstance(source_path, str):
            raise ValueError(f"adventures-pack bundle manifest component {canonical_name} is missing source_path")
        if not local_path or not isinstance(local_path, str):
            raise ValueError(f"adventures-pack bundle manifest component {canonical_name} is missing local_path")
        if local_path in seen_local_paths:
            raise ValueError(f"adventures-pack bundle manifest component local path is duplicated: {local_path}")
        seen_local_paths.add(local_path)

        if role not in {"adventures", "dependency"}:
            raise ValueError(f"adventures-pack bundle manifest component {canonical_name} has an unsupported role")
        if projection_status != "projected":
            raise ValueError(f"adventures-pack bundle manifest component {canonical_name} must be projected")

        source_md = ROOT / source_path
        local_md = ROOT / plugin_root / local_path
        check_path_exists(source_md)
        check_path_exists(local_md)
        validate_tree_mirror(source_md.parent, local_md.parent, canonical_name)

        if role == "adventures":
            adventure_count += 1
            if component_version != "v1.1":
                raise ValueError(f"adventures-pack bundle manifest component {canonical_name} must be v1.1")
        else:
            dependency_count += 1
            if component_version not in {"v1", "v0.1"}:
                raise ValueError(f"adventures-pack bundle manifest component {canonical_name} has an unexpected dependency version")

    if adventure_count != 10:
        raise ValueError("adventures-pack bundle manifest must project ten clean Adventures components")
    if dependency_count != 7:
        raise ValueError("adventures-pack bundle manifest must project seven generic dependency components")

    for required in (
        ROOT / plugin_root / "README.md",
        ROOT / plugin_root / "SOURCE.md",
        ROOT / plugin_root / "LICENSE",
        ROOT / plugin_root / ".codex-plugin" / "plugin.json",
        ADVENTURES_PACK_SOURCE_MAP_PATH,
        ADVENTURES_PACK_BUNDLE_MANIFEST_PATH,
        ADVENTURES_PACK_SKILL_PATH,
    ):
        check_path_exists(required)


def validate_source_map(text: str) -> None:
    for needle in (
        "codex-marketplace/plugins/house-skills/skills/",
        "codex-marketplace/plugins/house-skills/skills/house-skills",
        "codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json",
        "All live current roots are unversioned directory-level plugin folders with `SKILL.md` and `agents/openai.yaml`.",
    ):
        if needle not in text:
            raise ValueError(f"source map is missing {needle}")


def main() -> int:
    decisions = check_json(SOURCE_DECISIONS_JSON_PATH)
    intake = check_json(SOURCE_INTAKE_JSON_PATH)
    plugin_manifests: list[dict] = []
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec)
        plugin_manifests.append(plugin_manifest)
    registry = check_json(MARKETPLACE_PATH)
    bundle_manifest = check_json(BUNDLE_MANIFEST_PATH)
    decisions_md_text = check_text(SOURCE_DECISIONS_MD_PATH)
    decision_rows = parse_top_markdown_table(SOURCE_DECISIONS_MD_PATH)

    validate_decisions(decisions, decision_rows, decisions_md_text)
    validate_marketplace_registry(registry, plugin_manifests)
    validate_active_plugin_tree()
    validate_skill_zip_registry()
    codex_manifest = check_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    if codex_manifest != registry:
        raise ValueError("codex-marketplace/manifest.json does not match .agents/plugins/marketplace.json")
    validate_bundle_manifest(bundle_manifest, intake)
    for spec in MARKETPLACE_PLUGIN_SPECS:
        if spec["name"] == "house-skills":
            continue
        plugin_root = ROOT / spec["plugin_root"]
        if spec["name"] == "superpowers-plus":
            for required in ("SOURCE.md", "PROJECTION.md", "LICENSE"):
                check_text(plugin_root / required)
            check_json(plugin_root / ".codex-plugin" / "plugin.json")
            check_path_exists(plugin_root / "assets" / "app-icon.png")
            check_path_exists(plugin_root / "assets" / "superpowers-small.svg")
        else:
            for required in ("README.md", "SOURCE.md", "LICENSE"):
                check_text(plugin_root / required)
            if (plugin_root / "package.json").exists():
                check_json(plugin_root / "package.json")
            check_path_exists(plugin_root / "assets/icon.svg")

        bundle_path = plugin_root / "references/bundle-manifest.json"
        if bundle_path.exists():
            bundle_manifest_json = check_json(bundle_path)
            if spec["name"] == "adventures-pack":
                validate_project_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            elif spec["name"] == "wild-bunch-project-pack":
                validate_wild_bunch_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            elif spec["name"] == "superpowers-plus":
                validate_superpowers_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            elif spec["name"] == "everything-codex-code":
                validate_everything_codex_code_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            else:
                validate_skill_bundle_manifest(
                    bundle_manifest_json,
                    bundle_name=spec["name"],
                    plugin_root=spec["plugin_root"],
                )

    source_map = check_text(SOURCE_MAP_PATH)
    validate_source_map(source_map)
    check_json(PLUGIN_ROOT_INVENTORY_PATH)
    check_text(ROOT / "codex-marketplace/README.md")
    check_text(ROOT / "codex-marketplace/plugins/README.md")
    check_text(PLUGIN_README_PATH)
    check_text(PLUGIN_SKILL_PATH)
    check_text(PLUGIN_BUNDLE_AGENTS_PATH)
    check_text(PROVENANCE_PATH)
    check_text(ROOT / "provenance/MARK-99-unslop.md")
    check_text(REPO_INDEX_README_PATH)
    check_json(REPO_INDEX_PATH)
    validate_repo_index()

    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
