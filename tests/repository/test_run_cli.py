from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _fixture_env() -> dict[str, str]:
    import os

    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    return env


def test_changed_python_files_use_staged_snapshot_when_hook_marks_it(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "staged-python"
    repo.mkdir()
    env = _fixture_env()
    subprocess.run(["git", "init"], cwd=repo, env=env, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, env=env, check=True)
    source = repo / "sample.py"
    source.write_text("value = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "sample.py"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-m", "base"], cwd=repo, env=env, check=True, capture_output=True)
    source.write_text("value = 2\n", encoding="utf-8")
    subprocess.run(["git", "add", "sample.py"], cwd=repo, env=env, check=True)

    spec = importlib.util.spec_from_file_location("run_under_test", ROOT / "tools" / "run.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", repo)
    monkeypatch.setenv("REPO_STANDARDS_STAGED_SNAPSHOT", "1")
    monkeypatch.delenv("GIT_DIR", raising=False)
    monkeypatch.delenv("GIT_WORK_TREE", raising=False)
    monkeypatch.delenv("GIT_INDEX_FILE", raising=False)

    assert module._changed_python_files("HEAD") == [Path("sample.py")]


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
    assert "marketplace" in result.stdout
    assert "ci" in result.stdout


def test_apply_and_check_mutually_exclusive():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "run.py"), "inventory", "--apply", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "mutually exclusive" in result.stderr


def test_resolve_ci_order():
    assert run.resolve_targets(["ci"]) == ["ci"]
    targets = run._resolve_ci_deps()
    assert targets == [
        "normalize",
        "lint",
        "format",
        "validate",
        "repo-standards",
        "inventory",
        "marketplace",
        "tests-build",
        "tests-repository",
        "tests-shipping",
    ]
    assert "installed-skills" not in targets
    assert not {"repo-index", "mesh", "index-mesh"}.intersection(targets)
    assert "archive-links" not in targets


def test_ci_rejects_stale_marketplace_package_before_tests(tmp_path: Path):
    repo = tmp_path / "repo"
    subprocess.run(
        ["git", "clone", "--quiet", "--shared", str(ROOT), str(repo)],
        check=True,
    )
    shutil.copy2(ROOT / "tools" / "run.py", repo / "tools" / "run.py")
    source = repo / "skills" / "command-bus" / "SKILL.md"
    source.write_text(
        source.read_text(encoding="utf-8") + "\nStale package probe.\n",
        encoding="utf-8",
        newline="\n",
    )
    env = os.environ.copy()
    env["REPO_STANDARDS_STAGED_SNAPSHOT"] = "1"
    result = subprocess.run(
        [sys.executable, "tools/run.py", "ci", "--check"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "marketplace" in result.stderr
    assert "tests-build" not in result.stdout
    assert "tests-repository" not in result.stdout
    assert "tests-shipping" not in result.stdout


def test_validation_failure_stops_before_tests_and_preserves_status(monkeypatch, capsys):
    started = []
    original_steps = run._run_steps

    def fail_validation(ctx):
        raise subprocess.CalledProcessError(17, ["validator", "--check"])

    monkeypatch.setitem(run._TASKS, "validate", run.Task(check=(fail_validation,)))

    def probe(target, task, steps, ctx):
        if target == "ci":
            return original_steps(target, task, steps, ctx)
        started.append(target)
        if target == "validate":
            return original_steps(target, task, steps, ctx)
        if target.startswith("tests-"):
            pytest.fail("expensive test suite ran before cheap validation failed")

    monkeypatch.setattr(run, "_run_steps", probe)
    monkeypatch.setattr(run, "_resolve_base_ref", lambda args: "origin/main")

    assert run.main(["ci", "--check"]) == 17
    assert "validate" in started
    assert not any(target.startswith("tests-") for target in started)
    failure = capsys.readouterr().err
    assert "validator" in failure and "--check" in failure


def test_lint_failure_stops_before_tests(monkeypatch):
    started = []
    original_steps = run._run_steps

    def probe(target, task, steps, ctx):
        if target == "ci":
            return original_steps(target, task, steps, ctx)
        started.append(target)
        if target == "lint":
            raise run.RunnerError(target, "repair lint findings", subprocess.CalledProcessError(17, ["ruff", "check"]))
        if target.startswith("tests-"):
            pytest.fail("expensive test suite ran before cheap lint failed")

    monkeypatch.setattr(run, "_run_steps", probe)

    with pytest.raises(run.RunnerError) as exc_info:
        run._run_ci(run.Ctx("check", "origin/main", False, False))

    assert exc_info.value.exit_code == 17
    assert started[:2] == ["normalize", "lint"]
    assert not any(target.startswith("tests-") for target in started)


def test_ci_runs_only_the_three_repository_owned_test_suites(monkeypatch):
    calls = []
    monkeypatch.setenv("REPO_STANDARDS_STAGED_SNAPSHOT", "1")

    def fake_run(cmd, ctx, *, env=None):
        calls.append((cmd, env))

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_check_tracked_line_endings", lambda: None)
    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)

    run.run_targets(["ci"], ctx)

    test_targets = [target for target in run._resolve_ci_deps() if target.startswith("tests-")]
    assert test_targets == ["tests-build", "tests-repository", "tests-shipping"]
    pytest_calls = [(cmd, env) for cmd, env in calls if "pytest" in cmd]
    assert [command for command, _ in pytest_calls] == [
        [sys.executable, "-m", "pytest", "-q", "tests/build"],
        [sys.executable, "-m", "pytest", "-q", "tests/repository"],
        [sys.executable, "-m", "pytest", "-q", "tests/shipping"],
    ]
    for _, environment in pytest_calls:
        assert "REPO_STANDARDS_STAGED_SNAPSHOT" not in environment
        assert "REPO_STANDARDS_HOSTED_COMMIT" not in environment


def test_resolve_all_aliases_to_ci():
    assert run.resolve_targets(["all"]) == run.resolve_targets(["ci"])


def test_resolve_multiple_targets_deduped():
    targets = run.resolve_targets(["marketplace", "validate"])
    assert "marketplace" in targets
    assert "validate" in targets


def test_runner_check_mode_does_not_apply_mutations(monkeypatch):
    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)
    monkeypatch.setattr(run, "_check_tracked_line_endings", lambda: None)

    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)
    run.run_targets(["repo-standards", "validate"], ctx)

    for cmd in calls:
        assert "--apply" not in " ".join(cmd)


def test_failure_prints_fix(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["inventory"], ctx)
    assert "check 'inventory' failed" in str(exc_info.value)
    assert "Repair:" in str(exc_info.value) and "inventory" in str(exc_info.value)
    assert "Recheck:" in str(exc_info.value) and "--check" in str(exc_info.value)
    assert exc_info.value.exit_code == 1


def test_lint_apply_only_repairs_lint_findings(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="apply", base_ref="origin/main", verbose=False)
    run.run_targets(["lint"], ctx)

    check_cmd = [c for c in calls if c[1:4] == ["-m", "ruff", "check"]]
    assert check_cmd
    assert "--fix" in check_cmd[0]
    assert not [c for c in calls if c[1:4] == ["-m", "ruff", "format"]]


def test_lint_check_mode_runs_changed_line_lint_without_formatting(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="check", base_ref="origin/main", verbose=False)
    run.run_targets(["lint"], ctx)

    assert any("ruff_diff.py" in " ".join(command) for command in calls)
    assert not [c for c in calls if c[1:3] == ["-m", "ruff", "format"]]


def test_base_ref_forwards_to_ruff_diff(monkeypatch):
    files = [Path("tools/run.py")]
    monkeypatch.setattr(run, "_changed_python_files", lambda base: files)

    calls = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)

    ctx = run.Ctx(mode="check", base_ref="custom/base", verbose=False)
    run.run_targets(["lint"], ctx)

    diff_cmd = [c for c in calls if "tools/ruff_diff.py" in " ".join(c)]
    assert diff_cmd
    assert "--changed-from" in diff_cmd[0]
    assert "custom/base" in diff_cmd[0]


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash not available")
def test_bash_wrapper_delegates_to_runpy():
    result = subprocess.run(
        ["bash", "-lc", "./tools/run --help"],
        cwd=ROOT,
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


def test_check_only_tasks_reject_apply_before_work():
    from pathlib import Path
    import importlib.util

    RUN_SPEC = importlib.util.spec_from_file_location("run", str(Path("tools/run.py").resolve()))
    run = importlib.util.module_from_spec(RUN_SPEC)
    RUN_SPEC.loader.exec_module(run)

    for name, task in run._TASKS.items():
        if task.check and not task.apply and name not in {"ci", "all"}:
            with pytest.raises(ValueError, match="does not support --apply"):
                run._validate_invocation([name], run.Ctx("apply", None, False), diagnostics=False)


def test_validate_fix_message(monkeypatch):
    def boom(cmd, ctx):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(run, "_run", boom)

    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)
    with pytest.raises(run.RunnerError) as exc_info:
        run.run_targets(["validate"], ctx)
    assert "check 'validate' failed" in str(exc_info.value)
    assert "No automatic repair is available for validate" in str(exc_info.value)
    assert "Recheck:" in str(exc_info.value)


def test_ci_apply_does_not_run_manual_review_preflight(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd, ctx):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)
    monkeypatch.setattr(run, "_check_tracked_line_endings", lambda: None)

    ctx = run.Ctx(mode="apply", base_ref=None, verbose=False)
    run.run_targets(run.resolve_targets(["ci"]), ctx)

    assert not any(command[:2] == [sys.executable, "tools/review_preflight.py"] for command in calls)


def test_validate_does_not_call_git_diff_exit_code(monkeypatch):
    calls = []

    def fake_git_diff_exit_code(ctx):
        calls.append("git_diff_exit_code")

    monkeypatch.setattr(run, "_git_diff_exit_code", fake_git_diff_exit_code)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_check_tracked_line_endings", lambda: None)
    monkeypatch.setattr(run, "_run", lambda cmd, ctx: None)

    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)
    run._run_validate(ctx)

    assert "git_diff_exit_code" not in calls


@pytest.mark.parametrize("target", [("validate",), ("ci",)])
def test_validation_targets_run_the_focused_markdown_link_validator(monkeypatch, target):
    calls = []

    def fake_run(cmd, ctx, *, env=None):
        calls.append(cmd)

    monkeypatch.setattr(run, "_run", fake_run)
    monkeypatch.setattr(run, "_git_diff_check", lambda ctx: None)
    monkeypatch.setattr(run, "_git_diff_exit_code", lambda ctx: None)
    monkeypatch.setattr(run, "_check_tracked_line_endings", lambda: None)

    ctx = run.Ctx(mode="check", base_ref=None, verbose=False)
    run.run_targets(list(target), ctx)

    assert [sys.executable, "tools/validate_markdown_links.py", "--check"] in calls


def _run_rendered_command(command: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    if sys.platform == "win32":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        assert shell is not None
        return subprocess.run([shell, "-NoProfile", "-Command", command], cwd=cwd, capture_output=True, text=True)
    import shlex

    return subprocess.run(shlex.split(command), cwd=cwd, capture_output=True, text=True)


def _bus_fixture(root: Path) -> Path:
    repo = root / "bus fixture"
    (repo / "tools").mkdir(parents=True)
    shutil.copyfile(ROOT / "tools" / "run.py", repo / "tools" / "run.py")
    shutil.copyfile(ROOT / "tools" / "ruff_diff.py", repo / "tools" / "ruff_diff.py")
    shutil.copyfile(ROOT / "pyproject.toml", repo / "pyproject.toml")
    env = _fixture_env()
    subprocess.run(["git", "init", "--quiet"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "config", "user.name", "Bus Test"], cwd=repo, env=env, check=True)
    subprocess.run(["git", "config", "user.email", "bus-test@example.invalid"], cwd=repo, env=env, check=True)
    (repo / "tools/run.py").write_text((ROOT / "tools/run.py").read_text(encoding="utf-8"), encoding="utf-8")
    (repo / "notes file.txt").write_bytes(b"line one\nline two\n")
    (repo / "unselected.txt").write_bytes(b"stay\n")
    subprocess.run(["git", "add", "."], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "--quiet", "-m", "fixture"], cwd=repo, env=env, check=True, capture_output=True)
    return repo


def _hint(stderr: str, label: str) -> str:
    return next(line.removeprefix(f"{label}: ") for line in stderr.splitlines() if line.startswith(f"{label}: "))


def test_inventory_repair_hint_runs_the_bus_entrypoint_and_rechecks_only_inventory(tmp_path: Path):
    repo = _bus_fixture(tmp_path)
    shutil.copyfile(ROOT / "tools" / "run.py", repo / "tools" / "_bus_source.py")
    (repo / "inventory.txt").write_text("stale\n", encoding="utf-8")
    (repo / "tools" / "run.py").write_text(
        "from dataclasses import replace\n"
        "import importlib.util\n"
        "from pathlib import Path\n"
        "import sys\n"
        "spec = importlib.util.spec_from_file_location('bus', Path(__file__).with_name('_bus_source.py'))\n"
        "bus = importlib.util.module_from_spec(spec)\n"
        "sys.modules[spec.name] = bus\n"
        "spec.loader.exec_module(bus)\n"
        "state = bus.ROOT / 'inventory.txt'\n"
        "def check(ctx):\n"
        "    if state.read_text(encoding='utf-8') != 'current\\n':\n"
        "        raise __import__('subprocess').CalledProcessError(1, ['inventory-check', '--check'])\n"
        "def apply(ctx):\n"
        "    state.write_text('current\\n', encoding='utf-8')\n"
        "bus._TASKS['inventory'] = replace(bus._TASKS['inventory'], check=(check,), apply=(apply,))\n"
        "raise SystemExit(bus.main())\n",
        encoding="utf-8",
    )
    env = _fixture_env()
    subprocess.run(
        ["git", "add", "inventory.txt", "tools/run.py", "tools/_bus_source.py"], cwd=repo, env=env, check=True
    )

    failed = subprocess.run(
        [sys.executable, str(repo / "tools/run.py"), "inventory", "--check"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )

    assert failed.returncode == 1
    assert "inventory-check" in failed.stderr
    repair = _hint(failed.stderr, "Repair")
    recheck = _hint(failed.stderr, "Recheck")
    assert "inventory" in repair and "--apply" in repair
    repaired = _run_rendered_command(repair, repo)
    assert repaired.returncode == 0, repaired.stdout + repaired.stderr
    checked = _run_rendered_command(recheck, repo)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert (repo / "inventory.txt").read_text(encoding="utf-8") == "current\n"
    assert not (repo / "expensive marker.txt").exists()


def test_format_repair_and_recheck_commands_touch_only_selected_spaced_path(tmp_path: Path):
    repo = _bus_fixture(tmp_path)
    selected = repo / "notes file.py"
    selected.write_text('value={"a":1}\n', encoding="utf-8")
    unselected = repo / "unselected.py"
    unselected.write_text('value={"b":2}\n', encoding="utf-8")
    subprocess.run(["git", "add", "notes file.py", "unselected.py"], cwd=repo, check=True)
    copied_bus = repo / "tools/run.py"

    failed = subprocess.run(
        [sys.executable, str(copied_bus), "format", "--check", "--files", "notes file.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )

    assert failed.returncode == 1
    repair = _hint(failed.stderr, "Repair")
    recheck = _hint(failed.stderr, "Recheck")
    assert "notes file.py" in repair and "--apply" in repair
    assert "notes file.py" in recheck and "--check" in recheck
    repaired = _run_rendered_command(repair, repo)
    assert repaired.returncode == 0, repaired.stdout + repaired.stderr
    checked = _run_rendered_command(recheck, repo)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert selected.read_text(encoding="utf-8") == 'value = {"a": 1}\n'
    assert unselected.read_text(encoding="utf-8") == 'value={"b":2}\n'


def test_normalize_repair_and_recheck_preserve_newline_count_and_scope(tmp_path: Path):
    repo = _bus_fixture(tmp_path)
    selected = repo / "notes file.txt"
    selected.write_bytes(b"one\r\ntwo\r\n")
    unselected = repo / "unselected.txt"
    unselected.write_bytes(b"keep\r\n")
    subprocess.run(["git", "add", "notes file.txt", "unselected.txt"], cwd=repo, check=True)

    failed = subprocess.run(
        [sys.executable, str(repo / "tools/run.py"), "normalize", "--check", "--files", "notes file.txt"],
        cwd=repo,
        capture_output=True,
        text=True,
    )

    assert failed.returncode == 1
    repair = _hint(failed.stderr, "Repair")
    recheck = _hint(failed.stderr, "Recheck")
    assert "notes file.txt" in repair and "--apply" in repair
    repaired = _run_rendered_command(repair, repo)
    assert repaired.returncode == 0, repaired.stdout + repaired.stderr
    checked = _run_rendered_command(recheck, repo)
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert selected.read_bytes() == b"one\ntwo\n"
    assert unselected.read_bytes() == b"keep\r\n"


def test_staged_lint_candidate_ignores_an_unstaged_repair(tmp_path: Path):
    source = _bus_fixture(tmp_path)
    candidate_file = source / "sample.py"
    candidate_file.write_text("def check():\n    return undefined_name\n", encoding="utf-8")
    subprocess.run(["git", "add", "sample.py"], cwd=source, check=True)
    staged_tree = subprocess.run(
        ["git", "write-tree"], cwd=source, capture_output=True, text=True, check=True
    ).stdout.strip()
    candidate_file.write_text('def check():\n    return "repaired only in worktree"\n', encoding="utf-8")
    candidate = tmp_path / "isolated gate candidate"
    subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout", str(source), str(candidate)], check=True)
    parent = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "-C", str(candidate), "update-ref", "--no-deref", "HEAD", parent], check=True)
    subprocess.run(["git", "-C", str(candidate), "update-ref", "refs/remotes/origin/main", parent], check=True)
    subprocess.run(["git", "-C", str(candidate), "read-tree", staged_tree], check=True)
    subprocess.run(["git", "-C", str(candidate), "checkout-index", "--all", "--force"], check=True)
    env = _fixture_env()
    env["REPO_STANDARDS_STAGED_SNAPSHOT"] = "1"

    result = subprocess.run(
        [sys.executable, str(candidate / "tools" / "run.py"), "lint", "--check", "--base-ref", "origin/main"],
        cwd=candidate,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1, result.stdout + result.stderr
    assert "undefined_name" in result.stdout
    assert candidate_file.read_text(encoding="utf-8").endswith('return "repaired only in worktree"\n')


def test_scope_validation_help_and_failed_python_launch_are_clear(tmp_path: Path, monkeypatch, capsys):
    assert run.main(["lint", "--help"]) == 0
    help_text = capsys.readouterr().out
    assert "Supported modes" in help_text and "Side effects" in help_text and "--files" in help_text
    assert run.main(["tests-build", "--apply"]) == 2
    assert "does not support --apply" in capsys.readouterr().err
    outside = tmp_path / "outside.py"
    outside.write_text("pass\n", encoding="utf-8")
    assert run.main(["lint", "--check", "--files", str(outside)]) == 2
    assert "outside the repository" in capsys.readouterr().err
    binary = ROOT / "tests" / "repository" / "binary normalization fixture.bin"
    binary.write_bytes(b"\x00\xff")
    try:
        assert run.main(["normalize", "--check", "--files", str(binary)]) == 2
        assert "binary" in capsys.readouterr().err
    finally:
        binary.unlink(missing_ok=True)

    def fail_to_launch(*args, **kwargs):
        raise OSError("python interpreter unavailable")

    monkeypatch.setattr(run.subprocess, "run", fail_to_launch)
    with pytest.raises(run.RunnerError) as exc_info:
        run._run_steps(
            "inventory", run._TASKS["inventory"], run._TASKS["inventory"].check, run.Ctx("check", None, False)
        )
    assert exc_info.value.exit_code == 2
    assert "inventory" in str(exc_info.value)
    assert "Recheck:" in str(exc_info.value)
    assert "Could not start command" in str(exc_info.value)
    assert "Failed command:" in str(exc_info.value)


@pytest.mark.parametrize("target", ["repo-index", "mesh", "index-mesh"])
def test_retired_index_targets_are_rejected(target: str) -> None:
    with pytest.raises(ValueError, match="unknown target"):
        run.resolve_targets([target])


@pytest.mark.parametrize("target", ["installed-skills", "refresh-skills"])
def test_retired_skill_projection_targets_are_rejected(target: str) -> None:
    with pytest.raises(ValueError, match="unknown target"):
        run.resolve_targets([target])


@pytest.mark.parametrize("phase", ["inventory", "project", "shared-references", "all"])
def test_marketplace_validator_retains_non_index_phases(phase: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_marketplace.py"), "--phase", phase],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_marketplace_validator_rejects_retired_index_phase() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_marketplace.py"), "--phase", "index"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "invalid choice" in result.stderr
