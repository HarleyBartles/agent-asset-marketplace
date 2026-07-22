#!/usr/bin/env python3
"""Project marketplace skills into Codex plugin trees and flat skill zips."""

from __future__ import annotations

import argparse
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Iterable

from marketplace_utils import ROOT, as_windows_long_path, load_json, load_plugin_root_inventory
from skill_overlay_materializer import stage_overlay_tree
from tree_canonicalization import compare_trees_canonicalized


GENERATED_SKILL_ZIPS_ROOT = ROOT / "generated/skill-zips"

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
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".jsonl",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".py",
    ".sh",
    ".svg",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".cjs",
    ".mjs",
    ".cts",
    ".mts",
    ".dot",
    ".upstream",
    ".ts",
    ".tsx",
}
TEXT_FILENAMES = {"SKILL.md", "openai.yaml"}
CANONICAL_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
CANONICAL_ZIP_PERMISSIONS = 0o644

def _relative_path(path: Path, root: Path) -> str:
    path_text = as_windows_long_path(path)
    root_text = as_windows_long_path(root)
    if os.name == "nt":
        if not path_text.startswith("\\\\?\\"):
            path_text = "\\\\?\\" + path_text
        if not root_text.startswith("\\\\?\\"):
            root_text = "\\\\?\\" + root_text
        prefix = root_text + "\\"
        if path_text.startswith(prefix):
            return path_text[len(prefix) :].replace("\\", "/")
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as exc:
        raise ValueError(f"packaged path {path} is not under {root}") from exc


def _is_text_file(path: Path, raw: bytes | None = None) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES or (
        raw is not None and raw.startswith(b"#!")
    )


def _canonicalize_text_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _read_canonical_file_bytes(path: Path) -> bytes:
    raw = Path(as_windows_long_path(path)).read_bytes()
    if _is_text_file(path, raw):
        raw.decode("utf-8")
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        return _canonicalize_text_bytes(raw)
    return raw


def _zip_info_for_arcname(arcname: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(arcname, date_time=CANONICAL_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100000 | CANONICAL_ZIP_PERMISSIONS) << 16
    return info


def _write_canonical_zip_tree(
    archive: zipfile.ZipFile,
    files: Iterable[Path],
    *,
    root: Path,
    archive_root_name: str,
) -> None:
    for file_path in files:
        rel = _relative_path(file_path, root)
        archive.writestr(_zip_info_for_arcname(f"{archive_root_name}/{rel}"), _read_canonical_file_bytes(file_path))


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


def _write_skill_zip(canonical_name: str, staged_root: Path, packaged_files: list[Path]) -> None:
    """Atomically write a deterministic flat skill zip."""
    GENERATED_SKILL_ZIPS_ROOT.mkdir(parents=True, exist_ok=True)
    zip_path = GENERATED_SKILL_ZIPS_ROOT / f"{canonical_name}.zip"
    tmp_path = zip_path.parent / f".{zip_path.name}.{os.getpid()}.tmp"
    try:
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            _write_canonical_zip_tree(
                archive,
                packaged_files,
                root=staged_root,
                archive_root_name=canonical_name,
            )
        os.replace(str(as_windows_long_path(tmp_path)), str(as_windows_long_path(zip_path)))
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def _check_skill_zip(canonical_name: str, staged_root: Path, packaged_files: list[Path]) -> None:
    """Validate an existing flat skill zip matches the staged tree."""
    zip_path = GENERATED_SKILL_ZIPS_ROOT / f"{canonical_name}.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"expected zip missing: {zip_path}")
    with zipfile.ZipFile(zip_path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"{zip_path} zip integrity failure at {bad}")
        names = sorted(name for name in archive.namelist() if not name.endswith("/"))
        roots = sorted({name.split("/", 1)[0] for name in names})
        if len(roots) != 1 or roots[0] != canonical_name:
            raise ValueError(f"{zip_path} must contain exactly one top-level folder named {canonical_name}")
        if f"{canonical_name}/SKILL.md" not in names:
            raise ValueError(f"{zip_path} missing {canonical_name}/SKILL.md")
        expected_names = sorted(f"{canonical_name}/{_relative_path(path, staged_root)}" for path in packaged_files)
        if names != expected_names:
            raise ValueError(f"{zip_path} namelist mismatch: expected {expected_names}, got {names}")
        for file_path in packaged_files:
            arcname = f"{canonical_name}/{_relative_path(file_path, staged_root)}"
            with archive.open(arcname) as member:
                member_bytes = member.read()
            expected_bytes = _read_canonical_file_bytes(file_path)
            if member_bytes != expected_bytes:
                raise ValueError(f"{zip_path} content mismatch for {arcname}")


def _cleanup_generated_skill_zips(expected_names: set[str]) -> None:
    """Remove stale root-level zips and any leftover per-pack subdirectories or registry files."""
    if not GENERATED_SKILL_ZIPS_ROOT.exists():
        return
    for path in sorted(GENERATED_SKILL_ZIPS_ROOT.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir():
            if path.resolve() == GENERATED_SKILL_ZIPS_ROOT.resolve():
                continue
            try:
                next(path.iterdir())
            except StopIteration:
                path.rmdir()
            continue
        if path.name in expected_names and path.parent == GENERATED_SKILL_ZIPS_ROOT:
            continue
        path.unlink()
        print(f"Pruned stale generated zip {path.relative_to(ROOT)}")


def _validate_generated_skill_zips(expected_names: set[str]) -> None:
    """Fail if any unexpected files linger under generated/skill-zips/."""
    if not GENERATED_SKILL_ZIPS_ROOT.is_dir():
        raise FileNotFoundError(GENERATED_SKILL_ZIPS_ROOT)
    missing = sorted(name for name in expected_names if not (GENERATED_SKILL_ZIPS_ROOT / name).is_file())
    extra = [
        str(path.relative_to(ROOT))
        for path in GENERATED_SKILL_ZIPS_ROOT.rglob("*")
        if path.is_file() and (path.name not in expected_names or path.parent != GENERATED_SKILL_ZIPS_ROOT)
    ]
    if missing or extra:
        raise ValueError(f"generated skill zips mismatch: missing {missing}, extra {extra}")


def project_skills(*, write: bool = True, plugin_name: str | None = None) -> None:
    """Project every active skill into plugin trees and flat skill zips."""
    groups = _collect_skill_groups(plugin_name=plugin_name)
    expected_zip_names = {f"{name}.zip" for name in groups}

    for canonical_name, entries in sorted(groups.items()):
        source_path = entries[0]["canonical_source_path"]
        overlay_path = entries[0].get("adaptation_overlay_path")
        source_root = ROOT / source_path
        overlay_root = ROOT / overlay_path if overlay_path else None

        if not source_root.is_dir():
            raise ValueError(f"entry {canonical_name} canonical_source_path must be a directory: {source_root}")

        staged_root, tempdir = stage_overlay_tree(source_root, overlay_root)
        try:
            packaged_files, forbidden_paths = scan_skill_tree(staged_root)
            if forbidden_paths:
                raise ValueError(f"{canonical_name} staged tree contains forbidden paths: {forbidden_paths}")

            if write:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    _copy_staged_tree(staged_root, destination_root)
                _write_skill_zip(canonical_name, staged_root, packaged_files)
            else:
                for entry in entries:
                    destination_root = ROOT / entry["plugin_root"] / entry["local_path"]
                    if not destination_root.exists():
                        raise FileNotFoundError(f"projection missing for {canonical_name} in {entry['pack_name']}: {destination_root}")
                    compare_trees_canonicalized(staged_root, destination_root)
                _check_skill_zip(canonical_name, staged_root, packaged_files)
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
        _cleanup_generated_skill_zips(expected_zip_names)
        print(f"OK project skills: materialized {len(groups)} unique skills")
    else:
        _validate_generated_skill_zips(expected_zip_names)
        print(f"OK project skills: validated {len(groups)} unique skills and zips")


def expected_skill_names(*, plugin_name: str | None = None) -> set[str]:
    """Return the set of canonical skill names that should produce flat zips."""
    return set(_collect_skill_groups(plugin_name=plugin_name).keys())


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project skills into plugin trees and flat skill zips")
    parser.add_argument("--check", action="store_true", help="validate without writing")
    parser.add_argument("--plugin", help="target one plugin by name")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    project_skills(write=not args.check, plugin_name=args.plugin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())