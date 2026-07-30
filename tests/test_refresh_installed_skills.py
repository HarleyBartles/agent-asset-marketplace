from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


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
        "manifestSha": "current",
        "syncedAt": "2026-07-20T00:00:00",
        "syncedPlugins": ["superpowers-plus", "repo-worker-pack"],
        "syncedSkills": 0,
        "localSkills": [],
        "marketplace": {
            "source": "HarleyBartles/agent-asset-marketplace",
            "sourcePath": "codex-marketplace/plugins",
        },
        "localPlugins": [],
        "marketplaceFile": ".agents/plugins/marketplace.json",
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
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=skills_path),
        patch.object(refresh_installed_skills, "_install_plugin_skills", return_value=False),
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--force", "--apply", "--allow-shared-checkout"]),
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
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
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
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
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
        patch.object(
            refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}
        ),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[{"name": "example"}]),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
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
        patch.object(
            refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [{"name": "example"}]}
        ),
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
        assert (
            refresh_installed_skills._get_plugin_skills_path({"source": {"source": "local", "path": "missing-plugin"}})
            is None
        )
        assert (
            refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "path": "missing-plugin"}})
            is None
        )
        assert (
            refresh_installed_skills._get_plugin_skills_path({"source": {"source": "github", "owner": "HarleyBartles"}})
            is None
        )
        assert (
            refresh_installed_skills._get_plugin_skills_path(
                {"source": {"source": "github", "owner": "HarleyBartles", "repo": ""}}
            )
            is None
        )
        assert (
            refresh_installed_skills._get_plugin_skills_path(
                {
                    "source": {
                        "source": "github",
                        "owner": "",
                        "repo": "agent-asset-marketplace",
                        "path": "missing-plugin",
                    }
                }
            )
            is None
        )


def test_get_plugin_skills_path_rejects_path_escaping_root(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    sibling = tmp_path / "sibling"
    (sibling / "skills").mkdir(parents=True)
    plugin = {"source": {"source": "local", "path": "../sibling"}}
    with patch.object(refresh_installed_skills, "ROOT", repo_root):
        result = refresh_installed_skills._get_plugin_skills_path(plugin)
    assert result is None


def _git_init_and_commit(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True, capture_output=True)
    (repo / ".gitkeep").write_text("", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True, capture_output=True)


def test_get_marketplace_manifest_sha_returns_submodule_head(tmp_path: Path) -> None:
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    _git_init_and_commit(consumer)
    submodule = consumer / ".agents" / "plugins" / "marketplace-source"
    submodule.mkdir(parents=True)
    _git_init_and_commit(submodule)
    marketplace_json = consumer / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.write_text("{}", encoding="utf-8")

    with (
        patch.object(refresh_installed_skills, "ROOT", consumer),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
    ):
        sha = refresh_installed_skills._get_marketplace_manifest_sha()

    expected = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=submodule, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert sha == expected


def test_get_marketplace_manifest_sha_falls_back_to_consumer_head(tmp_path: Path) -> None:
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    _git_init_and_commit(consumer)
    marketplace_json = consumer / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text("{}", encoding="utf-8")

    with (
        patch.object(refresh_installed_skills, "ROOT", consumer),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
    ):
        sha = refresh_installed_skills._get_marketplace_manifest_sha()

    expected = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=consumer, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert sha == expected


def test_provenance_synced_plugins_lists_all_installed_plugins(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    provenance_path = skills_path / ".provenance.json"
    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    plugins = [
        {"name": "repo-worker-pack"},
        {"name": "superpowers-plus"},
    ]

    def install_side_effect(plugin, *args, **kwargs):
        return plugin.get("name") == "repo-worker-pack"

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="new-sha"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_install_plugin_skills", side_effect=install_side_effect),
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--force", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["syncedPlugins"] == ["repo-worker-pack", "superpowers-plus"]


def test_validate_local_skills_extra_hook_invoked(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    scripts_path = tmp_path / "scripts"
    scripts_path.mkdir()
    marketplace_json = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text('{"plugins": []}', encoding="utf-8")
    log_path = tmp_path / "hook-log.txt"

    if sys.platform == "win32":
        hook = scripts_path / "validate_local_skills_extra.ps1"
        hook.write_text(
            "param([switch]$Check, [Parameter(ValueFromRemainingArguments=$true)][string[]]$Remaining)\n"
            "$skillsRoot = $Remaining[0]\n"
            "$prefixes = $Remaining[1..($Remaining.Length-1)]\n"
            '$mode = if ($Check) { "check" } else { "write" }\n'
            f'[System.IO.File]::WriteAllText("{log_path.as_posix()}", "$skillsRoot $($prefixes -join ",") $mode")\n',
            encoding="utf-8",
        )
    else:
        hook = scripts_path / "validate_local_skills_extra.sh"
        hook.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            'if [ "$1" = "--check" ]; then mode=check; shift; else mode=write; fi\n'
            'skills_root="$1"\n'
            "shift\n"
            'prefixes="$*"\n'
            f'echo "$skills_root $prefixes $mode" > "{log_path.as_posix()}"\n',
            encoding="utf-8",
        )
        hook.chmod(0o755)

    with (
        patch.object(refresh_installed_skills, "ROOT", tmp_path),
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": []}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[]),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply"]),
    ):
        assert refresh_installed_skills.main() == 0

    log = log_path.read_text(encoding="utf-8").strip()
    rel_skills = skills_path.relative_to(tmp_path).as_posix()
    assert rel_skills in log
    assert "mark-" in log
    assert "write" in log


def test_validate_local_skills_extra_hook_failure_fails_run(tmp_path: Path, capsys) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    scripts_path = tmp_path / "scripts"
    scripts_path.mkdir()
    marketplace_json = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text('{"plugins": []}', encoding="utf-8")

    if sys.platform == "win32":
        hook = scripts_path / "validate_local_skills_extra.ps1"
        hook.write_text("Write-Host 'bad skill'\nexit 1\n", encoding="utf-8")
    else:
        hook = scripts_path / "validate_local_skills_extra.sh"
        hook.write_text("#!/usr/bin/env bash\necho 'bad skill'\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)

    with (
        patch.object(refresh_installed_skills, "ROOT", tmp_path),
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": []}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[]),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply"]),
    ):
        assert refresh_installed_skills.main() == 1

    assert "bad skill" in capsys.readouterr().out


def test_provenance_records_local_plugin_origin(tmp_path: Path) -> None:
    """Local plugins are recorded separately in provenance, not as marketplace."""
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    provenance_path = skills_path / ".provenance.json"
    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)

    plugins = [
        {
            "name": "repo-worker-pack",
            "source": {
                "source": "github",
                "owner": "HarleyBartles",
                "repo": "agent-asset-marketplace",
                "path": "codex-marketplace/plugins/repo-worker-pack",
            },
        },
        {
            "name": "game-studio",
            "source": {"source": "local", "path": ".agents/plugins/game-studio"},
        },
    ]

    def install_side_effect(plugin, check_mode=False, synced_skill_names=None, prefixes=None):
        if synced_skill_names is not None:
            synced_skill_names.add(plugin.get("name", "unknown"))
        return True

    roll_mock = MagicMock()

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "ROOT", tmp_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="pinned-sha"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills, "_install_plugin_skills", side_effect=install_side_effect),
        patch.object(refresh_installed_skills, "_clean_orphan_skills", return_value=False),
        patch.object(refresh_installed_skills, "_roll_marketplace_source", roll_mock),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--force", "--apply"]),
    ):
        assert refresh_installed_skills.main() == 0

    roll_mock.assert_not_called()
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["syncedPlugins"] == ["repo-worker-pack", "game-studio"]
    assert provenance["manifestSha"] == "pinned-sha"
    assert provenance["marketplace"]["source"] == "HarleyBartles/agent-asset-marketplace"
    assert provenance["marketplace"]["sourcePath"] == "codex-marketplace/plugins"
    assert provenance["localPlugins"] == [
        {
            "name": "game-studio",
            "path": ".agents/plugins/game-studio",
            "source": "local",
        }
    ]
    assert "source" not in provenance
    assert "sourcePath" not in provenance


def test_default_roll_marketplace_source_is_off(tmp_path: Path) -> None:
    """Without --roll-marketplace-source the pinned submodule is not rolled."""
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    _git_init_and_commit(consumer)
    submodule = consumer / ".agents" / "plugins" / "marketplace-source"
    submodule.mkdir(parents=True)
    _git_init_and_commit(submodule)

    marketplace_json = consumer / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text('{"plugins": []}', encoding="utf-8")

    with (
        patch.object(refresh_installed_skills, "ROOT", consumer),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", consumer / ".agents" / "skills"),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", consumer / ".agents" / "skills" / ".provenance.json"),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply"]),
    ):
        assert refresh_installed_skills.main() == 0

    assert not (consumer / ".agents" / "skills" / ".provenance.json").exists()


def test_roll_marketplace_source_flag_invokes_roll(tmp_path: Path) -> None:
    """--roll-marketplace-source explicitly rolls the submodule forward."""
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    _git_init_and_commit(consumer)
    marketplace_json = consumer / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text('{"plugins": []}', encoding="utf-8")

    roll_mock = MagicMock()

    with (
        patch.object(refresh_installed_skills, "ROOT", consumer),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(refresh_installed_skills, "_roll_marketplace_source", roll_mock),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--roll-marketplace-source"]),
    ):
        assert refresh_installed_skills.main() == 0

    roll_mock.assert_called_once()


def test_allow_shared_checkout_requires_apply(capsys) -> None:
    """--allow-shared-checkout without --apply is rejected."""
    with patch.object(sys, "argv", ["refresh_installed_skills.py", "--allow-shared-checkout"]):
        result = refresh_installed_skills.main()
    captured = capsys.readouterr()
    assert result == 1
    assert "--allow-shared-checkout requires --apply" in captured.err


def test_allow_shared_checkout_with_check_requires_apply(capsys) -> None:
    """--allow-shared-checkout with --check is rejected."""
    with patch.object(sys, "argv", ["refresh_installed_skills.py", "--allow-shared-checkout", "--check"]):
        result = refresh_installed_skills.main()
    captured = capsys.readouterr()
    assert result == 1
    assert "--allow-shared-checkout requires --apply" in captured.err


def test_apply_in_shared_checkout_requires_allow_flag(capsys, monkeypatch) -> None:
    """--apply in a shared checkout fails without --allow-shared-checkout."""
    monkeypatch.setattr(refresh_installed_skills.shared_checkout, "is_main_shared_checkout", lambda _root: True)
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)
    with patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply"]):
        result = refresh_installed_skills.main()
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert result == 1
    assert "Pass --allow-shared-checkout" in combined


def test_apply_allow_shared_checkout_succeeds_in_shared_checkout(tmp_path: Path, monkeypatch) -> None:
    """--apply --allow-shared-checkout works in a shared checkout."""
    monkeypatch.setattr(refresh_installed_skills.shared_checkout, "is_main_shared_checkout", lambda _root: True)
    consumer = tmp_path / "consumer"
    consumer.mkdir()
    _git_init_and_commit(consumer)
    marketplace_json = consumer / ".agents" / "plugins" / "marketplace.json"
    marketplace_json.parent.mkdir(parents=True, exist_ok=True)
    marketplace_json.write_text('{"plugins": []}', encoding="utf-8")
    with (
        patch.object(refresh_installed_skills, "ROOT", consumer),
        patch.object(refresh_installed_skills, "MARKETPLACE_PATH", marketplace_json),
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", consumer / ".agents" / "skills"),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", consumer / ".agents" / "skills" / ".provenance.json"),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0


def test_discover_local_skills_sorted_and_validated(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    valid = skills_path / "mark-valid"
    valid.mkdir(parents=True)
    (valid / "SKILL.md").write_text(
        "---\nname: mark-valid\n---\n\n# Valid\n",
        encoding="utf-8",
    )
    invalid = skills_path / "mark-invalid"
    invalid.mkdir(parents=True)
    (invalid / "SKILL.md").write_text(
        "---\nname: not-the-directory-name\n---\n\n",
        encoding="utf-8",
    )
    (skills_path / "marketplace-skill").mkdir()

    with patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path):
        result = refresh_installed_skills._discover_local_skills(["mark-"])

    assert result == ["mark-valid"]


def test_provenance_rewritten_on_plugin_list_only_change(tmp_path: Path) -> None:
    skills_path = tmp_path / "installed"
    skills_path.mkdir()
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    provenance_path = skills_path / ".provenance.json"
    provenance_path.write_text(
        json.dumps(
            {
                "manifestSha": "current",
                "syncedAt": "2026-07-20T00:00:00",
                "syncedPlugins": ["repo-worker-pack"],
                "syncedSkills": 1,
                "localSkills": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )

    plugins = [
        {"name": "repo-worker-pack"},
        {"name": "superpowers-plus"},
    ]

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["syncedPlugins"] == ["repo-worker-pack", "superpowers-plus"]
    assert provenance["syncedSkills"] == 1
    assert provenance["localSkills"] == []


def test_provenance_records_local_skills(tmp_path: Path) -> None:
    skills_path = tmp_path / "skills"
    skills_path.mkdir()
    local_skill = skills_path / "mark-local"
    local_skill.mkdir()
    (local_skill / "SKILL.md").write_text(
        "---\nname: mark-local\n---\n\n# Local\n",
        encoding="utf-8",
    )
    provenance_path = skills_path / ".provenance.json"
    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    plugin = {"name": "example"}

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": [plugin]}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=[plugin]),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(refresh_installed_skills.shared_checkout, "approve_mutation", return_value=True),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--apply", "--allow-shared-checkout"]),
    ):
        assert refresh_installed_skills.main() == 0

    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["localSkills"] == ["mark-local"]


def test_check_fails_when_provenance_plugin_list_stale(tmp_path: Path, capsys) -> None:
    skills_path = tmp_path / "installed"
    skills_path.mkdir()
    (skills_path / "marketplace-example").mkdir()
    (skills_path / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )
    provenance_path = skills_path / ".provenance.json"
    provenance_path.write_text(
        json.dumps(
            {
                "manifestSha": "current",
                "syncedAt": "2026-07-20T00:00:00",
                "syncedPlugins": ["repo-worker-pack"],
                "syncedSkills": 1,
                "localSkills": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    source_skills = tmp_path / "source" / "skills"
    source_skills.mkdir(parents=True)
    (source_skills / "marketplace-example").mkdir()
    (source_skills / "marketplace-example" / "SKILL.md").write_text(
        "source\n", encoding="utf-8"
    )

    plugins = [
        {"name": "repo-worker-pack"},
        {"name": "superpowers-plus"},
    ]

    with (
        patch.object(refresh_installed_skills, "AGENTS_SKILLS_PATH", skills_path),
        patch.object(refresh_installed_skills, "PROVENANCE_PATH", provenance_path),
        patch.object(refresh_installed_skills, "_load_marketplace_config", return_value={"plugins": plugins}),
        patch.object(refresh_installed_skills, "_get_installed_plugins", return_value=plugins),
        patch.object(refresh_installed_skills, "_get_marketplace_manifest_sha", return_value="current"),
        patch.object(refresh_installed_skills, "_get_plugin_skills_path", return_value=source_skills),
        patch.object(sys, "argv", ["refresh_installed_skills.py", "--check"]),
    ):
        result = refresh_installed_skills.main()

    assert result == 1
    assert "CHECK: Changes would be made" in capsys.readouterr().out
