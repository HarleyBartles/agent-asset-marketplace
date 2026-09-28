from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers"


def _text(relative: str) -> str:
    return (SKILL / relative).read_text(encoding="utf-8")


def test_complete_upstream_diagnostic_asset_shape_is_present():
    expected = {
        "SKILL.md",
        "prompts/analyst-common.md",
        "prompts/cost-and-time.md",
        "prompts/plan-adherence.md",
        "prompts/quality-evidence.md",
        "prompts/repeated-work.md",
        "prompts/request-conflicts.md",
        "prompts/scrub-audit.md",
        "prompts/scrub.md",
        "prompts/similar-session.md",
        "prompts/skill-timeline.md",
        "prompts/stumbles.md",
        "references/context-safety.md",
        "references/github-issues.md",
        "references/redaction-policy.md",
        "references/session-discovery.md",
        "templates/bundle-README.md",
        "templates/case.md",
        "templates/issue.md",
        "templates/report.md",
        "agents/openai.yaml",
    }
    actual = {path.relative_to(SKILL).as_posix() for path in SKILL.rglob("*") if path.is_file()}
    assert actual == expected


def test_wrapper_and_frontmatter_declare_first_party_codex_contract():
    skill = _text("SKILL.md")
    assert "source-category: first_party" in skill
    assert "owner: Harley Bartles" in skill
    wrapper = yaml.safe_load(_text("agents/openai.yaml"))
    assert wrapper["metadata"]["source_category"] == "first_party"
    assert wrapper["policy"]["products"] == ["codex"]


def test_session_discovery_is_limited_to_codex_and_devin_desktop():
    discovery = _text("references/session-discovery.md").lower()
    assert "codex" in discovery
    assert "devin desktop" in discovery
    assert "claude code" not in discovery
    assert "gemini" not in discovery
    assert "copilot" not in discovery


def test_diagnostics_preserve_evidence_custody_and_mutation_gates():
    skill = _text("SKILL.md").lower()
    assert "path:line" in skill
    assert "read-only" in skill
    assert "do not diagnose superpowers" in skill
    assert "repository-segregated" in skill
    assert "off-repo" in skill
    assert "approval" in skill and "archive" in skill and "issue" in skill
    assert "sequential/self-analysis fallback" in skill
    assert "do not claim" in skill and "analysts ran" in skill

    all_text = "\n".join(path.read_text(encoding="utf-8") for path in SKILL.rglob("*") if path.is_file()).lower()
    assert "~/.superpowers/diagnosing-superpowers" not in all_text
    assert "claude code" not in all_text
    assert "cursor" not in all_text


def test_diagnostics_routes_through_existing_safety_owners():
    skill = _text("SKILL.md")
    for owner in (
        "context-safety",
        "selecting-a-subagent",
        "dispatching-parallel-agents",
        "using-github-mcp",
        "connector-safety",
    ):
        assert owner in skill

    lowered = skill.lower()
    assert "similar sessions" in lowered
    assert lowered.count("sequential/self-analysis fallback") >= 2
    assert "seven analytical dimensions" in lowered
