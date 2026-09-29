from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/repo-shape/scripts"
sys.path.insert(0, str(SCRIPTS))

import document_contracts  # noqa: E402


def _runbook(required_skills: str = "- `repo-worker-base`", extra: str = "") -> str:
    sections = {
        "When": "When repository work begins.",
        "Required skills": required_skills,
        "Composition": "Compose focused capabilities.",
        "Doctrine and contracts": "Read local doctrine.",
        "Local commands and paths": "Run `tools/run.py ci --check`.",
        "Evidence contract": "Record passing output.",
        "Prohibited combinations": "Do not bypass validation.",
        "Playbook routing": "Use [testing](../playbooks/testing.md).",
    }
    return (
        "# Implementing\n\n" + "\n\n".join(f"## {name}\n\n{body}" for name, body in sections.items()) + "\n\n" + extra
    )


def _capability_runbook() -> str:
    return """# Implementing

## When
When repository-backed implementation is requested.

## Required capabilities
- Isolated repository work and source-custody guidance.

## Optional capabilities
- Writing-quality review for substantial prose.

## Required repository-owned skills
None.

## Optional repository-owned skills
None.

## Composition
Resolve each required capability from the skills available in the active runtime before dependent work.

## Doctrine and contracts
Follow the repository's declared policy.

## Local commands and paths
Use the locally declared command bus.

## Evidence contract
Record current validation evidence.

## Prohibited combinations
Do not bypass validation.

## Playbook routing
None.
"""


def test_customized_runbook_passes_without_matching_seed(tmp_path: Path) -> None:
    path = tmp_path / ".agents/runbooks/implementing.md"
    path.parent.mkdir(parents=True)
    path.write_text(_runbook(extra="## Repository-specific release train\n\nBlue/green only.\n"), encoding="utf-8")
    assert document_contracts.check_runbook(path, tmp_path) == []


def test_capability_contract_passes_in_a_custom_runbook_home(tmp_path: Path) -> None:
    path = tmp_path / "engineering/workflows/implementing.md"
    path.parent.mkdir(parents=True)
    path.write_text(_capability_runbook(), encoding="utf-8")

    assert document_contracts.check_runbook(path, tmp_path) == []


def test_placeholder_required_skills_does_not_pass(tmp_path: Path) -> None:
    path = tmp_path / "implementing.md"
    path.write_text(_runbook(required_skills="<!-- choose later -->"), encoding="utf-8")
    findings = document_contracts.check_runbook(path, tmp_path)
    assert any(item.code == "empty-required-skills" for item in findings)


def test_fenced_heading_does_not_satisfy_contract(tmp_path: Path) -> None:
    path = tmp_path / "implementing.md"
    path.write_text(_runbook().replace("## Evidence contract", "```md\n## Evidence contract\n```"), encoding="utf-8")
    assert any(item.code == "empty-evidence-contract" for item in document_contracts.check_runbook(path, tmp_path))


def test_optional_scoped_router_is_absent_or_valid(tmp_path: Path) -> None:
    path = tmp_path / ".agents/runbooks/AGENTS.md"
    assert document_contracts.check_optional_router(path, tmp_path) == []
    path.parent.mkdir(parents=True)
    path.write_text("# Runbook routing\n\nRepository-specific selection guidance.\n", encoding="utf-8")
    assert document_contracts.check_optional_router(path, tmp_path) == []
    path.write_text("<!-- choose later -->\n", encoding="utf-8")
    assert any(item.code == "empty-scoped-router" for item in document_contracts.check_optional_router(path, tmp_path))


def test_optional_scope_pointer_router_accepts_one_sentence_with_resolving_link(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine/docs.md"
    doctrine.parent.mkdir(parents=True)
    doctrine.write_text("# Documentation custody\n", encoding="utf-8")
    path = tmp_path / "docs/AGENTS.md"
    path.parent.mkdir()
    path.write_text(
        "For work under `docs/`, read and follow [documentation custody](../.agents/doctrine/docs.md).\n",
        encoding="utf-8",
    )

    assert document_contracts.check_optional_router(path, tmp_path) == []


def test_scope_pointer_router_rejects_wrong_scope_and_unresolved_link(tmp_path: Path) -> None:
    path = tmp_path / "docs/AGENTS.md"
    path.parent.mkdir(parents=True)
    path.write_text("For work under `other/`, read [the policy](missing.md).\n", encoding="utf-8")

    findings = document_contracts.check_optional_router(path, tmp_path)

    assert len(findings) == 1
    assert findings[0].code == "invalid-scope-pointer-router"
    assert "scope" in findings[0].message.lower()
    assert "link" in findings[0].message.lower()


def test_scope_pointer_router_rejects_extra_sentences_and_external_links(tmp_path: Path) -> None:
    path = tmp_path / "docs/AGENTS.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "For work under `docs/`, read [the policy](https://example.com/policy). Also follow local conventions.\n",
        encoding="utf-8",
    )

    findings = document_contracts.check_optional_router(path, tmp_path)

    assert len(findings) == 1
    assert findings[0].code == "invalid-scope-pointer-router"


def test_agent_docs_scope_pointer_uses_containing_tree_and_local_doctrine(tmp_path: Path) -> None:
    doctrine = tmp_path / ".agents/doctrine/docs.md"
    doctrine.parent.mkdir(parents=True)
    doctrine.write_text("# Documentation custody\n", encoding="utf-8")
    path = tmp_path / ".agents/docs/AGENTS.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "For work under `.agents/docs/`, read and follow [documentation custody](../doctrine/docs.md).\n",
        encoding="utf-8",
    )

    assert document_contracts.check_optional_router(path, tmp_path) == []
