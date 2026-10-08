from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "githooks" / "pre-commit"
ADAPTER = ROOT / "tools" / "hook_gate_adapter.sh"


def _env(**overrides: str) -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    env.update(overrides)
    return env


def _git(repo: Path, *args: str, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
        env=env or _env(),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def _run_hook(repo: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    if os.name == "nt":
        git = Path(shutil.which("git") or "git")
        bash = next(
            (parent / "bin" / "bash.exe" for parent in git.parents if (parent / "bin" / "bash.exe").is_file()),
            Path(shutil.which("bash") or "bash"),
        )
    else:
        bash = Path(shutil.which("bash") or "bash")
    return subprocess.run(
        [str(bash), "githooks/pre-commit"],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _setup_repo(tmp_path: Path, *, reject: bool = False) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "--quiet")
    _git(repo, "config", "user.name", "Hook Test")
    _git(repo, "config", "user.email", "hook-test@example.invalid")
    _git(repo, "config", "core.autocrlf", "false")
    (repo / "selected.txt").write_text("base selected\n", encoding="utf-8")
    (repo / "unrelated.txt").write_text("base unrelated\n", encoding="utf-8")
    (repo / ".gitignore").write_text("build/\n", encoding="utf-8")
    if reject:
        (repo / "reject-gate.txt").write_text("reject\n", encoding="utf-8")
    tools = repo / "tools"
    tools.mkdir()
    shutil.copyfile(ADAPTER, tools / "hook_gate_adapter.sh")
    (tools / "run.py").write_text(
        "import os, subprocess, sys\n"
        "from pathlib import Path\n"
        "if sys.argv[1:] != ['ci', '--check']:\n"
        "    raise SystemExit(2)\n"
        "root = Path.cwd()\n"
        "trace = os.environ.get('HOOK_GATE_TRACE')\n"
        "if trace:\n"
        "    tree = subprocess.check_output(['git', 'write-tree'], text=True).strip()\n"
        "    with open(trace, 'a', encoding='utf-8') as stream: stream.write(tree + '\\n')\n"
        "if (root / 'mutate-gate.txt').exists():\n"
        "    (root / 'selected.txt').write_text('corruption\\n', encoding='utf-8')\n"
        "    subprocess.run(['git', 'add', '--', 'selected.txt'], check=True)\n"
        "    print('candidate mutation detected by gate adapter', file=sys.stderr)\n"
        "    raise SystemExit(17 if (root / 'reject-gate.txt').exists() else 0)\n"
        "if (root / 'reject-gate.txt').exists():\n"
        "    print('cheap repository check failed', file=sys.stderr)\n"
        "    print('Repair: py -3 tools/run.py format --apply --files selected.txt', file=sys.stderr)\n"
        "    print('Recheck: py -3 tools/run.py format --check --files selected.txt', file=sys.stderr)\n"
        "    raise SystemExit(17)\n"
        "if (root / 'build-gate.txt').exists():\n"
        "    (root / 'build').mkdir(exist_ok=True)\n"
        "    (root / 'build' / 'report.txt').write_text('disposable output\\n', encoding='utf-8')\n"
        "expensive = os.environ.get('HOOK_GATE_EXPENSIVE')\n"
        "if expensive:\n"
        "    with open(expensive, 'a', encoding='utf-8') as stream: stream.write('started\\n')\n",
        encoding="utf-8",
    )
    contracts = repo / ".agents" / "contracts"
    contracts.mkdir(parents=True)
    (contracts / "repo-standards-commands.json").write_text(
        json.dumps({"check": [["@python", "tools/run.py", "ci", "--check"]]}),
        encoding="utf-8",
    )
    hooks = repo / "githooks"
    hooks.mkdir()
    shutil.copyfile(HOOK, hooks / "pre-commit")
    if os.name != "nt":
        (hooks / "pre-commit").chmod(0o755)
    _git(repo, "add", ".")
    _git(repo, "commit", "--quiet", "-m", "fixture base")
    _git(repo, "config", "core.hooksPath", "githooks")
    return repo


def test_path_limited_commit_checks_the_temporary_candidate_and_preserves_separate_staged_work(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    observations = tmp_path / "observed trees.txt"
    expensive = tmp_path / "expensive marker.txt"
    env = _env(HOOK_GATE_TRACE=str(observations), HOOK_GATE_EXPENSIVE=str(expensive))
    (repo / "unrelated.txt").write_text("separately staged\n", encoding="utf-8")
    _git(repo, "add", "unrelated.txt", env=env)
    (repo / "selected.txt").write_text("path-limited candidate\n", encoding="utf-8")

    result = subprocess.run(
        ["git", "commit", "--only", "-m", "commit selected path", "--", "selected.txt"],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    committed_tree = _git(repo, "rev-parse", "HEAD^{tree}")
    assert observations.read_text(encoding="utf-8").splitlines() == [committed_tree]
    assert _git(repo, "show", "HEAD:selected.txt") == "path-limited candidate"
    assert _git(repo, "show", "HEAD:unrelated.txt") == "base unrelated"
    assert _git(repo, "show", ":unrelated.txt") == "separately staged"
    assert expensive.read_text(encoding="utf-8").splitlines() == ["started"]


def test_local_and_hosted_gates_fail_fast_on_the_same_candidate(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path, reject=True)
    observations = tmp_path / "observed candidate trees.txt"
    expensive = tmp_path / "expensive marker.txt"
    env = _env(HOOK_GATE_TRACE=str(observations), HOOK_GATE_EXPENSIVE=str(expensive))
    (repo / "candidate.txt").write_text("candidate content\n", encoding="utf-8")
    _git(repo, "add", "candidate.txt", env=env)
    candidate_tree = _git(repo, "write-tree", env=env)

    local = _run_hook(repo, env)

    assert local.returncode == 17, local.stdout + local.stderr
    assert "cheap repository check failed" in local.stderr
    assert "Repair: py -3 tools/run.py format --apply --files selected.txt" in local.stderr
    assert "Recheck: py -3 tools/run.py format --check --files selected.txt" in local.stderr
    assert _git(repo, "write-tree") == candidate_tree
    assert _git(repo, "show", ":candidate.txt") == "candidate content"
    assert observations.read_text(encoding="utf-8").splitlines() == [candidate_tree]
    assert not expensive.exists()

    _git(repo, "-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", "record rejected candidate", env=env)
    head = _git(repo, "rev-parse", "HEAD", env=env)
    _git(repo, "checkout", "--quiet", "--detach", head, env=env)
    hosted_env = _env(**{**env, "REPO_STANDARDS_HOSTED_COMMIT": head})
    hosted = _run_hook(repo, hosted_env)

    assert hosted.returncode == 17, hosted.stdout + hosted.stderr
    assert "cheap repository check failed" in hosted.stderr
    assert observations.read_text(encoding="utf-8").splitlines() == [candidate_tree, candidate_tree]
    assert not expensive.exists()


@pytest.mark.parametrize("reject", [False, True])
def test_candidate_owned_bus_mutations_cannot_change_author_state(tmp_path: Path, reject: bool) -> None:
    repo = _setup_repo(tmp_path, reject=reject)
    ignored = repo / ".cache" / "protected ignored.txt"
    (repo / ".git" / "info" / "exclude").write_text(".cache/\n", encoding="utf-8")
    ignored.parent.mkdir()
    ignored.write_text("keep ignored bytes", encoding="utf-8")
    untracked = repo / "untracked file.txt"
    untracked.write_text("keep untracked bytes", encoding="utf-8")
    selected = repo / "selected.txt"
    selected.write_text("staged candidate\n", encoding="utf-8")
    (repo / "mutate-gate.txt").write_text("mutate\n", encoding="utf-8")
    _git(repo, "add", "selected.txt", "mutate-gate.txt")
    candidate_tree = _git(repo, "write-tree")
    selected.write_text("unstaged author repair\n", encoding="utf-8")
    scratch = tmp_path / "_agent-scratch" / "repo"
    hook_env = _env(HOOK_GATE_TRACE=str(tmp_path / "mutations.txt"))
    result = _run_hook(repo, hook_env)

    assert result.returncode == (17 if reject else 1), result.stdout + result.stderr
    assert "changed the candidate index" in result.stderr.lower()
    assert _git(repo, "write-tree") == candidate_tree
    assert _git(repo, "show", ":selected.txt") == "staged candidate"
    assert selected.read_text(encoding="utf-8") == "unstaged author repair\n"
    assert untracked.read_text(encoding="utf-8") == "keep untracked bytes"
    assert ignored.read_text(encoding="utf-8") == "keep ignored bytes"
    assert list(scratch.iterdir()) == []


def test_root_hook_allows_disposable_ignored_build_output(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    (repo / "build-gate.txt").write_text("run build\n", encoding="utf-8")
    _git(repo, "add", "build-gate.txt")
    before_tree = _git(repo, "write-tree")

    result = _run_hook(repo, _env())

    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(repo, "write-tree") == before_tree
    assert not (repo / "build/report.txt").exists()


def test_staged_bus_script_is_used_instead_of_unstaged_replacement(tmp_path: Path) -> None:
    repo = _setup_repo(tmp_path)
    observed = tmp_path / "script version.txt"
    staged_script = (
        "import os\n"
        "with open(os.environ['HOOK_SCRIPT_VERSION'], 'a', encoding='utf-8') as stream: stream.write('staged\\n')\n"
    )
    unstaged_script = staged_script.replace("write('staged", "write('unstaged")
    script = repo / "tools" / "run.py"
    script.write_text(staged_script, encoding="utf-8")
    _git(repo, "add", "tools/run.py")
    script.write_text(unstaged_script, encoding="utf-8")
    env = _env(HOOK_SCRIPT_VERSION=str(observed))

    result = subprocess.run(
        ["git", "commit", "-m", "use staged bus"],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert observed.read_text(encoding="utf-8").splitlines() == ["staged"]
    assert _git(repo, "status", "--short") == "M tools/run.py"


@pytest.mark.parametrize("submodule_state", ["dirty", "head-drift", "uninitialized"])
def test_submodule_state_rejection_precedes_gate_without_repair_or_fetch(tmp_path: Path, submodule_state: str) -> None:
    repo = _setup_repo(tmp_path)
    module_source = tmp_path / "module source"
    module_source.mkdir()
    _git(module_source, "init", "--quiet")
    _git(module_source, "config", "user.name", "Module Test")
    _git(module_source, "config", "user.email", "module@example.invalid")
    (module_source / "module.txt").write_text("module base\n", encoding="utf-8")
    _git(module_source, "add", "module.txt")
    _git(module_source, "commit", "--quiet", "-m", "module base")
    submodule_add = subprocess.run(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "-C",
            str(repo),
            "submodule",
            "add",
            str(module_source),
            "modules/child",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert submodule_add.returncode == 0, submodule_add.stdout + submodule_add.stderr
    _git(repo, "-c", "core.hooksPath=disabled-hooks", "commit", "--quiet", "-m", "record module")
    child = repo / "modules" / "child"
    before_tree = _git(repo, "write-tree")
    trace = tmp_path / "submodule gate trace.txt"

    if submodule_state == "dirty":
        (child / "module.txt").write_text("dirty module bytes\n", encoding="utf-8")
    elif submodule_state == "head-drift":
        (child / "module.txt").write_text("second module commit\n", encoding="utf-8")
        _git(child, "add", "module.txt")
        _git(
            child,
            "-c",
            "user.name=Module Test",
            "-c",
            "user.email=module@example.invalid",
            "commit",
            "--quiet",
            "-m",
            "second module commit",
        )
    else:
        _git(repo, "submodule", "deinit", "--force", "--", "modules/child")

    result = _run_hook(repo, _env(HOOK_GATE_TRACE=str(trace)))

    assert result.returncode == 1, result.stdout + result.stderr
    assert "submodule" in result.stderr.lower()
    assert "modules/child" in result.stderr
    assert not trace.exists()
    assert _git(repo, "write-tree") == before_tree
    if submodule_state == "dirty":
        assert (child / "module.txt").read_text(encoding="utf-8") == "dirty module bytes\n"
    elif submodule_state == "head-drift":
        assert _git(child, "rev-parse", "HEAD") != _git(repo, "ls-tree", "HEAD", "modules/child").split()[2]
    else:
        assert not (child / "module.txt").exists()


@pytest.mark.parametrize("candidate_change", ["adapter-deletion", "invalid-contract"])
def test_staged_adapter_and_contract_changes_fail_closed_without_using_worktree_replacements(
    tmp_path: Path, candidate_change: str
) -> None:
    repo = _setup_repo(tmp_path)
    adapter = repo / "tools" / "hook_gate_adapter.sh"
    declaration = repo / ".agents" / "contracts" / "repo-standards-commands.json"
    trace = tmp_path / "staged contract trace.txt"

    if candidate_change == "adapter-deletion":
        adapter.unlink()
        _git(repo, "add", "tools/hook_gate_adapter.sh")
        adapter.write_text("run_repository_check_gate() { return 0; }\n", encoding="utf-8")
    else:
        declaration.write_text('{"check":[["@python","tools/run.py","ci","--apply"]]}\n', encoding="utf-8")
        _git(repo, "add", ".agents/contracts/repo-standards-commands.json")
        declaration.write_text('{"check":[["@python","tools/run.py","ci","--check"]]}\n', encoding="utf-8")
    candidate_tree = _git(repo, "write-tree")

    result = _run_hook(repo, _env(HOOK_GATE_TRACE=str(trace)))

    assert result.returncode == 2, result.stdout + result.stderr
    assert (
        "adapter" in result.stderr.lower()
        if candidate_change == "adapter-deletion"
        else "check must be exactly" in result.stderr
    )
    assert not trace.exists()
    assert _git(repo, "write-tree") == candidate_tree
    if candidate_change == "adapter-deletion":
        assert adapter.read_text(encoding="utf-8") == "run_repository_check_gate() { return 0; }\n"
        assert _git(repo, "ls-files", "--stage", "--", "tools/hook_gate_adapter.sh") == ""
    else:
        assert "--check" in declaration.read_text(encoding="utf-8")
        assert "--apply" in _git(repo, "show", ":.agents/contracts/repo-standards-commands.json")
