from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "marketplace-validation.yml"
PROPOSED_COMMIT = "${{ github.event.pull_request.head.sha || github.sha }}"


def _isolated_env(overrides: dict[str, str] | None = None) -> dict[str, str]:
    inherited_git_variables = subprocess.check_output(
        ["git", "rev-parse", "--local-env-vars"], cwd=ROOT, text=True
    ).splitlines()
    env = {key: value for key, value in os.environ.items() if key not in inherited_git_variables}
    env.update(overrides or {})
    return env


def _git(root: Path, *arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=root, env=_isolated_env(), text=True).strip()


def _run_bash(script: str, root: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    git = Path(shutil.which("git") or "git")
    git_bash = git.parent.parent / "bin" / "bash.exe" if os.name == "nt" else Path("bash")
    bash = str(git_bash if git_bash.is_file() else shutil.which("bash") or "bash")
    return subprocess.run(
        [bash, "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", script],
        cwd=root,
        env=_isolated_env(env),
        text=True,
        capture_output=True,
        check=False,
    )


def _detached_repo(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    (repo / "tracked.txt").write_text("candidate\n", encoding="utf-8")
    _git(repo, "add", "tracked.txt")
    _git(repo, "commit", "--quiet", "-m", "candidate")
    _git(repo, "checkout", "--quiet", "--detach", "HEAD")
    return repo, _git(repo, "rev-parse", "HEAD")


def test_hosted_gate_executes_the_commit_parity_check_and_tracked_gate(tmp_path: Path) -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    job = workflow["jobs"]["marketplace-validation"]
    steps = job["steps"]
    checkout = next(step for step in steps if step.get("name") == "Checkout")
    parity = next(step for step in steps if step.get("id") == "verify-hosted-commit")
    gate = next(step for step in steps if step.get("id") == "tracked-commit-gate")

    assert checkout.get("with", {}).get("ref") == PROPOSED_COMMIT
    assert job.get("env", {}).get("REPO_STANDARDS_HOSTED_COMMIT") == PROPOSED_COMMIT
    repo, commit = _detached_repo(tmp_path)

    passed = _run_bash(parity["run"], repo, {"REPO_STANDARDS_HOSTED_COMMIT": commit})
    assert passed.returncode == 0, passed.stderr

    mismatched = _run_bash(parity["run"], repo, {"REPO_STANDARDS_HOSTED_COMMIT": "0" * 40})
    assert mismatched.returncode != 0

    hook = repo / "githooks" / "pre-commit"
    hook.parent.mkdir()
    hook.write_text(
        "#!/usr/bin/env bash\nprintf '%s' \"$REPO_STANDARDS_HOSTED_COMMIT\" > hook-commit\n",
        encoding="utf-8",
    )
    hook.chmod(0o755)
    gate_result = _run_bash(gate["run"], repo, {"REPO_STANDARDS_HOSTED_COMMIT": commit})

    assert gate_result.returncode == 0, gate_result.stderr
    assert (repo / "hook-commit").read_text(encoding="utf-8") == commit
