import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKTREE_HELPERS = REPO_ROOT / "scripts" / "worktree_helpers.py"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(WORKTREE_HELPERS), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_worktree_helpers_exists():
    assert WORKTREE_HELPERS.is_file(), f"{WORKTREE_HELPERS} is missing"


def test_new_help_exits_zero():
    result = _run(["new", "--help"])
    assert result.returncode == 0, result.stderr
    assert "Branch" in result.stdout or "branch" in result.stdout


def test_remove_help_exits_zero():
    result = _run(["remove", "--help"])
    assert result.returncode == 0, result.stderr
    assert "Worktree" in result.stdout or "worktree" in result.stdout
