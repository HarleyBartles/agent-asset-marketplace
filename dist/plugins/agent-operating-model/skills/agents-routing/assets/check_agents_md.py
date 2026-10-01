#!/usr/bin/env python3
"""Editable starter for checking repository-selected AGENTS.md size budgets."""

from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path


DEFAULT_WARN_LINES = 55
DEFAULT_ERROR_LINES = 100
DEFAULT_EXCLUDES = (".git/**",)


def _excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    relative = path.relative_to(root).as_posix()
    if ".git" in path.relative_to(root).parts:
        return True
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in (*DEFAULT_EXCLUDES, *patterns))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Check configured AGENTS.md line budgets. This reports size only; "
            "semantic router quality needs repository review. (read-only)"
        )
    )
    parser.add_argument(
        "--repo-root", type=Path, default=Path("."), help="repository root (default: current directory)"
    )
    parser.add_argument("--check", action="store_true", help="run read-only checks (default)")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="GLOB",
        help="exclude a repository-relative path pattern; repeatable",
    )
    parser.add_argument(
        "--warn-lines",
        type=int,
        default=DEFAULT_WARN_LINES,
        help="warn when a file is above this many lines (default: 55)",
    )
    parser.add_argument(
        "--error-lines",
        type=int,
        default=DEFAULT_ERROR_LINES,
        help="fail when a file is above this many lines (default: 100)",
    )
    args = parser.parse_args(argv)

    root = args.repo_root.resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")
    if args.warn_lines < 0 or args.error_lines <= args.warn_lines:
        parser.error("thresholds must satisfy 0 <= --warn-lines < --error-lines")

    files = sorted(path for path in root.rglob("AGENTS.md") if not _excluded(path, root, args.exclude))
    errors = 0
    warnings = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        try:
            count = len(path.read_text(encoding="utf-8").splitlines())
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: {relative}: cannot read file: {exc}")
            errors += 1
            continue
        if count > args.error_lines:
            print(f"ERROR: {relative}: {count} lines (error above {args.error_lines})")
            errors += 1
        elif count > args.warn_lines:
            print(f"WARN: {relative}: {count} lines (warn above {args.warn_lines})")
            warnings += 1

    print(f"Budgets: warn above {args.warn_lines}; error above {args.error_lines}. No file-count limit is applied.")
    print("Review is still required for scope, readability, safe routing, and whether the budget fits this repository.")
    print(f"Checked {len(files)} AGENTS.md file(s): {warnings} warning(s), {errors} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
