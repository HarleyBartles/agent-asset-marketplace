#!/usr/bin/env python3
"""Canonical skill.zip discovery, packaging, registry, and validation helpers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

from marketplace_utils import (
    CODEX_MARKETPLACE_MANIFEST_PATH,
    MARKETPLACE_PATH,
    load_json,
    load_plugin_root_inventory,
)
from skill_gpt_exports import resolve_gpt_export_policy, stage_skill_tree


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
PROJECTED_SKILL_METADATA_REQUIRED_NAMES = {
    "using-superpowers",
}


def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _relative_path(path: Path, root: Path) -> str:
    path_text = _as_windows_long_path(path)
    root_text = _as_windows_long_path(root)
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
    except ValueError:
        return str(path).replace("\\", "/")


def _projected_skill_requires_metadata(skill_root: Path) -> bool:
    return skill_root.name in PROJECTED_SKILL_METADATA_REQUIRED_NAMES


def validate_skill_markdown_frontmatter(skill_root: Path) -> None:
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        raise FileNotFoundError(skill_md)

    raw = Path(_as_windows_long_path(skill_md)).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"{skill_md} begins with a UTF-8 BOM")

    text = raw.decode("utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{skill_md} must start with a standalone YAML frontmatter delimiter")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError(f"{skill_md} is missing a closing YAML frontmatter delimiter")

    frontmatter_text = "\n".join(lines[1:end_index])
    parsed_frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(parsed_frontmatter, dict):
        raise ValueError(f"{skill_md} frontmatter must be a mapping")

    frontmatter_node = yaml.compose(frontmatter_text, Loader=yaml.SafeLoader)
    if not isinstance(frontmatter_node, MappingNode):
        raise ValueError(f"{skill_md} frontmatter must be a mapping")

    def ensure_unique_keys(node: MappingNode | SequenceNode) -> None:
        if isinstance(node, MappingNode):
            seen_keys: set[str] = set()
            for key_node, value_node in node.value:
                if not isinstance(key_node, ScalarNode):
                    raise ValueError(f"{skill_md} frontmatter keys must be simple scalars")
                key = key_node.value
                if key in seen_keys:
                    raise ValueError(f"{skill_md} frontmatter contains duplicate key {key!r}")
                seen_keys.add(key)
                ensure_unique_keys(value_node)
            return
        if isinstance(node, SequenceNode):
            for child in node.value:
                ensure_unique_keys(child)

    ensure_unique_keys(frontmatter_node)

    name = parsed_frontmatter.get("name")
    description = parsed_frontmatter.get("description")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"{skill_md} frontmatter must include nonblank name")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"{skill_md} frontmatter must include nonblank description")
    metadata = parsed_frontmatter.get("metadata")
    if _projected_skill_requires_metadata(skill_root) and not isinstance(metadata, dict):
        raise ValueError(f"{skill_md} frontmatter metadata must be a mapping")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError(f"{skill_md} frontmatter metadata must be a mapping when present")
    if isinstance(metadata, dict):
        def require_string(field_names: tuple[str, ...], *, allow_empty: bool = False) -> None:
            for field_name in field_names:
                if field_name not in metadata:
                    continue
                value = metadata.get(field_name)
                if not isinstance(value, str) or (not allow_empty and not value.strip()):
                    raise ValueError(
                        f"{skill_md} frontmatter metadata {field_name} must be a "
                        f"{'string' if allow_empty else 'nonblank string'}"
                    )

        require_string(
            (
                "source_category",
                "upstream_name",
                "upstream_version",
                "adaptation_overlay",
                "projection_plugin",
                "source-id",
                "source_path",
                "source-path",
                "provenance-name",
                "provenance_name",
                "origin",
                "content_mode",
                "source_author",
                "source_license",
                "source_repo",
                "adapted_author",
            )
        )
        if metadata.get("source_category") and metadata["source_category"] not in {"first_party", "third_party"}:
            raise ValueError(f"{skill_md} frontmatter metadata source_category must be first_party or third_party")
        if metadata.get("content_mode") and metadata["content_mode"] not in {"verbatim", "normalised", "adapted"}:
            raise ValueError(f"{skill_md} frontmatter metadata content_mode must be verbatim, normalised, or adapted")
        if metadata.get("source_category") == "third_party":
            for field_name in ("upstream_name", "upstream_version", "adaptation_overlay", "projection_plugin"):
                require_string((field_name,))
        if metadata.get("content_mode") == "adapted":
            require_string(("adapted_author",))
            if "source_author" not in metadata or "source_license" not in metadata:
                raise ValueError(
                    f"{skill_md} frontmatter metadata adapted projections must declare source_author and source_license"
                )
            require_string(("source_author", "source_license"))
        elif metadata.get("content_mode") == "normalised":
            if metadata.get("adapted_author") or metadata.get("adaptation_note"):
                raise ValueError(
                    f"{skill_md} frontmatter metadata normalised projections must not declare adapted_author or adaptation_note"
                )


@dataclass(frozen=True)
class SkillTarget:
    pack: str
    skill: str
    plugin_root: Path
    skill_root: Path
    export_mode: str = "direct"
    overlay_root: Path | None = None
    exclusion_reason: str | None = None

    @property
    def source_path(self) -> str:
        return _relative_path(self.skill_root, ROOT)

    @property
    def overlay_path(self) -> str | None:
        if self.overlay_root is None:
            return None
        return _relative_path(self.overlay_root, ROOT)

    @property
    def zip_path(self) -> Path:
        return GENERATED_SKILL_ZIPS_ROOT / self.pack / self.skill / "skill.zip"


@dataclass(frozen=True)
class SkillArtifact:
    pack: str
    skill: str
    export_mode: str
    source_path: str
    overlay_path: str | None
    zip_path: str
    source_file_count: int
    source_bytes: int
    source_sha256: str
    overlay_file_count: int
    overlay_bytes: int
    overlay_sha256: str | None
    zip_size_bytes: int
    zip_sha256: str


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(_as_windows_long_path(path)).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_text_file(path: Path, raw: bytes | None = None) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES or (
        raw is not None and raw.startswith(b"#!")
    )


def _canonicalize_text_bytes(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _read_canonical_file_bytes(path: Path) -> bytes:
    raw = Path(_as_windows_long_path(path)).read_bytes()
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


def load_marketplace_definition() -> dict[str, Any]:
    codex_manifest = load_json(CODEX_MARKETPLACE_MANIFEST_PATH)
    marketplace_manifest = load_json(MARKETPLACE_PATH)
    if codex_manifest != marketplace_manifest:
        raise ValueError("codex-marketplace/manifest.json does not match .agents/plugins/marketplace.json")
    return codex_manifest


def discover_skill_targets() -> list[SkillTarget]:
    # Validate the active marketplace manifests first, but discover zip targets
    # from the enabled plugin-root inventory so retained first-party roots such as
    # house-skills can still generate installable zips even when marketplace
    # exposure policy excludes them from direct plugin publication.
    load_marketplace_definition()
    targets: list[SkillTarget] = []
    for plugin in load_plugin_root_inventory():
        if not plugin["enabled"]:
            continue
        plugin_name = plugin["name"]
        plugin_root = (ROOT / plugin["plugin_root"]).resolve()
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
            if plugin_name == "superpowers-plus":
                validate_skill_markdown_frontmatter(skill_dir)
            targets.append(
                SkillTarget(
                    pack=plugin_name,
                    skill=skill_dir.name,
                    plugin_root=plugin_root,
                    skill_root=skill_dir,
                )
            )

    return sorted(targets, key=lambda item: (item.pack, item.skill))


def discover_skill_export_targets() -> list[SkillTarget]:
    targets = discover_skill_targets()
    export_targets: list[SkillTarget] = []
    for target in targets:
        policy = resolve_gpt_export_policy(pack=target.pack, skill=target.skill)
        if policy.export_mode == "excluded":
            export_targets.append(
                SkillTarget(
                    pack=target.pack,
                    skill=target.skill,
                    plugin_root=target.plugin_root,
                    skill_root=target.skill_root,
                    export_mode=policy.export_mode,
                    overlay_root=policy.overlay_root,
                    exclusion_reason=policy.reason,
                )
            )
            continue
        export_targets.append(
            SkillTarget(
                pack=target.pack,
                skill=target.skill,
                plugin_root=target.plugin_root,
                skill_root=target.skill_root,
                export_mode=policy.export_mode,
                overlay_root=policy.overlay_root,
                exclusion_reason=policy.reason,
            )
        )
    return export_targets


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
    skill_root_str = _as_windows_long_path(skill_root)

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


def compute_source_fingerprint(skill_root: Path) -> tuple[str, int, int, list[Path], list[str]]:
    packaged_files, forbidden_paths = scan_skill_tree(skill_root)
    skill_root_str = _as_windows_long_path(skill_root.resolve())
    digest = hashlib.sha256()
    total_bytes = 0
    for path in packaged_files:
        rel = str(path)[len(skill_root_str) + 1 :].replace("\\", "/")
        raw = _read_canonical_file_bytes(path)
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


def _materialize_export_tree(target: SkillTarget) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    return stage_skill_tree(target.skill_root, target.overlay_root)


def _build_artifact(
    target: SkillTarget,
    *,
    source_sha256: str,
    source_file_count: int,
    source_bytes: int,
    overlay_sha256: str | None,
    overlay_file_count: int,
    overlay_bytes: int,
    zip_path: Path,
) -> SkillArtifact:
    return SkillArtifact(
        pack=target.pack,
        skill=target.skill,
        export_mode=target.export_mode,
        source_path=target.source_path,
        overlay_path=target.overlay_path,
        zip_path=_relative_path(zip_path, ROOT),
        source_file_count=source_file_count,
        source_bytes=source_bytes,
        source_sha256=source_sha256,
        overlay_file_count=overlay_file_count,
        overlay_bytes=overlay_bytes,
        overlay_sha256=overlay_sha256,
        zip_size_bytes=zip_path.stat().st_size,
        zip_sha256=sha256_file(zip_path),
    )


def package_skill_target(target: SkillTarget) -> SkillArtifact:
    if target.skill_root.name != target.skill:
        raise ValueError(f"{target.pack}/{target.skill} source folder mismatch: {target.skill_root.name}")
    if target.export_mode == "excluded":
        raise ValueError(f"{target.pack}/{target.skill} is excluded from GPT exports")

    source_sha256, source_file_count, source_bytes, _, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{target.pack}/{target.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")

    overlay_sha256 = None
    overlay_file_count = 0
    overlay_bytes = 0
    if target.overlay_root is not None:
        overlay_sha256, overlay_file_count, overlay_bytes, _, overlay_forbidden_paths = compute_source_fingerprint(
            target.overlay_root
        )
        if overlay_forbidden_paths:
            raise ValueError(
                f"{target.pack}/{target.skill} overlay contains forbidden source paths: "
                f"{', '.join(overlay_forbidden_paths)}"
            )

    staged_root, tempdir = _materialize_export_tree(target)
    try:
        _, _, _, staged_files, staged_forbidden_paths = compute_source_fingerprint(staged_root)
        if staged_forbidden_paths:
            raise ValueError(
                f"{target.pack}/{target.skill} staged export contains forbidden source paths: "
                f"{', '.join(staged_forbidden_paths)}"
            )

        dest = _create_zip_path(target)
        if dest.exists():
            dest.unlink()
        dest.parent.mkdir(parents=True, exist_ok=True)

        tmp_path = dest.parent / f"{target.skill}-{os.getpid()}-{uuid.uuid4().hex}.tmp"
        tmp_path_text = _as_windows_long_path(tmp_path)
        dest_text = _as_windows_long_path(dest)
        try:
            with Path(tmp_path_text).open("wb") as handle:
                with zipfile.ZipFile(handle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    _write_canonical_zip_tree(archive, staged_files, root=staged_root, archive_root_name=target.skill)
            os.replace(tmp_path_text, dest_text)
        except Exception:
            if Path(tmp_path_text).exists():
                Path(tmp_path_text).unlink(missing_ok=True)
            raise
    finally:
        tempdir.cleanup()

    return _build_artifact(
        target,
        source_sha256=source_sha256,
        source_file_count=source_file_count,
        source_bytes=source_bytes,
        overlay_sha256=overlay_sha256,
        overlay_file_count=overlay_file_count,
        overlay_bytes=overlay_bytes,
        zip_path=dest,
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
    if artifact.export_mode != target.export_mode:
        raise ValueError(f"{artifact.pack}/{artifact.skill} export mode mismatch")
    if artifact.overlay_path != target.overlay_path:
        raise ValueError(f"{artifact.pack}/{artifact.skill} overlay path mismatch")

    errors, root = inspect_skill_zip(target.skill, zip_path)
    if errors:
        raise ValueError(f"{artifact.pack}/{artifact.skill} archive invalid: {'; '.join(errors)}")
    if root != target.skill:
        raise ValueError(f"{artifact.pack}/{artifact.skill} archive root mismatch")

    source_sha256, source_file_count, source_bytes, _, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{artifact.pack}/{artifact.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")
    if source_sha256 != artifact.source_sha256:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source fingerprint mismatch")
    if source_file_count != artifact.source_file_count:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source file count mismatch")
    if source_bytes != artifact.source_bytes:
        raise ValueError(f"{artifact.pack}/{artifact.skill} source byte count mismatch")

    overlay_sha256 = None
    overlay_file_count = 0
    overlay_bytes = 0
    if target.overlay_root is not None:
        overlay_sha256, overlay_file_count, overlay_bytes, _, overlay_forbidden_paths = compute_source_fingerprint(
            target.overlay_root
        )
        if overlay_forbidden_paths:
            raise ValueError(
                f"{artifact.pack}/{artifact.skill} overlay contains forbidden source paths: "
                f"{', '.join(overlay_forbidden_paths)}"
            )
    if overlay_sha256 != artifact.overlay_sha256:
        raise ValueError(f"{artifact.pack}/{artifact.skill} overlay fingerprint mismatch")
    if overlay_file_count != artifact.overlay_file_count:
        raise ValueError(f"{artifact.pack}/{artifact.skill} overlay file count mismatch")
    if overlay_bytes != artifact.overlay_bytes:
        raise ValueError(f"{artifact.pack}/{artifact.skill} overlay byte count mismatch")

    staged_root, tempdir = _materialize_export_tree(target)
    try:
        with zipfile.ZipFile(zip_path) as archive:
            extracted_names = sorted(name for name in archive.namelist() if name and not name.endswith("/"))
            staged_files, staged_forbidden_paths = scan_skill_tree(staged_root)
            if staged_forbidden_paths:
                raise ValueError(
                    f"{artifact.pack}/{artifact.skill} staged export contains forbidden source paths: "
                    f"{', '.join(staged_forbidden_paths)}"
                )
            expected_names = [f"{target.skill}/{_relative_path(path, staged_root)}" for path in staged_files]
            if extracted_names != expected_names:
                raise ValueError(f"{artifact.pack}/{artifact.skill} archive file inventory mismatch")
            for name in extracted_names:
                staged_file = staged_root / Path(name).relative_to(target.skill)
                if archive.read(name) != _read_canonical_file_bytes(staged_file):
                    raise ValueError(f"{artifact.pack}/{artifact.skill} archive content drift at {name}")
    finally:
        tempdir.cleanup()

    if sha256_file(zip_path) != artifact.zip_sha256:
        raise ValueError(f"{artifact.pack}/{artifact.skill} zip sha256 mismatch")
    if zip_path.stat().st_size != artifact.zip_size_bytes:
        raise ValueError(f"{artifact.pack}/{artifact.skill} zip size mismatch")


def artifact_to_record(artifact: SkillArtifact) -> dict[str, Any]:
    return {
        "pack": artifact.pack,
        "skill": artifact.skill,
        "export_mode": artifact.export_mode,
        "source_path": artifact.source_path,
        "overlay_path": artifact.overlay_path,
        "zip_path": artifact.zip_path,
        "source_file_count": artifact.source_file_count,
        "source_bytes": artifact.source_bytes,
        "source_sha256": artifact.source_sha256,
        "overlay_file_count": artifact.overlay_file_count,
        "overlay_bytes": artifact.overlay_bytes,
        "overlay_sha256": artifact.overlay_sha256,
        "zip_size_bytes": artifact.zip_size_bytes,
        "zip_sha256": artifact.zip_sha256,
    }


def record_to_artifact(record: dict[str, Any]) -> SkillArtifact:
    return SkillArtifact(
        pack=str(record["pack"]),
        skill=str(record["skill"]),
        export_mode=str(record.get("export_mode", "direct")),
        source_path=str(record["source_path"]),
        overlay_path=(str(record["overlay_path"]) if record.get("overlay_path") else None),
        zip_path=str(record["zip_path"]),
        source_file_count=int(record["source_file_count"]),
        source_bytes=int(record["source_bytes"]),
        source_sha256=str(record["source_sha256"]),
        overlay_file_count=int(record.get("overlay_file_count", 0)),
        overlay_bytes=int(record.get("overlay_bytes", 0)),
        overlay_sha256=(str(record["overlay_sha256"]) if record.get("overlay_sha256") else None),
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
    files.sort(key=lambda path: _relative_path(path, ROOT))
    return files


def validate_generated_surface(expected_records: list[SkillArtifact]) -> None:
    expected_zip_paths = {
        _relative_path((ROOT / record.zip_path).resolve(), ROOT)
        for record in expected_records
    }
    unexpected_files: list[str] = []
    actual_zip_paths: set[str] = set()
    for path in _discover_generated_surface_files():
        rel = _relative_path(path, ROOT)
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


def cleanup_generated_surface(expected_records: list[SkillArtifact]) -> None:
    expected_zip_paths = {
        _relative_path((ROOT / record.zip_path).resolve(), ROOT)
        for record in expected_records
    }
    for path in _discover_generated_surface_files():
        rel = _relative_path(path, ROOT)
        if path.resolve() == GENERATED_SKILL_ZIPS_REGISTRY_PATH.resolve():
            continue
        if path.name != "skill.zip":
            continue
        if rel not in expected_zip_paths:
            path.unlink()

    if GENERATED_SKILL_ZIPS_ROOT.exists():
        for candidate in sorted(GENERATED_SKILL_ZIPS_ROOT.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            if not candidate.is_dir():
                continue
            if candidate.resolve() == GENERATED_SKILL_ZIPS_ROOT.resolve():
                continue
            try:
                next(candidate.iterdir())
            except StopIteration:
                candidate.rmdir()


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
        return build_registry([])
    return load_json(GENERATED_SKILL_ZIPS_REGISTRY_PATH)


def _registry_artifact_indexes(registry: dict[str, Any]) -> dict[tuple[str, str], SkillArtifact]:
    return {
        (artifact.pack, artifact.skill): artifact
        for artifact in (record_to_artifact(record) for record in registry.get("artifacts", []))
    }


def _registry_exclusion_indexes(registry: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    exclusions: dict[tuple[str, str], dict[str, Any]] = {}
    for record in registry.get("excluded", []):
        if not isinstance(record, dict):
            raise ValueError("generated/skill-zips registry contains a malformed exclusion entry")
        pack = str(record.get("pack"))
        skill = str(record.get("skill"))
        exclusions[(pack, skill)] = record
    return exclusions


def _artifact_from_registry_record(target: SkillTarget, record: dict[str, Any]) -> SkillArtifact:
    artifact = record_to_artifact(record)
    if artifact.pack != target.pack or artifact.skill != target.skill:
        raise ValueError(f"{target.pack}/{target.skill} registry entry mismatch")
    return artifact


def _exclusion_record(target: SkillTarget) -> dict[str, Any]:
    source_sha256, source_file_count, source_bytes, _, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{target.pack}/{target.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")
    return {
        "pack": target.pack,
        "skill": target.skill,
        "export_mode": "excluded",
        "source_path": target.source_path,
        "overlay_path": target.overlay_path,
        "source_file_count": source_file_count,
        "source_bytes": source_bytes,
        "source_sha256": source_sha256,
        "reason": target.exclusion_reason,
    }


def _validate_existing_artifact(target: SkillTarget, artifact: SkillArtifact, *, scope_label: str) -> SkillArtifact:
    zip_path = ROOT / artifact.zip_path
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    if zip_path.name != "skill.zip":
        raise ValueError(f"{target.pack}/{target.skill} archive filename mismatch")
    if artifact.zip_path != _relative_path(target.zip_path, ROOT):
        raise ValueError(
            f"{scope_label} artifact for {target.pack}/{target.skill} points at {artifact.zip_path} "
            f"instead of {_relative_path(target.zip_path, ROOT)}"
        )
    if artifact.export_mode != target.export_mode:
        raise ValueError(
            f"{scope_label} artifact for {target.pack}/{target.skill} export mode mismatch: "
            f"{artifact.export_mode} != {target.export_mode}"
        )
    if artifact.overlay_path != target.overlay_path:
        raise ValueError(
            f"{scope_label} artifact for {target.pack}/{target.skill} overlay path mismatch: "
            f"{artifact.overlay_path} != {target.overlay_path}"
        )

    errors, root = inspect_skill_zip(target.skill, zip_path)
    if errors:
        raise ValueError(f"{target.pack}/{target.skill} archive invalid: {'; '.join(errors)}")
    if root != target.skill:
        raise ValueError(f"{target.pack}/{target.skill} archive root mismatch")

    source_sha256, source_file_count, source_bytes, _, forbidden_paths = compute_source_fingerprint(target.skill_root)
    if forbidden_paths:
        raise ValueError(f"{target.pack}/{target.skill} contains forbidden source paths: {', '.join(forbidden_paths)}")

    if artifact.source_path != target.source_path:
        raise ValueError(
            f"existing generated artifact for {target.pack}/{target.skill} points at {artifact.source_path} "
            f"instead of {target.source_path}"
        )
    if source_sha256 != artifact.source_sha256:
        raise ValueError(
            f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
            f"generated/{artifact.zip_path} is stale relative to {target.source_path}; "
            f"include --skill {target.pack}/{target.skill}, run py -3 tools/update_skill_artifacts.py --all, "
            f"or fix stale generated artifact before continuing"
        )
    if source_file_count != artifact.source_file_count:
        raise ValueError(
            f"{scope_label} artifact for {target.pack}/{target.skill} has the wrong source file count; "
            f"check {target.source_path}"
        )
    if source_bytes != artifact.source_bytes:
        raise ValueError(
            f"{scope_label} artifact for {target.pack}/{target.skill} has the wrong source byte count; "
            f"check {target.source_path}"
        )

    if sha256_file(zip_path) != artifact.zip_sha256:
        raise ValueError(
            f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
            f"generated/{artifact.zip_path} checksum differs from registry state; "
            f"check {target.source_path}"
        )
    if zip_path.stat().st_size != artifact.zip_size_bytes:
        raise ValueError(
            f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
            f"generated/{artifact.zip_path} size differs from registry state; "
            f"check {target.source_path}"
        )

    staged_root, tempdir = _materialize_export_tree(target)
    try:
        with zipfile.ZipFile(zip_path) as archive:
            extracted_names = sorted(name for name in archive.namelist() if name and not name.endswith("/"))
            staged_files, staged_forbidden_paths = scan_skill_tree(staged_root)
            if staged_forbidden_paths:
                raise ValueError(
                    f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
                    f"generated/{artifact.zip_path} staged export contains forbidden source paths: "
                    f"{', '.join(staged_forbidden_paths)}"
                )
            expected_names = [f"{target.skill}/{_relative_path(path, staged_root)}" for path in staged_files]
            if extracted_names != expected_names:
                raise ValueError(
                    f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
                    f"generated/{artifact.zip_path} content inventory differs from {target.source_path}"
                )
            for name in extracted_names:
                staged_file = staged_root / Path(name).relative_to(target.skill)
                if archive.read(name) != _read_canonical_file_bytes(staged_file):
                    raise ValueError(
                        f"{scope_label} artifact drift for {target.pack}/{target.skill}; "
                        f"generated/{artifact.zip_path} content differs from {target.source_path}"
                    )
    finally:
        tempdir.cleanup()

    return artifact


def synchronize_skill_zips(*, pack: str | None = None, skill: str | None = None, write: bool) -> dict[str, Any]:
    targets = discover_skill_export_targets()
    targets_by_key = {(target.pack, target.skill): target for target in targets}
    selected = _select_targets(targets, pack=pack, skill=skill)
    if pack is None and skill is None:
        selected = {key for key in selected if targets_by_key[key].export_mode != "excluded"}
    if not selected:
        if pack:
            raise ValueError(f"no installable skills found for pack {pack}")
        raise ValueError("no installable skills found in the active marketplace manifests")

    current_registry = load_registry()
    current_artifacts = _registry_artifact_indexes(current_registry)
    current_exclusions = _registry_exclusion_indexes(current_registry)

    artifacts: list[SkillArtifact] = []
    exclusions: list[dict[str, Any]] = []
    for target in targets:
        key = _target_key(target.pack, target.skill)
        current_artifact = current_artifacts.get(key)
        current_exclusion = current_exclusions.get(key)
        if current_exclusion is not None and current_exclusion.get("export_mode") != "excluded":
            raise ValueError(f"registry exclusion entry for {target.pack}/{target.skill} is malformed")
        if target.export_mode == "excluded":
            exclusion = _exclusion_record(target)
            if key in selected:
                raise ValueError(
                    f"{target.pack}/{target.skill} is excluded from GPT exports: {target.exclusion_reason}"
                )
            if write:
                exclusions.append(exclusion)
            else:
                if current_artifact is not None:
                    raise ValueError(
                        f"registry still contains an artifact for excluded skill {target.pack}/{target.skill}"
                    )
                if current_exclusion is None:
                    raise ValueError(
                        f"generated/skill-zips/registry.json is missing excluded skill {target.pack}/{target.skill}"
                    )
                if current_exclusion != exclusion:
                    raise ValueError(
                        f"generated/skill-zips/registry.json exclusion entry is stale for {target.pack}/{target.skill}"
                    )
                exclusions.append(current_exclusion)
            continue

        if key in selected:
            if write:
                artifact = package_skill_target(target)
            else:
                if current_artifact is None:
                    raise ValueError(
                        f"generated/skill-zips/registry.json is missing selected skill {target.pack}/{target.skill}"
                    )
                artifact = _validate_existing_artifact(target, current_artifact, scope_label="selected")
        else:
            if current_artifact is None:
                raise ValueError(
                    f"generated/skill-zips/registry.json is missing unselected skill {target.pack}/{target.skill}"
                )
            artifact = _validate_existing_artifact(target, current_artifact, scope_label="unselected")
        artifacts.append(artifact)

    registry = build_registry(artifacts, exclusions=exclusions)
    if write and pack is None and skill is None:
        cleanup_generated_surface(artifacts)
    validate_generated_surface(artifacts)
    if write:
        GENERATED_SKILL_ZIPS_ROOT.mkdir(parents=True, exist_ok=True)
        with GENERATED_SKILL_ZIPS_REGISTRY_PATH.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(registry, handle, indent=2)
            handle.write("\n")
    else:
        if current_registry != registry:
            raise ValueError("generated/skill-zips/registry.json is stale or inconsistent with on-disk artifacts")
    return registry


def validate_skill_zip_registry() -> dict[str, Any]:
    registry = load_registry()
    targets = discover_skill_export_targets()
    artifacts_by_key = _registry_artifact_indexes(registry)
    exclusions_by_key = _registry_exclusion_indexes(registry)
    artifacts = []
    exclusions: list[dict[str, Any]] = []
    for target in targets:
        key = (target.pack, target.skill)
        artifact = artifacts_by_key.get(key)
        exclusion = exclusions_by_key.get(key)
        if target.export_mode == "excluded":
            expected_exclusion = _exclusion_record(target)
            if exclusion is None:
                raise ValueError(
                    f"generated/skill-zips/registry.json is missing excluded skill {target.pack}/{target.skill}"
                )
            if exclusion != expected_exclusion:
                raise ValueError(
                    f"generated/skill-zips/registry.json exclusion entry is stale for {target.pack}/{target.skill}"
                )
            if artifact is not None:
                raise ValueError(f"excluded skill {target.pack}/{target.skill} still has a generated artifact")
            exclusions.append(exclusion)
            continue
        if artifact is None:
            raise ValueError(
                f"generated/skill-zips/registry.json is missing active skill {target.pack}/{target.skill}"
            )
        if exclusion is not None:
            raise ValueError(f"active skill {target.pack}/{target.skill} is incorrectly marked as excluded")
        artifacts.append(_validate_existing_artifact(target, artifact, scope_label="current"))
    validate_generated_surface(artifacts)
    expected = build_registry(artifacts, exclusions=exclusions)
    discovered_keys = {(target.pack, target.skill) for target in targets}
    registry_keys = {(artifact.pack, artifact.skill) for artifact in artifacts}
    registry_exclusion_keys = {(entry.get("pack"), entry.get("skill")) for entry in exclusions}
    covered_keys = registry_keys | registry_exclusion_keys
    missing_targets = sorted(discovered_keys - covered_keys)
    if missing_targets:
        formatted = ", ".join(f"{pack}/{skill}" for pack, skill in missing_targets)
        raise ValueError(
            "active installable skill roots are missing from generated/skill-zips without an explicit exclusion: "
            f"{formatted}"
        )
    missing_exclusions = sorted(
        (target.pack, target.skill)
        for target in targets
        if target.export_mode == "excluded" and (target.pack, target.skill) not in registry_exclusion_keys
    )
    if missing_exclusions:
        formatted = ", ".join(f"{pack}/{skill}" for pack, skill in missing_exclusions)
        raise ValueError(
            "excluded skill roots are missing from generated/skill-zips registry exclusions: " f"{formatted}"
        )
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
        f"registry_path={_relative_path(GENERATED_SKILL_ZIPS_REGISTRY_PATH, ROOT)}, "
        f"excluded={exclusion_summary}"
    )


def print_registry_receipt(registry: dict[str, Any]) -> None:
    artifact_count = registry.get("artifact_count", 0)
    exclusion_count = registry.get("excluded_count", 0)
    direct_count = sum(1 for artifact in registry.get("artifacts", []) if artifact.get("export_mode", "direct") == "direct")
    overlay_count = sum(1 for artifact in registry.get("artifacts", []) if artifact.get("export_mode") == "overlay")
    packs = sorted({artifact.get("pack") for artifact in registry.get("artifacts", []) if artifact.get("pack")})
    print(f"OK skill-zips registry: {_relative_path(GENERATED_SKILL_ZIPS_REGISTRY_PATH, ROOT)}")
    print(f"OK generated artifacts: {artifact_count}")
    print(f"OK direct exports: {direct_count}")
    print(f"OK overlay exports: {overlay_count}")
    print(f"OK included packs: {', '.join(packs)}")
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
