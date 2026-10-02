from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess

import yaml


WORKFLOW = Path(__file__).resolve().parents[2] / "assets" / "workflows" / "github-actions-hosted-gate.yml"


def _isolated_env() -> dict[str, str]:
    root = Path(__file__).resolve().parents[4]
    inherited_git_variables = subprocess.check_output(
        ["git", "rev-parse", "--local-env-vars"], cwd=root, text=True
    ).splitlines()
    return {key: value for key, value in os.environ.items() if key not in inherited_git_variables}


def test_workflow_executes_the_tracked_gate_for_the_declared_commit(tmp_path: Path) -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    jobs = workflow["jobs"]
    gate = jobs["complete-gate"]
    steps = gate["steps"]
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    hosted = next(step for step in steps if step.get("id") == "tracked-complete-gate")

    assert checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    assert gate["env"]["COMMIT_SHA"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    assert len([step for step in steps if step.get("uses", "").startswith("actions/checkout@")]) == 1

    repo = tmp_path / "repo"
    repo.mkdir()
    hook = repo / "githooks" / "pre-commit"
    hook.parent.mkdir()
    hook.write_text(
        '#!/usr/bin/env bash\nprintf \'%s\\n%s\' "$1" "$2" > hook-arguments\n',
        encoding="utf-8",
    )
    hook.chmod(0o755)
    git = Path(shutil.which("git") or "git")
    git_bash = git.parent.parent / "bin" / "bash.exe" if os.name == "nt" else Path("bash")
    bash = str(git_bash if git_bash.is_file() else shutil.which("bash") or "bash")
    result = subprocess.run(
        [bash, "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", hosted["run"]],
        cwd=repo,
        env={**_isolated_env(), "COMMIT_SHA": "candidate-sha"},
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (repo / "hook-arguments").read_text(encoding="utf-8").splitlines() == ["--hosted", "candidate-sha"]
