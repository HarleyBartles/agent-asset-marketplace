from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "marketplace-validation.yml"
HOOK = ROOT / "githooks" / "pre-commit"
ADAPTER = ROOT / "tools" / "hook_gate_adapter.sh"
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
    if os.name == "nt":
        git = Path(shutil.which("git") or "git")
        bash_path = next(
            (parent / "bin" / "bash.exe" for parent in git.parents if (parent / "bin" / "bash.exe").is_file()),
            Path(shutil.which("bash") or "bash"),
        )
    else:
        bash_path = Path(shutil.which("bash") or "bash")
    bash = str(bash_path)
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
    tools = repo / "tools"
    tools.mkdir()
    shutil.copyfile(ADAPTER, tools / "hook_gate_adapter.sh")
    (tools / "run.py").write_text(
        "import os, sys\n"
        "from pathlib import Path\n"
        "if sys.argv[1:] != ['ci', '--check']:\n"
        "    raise SystemExit(2)\n"
        "if (Path.cwd() / 'missing-prerequisite').exists():\n"
        "    print('required check prerequisite missing: pytest', file=sys.stderr)\n"
        "    raise SystemExit(2)\n"
        "marker = os.environ.get('HOSTED_LATE_MARKER')\n"
        "if marker:\n"
        "    Path(marker).write_text('expensive stage started\\n', encoding='utf-8')\n",
        encoding="utf-8",
    )
    contract = repo / ".agents" / "contracts"
    contract.mkdir(parents=True)
    (contract / "repo-standards-commands.json").write_text(
        json.dumps({"check": [["@python", "tools/run.py", "ci", "--check"]]}),
        encoding="utf-8",
    )
    hook_dir = repo / "githooks"
    hook_dir.mkdir()
    shutil.copyfile(HOOK, hook_dir / "pre-commit")
    if os.name != "nt":
        (hook_dir / "pre-commit").chmod(0o755)
    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "candidate")
    _git(repo, "checkout", "--quiet", "--detach", "HEAD")
    return repo, _git(repo, "rev-parse", "HEAD")


def test_hosted_workflow_executes_the_real_candidate_preserving_hook(tmp_path: Path) -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    job = workflow["jobs"]["marketplace-validation"]
    steps = job["steps"]
    checkout = next(step for step in steps if step.get("name") == "Checkout")
    parity = next(step for step in steps if step.get("id") == "verify-hosted-commit")
    gate = next(step for step in steps if step.get("id") == "tracked-commit-gate")

    assert checkout.get("with", {}).get("ref") == PROPOSED_COMMIT
    assert job.get("env", {}).get("REPO_STANDARDS_HOSTED_COMMIT") == PROPOSED_COMMIT
    repo, commit = _detached_repo(tmp_path)
    context = {"REPO_STANDARDS_HOSTED_COMMIT": commit}

    passed = _run_bash(parity["run"], repo, context)
    assert passed.returncode == 0, passed.stdout + passed.stderr
    gate_result = _run_bash(gate["run"], repo, context)

    assert gate_result.returncode == 0, gate_result.stdout + gate_result.stderr
    assert _git(repo, "status", "--porcelain", "--untracked-files=all") == ""


def test_hosted_missing_prerequisite_fails_before_later_gate_work(tmp_path: Path) -> None:
    workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    steps = workflow["jobs"]["marketplace-validation"]["steps"]
    gate = next(step for step in steps if step.get("id") == "tracked-commit-gate")
    repo, _ = _detached_repo(tmp_path)
    (repo / "missing-prerequisite").write_text("missing\n", encoding="utf-8")
    _git(repo, "add", "missing-prerequisite")
    _git(repo, "-c", "core.hooksPath=disabled-hooks", "commit", "--quiet", "-m", "missing prerequisite")
    commit = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "--quiet", "--detach", commit)
    late_marker = tmp_path / "late gate marker.txt"

    result = _run_bash(
        gate["run"],
        repo,
        {"REPO_STANDARDS_HOSTED_COMMIT": commit, "HOSTED_LATE_MARKER": str(late_marker)},
    )

    assert result.returncode == 2
    assert "required check prerequisite missing: pytest" in result.stderr
    assert not late_marker.exists()
