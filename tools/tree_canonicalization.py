#!/usr/bin/env python3
"""Shared tree canonicalization helpers for projection and validation tools."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

TEXT_FILENAMES = {"SKILL.md", "openai.yaml", "AGENTS.md", "README.md", "LICENSE", "SOURCE.md", "PROJECTION.md"}
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
}
SKIP_FILE_SUFFIXES = {".pyc", ".pyo", ".log"}
TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".jsonl",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".sh",
    ".toml",
    ".cfg",
    ".ini",
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


def _as_windows_long_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _is_text_file(path: Path, raw: bytes) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES or raw.startswith(b"#!")


def canonicalize_tree_bytes(path: Path, raw: bytes) -> bytes:
    """Normalize CRLF/CR to LF for text files. Binary files are returned as-is.

    For Codex agent YAML, the ``metadata.plugin`` and
    ``metadata.projection_plugin`` keys are projection-generated identity
    fields; they are stripped before comparison so that the same source skill
    can be projected into multiple plugin packs without breaking verbatim
    mirror validation.
    """
    if not _is_text_file(path, raw):
        return raw
    text = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if path.name == "openai.yaml":
        try:
            parsed = yaml.safe_load(text.decode("utf-8"))
        except Exception:
            return text
        if isinstance(parsed, dict):
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
            return rendered.encode("utf-8")
    return text


def canonicalize_tree(root: Path) -> dict[str, bytes]:
    """Read all files under root and return a dict of rel-path -> canonicalized bytes."""
    result: dict[str, bytes] = {}
    root = root.resolve()
    root_text = _as_windows_long_path(root)
    for current, dirnames, filenames in os.walk(root_text):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIR_NAMES)
        filenames.sort()
        current_path = Path(current)
        for filename in filenames:
            if Path(filename).suffix.lower() in SKIP_FILE_SUFFIXES:
                continue
            path = current_path / filename
            rel = str(path)[len(root_text) + 1 :].replace("\\", "/")
            result[rel] = canonicalize_tree_bytes(path, Path(_as_windows_long_path(path)).read_bytes())
    return result


def compare_trees_canonicalized(expected_root: Path, actual_root: Path) -> None:
    """Compare two directory trees after canonicalization. Raises ValueError on mismatch."""
    expected = canonicalize_tree(expected_root)
    actual = canonicalize_tree(actual_root)
    if set(expected.keys()) != set(actual.keys()):
        missing = set(expected.keys()) - set(actual.keys())
        extra = set(actual.keys()) - set(expected.keys())
        parts = []
        if missing:
            parts.append(f"missing files: {sorted(missing)}")
        if extra:
            parts.append(f"extra files: {sorted(extra)}")
        raise ValueError(f"file inventory mismatch: {', '.join(parts)}")
    for rel in sorted(expected.keys()):
        if expected[rel] != actual[rel]:
            raise ValueError(f"content differs at {rel}")
