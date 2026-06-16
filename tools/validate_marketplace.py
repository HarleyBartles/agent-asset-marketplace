#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

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
from skill_zip_artifacts import validate_skill_zip_registry


ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_SUPERPOWERS_SOURCES = {
    "linear-superpowers": "codex-marketplace/plugins/house-skills/skills/linear-superpowers",
    "github-superpowers": "codex-marketplace/plugins/house-skills/skills/github-superpowers",
    "unslop-superpowers": "codex-marketplace/plugins/house-skills/skills/unslop-superpowers",
}


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


def validate_tree_mirror(source_root: Path, local_root: Path, component_name: str) -> None:
    source_files = list_files(source_root)
    local_files = list_files(local_root)
    if source_files != local_files:
        raise ValueError(f"adventures-pack component {component_name} file inventory mismatch")
    for rel_path in source_files:
        source_bytes = (source_root / rel_path).read_bytes()
        local_bytes = (local_root / rel_path).read_bytes()
        if source_bytes != local_bytes:
            raise ValueError(f"adventures-pack component {component_name} file content mismatch at {rel_path}")


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
    if plugin_name == "superpowers":
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
        "codex-marketplace/plugins/house-skills/skills",
        "sources/third_party/game-studio/upstream/skills",
    ]:
        raise ValueError("wild-bunch-project-pack bundle manifest canonical_source_roots mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "codex-marketplace/plugins/house-skills/skills/wild-bunch-browser-game/SKILL.md",
        "codex-marketplace/plugins/house-skills/skills/wild-bunch-domain-modeling/SKILL.md",
        "codex-marketplace/plugins/house-skills/skills/wild-bunch-dotnet-architecture/SKILL.md",
        "codex-marketplace/plugins/house-skills/skills/wild-bunch-project-doctrine/SKILL.md",
        "codex-marketplace/plugins/house-skills/skills/wild-bunch-worker-verification/SKILL.md",
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


def validate_superpowers_bundle_manifest(bundle_manifest: dict, plugin_root: str) -> None:
    source_root = ROOT / "sources/third_party/superpowers/obra-superpowers/v5.1.0"
    if bundle_manifest.get("bundle_name") != "superpowers":
        raise ValueError("superpowers bundle manifest bundle_name mismatch")
    if bundle_manifest.get("bundle_version") != "5.1.0":
        raise ValueError("superpowers bundle manifest bundle_version mismatch")
    if bundle_manifest.get("bundle_type") != "third-party-codex-plugin-projection":
        raise ValueError("superpowers bundle manifest bundle_type mismatch")
    if bundle_manifest.get("marketplace_root") != ".agents/plugins/marketplace.json":
        raise ValueError("superpowers bundle manifest marketplace_root mismatch")
    if bundle_manifest.get("plugin_root") != "codex-marketplace/plugins/superpowers":
        raise ValueError("superpowers bundle manifest plugin_root mismatch")
    if bundle_manifest.get("canonical_source_root") != "sources/third_party/superpowers/obra-superpowers/v5.1.0":
        raise ValueError("superpowers bundle manifest canonical_source_root mismatch")
    if bundle_manifest.get("source_tag") != "v5.1.0":
        raise ValueError("superpowers bundle manifest source_tag mismatch")
    if bundle_manifest.get("source_commit") != "f2cbfbefebbfef77321e4c9abc9e949826bea9d7":
        raise ValueError("superpowers bundle manifest source_commit mismatch")
    if bundle_manifest.get("license") != "MIT":
        raise ValueError("superpowers bundle manifest license mismatch")
    if bundle_manifest.get("projection_policy") != (
        "Project only the Codex-facing plugin surface. Keep the upstream harness-specific metadata, docs, scripts, and hooks in third-party source custody."
    ):
        raise ValueError("superpowers bundle manifest projection_policy mismatch")
    if bundle_manifest.get("source_of_truth") != [
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/.codex-plugin/plugin.json",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/LICENSE",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/README.md",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/AGENTS.md",
        "sources/third_party/superpowers/obra-superpowers/v5.1.0/package.json",
    ]:
        raise ValueError("superpowers bundle manifest source_of_truth mismatch")

    for relative_path in (
        ".codex-plugin/plugin.json",
        "LICENSE",
        "assets/app-icon.png",
        "assets/superpowers-small.svg",
    ):
        source_bytes = (source_root / relative_path).read_bytes()
        projected_bytes = (ROOT / plugin_root / relative_path).read_bytes()
        if source_bytes != projected_bytes:
            raise ValueError(f"superpowers projection drift at {relative_path}")

    entries = bundle_manifest.get("entries", [])
    if not isinstance(entries, list) or not entries:
        raise ValueError("superpowers bundle manifest entries must be a non-empty list")
    if bundle_manifest.get("candidate_count") != len(entries):
        raise ValueError("superpowers bundle manifest candidate count mismatch")
    if bundle_manifest.get("imported_count") != len(entries):
        raise ValueError("superpowers bundle manifest imported count mismatch")
    if bundle_manifest.get("skipped_count") != 0:
        raise ValueError("superpowers bundle manifest skipped count mismatch")
    if bundle_manifest.get("blocked_count") != 0:
        raise ValueError("superpowers bundle manifest blocked count mismatch")

    support_entries = bundle_manifest.get("excluded", [])
    if not isinstance(support_entries, list) or len(support_entries) != 7:
        raise ValueError("superpowers bundle manifest excluded support surface count mismatch")

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
        raise ValueError("superpowers bundle manifest imported skill inventory mismatch")

    for entry in entries:
        canonical_name = entry.get("canonical_name")
        if not canonical_name or not isinstance(canonical_name, str):
            raise ValueError("superpowers imported entry is missing canonical_name")
        canonical_source_path = entry.get("canonical_source_path")
        source_category = entry.get("source_category")
        if source_category not in {"third_party", "first_party"}:
            raise ValueError(f"superpowers entry {canonical_name} has an invalid source_category")
        if source_category == "first_party":
            expected_source_path = FIRST_PARTY_SUPERPOWERS_SOURCES.get(canonical_name)
            if expected_source_path is None:
                allowed = ", ".join(sorted(FIRST_PARTY_SUPERPOWERS_SOURCES))
                raise ValueError(f"superpowers first-party projections are limited to {allowed}")
            if canonical_source_path != expected_source_path:
                raise ValueError(f"superpowers {canonical_name} first-party source path mismatch")
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "adapted"}:
            raise ValueError(f"superpowers entry {canonical_name} has an invalid content_mode")
        copy_expectation = entry.get("copy_expectation")
        if content_mode == "verbatim":
            if copy_expectation != "byte_identical":
                raise ValueError(f"superpowers entry {canonical_name} copy expectation mismatch")
        elif copy_expectation not in {"adapted_from_source", "documented_adaptation"}:
            raise ValueError(f"superpowers entry {canonical_name} copy expectation mismatch")
        if not entry.get("provenance_note"):
            raise ValueError(f"superpowers entry {canonical_name} needs a provenance note")
        if content_mode == "adapted" and not entry.get("adaptation_note"):
            raise ValueError(f"superpowers entry {canonical_name} needs an adaptation note")

        local_path = entry.get("local_path")
        if not isinstance(canonical_source_path, str) or not canonical_source_path:
            raise ValueError(f"superpowers entry {canonical_name} is missing canonical_source_path")
        if not isinstance(local_path, str) or not local_path:
            raise ValueError(f"superpowers entry {canonical_name} is missing local_path")
        check_path_exists(ROOT / canonical_source_path)
        check_path_exists(ROOT / plugin_root / local_path)
        source_path = ROOT / canonical_source_path
        local_full_path = ROOT / plugin_root / local_path
        if source_path.is_dir():
            if content_mode == "verbatim":
                validate_tree_mirror(source_path, local_full_path, canonical_name)
            else:
                if canonical_name == "using-superpowers":
                    projected_text = normalize_superpowers_projection_text(
                        local_full_path.joinpath("SKILL.md").read_text(encoding="utf-8")
                    )
                    if "workflow guidance inside the normal instruction stack" not in projected_text:
                        raise ValueError("superpowers using-superpowers adaptation note mismatch")
                    if "do not override system, developer, runtime" not in projected_text:
                        raise ValueError("superpowers using-superpowers adaptation note mismatch")
                    if "codex-marketplace-compatibility" not in projected_text:
                        raise ValueError("superpowers using-superpowers compatibility note missing")
                elif canonical_name == "finishing-a-development-branch":
                    projected_text = normalize_superpowers_projection_text(
                        local_full_path.joinpath("SKILL.md").read_text(encoding="utf-8")
                    )
                    if "codex marketplace note" not in projected_text:
                        raise ValueError("superpowers finishing-a-development-branch compatibility note missing")
                    if "publication flow" not in projected_text:
                        raise ValueError("superpowers finishing-a-development-branch publication note missing")
        else:
            if content_mode == "verbatim" and source_path.read_bytes() != local_full_path.read_bytes():
                raise ValueError(f"superpowers entry {canonical_name} drifted from its source copy")

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
            raise ValueError("superpowers excluded entries must contain objects")
        path = entry.get("path")
        reason = entry.get("reason")
        if not isinstance(path, str) or not path:
            raise ValueError("superpowers excluded entry is missing path")
        if not isinstance(reason, str) or not reason:
            raise ValueError(f"superpowers excluded entry {path} needs a reason")
        support_paths[path] = reason

    if set(support_paths) != set(expected_support_paths):
        raise ValueError("superpowers bundle manifest excluded support surface mismatch")

    for path in expected_support_paths:
        check_path_exists(source_root / path)
        if (ROOT / plugin_root / path).exists():
            raise ValueError(f"superpowers support surface {path} must not be projected")

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
    upstream_repo = bundle_manifest.get("upstream_repo")
    if not upstream_repo or not isinstance(upstream_repo, str):
        raise ValueError(f"{bundle_name} bundle manifest upstream_repo mismatch")
    pinned_commit = bundle_manifest.get("pinned_commit")
    if not pinned_commit or not isinstance(pinned_commit, str):
        raise ValueError(f"{bundle_name} bundle manifest pinned_commit mismatch")
    vendor_root = _resolve_vendor_root(upstream_repo, pinned_commit)
    source_root = bundle_manifest.get("source_root")
    if not source_root or not isinstance(source_root, str):
        raise ValueError(f"{bundle_name} bundle manifest source_root mismatch")
    check_path_exists(vendor_root / source_root)

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
        check_path_exists(vendor_root / snapshot_path)
        content_mode = entry.get("content_mode")
        if content_mode not in {"verbatim", "adapted"}:
            raise ValueError(f"{bundle_name} bundle manifest imported entry has invalid content_mode")
        if not entry.get("adaptation_note"):
            raise ValueError(f"{bundle_name} bundle manifest imported entry requires an adaptation note")
        if content_mode == "verbatim":
            source_bytes = (vendor_root / snapshot_path).read_bytes()
            projected_bytes = (ROOT / plugin_root / local_path).read_bytes()
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
        if spec["name"] == "superpowers":
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
            elif spec["name"] == "superpowers":
                validate_superpowers_bundle_manifest(bundle_manifest_json, spec["plugin_root"])
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
