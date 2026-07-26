from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "sources" / "first_party" / "skills" / "refreshing-installed-skills" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import refresh_installed_skills  # noqa: E402


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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="new-sha"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=skills_path),
        patch.object(refresh_installed_skills, "_install_plugin_skills", return_value=False),
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--force", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    assert json.loads(provenance_path.read_text(encoding="utf-8")) == original


def test_clean_orphan_skills_preserves_mark_skill(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    local_skill = skills_path / "mark-example"
    local_skill.mkdir(parents=True)
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-example\ndescription: Use when testing local skill custody.\n---\n\n# Example\n",
        encoding="utf-8",
    )

    with patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path):
        assert refresh_installed_skills._clean_orphan_skills([], synced_skill_names=set()) is False

    assert local_skill.is_dir()


def test_validate_local_skill_dirs_rejects_mark_skill_without_skill_md(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    (skills_path / "mark-invalid").mkdir(parents=True)

    with patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path):
        invalid = refresh_installed_skills._validate_local_skill_dirs(["mark-"])

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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": []}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[]),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--allow-shared-checkout"]),
    ):
        result = refresh_installed_skills.main()

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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--allow-shared-checkout"]),
    ):
        result = refresh_installed_skills.main()

    assert result == 1
    assert "must match frontmatter name" in capsys.readouterr().out


def test_main_rejects_marketplace_reserved_mark_skill_before_mutation(tmp_path: Path, capsys) -> None:
    source_skills = tmp_path / "source" / "skills"
    source_skill = source_skills / "mark-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("marketplace content\n", encoding="utf-8")

    installed_skills = tmp_path / "installed"
    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", installed_skills),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[{"name": "example"}]),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 1

    assert not installed_skills.exists()
    assert "reserved local skill prefix" in capsys.readouterr().out


def test_main_check_rejects_marketplace_reserved_mark_skill_before_mutation(tmp_path: Path, capsys) -> None:
    source_skills = tmp_path / "source" / "skills"
    source_skill = source_skills / "mark-example"
    source_skill.mkdir(parents=True)
    (source_skill / "SKILL.md").write_text("marketplace content\n", encoding="utf-8")

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", tmp_path / "installed"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[{"name": "example"}]),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        assert refresh_installed_skills.main() == 1

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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        assert refresh_installed_skills.main() == 1

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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", skills_path / ".provenance.json"),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        assert refresh_installed_skills.main() == 1

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
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", skills_path / ".provenance.json"),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_install_plugin_skills", return_value=True) as install,
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=True) as clean,
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        assert refresh_installed_skills.main() == 1

    install.assert_called_once()
    clean.assert_called_once()
    assert local_skill.is_dir()


def test_get_plugin_skills_path_local_source(tmp_path: Path) -> None:
    skills = tmp_path / "my-plugin" / "skills"
    skills.mkdir(parents=True)
    plugin = {"name": "my-plugin", "source": {"source": "local", "path": "my-plugin"}}
    with patch.object(refresh_installed_skills, "ROOT", tmp_path):
        result = refresh_installed_skills._get_plugin_skills_path(plugin)
    assert result == skills


def test_get_plugin_skills_path_github_source(tmp_path: Path) -> None:
    submodule = tmp_path / ".agents" / "plugins" / "marketplace-source"
    skills = submodule / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"
    skills.mkdir(parents=True)
    plugin = {
        "name": "repo-worker-pack",
        "source": {
            "source": "github",
            "owner": "HarleyBartles",
            "repo": "agent-asset-marketplace",
            "path": "codex-marketplace/plugins/repo-worker-pack",
        },
    }
    with patch.object(refresh_installed_skills, "ROOT", tmp_path):
        result = refresh_installed_skills._get_plugin_skills_path(plugin)
    assert result == skills


def test_get_plugin_skills_path_github_source_with_dotdot_resolving_inside_base(tmp_path: Path) -> None:
    submodule = tmp_path / ".agents" / "plugins" / "marketplace-source"
    skills = submodule / "codex-marketplace" / "plugins" / "repo-worker-pack" / "skills"
    skills.mkdir(parents=True)
    plugin = {
        "name": "repo-worker-pack",
        "source": {
            "source": "github",
            "owner": "HarleyBartles",
            "repo": "agent-asset-marketplace",
            "path": "../marketplace-source/codex-marketplace/plugins/repo-worker-pack",
        },
    }
    with patch.object(refresh_installed_skills, "ROOT", tmp_path):
        result = refresh_installed_skills._get_plugin_skills_path(plugin)
    assert result == skills


def test_get_plugin_skills_path_returns_none_for_unsupported_or_malformed(tmp_path: Path) -> None:
    with patch.object(refresh_installed_skills, "ROOT", tmp_path):
        assert refresh_installed_skills._get_plugin_skills_path({}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "bitbucket"}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "local"}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "local", "path": ""}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "local", "path": 123}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "local", "path": "missing-plugin"}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "path": "missing-plugin"}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "owner": "HarleyBartles"}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "owner": "HarleyBartles", "repo": ""}}) is None
        assert refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "owner": "", "repo": "agent-asset-marketplace", "path": "missing-plugin"}}) is None


def test_get_plugin_skills_path_rejects_path_escaping_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    sibling = tmp_path / "sibling"
    (sibling / "skills").mkdir(parents=True)
    plugin = {"source": {"source": "local", "path": "../sibling"}}
    with patch.object(refresh_installed_skills, "ROOT", repo_root):
        result = refresh_installed_skills._get_plugin_skills_path(plugin)
    assert result is None
