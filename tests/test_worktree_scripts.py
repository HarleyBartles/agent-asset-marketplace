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


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


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
    worktree_root = tmp_path / "_agent-worktrees" / "cycle-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_root.exists()


def test_new_worktree_base_ref(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "base-ref-repo")
    marker = "base-marker.txt"
    (repo / marker).write_text("from-base", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "tag", "v1-base"], cwd=repo, check=True, capture_output=True)

    worktree_root = tmp_path / "_agent-worktrees" / "base-ref-repo" / "feature"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--base-ref", "v1-base", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_root.is_dir()
    assert (worktree_root / marker).read_text(encoding="utf-8") == "from-base"


def test_remove_worktree_resolves_by_full_ref_and_directory(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "resolve-repo")

    # Full ref match
    worktree_full = tmp_path / "_agent-worktrees" / "resolve-repo" / "feature-full"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature-full", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_full.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "refs/heads/feature-full"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_full.exists()

    # Trailing segment / directory name match
    worktree_dir = tmp_path / "_agent-worktrees" / "resolve-repo" / "feature-dir"
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature-dir", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert worktree_dir.is_dir()

    result = subprocess.run(
        [sys.executable, str(REMOVE_WORKTREE), "feature-dir"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not worktree_dir.exists()


def test_new_worktree_fails_when_target_path_already_exists(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "exists-repo")
    worktree_root = tmp_path / "_agent-worktrees" / "exists-repo" / "feature"
    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    # Existing file
    worktree_root.write_text("existing file", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "file" in result.stderr.lower()

    # Existing directory
    worktree_root.unlink()
    worktree_root.mkdir(parents=True)
    result = subprocess.run(
        [sys.executable, str(NEW_WORKTREE), "feature", "--no-skill-refresh"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "directory" in result.stderr.lower()
