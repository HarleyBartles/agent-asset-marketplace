import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NEW_WORKTREE = REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "new_worktree.py"
REMOVE_WORKTREE = REPO_ROOT / "adapters" / "codex" / "superpowers-plus" / "using-git-worktrees" / "scripts" / "remove_worktree.py"


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "README.md").write_text("# test\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)
    return repo


def test_new_help_exits_zero() -> None:
    result = subprocess.run([sys.executable, str(NEW_WORKTREE), "--help"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "branch" in result.stdout.lower()


def test_remove_help_exits_zero() -> None:
    result = subprocess.run([sys.executable, str(REMOVE_WORKTREE), "--help"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "worktree" in result.stdout.lower()


def test_new_and_remove_create_cycle(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "cycle-repo")
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)

    worktree_root = repo.parent / "_agent-worktrees" / "cycle-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()
