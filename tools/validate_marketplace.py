#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    PLUGIN_ROOT_INVENTORY_PATH,
    REPO_INDEX_PATH,
    build_marketplace_manifest,
    load_json,
    parse_top_markdown_table,
    _installation_policy_for_plugin,
)
from validate_repo_index import validate_repo_index


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


def _run_tool_check(command: list[str], label: str) -> None:
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - exercised via integration checks
        raise ValueError(f"{label} failed with exit code {exc.returncode}") from exc


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


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


def _validate_skill_frontmatter_metadata(skill_path: Path, *, bundle_name: str, entry: dict) -> None:
    """Validate that SKILL.md frontmatter has required metadata fields based on content_mode.

    MARK-262: Adapted skills must have complete metadata frontmatter.
    Verbatim skills should be byte-identical to upstream and should NOT
    have metadata.
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
                    mark262_fields = [
                        "source_author",
                        "source_license",
                        "source_repo",
                        "source_path",
                        "content_mode",
                        "adapted_author",
                    ]
                    if any(field in metadata for field in mark262_fields):
                        raise ValueError(
                            f"{bundle_name} skill {canonical_name} has "
                            f"MARK-262 authorship metadata but content_mode is "
                            f"verbatim - third-party verbatim skills must be "
                            f"byte-identical to upstream"
                        )
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
            raise ValueError(
                f"{bundle_name} skill {canonical_name} normalised content "
                f"should not have adapted_author or adaptation_note"
            )

    # Ensure content_mode in frontmatter matches bundle manifest
    if metadata.get("content_mode") != content_mode:
        raise ValueError(
            f"{bundle_name} skill {canonical_name} frontmatter content_mode "
            f"'{metadata.get('content_mode')}' does not match bundle manifest "
            f"'{content_mode}'"
        )


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
                    raise ValueError(
                        f"{bundle_name} entry {canonical_name} incorrectly "
                        f"claims repo author for verbatim third-party content"
                    )


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
                    f"{spec['name']}: entry {i} canonical_source_path "
                    f"must be directory-level (legacy file-level path: {csp})"
                )
    print("OK manifest shape: all plugins use plugin-first directory-level entries[]")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the local marketplace registry. (read-only)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="run the validation (default)",
    )
    parser.add_argument(
        "--phase",
        choices=("inventory", "project", "index", "all"),
        default="all",
        help="Validate only one phase. Default: all",
    )
    parser.add_argument(
        "--skip-freshness-checks",
        action="store_true",
        help=(
            "Skip freshness checks already covered by an upstream step "
            "(generate_plugin_root_inventory --check and pack manifests). "
            "Metadata validation (validate_repo_index) still runs."
        ),
    )
    return parser.parse_args()


def validate_inventory(*, skip_freshness: bool = False) -> None:
    if not skip_freshness:
        _run_tool_check(
            [sys.executable, "tools/generate_plugin_root_inventory.py", "--check"],
            "plugin root inventory check",
        )
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec)
    validate_active_plugin_tree()
    check_json(PLUGIN_ROOT_INVENTORY_PATH)
    print("OK validate_marketplace: inventory")


def validate_project(*, skip_freshness: bool = False) -> None:
    plugin_manifests: list[dict] = []
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_manifest = check_json(spec["manifest_path"])
        validate_plugin_manifest(plugin_manifest, spec)
        plugin_manifests.append(plugin_manifest)
    registry = check_json(MARKETPLACE_PATH)

    validate_marketplace_registry(registry, plugin_manifests)
    codex_manifest = check_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    if codex_manifest != registry:
        raise ValueError("codex-marketplace/manifest.json does not match .agents/plugins/marketplace.json")
    for spec in MARKETPLACE_PLUGIN_SPECS:
        plugin_root = ROOT / spec["plugin_root"]
        if spec["name"] == "superpowers-plus":
            for required in ("README.md", "SOURCE.md", "LICENSE"):
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
            check_json(bundle_path)

    check_text(ROOT / "codex-marketplace/README.md")
    check_text(ROOT / "codex-marketplace/plugins/README.md")
    check_text(ROOT / "codex-marketplace/plugins/unslop-plus/SOURCE.md")
    validate_no_legacy_manifest_shapes()
    print("OK validate_marketplace: project")


def validate_index(*, skip_freshness: bool = False) -> None:
    _ = skip_freshness
    root = check_json(REPO_INDEX_PATH)
    for zone in root.get("zones", []):
        index_json = zone.get("index_json")
        if index_json:
            if Path(index_json).is_absolute():
                raise ValueError(f"index_json must be a relative path: {index_json}")
            check_json(ROOT / index_json)
    validate_repo_index()
    print("OK validate_marketplace: index")


def validate_all(*, skip_freshness: bool = False) -> None:
    validate_inventory(skip_freshness=skip_freshness)
    validate_project(skip_freshness=skip_freshness)
    validate_index(skip_freshness=skip_freshness)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    phase_runners = {
        "inventory": lambda: validate_inventory(skip_freshness=args.skip_freshness_checks),
        "project": lambda: validate_project(skip_freshness=args.skip_freshness_checks),
        "index": lambda: validate_index(skip_freshness=args.skip_freshness_checks),
        "all": lambda: validate_all(skip_freshness=args.skip_freshness_checks),
    }
    phase_runners[args.phase]()
    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
