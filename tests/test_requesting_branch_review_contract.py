from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/first_party/skills/requesting-branch-review"
SKILL = SOURCE / "SKILL.md"
AGENTS = SOURCE / "agents" / "openai.yaml"
ASSET = SOURCE / "assets" / "branch-reviewer" / "AGENT.md"


def _skill_frontmatter() -> dict:
    text = SKILL.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        raise ValueError("SKILL.md must have opening and closing frontmatter delimiters")
    return yaml.safe_load(parts[1]) or {}


def test_source_skill_has_required_files():
    assert SKILL.is_file()
    assert AGENTS.is_file()
    assert ASSET.is_file()


def test_skill_frontmatter_has_required_fields():
    frontmatter = _skill_frontmatter()
    assert frontmatter.get("name") == "requesting-branch-review"
    assert frontmatter.get("description")
    assert frontmatter.get("license") == "MIT"
    assert "agent" not in frontmatter

    metadata = frontmatter.get("metadata") or {}
    assert metadata.get("source-id") == "requesting-branch-review"
    assert metadata.get("source-category") == "first_party"
    assert metadata.get("status") == "active"
    assert isinstance(metadata.get("use_when"), list)
    assert isinstance(metadata.get("do_not_use_when"), list)


def test_agents_openai_yaml_has_required_fields():
    data = yaml.safe_load(AGENTS.read_text(encoding="utf-8"))
    assert data.get("version") == 1
    assert data.get("metadata", {}).get("skill_name") == "requesting-branch-review"
    interface = data.get("interface") or {}
    assert interface.get("display_name") == "Requesting Branch Review"
    assert interface.get("short_description")
    assert interface.get("default_prompt").startswith("Use /requesting-branch-review")
    assert data.get("policy", {}).get("allow_implicit_invocation") is False


def test_branch_reviewer_asset_is_swe_1_7():
    text = ASSET.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        raise ValueError("AGENT.md must have opening and closing frontmatter delimiters")
    asset = yaml.safe_load(parts[1]) or {}
    assert asset.get("name") == "branch-reviewer"
    assert asset.get("model") == "swe-1-7"
    assert isinstance(asset.get("allowed-tools"), list)
    assert "read" in asset["allowed-tools"]
