from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "sources/first_party/skills/subagent-model-routing"
SKILL = SKILL_ROOT / "SKILL.md"
V1_PROFILE = SKILL_ROOT / "references/codex-multi-agent-v1-profile.md"
V2_PROFILE = SKILL_ROOT / "references/codex-multi-agent-v2-profile.md"


def test_router_selects_a_profile_from_the_live_dispatch_contract():
    text = SKILL.read_text(encoding="utf-8")

    assert "multi_agent_v1__spawn_agent" in text
    assert "fork_context" in text
    assert "spawn_agent` with `fork_turns" in text
    assert "codex-multi-agent-v1-profile.md" in text
    assert "codex-multi-agent-v2-profile.md" in text


def test_v1_profile_describes_the_v1_schema_without_claiming_unobserved_facts():
    text = V1_PROFILE.read_text(encoding="utf-8")

    for slug in ("gpt-5.4", "gpt-5.5", "gpt-5.6-luna", "gpt-5.6-terra", "gpt-5.6-sol"):
        assert f"`{slug}`" in text
    assert "`fork_context: true`" in text
    assert "`fork_context: false`" in text
    assert "pricing, entitlement, or numeric concurrency" in text
    assert "gpt-5.4-mini" not in text


def test_v2_profile_requires_bounded_context_for_model_or_reasoning_overrides():
    text = V2_PROFILE.read_text(encoding="utf-8")

    assert "`gpt-5.6-terra`" in text
    assert "`gpt-5.6-sol`" in text
    assert "`fork_turns: \"all\"`" in text
    assert "`fork_turns: \"none\"`" in text
    assert "inherit the parent model and reasoning" in text
    assert "cannot take a model or reasoning override" in text
    assert "gpt-5.6-luna" not in text
    assert "Four total agent slots" in text
    assert "inherited Terra" not in text
    assert "inherited parent model and reasoning" in text


def test_pressure_scenarios_allow_profile_supported_max_without_allowing_ultra():
    text = (SKILL_ROOT / "references/pressure-scenarios.md").read_text(encoding="utf-8")

    assert "requesting `ultra`" in text
    assert "`max` only when the active profile exposes it" in text
    assert "do not silently inherit the parent model and reasoning" in text
