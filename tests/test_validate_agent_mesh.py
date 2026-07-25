import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = (
    REPO_ROOT
    / "sources"
    / "first_party"
    / "skills"
    / "generating-agent-mesh"
    / "scripts"
    / "validate_agent_mesh.py"
)


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def test_source_repo_agent_mesh_passes() -> None:
    """The current checkout's agent mesh is valid."""
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=REPO_ROOT,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK agent mesh" in result.stdout


def test_broken_markdown_link_fails(tmp_path: Path) -> None:
    """A repo with a broken local link in an INDEX.md fails validation."""
    repo = tmp_path / "broken-link-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)

    (repo / "INDEX.md").write_text(
        "# Test\n[broken](./missing.md)\n",
        encoding="utf-8",
        newline="\n",
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken link" in result.stderr.lower()
