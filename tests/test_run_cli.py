from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run  # noqa: E402


def test_run_help_exposes_targets_and_flags():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--check" in result.stdout
    assert "--apply" in result.stdout
    assert "--base-ref" in result.stdout
    assert "--allow-shared-checkout" in result.stdout
    assert "marketplace" in result.stdout
    assert "ci" in result.stdout


def test_apply_and_check_mutually_exclusive():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "inventory", "--apply", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "mutually exclusive" in result.stderr


def test_allow_shared_checkout_requires_apply():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "inventory", "--allow-shared-checkout"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "--allow-shared-checkout requires --apply" in result.stderr


def test_resolve_ci_order():
    assert run.resolve_targets(["ci"]) == ["ci"]
    targets = run._resolve_ci_deps()
    assert targets.index("lint") < targets.index("repo-standards") < targets.index("marketplace")
    assert targets.index("inventory") < targets.index("installed-skills")
    assert targets.index("installed-skills") < targets.index("repo-index")
    assert targets.index("repo-index") < targets.index("mesh")
    assert targets.index("mesh") < targets.index("validate")
    assert targets[-1] == "archive-links"


def test_resolve_all_aliases_to_ci():
    assert run.resolve_targets(["all"]) == run.resolve_targets(["ci"])


def test_resolve_multiple_targets_deduped():
    targets = run.resolve_targets(["mesh", "installed-skills"])
    assert "mesh" in targets
    assert "installed-skills" in targets
    assert targets.index("installed-skills") < targets.index("repo-index") < targets.index("mesh")


def test_runner_forwards_allow_shared_checkout(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["mesh"], ctx)

    mesh_cmd = next(
        (c for c in calls if "generate_index_mesh.py" in " ".join(c) and "--apply" in c),
        None,
    )
    assert mesh_cmd is not None
    assert "--allow-shared-checkout" in mesh_cmd


def test_runner_check_mode_no_allow_shared(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["repo-standards", "mesh"], ctx)

    for cmd in calls:
        assert "--allow-shared-checkout" not in " ".join(cmd)
        assert "--apply" not in " ".join(cmd)


def test_failure_prints_fix(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["inventory"], ctx)
    assert "target 'inventory' failed" in str(exc_info.value)
    assert "Fix: tools/run inventory --apply" in str(exc_info.value)


def test_lint_fix_command_used_in_apply(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref="origin/main", allow_shared=False, verbose=False)
    run.run_targets(["lint"], ctx)

    check_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "check"]]
    assert check_cmd
    assert "--fix" in check_cmd[0]
    fmt_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "format"]]
    assert fmt_cmd


def test_lint_check_mode_does_not_format_files(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_all_tracked_python_files", lambda: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    run.run_targets(["lint"], ctx)

    fmt_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "format"]]
    assert fmt_cmd
    assert "--check" in fmt_cmd[0]


def test_base_ref_forwards_to_ruff_diff(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="check", base_ref="custom/base", allow_shared=False, verbose=False)
    run.run_targets(["lint"], ctx)

    diff_cmd = [c for c in calls if "tools/ruff_diff.py" in " ".join(c)]
    assert diff_cmd
    assert "--changed-from" in diff_cmd[0]
    assert "custom/base" in diff_cmd[0]


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash not available")
def test_bash_wrapper_delegates_to_runpy():
    result = subprocess.run(
        ["bash", str(ROOT / "tools" / "run"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--check" in result.stdout
    assert "--apply" in result.stdout


@pytest.mark.skipif(
    shutil.which("powershell") is None and shutil.which("pwsh") is None,
    reason="PowerShell not available",
)
def test_powershell_wrapper_delegates_to_runpy():
    ps = shutil.which("pwsh") or shutil.which("powershell")
    result = subprocess.run(
        [ps, "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "tools" / "run.ps1"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--check" in result.stdout
    assert "--apply" in result.stdout


def test_read_only_tasks_do_not_advertise_apply():
    from pathlib import Path
    import importlib.util

    RUN_SPEC = importlib.util.spec_from_file_location("run", str(Path("tools/run.py").resolve()))
    run = importlib.util.module_from_spec(RUN_SPEC)
    RUN_SPEC.loader.exec_module(run)

    aggregators = {"ci", "all"}
    for name, task in run._TASKS.items():
        if name in aggregators:
            continue
        if not getattr(task, "apply", None):
            assert f"tools/run {name} --apply" not in task.fix, (
                f"{name} is read-only but its fix advertises tools/run {name} --apply"
            )


def test_validate_fix_message(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["validate"], ctx)
    assert "target 'validate' failed" in str(exc_info.value)
    assert "Fix: tools/run validate --apply" in str(exc_info.value)


def test_ci_apply_does_not_run_manual_review_preflight(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(" ".join(cmd))

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(run.resolve_targets(["ci"]), ctx)

    review_preflight_calls = [c for c in calls if "tools/review_preflight.py" in c]
    assert not review_preflight_calls


def test_validate_does_not_call_git_diff_exit_code(monkeypatch):
    calls = []

    def fake_git_diff_exit_code(ctx):
        calls.append("git_diff_exit_code")

    monkeypatch.setattr(run, "_git_diff_exit_code", fake_git_diff_exit_code)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_run", lambda cmd, ctx: None)

    ctx = run.Ctx(mode="check", base_ref=None, allow_shared=False, verbose=False)
    run._run_validate(ctx)

    assert "git_diff_exit_code" not in calls


def test_index_mesh_target_delegates_to_bundled(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=False, verbose=False)
    run.run_targets(["index-mesh"], ctx)

    mesh_cmd = next(
        (c for c in calls if "generate_index_mesh.py" in " ".join(c) and "--apply" in c),
        None,
    )
    assert mesh_cmd is not None


def test_index_mesh_target_forwards_allow_shared_checkout(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=True, verbose=False)
    run.run_targets(["index-mesh"], ctx)

    mesh_cmd = next(
        (c for c in calls if "generate_index_mesh.py" in " ".join(c) and "--allow-shared-checkout" in c),
        None,
    )
    assert mesh_cmd is not None


def test_refresh_skills_target_delegates_to_bundled(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref=None, allow_shared=False, verbose=False)
    run.run_targets(["refresh-skills"], ctx)

    refresh_cmd = next(
        (c for c in calls if "refresh_installed_skills.py" in " ".join(c) and "--apply" in c),
        None,
    )
    assert refresh_cmd is not None
