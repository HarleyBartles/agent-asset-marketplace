import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "sources" / "first_party" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py"


def _make_source_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "source-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "tools").mkdir()
    (repo / "tools" / "generate_index_mesh.py").write_text("print('mesh ok')\n", encoding="utf-8")
    return repo


def _make_consumer_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "consumer-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "generate_index_mesh.py").write_text("print('mesh ok')\n", encoding="utf-8")
    return repo


def test_source_layout_finds_tools_command(tmp_path: Path) -> None:
    repo = _make_source_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "mesh ok" in result.stdout


def test_consumer_layout_finds_scripts_command(tmp_path: Path) -> None:
    repo = _make_consumer_repo(tmp_path)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "mesh ok" in result.stdout


def test_missing_command_fails(tmp_path: Path) -> None:
    repo = tmp_path / "empty-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    result = subprocess.run([sys.executable, str(CORE)], cwd=repo, env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert "generate_index_mesh" in result.stderr or "index mesh" in result.stderr
