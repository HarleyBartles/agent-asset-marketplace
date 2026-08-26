import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    REPO_ROOT
    / "codex-marketplace"
    / "plugins"
    / "repo-worker-pack"
    / "skills"
    / "repo-standards"
    / "scripts"
)
SCAFFOLD_AGENTS_MD = SKILL_ROOT / "scaffold_agents_md.py"
SCAFFOLD_CONTRIBUTING = SKILL_ROOT / "scaffold_contributing.py"
SCAFFOLD_GITIGNORE = SKILL_ROOT / "scaffold_gitignore.py"
SCAFFOLD_MARKETPLACE_JSON = SKILL_ROOT / "scaffold_marketplace_json.py"
SCAFFOLD_REPO_RUNBOOK_POLICY = SKILL_ROOT / "scaffold_repo_runbook_policy.py"
REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _init_git_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True, capture_output=True)


def _init_git_repo_with_commit(path: Path) -> None:
    _init_git_repo(path)
    (path / "initial.txt").write_text("initial\n", encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", "initial.txt"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=path, check=True, capture_output=True)


def _create_worktree(repo: Path, name: str) -> Path:
    worktree = repo.parent / f"{repo.name}-{name}"
    subprocess.run(
        ["git", "worktree", "add", "-b", name, str(worktree), "HEAD"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    return worktree


def test_scaffold_agents_md_check_missing_fails(tmp_path: Path) -> None:
    """scaffold_agents_md --check fails when root AGENTS.md is missing."""
    repo = tmp_path / "no-agents"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_AGENTS_MD), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "DRIFT:" in result.stdout or "DRIFT:" in result.stderr


def test_scaffold_agents_md_creates_agents_md(tmp_path: Path) -> None:
    """scaffold_agents_md writes a router AGENTS.md scaffold when missing."""
    repo = tmp_path / "fresh-agents"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_AGENTS_MD)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    agents = repo / "AGENTS.md"
    assert agents.is_file()
    text = agents.read_text(encoding="utf-8")
    assert "## Repository purpose" in text
    assert "## Routing pointers" in text


def test_scaffold_agents_md_check_valid_passes(tmp_path: Path) -> None:
    """scaffold_agents_md --check passes for a valid router AGENTS.md."""
    repo = tmp_path / "valid-agents"
    repo.mkdir()
    _init_git_repo(repo)

    runbooks = repo / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    runbook_files = {
        "publication.md": "# Publication proof\n",
        "testing.md": "# Testing instructions\n",
        "code-style.md": "# Code style guidelines\n",
        "code-review.md": "# Review guidelines\n",
        "pr.md": "# PR instructions\n",
        "security.md": "# Security considerations\n",
    }
    for name, content in runbook_files.items():
        (runbooks / name).write_text(content, encoding="utf-8", newline="\n")
    (repo / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8", newline="\n")

    agents = repo / "AGENTS.md"
    agents.write_text(
        "# Repo\n\n"
        "## Repository purpose\n\nPurpose.\n\n"
        "## Source-of-truth split\n\nSplit.\n\n"
        "## Build and test commands\n\nCommands.\n\n"
        "## Routing pointers\n\n"
        "- [Repository purpose](AGENTS.md)\n"
        "- [Source-of-truth split](AGENTS.md)\n"
        "- [Publication proof](.agents/runbooks/publication.md)\n"
        "- [Build and test commands](AGENTS.md)\n"
        "- [Testing instructions](.agents/runbooks/testing.md)\n"
        "- [Code style guidelines](.agents/runbooks/code-style.md)\n"
        "- [Review guidelines](.agents/runbooks/code-review.md)\n"
        "- [PR instructions](.agents/runbooks/pr.md)\n"
        "- [Contributing](CONTRIBUTING.md)\n"
        "- [Security considerations](.agents/runbooks/security.md)\n"
        "- [Routing pointers](AGENTS.md)\n"
        "- [Maintenance responsibility](AGENTS.md)\n\n"
        "## Maintenance responsibility\n\nMaintainer.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_AGENTS_MD), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK" in result.stdout


def test_scaffold_agents_md_check_missing_core_section(tmp_path: Path) -> None:
    """scaffold_agents_md --check fails when a core section is missing."""
    repo = tmp_path / "bad-agents"
    repo.mkdir()
    _init_git_repo(repo)

    agents = repo / "AGENTS.md"
    agents.write_text(
        "# Repo\n\n"
        "## Repository purpose\n\nPurpose.\n\n"
        "## Source-of-truth split\n\nSplit.\n\n"
        "## Build and test commands\n\nCommands.\n\n"
        "## Maintenance responsibility\n\nMaintainer.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_AGENTS_MD), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "DRIFT:" in result.stdout or "DRIFT:" in result.stderr


def test_scaffold_agents_md_check_broken_routing_link(tmp_path: Path) -> None:
    """scaffold_agents_md --check fails when a routing pointer is broken."""
    repo = tmp_path / "broken-route"
    repo.mkdir()
    _init_git_repo(repo)

    agents = repo / "AGENTS.md"
    agents.write_text(
        "# Repo\n\n"
        "## Repository purpose\n\nPurpose.\n\n"
        "## Source-of-truth split\n\nSplit.\n\n"
        "## Build and test commands\n\nCommands.\n\n"
        "## Routing pointers\n\n"
        "- [Missing](missing.md)\n\n"
        "## Maintenance responsibility\n\nMaintainer.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_AGENTS_MD), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "broken link" in (result.stdout + result.stderr).lower()


def test_scaffold_marketplace_json_check_missing_fails(tmp_path: Path) -> None:
    """scaffold_marketplace_json --check fails when marketplace.json is missing."""
    repo = tmp_path / "no-marketplace"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKETPLACE_JSON), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "DRIFT:" in result.stdout or "DRIFT:" in result.stderr


def test_scaffold_marketplace_json_creates_minimal(tmp_path: Path) -> None:
    """scaffold_marketplace_json writes a minimal marketplace.json."""
    repo = tmp_path / "fresh-marketplace"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKETPLACE_JSON)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    marketplace = repo / ".agents" / "plugins" / "marketplace.json"
    assert marketplace.is_file()
    import json

    data = json.loads(marketplace.read_text(encoding="utf-8"))
    assert "repo" in data
    assert data["repo"]["local_skills"] == []


def test_scaffold_marketplace_json_migrates_legacy(tmp_path: Path) -> None:
    """scaffold_marketplace_json moves legacy top-level keys under repo."""
    import json

    repo = tmp_path / "legacy-marketplace"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / ".agents" / "plugins").mkdir(parents=True)
    marketplace = repo / ".agents" / "plugins" / "marketplace.json"
    marketplace.write_text(
        json.dumps(
            {
                "local_skill_prefixes": ["mark-"],
                "plugins": [{"name": "repo-worker-pack"}],
            }
        ),
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKETPLACE_JSON)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(marketplace.read_text(encoding="utf-8"))
    assert data["repo"]["local_skills"] == ["mark-"]
    assert data["plugins"] == [{"name": "repo-worker-pack"}]
    assert "local_skill_prefixes" not in data


def test_scaffold_marketplace_json_check_after_migration(tmp_path: Path) -> None:
    """scaffold_marketplace_json --check passes after a migration."""
    import json

    repo = tmp_path / "migrated-marketplace"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / ".agents" / "plugins").mkdir(parents=True)
    marketplace = repo / ".agents" / "plugins" / "marketplace.json"
    marketplace.write_text(
        json.dumps({"repo": {"local_skill_prefixes": ["mark-"]}, "plugins": []}),
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKETPLACE_JSON), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK" in result.stdout


def test_repo_standards_check_invalid_agents_md(tmp_path: Path) -> None:
    """repo_standards --check reports AGENTS.md router drift."""
    repo = tmp_path / "repo-standards-agents"
    repo.mkdir()
    _init_git_repo(repo)

    # Except all surfaces except root-agents-md so the test isolates AGENTS.md.
    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-run\n"
        "- pre-commit-hook\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
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

    (repo / "AGENTS.md").write_text(
        "# Repo\n\n## Repository purpose\n\nPurpose.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode != 0, combined
    assert "DRIFT:" in combined
    assert "AGENTS.md" in combined


def test_scaffold_contributing_check_missing_boilerplate_fails(tmp_path: Path) -> None:
    """scaffold_contributing --check fails when the file is missing required boilerplate."""
    repo = tmp_path / "bad-contributing"
    repo.mkdir()
    _init_git_repo(repo)

    (repo / "CONTRIBUTING.md").write_text("# Contributing\n\nNo skills here.\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_CONTRIBUTING), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "DRIFT: CONTRIBUTING.md" in result.stdout


def test_scaffold_repo_runbook_policy_check_missing_boilerplate_fails(tmp_path: Path) -> None:
    """scaffold_repo_runbook_policy --check fails when the file is missing required boilerplate."""
    repo = tmp_path / "bad-policy"
    repo.mkdir()
    _init_git_repo(repo)

    policy_path = repo / ".agents" / "docs" / "repo-runbook-policy.md"
    policy_path.parent.mkdir(parents=True)
    policy_path.write_text("# Repo Runbook Policy\n\nNo mapping.\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_REPO_RUNBOOK_POLICY), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "DRIFT: repo-runbook-policy.md" in result.stdout


def test_scaffold_gitignore_accepts_force_no_op(tmp_path: Path) -> None:
    """scaffold_gitignore --force is accepted as a uniform CLI no-op."""
    repo = tmp_path / "gitignore-force"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_GITIGNORE), "--force"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (repo / ".gitignore").is_file()


def test_scaffold_gitignore_check_no_stale_sdd_scaffold_passes(tmp_path: Path) -> None:
    """scaffold_gitignore --check passes when there is no stale sdd scaffold."""
    repo = tmp_path / "no-sdd-scaffold"
    repo.mkdir()
    _init_git_repo(repo)

    (repo / ".gitignore").write_text("", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_GITIGNORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK" in result.stdout


def test_scaffold_gitignore_check_stale_sdd_scaffold_fails(tmp_path: Path) -> None:
    """scaffold_gitignore --check fails when a stale in-repo sdd .gitignore exists."""
    repo = tmp_path / "stale-sdd-scaffold"
    repo.mkdir()
    _init_git_repo(repo)

    sdd_gitignore = repo / ".agents" / "superpowers" / "sdd" / ".gitignore"
    sdd_gitignore.parent.mkdir(parents=True)
    sdd_gitignore.write_text("*\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_GITIGNORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "DRIFT:" in combined
    assert ".agents/superpowers/sdd/.gitignore" in combined


def test_scaffold_gitignore_removes_stale_sdd_scaffold(tmp_path: Path) -> None:
    """scaffold_gitignore removes a stale in-repo sdd .gitignore and directory."""
    repo = tmp_path / "remove-sdd-scaffold"
    repo.mkdir()
    _init_git_repo(repo)

    sdd_gitignore = repo / ".agents" / "superpowers" / "sdd" / ".gitignore"
    sdd_gitignore.parent.mkdir(parents=True)
    sdd_gitignore.write_text("*\n!.gitignore\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_GITIGNORE)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not sdd_gitignore.is_file()
    assert not sdd_gitignore.parent.is_dir()


def test_scaffold_gitignore_check_stale_root_rule_fails(tmp_path: Path) -> None:
    """scaffold_gitignore --check fails when root .gitignore still has the old sdd rule."""
    repo = tmp_path / "stale-root-sdd-rule"
    repo.mkdir()
    _init_git_repo(repo)

    root_gitignore = repo / ".gitignore"
    root_gitignore.write_text(
        ".agents/superpowers/sdd/**\n!.agents/superpowers/sdd/.gitignore\n",
        encoding="utf-8",
        newline="\n",
    )

    sdd_gitignore = repo / ".agents" / "superpowers" / "sdd" / ".gitignore"
    sdd_gitignore.parent.mkdir(parents=True)
    sdd_gitignore.write_text("*\n!.gitignore\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_GITIGNORE), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "DRIFT:" in combined
    assert ".gitignore" in combined


def test_repo_standards_apply_force_overwrites_drifted_contributing(tmp_path: Path) -> None:
    """repo_standards --apply --yes --force overwrites a drifted scaffolded surface."""
    repo = tmp_path / "repo-standards-force"
    repo.mkdir()
    _init_git_repo(repo)

    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-run\n"
        "- pre-commit-hook\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )

    (repo / "CONTRIBUTING.md").write_text("# Contributing\n\nStale.\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--force", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    text = (repo / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "/repo-standards" in text
    assert "/repo-worker-base" in text


def test_scaffold_contributing_check_customized_passes(tmp_path: Path) -> None:
    """scaffold_contributing --check passes when only the heading and skill invocations are kept."""
    repo = tmp_path / "custom-contributing"
    repo.mkdir()
    _init_git_repo(repo)

    (repo / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n"
        "Our own contributor process.\n\n"
        "## Required skill invocations\n\n"
        "- `/repo-standards` for repo-shape and runbook routing.\n"
        "- `/repo-worker-base` for worktree, branch, validation, and publication boundaries.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_CONTRIBUTING), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK" in result.stdout


def test_repo_standards_allow_shared_checkout_combines_with_apply(tmp_path: Path) -> None:
    """repo_standards --apply --allow-shared-checkout works in the main shared checkout."""
    repo = tmp_path / "allow-apply"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo, check=True)

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    assert "--allow-shared-checkout supplied" in combined


def test_repo_standards_allow_shared_checkout_requires_apply(tmp_path: Path) -> None:
    """repo_standards --allow-shared-checkout requires --apply (not --check)."""
    repo = tmp_path / "allow-check"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--allow-shared-checkout", "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1, combined
    assert "--allow-shared-checkout requires --apply" in combined


def test_repo_standards_allow_shared_checkout_alone_requires_apply(tmp_path: Path) -> None:
    """repo_standards --allow-shared-checkout alone is rejected."""
    repo = tmp_path / "allow-alone"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--allow-shared-checkout"],
        cwd=repo,
        env=_stripped_env(),
        input="",
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1, combined
    assert "--allow-shared-checkout requires --apply" in combined


def test_repo_standards_apply_in_main_shared_checkout_requires_approval(tmp_path: Path) -> None:
    """repo_standards --apply in the main shared checkout fails without --allow-shared-checkout."""
    repo = tmp_path / "main-no-approval"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo, check=True)

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1, combined
    assert "Pass --allow-shared-checkout" in combined


def test_repo_standards_apply_in_shared_checkout_with_flag_succeeds(tmp_path: Path) -> None:
    """repo_standards --apply --allow-shared-checkout in a shared checkout applies changes."""
    repo = tmp_path / "shared-apply"
    repo.mkdir()
    _init_git_repo_with_commit(repo)

    exceptions = (
        "- marketplace-source-submodule\n"
        "- marketplace-json\n"
        "- tools-run\n"
        "- pre-commit-hook\n"
        "- repo-runbook-policy\n"
        "- runbooks-agents-md\n"
        "- review-entry\n"
        "- root-agents-md\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-runbook-policy.md").write_text(
        f"# Repo runbook policy\n\n## Exceptions\n\n{exceptions}",
        encoding="utf-8",
        newline="\n",
    )
    (repo / "CONTRIBUTING.md").write_text("# Contributing\n\nStale.\n", encoding="utf-8", newline="\n")

    # Commit files so worktree has them
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "setup"], cwd=repo, check=True, capture_output=True)

    worktree = _create_worktree(repo, "feature")

    # Write the stale file in the worktree too
    (worktree / "CONTRIBUTING.md").write_text("# Contributing\n\nStale.\n", encoding="utf-8", newline="\n")

    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--apply", "--yes", "--force", "--allow-shared-checkout"],
        cwd=worktree,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 0, combined
    text = (worktree / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert "/repo-standards" in text


def test_scaffold_repo_runbook_policy_check_customized_passes(tmp_path: Path) -> None:
    """scaffold_repo_runbook_policy --check passes when only the heading and required sections are kept."""
    repo = tmp_path / "custom-policy"
    repo.mkdir()
    _init_git_repo(repo)

    policy_path = repo / ".agents" / "doctrine" / "repo-runbook-policy.md"
    policy_path.parent.mkdir(parents=True)
    policy_path.write_text(
        "# Repo Runbook Policy\n\n"
        "This repository uses repo-standards.\n\n"
        "## Standard-to-local mapping\n\n"
        "| Standard runbook | Local path |\n|---|---|\n"
        "| code-review.md | `.agents/runbooks/code-review.md` |\n\n"
        "## Exceptions\n\n"
        "None.\n",
        encoding="utf-8",
        newline="\n",
    )

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_REPO_RUNBOOK_POLICY), "--check"],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK" in result.stdout


def test_pre_commit_hook_template_uses_apply_then_check(tmp_path: Path) -> None:
    """repo-standards installs a pre-commit hook that runs tools/run.py ci --apply."""
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
    hook = repo / ".git" / "hooks" / "pre-commit"
    assert hook.is_file(), "pre-commit hook was not installed"
    text = hook.read_text(encoding="utf-8")
    assert "tools/run.py ci --apply" in text, text
