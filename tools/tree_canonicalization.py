#!/usr/bin/env python3
"""Shared tree canonicalization helpers for projection and validation tools."""

from __future__ import annotations

from pathlib import Path

TEXT_FILENAMES = {"SKILL.md", "openai.yaml", "AGENTS.md", "README.md", "LICENSE", "SOURCE.md", "PROJECTION.md"}
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
    ".ts",
    ".tsx",
}


def _is_text_file(path: Path, raw: bytes) -> bool:
    return path.name in TEXT_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES or raw.startswith(b"#!")


def canonicalize_tree_bytes(path: Path, raw: bytes) -> bytes:
    """Normalize CRLF/CR to LF for text files. Binary files are returned as-is."""
    if _is_text_file(path, raw):
        return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return raw


def canonicalize_tree(root: Path) -> dict[str, bytes]:
    """Read all files under root and return a dict of rel-path -> canonicalized bytes."""
    result: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = canonicalize_tree_bytes(path, path.read_bytes())
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
