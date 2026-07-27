#!/usr/bin/env python3
"""Shared-checkout detection and human-approval helpers."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _git_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--absolute-git-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip()).resolve()


def _git_common_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip()).resolve()


def is_shared_checkout(repo_root: Path) -> bool:
    """Return True if repo_root is a linked worktree or otherwise shared checkout."""
    return _git_dir(repo_root) != _git_common_dir(repo_root)


def prompt_for_approval(script_name: str) -> bool:
    """Prompt an interactive user for shared-checkout approval."""
    if not sys.stdin.isatty():
        return False
    try:
        response = input(
            f"warning: this is a shared/git-worktree checkout. "
            f"Allow {script_name} to apply changes? (y/N) "
        )
    except EOFError:
        return False
    return response.strip().lower() == "y"


def approve_mutation(repo_root: Path, script_name: str, flag_approved: bool) -> bool:
    """Return True if mutation in a shared checkout is approved.

    - Normal checkout: always approved.
    - --allow-shared-checkout passed: approved with a warning.
    - Interactive terminal: prompt the user.
    - Otherwise: print an actionable error and return False.
    """
    if not is_shared_checkout(repo_root):
        return True
    if flag_approved:
        print(
            f"warning: --allow-shared-checkout supplied; {script_name} will apply changes in a shared/git-worktree checkout",
            file=sys.stderr,
        )
        return True
    if prompt_for_approval(script_name):
        return True
    print(
        f"error: refusing to apply {script_name} in a shared checkout. "
        f"Pass --allow-shared-checkout if this is intentional, or run interactively to confirm.",
        file=sys.stderr,
    )
    return False
