import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "sources" / "first_party" / "skills" / "repo-standards" / "scripts"
SCAFFOLD_AGENTS_MD = SKILL_ROOT / "scaffold_agents_md.py"
SCAFFOLD_MARKETPLACE_JSON = SKILL_ROOT / "scaffold_marketplace_json.py"
REPO_STANDARDS = SKILL_ROOT / "repo_standards.py"


def _stripped_env():
    env = os.environ.copy()
    env.pop("GIT_DIR", None)
    env.pop("GIT_WORK_TREE", None)
    env.pop("GIT_INDEX_FILE", None)
    return env


def _init_git_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test"], cwd=path, check=True, capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"], cwd=path, check=True, capture_output=True
    )


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

    guides = repo / ".agents" / "guides"
    guides.mkdir(parents=True)
    guide_files = {
        "publication-guide.md": "# Publication proof\n",
        "testing-guide.md": "# Testing instructions\n",
        "code-style-guide.md": "# Code style guidelines\n",
        "code-review-guide.md": "# Review guidelines\n",
        "pr-guide.md": "# PR instructions\n",
        "security-guide.md": "# Security considerations\n",
    }
    for name, content in guide_files.items():
        (guides / name).write_text(content, encoding="utf-8", newline="\n")
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
        "- [Publication proof](.agents/guides/publication-guide.md)\n"
        "- [Build and test commands](AGENTS.md)\n"
        "- [Testing instructions](.agents/guides/testing-guide.md)\n"
        "- [Code style guidelines](.agents/guides/code-style-guide.md)\n"
        "- [Review guidelines](.agents/guides/code-review-guide.md)\n"
        "- [PR instructions](.agents/guides/pr-guide.md)\n"
        "- [Contributing](CONTRIBUTING.md)\n"
        "- [Security considerations](.agents/guides/security-guide.md)\n"
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
    assert data["repo"]["local_skill_prefixes"] == ["mark-"]


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
    assert data["repo"]["local_skill_prefixes"] == ["mark-"]
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
        "- ci-preflight-ps1\n"
        "- ci-preflight-sh\n"
        "- pre-commit-hook\n"
        "- repo-guide-policy\n"
        "- guides-agents-md\n"
        "- review-entry\n"
        "- contributing-entry\n"
        "- root-gitignore\n"
    )
    policy_dir = repo / ".agents" / "docs"
    policy_dir.mkdir(parents=True)
    (policy_dir / "repo-guide-policy.md").write_text(
        f"# Repo guide policy\n\n## Exceptions\n\n{exceptions}",
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
