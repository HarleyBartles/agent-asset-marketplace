from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[4]
SCRIPT = REPO / "skills/repo-standards/scripts/pinned_definition.py"
HELPER_DIR = SCRIPT.parent
sys.path.insert(0, str(HELPER_DIR))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


subscriptions = _load_module("subscriptions", HELPER_DIR / "subscriptions.py")
pinned_definition = _load_module("pinned_definition", SCRIPT)
read_pinned_definition = pinned_definition.read_pinned_definition


@pytest.fixture
def git_authority(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "authority"
    root.mkdir()
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)

    def git(*args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    git("init")
    git("config", "user.name", "Fixture")
    git("config", "user.email", "fixture@example.invalid")
    git("config", "commit.gpgsign", "false")
    git("config", "core.autocrlf", "false")
    path = root / "rules/standard.md"
    path.parent.mkdir()
    path.write_bytes(b"old requirements\n")
    git("add", "rules/standard.md")
    git("-c", "core.hooksPath=", "commit", "-m", "old definition")
    old_commit = git("rev-parse", "HEAD")
    path.write_bytes(b"new requirements\n")
    git("add", "rules/standard.md")
    git("-c", "core.hooksPath=", "commit", "-m", "new definition")
    return root, old_commit


def test_older_commit_is_read_after_branch_advances(git_authority: tuple[Path, str]) -> None:
    root, old_commit = git_authority

    assert read_pinned_definition(root, old_commit, "rules/standard.md") == b"old requirements\n"


def test_missing_path_has_no_head_fallback(git_authority: tuple[Path, str]) -> None:
    root, old_commit = git_authority

    with pytest.raises(RuntimeError, match="Git could not read pinned definition"):
        read_pinned_definition(root, old_commit, "rules/missing.md")


def test_unavailable_commit_has_no_current_branch_fallback(git_authority: tuple[Path, str]) -> None:
    root, _old_commit = git_authority

    with pytest.raises(RuntimeError, match="Git could not read pinned definition"):
        read_pinned_definition(root, "0" * 40, "rules/standard.md")


@pytest.mark.parametrize("commit", ["main", "a" * 39, "A" * 40])
def test_invalid_commit_is_rejected_before_git(commit: str, git_authority: tuple[Path, str]) -> None:
    root, _old_commit = git_authority

    with pytest.raises(ValueError, match="commit must be a full"):
        read_pinned_definition(root, commit, "rules/standard.md")


@pytest.mark.parametrize("definition", ["../outside.md", "C:rules\\standard.md", "/absolute.md", "a/./b.md"])
def test_unsafe_definition_path_is_rejected(definition: str, git_authority: tuple[Path, str]) -> None:
    root, old_commit = git_authority

    with pytest.raises(ValueError, match="path must be normalized"):
        read_pinned_definition(root, old_commit, definition)


def test_dirty_worktree_is_untouched_and_cannot_change_pinned_bytes(git_authority: tuple[Path, str]) -> None:
    root, old_commit = git_authority
    path = root / "rules/standard.md"
    path.write_bytes(b"uncommitted replacement\n")

    actual = read_pinned_definition(root, old_commit, "rules/standard.md")

    assert actual == b"old requirements\n"
    assert path.read_bytes() == b"uncommitted replacement\n"


def test_cli_prints_exact_bytes_and_help_does_not_read_source(tmp_path: Path, git_authority: tuple[Path, str]) -> None:
    root, old_commit = git_authority
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source-root",
            str(root),
            "--commit",
            old_commit,
            "--definition",
            "rules/standard.md",
            "--check",
        ],
        capture_output=True,
        check=False,
    )
    help_result = subprocess.run(
        [sys.executable, str(SCRIPT), "--source-root", str(tmp_path / "missing"), "--help"],
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == b"old requirements\n"
    assert help_result.returncode == 0


def test_bare_check_reports_missing_inputs_without_argparse_error() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert b"missing" in result.stderr.lower()
