#!/usr/bin/env python3
"""Skill projection helpers for staging source trees and managing plugin identity.

This module contains the no-overlay projection primitives shared by
`project_skills.py` and `validate_marketplace.py`. The historical
overlay/adaptation machinery (`overlay.yaml` line edits, deletes, generated
files) has been retired: the marketplace now uses first- and third-party
verbatim source custody only, so projection staging is a plain source-tree
copy plus optional shared-checkout companion injection.
"""

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
OPENAI_AGENT_FILENAME = Path("agents/openai.yaml")
SHARED_CHECKOUT_HELPER = ROOT / "tools" / "shared_checkout.py"
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


def stage_source_tree(source_root: Path) -> tuple[Path, tempfile.TemporaryDirectory[str]]:
    """Stage a verbatim copy of `source_root` in a temp dir for projection/validation.

    The overlay/adaptation layer has been retired, so projection staging is a
    plain source-tree copy plus the shared-checkout companion injection that
    projected skill scripts rely on.
    """
    if not source_root.exists():
        raise FileNotFoundError(source_root)
    if not source_root.is_dir():
        raise NotADirectoryError(source_root)
    tempdir: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
    staged_root = Path(tempdir.name) / source_root.name
    try:
        shutil.copytree(_as_windows_long_path(source_root), staged_root)
        _add_shared_checkout_companion(staged_root)
    except Exception:
        tempdir.cleanup()
        raise
    return staged_root, tempdir
