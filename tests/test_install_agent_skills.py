from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import install_agent_skills  # noqa: E402


def test_force_refresh_with_no_skill_changes_is_a_no_diff_operation(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    provenance_path = skills_path / ".provenance.json"
    original = {
        "manifestSha": "old-sha",
        "syncedAt": "2026-07-20T00:00:00",
        "syncedPlugins": ["repo-worker-pack"],
        "syncedSkills": 27,
    }
    provenance_path.write_text(json.dumps(original, indent=2) + "\n", encoding="utf-8")

    plugins = [
        {"name": "superpowers-plus"},
        {"name": "repo-worker-pack"},
    ]

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(install_agent_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(install_agent_skills, "_get_marketplace_manifest_sha", return_value="new-sha"),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=skills_path),
        patch.object(install_agent_skills, "_install_plugin_skills", return_value=False),
        patch.object(install_agent_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["install_agent_skills.py", "--force"]),
    ):
        assert install_agent_skills.main() == 0

    assert json.loads(provenance_path.read_text(encoding="utf-8")) == original
