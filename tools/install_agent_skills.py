#!/usr/bin/env python3
"""Install/refresh skills in .agents/skills from installed marketplace plugins."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, MARKETPLACE_PATH, load_json

AGENTS_SKILLS_PATH = ROOT / ".agents/skills"


def _load_marketplace_config() -> dict[str, Any]:
    """Load the marketplace configuration."""
    config = load_json(MARKETPLACE_PATH)
    if not isinstance(config, dict):
        raise ValueError(f"{MARKETPLACE_PATH}: must contain a JSON object")
    return config


def _get_installed_plugins(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Get plugins that should be installed (INSTALLED_BY_DEFAULT)."""
    plugins = config.get("plugins", [])
    if not isinstance(plugins, list):
        raise ValueError(f"{MARKETPLACE_PATH}: plugins must be a list")
    
    installed = []
    for plugin in plugins:
        if not isinstance(plugin, dict):
            continue
        policy = plugin.get("policy", {})
        if not isinstance(policy, dict):
            continue
        installation = policy.get("installation")
        if installation == "INSTALLED_BY_DEFAULT":
            installed.append(plugin)
    return installed


def _get_plugin_skills_path(plugin: dict[str, Any]) -> Path | None:
    """Get the skills directory path for a plugin."""
    source = plugin.get("source", {})
    if not isinstance(source, dict):
        return None
    
    source_type = source.get("source")
    if source_type != "local":
        return None
    
    path = source.get("path")
    if not isinstance(path, str) or not path:
        return None
    
    plugin_path = ROOT / path
    skills_path = plugin_path / "skills"
    return skills_path if skills_path.is_dir() else None


def _copy_skill_directory(source_skill: Path, dest_skill: Path) -> None:
    """Copy a skill directory from plugin to .agents/skills."""
    if dest_skill.exists():
        shutil.rmtree(dest_skill)
    
    shutil.copytree(source_skill, dest_skill)
    print(f"Installed skill: {dest_skill.relative_to(ROOT)}")


def _files_are_identical(source: Path, dest: Path) -> bool:
    """Check if two files have identical content."""
    if not source.exists() or not dest.exists():
        return False
    return source.read_bytes() == dest.read_bytes()


def _skill_needs_update(source_skill: Path, dest_skill: Path) -> bool:
    """Check if a skill needs to be updated."""
    if not dest_skill.exists():
        return True

    # Check if all files exist and have identical content
    for source_file in source_skill.rglob("*"):
        if not source_file.is_file():
            continue
        relative_path = source_file.relative_to(source_skill)
        dest_file = dest_skill / relative_path

        if not dest_file.exists():
            return True

        if not _files_are_identical(source_file, dest_file):
            return True

    # Check if there are any extra files in dest
    for dest_file in dest_skill.rglob("*"):
        if not dest_file.is_file():
            continue
        relative_path = dest_file.relative_to(dest_skill)
        source_file = source_skill / relative_path

        if not source_file.exists():
            return True

    return False


def _install_plugin_skills(plugin: dict[str, Any], check_mode: bool = False) -> bool:
    """Install skills from a single plugin."""
    skills_path = _get_plugin_skills_path(plugin)
    if skills_path is None:
        return False
    
    plugin_name = plugin.get("name", "unknown")
    if not isinstance(plugin_name, str):
        return False
    
    installed_any = False
    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        dest_skill = AGENTS_SKILLS_PATH / skill_dir.name
        
        if check_mode:
            # In check mode, verify if skills would need installation
            if not dest_skill.exists():
                print(f"CHECK: Would install skill: {dest_skill.relative_to(ROOT)}")
                installed_any = True
            elif _skill_needs_update(skill_dir, dest_skill):
                print(f"CHECK: Skill {dest_skill.relative_to(ROOT)} would be updated")
                installed_any = True
        else:
            if _skill_needs_update(skill_dir, dest_skill):
                _copy_skill_directory(skill_dir, dest_skill)
                installed_any = True
    
    return installed_any


def _clean_orphan_skills(installed_plugins: list[dict[str, Any]], check_mode: bool = False) -> bool:
    """Remove skills that don't belong to any installed plugin."""
    if not AGENTS_SKILLS_PATH.exists():
        return False
    
    # Collect all skill names from installed plugins
    installed_skill_names = set()
    for plugin in installed_plugins:
        skills_path = _get_plugin_skills_path(plugin)
        if skills_path is None:
            continue
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                installed_skill_names.add(skill_dir.name)
    
    cleaned_any = False
    for skill_dir in sorted(AGENTS_SKILLS_PATH.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        if skill_dir.name not in installed_skill_names:
            if check_mode:
                print(f"CHECK: Would remove orphan skill: {skill_dir.relative_to(ROOT)}")
                cleaned_any = True
            else:
                shutil.rmtree(skill_dir)
                print(f"Removed orphan skill: {skill_dir.relative_to(ROOT)}")
                cleaned_any = True
    
    return cleaned_any


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install/refresh skills in .agents/skills from installed marketplace plugins"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: report what would change without making changes"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    
    config = _load_marketplace_config()
    installed_plugins = _get_installed_plugins(config)
    
    if not installed_plugins:
        print("No plugins with INSTALLED_BY_DEFAULT policy found")
        return 0
    
    print(f"Found {len(installed_plugins)} installed plugin(s)")
    
    # Ensure .agents/skills directory exists
    if not args.check:
        AGENTS_SKILLS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Install skills from each plugin
    changes_made = False
    for plugin in installed_plugins:
        plugin_name = plugin.get("name", "unknown")
        print(f"\nProcessing plugin: {plugin_name}")
        if _install_plugin_skills(plugin, check_mode=args.check):
            changes_made = True
    
    # Clean orphan skills
    print("\nChecking for orphan skills...")
    if _clean_orphan_skills(installed_plugins, check_mode=args.check):
        changes_made = True
    
    if args.check:
        if changes_made:
            print("\nCHECK: Changes would be made")
            return 1
        else:
            print("\nCHECK: No changes needed")
            return 0
    else:
        if changes_made:
            print("\nSkills installed/refreshed successfully")
        else:
            print("\nNo changes needed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())