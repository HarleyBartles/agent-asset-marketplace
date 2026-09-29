#!/usr/bin/env python3
"""Validate the local marketplace registry and bundle surfaces."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    EXPECTED_ACTIVE_MARKETPLACE_PLUGIN_NAMES,
    EXPECTED_MARKETPLACE,
    MARKETPLACE_PATH,
    MARKETPLACE_PLUGIN_SPECS,
    PLUGIN_ROOT_INVENTORY_PATH,
    build_marketplace_manifest,
    load_json,
    _installation_policy_for_plugin,
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


def _run_tool_check(command: list[str], label: str) -> None:
    try:
        subprocess.run(command, cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:  # pragma: no cover - exercised via integration checks
        raise ValueError(f"{label} failed with exit code {exc.returncode}") from exc


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
    plugin_root = ROOT / "dist/plugins"
    expected_names = sorted(spec["name"] for spec in MARKETPLACE_PLUGIN_SPECS)
    actual_names = sorted(path.name for path in plugin_root.iterdir() if path.is_dir())
    if actual_names != expected_names:
        raise ValueError(
            f"dist/plugins contains non-protected plugin roots: expected {expected_names}, found {actual_names}"
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


def validate_bundle_source_contracts() -> None:
    """Check that built bundle metadata names canonical skills and installed copies."""
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
        names: set[str] = set()
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValueError(f"{spec['name']}: entry {i} must be an object")
            name = entry.get("canonical_name")
            source = entry.get("canonical_source_path")
            if not isinstance(name, str) or not name or name in names:
                raise ValueError(f"{spec['name']}: entry {i} has a missing or duplicate skill name")
            names.add(name)
            if (
                not isinstance(source, str)
                or Path(source).parts[:1] != ("skills",)
                or ".." in Path(source).parts
                or len(Path(source).parts) != 2
            ):
                raise ValueError(f"{spec['name']}: entry {i} must point to top-level skill source")
            if entry.get("source_category") != "first_party":
                raise ValueError(f"{spec['name']}: entry {i} must declare first-party source custody")
            if entry.get("source_path") != f"{source}/SKILL.md" or not (ROOT / source / "SKILL.md").is_file():
                raise ValueError(f"{spec['name']}: entry {i} has an unresolved canonical source")
            if (
                entry.get("local_path") != f"skills/{name}"
                or not (plugin_root / "skills" / name / "SKILL.md").is_file()
            ):
                raise ValueError(f"{spec['name']}: entry {i} has an unresolved installed skill")
        if names != _load_skill_inventory(spec["plugin_root"]):
            raise ValueError(f"{spec['name']}: bundle entries differ from packaged skills")
    print("OK bundle source contracts: every installed skill maps to canonical first-party source")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the local marketplace registry. (read-only)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="run the validation (default)",
    )
    parser.add_argument(
        "--phase",
        choices=("inventory", "project", "shared-references", "all"),
        default="all",
        help="Validate only one phase. Default: all",
    )
    parser.add_argument(
        "--skip-freshness-checks",
        action="store_true",
        help=(
            "Skip freshness checks already covered by an upstream step "
            "(generate_plugin_root_inventory --check and pack manifests)."
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
        raise ValueError("dist/manifest.json does not match .agents/plugins/marketplace.json")
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

    check_text(ROOT / "docs/distribution.md")
    check_text(ROOT / "dist/plugins/unslop-plus/SOURCE.md")
    validate_bundle_source_contracts()
    print("OK validate_marketplace: project")


def validate_shared_references(*, skip_freshness: bool = False) -> None:
    _ = skip_freshness
    _run_tool_check(
        [sys.executable, "tools/sync_skill_shared_references.py", "--check"],
        "shared skill references check",
    )
    print("OK validate_marketplace: shared-references")


def validate_all(*, skip_freshness: bool = False) -> None:
    validate_inventory(skip_freshness=skip_freshness)
    validate_project(skip_freshness=skip_freshness)
    validate_shared_references(skip_freshness=skip_freshness)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    phase_runners = {
        "inventory": lambda: validate_inventory(skip_freshness=args.skip_freshness_checks),
        "project": lambda: validate_project(skip_freshness=args.skip_freshness_checks),
        "shared-references": lambda: validate_shared_references(skip_freshness=args.skip_freshness_checks),
        "all": lambda: validate_all(skip_freshness=args.skip_freshness_checks),
    }
    phase_runners[args.phase]()
    print("Marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
