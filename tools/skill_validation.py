#!/usr/bin/env python3
"""Canonical skill frontmatter validation helpers."""

from __future__ import annotations

import os
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


ROOT = Path(__file__).resolve().parents[1]
PROJECTED_SKILL_METADATA_REQUIRED_NAMES = {"using-superpowers"}


def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


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
