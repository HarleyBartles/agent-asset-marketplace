import json
import importlib.util
import subprocess
import sys
from pathlib import Path
import pytest
from repo_standards_test_support import _create_worktree, _init_git_repo, _init_git_repo_with_commit, _stripped_env


REPO_ROOT = Path(__file__).resolve().parents[4]

SKILL_ROOT = REPO_ROOT / "skills" / "repo-shape" / "scripts"

SCAFFOLD_AGENTS_MD = SKILL_ROOT / "scaffold_agents_md.py"

SCAFFOLD_CONTRIBUTING = SKILL_ROOT / "scaffold_contributing.py"

SCAFFOLD_GITIGNORE = SKILL_ROOT / "scaffold_gitignore.py"

SCAFFOLD_MARKETPLACE_JSON = SKILL_ROOT / "scaffold_marketplace_json.py"

SCAFFOLD_REPO_RUNBOOK_POLICY = SKILL_ROOT / "scaffold_repo_runbook_policy.py"

REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"

SCAFFOLD_RUNBOOKS = SKILL_ROOT / "scaffold_runbooks.py"

SCAFFOLD_MARKDOWN_FORMATTING = SKILL_ROOT / "scaffold_markdown_formatting.py"


sys.path.insert(0, str(SKILL_ROOT))


_SPEC = importlib.util.spec_from_file_location("repo_standards_under_test", REPO_STANDARDS)

repo_standards = importlib.util.module_from_spec(_SPEC)


assert _SPEC.loader is not None


_SPEC.loader.exec_module(repo_standards)


_MARKDOWN_SPEC = importlib.util.spec_from_file_location(
    "scaffold_markdown_formatting_under_test", SCAFFOLD_MARKDOWN_FORMATTING
)

scaffold_markdown_formatting = importlib.util.module_from_spec(_MARKDOWN_SPEC)


assert _MARKDOWN_SPEC.loader is not None


_MARKDOWN_SPEC.loader.exec_module(scaffold_markdown_formatting)


def test_command_declaration_accepts_legacy_and_ordered_vectors(tmp_path: Path) -> None:
    contracts = tmp_path / ".agents" / "contracts"
    contracts.mkdir(parents=True)
    path = contracts / "repo-standards-commands.json"
    path.write_text(
        json.dumps(
            {
                "apply": ["@python", "tools/run.py", "ci", "--apply"],
                "check": [
                    ["@python", ".agents/skills/markdown-formatting/scripts/format_markdown.py", "--check"],
                    ["@python", "tools/run.py", "ci", "--check"],
                ],
                "generated_paths": ["generated/**"],
            }
        ),
        encoding="utf-8",
    )
    declaration, findings = repo_standards._check_declared_commands(tmp_path)
    assert findings == []
    assert declaration is not None
    assert declaration.apply == (("@python", "tools/run.py", "ci", "--apply"),)
    assert declaration.check[0][-1] == "--check"
    assert len(declaration.check) == 2


@pytest.mark.parametrize("value", [[], [[]], [["@python"]], ["@python", ["bad"]]])
def test_command_declaration_rejects_invalid_ordered_vectors(tmp_path: Path, value: object) -> None:
    contracts = tmp_path / ".agents" / "contracts"
    contracts.mkdir(parents=True)
    (contracts / "repo-standards-commands.json").write_text(
        json.dumps(
            {
                "apply": value,
                "check": ["@python", "tools/run.py", "ci", "--check"],
                "generated_paths": ["generated/**"],
            }
        ),
        encoding="utf-8",
    )
    declaration, findings = repo_standards._check_declared_commands(tmp_path)
    assert declaration is None
    assert any("invalid apply command" in finding for finding in findings)


def test_markdown_surface_adoption_and_enforcement_are_separate(tmp_path: Path) -> None:
    repo = tmp_path / "consumer"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / ".agents/contracts").mkdir(parents=True)
    (repo / ".agents/contracts/repo-standards-commands.json").write_text(
        json.dumps(
            {
                "apply": ["@python", "tools/run.py", "ci", "--apply"],
                "check": ["@python", "tools/run.py", "ci", "--check"],
                "generated_paths": ["generated/**"],
            }
        ),
        encoding="utf-8",
    )
    markdown = repo / "README.md"
    markdown.write_text("#  Title   \n", encoding="utf-8")
    (repo / ".mdformat.toml").write_bytes((REPO_ROOT / ".mdformat.toml").read_bytes())
    subprocess.run(["git", "add", "--all"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
    before = markdown.read_bytes()

    adopted = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKDOWN_FORMATTING), "--apply", "--state", "adopted"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert adopted.returncode == 0, adopted.stdout + adopted.stderr
    contract = json.loads((repo / ".agents/contracts/markdown-formatting.json").read_text(encoding="utf-8"))
    declaration = json.loads((repo / ".agents/contracts/repo-standards-commands.json").read_text(encoding="utf-8"))
    assert contract["state"] == "adopted"
    assert declaration["apply"] == ["@python", "tools/run.py", "ci", "--apply"]
    assert markdown.read_bytes() == before

    enforced = subprocess.run(
        [sys.executable, str(SCAFFOLD_MARKDOWN_FORMATTING), "--apply", "--state", "enforced"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert enforced.returncode == 0, enforced.stdout + enforced.stderr
    contract = json.loads((repo / ".agents/contracts/markdown-formatting.json").read_text(encoding="utf-8"))
    declaration = json.loads((repo / ".agents/contracts/repo-standards-commands.json").read_text(encoding="utf-8"))
    assert contract["state"] == "enforced"
    assert declaration["apply"][0][-1] == "--apply"
    assert declaration["check"][0][-1] == "--check"
    assert markdown.read_text(encoding="utf-8") == "# Title\n"


def test_markdown_enforcement_failure_restores_markdown(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "consumer"
    repo.mkdir()
    _init_git_repo(repo)
    (repo / ".agents/contracts").mkdir(parents=True)
    declaration_path = repo / ".agents/contracts/repo-standards-commands.json"
    declaration_path.write_text(
        json.dumps(
            {
                "apply": ["@python", "tools/run.py", "ci", "--apply"],
                "check": ["@python", "tools/run.py", "ci", "--check"],
                "generated_paths": ["generated/**"],
            }
        ),
        encoding="utf-8",
    )
    markdown = repo / "README.md"
    markdown.write_text("#  Title   \n", encoding="utf-8")
    subprocess.run(["git", "add", "--all"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
    before = markdown.read_bytes()

    class FailingFormatter:
        @staticmethod
        def load_contract(_root):
            return object()

        @staticmethod
        def eligible_markdown(_root, _contract):
            return (markdown,)

        @staticmethod
        def main(args):
            if args == ["--apply"]:
                markdown.write_text("# Title\n", encoding="utf-8")
                return 0
            return 1

    monkeypatch.setattr(
        scaffold_markdown_formatting,
        "_formatter",
        lambda _root: (FailingFormatter, Path("formatter.py")),
    )

    with pytest.raises(RuntimeError, match="check failed"):
        scaffold_markdown_formatting._enforce(repo)
    assert markdown.read_bytes() == before


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


def test_scaffold_gitignore_rejects_direct_force(tmp_path: Path) -> None:
    """Individual scaffolds cannot bypass coordinator force confirmation."""
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
    assert result.returncode == 1, result.stdout + result.stderr
    assert "direct scaffold force is disabled" in result.stdout
    assert not (repo / ".gitignore").exists()


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


def test_repo_standards_force_rejects_surface_without_reset_contract(tmp_path: Path) -> None:
    """Targeted force cannot bypass a surface's unavailable reset contract."""
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
        [
            sys.executable,
            str(REPO_STANDARDS),
            "--force",
            "contributing-entry",
            "--confirm-local-customisations-will-be-overwritten",
            "--allow-shared-checkout",
        ],
        cwd=repo,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1, combined
    assert "force reset is unavailable" in combined
    assert (repo / "CONTRIBUTING.md").read_text(encoding="utf-8") == "# Contributing\n\nStale.\n"


def test_targeted_force_warns_and_requires_noninteractive_acknowledgement(tmp_path: Path) -> None:
    repo = tmp_path / "force-confirmation"
    repo.mkdir()
    _init_git_repo(repo)
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--force", "completed-artifacts-doctrine"],
        cwd=repo,
        input="",
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "are you sure? This will force overwrite repo-local customisations" in combined
    assert "--confirm-local-customisations-will-be-overwritten" in combined


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


def test_repo_standards_allow_shared_checkout_does_not_mask_non_convergence(tmp_path: Path) -> None:
    """Shared-checkout approval does not turn an incomplete consumer into success."""
    repo = tmp_path / "allow-apply"
    repo.mkdir()
    _init_git_repo_with_commit(repo)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo, check=True)

    command_dir = repo / ".agents" / "contracts"
    command_dir.mkdir(parents=True)
    (command_dir / "repo-standards-commands.json").write_text(
        '{"apply":["@python","tools/run.py","ci","--apply"],'
        '"check":["@python","tools/run.py","ci","--check","--diagnostics"],"generated_paths":[".agents/skills/**"]}\n',
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
    assert result.returncode == 1, combined
    assert "--allow-shared-checkout supplied" in combined
    assert "did not converge" in combined


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


def test_repo_standards_force_preflight_precedes_shared_checkout_mutation(tmp_path: Path) -> None:
    """Invalid force targets fail before shared-checkout mutation or writes."""
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
        [
            sys.executable,
            str(REPO_STANDARDS),
            "--force",
            "contributing-entry",
            "--confirm-local-customisations-will-be-overwritten",
            "--allow-shared-checkout",
        ],
        cwd=worktree,
        env=_stripped_env(),
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 1, combined
    assert "force reset is unavailable" in combined
    assert (worktree / "CONTRIBUTING.md").read_text(encoding="utf-8") == "# Contributing\n\nStale.\n"


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


def test_direct_scaffold_force_is_disabled(tmp_path: Path) -> None:
    repo = tmp_path / "direct-force"
    repo.mkdir()
    _init_git_repo(repo)
    result = subprocess.run(
        [sys.executable, str(SCAFFOLD_CONTRIBUTING), "--force"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "direct scaffold force is disabled" in result.stdout


def test_shared_checkout_help_does_not_require_flag_in_worktrees() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO_STANDARDS), "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "shared/git-worktree checkout" not in result.stdout
    assert "shared/worktree checkouts" not in result.stdout
