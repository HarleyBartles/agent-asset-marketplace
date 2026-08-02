#!/usr/bin/env python3
"""Check for stale archive links after moving plans/specs to completed/."""

import argparse
import re
from pathlib import Path


_COMPLETED_DIRS = [Path(".agents/plans/completed"), Path(".agents/specs/completed")]
_ACTIVE_DIRS = [Path(".agents/plans"), Path(".agents/specs"), Path(".agents/runbooks"), Path("docs")]

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
            return d.parent / rel
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
        for m in _STALE_ACTIVE_RE.finditer(text):
            stale.append(f"{c.as_posix()}: {m.group()}")

    # 2. active files should not still reference the old active paths of completed files
    old_paths: set[str] = set()
    for c in completed:
        old = _old_active_path(c)
        if old is not None:
            old_paths.add(old.as_posix())

    if old_paths:
        pattern = re.compile(
            r"(?<![\w/])(" + "|".join(re.escape(p) for p in sorted(old_paths)) + r")(?![\w/])"
        )
        for a in active:
            text = a.read_text(encoding="utf-8", errors="replace")
            for m in pattern.finditer(text):
                stale.append(f"{a.as_posix()}: {m.group()}")

    if stale:
        for s in sorted(set(stale)):
            print(s)
        return 1

    print("No stale archive links found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
