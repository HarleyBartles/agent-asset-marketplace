#!/usr/bin/env python3
"""Project marketplace skills into Codex plugin trees."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path
from typing import Any, Iterable

from marketplace_utils import ROOT, as_windows_long_path, load_json, load_plugin_root_inventory
from skill_projection_helpers import _inject_plugin_identity, _strip_plugin_identity, stage_source_tree
from tree_canonicalization import compare_trees_canonicalized


VALID_SOURCE_CATEGORIES = {"first_party", "third_party"}
VALID_CONTENT_MODES = {"verbatim", "normalised", "adapted"}
SKIP_CONTENT_MODES = {"blocked", "skipped"}
SKIP_STATUSES = {"skipped", "blocked", "out_of_scope"}

# Deterministic packaging constants copied from tools/skill_zip_artifacts.py
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "tmp",
    "temp",
    "generated",
    "logs",
    "worker-output",
}
FORBIDDEN_FILE_NAMES = {
    "skill.zip",
    "package-evidence.json",
    "package-run-receipt.json",
}



def _is_packaging_ignored(rel: Path) -> bool:
    if any(part.startswith(".") for part in rel.parts):
        return True
    if any(part in SKIP_DIR_NAMES for part in rel.parts):
        return True
    if rel.suffix.lower() == ".log":
        return True
    return False


def scan_skill_tree(skill_root: Path) -> tuple[list[Path], list[str]]:
    skill_root = skill_root.resolve()
    if not skill_root.exists():
        raise FileNotFoundError(skill_root)
    if not skill_root.is_dir():
        raise NotADirectoryError(skill_root)
    skill_root_str = as_windows_long_path(skill_root)

    packaged_files: list[Path] = []
    forbidden_paths: list[str] = []
    for current, dirnames, filenames in os.walk(skill_root_str):
        current_path = Path(current)
        dirnames.sort()
        filenames.sort()
        for dirname in list(dirnames):
            candidate = current_path / dirname
            rel = Path(str(candidate)[len(skill_root_str) + 1 :])
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())

        for filename in filenames:
            candidate = current_path / filename
            rel = Path(str(candidate)[len(skill_root_str) + 1 :])
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())
                continue
            if rel.name in FORBIDDEN_FILE_NAMES:
                forbidden_paths.append(rel.as_posix())
                continue
            if _is_packaging_ignored(rel):
                continue
            packaged_files.append(candidate)

    packaged_files.sort(key=lambda path: str(path)[len(skill_root_str) + 1 :])
    forbidden_paths = sorted(dict.fromkeys(forbidden_paths))
    return packaged_files, forbidden_paths


def _load_bundle_manifest(plugin_root: Path) -> dict[str, Any] | None:
    """Load a projection-lane bundle manifest or return None for legacy/empty plugins."""
    manifest_path = plugin_root / "references" / "bundle-manifest.json"
    if not manifest_path.exists():
        return None
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"{manifest_path} must contain a JSON object")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return None
    if entries:
        first = entries[0]
        if not isinstance(first, dict):
            return None
        if "canonical_name" not in first or "canonical_source_path" not in first:
            return None
        csp = first.get("canonical_source_path", "")
        if isinstance(csp, str) and Path(csp).name == "SKILL.md":
            return None
    return manifest


def _validate_entry(entry: dict[str, Any]) -> bool:
    """Validate a bundle entry and return True if it should be projected."""
    canonical_name = entry.get("canonical_name")
    if not isinstance(canonical_name, str) or not canonical_name:
        raise ValueError(f"entry missing canonical_name: {entry}")
    source_category = entry.get("source_category")
    if source_category not in VALID_SOURCE_CATEGORIES:
        raise ValueError(f"entry {canonical_name} invalid source_category: {source_category}")
    import_status = entry.get("import_status")
    content_mode = entry.get("content_mode")
    if import_status in SKIP_STATUSES or content_mode in SKIP_CONTENT_MODES:
        return False
    if content_mode not in VALID_CONTENT_MODES:
        raise ValueError(f"entry {canonical_name} invalid content_mode: {content_mode}")
    for field in ("canonical_source_path", "local_path"):
        if not isinstance(entry.get(field), str) or not entry[field]:
            raise ValueError(f"entry {canonical_name} missing {field}")
    overlay_path = entry.get("adaptation_overlay_path")
    if source_category == "first_party":
        if content_mode != "verbatim":
            raise ValueError(f"first-party entry {canonical_name} must be verbatim")
        if overlay_path is not None:
            raise ValueError(f"first-party entry {canonical_name} must not declare adaptation_overlay_path")
    else:
        if content_mode == "verbatim":
            if overlay_path is not None:
                raise ValueError(f"verbatim entry {canonical_name} must not declare adaptation_overlay_path")
        else:
            if not isinstance(overlay_path, str) or not overlay_path:
                raise ValueError(f"third-party {content_mode} entry {canonical_name} requires adaptation_overlay_path")
    return True


def _collect_skill_groups(*, plugin_name: str | None = None) -> dict[str, list[dict[str, Any]]]:
    """Group active bundle entries by canonical_name across all enabled plugin roots."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for spec in load_plugin_root_inventory():
        if not spec.get("enabled", True):
            continue
        if plugin_name and spec["name"] != plugin_name:
            continue
        plugin_root = ROOT / spec["plugin_root"]
        manifest = _load_bundle_manifest(plugin_root)
        if manifest is None:
            continue
        for entry in manifest.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if not _validate_entry(entry):
                continue
            canonical_name = entry["canonical_name"]
            enriched = {
                **entry,
                "plugin_root": spec["plugin_root"],
                "pack_name": spec["name"],
            }
            groups.setdefault(canonical_name, []).append(enriched)

    for canonical_name, entries in groups.items():
        reference = (entries[0]["canonical_source_path"], entries[0].get("adaptation_overlay_path"))
        for entry in entries[1:]:
            candidate = (entry["canonical_source_path"], entry.get("adaptation_overlay_path"))
            if candidate != reference:
                conflicting = [
                    f"{e['pack_name']}: source={e['canonical_source_path']}, overlay={e.get('adaptation_overlay_path')}"
                    for e in entries
                ]
                raise ValueError(
                    f"cross-pack conflict for {canonical_name}: diverging canonical_source_path or adaptation_overlay_path; "
                    f"packs: {conflicting}"
                )
    return groups


def _expected_plugin_roots(groups: dict[str, list[dict[str, Any]]]) -> dict[str, set[str]]:
    """Map plugin_root -> set of expected skill directory names."""
    expected: dict[str, set[str]] = {}
    for entries in groups.values():
        for entry in entries:
            local_path = entry["local_path"]
            parts = Path(local_path).parts
            if len(parts) >= 2 and parts[0] == "skills":
                expected.setdefault(entry["plugin_root"], set()).add(parts[1])
    return expected


def _copy_staged_tree(staged_root: Path, destination_root: Path) -> None:
    """Replace a plugin skill tree with the freshly staged tree."""
    if destination_root.exists():
        shutil.rmtree(as_windows_long_path(destination_root))
    destination_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(as_windows_long_path(staged_root), as_windows_long_path(destination_root))




def project_skills(*, write: bool = True, plugin_name: str | None = None) -> None:
    """Project every active skill into plugin trees and flat skill zips."""
    groups = _collect_skill_groups(plugin_name=plugin_name)

    for canonical_name, entries in sorted(groups.items()):
        source_path = entries[0]["canonical_source_path"]
        source_root = ROOT / source_path

        if not source_root.is_dir():
            raise ValueError(f"entry {canonical_name} canonical_source_path must be a directory: {source_root}")

        staged_root, tempdir = stage_source_tree(source_root)
        try:
            _packaged_files, forbidden_paths = scan_skill_tree(staged_root)
            if forbidden_paths:
                raise ValueError(f"{canonical_name} staged tree contains forbidden paths: {forbidden_paths}")

            _strip_plugin_identity(staged_root)

            if write:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    _copy_staged_tree(staged_root, destination_root)
                    _inject_plugin_identity(destination_root, entry["pack_name"])
            else:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    if not destination_root.exists():
                        raise FileNotFoundError(f"projection missing for {canonical_name} in {entry['pack_name']}: {destination_root}")
                    compare_trees_canonicalized(staged_root, destination_root)
        finally:
            tempdir.cleanup()

    expected_roots = _expected_plugin_roots(groups)
    for spec in load_plugin_root_inventory():
        if not spec.get("enabled", True):
            continue
        plugin_root = spec["plugin_root"]
        skills_root = ROOT / plugin_root / "skills"
        if not skills_root.is_dir():
            continue
        roots = expected_roots.get(plugin_root, set())
        for child in sorted(skills_root.iterdir()):
            if not child.is_dir():
                continue
            if child.name in roots:
                continue
            if write:
                shutil.rmtree(as_windows_long_path(child))
                print(f"Pruned stale projected skill root {child.relative_to(ROOT)}")
            else:
                raise ValueError(f"{plugin_root} has stale projected skill roots: {child.name}")

    if write:
        print(f"OK project skills: materialized {len(groups)} unique skills")
    else:
        print(f"OK project skills: validated {len(groups)} unique skills")


def expected_skill_names(*, plugin_name: str | None = None) -> set[str]:
    """Return the set of canonical skill names currently projected."""
    return set(_collect_skill_groups(plugin_name=plugin_name).keys())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project skills into plugin trees")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--plugin", help="target one plugin by name")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    project_skills(write=not args.check, plugin_name=args.plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())