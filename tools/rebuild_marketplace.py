#!/usr/bin/env python3
"""Canonical full marketplace rebuild and validation entrypoint."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from superpowers_source import load_superpowers_bundle_manifest, superpowers_source_root

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOTS_PATH = ROOT / "codex-marketplace/plugins"
PLUGIN_ROOT_INVENTORY_PATH = ROOT / "codex-marketplace/plugin-roots.json"


def _run_tool(script_name: str, *args: str) -> None:
    script_path = Path(__file__).resolve().with_name(script_name)
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def _run_git(*args: str) -> None:
    subprocess.run(["git", *args], cwd=ROOT, check=True)


def _git_output(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True)
    return completed.stdout


def _load_active_plugin_root_names() -> set[str]:
    inventory = json.loads(PLUGIN_ROOT_INVENTORY_PATH.read_text(encoding="utf-8"))
    roots = inventory.get("roots")
    if not isinstance(roots, list):
        raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: roots must be a list")
    active_names: set[str] = set()
    for entry in roots:
        if not isinstance(entry, dict):
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: roots must contain objects")
        if entry.get("enabled") is False:
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{PLUGIN_ROOT_INVENTORY_PATH}: enabled roots require a non-empty name")
        active_names.add(name)
    return active_names


def _prune_stale_projected_plugin_roots() -> None:
    active_names = _load_active_plugin_root_names()
    for child in sorted(PLUGIN_ROOTS_PATH.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name in active_names:
            continue
        if not (child / ".codex-plugin" / "plugin.json").is_file():
            continue
        shutil.rmtree(child)
        print(f"Pruned stale projected plugin root {child.relative_to(ROOT)}")


def _retained_verbatim_paths() -> set[str]:
    bundle_manifest = load_superpowers_bundle_manifest()
    source_root = superpowers_source_root(bundle_manifest).relative_to(ROOT).as_posix()
    skip_paths: set[str] = set()
    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("source_category") != "third_party" or entry.get("content_mode") != "verbatim":
            continue
        canonical_source_path = entry.get("canonical_source_path")
        if isinstance(canonical_source_path, str) and canonical_source_path.strip():
            skip_paths.add(canonical_source_path)
            skip_paths.add(f"{canonical_source_path}/SKILL.md")
        source_path = entry.get("source_path")
        if isinstance(source_path, str) and source_path.strip():
            skip_paths.add(source_path)
        local_path = entry.get("local_path")
        if isinstance(local_path, str) and local_path.strip():
            skip_paths.add(f"codex-marketplace/plugins/superpowers-plus/{local_path}")
            skip_paths.add(f"codex-marketplace/plugins/superpowers-plus/{local_path}/SKILL.md")
    skip_paths.add(source_root)
    skip_paths.add(f"{source_root}/AGENTS.md")
    return skip_paths


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the full marketplace rebuild and validation stack")
    parser.add_argument("--base", default="origin/main", help="git revision used for generated drift validation")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    _run_tool("generate_plugin_root_inventory.py")
    _prune_stale_projected_plugin_roots()
    _run_tool("update_skill_artifacts.py", "--all", "--base", args.base)
    _run_tool("normalize_first_party_skill_sources.py", "--check")
    _run_tool("install_agent_skills.py")
    _run_tool("generate_repo_index.py")
    _run_tool("validate_marketplace.py")
    _run_tool("generate_repo_index.py", "--check")
    _run_tool("generate_index_mesh.py")
    _run_tool("generate_index_mesh.py", "--check")
    _run_tool("generate_first_party_skill_catalog.py", "--check")
    _run_tool("validate_repo_index.py")
    _run_tool("validate_skill_zips.py")
    skip_paths = _retained_verbatim_paths()
    changed_paths = [path for path in _git_output("diff", "--name-only", "HEAD").splitlines() if path and path not in skip_paths]
    if changed_paths:
        # Retained third-party source custody intentionally preserves upstream byte
        # fidelity, including whitespace that would be a false-positive in a generic
        # working-tree diff check. The projection mirror for those verbatim entries
        # is skipped here as well so the gate stays aligned with the custody model.
        _run_git("diff", "--check", "HEAD", "--", *changed_paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
