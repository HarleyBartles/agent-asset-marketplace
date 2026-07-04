#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

from skill_overlay_materializer import stage_overlay_tree, validate_openai_agent_yaml
from tree_canonicalization import canonicalize_tree_bytes as _canonicalize_tree_bytes, compare_trees_canonicalized
from superpowers_source import superpowers_source_commit, superpowers_source_root, superpowers_source_tag


ROOT = Path(__file__).resolve().parents[1]


def _bootstrap_marketplace_dependencies() -> None:
    marketplace_utils = importlib.import_module("marketplace_utils")
    for name in (
        "CODEX_MARKETPLACE_MANIFEST_PATH",
        "BUNDLE_MANIFEST_PATH",
        "EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES",
        "EXPECTED_MARKETPLACE",
        "MARKETPLACE_PATH",
        "MARKETPLACE_PLUGIN_SPECS",
        "PROTECTED_MARKETPLACE_PLUGIN_NAMES",
        "PLUGIN_README_PATH",
        "PLUGIN_SKILL_PATH",
        "PROVENANCE_PATH",
        "PLUGIN_BUNDLE_AGENTS_PATH",
        "ADVENTURES_PACK_BUNDLE_MANIFEST_PATH",
        "ADVENTURES_PACK_SOURCE_MAP_PATH",
        "ADVENTURES_PACK_SKILL_PATH",
        "SOURCE_DECISIONS_JSON_PATH",
        "SOURCE_DECISIONS_MD_PATH",
        "SOURCE_INTAKE_JSON_PATH",
        "SOURCE_MAP_PATH",
        "PLUGIN_ROOT_INVENTORY_PATH",
        "REPO_INDEX_PATH",
        "REPO_INDEX_README_PATH",
        "build_marketplace_manifest",
        "load_json",
        "normalize_decision_record",
        "normalize_decision_row",
        "parse_top_markdown_table",
        "_installation_policy_for_plugin",
    ):
        globals()[name] = getattr(marketplace_utils, name)

    globals()["validate_repo_index"] = importlib.import_module("validate_repo_index").validate_repo_index
    skill_zip_artifacts = importlib.import_module("skill_zip_artifacts")
    globals()["validate_skill_markdown_frontmatter"] = skill_zip_artifacts.validate_skill_markdown_frontmatter
    globals()["validate_skill_zip_registry"] = skill_zip_artifacts.validate_skill_zip_registry


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


def _run_tool_check(command: list[str], label: str) -> None:
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - exercised via integration checks
        raise ValueError(f"{label} failed with exit code {exc.returncode}") from exc


def validate_projection_materializer() -> None:
    _run_tool_check([sys.executable, "tools/materialize_projection.py", "--check"], "projection materializer check")


def validate_pack_manifests() -> None:
    _run_tool_check(
        [sys.executable, "tools/generate_pack_manifests.py", "--check"],
        "pack manifest generator check",
    )


def list_files(root: Path) -> list[Path]:
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


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


def _files_match_canonicalized(source_path: Path, projected_path: Path) -> bool:
    source_bytes = _canonicalize_tree_bytes(source_path, source_path.read_bytes())
    projected_bytes = _canonicalize_tree_bytes(projected_path, projected_path.read_bytes())
    return source_bytes == projected_bytes


def _trees_match_canonicalized(source_root: Path, projected_root: Path) -> None:
    if not source_root.is_dir():
        raise ValueError(f"{source_root} must be a directory")
    if not projected_root.is_dir():
        raise ValueError(f"{projected_root} must be a directory")
    compare_trees_canonicalized(source_root, projected_root)


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
        and entry.get("content_mode") == "verbatim"
    }
    expected_adapted = {
        entry["canonical_name"]: entry
        for entry in bundle_manifest.get("entries", [])
        if isinstance(entry, dict)
        and entry.get("content_mode") in ("adapted", "normalised")
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
    
    # MARK-262: Adapted and normalised entries must have source authorship fields
    # Verbatim entries should NOT have these at entry level (byte-identical to upstream)
    if content_mode in ("adapted", "normalised"):
        for field_name in ("source_path", "source_author", "source_license", "source_repo"):
            require_nonblank(field_name)

    if content_mode == "verbatim":
        if source_category not in {"first_party", "third_party"}:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has an invalid source_category")
        if entry.get("adaptation_overlay_path") is not None:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} must not declare adaptation_overlay_path for verbatim content")
        if entry.get("adapted_author") is not None:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} must not declare adapted_author for verbatim content")
        if entry.get("adaptation_note") is not None:
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} must not declare adaptation_note for verbatim content")

        # Ensure upstream author is not claimed as repo author for verbatim skills
        source_author = entry.get("source_author")
        if source_author and "Harley Bartles" in source_author and source_category == "third_party":
            raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} incorrectly claims repo author for verbatim third-party content")
        return

    if content_mode not in ("adapted", "normalised"):
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has invalid content_mode: {content_mode}")
    if not entry.get("adaptation_note"):
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} requires an adaptation note for {content_mode} content")

    # MARK-262: Adapted and normalised entries must have adapted_author
    require_nonblank("adapted_author")

    if source_category == "third_party":
        require_nonblank("adaptation_overlay_path")
    elif source_category == "first_party":
        # First-party adapted/normalised entries still need source attribution
        require_nonblank("source_path")
        require_nonblank("source_author")
        require_nonblank("source_license")
    else:
        raise ValueError(f"{bundle_name} bundle manifest imported entry {canonical_name} has an invalid source_category: {source_category}")


def _validate_skill_frontmatter_metadata(skill_path: Path, *, bundle_name: str, entry: dict) -> None:
    """Validate that SKILL.md frontmatter has required metadata fields based on content_mode.
    
    MARK-262: Adapted skills must have complete metadata frontmatter. Verbatim skills should be byte-identical to upstream and should NOT have metadata.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(skill_md)

    content_mode = entry.get("content_mode")
    canonical_name = entry.get("canonical_name") or skill_path.name

    # For verbatim entries, SKILL.md should NOT have MARK-262 authorship metadata
    # (byte-identical to upstream). First-party verbatim skills are exempt: their
    # source custody legitimately carries provenance metadata since the source IS
    # the first-party asset.
    if content_mode == "verbatim":
        source_category = entry.get("source_category")
        frontmatter, _ = _split_skill_frontmatter_and_body(skill_md)
        if frontmatter:
            try:
                parsed = yaml.safe_load(frontmatter)
            except yaml.YAMLError as e:
                raise ValueError(f"{skill_md} has invalid YAML frontmatter: {e}")
            if isinstance(parsed, dict) and "metadata" in parsed:
                metadata = parsed["metadata"]
                if isinstance(metadata, dict) and source_category == "third_party":
                    # Check for MARK-262 authorship fields that should not be in
                    # third-party verbatim skills (they must be byte-identical to upstream)
                    mark262_fields = ["source_author", "source_license", "source_repo", "source_path", "content_mode", "adapted_author"]
                    if any(field in metadata for field in mark262_fields):
                        raise ValueError(f"{bundle_name} skill {canonical_name} has MARK-262 authorship metadata but content_mode is verbatim - third-party verbatim skills must be byte-identical to upstream")
        return

    # For adapted entries, metadata is required
    frontmatter, _ = _split_skill_frontmatter_and_body(skill_md)
    if not frontmatter:
        raise ValueError(f"{skill_md} is missing frontmatter - required for adapted content")

    # Parse frontmatter as YAML
    try:
        parsed = yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        raise ValueError(f"{skill_md} has invalid YAML frontmatter: {e}")

    if not isinstance(parsed, dict):
        raise ValueError(f"{skill_md} frontmatter must be a mapping")

    # MARK-262: Adapted and normalised skills must have metadata section
    # Verbatim skills may have optional metadata (e.g., origin field for provenance tracking)
    metadata = parsed.get("metadata")
    
    if content_mode in {"adapted", "normalised"}:
        if not isinstance(metadata, dict):
            raise ValueError(f"{skill_md} frontmatter is missing required metadata section for {content_mode} content")

    def require_metadata_field(field_name: str) -> None:
        if field_name not in metadata or not metadata[field_name]:
            raise ValueError(f"{bundle_name} skill {canonical_name} frontmatter metadata is missing {field_name}")

    # Required fields for adapted and normalised skills
    require_metadata_field("content_mode")
    require_metadata_field("source_author")
    require_metadata_field("source_license")
    require_metadata_field("source_repo")
    require_metadata_field("source_path")

    # Adapted skills require adapted_author and adaptation_note
    if content_mode == "adapted":
        require_metadata_field("adapted_author")
        require_metadata_field("adaptation_note")
    # Normalised skills should NOT have adapted_author or adaptation_note
    elif content_mode == "normalised":
        if metadata.get("adapted_author") or metadata.get("adaptation_note"):
            raise ValueError(f"{bundle_name} skill {canonical_name} normalised content should not have adapted_author or adaptation_note")

    # Ensure content_mode in frontmatter matches bundle manifest
    if metadata.get("content_mode") != content_mode:
        raise ValueError(f"{bundle_name} skill {canonical_name} frontmatter content_mode '{metadata.get('content_mode')}' does not match bundle manifest '{content_mode}'")


def _validate_plugin_level_authorship(bundle_manifest: dict, *, bundle_name: str) -> None:
    """Validate that plugin-level authorship does not flatten skill-level attribution.
    
    MARK-262: Strict validation - all plugins must have proper plugin-level authorship.
    """
    plugin_author = bundle_manifest.get("plugin_author")
    plugin_license = bundle_manifest.get("plugin_license")

    # MARK-262: All plugins must declare plugin_author and plugin_license
    if not plugin_author or not isinstance(plugin_author, str) or not plugin_author.strip():
        raise ValueError(f"{bundle_name} bundle manifest is missing plugin_author")
    if not plugin_license or not isinstance(plugin_license, str) or not plugin_license.strip():
        raise ValueError(f"{bundle_name} bundle manifest is missing plugin_license")

    # For repo-authored plugin shells, check standard authorship
    if plugin_author == "Harley Bartles":
        if plugin_license != "MIT":
            raise ValueError(f"{bundle_name} plugin_author is Harley Bartles but plugin_license is not MIT")

    # Check that individual skills retain their own upstream authorship
    entries = bundle_manifest.get("entries", [])
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        canonical_name = entry.get("canonical_name")
        content_mode = entry.get("content_mode")
        source_author = entry.get("source_author")
        source_category = entry.get("source_category")

        if content_mode == "verbatim" and source_author:
            # For verbatim third-party content, ensure upstream author is not overwritten
            if plugin_author == "Harley Bartles" and "Harley Bartles" in source_author:
                if source_category == "third_party":
                    raise ValueError(f"{bundle_name} entry {canonical_name} incorrectly claims repo author for verbatim third-party content")


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
        return ROOT / "sources/third_party/claude-cortex/upstream"
    if upstream_repo == "affaan-m/ECC":
        if pinned_commit != "ceca28852e5b31edbbf66ebccc8fd163dd14208e":
            raise ValueError("Unexpected pinned commit for affaan-m/ECC vendor snapshot")
        return ROOT / "sources/third_party/ecc/upstream"
    if upstream_repo == "https://github.com/affaan-m/ECC/tree/main/skills":
        if pinned_commit != "ceca28852e5b31edbbf66ebccc8fd163dd14208e":
            raise ValueError("Unexpected pinned commit for affaan-m/ECC vendor snapshot")
        return ROOT / "sources/third_party/ecc/upstream"
    if upstream_repo == "combined-source":
        # Combined-source bundles aggregate from multiple upstreams; no single vendor root
        return None
    if upstream_repo == "first-party":
        # First-party source custody under sources/first_party/
        return ROOT / "sources/first_party"
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
    expected_plugins = {
        spec["name"]: spec["registry_path"]
        for spec in MARKETPLACE_PLUGIN_SPECS
        if spec["name"] in EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES
    }
    actual_plugin_names = [plugin.get("name") for plugin in registry.get("plugins", [])]
    if actual_plugin_names != list(EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES):
        raise ValueError("Marketplace registry plugin order does not match the protected marketplace shape")
    for name, path in expected_plugins.items():
        plugin = plugins_by_name.get(name)
        if not plugin:
            raise ValueError(f"Marketplace registry is missing the {name} plugin entry")
        if plugin.get("source", {}).get("path") != path:
            raise ValueError(f"Marketplace registry {name} plugin path mismatch")
        if plugin.get("source", {}).get("source") != "local":
            raise ValueError(f"Marketplace registry {name} plugin source kind mismatch")
        if plugin.get("policy", {}).get("installation") != _installation_policy_for_plugin(name):
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
    # Projection-lane manifests are validated by the materializer --check.
    # Skip legacy field validation for the normalized shape.
    if bundle_manifest.get("bundle_type") == "projection-lane":
        return
    if bundle_manifest.get("bundle_name") != "house-skills":
        raise ValueError("bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError("bundle manifest bundle_version mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/house-skills":
        raise ValueError("bundle manifest plugin_root mismatch")
    if bundle_manifest.get("bundle_type") not in ("current-first-party-house-skills-plugin", "projection-lane"):
        raise ValueError("bundle manifest bundle_type mismatch")

    # The control_plane_skill field is only required for the legacy
    # "current-first-party-house-skills-plugin" bundle_type.  Projection-lane
    # manifests use standard entries[] instead.
    if bundle_manifest.get("bundle_type") != "projection-lane":
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
        path.name for path in skill_dir.iterdir() if path.is_dir()
    )
    if any(re.match(r"^v\d", path.name) for path in skill_dir.rglob("*") if path.is_dir()):
        raise ValueError("house-skills plugin root still contains live versioned subdirectories")

    entries = bundle_manifest.get("entries", [])
    if not isinstance(entries, list):
        raise ValueError("bundle manifest entries must be a list")

    manifest_names: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("bundle manifest entries must contain objects")
        name = entry.get("canonical_name")
        lane = entry.get("lane")
        source_path = entry.get("canonical_source_path")
        local_path = entry.get("local_path")
        if not name or not isinstance(name, str):
            raise ValueError("bundle manifest entry is missing canonical_name")
        if not lane or not isinstance(lane, str):
            raise ValueError(f"bundle manifest entry {name} is missing a lane")
        if not source_path or not isinstance(source_path, str):
            raise ValueError(f"bundle manifest entry {name} is missing canonical_source_path")
        if not local_path or not isinstance(local_path, str):
            raise ValueError(f"bundle manifest entry {name} is missing local_path")
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
            raise ValueError(f"bundle manifest entry {name} lane mismatch")
        check_path_exists(ROOT / source_path)
        # local_path is relative to plugin root
        projected_root = ROOT / "codex-marketplace/plugins/house-skills" / local_path
        if projected_root.name != name:
            raise ValueError(f"bundle manifest entry {name} local_path mismatch")
        check_path_exists(projected_root / "SKILL.md")
        check_path_exists(projected_root / "agents" / "openai.yaml")
        manifest_names.append(name)

    if sorted(manifest_names) != current_skill_dirs:
        raise ValueError("bundle manifest entry inventory does not match the live plugin root")

    archive_roots = bundle_manifest.get("archive_roots", [])
    if archive_roots:
        raise ValueError("bundle manifest archive_roots must be absent in the reduced marketplace")

    notes = bundle_manifest.get("notes", [])
    if not isinstance(notes, list) or len(notes) < 1:
        raise ValueError("bundle manifest notes mismatch")


def _load_skill_inventory(plugin_root: str) -> set[str]:
    skills_root = ROOT / plugin_root / "skills"
    if not skills_root.is_dir():
        return set()
    return {child.name for child in skills_root.iterdir() if child.is_dir()}


def _normalize_string_list(value: object, *, context: str, field_name: str, allow_empty: bool) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{context} {field_name} must be a list")
    if not value and not allow_empty:
        raise ValueError(f"{context} {field_name} must be a non-empty list")

    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{context} {field_name} entries must be nonblank strings")
        if item in seen:
            raise ValueError(f"{context} {field_name} contains a duplicate value: {item}")
        seen.add(item)
        normalized.append(item)
    return tuple(normalized)


def validate_projection_pack_manifest(bundle_manifest: dict, *, bundle_name: str, plugin_root: str) -> None:
    if bundle_manifest.get("bundle_name") != bundle_name:
        raise ValueError(f"{bundle_name} bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "1.0.0":
        raise ValueError(f"{bundle_name} bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") not in {"projection-lane", "project-scoped-codex-plugin-projection"}:
        raise ValueError(f"{bundle_name} bundle manifest bundle_type mismatch")
    if bundle_manifest.get("plugin_root") != plugin_root:
        raise ValueError(f"{bundle_name} bundle manifest plugin_root mismatch")

    entries = bundle_manifest.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{bundle_name} bundle manifest entries must be a non-empty list")

    imported_entries = entries

    skill_dir = ROOT / plugin_root / "skills"
    actual_skill_dirs = sorted(path.name for path in skill_dir.iterdir() if path.is_dir())
    imported_skill_dirs = sorted(
        Path(entry["local_path"]).parts[1]
        for entry in imported_entries
        if isinstance(entry.get("local_path"), str)
        and Path(entry["local_path"]).parts[:1] == ("skills",)
        and len(Path(entry["local_path"]).parts) >= 2
    )
    if actual_skill_dirs != imported_skill_dirs:
        raise ValueError(f"{bundle_name} bundle manifest imported skill inventory mismatch")

    source_families = bundle_manifest.get("source_families")
    if not isinstance(source_families, list) or not source_families:
        raise ValueError(f"{bundle_name} bundle manifest source_families must be a non-empty list")
    expected_source_families = sorted({entry.get("source_family") for entry in imported_entries if isinstance(entry.get("source_family"), str)})
    if sorted(source_families) != expected_source_families:
        raise ValueError(f"{bundle_name} bundle manifest source_families mismatch")

    for entry in imported_entries:
        canonical_name = entry.get("canonical_name")
        if not canonical_name or not isinstance(canonical_name, str):
            raise ValueError(f"{bundle_name} imported entry is missing canonical_name")
        if entry.get("source_category") not in {"first_party", "third_party"}:
            raise ValueError(f"{bundle_name} entry {canonical_name} has an invalid source_category")
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "normalised", "adapted"}:
            raise ValueError(f"{bundle_name} entry {canonical_name} has an invalid content_mode")
        expected_copy_expectation = {
            "verbatim": "byte_identical",
            "normalised": "normalised_from_source",
            "adapted": "adapted_from_source",
        }[content_mode]
        if entry.get("copy_expectation") != expected_copy_expectation:
            raise ValueError(f"{bundle_name} entry {canonical_name} copy expectation mismatch")
        if not entry.get("provenance_note"):
            raise ValueError(f"{bundle_name} entry {canonical_name} needs a provenance note")
        adaptation_overlay_path = entry.get("adaptation_overlay_path")
        if content_mode == "verbatim" and adaptation_overlay_path is not None:
            raise ValueError(f"{bundle_name} verbatim entry {canonical_name} must not declare adaptation_overlay_path")
        if content_mode in {"normalised", "adapted"} and not isinstance(adaptation_overlay_path, str):
            raise ValueError(f"{bundle_name} entry {canonical_name} needs an adaptation overlay path")
        if isinstance(adaptation_overlay_path, str):
            check_path_exists(ROOT / adaptation_overlay_path)

        canonical_source_path = entry.get("canonical_source_path")
        local_path = entry.get("local_path")
        if not isinstance(canonical_source_path, str) or not canonical_source_path:
            raise ValueError(f"{bundle_name} entry {canonical_name} is missing canonical_source_path")
        if not isinstance(local_path, str) or not local_path:
            raise ValueError(f"{bundle_name} entry {canonical_name} is missing local_path")
        source_root = ROOT / canonical_source_path
        projected_root = ROOT / plugin_root / local_path
        check_path_exists(source_root)
        check_path_exists(projected_root)
        if source_root.is_dir():
            if content_mode == "verbatim":
                validate_tree_mirror(source_root, projected_root, canonical_name)
            else:
                overlay_root = ROOT / adaptation_overlay_path  # type: ignore[arg-type]
                validate_tree_reconstruction(source_root, overlay_root, projected_root, canonical_name)
        else:
            if not _files_match_canonicalized(source_root, projected_root):
                raise ValueError(f"{bundle_name} entry {canonical_name} drifted from its source copy")
        if projected_root.name != canonical_name:
            raise ValueError(f"{bundle_name} entry {canonical_name} drifted from its source copy")

    notes = bundle_manifest.get("notes", [])
    if not isinstance(notes, list) or not notes:
        raise ValueError(f"{bundle_name} bundle manifest notes mismatch")


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
    # Projection-lane manifests are validated by the materializer --check.
    # Skip legacy field validation for the normalized shape.
    if bundle_manifest.get("bundle_type") == "projection-lane":
        return
    source_root = superpowers_source_root(bundle_manifest)
    source_tag = superpowers_source_tag(bundle_manifest)
    source_commit = superpowers_source_commit(bundle_manifest)
    if bundle_manifest.get("bundle_name") != "superpowers-plus":
        raise ValueError("superpowers-plus bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") not in ("5.1.0", "1.0.0"):
        raise ValueError("superpowers-plus bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") not in ("third-party-codex-plugin-projection", "projection-lane"):
        raise ValueError("superpowers-plus bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("superpowers-plus bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/superpowers-plus":
        raise ValueError("superpowers-plus bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_root") != source_root.relative_to(ROOT).as_posix():
        raise ValueError("superpowers-plus bundle manifest canonical_source_root mismatch")
    if bundle_manifest.get("source_tag") != source_tag:
        raise ValueError("superpowers-plus bundle manifest source_tag mismatch")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("superpowers-plus bundle manifest source_commit mismatch")
    if bundle_manifest.get("license") != "MIT":
        raise ValueError("superpowers-plus bundle manifest license mismatch")
    if bundle_manifest.get("projection_policy") != (
        "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody."
    ):
        raise ValueError("superpowers-plus bundle manifest projection_policy mismatch")
    if bundle_manifest.get("source_of_truth") != [
        (source_root / ".codex-plugin/plugin.json").as_posix(),
        (source_root / "LICENSE").as_posix(),
        (source_root / "README.md").as_posix(),
        (source_root / "AGENTS.md").as_posix(),
        (source_root / "package.json").as_posix(),
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
        if not _files_match_canonicalized(source_root / relative_path, ROOT / plugin_root / relative_path):
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
    _validate_plugin_level_authorship(bundle_manifest, bundle_name="superpowers-plus")

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
            # First-party entries must be verbatim and point at an existing source path.
            # The canonical_source_path is the source of truth — no hardcoded list needed.
            if not isinstance(canonical_source_path, str) or not canonical_source_path:
                raise ValueError(f"superpowers-plus entry {canonical_name} is missing canonical_source_path")
            source_full = ROOT / canonical_source_path
            if not source_full.exists():
                raise ValueError(f"superpowers-plus first-party entry {canonical_name} canonical_source_path does not exist: {canonical_source_path}")
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "normalised", "adapted"}:
            raise ValueError(f"superpowers-plus entry {canonical_name} has an invalid content_mode")
        copy_expectation = entry.get("copy_expectation")
        if content_mode == "verbatim":
            if copy_expectation != "byte_identical":
                raise ValueError(f"superpowers-plus entry {canonical_name} copy expectation mismatch")
        elif content_mode == "normalised":
            if copy_expectation not in {"normalised_from_source", "documented_normalisation"}:
                raise ValueError(f"superpowers-plus entry {canonical_name} copy expectation mismatch for normalised")
        elif copy_expectation not in {"adapted_from_source", "documented_adaptation"}:
            raise ValueError(f"superpowers-plus entry {canonical_name} copy expectation mismatch")
        if not entry.get("provenance_note"):
            raise ValueError(f"superpowers-plus entry {canonical_name} needs a provenance note")
        if content_mode in ("adapted", "normalised") and not entry.get("adaptation_note"):
            raise ValueError(f"superpowers-plus entry {canonical_name} needs an adaptation note")
        adaptation_overlay_path = entry.get("adaptation_overlay_path")
        if source_category == "third_party" and content_mode in ("adapted", "normalised"):
            expected_overlay_path = f"adapters/codex/superpowers-plus/{canonical_name}"
            if adaptation_overlay_path != expected_overlay_path:
                raise ValueError(f"superpowers-plus {content_mode} entry {canonical_name} needs {expected_overlay_path}")
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
        # Validate skill frontmatter metadata (only if entry has required fields)
        _validate_skill_frontmatter_metadata(local_full_path, bundle_name="superpowers-plus", entry=entry)
        if source_path.is_dir():
            if content_mode == "verbatim":
                validate_tree_mirror(source_path, local_full_path, canonical_name)
            elif content_mode == "normalised":
                validate_openai_agent_yaml(local_full_path / "agents" / "openai.yaml")
                if adaptation_overlay_path is None:
                    raise ValueError(f"superpowers-plus normalised entry {canonical_name} needs an overlay path")
                overlay_root = ROOT / adaptation_overlay_path
                validate_tree_reconstruction(source_path, overlay_root, local_full_path, canonical_name)
            else:  # adapted
                validate_openai_agent_yaml(local_full_path / "agents" / "openai.yaml")
                if adaptation_overlay_path is None:
                    raise ValueError(f"superpowers-plus adapted entry {canonical_name} needs an overlay path")
                overlay_root = ROOT / adaptation_overlay_path
                validate_tree_reconstruction(source_path, overlay_root, local_full_path, canonical_name)
        else:
            if content_mode == "verbatim" and not _files_match_canonicalized(source_path, local_full_path):
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
    
    # First-party bundles have specific structure requirements
    bundle_type = bundle_manifest.get("bundle_type")
    if bundle_type and "first-party" in bundle_type:
        # Validate first-party bundle structure
        if not bundle_manifest.get("plugin_root"):
            raise ValueError(f"{bundle_name} bundle manifest plugin_root missing")
        if not bundle_manifest.get("skills_root"):
            raise ValueError(f"{bundle_name} bundle manifest skills_root missing")
        
        # Validate control_plane_skill for first-party bundles
        control_plane = bundle_manifest.get("control_plane_skill")
        if not isinstance(control_plane, dict):
            raise ValueError(f"{bundle_name} bundle manifest control_plane_skill missing")
        if not control_plane.get("name"):
            raise ValueError(f"{bundle_name} bundle manifest control_plane_skill.name missing")
        if not control_plane.get("path"):
            raise ValueError(f"{bundle_name} bundle manifest control_plane_skill.path missing")
        
        # Validate skills array
        skills = bundle_manifest.get("skills")
        if not isinstance(skills, list):
            raise ValueError(f"{bundle_name} bundle manifest skills missing or not array")
        
        # Validate skill_count matches skills array length
        skill_count = bundle_manifest.get("skill_count")
        if skill_count != len(skills):
            raise ValueError(f"{bundle_name} bundle manifest skill_count mismatch")
        
        # Validate each skill has required fields
        for skill in skills:
            if not skill.get("name"):
                raise ValueError(f"{bundle_name} bundle manifest skill missing name")
            if not skill.get("path"):
                raise ValueError(f"{bundle_name} bundle manifest skill missing path")
        
        # Validate plugin_root exists
        plugin_root_path = ROOT / bundle_manifest["plugin_root"]
        check_path_exists(plugin_root_path)

        # Validate skills_root exists
        skills_root_path = ROOT / bundle_manifest["skills_root"]
        check_path_exists(skills_root_path)

        # Validate control_plane_skill.path exists and has SKILL.md
        control_plane_path = ROOT / control_plane["path"]
        check_path_exists(control_plane_path)
        check_path_exists(control_plane_path / "SKILL.md")

        # Require and validate source_map for first-party bundles
        source_map = bundle_manifest.get("source_map")
        if not source_map or not isinstance(source_map, str):
            raise ValueError(f"{bundle_name} bundle manifest source_map missing or malformed")
        check_path_exists(ROOT / plugin_root / source_map)

        # Validate each skills[] source path exists
        for skill in skills:
            source_path = ROOT / skill["path"]
            check_path_exists(source_path)

        # Validate each corresponding projected local skill path exists
        skills_root = bundle_manifest["skills_root"]
        for skill in skills:
            skill_name = skill["name"]
            local_skill_path = ROOT / skills_root / skill_name
            check_path_exists(local_skill_path)
            check_path_exists(local_skill_path / "SKILL.md")

        # Require and validate provenance_refs for first-party bundles
        provenance_refs = bundle_manifest.get("provenance_refs")
        if not provenance_refs or not isinstance(provenance_refs, list):
            raise ValueError(f"{bundle_name} bundle manifest provenance_refs missing or malformed")
        for ref in provenance_refs:
            if not ref or not isinstance(ref, str):
                raise ValueError(f"{bundle_name} bundle manifest provenance_refs entry missing or malformed")
            check_path_exists(ROOT / ref)

        # Do not return early - allow repo-index metadata validation to run
    else:
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

        if bundle_name in ("security-pack", "unslop-plus") and isinstance(bundle_manifest.get("source_families"), list):
            source_family_roots = {}
            for family in bundle_manifest["source_families"]:
                if isinstance(family, str):
                    # Legacy string-list format: resolve via source_family_roots map
                    family_name = family
                    if family_name in source_family_roots:
                        raise ValueError(f"{bundle_name} bundle manifest source_families entry name duplicated")
                    roots_map = bundle_manifest.get("source_family_roots")
                    if isinstance(roots_map, dict) and family_name in roots_map:
                        resolved = ROOT / roots_map[family_name]
                        check_path_exists(resolved)
                        source_family_roots[family_name] = resolved
                    continue
                if not isinstance(family, dict):
                    raise ValueError(f"{bundle_name} bundle manifest source_families must contain objects or strings")
                family_name = family.get("name")
                family_upstream_repo = family.get("upstream_repo")
                family_pinned_commit = family.get("pinned_commit")
                family_source_root = family.get("source_root")
                if not family_name or not isinstance(family_name, str):
                    raise ValueError(f"{bundle_name} bundle manifest source_families entry name mismatch")
                if family_name in source_family_roots:
                    raise ValueError(f"{bundle_name} bundle manifest source_families entry name duplicated")
                if not family_upstream_repo or not isinstance(family_upstream_repo, str):
                    raise ValueError(f"{bundle_name} bundle manifest source_families upstream_repo mismatch")
                if not family_pinned_commit or not isinstance(family_pinned_commit, str):
                    raise ValueError(f"{bundle_name} bundle manifest source_families pinned_commit mismatch")
                if not family_source_root or not isinstance(family_source_root, str):
                    raise ValueError(f"{bundle_name} bundle manifest source_families source_root mismatch")
                family_vendor_root = _resolve_vendor_root(family_upstream_repo, family_pinned_commit)
                if family_vendor_root is not None:
                    resolved_family_root = family_vendor_root / family_source_root
                    check_path_exists(resolved_family_root)
                    source_family_roots[family_name] = resolved_family_root
            check_path_exists(ROOT / plugin_root / source_root)
        else:
            vendor_root = _resolve_vendor_root(upstream_repo, pinned_commit)
            if vendor_root is not None:
                check_path_exists(vendor_root / source_root)

    _validate_repo_index_metadata(bundle_manifest.get("repo_index"), bundle_name=bundle_name, plugin_root=plugin_root)
    _validate_plugin_level_authorship(bundle_manifest, bundle_name=bundle_name)

    # Only validate entries/candidate_count for third-party import manifests
    entries = bundle_manifest.get("entries")
    if entries is not None:
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
            entry_vendor_root = vendor_root
            if source_family_roots is not None:
                source_family = entry.get("source_family")
                if source_family and isinstance(source_family, str):
                    entry_vendor_root = source_family_roots.get(source_family)
                    if entry_vendor_root is None:
                        raise ValueError(
                            f"{bundle_name} bundle manifest imported entry uses an unknown source_family: {source_family}"
                        )
                else:
                    entry_vendor_root = None
            # For combined-source bundles, vendor_root may be None; skip snapshot path validation in that case
            if entry_vendor_root is not None:
                check_path_exists(entry_vendor_root / snapshot_path)
            content_mode = entry.get("content_mode")
            
            # Validate skill frontmatter metadata (only if entry has required fields and is a skill)
            local_full_path = ROOT / plugin_root / local_path
            # Only validate if the local path points to a SKILL.md file (not profiles or other files)
            if local_full_path.name == "SKILL.md":
                _validate_skill_frontmatter_metadata(local_full_path.parent, bundle_name=bundle_name, entry=entry)
            
            if content_mode not in {"verbatim", "normalised", "adapted"}:
                raise ValueError(f"{bundle_name} bundle manifest imported entry has invalid content_mode")
            
            # For adapted and normalised entries, require source attribution fields
            if content_mode in {"adapted", "normalised"}:
                for field in ("source_path", "source_author", "source_license", "source_repo"):
                    if not isinstance(entry.get(field), str) or not entry.get(field):
                        raise ValueError(f"{bundle_name} bundle manifest imported entry is missing {field}")
            
            if content_mode == "normalised":
                # Normalised: substantive content unchanged, but projection is Codex/OpenAI-canonical
                # Requires attribution but not adapted_author/adaptation_note
                if entry.get("adapted_author") or entry.get("adaptation_note"):
                    raise ValueError(f"{bundle_name} bundle manifest normalised entry should not have adapted_author or adaptation_note")
            if content_mode == "adapted" and not entry.get("adaptation_note"):
                raise ValueError(f"{bundle_name} bundle manifest adapted entry requires an adaptation note")
            
            # Content-equivalence checks (only if vendor_root is available)
            if entry_vendor_root is not None:
                source_path = entry_vendor_root / snapshot_path
                projected_path = ROOT / plugin_root / local_path
                
                if content_mode == "verbatim":
                    # Verbatim: canonicalized content identity against retained source
                    if not _files_match_canonicalized(source_path, projected_path):
                        raise ValueError(
                            f"{bundle_name} bundle manifest imported entry {local_path} drifted from retained snapshot"
                        )
                elif content_mode == "normalised":
                    # Normalised: body-equivalence comparison ignoring projection-only metadata
                    # and accounting for canonical path normalization (e.g., references/ moves)
                    _, source_body = _split_skill_frontmatter_and_body(source_path)
                    _, projected_body = _split_skill_frontmatter_and_body(projected_path)
                    
                    # For combined-source bundles, canonicalize path references in the body
                    # to account for projection-only path normalization (e.g., skills/x/references/ -> references/)
                    if bundle_manifest.get("content_mode") == "combined-source":
                        # Extract skill name from local_path to build canonical path mappings
                        # local_path format: skills/<skill-name>/SKILL.md
                        parts = local_path.split('/')
                        if len(parts) >= 2 and parts[0] == "skills":
                            skill_name = parts[1]
                            # Normalize path references from skills/<skill>/references/ to references/
                            source_body = source_body.replace(f"skills/{skill_name}/references/", "references/")
                    
                    # Normalize line endings for comparison (CRLF vs LF)
                    source_body = source_body.replace('\r\n', '\n')
                    projected_body = projected_body.replace('\r\n', '\n')
                    
                    if source_body != projected_body:
                        raise ValueError(
                            f"{bundle_name} bundle manifest imported entry {local_path} substantive content drifted from retained snapshot"
                        )
                # For adapted entries, no content-equivalence check

        for entry in skipped_entries + blocked_entries:
            if entry.get("local_path") not in ("", None):
                raise ValueError(f"{bundle_name} bundle manifest skipped/blocked entry should not expose a local path")
            if not entry.get("adaptation_note"):
                raise ValueError(f"{bundle_name} bundle manifest skipped/blocked entry requires an adaptation note")


def validate_project_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    # Projection-lane manifests are validated by the materializer --check.
    if bundle_manifest.get("bundle_type") == "projection-lane":
        return
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
    if dependency_count != 2:
        raise ValueError("adventures-pack bundle manifest must project two generic dependency components")

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
        "codex-marketplace/plugins/house-skills/references/bundle-manifest.json",
        "Generated from `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`.",
    ):
        if needle not in text:
            raise ValueError(f"source map is missing {needle}")


def detect_first_party_orphans() -> list[str]:
    """Detect first-party skill dirs with SKILL.md that have no projection entry."""
    skills_root = ROOT / "sources" / "first_party" / "skills"
    if not skills_root.is_dir():
        return []
    custody_skills: set[str] = set()
    for d in skills_root.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            custody_skills.add(d.name)
    projected_names: set[str] = set()
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        manifest_path = plugin_root / "references" / "bundle-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest.get("entries", []):
            if isinstance(entry, dict) and entry.get("source_category") == "first_party":
                name = entry.get("canonical_name")
                if name:
                    projected_names.add(name)
    orphans = sorted(custody_skills - projected_names)
    return orphans


def validate_mega_pack_inclusion() -> None:
    """Validate that every entry in a topical plugin also appears in its mega-pack."""
    import sys
    tools_dir = str(ROOT / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    from generate_mega_packs import _entry_matches_selection, collect_entries_by_family, load_mega_pack_registry, load_plugin_manifest

    registry = load_mega_pack_registry()
    mega_pack_names = {m["mega_pack"] for m in registry}
    selection_by_family = {
        mapping["source_family"]: mapping.get("entry_selection")
        for mapping in registry
        if mapping.get("entry_selection") is not None
    }
    plugin_manifests: list[dict] = []
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        manifest = load_plugin_manifest(plugin_root)
        if manifest is None:
            continue
        if spec["name"] in mega_pack_names:
            continue
        plugin_manifests.append(manifest)

    by_family = collect_entries_by_family(plugin_manifests, selection_by_family=selection_by_family)

    for mapping in registry:
        family = mapping["source_family"]
        mega_name = mapping["mega_pack"]
        mega_root = ROOT / mapping["mega_pack_root"]
        mega_manifest_path = mega_root / "references" / "bundle-manifest.json"
        if not mega_manifest_path.exists():
            raise ValueError(f"mega-pack manifest missing for {family}: {mega_manifest_path}")
        mega_manifest = check_json(mega_manifest_path)
        mega_names_set = {
            e.get("canonical_name") for e in mega_manifest.get("entries", [])
            if isinstance(e, dict) and e.get("content_mode") not in ("blocked", "skipped")
        }
        topical_names_set = {
            e.get("canonical_name") for e in by_family.get(family, [])
            if isinstance(e, dict)
            and e.get("canonical_name") is not None
            and _entry_matches_selection(e, mapping.get("entry_selection"))
        }
        missing = sorted(topical_names_set - mega_names_set)
        if missing:
            raise ValueError(
                f"mega-pack {mega_name} is missing entries that appear in topical plugins: {missing}\n"
                f"Fix: run py -3 tools/generate_mega_packs.py"
            )
    print("OK mega-pack inclusion: all topical entries appear in their mega-packs")


def validate_no_legacy_manifest_shapes() -> None:
    """Validate that no plugin manifest uses a legacy shape that the materializer would skip."""
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        manifest_path = plugin_root / "references" / "bundle-manifest.json"
        if not manifest_path.exists():
            continue
        manifest = check_json(manifest_path)
        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise ValueError(
                f"{spec['name']}: manifest must have entries[] array (legacy skills[] or components[] not allowed)"
            )
        if not entries:
            continue
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValueError(f"{spec['name']}: entry {i} must be an object")
            if "canonical_name" not in entry or "canonical_source_path" not in entry:
                raise ValueError(
                    f"{spec['name']}: entry {i} must have canonical_name and canonical_source_path (legacy shape)"
                )
            csp = entry.get("canonical_source_path", "")
            if isinstance(csp, str) and Path(csp).suffix:
                raise ValueError(
                    f"{spec['name']}: entry {i} canonical_source_path must be directory-level (legacy file-level path: {csp})"
                )
    print("OK manifest shape: all plugins use projection-lane directory-level entries[]")


def main() -> int:
    _run_tool_check(
        [sys.executable, "tools/generate_plugin_root_inventory.py", "--check"],
        "plugin root inventory check",
    )
    _bootstrap_marketplace_dependencies()

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
    validate_projection_materializer()
    validate_pack_manifests()
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
            elif spec["name"] == "superpowers-plus":
                validate_superpowers_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
            elif bundle_manifest_json.get("bundle_type") == "projection-lane":
                if "entries" in bundle_manifest_json:
                    validate_projection_pack_manifest(
                        bundle_manifest_json,
                        bundle_name=spec["name"],
                        plugin_root=spec["plugin_root"],
                    )
                elif "components" in bundle_manifest_json:
                    validate_project_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
                else:
                    raise ValueError(f"{spec['name']} projection-lane bundle manifest has no recognized payload shape")
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

    # New validation checks for normalized projection-lane shape
    validate_no_legacy_manifest_shapes()
    orphans = detect_first_party_orphans()
    if orphans:
        raise ValueError(
            f"first-party orphan skills detected (have SKILL.md in custody but no projection entry): {orphans}\n"
            f"Fix: add manifest entries for these skills and regenerate, or remove retired source custody that should not stay in the active first-party tree."
        )
    print(f"OK first-party orphan check: 0 orphans")
    validate_mega_pack_inclusion()

    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
