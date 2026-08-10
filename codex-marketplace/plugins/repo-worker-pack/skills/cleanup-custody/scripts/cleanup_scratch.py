#!/usr/bin/env python3
"""Classify and optionally clean orphan _agent-scratch directories.

This script follows the skill-bundled CLI contract:
- `--help` prints usage and classifies each flag.
- `--check` (the default) reports what the script would do and exits 0
  regardless so it can be used in a read-only preflight.
- `--apply` removes delete_now entries.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _main_repo_root() -> Path:
    result = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            return Path(line.split(" ", 1)[1]).resolve()
    raise RuntimeError("Could not determine the main repository root")


def _active_branches(main_repo_root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "branch", "--format=%(refname:short)"],
        cwd=main_repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _classify(scratch_root: Path, repo_name: str, active_branches: set[str]) -> list[tuple[str, Path]]:
    repo_scratch = scratch_root / repo_name
    if not repo_scratch.exists():
        return []
    decisions = []
    for entry in repo_scratch.iterdir():
        if entry.is_dir() and entry.name in active_branches:
            decisions.append(("keep_live", entry))
        elif entry.is_dir():
            decisions.append(("delete_now", entry))
        else:
            decisions.append(("delete_now", entry))
    return decisions


def _main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify or remove orphan _agent-scratch directories. (mixed: supports --check and --apply)"
    )
    parser.add_argument("--repo-name", help="repository name to inspect; defaults to main checkout basename")
    parser.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="report classification and exit 0 (default, read-only)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="remove delete_now entries (mutating)",
    )
    args = parser.parse_args()

    main_repo_root = _main_repo_root()
    repo_name = args.repo_name or main_repo_root.name
    scratch_root = main_repo_root.parent / "_agent-scratch"
    active = _active_branches(main_repo_root)

    decisions = _classify(scratch_root, repo_name, active)
    if not decisions:
        print(f"No scratch entries for {repo_name}")
        return 0

    for decision, path in decisions:
        print(f"{decision}: {path}")
        if decision == "delete_now" and args.apply:
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            print(f"  removed {path}")

    return 0


if __name__ == "__main__":
    sys.exit(_main())
