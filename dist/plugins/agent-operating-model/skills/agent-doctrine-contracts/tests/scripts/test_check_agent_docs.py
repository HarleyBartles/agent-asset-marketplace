from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "assets" / "check_agent_docs.py"


def check(root: Path, *options: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", str(root), "--check", *options],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def test_requires_agent_document_stores_and_parses_json_syntax_only(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine"
    contracts = tmp_path / ".agents/contracts"
    doctrine.mkdir(parents=True)
    contracts.mkdir(parents=True)
    (contracts / "standard.json").write_text('{"pledge": "local"}\n', encoding="utf-8")
    (contracts / "bad.json").write_text('{"pledge": }\n', encoding="utf-8")

    result = check(tmp_path)

    assert result.returncode == 1
    assert "bad.json" in result.stdout and "invalid JSON syntax" in result.stdout
    assert "schema validation is not performed" in result.stdout.lower()
    assert "product schema" in result.stdout.lower()


def test_reports_missing_canonical_store(tmp_path: Path) -> None:
    (tmp_path / ".agents/contracts").mkdir(parents=True)

    result = check(tmp_path)

    assert result.returncode == 1
    assert "required agent-document store is missing: .agents/doctrine" in result.stdout


def test_valid_json_needs_no_universal_contract_schema(tmp_path: Path) -> None:
    (tmp_path / ".agents/doctrine").mkdir(parents=True)
    contracts = tmp_path / ".agents/contracts"
    contracts.mkdir(parents=True)
    (contracts / "local-contract.json").write_text('{"any": "repository-owned shape"}\n', encoding="utf-8")

    result = check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "schema validation is not performed" in result.stdout.lower()


def test_reports_broken_links_and_unlinked_documents_as_candidates(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine"
    contracts = tmp_path / ".agents/contracts"
    doctrine.mkdir(parents=True)
    contracts.mkdir(parents=True)
    (doctrine / "routed.md").write_text("See [contract](../contracts/rules.md).\n", encoding="utf-8")
    (doctrine / "broken.md").write_text("See [missing](not-here.md).\n", encoding="utf-8")
    (contracts / "rules.md").write_text("Keep a durable invariant.\n", encoding="utf-8")
    (contracts / "orphan.md").write_text("A governance document without a static inbound link.\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("Read [doctrine](.agents/doctrine/routed.md).\n", encoding="utf-8")

    result = check(tmp_path)

    assert result.returncode == 1
    assert "broken local link" in result.stdout.lower()
    assert "candidate without an inbound markdown link" in result.stdout.lower()
    assert "orphan.md" in result.stdout
    assert "routed.md" not in result.stdout.split("candidate without an inbound markdown link:")[-1]


def test_route_roots_and_excludes_affect_static_discovery_without_certifying_routes(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine"
    contracts = tmp_path / ".agents/contracts"
    custom = tmp_path / "custom-routes"
    doctrine.mkdir(parents=True)
    contracts.mkdir(parents=True)
    custom.mkdir()
    (doctrine / "rule.md").write_text("A durable rule.\n", encoding="utf-8")
    (doctrine / "runtime.md").write_text("A document loaded through plugin metadata.\n", encoding="utf-8")
    (custom / "entry.md").write_text("Read [the rule](../.agents/doctrine/rule.md).\n", encoding="utf-8")
    (tmp_path / "ignored.md").write_text("Read [the rule](.agents/doctrine/rule.md).\n", encoding="utf-8")
    (tmp_path / "plugin.json").write_text('{"skill_reference": ".agents/doctrine/runtime.md"}\n', encoding="utf-8")
    before = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()
    }

    result = check(tmp_path, "--exclude", "ignored.md", "--route-root", "custom-routes")
    after = {path.relative_to(tmp_path).as_posix(): path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}

    assert result.returncode == 0, result.stdout + result.stderr
    assert "static markdown links only" in result.stdout.lower()
    assert "candidate without an inbound markdown link: .agents/doctrine/runtime.md" in result.stdout.lower()
    assert before == after


def test_unrelated_markdown_links_contribute_inbound_evidence_without_failing(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine"
    contracts = tmp_path / ".agents/contracts"
    doctrine.mkdir(parents=True)
    contracts.mkdir(parents=True)
    (doctrine / "rule.md").write_text("A durable rule.\n", encoding="utf-8")
    (contracts / "contract.md").write_text("A repository contract.\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "See [rule](.agents/doctrine/rule.md) and [missing](not-here.md).\n", encoding="utf-8"
    )

    result = check(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "README.md: broken local link" not in result.stdout
    assert "candidate without an inbound markdown link: .agents/doctrine/rule.md" not in result.stdout.lower()
    assert "candidate without an inbound markdown link: .agents/contracts/contract.md" in result.stdout.lower()
