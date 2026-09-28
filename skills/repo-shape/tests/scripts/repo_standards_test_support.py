import os
import subprocess
from pathlib import Path


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _init_git_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True, capture_output=True)


def _init_git_repo_with_commit(path: Path) -> None:
    _init_git_repo(path)
    (path / "initial.txt").write_text("initial\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "initial.txt"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=path, check=True, capture_output=True)


def _create_worktree(repo: Path, name: str) -> Path:
    worktree = repo.parent / f"{repo.name}-{name}"
    subprocess.run(
        ["git", "worktree", "add", "-b", name, str(worktree), "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return worktree
