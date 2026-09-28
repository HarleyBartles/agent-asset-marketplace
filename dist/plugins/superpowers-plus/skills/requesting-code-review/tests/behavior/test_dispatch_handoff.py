from pathlib import Path

import yaml


SKILL = Path(__file__).resolve().parents[2] / "SKILL.md"


def test_reviewer_skill_declares_its_route_owner() -> None:
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(text.split("---", 2)[1])
    assert "selecting-a-subagent" in frontmatter["metadata"]["related_skills"]
