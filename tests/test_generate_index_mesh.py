import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE = REPO_ROOT / "sources" / "first_party" / "skills" / "generating-agent-mesh" / "scripts" / "generate_index_mesh.py"


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    return repo


def _commit_file(repo: Path, path: str) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"# {target.name}\n\ncontent\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"add {path}"], cwd=repo, check=True, capture_output=True)


def test_source_repo_generates_index_mesh(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "source-repo")
    _commit_file(repo, "docs/guide.md")
    result = subprocess.run(
        [sys.executable, str(CORE)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Wrote index mesh" in result.stdout
    assert (repo / "INDEX.md").is_file()
    assert (repo / "docs" / "INDEX.md").is_file()


def test_check_mode_passes_when_current(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "check-repo")
    _commit_file(repo, "docs/guide.md")
    subprocess.run([sys.executable, str(CORE)], cwd=repo, env=_stripped_env(), check=True)
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "OK index mesh" in result.stdout


def test_check_mode_fails_when_stale(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "stale-repo")
    _commit_file(repo, "docs/guide.md")
    subprocess.run([sys.executable, str(CORE)], cwd=repo, env=_stripped_env(), check=True)
    _commit_file(repo, "docs/new.md")
    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "stale" in result.stderr.lower() or "stale" in result.stdout.lower()


def test_empty_repo_generates_root_index(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "empty-repo")
    _commit_file(repo, "README.md")
    result = subprocess.run(
        [sys.executable, str(CORE)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Wrote index mesh" in result.stdout
    assert (repo / "INDEX.md").is_file()


def _hook_ext() -> str:
    return ".ps1" if sys.platform == "win32" else ".sh"


def test_generate_index_mesh_extra_hook_post_processes_and_check_passes(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "hook-repo")
    _commit_file(repo, "docs/adr/README.md")
    scripts_path = repo / "scripts"
    scripts_path.mkdir()
    hook = scripts_path / f"generate_index_mesh_extra{_hook_ext()}"
    log_path = tmp_path / "hook-log.txt"

    if sys.platform == "win32":
        hook.write_text(
            "param([switch]$Check, [string]$RepoRoot)\n"
            "$path = Join-Path $RepoRoot \"docs/adr/INDEX.md\"\n"
            "if ($Check) {\n"
            '    if (-not (Test-Path $path) -or -not (Select-String -Path $path -Pattern "## Extra" -Quiet)) { Write-Host "DRIFT: missing extra"; exit 1 }\n'
            f'    [System.IO.File]::WriteAllText("{log_path.as_posix()}", "check $RepoRoot")\n'
            "} else {\n"
            '    Add-Content -Path $path -Value "## Extra`n" -NoNewline\n'
            f'    [System.IO.File]::WriteAllText("{log_path.as_posix()}", "write $RepoRoot")\n'
            "}\n",
            encoding="utf-8",
        )
    else:
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [ \"$1\" = \"--check\" ]; then\n"
            "    mode=check\n"
            "    shift\n"
            "else\n"
            "    mode=write\n"
            "fi\n"
            "repo_root=\"$1\"\n"
            "path=\"$repo_root/docs/adr/INDEX.md\"\n"
            'if [ "$mode" = "check" ]; then\n'
            '    if ! grep -q "## Extra" "$path"; then\n'
            '        echo "DRIFT: missing extra"\n'
            "        exit 1\n"
            "    fi\n"
            "else\n"
            '    echo -e "## Extra" >> "$path"\n'
            "fi\n"
            f'echo "$mode $repo_root" > "{log_path.as_posix()}"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

    result = subprocess.run(
        [sys.executable, str(CORE)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "## Extra" in (repo / "docs" / "adr" / "INDEX.md").read_text(encoding="utf-8")

    log = log_path.read_text(encoding="utf-8").strip()
    assert "write" in log
    assert str(repo) in log

    result = subprocess.run(
        [sys.executable, str(CORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "check" in log_path.read_text(encoding="utf-8").strip()


def test_generate_index_mesh_extra_hook_failure_fails(tmp_path: Path) -> None:
    repo = _make_repo(tmp_path, "fail-hook-repo")
    _commit_file(repo, "docs/adr/README.md")
    scripts_path = repo / "scripts"
    scripts_path.mkdir()
    hook = scripts_path / f"generate_index_mesh_extra{_hook_ext()}"

    if sys.platform == "win32":
        hook.write_text(
            "param([switch]$Check, [string]$RepoRoot)\n"
            "Write-Host 'broken hook'\n"
            "exit 1\n",
            encoding="utf-8",
        )
    else:
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "echo 'broken hook'\n"
            "exit 1\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)

    result = subprocess.run(
        [sys.executable, str(CORE)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken hook" in (result.stdout + result.stderr).lower()
