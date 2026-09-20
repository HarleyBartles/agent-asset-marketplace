from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts"
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


def test_customized_runbook_passes_without_matching_seed(tmp_path: Path) -> None:
    path = tmp_path / ".agents/runbooks/implementing.md"
    path.parent.mkdir(parents=True)
    path.write_text(_runbook(extra="## Repository-specific release train\n\nBlue/green only.\n"), encoding="utf-8")
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
