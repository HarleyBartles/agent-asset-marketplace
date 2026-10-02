from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
STANDARD_SKILLS = (
    "agents-routing",
    "agent-doctrine-contracts",
    "completed-artifact-custody",
    "contribution-entrypoint",
    "playbook-composition",
    "review-entrypoint",
    "runbook-composition",
    "unslop",
)


def _frontmatter(skill_md: Path) -> dict[str, object]:
    text = skill_md.read_text(encoding="utf-8")
    _, frontmatter, _ = text.split("---", maxsplit=2)
    parsed = yaml.safe_load(frontmatter)
    assert isinstance(parsed, dict)
    return parsed


def test_aom_standard_skills_ship_codex_discovery_metadata() -> None:
    bundle_path = ROOT / "src/plugin-definitions/agent-operating-model/contents.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundled_names = {entry["name"] for entry in bundle["skills"]}
    package_root = ROOT / "dist/plugins/agent-operating-model/skills"

    assert set(STANDARD_SKILLS) <= bundled_names

    for name in STANDARD_SKILLS:
        source_root = ROOT / "skills" / name
        frontmatter = _frontmatter(source_root / "SKILL.md")
        metadata = frontmatter["metadata"]
        assert isinstance(metadata, dict)
        for field in ("use_when", "do_not_use_when"):
            triggers = metadata[field]
            assert isinstance(triggers, list) and triggers
            assert all(isinstance(trigger, str) and trigger.strip() for trigger in triggers)

        source_wrapper = source_root / "agents/openai.yaml"
        wrapper = yaml.safe_load(source_wrapper.read_text(encoding="utf-8"))
        assert wrapper["version"] == 1
        assert wrapper["metadata"]["skill_name"] == name
        assert wrapper["interface"]["display_name"].strip()
        assert wrapper["interface"]["short_description"].strip()
        assert wrapper["interface"]["default_prompt"].startswith(f"Use {name} ")
        assert wrapper["policy"]["allow_implicit_invocation"] is True

        packaged_root = package_root / name
        assert (packaged_root / "SKILL.md").is_file()
        assert (packaged_root / "agents/openai.yaml").read_bytes() == source_wrapper.read_bytes()
