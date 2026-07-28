from __future__ import annotations

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
    targets = run.resolve_targets(["ci"])
    assert targets.index("lint") < targets.index("repo-standards") < targets.index("marketplace")
    assert targets.index("inventory") < targets.index("heal") < targets.index("project")
    assert targets.index("project") < targets.index("installed-skills")
    assert targets.index("installed-skills") < targets.index("repo-index")
    assert targets.index("repo-index") < targets.index("mesh")
    assert targets.index("mesh") < targets.index("catalog")
    assert targets.index("catalog") < targets.index("validate")
    assert targets[-1] == "ci"


def test_resolve_all_aliases_to_ci():
    assert run.resolve_targets(["all"]) == run.resolve_targets(["ci"])


def test_resolve_multiple_targets_deduped():
    targets = run.resolve_targets(["mesh", "installed-skills"])
    assert "mesh" in targets
    assert "installed-skills" in targets
    assert targets.index("project") < targets.index("installed-skills")
    assert targets.index("project") < targets.index("repo-index") < targets.index("mesh")


def test_runner_forwards_allow_shared_checkout(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_prune_stale_projected_plugin_roots", lambda: None)
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
