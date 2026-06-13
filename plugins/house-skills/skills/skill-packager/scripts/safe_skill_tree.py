#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
"""Bounded source-tree helpers for skill packaging scripts."""

from pathlib import Path
from typing import Iterable, Iterator

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
}
SKIP_FILE_NAMES = {
    "skill.zip",
    "package-evidence.json",
}
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
BINARY_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".zip",
}
MAX_TEXT_BYTES = 2 * 1024 * 1024


def is_hidden_path(rel: Path) -> bool:
    return any(part.startswith(".") for part in rel.parts)


def is_skipped_dir(path: Path) -> bool:
    return path.name in SKIP_DIR_NAMES


def is_text_file(path: Path) -> bool:
    return path.name in {"SKILL.md", "openai.yaml"} or path.suffix.lower() in TEXT_SUFFIXES


def iter_skill_files(skill_dir: Path, include_skipped: bool = False) -> Iterator[Path]:
    """Yield files under skill_dir without descending into known output/cache dirs."""
    root = Path(skill_dir).resolve()
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name)
        except OSError:
            continue
        dirs = []
        for entry in entries:
            rel = entry.relative_to(root)
            if entry.is_symlink():
                raise ValueError(f"symlink not allowed: {rel}")
            if entry.is_dir():
                if not include_skipped and (is_hidden_path(rel) or is_skipped_dir(entry)):
                    continue
                dirs.append(entry)
            elif entry.is_file():
                if not include_skipped and any(part in SKIP_DIR_NAMES for part in rel.parts):
                    continue
                yield entry
        stack.extend(reversed(dirs))


def skipped_output_paths(skill_dir: Path) -> list[str]:
    root = Path(skill_dir).resolve()
    skipped: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_symlink():
            skipped.append(str(rel))
            continue
        if any(part in SKIP_DIR_NAMES for part in rel.parts):
            skipped.append(str(rel))
            continue
        if path.is_file() and path.name in SKIP_FILE_NAMES:
            skipped.append(str(rel))
    return skipped


def read_bounded_text(path: Path) -> tuple[bytes | None, str | None, str | None]:
    size = path.stat().st_size
    if size > MAX_TEXT_BYTES:
        return None, None, f"text file exceeds {MAX_TEXT_BYTES} byte lint limit"
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return raw, None, f"text file is not valid UTF-8: {exc}"
    return raw, text, None
