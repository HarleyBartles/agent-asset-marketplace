#!/usr/bin/env python3
"""Read exact standard-definition bytes from a locally available Git commit."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from subscriptions import validate_commit, validate_relative_path


def read_pinned_definition(source_root: Path, commit: str, definition: str) -> bytes:
    """Read exactly commit:path or raise for invalid input or unavailable authority."""
    issues = validate_commit(commit) + validate_relative_path(definition)
    if issues:
        raise ValueError("; ".join(issues))

    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    try:
        result = subprocess.run(
            ["git", "-C", str(source_root), "show", f"{commit}:{definition}"],
            env=env,
            shell=False,
            capture_output=True,
        )
    except OSError as exc:
        raise RuntimeError(f"Git could not read pinned definition {commit}:{definition}: {exc}") from exc

    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        if not detail:
            detail = f"git show exited with status {result.returncode}"
        raise RuntimeError(f"Git could not read pinned definition {commit}:{definition}: {detail}")
    return result.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read exact standard-definition bytes from a local Git pin. (read-only)"
    )
    parser.add_argument("--source-root", type=Path, help="checkout verified against the declared source repository")
    parser.add_argument("--commit", help="full immutable 40- or 64-character Git object ID")
    parser.add_argument("--definition", help="normalized repository-relative POSIX definition path")
    parser.add_argument("--check", action="store_true", help="read-only retrieval (required)")
    args = parser.parse_args(argv)

    missing = [
        flag
        for flag, value in (
            ("--source-root", args.source_root),
            ("--commit", args.commit),
            ("--definition", args.definition),
        )
        if value is None
    ]
    if missing:
        print(f"ERROR: missing retrieval input(s): {', '.join(missing)}", file=sys.stderr)
        return 1
    if not args.check:
        print("ERROR: pass --check to read pinned authority", file=sys.stderr)
        return 1

    try:
        content = read_pinned_definition(args.source_root, args.commit, args.definition)
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
