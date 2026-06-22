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

    def _require_nonblank_string(field_name: str) -> None:
        value = metadata.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{agent_yaml_path} metadata {field_name} must be a nonblank string")

    for field_name in (
        "skill_name",
        "plugin",
        "source_category",
        "upstream_name",
        "upstream_version",
        "adaptation_overlay",
        "projection_plugin",
        "source-id",
        "source-path",
        "provenance-name",
        "origin",
        "content_mode",
        "source_author",
        "source_license",
        "source_repo",
        "adapted_author",
    ):
        if field_name in metadata:
            _require_nonblank_string(field_name)

    if metadata.get("source_category") and metadata["source_category"] not in {"first_party", "third_party"}:
        raise ValueError(f"{agent_yaml_path} metadata source_category must be first_party or third_party")
    if metadata.get("content_mode") and metadata["content_mode"] not in {"verbatim", "normalised", "adapted"}:
        raise ValueError(f"{agent_yaml_path} metadata content_mode must be verbatim, normalised, or adapted")

    if metadata.get("source_category") == "third_party":
        for field_name in ("upstream_version", "adaptation_overlay"):
            _require_nonblank_string(field_name)

    if metadata.get("content_mode") == "adapted":
        _require_nonblank_string("adapted_author")

    interface = parsed.get("interface")
    if interface is not None:
        if not isinstance(interface, dict):
            raise ValueError(f"{agent_yaml_path} interface must be a mapping when present")
        for field_name in ("display_name", "short_description"):
            value = interface.get(field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{agent_yaml_path} interface {field_name} must be a nonblank string")
        for field_name in ("default_prompt", "icon_small", "icon_large", "brand_color"):
            value = interface.get(field_name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{agent_yaml_path} interface {field_name} must be a nonblank string when present")

    policy = parsed.get("policy")
    if policy is not None:
        if not isinstance(policy, dict):
            raise ValueError(f"{agent_yaml_path} policy must be a mapping when present")
        allow_implicit_invocation = policy.get("allow_implicit_invocation")
        if allow_implicit_invocation is not None and not isinstance(allow_implicit_invocation, bool):
            raise ValueError(
                f"{agent_yaml_path} policy allow_implicit_invocation must be a boolean when present"
            )
        products = policy.get("products")
        if products is not None:
            if not isinstance(products, list) or not products:
                raise ValueError(f"{agent_yaml_path} policy products must be a non-empty list when present")
            for product in products:
                if not isinstance(product, str) or not product.strip():
                    raise ValueError(f"{agent_yaml_path} policy products must contain nonblank strings")

    dependencies = parsed.get("dependencies")
    if dependencies is not None:
        if not isinstance(dependencies, dict):
            raise ValueError(f"{agent_yaml_path} dependencies must be a mapping when present")
        tools = dependencies.get("tools")
        if tools is not None:
            if not isinstance(tools, list) or not tools:
                raise ValueError(f"{agent_yaml_path} dependencies.tools must be a non-empty list when present")
            for tool in tools:
                if not isinstance(tool, dict):
                    raise ValueError(f"{agent_yaml_path} dependencies.tools entries must be mappings")
                for field_name in ("type", "value"):
                    value = tool.get(field_name)
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(
                            f"{agent_yaml_path} dependencies.tools entries must include nonblank {field_name}"
                        )
                description = tool.get("description")
                if description is not None and (not isinstance(description, str) or not description.strip()):
                    raise ValueError(
                        f"{agent_yaml_path} dependencies.tools description must be a nonblank string when present"
                    )
                transport = tool.get("transport")
                if transport is not None and (not isinstance(transport, str) or not transport.strip()):
                    raise ValueError(
                        f"{agent_yaml_path} dependencies.tools transport must be a nonblank string when present"
                    )
                url = tool.get("url")
                if url is not None and (not isinstance(url, str) or not url.strip()):
                    raise ValueError(f"{agent_yaml_path} dependencies.tools url must be a nonblank string when present")


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
    except Exception:
        tempdir.cleanup()
        raise
    return staged_root, tempdir
