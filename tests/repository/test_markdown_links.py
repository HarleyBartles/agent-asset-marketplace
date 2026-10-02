from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "validate_markdown_links.py"


def _fixture_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(name, None)
    return env


def _init_repo(path: Path) -> Path:
    path.mkdir()
    env = _fixture_env()
    subprocess.run(["git", "init"], cwd=path, env=env, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=path, env=env, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, env=env, check=True, capture_output=True)
    return path


def _commit_files(repo: Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    env = _fixture_env()
    subprocess.run(["git", "add", "-A"], cwd=repo, env=env, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, env=env, check=True, capture_output=True)


def _run(repo: Path) -> subprocess.CompletedProcess[str]:
    env = _fixture_env()
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
    )


def test_relative_rooted_and_external_links_and_agent_routed_doctrine_pass(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "valid-links")
    _commit_files(
        repo,
        {
            "AGENTS.md": (
                "# Home\n[Guide](docs/guide.md#usage)\n[Rooted](/docs/guide.md)\n[External](https://example.com/path)\n"
            ),
            "docs/guide.md": "# Guide\n\n## Usage\n",
            ".agents/AGENTS.md": "Read [the rule](doctrine/rule.md) when working with doctrine.\n",
            ".agents/doctrine/rule.md": "---\nstatus: active\n---\n# Rule\n",
            "skills/example/SKILL.md": "---\nname: example\nmetadata:\n  status: active\n---\n# Skill\n",
        },
    )

    result = _run(repo)

    assert result.returncode == 0, result.stderr
    assert "OK markdown links and doctrine routes" in result.stdout


def test_broken_and_repo_escaping_links_fail(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "bad-links")
    _commit_files(
        repo,
        {
            "AGENTS.md": "[Missing](missing.md)\n",
            "nested/AGENTS.md": "[Escape](../../outside.md)\n",
        },
    )

    result = _run(repo)

    assert result.returncode != 0
    assert "broken link: AGENTS.md -> missing.md" in result.stderr
    assert "repo-escaping link: nested/AGENTS.md -> ../../outside.md" in result.stderr


def test_active_doctrine_without_an_ancestor_route_fails(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "unrouted-doctrine")
    _commit_files(repo, {".agents/doctrine/rule.md": "---\nstatus: active\n---\n# Rule\n"})

    result = _run(repo)

    assert result.returncode != 0
    assert "active doctrine not routed: .agents/doctrine/rule.md" in result.stderr


def test_generated_index_does_not_route_active_doctrine(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "legacy-doctrine-route")
    _commit_files(
        repo,
        {
            ".agents/doctrine/INDEX.md": "[Rule](rule.md)\n",
            ".agents/doctrine/rule.md": "---\nstatus: active\n---\n# Rule\n",
        },
    )

    result = _run(repo)

    assert result.returncode != 0
    assert "active doctrine not routed: .agents/doctrine/rule.md" in result.stderr


def test_consumer_relative_examples_outside_guidance_and_docs_are_not_link_checked(tmp_path: Path) -> None:
    repo = _init_repo(tmp_path / "portable-example")
    _commit_files(repo, {"examples/template.md": "[Consumer runbook](../.agents/runbooks/implementing.md)\n"})

    result = _run(repo)

    assert result.returncode == 0, result.stderr
