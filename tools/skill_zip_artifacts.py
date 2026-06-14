#!/usr/bin/env python3
"""Canonical skill.zip discovery, packaging, registry, and validation helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from marketplace_utils import CODEX_MARKETPLACE_MANIFEST_PATH, MARKETPLACE_PATH, load_json


ROOT = Path(__file__).resolve().parents[1]
GENERATED_SKILL_ZIPS_ROOT = ROOT / "generated/skill-zips"
GENERATED_SKILL_ZIPS_REGISTRY_PATH = GENERATED_SKILL_ZIPS_ROOT / "registry.json"

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


@dataclass(frozen=True)
class SkillTarget:
    pack: str
    skill: str
    plugin_root: Path
    skill_root: Path

    @property
    def source_path(self) -> str:
        return self.skill_root.relative_to(ROOT).as_posix()

    @property
    def zip_path(self) -> Path:
        return GENERATED_SKILL_ZIPS_ROOT / self.pack / self.skill / "skill.zip"


@dataclass(frozen=True)
class SkillArtifact:
    pack: str
    skill: str
    source_path: str
    zip_path: str
    source_file_count: int
    source_bytes: int
    source_sha256: str
    zip_size_bytes: int
    zip_sha256: str


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_marketplace_definition() -> dict[str, Any]:
    codex_manifest = load_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    marketplace_manifest = load_json(MARKETPLACE_PATH)
    if codex_manifest != marketplace_manifest:
        raise ValueError("codex-marketplace/manifest.json does not match .agents/plugins/marketplace.json")
    return codex_manifest


def discover_skill_targets() -> list[SkillTarget]:
    marketplace = load_marketplace_definition()
    targets: list[SkillTarget] = []
    for plugin in marketplace.get("plugins", []):
        if not isinstance(plugin, dict):
            raise ValueError("marketplace manifest contains a malformed plugin entry")
        plugin_name = plugin.get("name")
        source = plugin.get("source", {})
        if not isinstance(plugin_name, str) or not plugin_name:
            raise ValueError("marketplace manifest contains a plugin without a name")
        if not isinstance(source, dict) or source.get("source") != "local":
            raise ValueError(f"marketplace plugin {plugin_name} must use a local source")
        source_path = source.get("path")
        if not isinstance(source_path, str) or not source_path:
            raise ValueError(f"marketplace plugin {plugin_name} is missing a source path")

        plugin_root = (ROOT / source_path.removeprefix("./")).resolve()
        plugin_manifest_path = plugin_root / ".codex-plugin/plugin.json"
        if not plugin_manifest_path.exists():
            raise FileNotFoundError(plugin_manifest_path)
        plugin_manifest = load_json(plugin_manifest_path)
        skills_path = plugin_manifest.get("skills")
        if not isinstance(skills_path, str) or not skills_path:
            raise ValueError(f"{plugin_name} plugin manifest is missing a skills path")

        skills_root = (plugin_root / skills_path).resolve()
        if not skills_root.exists():
            raise FileNotFoundError(skills_root)

        for skill_dir in sorted((path for path in skills_root.iterdir() if path.is_dir()), key=lambda path: path.name):
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                continue
            targets.append(
                SkillTarget(
                    pack=plugin_name,
                    skill=skill_dir.name,
                    plugin_root=plugin_root,
                    skill_root=skill_dir,
                )
            )

    return sorted(targets, key=lambda item: (item.pack, item.skill))


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

    packaged_files: list[Path] = []
    forbidden_paths: list[str] = []
    for current, dirnames, filenames in os.walk(skill_root):
        current_path = Path(current)
        dirnames.sort()
        filenames.sort()
        for dirname in list(dirnames):
            candidate = current_path / dirname
            rel = candidate.relative_to(skill_root)
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())

        for filename in filenames:
            candidate = current_path / filename
            rel = candidate.relative_to(skill_root)
            if candidate.is_symlink():
                forbidden_paths.append(rel.as_posix())
                continue
            if rel.name in FORBIDDEN_FILE_NAMES:
                forbidden_paths.append(rel.as_posix())
                continue
            if _is_packaging_ignored(rel):
                continue
            packaged_files.append(candidate)

    packaged_files.sort(key=lambda path: path.relative_to(skill_root).as_posix())
    forbidden_paths = sorted(dict.fromkeys(forbidden_paths))
    return packaged_files, forbidden_paths


def compute_source_fingerprint(skill_root: Path) -> tuple[str, int, int, list[Path], list[str]]:
    packaged_files, forbidden_paths = scan_skill_tree(skill_root)
    digest = hashlib.sha256()
    total_bytes = 0
    for path in packaged_files:
        rel = path.relative_to(skill_root).as_posix()
        raw = path.read_bytes()
        file_digest = _sha256_bytes(raw)
        total_bytes += len(raw)
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_digest.encode("ascii"))
        digest.update(b"\0")
        digest.update(str(len(raw)).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest(), len(packaged_files), total_bytes, packaged_files, forbidden_paths


def _create_zip_path(target: SkillTarget) -> Path:
    dest = target.zip_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def package_skill_target(target: SkillTarget) -> SkillArtifact:
    if target.skill_root.name != target.skill:
        raise ValueError(f"{target.pack}/{target.skill} source folder mismatch: {target.skill_root.name}")

    source_sha256, source_file_count, source_bytes, files, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{target.pack}/{target.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")

    dest = _create_zip_path(target)
    if dest.exists():
        dest.unlink()

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=dest.parent, prefix=f"{target.skill}-", suffix=".tmp") as tmp:
            tmp_path = Path(tmp.name)
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                rel = file_path.relative_to(target.skill_root).as_posix()
                archive.write(file_path, arcname=f"{target.skill}/{rel}")
        tmp_path.replace(dest)
    except Exception:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise

    zip_sha256 = sha256_file(dest)
    return SkillArtifact(
        pack=target.pack,
        skill=target.skill,
        source_path=target.source_path,
        zip_path=dest.relative_to(ROOT).as_posix(),
        source_file_count=source_file_count,
        source_bytes=source_bytes,
        source_sha256=source_sha256,
        zip_size_bytes=dest.stat().st_size,
        zip_sha256=zip_sha256,
    )


def _archive_root_names(zip_names: Iterable[str]) -> list[str]:
    roots = sorted({name.split("/", 1)[0] for name in zip_names if name and not name.endswith("/")})
    return roots


def inspect_skill_zip(skill: str, zip_path: Path) -> tuple[list[str], str | None]:
    errors: list[str] = []
    root: str | None = None
    if zip_path.name != "skill.zip":
        errors.append("archive filename must be skill.zip")
    try:
        with zipfile.ZipFile(zip_path) as archive:
            bad = archive.testzip()
            if bad:
                errors.append(f"zip integrity failure at {bad}")
            names = [name for name in archive.namelist() if name and not name.endswith("/")]
            roots = _archive_root_names(names)
            if len(roots) != 1:
                errors.append("archive must contain exactly one top-level folder")
                return errors, None
            root = roots[0]
            if root != skill:
                errors.append(f"archive top-level folder must be {skill}")
            if f"{skill}/SKILL.md" not in names:
                errors.append("SKILL.md missing")
            forbidden_members = []
            for name in names:
                rel = Path(name)
                if rel.is_absolute() or ".." in rel.parts:
                    forbidden_members.append(name)
                if any(part in SKIP_DIR_NAMES for part in rel.parts):
                    forbidden_members.append(name)
                if rel.name in FORBIDDEN_FILE_NAMES:
                    forbidden_members.append(name)
                if rel.suffix.lower() == ".log":
                    forbidden_members.append(name)
            if forbidden_members:
                errors.append("archive contains forbidden members: " + ", ".join(sorted(dict.fromkeys(forbidden_members))))
    except Exception as exc:
        errors.append(f"archive inspection failed: {exc}")
    return errors, root


def validate_package_matches_source(target: SkillTarget, artifact: SkillArtifact) -> None:
    zip_path = ROOT / artifact.zip_path
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    if zip_path.name != "skill.zip":
        raise ValueError(f"{artifact.pack}/{artifact.skill} archive filename mismatch")

    errors, root = inspect_skill_zip(target.skill, zip_path)
    if errors:
        raise ValueError(f"{artifact.pack}/{artifact.skill} archive invalid: {'; '.join(errors)}")
    if root != target.skill:
        raise ValueError(f"{artifact.pack}/{artifact.skill} archive root mismatch")

    source_sha256, source_file_count, source_bytes, files, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{artifact.pack}/{artifact.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")
    if source_sha256 != artifact.source_sha256:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source fingerprint mismatch")
    if source_file_count != artifact.source_file_count:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source file count mismatch")
    if source_bytes != artifact.source_bytes:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source byte count mismatch")

    with zipfile.ZipFile(zip_path) as archive:
        extracted_names = sorted(name for name in archive.namelist() if name and not name.endswith("/"))
        expected_names = [f"{target.skill}/{path.relative_to(target.skill_root).as_posix()}" for path in files]
        if extracted_names != expected_names:
            raise ValueError(f"{artifact.pack}/{artifact.skill} archive file inventory mismatch")
        for name in extracted_names:
            if archive.read(name) != (target.skill_root / Path(name).relative_to(target.skill)).read_bytes():
                raise ValueError(f"{artifact.pack}/{artifact.skill} archive content drift at {name}")

    if sha256_file(zip_path) != artifact.zip_sha256:
        raise ValueError(f"{artifact.pack}/{artifact.skill} zip sha256 mismatch")
    if zip_path.stat().st_size != artifact.zip_size_bytes:
        raise ValueError(f"{artifact.pack}/{artifact.skill} zip size mismatch")


def artifact_to_record(artifact: SkillArtifact) -> dict[str, Any]:
    return {
        "pack": artifact.pack,
        "skill": artifact.skill,
        "source_path": artifact.source_path,
        "zip_path": artifact.zip_path,
        "source_file_count": artifact.source_file_count,
        "source_bytes": artifact.source_bytes,
        "source_sha256": artifact.source_sha256,
        "zip_size_bytes": artifact.zip_size_bytes,
        "zip_sha256": artifact.zip_sha256,
    }


def record_to_artifact(record: dict[str, Any]) -> SkillArtifact:
    return SkillArtifact(
        pack=str(record["pack"]),
        skill=str(record["skill"]),
        source_path=str(record["source_path"]),
        zip_path=str(record["zip_path"]),
        source_file_count=int(record["source_file_count"]),
        source_bytes=int(record["source_bytes"]),
        source_sha256=str(record["source_sha256"]),
        zip_size_bytes=int(record["zip_size_bytes"]),
        zip_sha256=str(record["zip_sha256"]),
    )


def build_registry(records: list[SkillArtifact], exclusions: list[dict[str, str]] | None = None) -> dict[str, Any]:
    exclusions = exclusions or []
    return {
        "schema_version": "skill-zip-registry.v1",
        "source_manifest_paths": [
            ".agents/plugins/marketplace.json",
            "codex-marketplace/manifest.json",
        ],
        "artifact_count": len(records),
        "excluded_count": len(exclusions),
        "artifacts": [artifact_to_record(record) for record in sorted(records, key=lambda item: (item.pack, item.skill))],
        "excluded": exclusions,
    }


def _target_key(pack: str, skill: str) -> tuple[str, str]:
    return pack, skill


def _discover_generated_surface_files() -> list[Path]:
    if not GENERATED_SKILL_ZIPS_ROOT.exists():
        return []
    files = [path for path in GENERATED_SKILL_ZIPS_ROOT.rglob("*") if path.is_file()]
    files.sort(key=lambda path: path.relative_to(ROOT).as_posix())
    return files


def validate_generated_surface(expected_records: list[SkillArtifact]) -> None:
    expected_zip_paths = {
        (ROOT / record.zip_path).resolve().relative_to(ROOT).as_posix()
        for record in expected_records
    }
    unexpected_files: list[str] = []
    actual_zip_paths: set[str] = set()
    for path in _discover_generated_surface_files():
        rel = path.relative_to(ROOT).as_posix()
        if path.resolve() == GENERATED_SKILL_ZIPS_REGISTRY_PATH.resolve():
            continue
        if path.name == "skill.zip":
            actual_zip_paths.add(rel)
            continue
        unexpected_files.append(rel)
    if unexpected_files:
        raise ValueError("generated/skill-zips contains unexpected files: " + ", ".join(unexpected_files))
    if actual_zip_paths != expected_zip_paths:
        missing = sorted(expected_zip_paths - actual_zip_paths)
        extra = sorted(actual_zip_paths - expected_zip_paths)
        parts = []
        if missing:
            parts.append("missing zips: " + ", ".join(missing))
        if extra:
            parts.append("unregistered zips: " + ", ".join(extra))
        raise ValueError("generated/skill-zips artifact surface mismatch: " + "; ".join(parts))


def _select_targets(targets: list[SkillTarget], pack: str | None, skill: str | None) -> set[tuple[str, str]]:
    if skill:
        parts = skill.split("/", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("--skill must be formatted as <pack>/<skill-name>")
        return {(parts[0], parts[1])}
    if pack:
        return {_target_key(target.pack, target.skill) for target in targets if target.pack == pack}
    return {_target_key(target.pack, target.skill) for target in targets}


def load_registry() -> dict[str, Any]:
    if not GENERATED_SKILL_ZIPS_REGISTRY_PATH.exists():
        raise FileNotFoundError(GENERATED_SKILL_ZIPS_REGISTRY_PATH)
    return load_json(GENERATED_SKILL_ZIPS_REGISTRY_PATH)


def _artifact_from_existing(target: SkillTarget) -> SkillArtifact:
    zip_path = target.zip_path
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    if zip_path.name != "skill.zip":
        raise ValueError(f"{target.pack}/{target.skill} archive filename mismatch")

    source_sha256, source_file_count, source_bytes, files, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{target.pack}/{target.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")

    errors, root = inspect_skill_zip(target.skill, zip_path)
    if errors:
        raise ValueError(f"{target.pack}/{target.skill} archive invalid: {'; '.join(errors)}")
    if root != target.skill:
        raise ValueError(f"{target.pack}/{target.skill} archive root mismatch")

    zip_sha256 = sha256_file(zip_path)
    return SkillArtifact(
        pack=target.pack,
        skill=target.skill,
        source_path=target.source_path,
        zip_path=zip_path.relative_to(ROOT).as_posix(),
        source_file_count=source_file_count,
        source_bytes=source_bytes,
        source_sha256=source_sha256,
        zip_size_bytes=zip_path.stat().st_size,
        zip_sha256=zip_sha256,
    )


def synchronize_skill_zips(*, pack: str | None = None, skill: str | None = None, write: bool) -> dict[str, Any]:
    targets = discover_skill_targets()
    selected = _select_targets(targets, pack=pack, skill=skill)
    if not selected:
        if pack:
            raise ValueError(f"no installable skills found for pack {pack}")
        raise ValueError("no installable skills found in the active marketplace manifests")

    artifacts: list[SkillArtifact] = []
    for target in targets:
        key = _target_key(target.pack, target.skill)
        if key in selected:
            artifact = package_skill_target(target) if write else _artifact_from_existing(target)
        else:
            artifact = _artifact_from_existing(target)
        artifacts.append(artifact)

    registry = build_registry(artifacts, exclusions=[])
    if write:
        validate_generated_surface(artifacts)
        GENERATED_SKILL_ZIPS_ROOT.mkdir(parents=True, exist_ok=True)
        with GENERATED_SKILL_ZIPS_REGISTRY_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(registry, handle, indent=2)
            handle.write("\n")
    else:
        validate_generated_surface(artifacts)
        current = load_registry()
        if current != registry:
            raise ValueError("generated/skill-zips/registry.json is stale or inconsistent with on-disk artifacts")
    return registry


def validate_skill_zip_registry() -> dict[str, Any]:
    registry = load_registry()
    targets = discover_skill_targets()
    artifacts = [_artifact_from_existing(target) for target in targets]
    validate_generated_surface(artifacts)
    expected = build_registry(artifacts, exclusions=[])
    if registry != expected:
        raise ValueError("generated/skill-zips/registry.json does not match the current artifact state")
    return registry


def registry_summary(registry: dict[str, Any]) -> str:
    exclusions = registry.get("excluded", [])
    exclusion_summary = "none" if not exclusions else ", ".join(
        f"{entry.get('pack')}/{entry.get('skill')}: {entry.get('reason')}" for entry in exclusions
    )
    return (
        f"artifact_count={registry.get('artifact_count')}, "
        f"registry_path={GENERATED_SKILL_ZIPS_REGISTRY_PATH.relative_to(ROOT).as_posix()}, "
        f"excluded={exclusion_summary}"
    )


def print_registry_receipt(registry: dict[str, Any]) -> None:
    artifact_count = registry.get("artifact_count", 0)
    exclusion_count = registry.get("excluded_count", 0)
    print(f"OK skill-zips registry: {GENERATED_SKILL_ZIPS_REGISTRY_PATH.relative_to(ROOT).as_posix()}")
    print(f"OK generated artifacts: {artifact_count}")
    print(f"OK explicit exclusions: {exclusion_count}")
    print("OK archive guard: skill.zip is not nested inside packaged skill contents")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or validate canonical skill.zip artifacts")
    parser.add_argument("--check", action="store_true", help="validate on-disk artifacts without rewriting")
    parser.add_argument("--all", action="store_true", help="package every discovered installable skill")
    parser.add_argument("--pack", help="package every installable skill in a single marketplace pack")
    parser.add_argument("--skill", help="package one installable skill as <pack>/<skill-name>")
    args = parser.parse_args()

    selected_flags = sum(1 for value in (args.check, args.all, args.pack is not None, args.skill is not None) if value)
    if selected_flags != 1:
        parser.error("choose exactly one of --check, --all, --pack, or --skill")

    if args.check:
        registry = validate_skill_zip_registry()
        print_registry_receipt(registry)
        return 0

    if args.all:
        registry = synchronize_skill_zips(write=True)
    elif args.pack:
        registry = synchronize_skill_zips(pack=args.pack, write=True)
    else:
        registry = synchronize_skill_zips(skill=args.skill, write=True)

    print_registry_receipt(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
