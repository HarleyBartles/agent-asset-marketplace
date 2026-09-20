import os
import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "codex-marketplace" / "plugins" / "agent-operating-model" / "skills" / "repo-shape" / "scripts"
SCAFFOLD_AGENTS_MD = SKILL_ROOT / "scaffold_agents_md.py"
SCAFFOLD_CONTRIBUTING = SKILL_ROOT / "scaffold_contributing.py"
SCAFFOLD_GITIGNORE = SKILL_ROOT / "scaffold_gitignore.py"
SCAFFOLD_MARKETPLACE_JSON = SKILL_ROOT / "scaffold_marketplace_json.py"
SCAFFOLD_REPO_RUNBOOK_POLICY = SKILL_ROOT / "scaffold_repo_runbook_policy.py"
REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"
SCAFFOLD_RUNBOOKS = SKILL_ROOT / "scaffold_runbooks.py"
sys.path.insert(0, str(SKILL_ROOT))
_SPEC = importlib.util.spec_from_file_location("repo_standards_under_test", REPO_STANDARDS)
repo_standards = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(repo_standards)


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


def test_absent_surface_reports_tracked_completed_artifact_directory(tmp_path: Path) -> None:
    """A completed-artifact directory must be drift rather than a supported repo surface."""
    completed = tmp_path / ".agents" / "specs" / "completed"
    completed.mkdir(parents=True)
    findings = repo_standards._check_surface(
        tmp_path,
        {"id": "retired-specs", "path": ".agents/specs/completed", "kind": "absent"},
        set(),
    )
    assert findings == ["retired path remains: .agents/specs/completed"]


def test_runbook_scaffolds_bind_planning_artifact_lifecycle(tmp_path: Path) -> None:
    repo = tmp_path / "lifecycle-runbooks"
    repo.mkdir()
    _init_git_repo(repo)

    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_RUNBOOKS)],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    planning = (repo / ".agents" / "runbooks" / "planning.md").read_text(encoding="utf-8").lower()
    publication = (repo / ".agents" / "runbooks" / "pr.md").read_text(encoding="utf-8").lower()
    assert "completing-planning-artifacts" in planning
    assert "successor-slice" in planning
    assert "completing-planning-artifacts" in publication
    assert "completed-awaiting-retirement" in publication


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
    assert ".agents/runbooks/INDEX.md" in text
    assert ".agents/playbooks/INDEX.md" in text


def test_scaffold_agents_md_check_valid_passes(tmp_path: Path) -> None:
    """scaffold_agents_md --check passes for a valid router AGENTS.md."""
    repo = tmp_path / "valid-agents"
    repo.mkdir()
    _init_git_repo(repo)

    runbooks = repo / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    runbook_files = {
        "publication.md": "# Publication proof\n",
        "code-review.md": "# Review guidelines\n",
        "pr.md": "# PR instructions\n",
    }
    for name, content in runbook_files.items():
        (runbooks / name).write_text(content, encoding="utf-8", newline="\n")
    playbooks = repo / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    for name, content in {
        "testing.md": "# Testing instructions\n",
        "code-style.md": "# Code style guidelines\n",
        "security.md": "# Security considerations\n",
    }.items():
        (playbooks / name).write_text(content, encoding="utf-8", newline="\n")
    (runbooks / "INDEX.md").write_text("# Runbook inventory\n", encoding="utf-8", newline="\n")
    (playbooks / "INDEX.md").write_text("# Playbook inventory\n", encoding="utf-8", newline="\n")
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
        "- [Testing instructions](.agents/playbooks/testing.md)\n"
        "- [Code style guidelines](.agents/playbooks/code-style.md)\n"
        "- [Review guidelines](.agents/runbooks/code-review.md)\n"
        "- [PR instructions](.agents/runbooks/pr.md)\n"
        "- [Contributing](CONTRIBUTING.md)\n"
        "- [Security considerations](.agents/playbooks/security.md)\n"
        "- [Runbook inventory](.agents/runbooks/INDEX.md)\n"
        "- [Playbook inventory](.agents/playbooks/INDEX.md)\n"
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


def test_agents_router_requires_direct_runbook_and_playbook_inventory_links(tmp_path: Path) -> None:
    repo = tmp_path / "missing-workflow-inventories"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / "CONTRIBUTING.md").write_text("# Contributing\n", encoding="utf-8", newline="\n")
    for directory, title in (("runbooks", "Runbook inventory"), ("playbooks", "Playbook inventory")):
        path = repo / ".agents" / directory
        path.mkdir(parents=True)
        (path / "INDEX.md").write_text(f"# {title}\n", encoding="utf-8", newline="\n")

    agents = repo / "AGENTS.md"
    agents.write_text(
        "# Repo\n\n"
        "## Repository purpose\n\nPurpose.\n\n"
        "## Source-of-truth split\n\nSplit.\n\n"
        "## Build and test commands\n\nCommands.\n\n"
        "## Routing pointers\n\n"
        "- [Routing pointers](AGENTS.md)\n"
        "- [Contributing](CONTRIBUTING.md)\n\n"
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
    combined = result.stdout + result.stderr

    assert result.returncode != 0
    assert "AGENTS.md missing direct runbook inventory link: .agents/runbooks/INDEX.md" in combined
    assert "AGENTS.md missing direct playbook inventory link: .agents/playbooks/INDEX.md" in combined


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
    (repo / ".agents" / "skills" / "mark-example").mkdir(parents=True)
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
    assert data["repo"]["local_skills"] == ["mark-example"]
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
    assert result.returncode == 1, result.stdout + result.stderr
    assert "local_skill_prefixes" in result.stdout


def test_scaffold_marketplace_json_rejects_unresolved_legacy_prefix(tmp_path: Path) -> None:
    """Migration must not silently discard a prefix with no matching local skill."""
    import json

    repo = tmp_path / "unresolved-legacy-marketplace"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / ".agents" / "plugins").mkdir(parents=True)
    marketplace = repo / ".agents" / "plugins" / "marketplace.json"
    marketplace.write_text(
        json.dumps({"repo": {"local_skill_prefixes": ["missing-"]}, "plugins": []}),
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
    assert result.returncode == 1
    assert "no matching local skill directories" in result.stdout
    assert "Traceback" not in result.stderr


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
    policy_dir = repo / ".agents" / "doctrine"
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
    assert "using-superpowers-plus" in text
    assert "/using-superpowers-plus" not in text


def test_scaffold_contributing_check_customized_passes(tmp_path: Path) -> None:
    """scaffold_contributing --check passes with the heading and sole bootstrap route."""
    repo = tmp_path / "custom-contributing"
    repo.mkdir()
    _init_git_repo(repo)

    (repo / "CONTRIBUTING.md").write_text(
        "# Contributing\n\n"
        "Our own contributor process.\n\n"
        "## Workflow routing\n\n"
        "Invoke `using-superpowers-plus` once and follow its handoff.\n",
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

    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","tools/run.py","ci","--apply"],'
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":["generated/**"]}\n',
        encoding="utf-8",
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
    policy_dir = repo / ".agents" / "doctrine"
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
    assert "using-superpowers-plus" in text
    assert "/using-superpowers-plus" not in text


def test_scaffold_repo_runbook_policy_check_customized_passes(tmp_path: Path) -> None:
    """scaffold_repo_runbook_policy --check passes when only the heading and required sections are kept."""
    repo = tmp_path / "custom-policy"
    repo.mkdir()
    _init_git_repo(repo)

    policy_path = repo / ".agents" / "doctrine" / "repo-runbook-policy.md"
    policy_path.parent.mkdir(parents=True)
    policy_path.write_text(
        "# Repository Runbook and Playbook Policy\n\n"
        "This repository uses repo-standards.\n\n"
        "## Standard runbooks\n\n"
        "| Standard runbook | Local path |\n|---|---|\n"
        "| code-review.md | `.agents/runbooks/code-review.md` |\n\n"
        "## Standard playbooks\n\n"
        "| Standard playbook | Local path |\n|---|---|\n"
        "| testing.md | `.agents/playbooks/testing.md` |\n\n"
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


def test_scaffold_repo_runbook_policy_check_duplicate_playbook_classification_fails(
    tmp_path: Path,
) -> None:
    """A standard playbook cannot also be listed as repository-specific."""
    repo = tmp_path / "duplicate-playbook-policy"
    repo.mkdir()
    _init_git_repo(repo)

    policy_path = repo / ".agents" / "doctrine" / "repo-runbook-policy.md"
    policy_path.parent.mkdir(parents=True)
    policy_path.write_text(
        "# Repository Runbook and Playbook Policy\n\n"
        "## Standard runbooks\n\n"
        "| Standard runbook | Local path | Status |\n|---|---|---|\n"
        "| implementing.md | `.agents/runbooks/implementing.md` | required |\n\n"
        "## Standard playbooks\n\n"
        "| Standard playbook | Local path | Status |\n|---|---|---|\n"
        "| repo-doctrine.md | `.agents/playbooks/repo-doctrine.md` | optional |\n\n"
        "## Additional repository-specific playbooks\n\n"
        "- `repo-doctrine.md` exists because this repository authors doctrine.\n\n"
        "## Exceptions\n\nNone.\n",
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

    assert result.returncode != 0
    assert "repo-doctrine.md" in result.stdout
    assert "both standard and repository-specific" in result.stdout


def test_scaffold_repo_runbook_policy_check_linked_duplicate_playbook_fails(tmp_path: Path) -> None:
    """Markdown-linked repository-specific entries cannot duplicate standard playbooks."""
    repo = tmp_path / "linked-duplicate-playbook-policy"
    repo.mkdir()
    _init_git_repo(repo)

    policy_path = repo / ".agents" / "doctrine" / "repo-runbook-policy.md"
    policy_path.parent.mkdir(parents=True)
    policy_path.write_text(
        "# Repository Runbook and Playbook Policy\n\n"
        "## Standard runbooks\n\n"
        "| Standard runbook | Local path | Status |\n|---|---|---|\n"
        "| implementing.md | `.agents/runbooks/implementing.md` | required |\n\n"
        "## Standard playbooks\n\n"
        "| Standard playbook | Local path | Status |\n|---|---|---|\n"
        "| repo-doctrine.md | `.agents/playbooks/repo-doctrine.md` | optional |\n\n"
        "## Additional repository-specific playbooks\n\n"
        "- [Repo doctrine](../playbooks/repo-doctrine.md)\n\n"
        "## Exceptions\n\nNone.\n",
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

    assert result.returncode != 0
    assert "repo-doctrine.md" in result.stdout
    assert "both standard and repository-specific" in result.stdout


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
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":["generated/**"]}\n',
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
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":["generated/**"]}\n',
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
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":["generated/**"]}\n',
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
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":["generated/**"]}\n',
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
        '{"apply":["@python","consumer.py","--apply"],"check":["@python","consumer.py","--check"],"generated_paths":["generated/**"]}\n',
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


@pytest.mark.parametrize("generated_path", ["", "../outside", "/absolute", "C:/absolute", "**"])
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
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":["generated/**"]}\n',
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
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":["generated/**"]}\n',
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


def test_scaffold_runbooks_stub_is_stage_composition_root(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("scaffold_runbooks_under_test", SKILL_ROOT / "scaffold_runbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._runbook_content("implementing.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
        "## Playbook routing",
    ):
        assert heading in content
    assert "completing-plans.md" not in mod.RUNBOOK_TITLES


def test_scaffold_playbooks_stub_is_topical_composition(tmp_path: Path) -> None:
    spec = importlib.util.spec_from_file_location("scaffold_playbooks_under_test", SKILL_ROOT / "scaffold_playbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._playbook_content("testing.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
        "## Runbook routing",
    ):
        assert heading in content
    assert "testing.md" in mod.PLAYBOOK_TITLES


def test_code_style_playbook_template_teaches_ownership_boundaries() -> None:
    template = SKILL_ROOT.parent / "templates" / "code-style.md"
    text = template.read_text(encoding="utf-8")
    assert "Durable coding and architecture invariants belong in doctrine" in text
    assert "Reusable language and framework technique belongs in capability skills" in text
    assert "## Runbook routing" in text


def _composition_document(extra_heading: str, links: str = "") -> str:
    headings = (
        "When",
        "Required skills",
        "Composition",
        "Doctrine and contracts",
        "Local commands and paths",
        "Evidence contract",
        "Prohibited combinations",
    )
    body = "# Example\n\n" + "\n\n".join(f"## {heading}\n\n- defined" for heading in headings)
    return body + f"\n\n## {extra_heading}\n\n{links}\n"


def test_runbook_composition_reports_missing_required_sections(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\nLocal commands only.\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding and "Required skills" in finding for finding in findings)


def test_composition_graph_accepts_reciprocal_playbook_route(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(
        _composition_document("Playbook routing", "- [Testing](../playbooks/testing.md) - when tests change."),
        encoding="utf-8",
    )
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)"),
        encoding="utf-8",
    )
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_accepts_standalone_playbook(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(_composition_document("Playbook routing", "None."), encoding="utf-8")
    (playbooks / "testing.md").write_text(_composition_document("Runbook routing", "None."), encoding="utf-8")
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_rejects_nonreciprocal_edge(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text(
        _composition_document("Playbook routing", "- [Testing](../playbooks/testing.md)"), encoding="utf-8"
    )
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Review](../runbooks/code-review.md)"), encoding="utf-8"
    )
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("reciprocal" in finding for finding in findings)


def test_composition_graph_accepts_playbook_to_playbook_composition(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    playbooks = tmp_path / ".agents" / "playbooks"
    runbooks.mkdir(parents=True)
    playbooks.mkdir(parents=True)
    routing = "- [Testing](../playbooks/testing.md)\n- [Security](../playbooks/security.md)"
    (runbooks / "implementing.md").write_text(_composition_document("Playbook routing", routing), encoding="utf-8")
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "- [Implementation](../runbooks/implementing.md)"),
        encoding="utf-8",
    )
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_composition_graph_rejects_missing_playbook_composition_target(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )

    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("security.md" in finding and "does not resolve" in finding for finding in findings)


def test_composition_graph_rejects_playbook_composition_cycle(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Composition\n\n- defined",
            "## Composition\n\n- [Testing](testing.md)",
        ),
        encoding="utf-8",
    )

    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("composition cycle" in finding and "testing.md" in finding for finding in findings)


def test_composition_graph_ignores_playbook_links_outside_composition(tmp_path: Path) -> None:
    playbooks = tmp_path / ".agents" / "playbooks"
    playbooks.mkdir(parents=True)
    (playbooks / "testing.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Doctrine and contracts\n\n- defined",
            "## Doctrine and contracts\n\n- [Security](security.md)",
        ),
        encoding="utf-8",
    )
    (playbooks / "security.md").write_text(
        _composition_document("Runbook routing", "None.").replace(
            "## Doctrine and contracts\n\n- defined",
            "## Doctrine and contracts\n\n- [Testing](testing.md)",
        ),
        encoding="utf-8",
    )

    assert repo_standards._check_composition_graph(tmp_path) == []


def test_apply_fails_when_composition_graph_remains_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "implementing.md").write_text("# Implementation\n", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"version": 3, "surfaces": []}\n', encoding="utf-8")
    monkeypatch.setattr(repo_standards, "_repo_root", lambda: tmp_path)
    monkeypatch.setattr(repo_standards, "_manifest_path", lambda: manifest)
    monkeypatch.setattr(repo_standards, "_is_submodule", lambda _root: False)
    monkeypatch.setattr(repo_standards.shared_checkout, "approve_mutation", lambda *_args: True)

    assert repo_standards.main(["--apply", "--yes"]) == 1
    captured = capsys.readouterr()
    assert "unresolved composition-graph drift" in captured.err


def test_runbook_composition_ignores_agents_md_and_absent_dir(tmp_path: Path) -> None:
    assert repo_standards._check_composition_graph(tmp_path) == []
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "AGENTS.md").write_text("# Router\n", encoding="utf-8")
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_runbook_composition_ignores_generated_index(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "INDEX.md").write_text("# Index\n", encoding="utf-8")
    assert repo_standards._check_composition_graph(tmp_path) == []


def test_runbook_composition_warns_on_fenced_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n```markdown\n## Required skills\n```\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_runbook_composition_warns_on_commented_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n<!-- ## Required skills -->\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_runbook_composition_warns_on_extended_heading(tmp_path: Path) -> None:
    runbooks = tmp_path / ".agents" / "runbooks"
    runbooks.mkdir(parents=True)
    (runbooks / "testing.md").write_text("# Testing\n\n## Required skills for maintainers\n", encoding="utf-8")
    findings = repo_standards._check_composition_graph(tmp_path)
    assert any("testing.md" in finding for finding in findings)


def test_scaffold_pr_template_carries_composition_sections() -> None:
    spec = importlib.util.spec_from_file_location("scaffold_runbooks_pr_test", SKILL_ROOT / "scaffold_runbooks.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    content = mod._runbook_content("pr.md")
    for heading in (
        "## When",
        "## Required skills",
        "## Composition",
        "## Doctrine and contracts",
        "## Local commands and paths",
        "## Evidence contract",
        "## Prohibited combinations",
    ):
        assert heading in content
