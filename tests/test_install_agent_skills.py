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


def test_clean_orphan_skills_preserves_mark_skill(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    local_skill = skills_path / "mark-example"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-example\ndescription: Use when testing local skill custody.\n---\n\n# Example\n",
        encoding="utf-8",
    )

    with patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path):
        assert install_agent_skills._clean_orphan_skills([], synced_skill_names=set()) is False

    assert local_skill.is_dir()


def test_validate_local_skill_dirs_rejects_mark_skill_without_skill_md(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    (skills_path / "mark-invalid").mkdir(parents=True)

    with patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path):
        invalid = install_agent_skills._validate_local_skill_dirs()

    assert invalid == [skills_path / "mark-invalid"]


def test_main_rejects_malformed_mark_skill_frontmatter(tmp_path: Path, capsys) -> None:
    skills_path = tmp_path / "skills"
    local_skill = skills_path / "mark-invalid"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text(
        "---\nname: [unterminated\ndescription: invalid\n---\n\n# Invalid\n",
        encoding="utf-8",
    )

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": []}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[]),
        patch.object(sys, "argv", ["install_agent_skills.py"]),
    ):
        result = install_agent_skills.main()

    captured = capsys.readouterr()
    assert result == 1
    assert "ERROR: local skill" in captured.out
    assert "Traceback" not in captured.err


def test_main_rejects_mark_directory_name_that_differs_from_frontmatter(tmp_path: Path, capsys) -> None:
    skills_path = tmp_path / "skills"
    local_skill = skills_path / "mark-directory"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-frontmatter\ndescription: Use when testing local skill identity.\n---\n\n# Example\n",
        encoding="utf-8",
    )

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(sys, "argv", ["install_agent_skills.py"]),
    ):
        result = install_agent_skills.main()

    assert result == 1
    assert "must match frontmatter name" in capsys.readouterr().out


def test_main_rejects_marketplace_reserved_mark_skill_before_mutation(tmp_path: Path, capsys) -> None:
    source_skills = tmp_path / "source" / "skills"
    source_skill = source_skills / "mark-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("marketplace content\n", encoding="utf-8")

    installed_skills = tmp_path / "installed"
    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", installed_skills),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[{"name": "example"}]),
        patch.object(sys, "argv", ["install_agent_skills.py"]),
    ):
        assert install_agent_skills.main() == 1

    assert not installed_skills.exists()
    assert "reserved local skill prefix" in capsys.readouterr().out


def test_main_check_rejects_marketplace_reserved_mark_skill_before_mutation(tmp_path: Path, capsys) -> None:
    source_skills = tmp_path / "source" / "skills"
    source_skill = source_skills / "mark-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("marketplace content\n", encoding="utf-8")

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", tmp_path / "installed"),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[{"name": "example"}]),
        patch.object(sys, "argv", ["install_agent_skills.py", "--check"]),
    ):
        assert install_agent_skills.main() == 1

    assert "reserved local skill prefix" in capsys.readouterr().out


def test_matching_provenance_with_missing_marketplace_skill_continues_sync(tmp_path: Path) -> None:
    skills_path = tmp_path / "installed"
    skills_path.mkdir()
    provenance_path = skills_path / ".provenance.json"
    provenance_path.write_text('{"manifestSha": "current"}\n', encoding="utf-8")
    source_skills = tmp_path / "source/skills"
    source_skill = source_skills / "marketplace-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("source\n", encoding="utf-8")
    plugin = {"name": "example"}

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(install_agent_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(install_agent_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(install_agent_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(install_agent_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["install_agent_skills.py", "--check"]),
    ):
        assert install_agent_skills.main() == 1

    install.assert_called_once()


def test_matching_provenance_with_stale_marketplace_skill_continues_sync(tmp_path: Path) -> None:
    skills_path = tmp_path / "installed"
    installed_skill = skills_path / "marketplace-example"
    installed_skill.mkdir(parents=True)
    (installed_skill / "SKILL.md").write_text("stale\n", encoding="utf-8")
    (skills_path / ".provenance.json").write_text('{"manifestSha": "current"}\n', encoding="utf-8")
    local_skill = skills_path / "mark-local"
    local_skill.mkdir()
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-local\ndescription: Use when preserving local custody.\n---\n\n# Local\n",
        encoding="utf-8",
    )
    source_skills = tmp_path / "source/skills"
    source_skill = source_skills / "marketplace-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("current\n", encoding="utf-8")
    plugin = {"name": "example"}

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(install_agent_skills, "PROVENANCE_PATH", skills_path / ".provenance.json"),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(install_agent_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(install_agent_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(install_agent_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["install_agent_skills.py", "--check"]),
    ):
        assert install_agent_skills.main() == 1

    install.assert_called_once()
    assert local_skill.is_dir()


def test_matching_provenance_with_extra_marketplace_orphan_continues_sync(tmp_path: Path) -> None:
    skills_path = tmp_path / "installed"
    installed_skill = skills_path / "marketplace-example"
    installed_skill.mkdir(parents=True)
    (installed_skill / "SKILL.md").write_text("current\n", encoding="utf-8")
    (skills_path / "orphan-marketplace-skill").mkdir()
    (skills_path / ".provenance.json").write_text('{"manifestSha": "current"}\n', encoding="utf-8")
    local_skill = skills_path / "mark-local"
    local_skill.mkdir()
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-local\ndescription: Use when preserving local custody.\n---\n\n# Local\n",
        encoding="utf-8",
    )
    source_skills = tmp_path / "source/skills"
    source_skill = source_skills / "marketplace-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("current\n", encoding="utf-8")
    plugin = {"name": "example"}

    with (
        patch.object(install_agent_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(install_agent_skills, "PROVENANCE_PATH", skills_path / ".provenance.json"),
        patch.object(install_agent_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(install_agent_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(install_agent_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(install_agent_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(install_agent_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(install_agent_skills, "_clean_orphan_skills", return_value=True) as clean,
        patch.object(sys, "argv", ["install_agent_skills.py", "--check"]),
    ):
        assert install_agent_skills.main() == 1

    install.assert_called_once()
    clean.assert_called_once()
    assert local_skill.is_dir()
