#!/usr/bin/env python3
"""Validate and optionally clean the _agent-scratch directory layout."""

import argparse
import os
import re
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


def _scratch_root() -> Path:
    main = _main_repo_root()
    return main.parent / "_agent-scratch"


def _valid_name(name: str) -> bool:
    """Return True if name is a non-empty, path-safe token without separators."""
    return bool(name) and re.fullmatch(r"[A-Za-z0-9_.-]+", name) is not None


def _validate(check: bool, apply: bool) -> int:
    scratch_root = _scratch_root()
    if not scratch_root.exists():
        print(f"OK: {scratch_root} does not exist")
        return 0

    issues = 0
    for entry in scratch_root.iterdir():
        if entry.is_file():
            print(f"FAIL: top-level scratch file {entry.name} is not a repo folder")
            if apply:
                entry.unlink()
                print(f"  removed {entry}")
            issues += 1
            continue
        if not _valid_name(entry.name):
            print(f"FAIL: {entry.name} is not a valid repo-name folder")
            if apply:
                shutil.rmtree(entry, ignore_errors=True)
                print(f"  removed {entry}")
            issues += 1
            continue
        for repo_entry in entry.iterdir():
            if repo_entry.is_file():
                print(f"FAIL: {entry.name} contains a file {repo_entry.name}, expected branch/task folders")
                if apply:
                    repo_entry.unlink()
                    print(f"  removed {repo_entry}")
                issues += 1
                continue
            if not _valid_name(repo_entry.name):
                print(f"FAIL: {entry.name}/{repo_entry.name} is not a valid branch/task folder")
                if apply:
                    shutil.rmtree(repo_entry, ignore_errors=True)
                    print(f"  removed {repo_entry}")
                issues += 1

    if issues:
        print(f"FAIL: {issues} issue(s) found")
        return 0 if apply else 1
    print(f"OK: {scratch_root} is clean and namespaced")
    return 0


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the _agent-scratch directory is namespaced by repo. (mixed: supports --check and --apply)"
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        default=True,
        help="report drift and exit 1 if found (default, read-only)",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help="remove invalid top-level files and non-namespaced folders (mutating)",
    )
    args = parser.parse_args()
    if args.apply:
        return _validate(check=False, apply=True)
    return _validate(check=True, apply=False)


if __name__ == "__main__":
    sys.exit(_cli())
