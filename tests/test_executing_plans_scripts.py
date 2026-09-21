from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXECUTING = ROOT / "codex-marketplace/plugins/superpowers-plus/skills/executing-plans"


def _bash() -> str | None:
    git_bash = Path("C:/Program Files/Git/bin/bash.exe")
    if git_bash.is_file():
        return str(git_bash)
    return shutil.which("bash")


def _wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    tail = resolved.as_posix().split(":", 1)[1].lstrip("/")
    return f"/mnt/{drive}/{tail}"


def test_upstream_task_helpers_remain_bash_and_resolve_python_workspace_helpers():
    scripts = EXECUTING / "scripts"
    assert {path.name for path in scripts.iterdir() if path.is_file()} == {
        "resolve-runtime",
        "task-done",
        "task-start",
    }
    for name in ("task-start", "task-done"):
        text = (scripts / name).read_text(encoding="utf-8")
        assert text.startswith("#!/usr/bin/env bash\n")
        assert '"$script_dir/resolve-runtime"' in text
        assert "py -3" not in text
        assert ".ps1" not in text


@pytest.mark.skipif(_bash() is None, reason="Git Bash/bash is unavailable")
def test_upstream_task_helpers_have_valid_bash_syntax():
    bash = _bash()
    assert bash is not None
    for name in ("resolve-runtime", "task-start", "task-done"):
        subprocess.run([bash, "-n", (EXECUTING / "scripts" / name).as_posix()], check=True)


@pytest.mark.skipif(_bash() is None, reason="Git Bash/bash is unavailable")
def test_task_start_uses_explicit_python_when_launcher_is_absent(tmp_path: Path):
    bash = _bash()
    assert bash is not None
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    plan = repo / "plan.md"
    plan.write_text("### Task 1: Explicit interpreter\n\nOne bounded task.\n", encoding="utf-8")
    subprocess.run(["git", "add", "plan.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True)

    env = os.environ.copy()
    env["PYTHON_EXECUTABLE"] = sys.executable
    env["PATH"] = os.pathsep.join(entry for entry in env["PATH"].split(os.pathsep) if "Python\\Launcher" not in entry)
    result = subprocess.run(
        [bash, (EXECUTING / "scripts" / "task-start").as_posix(), str(plan), "1"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "brief:" in result.stdout
    assert "base:" in result.stdout


@pytest.mark.skipif(_bash() is None, reason="Git Bash/bash is unavailable")
def test_runtime_resolution_falls_back_from_broken_python3_to_python(tmp_path: Path):
    bash = _bash()
    assert bash is not None
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    (fake_bin / "python3").write_text("#!/usr/bin/env bash\nexit 9\n", encoding="utf-8")
    concrete_python = Path(sys.executable).as_posix()
    (fake_bin / "python").write_text(
        f'#!/usr/bin/env bash\nexec "{concrete_python}" "$@"\n',
        encoding="utf-8",
    )
    for path in (fake_bin / "python3", fake_bin / "python"):
        path.chmod(0o755)

    env = os.environ.copy()
    env.pop("PYTHON_EXECUTABLE", None)
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
    result = subprocess.run(
        [bash, (EXECUTING / "scripts" / "resolve-runtime").as_posix()],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    native = subprocess.run(
        [bash, "-lc", 'cygpath -w "$1"', "resolve-runtime-test", result.stdout.strip()],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert Path(native).resolve() == Path(sys.executable).resolve()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows host mismatch scenario")
def test_wsl_bash_rejects_a_windows_managed_worktree_before_running_python():
    system_bash = Path("C:/Windows/System32/bash.exe")
    if not system_bash.is_file():
        pytest.skip("WSL bash is unavailable")

    probe = subprocess.run(
        [str(system_bash), "-lc", "grep -qi microsoft /proc/sys/kernel/osrelease"],
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        pytest.skip("System bash is not WSL")

    result = subprocess.run(
        [
            str(system_bash),
            _wsl_path(EXECUTING / "scripts" / "task-start"),
            ".agents/plans/2026-09-21-receiving-code-review-deeper-smell.md",
            "5",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "execution environment mismatch" in result.stderr.lower()
    assert "traceback" not in result.stderr.lower()


@pytest.mark.skipif(_bash() is None, reason="Git Bash/bash is unavailable")
def test_task_done_records_a_silent_success(tmp_path: Path):
    bash = _bash()
    assert bash is not None
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    plan = repo / "plan.md"
    plan.write_text("### Task 1: Silent\n", encoding="utf-8")
    subprocess.run(["git", "add", "plan.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "seed"], cwd=repo, check=True, capture_output=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()

    result = subprocess.run(
        [
            bash,
            (EXECUTING / "scripts" / "task-done").as_posix(),
            str(plan),
            "1",
            base,
            "--",
            sys.executable,
            "-c",
            "pass",
        ],
        cwd=repo,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS (no output)" in result.stdout
