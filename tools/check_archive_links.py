#!/usr/bin/env python3
"""Check for stale archive links after moving plans/specs to completed/."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

_FENCE_RE = re.compile(r"^\s*(```+|~~~+).*$")


_COMPLETED_DIRS = [
    REPO_ROOT / ".agents/plans/completed",
    REPO_ROOT / ".agents/specs/completed",
]
_ACTIVE_DIRS = [
    REPO_ROOT / ".agents/plans",
    REPO_ROOT / ".agents/specs",
    REPO_ROOT / ".agents/runbooks",
    REPO_ROOT / "docs",
]


def _code_block_lines(text: str) -> set[int]:
    """Return 0-based line numbers that fall inside fenced code blocks."""
    fence: str | None = None
    fence_len: int = 0
    lines = text.splitlines()
    inside: set[int] = set()
    for i, line in enumerate(lines):
        m = _FENCE_RE.match(line)
        if m:
            run = m.group(1)
            if fence is None:
                fence = run[0]
                fence_len = len(run)
            elif run[0] == fence and len(run) >= fence_len:
                fence = None
                fence_len = 0
            continue
        if fence is not None:
            inside.add(i)
    return inside


# Active .agents/plans/ or .agents/specs/ path that is not inside completed/
_STALE_ACTIVE_RE = re.compile(
    r"\.agents/(?:plans|specs)/(?!completed/)(?:[A-Za-z0-9_\-]+/)*\d{4}-\d{2}-\d{2}-[A-Za-z0-9_\-]+\.md"
)


def _completed_files() -> list[Path]:
    files: list[Path] = []
    for d in _COMPLETED_DIRS:
        if d.is_dir():
            files.extend(p for p in d.rglob("*.md") if p.name != "INDEX.md")
    return sorted(files)


def _active_files() -> list[Path]:
    files: list[Path] = []
    for d in _ACTIVE_DIRS:
        if d.is_dir():
            files.extend(p for p in d.rglob("*.md") if "completed/" not in p.as_posix())
    return sorted(files)


def _old_active_path(completed: Path) -> Path | None:
    for d in _COMPLETED_DIRS:
        if completed.is_relative_to(d):
            rel = completed.relative_to(d)
            return d.parent.relative_to(REPO_ROOT) / rel
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check for stale archive links after moving plans and specs to completed/.",
    )
    parser.parse_args(argv)

    completed = _completed_files()
    active = _active_files()
    stale: list[str] = []

    # 1. completed/ files should reference other completed/ files, not active .agents/plans/ or .agents/specs/ paths
    for c in completed:
        text = c.read_text(encoding="utf-8", errors="replace")
        code_lines = _code_block_lines(text)
        for m in _STALE_ACTIVE_RE.finditer(text):
            line_no = text[: m.start()].count("\n")
            if line_no in code_lines:
                continue
            stale.append(f"{c.as_posix()}: {m.group()}")

    # 2. active files should not still reference the old active paths of completed files
    old_paths: set[str] = set()
    for c in completed:
        old = _old_active_path(c)
        if old is not None:
            old_paths.add(old.as_posix())

    if old_paths:
        pattern = re.compile(
            r"(?<![\w.])(" + "|".join(re.escape(p) for p in sorted(old_paths)) + r")(?![\w/])"
        )
        for a in active:
            text = a.read_text(encoding="utf-8", errors="replace")
            code_lines = _code_block_lines(text)
            for m in pattern.finditer(text):
                line_no = text[: m.start()].count("\n")
                if line_no in code_lines:
                    continue
                stale.append(f"{a.as_posix()}: {m.group()}")

    if stale:
        for s in sorted(set(stale)):
            print(s)
        return 1

    print("No stale archive links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
