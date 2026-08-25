from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "codex-marketplace" / "plugins" / "writing-pack"
APPROVED_SKILLS = {
    "writing",
    "writing-with-clarity",
    "writing-style",
    "writing-profile-engine",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_writing_pack_is_an_enabled_marketplace_root() -> None:
    inventory = _load_json(ROOT / "codex-marketplace" / "plugin-roots.json")
    writing_pack = next(root for root in inventory["roots"] if root["name"] == "writing-pack")

    assert writing_pack["enabled"] is True


def test_writing_pack_manifests_expose_the_approved_boundary() -> None:
    plugin_manifest = _load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    package_manifest = _load_json(PLUGIN_ROOT / "package.json")

    assert plugin_manifest["name"] == "writing-pack"
    assert package_manifest["name"] == "@harleybartles/writing-pack"
    assert APPROVED_SKILLS <= set(plugin_manifest["keywords"])
    assert APPROVED_SKILLS <= set(package_manifest["keywords"])


def test_clarity_skill_has_one_writing_pack_custody_path() -> None:
    clarity_skill = PLUGIN_ROOT / "skills" / "writing-with-clarity"

    assert clarity_skill.is_dir()
    old_clarity_skill = (
        ROOT / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills" / "writing-with-clarity"
    )

    assert not old_clarity_skill.exists()


def test_clarity_authority_assets_and_report_hygiene_survive_the_move() -> None:
    clarity_skill = PLUGIN_ROOT / "skills" / "writing-with-clarity"
    authority = clarity_skill / "assets" / "authority"

    assert authority.is_dir()
    assert (authority / "authority.yaml").is_file()
    assert (authority / "source-map.yaml").is_file()
    assert (authority / "CITATIONS.md").is_file()
    assert (authority / "reference-source" / "elements-of-style-1918").is_dir()
    assert (clarity_skill / "references" / "report-hygiene-checklist.md").is_file()


def test_writing_pack_skills_do_not_own_top_level_profiles_directories() -> None:
    skills_root = PLUGIN_ROOT / "skills"

    assert all(not (skill / "profiles").exists() for skill in skills_root.iterdir() if skill.is_dir())
