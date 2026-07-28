#!/usr/bin/env python3
"""Deterministic tree materialization helpers for skill adaptation overlays."""

from __future__ import annotations

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


ROOT = Path(__file__).resolve().parents[1]
OVERLAY_FILENAME = "overlay.yaml"
OPENAI_AGENT_FILENAME = Path("agents/openai.yaml")
ALLOWED_OVERLAY_KEYS = {"schema_version", "deletes", "metadata", "generated_files"}
SHARED_CHECKOUT_HELPER = ROOT / "tools" / "shared_checkout.py"
ALLOWED_LINE_EDIT_OPS = {"insert_before", "insert_after", "replace", "delete"}
UTF8_BOM = b"\xef\xbb\xbf"


def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _add_shared_checkout_companion(staged_root: Path) -> None:
    """Copy the canonical shared_checkout.py next to any skill script that needs it."""
    if not SHARED_CHECKOUT_HELPER.is_file():
        return
    for scripts_dir in staged_root.rglob("scripts"):
        if not scripts_dir.is_dir():
            continue
        target = scripts_dir / "shared_checkout.py"
        if target.exists():
            continue
        for script in scripts_dir.iterdir():
            if script.suffix == ".py" and script.name != "shared_checkout.py" and script.is_file():
                text = script.read_text(encoding="utf-8")
                needs = any(
                    re.match(r"^\s*import\s+shared_checkout\b", line)
                    or re.match(r"^\s*from\s+shared_checkout\b", line)
                    for line in text.splitlines()
                )
                if needs:
                    shutil.copy2(_as_windows_long_path(SHARED_CHECKOUT_HELPER), _as_windows_long_path(target))
                    break


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


def _validate_relative_file_path(file_path: Any, *, overlay_root: Path) -> str:
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit paths must be nonblank strings")
    candidate = Path(file_path)
    if candidate.is_absolute():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit path must be relative: {file_path}")
    if any(part == ".." for part in candidate.parts):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit path must not traverse upward: {file_path}")
    if any(char in file_path for char in "*?[]"):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit path must not use globs: {file_path}")
    if candidate.parts and candidate.name == "":
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit path must resolve to a file or leaf path: {file_path}")
    return candidate.as_posix()


def _validate_repo_relative_source_path(file_path: Any, *, overlay_root: Path) -> str:
    if not isinstance(file_path, str) or not file_path.strip():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source paths must be nonblank strings")
    candidate = Path(file_path)
    if candidate.is_absolute():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source path must be relative: {file_path}")
    if any(part == ".." for part in candidate.parts):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source path must not traverse upward: {file_path}")
    if any(char in file_path for char in "*?[]"):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source path must not use globs: {file_path}")
    resolved = ROOT / candidate
    if not resolved.exists():
        raise FileNotFoundError(f"{overlay_root / OVERLAY_FILENAME} generated source path does not exist: {file_path}")
    if not resolved.is_file():
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source path must resolve to a file: {file_path}")
    return candidate.as_posix()


def _validate_line_list(value: Any, *, overlay_root: Path, field_name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} {field_name} must be a non-empty list")
    normalized: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} {field_name} entries must be strings")
        normalized.append(item)
    return normalized


def _validate_generated_file(entry: Any, *, overlay_root: Path) -> dict[str, Any]:
    if not isinstance(entry, dict):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated_files entries must contain mappings")
    unknown_keys = sorted(set(entry) - {"source", "path"})
    if unknown_keys:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated_files entry contains unsupported keys: {', '.join(unknown_keys)}")
    source = _validate_repo_relative_source_path(entry.get("source"), overlay_root=overlay_root)
    path = _validate_relative_file_path(entry.get("path"), overlay_root=overlay_root)
    return {"source": source, "path": path}


def _validate_line_number(value: Any, *, overlay_root: Path, field_name: str) -> int:
    if not isinstance(value, int) or value < 1:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} {field_name} must be a positive integer")
    return value


def _validate_line_edit(edit: Any, *, overlay_root: Path) -> dict[str, Any]:
    if not isinstance(edit, dict):
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edits must contain mapping entries")

    unknown_keys = sorted(
        set(edit)
        - {
            "path",
            "op",
            "line",
            "start_line",
            "end_line",
            "anchor",
            "expected_lines",
            "insert_lines",
            "replace_lines",
        }
    )
    if unknown_keys:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit contains unsupported keys: {', '.join(unknown_keys)}")

    path = _validate_relative_file_path(edit.get("path"), overlay_root=overlay_root)
    op = edit.get("op")
    if op not in ALLOWED_LINE_EDIT_OPS:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit op must be one of: {', '.join(sorted(ALLOWED_LINE_EDIT_OPS))}")

    normalized: dict[str, Any] = {"path": path, "op": op}
    if op in {"insert_before", "insert_after"}:
        normalized["line"] = _validate_line_number(edit.get("line"), overlay_root=overlay_root, field_name="line")
        anchor = edit.get("anchor")
        if not isinstance(anchor, str) or not anchor.strip():
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} insert edits require a nonblank anchor")
        normalized["anchor"] = anchor
        normalized["insert_lines"] = _validate_line_list(
            edit.get("insert_lines"), overlay_root=overlay_root, field_name="insert_lines"
        )
        return normalized

    start_line = _validate_line_number(edit.get("start_line"), overlay_root=overlay_root, field_name="start_line")
    end_line = _validate_line_number(edit.get("end_line"), overlay_root=overlay_root, field_name="end_line")
    if end_line < start_line:
        raise ValueError(f"{overlay_root / OVERLAY_FILENAME} edit end_line must be greater than or equal to start_line")
    normalized["start_line"] = start_line
    normalized["end_line"] = end_line
    normalized["expected_lines"] = _validate_line_list(
        edit.get("expected_lines"), overlay_root=overlay_root, field_name="expected_lines"
    )
    if len(normalized["expected_lines"]) != end_line - start_line + 1:
        raise ValueError(
            f"{overlay_root / OVERLAY_FILENAME} expected_lines length must match the declared line range"
        )
    if op == "replace":
        normalized["replace_lines"] = _validate_line_list(
            edit.get("replace_lines"), overlay_root=overlay_root, field_name="replace_lines"
        )
    return normalized


def load_overlay_spec(overlay_root: Path) -> dict[str, Any]:
    overlay_yaml = overlay_root / OVERLAY_FILENAME
    if not overlay_yaml.exists():
        return {"schema_version": 1, "deletes": [], "metadata": None, "generated_files": []}

    parsed = _load_yaml_mapping(overlay_yaml)
    schema_version = parsed.get("schema_version")
    if schema_version == 1:
        unknown_keys = sorted(set(parsed) - ALLOWED_OVERLAY_KEYS)
        if unknown_keys:
            raise ValueError(f"{overlay_yaml} contains unsupported keys: {', '.join(unknown_keys)}")

        deletes = parsed.get("deletes", [])
        if deletes is None:
            deletes = []
        if not isinstance(deletes, list):
            raise ValueError(f"{overlay_yaml} deletes must be a list")
        normalized_deletes = [_validate_delete_path(delete_path, overlay_root=overlay_root) for delete_path in deletes]
        generated_files = parsed.get("generated_files", [])
        if generated_files is None:
            generated_files = []
        if not isinstance(generated_files, list):
            raise ValueError(f"{overlay_yaml} generated_files must be a list")
        normalized_generated_files = [
            _validate_generated_file(generated_file, overlay_root=overlay_root) for generated_file in generated_files
        ]

        metadata = parsed.get("metadata")
        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError(f"{overlay_yaml} metadata must be a mapping when present")

        return {
            "schema_version": 1,
            "deletes": normalized_deletes,
            "metadata": metadata,
            "generated_files": normalized_generated_files,
        }

    if schema_version == 2:
        unknown_keys = sorted(set(parsed) - {"schema_version", "edits", "metadata", "generated_files"})
        if unknown_keys:
            raise ValueError(f"{overlay_yaml} contains unsupported keys: {', '.join(unknown_keys)}")
        edits = parsed.get("edits")
        if not isinstance(edits, list) or not edits:
            raise ValueError(f"{overlay_yaml} edits must be a non-empty list")
        normalized_edits = [_validate_line_edit(edit, overlay_root=overlay_root) for edit in edits]
        generated_files = parsed.get("generated_files", [])
        if generated_files is None:
            generated_files = []
        if not isinstance(generated_files, list):
            raise ValueError(f"{overlay_yaml} generated_files must be a list")
        normalized_generated_files = [
            _validate_generated_file(generated_file, overlay_root=overlay_root) for generated_file in generated_files
        ]
        metadata = parsed.get("metadata")
        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError(f"{overlay_yaml} metadata must be a mapping when present")
        return {
            "schema_version": 2,
            "edits": normalized_edits,
            "metadata": metadata,
            "generated_files": normalized_generated_files,
        }

    raise ValueError(f"{overlay_yaml} schema_version must be 1 or 2")


def _apply_line_edits(staged_root: Path, overlay_root: Path, edits: list[dict[str, Any]]) -> None:
    edits_by_path: dict[str, list[dict[str, Any]]] = {}
    for edit in edits:
        edits_by_path.setdefault(edit["path"], []).append(edit)

    for rel_path, file_edits in edits_by_path.items():
        target = staged_root / rel_path
        if not target.exists():
            raise FileNotFoundError(f"{overlay_root / OVERLAY_FILENAME} edit target does not exist: {rel_path}")
        if target.is_dir():
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} cannot edit directories: {rel_path}")

        original_lines = target.read_text(encoding="utf-8").splitlines()
        current_lines = original_lines[:]
        ordered_edits = sorted(
            file_edits,
            key=lambda edit: (
                -(edit.get("line") or edit.get("start_line") or 0),
                0 if edit["op"] == "replace" else 1 if edit["op"] == "delete" else 2 if edit["op"] == "insert_after" else 3,
            ),
        )

        for edit in ordered_edits:
            op = edit["op"]
            if op in {"insert_before", "insert_after"}:
                line = edit["line"]
                if line > len(original_lines):
                    raise ValueError(
                        f"{overlay_root / OVERLAY_FILENAME} insert edit line out of range for {rel_path}: {line}"
                    )
                anchor = edit["anchor"]
                if original_lines[line - 1] != anchor:
                    raise ValueError(
                        f"{overlay_root / OVERLAY_FILENAME} insert edit anchor mismatch for {rel_path} line {line}"
                    )
                insert_at = line - 1 if op == "insert_before" else line
                current_lines[insert_at:insert_at] = edit["insert_lines"]
                continue

            start_line = edit["start_line"]
            end_line = edit["end_line"]
            if end_line > len(original_lines):
                raise ValueError(
                    f"{overlay_root / OVERLAY_FILENAME} edit range out of range for {rel_path}: {start_line}-{end_line}"
                )
            original_slice = original_lines[start_line - 1 : end_line]
            if original_slice != edit["expected_lines"]:
                raise ValueError(
                    f"{overlay_root / OVERLAY_FILENAME} edit expected lines mismatch for {rel_path} {start_line}-{end_line}"
                )
            current_slice = current_lines[start_line - 1 : end_line]
            if current_slice != edit["expected_lines"]:
                raise ValueError(
                    f"{overlay_root / OVERLAY_FILENAME} edit target drifted for {rel_path} {start_line}-{end_line}"
                )
            if op == "delete":
                del current_lines[start_line - 1 : end_line]
            else:
                current_lines[start_line - 1 : end_line] = edit["replace_lines"]

        with target.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(current_lines) + ("\n" if current_lines else ""))


def _apply_generated_files(staged_root: Path, overlay_root: Path, generated_files: list[dict[str, Any]]) -> None:
    for generated_file in generated_files:
        source = ROOT / generated_file["source"]
        rel_path = generated_file["path"]
        target = staged_root / rel_path
        if not source.exists():
            raise FileNotFoundError(f"{overlay_root / OVERLAY_FILENAME} generated source missing: {generated_file['source']}")
        if source.is_dir():
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated source must be a file: {generated_file['source']}")
        if target.exists() and target.is_dir():
            raise ValueError(f"{overlay_root / OVERLAY_FILENAME} generated target cannot be a directory: {rel_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


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


def _strip_plugin_identity(staged_root: Path) -> None:
    """Remove metadata.plugin and metadata.projection_plugin from staged agent YAML.

    Zips are plugin-neutral export artifacts; plugin identity is injected only
    into per-plugin projected trees and installed skill mirrors.
    """
    openai_yaml = staged_root / OPENAI_AGENT_FILENAME
    if not openai_yaml.is_file():
        return
    parsed = _load_yaml_mapping(openai_yaml)
    metadata = parsed.get("metadata")
    if isinstance(metadata, dict):
        metadata.pop("plugin", None)
        metadata.pop("projection_plugin", None)
        if not metadata:
            parsed.pop("metadata", None)
    rendered = yaml.safe_dump(
        parsed,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
        default_flow_style=False,
    ).rstrip() + "\n"
    openai_yaml.write_text(rendered, encoding="utf-8", newline="\n")


def _inject_plugin_identity(staged_root: Path, plugin_name: str) -> None:
    """Set metadata.plugin and metadata.projection_plugin in the projected agent YAML."""
    openai_yaml = staged_root / OPENAI_AGENT_FILENAME
    if not openai_yaml.is_file():
        return
    parsed = _load_yaml_mapping(openai_yaml)
    metadata = parsed.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        parsed["metadata"] = metadata
    metadata["plugin"] = plugin_name
    metadata["projection_plugin"] = plugin_name
    rendered = yaml.safe_dump(
        parsed,
        sort_keys=False,
        allow_unicode=True,
        width=4096,
        default_flow_style=False,
    ).rstrip() + "\n"
    openai_yaml.write_text(rendered, encoding="utf-8", newline="\n")


def _materialize_into(source_root: Path, overlay_root: Path | None, destination_root: Path) -> None:
    if not source_root.exists():
        raise FileNotFoundError(source_root)
    if not source_root.is_dir():
        raise NotADirectoryError(source_root)

    if destination_root.exists():
        shutil.rmtree(_as_windows_long_path(destination_root))
    destination_root.parent.mkdir(parents=True, exist_ok=True)

    tempdir = tempfile.TemporaryDirectory()
    staged_root = Path(tempdir.name) / source_root.name
    try:
        shutil.copytree(_as_windows_long_path(source_root), staged_root)
        if overlay_root is not None:
            if not overlay_root.exists():
                raise FileNotFoundError(overlay_root)
            if not overlay_root.is_dir():
                raise NotADirectoryError(overlay_root)
            spec = load_overlay_spec(overlay_root)
            openai_yaml = overlay_root / OPENAI_AGENT_FILENAME
            if openai_yaml.exists():
                validate_openai_agent_yaml(openai_yaml)
            _apply_overlay_files(staged_root, overlay_root)
            if spec["schema_version"] == 1:
                _apply_deletes(staged_root, overlay_root, spec["deletes"])
            else:
                _apply_line_edits(staged_root, overlay_root, spec["edits"])
            _apply_generated_files(staged_root, overlay_root, spec.get("generated_files", []))
        _add_shared_checkout_companion(staged_root)
        shutil.copytree(staged_root, _as_windows_long_path(destination_root))
    finally:
        tempdir.cleanup()


def apply_overlay_tree(source_root: Path, overlay_root: Path | None, destination_root: Path) -> None:
    _materialize_into(source_root, overlay_root, destination_root)


def stage_overlay_tree(source_root: Path, overlay_root: Path | None) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    tempdir: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
    staged_root = Path(tempdir.name) / source_root.name
    try:
        shutil.copytree(_as_windows_long_path(source_root), staged_root)
        if overlay_root is not None:
            if not overlay_root.exists():
                raise FileNotFoundError(overlay_root)
            if not overlay_root.is_dir():
                raise NotADirectoryError(overlay_root)
            spec = load_overlay_spec(overlay_root)
            openai_yaml = overlay_root / OPENAI_AGENT_FILENAME
            if openai_yaml.exists():
                validate_openai_agent_yaml(openai_yaml)
            _apply_overlay_files(staged_root, overlay_root)
            if spec["schema_version"] == 1:
                _apply_deletes(staged_root, overlay_root, spec["deletes"])
            else:
                _apply_line_edits(staged_root, overlay_root, spec["edits"])
            _apply_generated_files(staged_root, overlay_root, spec.get("generated_files", []))
        _add_shared_checkout_companion(staged_root)
    except Exception:
        tempdir.cleanup()
        raise
    return staged_root, tempdir
