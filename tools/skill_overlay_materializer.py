#!/usr/bin/env python3
"""Deterministic tree materialization helpers for skill adaptation overlays."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


ROOT = Path(__file__).resolve().parents[1]
OVERLAY_FILENAME = "overlay.yaml"
OPENAI_AGENT_FILENAME = Path("agents/openai.yaml")
ALLOWED_OVERLAY_KEYS = {"schema_version", "deletes", "metadata"}
UTF8_BOM = b"\xef\xbb\xbf"
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".sh",
    ".svg",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".ts",
}
TEXT_FILENAMES = {"SKILL.md", "openai.yaml"}


def _ensure_unique_keys(node: MappingNode | SequenceNode, *, path: Path) -> None:
    if isinstance(node, MappingNode):
        seen_keys: set[str] = set()
        for key_node, value_node in node.value:
            if not isinstance(key_node, ScalarNode):
                raise ValueError(f"{path} keys must be simple scalars")
            key = key_node.value
            if key in seen_keys:
                raise ValueError(f"{path} contains duplicate key {key!r}")
            seen_keys.add(key)
            _ensure_unique_keys(value_node, path=path)
        return
    if isinstance(node, SequenceNode):
        for child in node.value:
            _ensure_unique_keys(child, path=path)


def _load_yaml_document(path: Path) -> Any:
    raw = path.read_bytes()
    if raw.startswith(UTF8_BOM):
        raise ValueError(f"{path} begins with a UTF-8 BOM")

    text = raw.decode("utf-8")
    parsed = yaml.safe_load(text)
    node = yaml.compose(text, Loader=yaml.SafeLoader)
    if node is not None:
        _ensure_unique_keys(node, path=path)
    return parsed


def _is_text_file(path: Path) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES


def _normalize_tree_text_files(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or not _is_text_file(path):
            continue
        raw = path.read_bytes()
        if raw.startswith(UTF8_BOM):
            raw = raw[len(UTF8_BOM) :]
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if normalized != raw:
            path.write_bytes(normalized)
        elif raw.startswith(UTF8_BOM):
            path.write_bytes(raw[len(UTF8_BOM) :])


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    parsed = _load_yaml_document(path)
    if not isinstance(parsed, dict):
        raise ValueError(f"{path} must parse to a mapping")
    return parsed


def _validate_delete_path(delete_path: Any, *, overlay_root: Path) -> str:
    if not isinstance(delete_path, str) or not delete_path.strip():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} delete entries must be nonblank strings")
    candidate = Path(delete_path)
    if candidate.is_absolute():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} delete path must be relative: {delete_path}")
    if any(part == ".." for part in candidate.parts):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} delete path must not traverse upward: {delete_path}")
    if any(char in delete_path for char in "*?[]"):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} delete path must not use globs: {delete_path}")
    if candidate.parts and candidate.name == "":
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} delete path must resolve to a file or leaf path: {delete_path}")
    return candidate.as_posix()


def load_overlay_spec(overlay_root: Path) -> dict[str, Any]:
    overlay_yaml = overlay_root / OVERLAY_FILENAME
    if not overlay_yaml.exists():
        return {"deletes": [], "metadata": None}

    parsed = _load_yaml_mapping(overlay_yaml)
    unknown_keys = sorted(set(parsed) - ALLOWED_OVERLAY_KEYS)
    if unknown_keys:
        raise ValueError(f"{overlay_yaml} contains unsupported keys: {', '.join(unknown_keys)}")
    if parsed.get("schema_version") != 1:
        raise ValueError(f"{overlay_yaml} schema_version must be 1")

    deletes = parsed.get("deletes", [])
    if deletes is None:
        deletes = []
    if not isinstance(deletes, list):
        raise ValueError(f"{overlay_yaml} deletes must be a list")
    normalized_deletes = [_validate_delete_path(delete_path, overlay_root=overlay_root) for delete_path in deletes]

    metadata = parsed.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        raise ValueError(f"{overlay_yaml} metadata must be a mapping when present")

    return {
        "deletes": normalized_deletes,
        "metadata": metadata,
    }


def validate_openai_agent_yaml(agent_yaml_path: Path) -> None:
    if not agent_yaml_path.exists():
        raise FileNotFoundError(agent_yaml_path)
    parsed = _load_yaml_mapping(agent_yaml_path)
    if parsed.get("version") != 1:
        raise ValueError(f"{agent_yaml_path} version must be 1")
    metadata = parsed.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{agent_yaml_path} metadata must be a mapping")


def _apply_deletes(staged_root: Path, overlay_root: Path, deletes: list[str]) -> None:
    for delete_path in deletes:
        candidate = staged_root / delete_path
        if not candidate.exists():
            raise FileNotFoundError(f"{overlay_root / OVERLAY_FILENAME} delete target does not exist: {delete_path}")
        if candidate.is_dir():
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} cannot delete directories: {delete_path}")
        candidate.unlink()


def _apply_overlay_files(staged_root: Path, overlay_root: Path) -> None:
    for overlay_file in sorted(path for path in overlay_root.rglob("*") if path.is_file()):
        rel = overlay_file.relative_to(overlay_root)
        if rel == Path(OVERLAY_FILENAME):
            continue
        dest = staged_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(overlay_file, dest)


def _materialize_into(source_root: Path, overlay_root: Path | None, destination_root: Path) -> None:
    if not source_root.exists():
        raise FileNotFoundError(source_root)
    if not source_root.is_dir():
        raise NotADirectoryError(source_root)

    if destination_root.exists():
        shutil.rmtree(destination_root)
    destination_root.parent.mkdir(parents=True, exist_ok=True)

    tempdir = tempfile.TemporaryDirectory()
    staged_root = Path(tempdir.name) / source_root.name
    try:
        shutil.copytree(source_root, staged_root)
        if overlay_root is not None:
            if not overlay_root.exists():
                raise FileNotFoundError(overlay_root)
            if not overlay_root.is_dir():
                raise NotADirectoryError(overlay_root)
            spec = load_overlay_spec(overlay_root)
            openai_yaml = overlay_root / OPENAI_AGENT_FILENAME
            if openai_yaml.exists():
                validate_openai_agent_yaml(openai_yaml)
            _apply_deletes(staged_root, overlay_root, spec["deletes"])
            _apply_overlay_files(staged_root, overlay_root)
        _normalize_tree_text_files(staged_root)
        shutil.copytree(staged_root, destination_root)
    finally:
        tempdir.cleanup()


def apply_overlay_tree(source_root: Path, overlay_root: Path | None, destination_root: Path) -> None:
    _materialize_into(source_root, overlay_root, destination_root)


def stage_overlay_tree(source_root: Path, overlay_root: Path | None) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    tempdir: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
    staged_root = Path(tempdir.name) / source_root.name
    try:
        shutil.copytree(source_root, staged_root)
        if overlay_root is not None:
            if not overlay_root.exists():
                raise FileNotFoundError(overlay_root)
            if not overlay_root.is_dir():
                raise NotADirectoryError(overlay_root)
            spec = load_overlay_spec(overlay_root)
            openai_yaml = overlay_root / OPENAI_AGENT_FILENAME
            if openai_yaml.exists():
                validate_openai_agent_yaml(openai_yaml)
            _apply_deletes(staged_root, overlay_root, spec["deletes"])
            _apply_overlay_files(staged_root, overlay_root)
        _normalize_tree_text_files(staged_root)
    except Exception:
        tempdir.cleanup()
        raise
    return staged_root, tempdir
