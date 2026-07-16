#!/usr/bin/env python3
"""Validate that generated skill-zips changed only with matching source updates."""

from __future__ import annotations

import argparse
import json
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from skill_zip_artifacts import (
    GENERATED_SKILL_ZIPS_REGISTRY_PATH,
    ROOT,
    artifact_to_record,
    load_registry,
    record_to_artifact,
    validate_skill_zip_registry,
)
from marketplace_utils import load_json

PACKAGING_TOOLING_PATHS = {
    "tools/generate_pack_manifests.py",
    "tools/skill_zip_artifacts.py",
    "tools/skill_gpt_exports.py",
    "tools/materialize_projection.py",
    "tools/update_skill_artifacts.py",
    "tools/package_skill_zips.py",
}


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _git_text(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _load_git_json(*args: str) -> dict[str, Any] | None:
    text = _git_text(*args)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"WARNING: failed to parse JSON from {' '.join(args)}: {exc}", file=sys.stderr)
        return None


def _path_changes(base: str) -> list[str]:
    return _git_lines("diff", "--name-only", base, "--")


def _path_status_changes(base: str) -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "diff", "--name-status", base, "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    entries: list[tuple[str, str]] = []
    for raw_line in result.stdout.splitlines():
        if not raw_line.strip():
            continue
        parts = raw_line.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            entries.append((status, parts[1]))
            entries.append((status, parts[2]))
            continue
        if len(parts) >= 2:
            entries.append((status, parts[-1]))
    return entries


def _generated_changes(base: str) -> list[tuple[str, str]]:
    return [(status, path) for status, path in _path_status_changes(base) if path.startswith("generated/skill-zips/")]


def _source_changes(base: str) -> list[str]:
    return [
        path
        for path in _path_changes(base)
        if not path.startswith("generated/skill-zips/") and not path.startswith(".git/")
    ]


def _artifact_key_from_generated_path(path: str) -> tuple[str, str] | None:
    rel = Path(path)
    parts = rel.parts
    if len(parts) != 5 or parts[:2] != ("generated", "skill-zips") or parts[4] != "skill.zip":
        return None
    return parts[2], parts[3]


def _source_changed_for_path(source_changes: list[str], source_path: str) -> bool:
    prefix = source_path.rstrip("/") + "/"
    return any(change == source_path or change.startswith(prefix) for change in source_changes)


def _artifact_relevant_changes(artifact: Any) -> list[str]:
    paths = [artifact.source_path, "adapters/gpt/manifest.json"]
    overlay_path = getattr(artifact, "overlay_path", None)
    if overlay_path:
        paths.append(str(overlay_path))
    if getattr(artifact, "pack", None) == "superpowers-plus":
        paths.append("codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json")
        adaptation_overlay_path = _superpowers_adaptation_overlay_path(getattr(artifact, "skill", ""))
        if adaptation_overlay_path:
            paths.append(adaptation_overlay_path)
    return paths


@lru_cache(maxsize=1)
def _superpowers_bundle_manifest() -> dict[str, Any] | None:
    bundle_manifest_path = ROOT / "codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json"
    if not bundle_manifest_path.exists():
        return None
    loaded = load_json(bundle_manifest_path)
    if not isinstance(loaded, dict):
        return None
    return loaded


@lru_cache(maxsize=None)
def _superpowers_adaptation_overlay_path(skill: str) -> str | None:
    bundle_manifest = _superpowers_bundle_manifest()
    if not bundle_manifest:
        return None
    for entry in bundle_manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("canonical_name") != skill:
            continue
        overlay_path = entry.get("adaptation_overlay_path")
        if isinstance(overlay_path, str) and overlay_path.strip():
            return overlay_path
        return None
    return None


def _artifact_changed(source_changes: list[str], artifact: Any) -> bool:
    return any(_source_changed_for_path(source_changes, path) for path in _artifact_relevant_changes(artifact))


def _packaging_tool_changed(source_changes: list[str]) -> bool:
    return any(change in PACKAGING_TOOLING_PATHS for change in source_changes)


def validate_generated_drift(*, base: str, full_regeneration: bool = False) -> None:
    validate_skill_zip_registry()

    current_registry = load_registry()
    current_by_key = {
        (artifact.pack, artifact.skill): artifact
        for artifact in (record_to_artifact(record) for record in current_registry.get("artifacts", []))
    }
    current_exclusions_by_key = {
        (str(record.get("pack")), str(record.get("skill"))): record for record in current_registry.get("excluded", [])
    }

    base_registry = _load_git_json("show", f"{base}:generated/skill-zips/registry.json")
    base_by_key = {}
    base_exclusions_by_key = {}
    if isinstance(base_registry, dict):
        base_by_key = {
            (artifact.pack, artifact.skill): artifact
            for artifact in (record_to_artifact(record) for record in base_registry.get("artifacts", []))
        }
        base_exclusions_by_key = {
            (str(record.get("pack")), str(record.get("skill"))): record for record in base_registry.get("excluded", [])
        }

    source_changes = _source_changes(base)
    generated_changes = _generated_changes(base)
    packaging_tooling_changed = _packaging_tool_changed(source_changes)

    if not generated_changes:
        return

    for status, path in generated_changes:
        if path == "generated/skill-zips/registry.json":
            continue
        key = _artifact_key_from_generated_path(path)
        if key is None:
            raise ValueError(f"unexpected generated artifact path in diff: {path}")
        artifact = current_by_key.get(key)
        base_artifact = base_by_key.get(key)
        if artifact is None and key[0] == "superpowers" and current_by_key.get(("superpowers-plus", key[1])) is not None:
            continue
        if status.startswith("D"):
            if base_artifact is None:
                raise ValueError(f"deleted generated artifact diff references missing base registry entry: {path}")
            if (
                base_artifact.pack == "superpowers"
                and (current_by_key.get(("superpowers-plus", base_artifact.skill)) is not None)
            ):
                continue
            if not full_regeneration and not packaging_tooling_changed and not _artifact_changed(source_changes, base_artifact):
                raise ValueError(
                    f"generated artifact deletion detected for {base_artifact.pack}/{base_artifact.skill}: "
                    f"{path} was removed without a matching source or overlay change for {base_artifact.source_path}; "
                    f"run py -3 tools/update_skill_artifacts.py --all for explicit full regeneration "
                    f"or delete the matching source/projection input first"
                )
            continue
        if artifact is None:
            if status.startswith(("R", "C")) and base_artifact is not None:
                continue
            raise ValueError(f"generated artifact diff references missing registry entry: {path}")
        if not full_regeneration and not packaging_tooling_changed and not _artifact_changed(source_changes, artifact):
            raise ValueError(
                f"generated artifact drift detected for {artifact.pack}/{artifact.skill}: "
                f"{path} changed without a matching source or overlay change at {artifact.source_path}; "
                f"run py -3 tools/update_skill_artifacts.py --skill {artifact.pack}/{artifact.skill} "
                f"or use py -3 tools/update_skill_artifacts.py --all for explicit full regeneration"
            )

    changed_registry_keys: set[tuple[str, str]] = set()
    if isinstance(base_registry, dict):
        all_keys = set(base_by_key) | set(current_by_key) | set(base_exclusions_by_key) | set(current_exclusions_by_key)
        for key in sorted(all_keys):
            current_record = (
                artifact_to_record(current_by_key[key])
                if key in current_by_key
                else current_exclusions_by_key.get(key)
            )
            base_record = artifact_to_record(base_by_key[key]) if key in base_by_key else base_exclusions_by_key.get(key)
            if current_record != base_record:
                changed_registry_keys.add(key)

    for key in sorted(changed_registry_keys):
        artifact = current_by_key.get(key)
        if artifact is not None:
            if full_regeneration or packaging_tooling_changed:
                continue
            if not _artifact_changed(source_changes, artifact):
                raise ValueError(
                    f"generated registry drift detected for {artifact.pack}/{artifact.skill}: "
                    f"registry entry changed without a matching source or overlay change at {artifact.source_path}; "
                    f"run py -3 tools/update_skill_artifacts.py --skill {artifact.pack}/{artifact.skill} "
                    f"or use py -3 tools/update_skill_artifacts.py --all for explicit full regeneration"
                )
            continue

        exclusion = current_exclusions_by_key.get(key)
        if exclusion is None:
            continue
        if full_regeneration or packaging_tooling_changed:
            continue
        source_path = str(exclusion.get("source_path", ""))
        if not _source_changed_for_path(source_changes, source_path) and "adapters/gpt/manifest.json" not in source_changes:
            raise ValueError(
                f"generated registry drift detected for excluded skill {exclusion.get('pack')}/{exclusion.get('skill')}: "
                f"registry entry changed without a matching source or overlay manifest change at "
                f"{source_path or 'adapters/gpt/manifest.json'}; run py -3 tools/update_skill_artifacts.py --all "
                "for explicit full regeneration"
            )

    if not full_regeneration and base_registry is not None:
        for key in sorted(set(current_by_key) - set(base_by_key)):
            artifact = current_by_key[key]
            if not packaging_tooling_changed and not _artifact_changed(source_changes, artifact):
                raise ValueError(
                    f"generated registry added {artifact.pack}/{artifact.skill} without a matching source change "
                    f"at {artifact.source_path}; run py -3 tools/update_skill_artifacts.py --skill "
                    f"{artifact.pack}/{artifact.skill} or use py -3 tools/update_skill_artifacts.py --all"
                )
        for key in sorted(set(current_exclusions_by_key) - set(base_exclusions_by_key)):
            entry = current_exclusions_by_key[key]
            source_path = str(entry.get("source_path", ""))
            if not packaging_tooling_changed and not _source_changed_for_path(source_changes, source_path) and "adapters/gpt/manifest.json" not in source_changes:
                raise ValueError(
                    f"generated registry added exclusion {entry.get('pack')}/{entry.get('skill')} without a matching "
                    f"source or overlay manifest change at {source_path or 'adapters/gpt/manifest.json'}; run "
                    "py -3 tools/update_skill_artifacts.py --all for explicit full regeneration"
                )
        for key in sorted(set(base_exclusions_by_key) - set(current_exclusions_by_key)):
            entry = base_exclusions_by_key[key]
            source_path = str(entry.get("source_path", ""))
            if not packaging_tooling_changed and not _source_changed_for_path(source_changes, source_path) and "adapters/gpt/manifest.json" not in source_changes:
                raise ValueError(
                    f"generated registry removed exclusion {entry.get('pack')}/{entry.get('skill')} without a matching "
                    f"source or overlay manifest change at {source_path or 'adapters/gpt/manifest.json'}; run "
                    "py -3 tools/update_skill_artifacts.py --all for explicit full regeneration"
                )
        for key in sorted(set(base_by_key) - set(current_by_key)):
            artifact = base_by_key[key]
            if not packaging_tooling_changed and not _artifact_changed(source_changes, artifact):
                raise ValueError(
                    f"generated registry removed {artifact.pack}/{artifact.skill} without a matching source change "
                    f"at {artifact.source_path}; run py -3 tools/update_skill_artifacts.py --all "
                    f"for explicit full regeneration or delete the matching source/projection input first"
                )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated skill-zips against the current git base")
    parser.add_argument("--base", default="origin/main", help="git revision to compare against")
    parser.add_argument(
        "--full-regeneration",
        action="store_true",
        help="treat generated skill-zips changes as explicitly declared full regeneration",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    validate_generated_drift(base=args.base, full_regeneration=args.full_regeneration)
    print(
        "OK generated skill-zips drift: "
        f"base={args.base}, full_regeneration={str(args.full_regeneration).lower()}, "
        f"registry={GENERATED_SKILL_ZIPS_REGISTRY_PATH.relative_to(ROOT).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
