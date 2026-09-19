from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXECUTING = ROOT / "codex-marketplace/plugins/superpowers-plus/skills/executing-plans"


def _bash() -> str | None:
    git_bash = Path("C:/Program Files/Git/bin/bash.exe")
    if git_bash.is_file():
        return str(git_bash)
    return shutil.which("bash")


def test_upstream_task_helpers_remain_bash_and_call_python_workspace_helpers():
    scripts = EXECUTING / "scripts"
    assert {path.name for path in scripts.iterdir() if path.is_file()} == {"task-done", "task-start"}
    for name in ("task-start", "task-done"):
        text = (scripts / name).read_text(encoding="utf-8")
        assert text.startswith("#!/usr/bin/env bash\n")
        assert "py -3" in text
        assert ".ps1" not in text


@pytest.mark.skipif(_bash() is None, reason="Git Bash/bash is unavailable")
def test_upstream_task_helpers_have_valid_bash_syntax():
    bash = _bash()
    assert bash is not None
    for name in ("task-start", "task-done"):
        subprocess.run([bash, "-n", (EXECUTING / "scripts" / name).as_posix()], check=True)
