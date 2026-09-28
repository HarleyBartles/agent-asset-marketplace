import json
import importlib.util
import subprocess
import sys
from pathlib import Path
import pytest
from repo_standards_test_support import _create_worktree, _init_git_repo, _init_git_repo_with_commit, _stripped_env


REPO_ROOT = Path(__file__).resolve().parents[1]

SKILL_ROOT = REPO_ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills" / "repo-shape" / "scripts"

SCAFFOLD_CONTRIBUTING = SKILL_ROOT / "scaffold_contributing.py"

REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"

SCAFFOLD_MARKDOWN_FORMATTING = SKILL_ROOT / "scaffold_markdown_formatting.py"

sys.path.insert(0, str(SKILL_ROOT))

_SPEC = importlib.util.spec_from_file_location("repo_standards_under_test", REPO_STANDARDS)

repo_standards = importlib.util.module_from_spec(_SPEC)


_SPEC.loader.exec_module(repo_standards)


_MARKDOWN_SPEC = importlib.util.spec_from_file_location(
    "scaffold_markdown_formatting_under_test", SCAFFOLD_MARKDOWN_FORMATTING
)

scaffold_markdown_formatting = importlib.util.module_from_spec(_MARKDOWN_SPEC)


_MARKDOWN_SPEC.loader.exec_module(scaffold_markdown_formatting)


def test_pre_commit_hook_wired_to_ci_apply_and_diagnostics(tmp_path: Path) -> None:
    """repo-standards installs a pre-commit hook that runs ci --apply then ci --check --diagnostics."""
    repo = tmp_path / "precommit-check"
    repo.mkdir()
    _init_git_repo(repo)

    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-run\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )
    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","tools/run.py","ci","--apply"],'
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_STANDARDS),
            "--apply",
            "--yes",
            "--allow-shared-checkout",
        ],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    hook = repo / "githooks" / "pre-commit"
    assert hook.is_file(), "pre-commit hook was not installed"
    text = hook.read_text(encoding="utf-8")
    assert "repo-standards-commands.json" in text, text
    assert "run_declared apply" in text, text
    assert "run_declared check" in text, text
    assert "tools/run.py" not in text, text
    hooks_path = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert hooks_path == "githooks"


def test_tracked_hook_check_reports_missing_hook_and_hooks_path(tmp_path: Path) -> None:
    repo = tmp_path / "missing-tracked-hook"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    surface = {
        "id": "pre-commit-hook",
        "path": "githooks/pre-commit",
        "kind": "hook",
        "source": "templates/pre-commit",
    }

    findings = repo_standards._check_surface(repo, surface, set())

    assert "missing hook: githooks/pre-commit" in findings
    assert any("core.hooksPath" in finding for finding in findings)


def test_tracked_hook_check_accepts_clean_repo(tmp_path: Path) -> None:
    repo = tmp_path / "clean-tracked-hook"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)
    surface = {
        "id": "pre-commit-hook",
        "path": "githooks/pre-commit",
        "kind": "hook",
        "source": "templates/pre-commit",
    }

    assert repo_standards._check_surface(repo, surface, set()) == []


def test_tracked_hook_check_rejects_drift_and_wrong_hooks_path(tmp_path: Path) -> None:
    repo = tmp_path / "drifted-tracked-hook"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    hook = repo / "githooks" / "pre-commit"
    hook.parent.mkdir()
    hook.write_text("#!/usr/bin/env bash\nset -euo pipefail\nexit 0\n", encoding="utf-8")
    subprocess.run(["git", "config", "core.hooksPath", ".git/hooks"], cwd=repo, check=True)
    surface = {
        "id": "pre-commit-hook",
        "path": "githooks/pre-commit",
        "kind": "hook",
        "source": "templates/pre-commit",
    }

    findings = repo_standards._check_surface(repo, surface, set())

    assert any("canonical staged-snapshot contract" in finding for finding in findings)
    assert any("core.hooksPath" in finding for finding in findings)


def test_apply_migrates_legacy_private_hook_to_tracked_custody(tmp_path: Path) -> None:
    repo = tmp_path / "legacy-hook"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    legacy_hook = repo / ".git" / "hooks" / "pre-commit"
    legacy_hook.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    _install_repo_standards(repo)

    tracked_hook = repo / "githooks" / "pre-commit"
    assert tracked_hook.is_file()
    assert "run_declared apply" in tracked_hook.read_text(encoding="utf-8")
    assert (
        subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == "githooks"
    )
    assert legacy_hook.read_text(encoding="utf-8") == "#!/usr/bin/env bash\nexit 0\n"


def test_hooks_path_resolves_to_each_linked_worktree_tracked_directory(tmp_path: Path) -> None:
    repo = tmp_path / "worktree-hooks"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)
    subprocess.run(["git", "add", "githooks/pre-commit"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--no-verify", "-m", "track hook"], cwd=repo, check=True)
    worktree = _create_worktree(repo, "hook-worktree")

    main_resolved = Path(
        subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-path", "hooks"],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    worktree_resolved = Path(
        subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-path", "hooks"],
            cwd=worktree,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )

    assert main_resolved.resolve() == (repo / "githooks").resolve()
    assert worktree_resolved.resolve() == (worktree / "githooks").resolve()


def test_tracked_hook_platform_execution_contract(tmp_path: Path) -> None:
    repo = tmp_path / "platform-hook"
    repo.mkdir()
    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    template = Path(repo_standards.__file__).parent.parent / "templates" / "pre-commit"
    hook = repo / "pre-commit"
    hook.write_bytes(template.read_bytes())

    assert "pre-commit hook is not executable" in repo_standards._check_hook_contract(
        hook, repo, platform_name="posix", executable=False
    )
    assert "pre-commit hook is not executable" not in repo_standards._check_hook_contract(
        hook, repo, platform_name="posix", executable=True
    )

    hook.write_text(hook.read_text(encoding="utf-8").removeprefix("#!/usr/bin/env bash\n"), encoding="utf-8")
    assert "pre-commit hook has no shebang" in repo_standards._check_hook_contract(hook, repo, platform_name="nt")


def test_hosted_ci_executes_tracked_hook_without_private_copy() -> None:
    workflow = (REPO_ROOT / ".github" / "workflows" / "marketplace-validation.yml").read_text(encoding="utf-8")
    assert "githooks/pre-commit" in workflow
    assert "REPO_STANDARDS_HOSTED_COMMIT: HEAD" in workflow
    assert ".git/hooks" not in workflow


def test_hosted_hook_reconstructs_commit_as_staged_snapshot(tmp_path: Path) -> None:
    repo = tmp_path / "hosted-parity"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    retired = repo / "retired-plan.md"
    retired.write_text("completed\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "retired-plan.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--no-verify", "-m", "add completed plan"], cwd=repo, check=True)
    _install_repo_standards(repo)
    tools = repo / "tools"
    tools.mkdir(exist_ok=True)
    (tools / "run.py").write_text(
        """import os
import subprocess
import sys

if os.environ.get("REPO_STANDARDS_STAGED_SNAPSHOT") != "1":
    raise SystemExit("missing staged-snapshot marker")
changed = subprocess.run(
    ["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=True
).stdout.splitlines()
if "change.txt" not in changed:
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, check=True).stdout
    raise SystemExit(f"published change is not staged: {changed}; head={head}; status={status!r}")
if "--apply" in sys.argv or "--check" in sys.argv:
    raise SystemExit(0)
raise SystemExit(2)
""",
        encoding="utf-8",
        newline="\n",
    )
    (repo / "change.txt").write_text("published\n", encoding="utf-8", newline="\n")
    retired.unlink()
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--no-verify", "-m", "published change"], cwd=repo, check=True)
    published_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "checkout", "--detach", "HEAD"], cwd=repo, check=True, capture_output=True)
    result = subprocess.run(
        ["bash", "-c", "REPO_STANDARDS_HOSTED_COMMIT=HEAD githooks/pre-commit"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        subprocess.run(["git", "write-tree"], cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
        == published_tree
    )


def test_hosted_hook_refuses_to_rewrite_a_branch_checkout(tmp_path: Path) -> None:
    repo = tmp_path / "hosted-branch"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--no-verify", "-m", "install standards"], cwd=repo, check=True)

    result = subprocess.run(
        ["bash", "-c", "REPO_STANDARDS_HOSTED_COMMIT=HEAD githooks/pre-commit"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "requires a detached checkout" in result.stderr


def test_hook_validator_rejects_unbound_apply_and_check_switches(tmp_path: Path) -> None:
    repo = tmp_path / "unbound-hook"
    declaration = repo / ".agents" / "contracts"
    declaration.mkdir(parents=True)
    (declaration / "repo-standards-commands.json").write_text(
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    hook = repo / "pre-commit"
    hook.write_text(
        "#!/usr/bin/env bash\nset -euo pipefail\nsome-unrelated-tool --apply\nanother-tool --check\n",
        encoding="utf-8",
    )
    findings = repo_standards._check_hook_contract(hook, repo)
    assert "pre-commit hook must source the consumer command declaration" in findings
    assert "pre-commit hook must invoke the declared apply capability" in findings
    assert "pre-commit hook must invoke the declared check capability" in findings


def test_hook_validator_rejects_marker_bearing_but_incomplete_hook(tmp_path: Path) -> None:
    repo = tmp_path / "marker-only-hook"
    declaration = repo / ".agents" / "contracts"
    declaration.mkdir(parents=True)
    (declaration / "repo-standards-commands.json").write_text(
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    hook = repo / "pre-commit"
    hook.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        'COMMAND_DECLARATION="$REPO_ROOT/.agents/contracts/repo-standards-commands.json"\n'
        'required_switch="--apply"\n'
        "run_declared apply\n"
        "run_declared check\n",
        encoding="utf-8",
    )
    findings = repo_standards._check_hook_contract(hook, repo)
    assert any("canonical staged-snapshot contract" in finding for finding in findings)


def test_command_declaration_exposes_generated_paths(tmp_path: Path) -> None:
    path = tmp_path / ".agents" / "contracts" / "repo-standards-commands.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "apply": ["@python", "tools/run.py", "ci", "--apply"],
                "check": ["@python", "tools/run.py", "ci", "--check"],
                "generated_paths": [".agents/skills/**", "**/INDEX.md"],
            }
        ),
        encoding="utf-8",
    )
    declaration, findings = repo_standards._check_declared_commands(tmp_path)
    assert findings == []
    assert declaration is not None
    assert declaration.generated_paths == (".agents/skills/**", "**/INDEX.md")


@pytest.mark.parametrize(
    "generated_path",
    ["", "../outside", "/absolute", "C:/absolute", "*", "**", "./**", ":(top)**", "!ignored"],
)
def test_command_declaration_rejects_unsafe_generated_paths(tmp_path: Path, generated_path: str) -> None:
    path = tmp_path / ".agents" / "contracts" / "repo-standards-commands.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "apply": ["@python", "tools/run.py", "ci", "--apply"],
                "check": ["@python", "tools/run.py", "ci", "--check"],
                "generated_paths": [generated_path],
            }
        ),
        encoding="utf-8",
    )
    declaration, findings = repo_standards._check_declared_commands(tmp_path)
    assert declaration is None
    assert any("generated_paths" in finding for finding in findings)


def test_hook_rejects_inserted_control_flow() -> None:
    template = Path(repo_standards.__file__).parent.parent / "templates" / "pre-commit"
    text = template.read_text(encoding="utf-8")
    assert repo_standards._retains_canonical_hook_contract(text)
    for injected in ("exit 0", "set +e", "run_declared() { :; }"):
        altered = text.replace("run_declared apply", injected + "\nrun_declared apply", 1)
        assert not repo_standards._retains_canonical_hook_contract(altered)
    assert not repo_standards._retains_canonical_hook_contract("if false; then\n" + text + "\nfi\n")


def test_ordinary_apply_preserves_existing_customized_hook(tmp_path: Path) -> None:
    repo = tmp_path / "preserve-custom-hook"
    repo.mkdir()
    _init_git_repo(repo)
    template = Path(repo_standards.__file__).parent.parent / "templates" / "pre-commit"
    hook = repo / "githooks/pre-commit"
    hook.parent.mkdir(parents=True)
    customized = template.read_text(encoding="utf-8") + "\n# repository-owned audit note\n"
    hook.write_text(customized, encoding="utf-8", newline="\n")
    surface = {
        "id": "pre-commit-hook",
        "path": "githooks/pre-commit",
        "kind": "hook",
        "source": "templates/pre-commit",
    }

    assert not repo_standards._apply_surface(repo, surface, set(), False)
    assert hook.read_text(encoding="utf-8") == customized
    configured = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert configured == "githooks"


def _forbidden_ci_check_guidance() -> tuple[str, ...]:
    return (
        "re-run `tools/run.py ci --check`",
        "Run the repair command, then re-run `tools/run.py ci --check`",
        "re-run `py -3 tools/run.py ci --check`",
        "Run the repair command, then re-run `py -3 tools/run.py ci --check`",
        "run `py -3 tools/run.py ci --check` before",
        "run `tools/run.py ci --check` before",
        "re-run `ci --check`",
        "before pushing or flipping",
    )


_GATED_FILES = (
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "agent-operating-model"
    / "skills"
    / "repo-shape"
    / "references"
    / "ci-validation-pipeline.md",
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "agent-operating-model"
    / "skills"
    / "repo-shape"
    / "templates"
    / "pr.md",
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "agent-operating-model"
    / "skills"
    / "repo-shape"
    / "references"
    / "repository-shape-standard.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / ".agents" / "runbooks" / "pr.md",
    REPO_ROOT / ".agents" / "doctrine" / "tools.md",
    REPO_ROOT / ".agents" / "doctrine" / "plans.md",
    REPO_ROOT / ".agents" / "runbooks" / "planning.md",
    REPO_ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills" / "handoff-gates" / "SKILL.md",
    REPO_ROOT / "codex-marketplace" / "plugins" / "superpowers-plus" / "skills" / "publishing-source" / "SKILL.md",
)


def _fake_tools_run_py(behavior: str) -> str:
    return f"""import sys, os

BEHAVIOR = {behavior!r}

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def apply():
    if BEHAVIOR == "outside":
        os.makedirs(".agents/skills", exist_ok=True)
        write(".agents/skills/owned.txt", "generated")
        os.makedirs("build", exist_ok=True)
        write("build/outside.txt", "untracked")
    elif BEHAVIOR == "format-staged":
        write("source.py", "value = 1\\n")
    elif BEHAVIOR in ("broken", "ok"):
        pass
    print("OK apply")

def check():
    if BEHAVIOR == "broken":
        with open("broken.txt", "r", encoding="utf-8") as f:
            if "BAD" in f.read():
                fail("broken.txt is still broken")
    print("OK check")

if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    elif "--check" in sys.argv:
        check()
    else:
        print("OK")
"""


def _install_repo_standards(repo: Path) -> None:
    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-run\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )
    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True, exist_ok=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","tools/run.py","ci","--apply"],'
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", ".agents/contracts/repo-standards-commands.json"],
        cwd=repo,
        env=_stripped_env(),
        check=True,
        capture_output=True,
    )
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined


def test_pre_commit_hook_blocks_staged_broken_with_unstaged_fix(tmp_path: Path) -> None:
    """The hook materializes the index, so an unstaged fix cannot hide staged-broken content."""
    repo = tmp_path / "staged-broken"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("broken"), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py"], cwd=repo, env=_stripped_env(), check=True)

    # Staged content is broken; working tree has a fix that is not staged.
    broken = repo / "broken.txt"
    broken.write_text("BAD", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "broken.txt"], cwd=repo, env=_stripped_env(), check=True)
    broken.write_text("GOOD", encoding="utf-8", newline="\n")

    result = subprocess.run(
        ["git", "commit", "-m", "test staged broken"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    # The unstaged fix is restored after the failed validation.
    assert broken.read_text(encoding="utf-8").strip() == "GOOD"


def test_pre_commit_hook_preserves_unstaged_edits(tmp_path: Path) -> None:
    """The hook restores unstaged edits after running validation on the staged snapshot."""
    repo = tmp_path / "preserve-edits"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("ok"), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py"], cwd=repo, env=_stripped_env(), check=True)

    keep = repo / "keep.txt"
    keep.write_text("staged", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "keep.txt"], cwd=repo, env=_stripped_env(), check=True)
    keep.write_text("staged plus unstaged", encoding="utf-8", newline="\n")

    result = subprocess.run(
        ["git", "commit", "-m", "test preserve edits"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert keep.read_text(encoding="utf-8").strip() == "staged plus unstaged"


def test_pre_commit_hook_stages_apply_edits_to_already_staged_paths(tmp_path: Path) -> None:
    """Formatter-style apply edits belong in the candidate tree when their path was already staged."""
    repo = tmp_path / "stage-formatted-source"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("format-staged"), encoding="utf-8", newline="\n")
    source = repo / "source.py"
    source.write_text("value=1\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, env=_stripped_env(), check=True)

    result = subprocess.run(
        ["git", "commit", "-m", "test staged formatter output"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    committed = subprocess.run(
        ["git", "show", "HEAD:source.py"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert committed == "value = 1\n"


def test_pre_commit_hook_stages_only_owned_generated_surfaces(tmp_path: Path) -> None:
    """The hook stages allow-listed generated surfaces and fails on unexpected new files."""
    repo = tmp_path / "owned-staging"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("outside"), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py"], cwd=repo, env=_stripped_env(), check=True)

    base = repo / "base.txt"
    base.write_text("ok", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "base.txt"], cwd=repo, env=_stripped_env(), check=True)

    result = subprocess.run(
        ["git", "commit", "-m", "test owned staging"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout + result.stderr

    # Owned generated surface is staged; the unexpected file remains untracked.
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    ).stdout
    assert ".agents/skills/owned.txt" in staged, staged
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    ).stdout
    assert "build/outside.txt" in status, status


def test_pre_commit_hook_normalizes_crlf_generated_path_lines() -> None:
    """Windows Python may emit CRLF, so the Bash reader must remove the trailing CR."""
    template = Path(repo_standards.__file__).parent.parent / "templates" / "pre-commit"
    text = template.read_text(encoding="utf-8")
    read_loop = "while IFS= read -r generated_path; do\n"
    normalization = "  generated_path=\"${generated_path%$'\\r'}\"\n"
    assert read_loop + normalization in text


def test_pre_commit_hook_rejects_invalid_generated_pathspec_at_runtime(tmp_path: Path) -> None:
    repo = tmp_path / "invalid-generated-pathspec"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _install_repo_standards(repo)
    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools/run.py").write_text(_fake_tools_run_py("ok"), encoding="utf-8", newline="\n")
    declaration = repo / ".agents/contracts/repo-standards-commands.json"
    data = json.loads(declaration.read_text(encoding="utf-8"))
    data["generated_paths"] = [":(top)**"]
    declaration.write_text(json.dumps(data) + "\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py", str(declaration.relative_to(repo))], cwd=repo, check=True)

    result = subprocess.run(
        ["git", "commit", "-m", "reject unsafe generated path"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "invalid generated_paths entry" in result.stdout + result.stderr


def _add_marketplace_submodule(repo: Path, marketplace: Path) -> None:
    subprocess.run(
        [
            "git",
            "-c",
            "protocol.file.allow=always",
            "submodule",
            "add",
            str(marketplace),
            ".agents/plugins/marketplace-source",
        ],
        cwd=repo,
        env=_stripped_env(),
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--no-verify", "-m", "add marketplace submodule"],
        cwd=repo,
        env=_stripped_env(),
        check=True,
    )


def _install_repo_standards_with_submodule(repo: Path) -> None:
    exceptions = (
        "- marketplace-json\n"
        "- tools-run\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )
    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True, exist_ok=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","tools/run.py","ci","--apply"],'
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":[".agents/skills/**"]}\n',
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", ".agents/contracts/repo-standards-commands.json"],
        cwd=repo,
        env=_stripped_env(),
        check=True,
        capture_output=True,
    )
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined


def test_pre_commit_hook_rejects_dirty_submodule(tmp_path: Path) -> None:
    """The hook refuses to commit when a required marketplace submodule is dirty."""
    marketplace = tmp_path / "marketplace"
    marketplace.mkdir()
    _init_git_repo_with_commit(marketplace)

    repo = tmp_path / "consumer-dirty"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _add_marketplace_submodule(repo, marketplace)
    _install_repo_standards_with_submodule(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("ok"), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py"], cwd=repo, env=_stripped_env(), check=True)

    (repo / ".agents" / "plugins" / "marketplace-source" / "dirty.txt").write_text(
        "dirty", encoding="utf-8", newline="\n"
    )

    result = subprocess.run(
        ["git", "commit", "-m", "test dirty submodule"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "submodule source does not match" in (result.stdout + result.stderr)


def test_pre_commit_hook_rejects_wrong_head_submodule(tmp_path: Path) -> None:
    """The hook refuses to commit when a required marketplace submodule is at the wrong commit."""
    marketplace = tmp_path / "marketplace"
    marketplace.mkdir()
    _init_git_repo_with_commit(marketplace)

    repo = tmp_path / "consumer-wrong-head"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    _add_marketplace_submodule(repo, marketplace)

    # Move the marketplace source forward without updating the superproject gitlink.
    (marketplace / "extra.txt").write_text("extra", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "extra.txt"], cwd=marketplace, env=_stripped_env(), check=True)
    subprocess.run(["git", "commit", "-m", "second"], cwd=marketplace, env=_stripped_env(), check=True)
    new_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=marketplace,
        env=_stripped_env(),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    _install_repo_standards_with_submodule(repo)

    (repo / "tools").mkdir(exist_ok=True)
    (repo / "tools" / "run.py").write_text(_fake_tools_run_py("ok"), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "tools/run.py"], cwd=repo, env=_stripped_env(), check=True)

    submodule = repo / ".agents" / "plugins" / "marketplace-source"
    subprocess.run(
        ["git", "-c", "protocol.file.allow=always", "fetch", "origin"],
        cwd=submodule,
        env=_stripped_env(),
        check=True,
    )
    subprocess.run(["git", "checkout", new_head], cwd=submodule, env=_stripped_env(), check=True)

    result = subprocess.run(
        ["git", "commit", "-m", "test wrong-head submodule"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "submodule source does not match" in (result.stdout + result.stderr)


def test_repo_standards_apply_refuses_missing_consumer_command_declaration(tmp_path: Path) -> None:
    repo = tmp_path / "missing-command-declaration"
    repo.mkdir()
    _init_git_repo_with_commit(repo)

    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-shared-checkout\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
        "- completed-artifacts-doctrine\n"
        "- retired-plans-completed-dir\n"
        "- retired-specs-completed-dir\n"
        "- retired-roadmaps-completed-dir\n"
    )
    policy_dir = repo / ".agents" / "doctrine"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode != 0, combined
    assert "missing consumer command declaration" in combined
    assert not (repo / "githooks" / "pre-commit").exists()


def test_repo_standards_refuses_asymmetric_command_declaration_exception(tmp_path: Path) -> None:
    repo = tmp_path / "except-command-only"
    repo.mkdir()
    _init_git_repo_with_commit(repo)

    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- repo-standards-commands\n"
        "- tools-shared-checkout\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
        "- completed-artifacts-doctrine\n"
        "- retired-plans-completed-dir\n"
        "- retired-specs-completed-dir\n"
        "- retired-roadmaps-completed-dir\n"
    )
    policy_dir = repo / ".agents" / "doctrine"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode != 0, combined
    assert "pre-commit-hook requires repo-standards-commands" in combined
    assert not (repo / "githooks" / "pre-commit").exists()
