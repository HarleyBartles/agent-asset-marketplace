#!/usr/bin/env python3
"""Capture the consumer's canonical preflight/CI output for an iterative-review run."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _check() -> int:
    """Validate the script can be invoked without errors."""
    return 0


def _run(cwd: Path, cmd: list[str]) -> str:
    p = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
    )
    return f"--- {' '.join(cmd)} ---\n{p.stdout}\n"


def _capture(worktree: Path, output: Path) -> int:
    if not worktree.is_dir():
        print(f"error: worktree directory does not exist: {worktree}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)

    text = ""
    text += _run(worktree, ["py", "-3", "tools/run.py", "review-preflight", "--check"])
    text += _run(worktree, ["py", "-3", "tools/run.py", "ci", "--check"])

    output.write_text(text, encoding="utf-8")
    print(f"wrote {output}")
    return 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "(read-only) Capture the consumer's canonical preflight/CI output "
            "and write it as UTF-8 for an iterative-review run."
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the script and exit without capturing",
    )
    parser.add_argument(
        "--worktree",
        type=Path,
        default=Path.cwd(),
        help="path to the worktree to run preflight/CI in (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="path to write the captured preflight/CI output (UTF-8)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.check:
        return _check()
    if args.output is None:
        print("error: --output is required unless --check is used", file=sys.stderr)
        return 1
    return _capture(args.worktree, args.output)


if __name__ == "__main__":
    sys.exit(main())
