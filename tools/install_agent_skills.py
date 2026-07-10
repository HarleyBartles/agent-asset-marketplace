#!/usr/bin/env python3
"""Install/refresh skills in .agents/skills from installed marketplace plugins."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from marketplace_utils import ROOT, MARKETPLACE_PATH, load_json

AGENTS_SKILLS_PATH = ROOT / ".agents/skills"
PROVENANCE_PATH = AGENTS_SKILLS_PATH / ".provenance.json"


def _load_marketplace_config() -> dict[str, Any]:
    """Load the marketplace configuration."""
    config = load_json(MARKETPLACE_PATH)
    if not isinstance(config, dict):
        raise ValueError(f"{MARKETPLACE_PATH}: must contain a JSON object")
    return config


def _get_marketplace_manifest_sha() -> str:
    """Get the current marketplace manifest SHA for provenance tracking."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Fallback: use marketplace.json modification time
        return MARKETPLACE_PATH.stat().st_mtime.isoformat()


def _load_provenance() -> dict[str, Any] | None:
    """Load existing provenance data."""
    if not PROVENANCE_PATH.exists():
        return None
    try:
        return load_json(PROVENANCE_PATH)
    except (json.JSONDecodeError, ValueError):
        return None


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


def _install_plugin_skills(plugin: dict[str, Any], check_mode: bool = False, synced_skill_names: set[str] | None = None) -> bool:
    """Install skills from a single plugin."""
    skills_path = _get_plugin_skills_path(plugin)
    if skills_path is None:
        return False
    
    plugin_name = plugin.get("name", "unknown")
    if not isinstance(plugin_name, str):
        return False

    if synced_skill_names is None:
        synced_skill_names = set()

    installed_any = False
    for skill_dir in sorted(skills_path.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        dest_skill = AGENTS_SKILLS_PATH / skill_dir.name
        
        # Collision guard: if two plugins project a skill with the same name,
        # the first one wins and a warning is emitted.
        if skill_dir.name in synced_skill_names:
            print(f"WARNING: Skill '{skill_dir.name}' (from plugin '{plugin_name}') collides with an already-synced skill of the same name; keeping the first copy.")
            continue

        if check_mode:
            # In check mode, verify if skills would need installation
            if not dest_skill.exists():
                print(f"CHECK: Would install skill: {dest_skill.relative_to(ROOT)}")
                installed_any = True
            elif _skill_needs_update(skill_dir, dest_skill):
                print(f"CHECK: Skill {dest_skill.relative_to(ROOT)} would be updated")
                installed_any = True
            synced_skill_names.add(skill_dir.name)
        else:
            if _skill_needs_update(skill_dir, dest_skill):
                _copy_skill_directory(skill_dir, dest_skill)
                installed_any = True
            synced_skill_names.add(skill_dir.name)

    return installed_any


def _clean_orphan_skills(installed_plugins: list[dict[str, Any]], check_mode: bool = False, synced_skill_names: set[str] | None = None) -> bool:
    """Remove skills that don't belong to any installed plugin."""
    if not AGENTS_SKILLS_PATH.exists():
        return False

    if synced_skill_names is None:
        synced_skill_names = set()

    cleaned_any = False
    for skill_dir in sorted(AGENTS_SKILLS_PATH.iterdir()):
        if not skill_dir.is_dir():
            continue

        if skill_dir.name not in synced_skill_names:
            if check_mode:
                print(f"CHECK: Would remove orphan skill: {skill_dir.relative_to(ROOT)}")
                cleaned_any = True
            else:
                shutil.rmtree(skill_dir)
                print(f"Removed orphan skill: {skill_dir.relative_to(ROOT)}")
                cleaned_any = True

    return cleaned_any


def _write_provenance(manifest_sha: str, synced_plugins: list[str], synced_skill_count: int) -> None:
    """Write provenance data."""
    provenance = {
        "manifestSha": manifest_sha,
        "syncedAt": datetime.now().isoformat(),
        "syncedPlugins": synced_plugins,
        "syncedSkills": synced_skill_count,
        "source": "HarleyBartles/agent-asset-marketplace",
        "sourcePath": "codex-marketplace/plugins",
        "marketplaceFile": ".agents/plugins/marketplace.json"
    }
    PROVENANCE_PATH.write_text(json.dumps(provenance, indent=2), encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install/refresh skills in .agents/skills from installed marketplace plugins"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: report what would change without making changes"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force refresh even when provenance matches"
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    
    config = _load_marketplace_config()
    installed_plugins = _get_installed_plugins(config)
    
    if not installed_plugins:
        print("No plugins with INSTALLED_BY_DEFAULT policy found")
        return 0
    
    # Get current provenance and manifest SHA
    existing_provenance = _load_provenance()
    current_manifest_sha = _get_marketplace_manifest_sha()

    # Check if refresh is needed based on provenance
    if not args.force and existing_provenance:
        if existing_provenance.get("manifestSha") == current_manifest_sha:
            has_skill_dirs = AGENTS_SKILLS_PATH.exists() and any(
                AGENTS_SKILLS_PATH.iterdir()
            )
            if has_skill_dirs:
                print(f"Skills already synced at manifest SHA {current_manifest_sha}. Use --force to re-copy.")
                print(f"Synced skills: {existing_provenance.get('syncedSkills')} from {existing_provenance.get('syncedPlugins')} plugins.")
                return 0

    print(f"Found {len(installed_plugins)} installed plugin(s)")

    # Ensure .agents/skills directory exists
    if not args.check:
        AGENTS_SKILLS_PATH.mkdir(parents=True, exist_ok=True)

    # Install skills from each plugin
    changes_made = False
    synced_skill_names = set()
    synced_plugin_names = []

    for plugin in installed_plugins:
        plugin_name = plugin.get("name", "unknown")
        print(f"\nProcessing plugin: {plugin_name}")
        if _install_plugin_skills(plugin, check_mode=args.check, synced_skill_names=synced_skill_names):
            changes_made = True
            synced_plugin_names.append(plugin_name)

    # Clean orphan skills
    print("\nChecking for orphan skills...")
    if _clean_orphan_skills(installed_plugins, check_mode=args.check, synced_skill_names=synced_skill_names):
        changes_made = True
    
    # Write provenance if changes were made
    if not args.check and (changes_made or args.force):
        _write_provenance(current_manifest_sha, synced_plugin_names, len(synced_skill_names))
        print(f"\nProvenance: {current_manifest_sha} -> {PROVENANCE_PATH}")

    if args.check:
        if changes_made:
            print("\nCHECK: Changes would be made")
            return 1
        else:
            print("\nCHECK: No changes needed")
            return 0
    else:
        if changes_made:
            print(f"\nSkills installed/refreshed successfully ({len(synced_skill_names)} skills from {len(synced_plugin_names)} plugins)")
        else:
            print("\nNo changes needed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())