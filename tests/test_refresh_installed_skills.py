import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "sources" / "first_party" / "skills" / "refreshing-installed-skills" / "scripts" / "refresh_installed_skills.py"


def _load_core_module():
    spec = importlib.util.spec_from_file_location("refresh_installed_skills", CORE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


refresh_installed_skills = _load_core_module()


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _make_source_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "source-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "codex-marketplace" / "plugins").mkdir(parents=True)
    (repo / "tools").mkdir()
    (repo / "tools" / "install_agent_skills.py").write_text(
        "import sys\nprint('install ok')\n", encoding="utf-8"
    )
    (repo / "tools" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts").mkdir(parents=True)
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    return repo


def _make_consumer_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "consumer-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "install_agent_skills.py").write_text(
        "import sys\nprint('install ok')\n", encoding="utf-8"
    )
    (repo / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts").mkdir(parents=True)
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh ok')\n", encoding="utf-8"
    )
    return repo


def test_source_layout_runs_tools_commands(tmp_path: Path) -> None:
    repo = _make_source_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "install ok" in result.stdout
    assert "mesh ok" in result.stdout


def test_consumer_layout_runs_scripts_commands(tmp_path: Path) -> None:
    repo = _make_consumer_repo(tmp_path)
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "install ok" in result.stdout
    assert "mesh ok" in result.stdout


def test_missing_install_command_fails(tmp_path: Path) -> None:
    repo = tmp_path / "empty-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "install_agent_skills" in result.stderr or "install skills" in result.stderr


def test_check_is_propagated_to_install_and_mesh(tmp_path: Path) -> None:
    repo = tmp_path / "check-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "install_agent_skills.py").write_text(
        "import sys\nprint('install check ok')\nsys.exit(0 if '--check' in sys.argv else 1)\n",
        encoding="utf-8",
    )
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts").mkdir(parents=True)
    (repo / ".agents" / "skills" / "generating-index-mesh" / "scripts" / "generate_index_mesh.py").write_text(
        "import sys\nprint('mesh check ok')\nsys.exit(0 if '--check' in sys.argv else 1)\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "install check ok" in result.stdout
    assert "mesh check ok" in result.stdout


def test_check_is_propagated_to_override(tmp_path: Path) -> None:
    repo = tmp_path / "override-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / "scripts").mkdir()
    (repo / "scripts" / "refresh-installed-skills.py").write_text(
        "import sys\nprint('override check ok')\nsys.exit(0 if '--check' in sys.argv else 1)\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "override check ok" in result.stdout


def test_missing_marketplace_source_initializes_submodule(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "submodule-repo"
    repo.mkdir()
    (repo / ".gitmodules").write_text(
        "[submodule \"marketplace-source\"]\n\tpath = .agents/plugins/marketplace-source\n",
        encoding="utf-8",
    )
    recorded = []

    def fake_run(cmd, **kwargs):
        recorded.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(refresh_installed_skills.subprocess, "run", fake_run)
    refresh_installed_skills._init_marketplace_source(repo)
    assert len(recorded) == 2
    assert recorded[0][:3] == ["git", "submodule", "status"]
    assert recorded[1][:5] == ["git", "submodule", "update", "--init", "--recursive"]
    assert Path(recorded[1][-1]).as_posix() == ".agents/plugins/marketplace-source"


def test_unrelated_submodule_is_not_initialized(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "other-submodule-repo"
    repo.mkdir()
    (repo / ".gitmodules").write_text(
        "[submodule \"other\"]\n\tpath = other\n",
        encoding="utf-8",
    )
    recorded = []

    def fake_run(cmd, **kwargs):
        recorded.append(cmd)
        return subprocess.CompletedProcess(cmd, 1, "", "")

    monkeypatch.setattr(refresh_installed_skills.subprocess, "run", fake_run)
    refresh_installed_skills._init_marketplace_source(repo)
    assert len(recorded) == 1
    assert recorded[0][:3] == ["git", "submodule", "status"]
