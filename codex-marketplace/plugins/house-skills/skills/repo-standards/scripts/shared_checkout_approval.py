#!/usr/bin/env python3
"""Shared-checkout approval token helpers."""

from __future__ import annotations

import datetime
import os
import subprocess
from pathlib import Path


APPROVAL_TTL_SECONDS = 600
APPROVAL_FILENAME_PREFIX = "devin-shared-checkout-approval-"


def _stripped_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _git_dir(repo_root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
        env=_stripped_env(),
    )
    return Path(result.stdout.strip()).resolve()


def approval_path(repo_root: Path, script_name: str) -> Path:
    """Return the path to the shared-checkout approval token for a script."""
    return _git_dir(repo_root) / "info" / f"{APPROVAL_FILENAME_PREFIX}{script_name}"


def _read_timestamp(path: Path) -> datetime.datetime | None:
    try:
        text = path.read_text(encoding="utf-8").strip()
        return datetime.datetime.fromisoformat(text)
    except (OSError, ValueError):
        return None


def is_valid(repo_root: Path, script_name: str) -> bool:
    """Return True if a non-expired approval token exists for the script."""
    path = approval_path(repo_root, script_name)
    timestamp = _read_timestamp(path)
    if timestamp is None:
        return False
    age = (datetime.datetime.now(datetime.timezone.utc) - timestamp).total_seconds()
    return age < APPROVAL_TTL_SECONDS


def write(repo_root: Path, script_name: str) -> Path:
    """Write an approval token for the script and return its path."""
    path = approval_path(repo_root, script_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(timestamp)
        f.write("\n")
    return path


def consume(repo_root: Path, script_name: str) -> bool:
    """Consume the approval token if it is valid; return True if consumed."""
    path = approval_path(repo_root, script_name)
    if is_valid(repo_root, script_name):
        path.unlink(missing_ok=True)
        return True
    path.unlink(missing_ok=True)
    return False
