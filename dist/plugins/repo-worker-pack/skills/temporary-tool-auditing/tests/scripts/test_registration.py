import json
import sys
import tomllib
from pathlib import Path
from unittest.mock import patch

import pytest

from registration import install, remove
from store import load_manifest, save_manifest


@pytest.fixture(autouse=True)
def isolated_codex_home(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex-home"))


def handler_commands(path, event):
    return [entry["hooks"][0]["command"] for entry in json.loads(path.read_text())["hooks"][event]]


def test_install_preserves_existing_fields_and_remove_only_owned_entry(tmp_path):
    project = tmp_path / "repo with spaces"
    run = project / ".audit-runs" / "run-1"
    config = project / ".codex" / "hooks.json"
    config.parent.mkdir(parents=True)
    config.write_text(
        json.dumps(
            {
                "description": "keep",
                "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "keep-me"}]}]},
            }
        )
    )
    save_manifest(run, {"run_id": "run-1", "runtime": "codex", "armed": False, "cleanup_required": False})

    installed = install(run, project, "codex")
    assert installed["registration_state"] == "installed"
    assert "keep-me" in handler_commands(config, "PreToolUse")
    assert len(handler_commands(config, "PreToolUse")) == 2
    # Another actor's new entry survives cleanup.
    data = json.loads(config.read_text())
    data["hooks"]["PreToolUse"].append({"matcher": "Write", "hooks": [{"type": "command", "command": "new-unrelated"}]})
    config.write_text(json.dumps(data))
    removed = remove(run)
    assert removed["config_absent"] is True
    assert handler_commands(config, "PreToolUse") == ["keep-me", "new-unrelated"]
    manifest = load_manifest(run)
    assert manifest["cleanup_required"] is True


def test_install_is_idempotent_and_conflicts_with_another_active_run(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    run2 = project / ".audit-runs" / "two"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    save_manifest(run2, {"run_id": "two", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    install(run, project, "codex")
    try:
        install(run2, project, "codex")
    except Exception as error:
        assert getattr(error, "code", None) == "registration-conflict"
    else:
        raise AssertionError("second run should be rejected")
    remove(run)
    assert not (tmp_path / "codex-home" / "config.toml").exists()


def test_remove_keeps_modified_owned_entry_as_conflict(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    config = project / ".codex" / "hooks.json"
    data = json.loads(config.read_text())
    data["hooks"]["PreToolUse"][0]["hooks"][0]["timeout"] = 4
    config.write_text(json.dumps(data))
    result = remove(run)
    assert result["conflicts"]
    assert json.loads(config.read_text())["hooks"]["PreToolUse"]


def test_remove_recovers_an_interrupted_install_from_manifest_intent(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    config = project / ".codex" / "hooks.json"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": True})
    install(run, project, "codex")
    manifest = load_manifest(run)
    manifest["registration_state"] = "installing"
    save_manifest(run, manifest)
    assert config.exists()
    result = remove(run)
    assert result["registration_state"] == "removed"
    assert result["config_absent"] is True
    assert load_manifest(run)["cleanup_required"] is True


def test_install_refuses_identical_unowned_hook_without_claiming_it(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    config = project / ".codex" / "hooks.json"
    entry = {"matcher": "", "hooks": [{"type": "command", "command": "owned-by-someone-else"}]}
    config.parent.mkdir(parents=True)
    config.write_text(json.dumps({"hooks": {"PreToolUse": [entry]}}))
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    with patch("registration.render_handlers", return_value={"PreToolUse": [entry]}):
        try:
            install(run, project, "codex")
        except Exception as error:
            assert getattr(error, "code", None) == "registration-conflict"
        else:
            raise AssertionError("an identical unowned hook must not be adopted")
    assert json.loads(config.read_text())["hooks"]["PreToolUse"] == [entry]
    assert load_manifest(run).get("owned_entries", []) == []


def test_remove_checks_owner_before_mutating_hook_configuration(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    config = project / ".codex" / "hooks.json"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    before = config.read_bytes()
    owner = project / ".codex" / ".temporary-tool-auditing-owner.json"
    owner.write_text(json.dumps({"run_id": "other", "run_dir": "elsewhere"}))
    try:
        remove(run)
    except Exception as error:
        assert getattr(error, "code", None) == "registration-conflict"
    else:
        raise AssertionError("removal must reject an owner mismatch")
    assert config.read_bytes() == before


def test_remove_fails_closed_when_owner_marker_is_missing(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    config = project / ".codex" / "hooks.json"
    before = config.read_bytes()
    (project / ".codex" / ".temporary-tool-auditing-owner.json").unlink()
    try:
        remove(run)
    except Exception as error:
        assert getattr(error, "code", None) == "registration-owner-missing"
    else:
        raise AssertionError("removal without its owner marker must fail closed")
    assert config.read_bytes() == before


def test_remove_does_not_miss_owned_entry_whose_command_was_changed(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    config = project / ".codex" / "hooks.json"
    data = json.loads(config.read_text())
    entry = data["hooks"]["PreToolUse"][0]
    entry["hooks"][0]["command"] = "malicious replacement"
    entry["hooks"][0]["commandWindows"] = "malicious replacement"
    config.write_text(json.dumps(data))
    before = config.read_bytes()
    result = remove(run)
    assert result["registration_state"] == "conflict"
    assert result["conflicts"]
    assert config.read_bytes() == before
    assert (project / ".codex" / ".temporary-tool-auditing-owner.json").exists()


def test_removal_deletes_empty_registration_root_created_by_helper(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    root = project / ".codex"
    assert root.exists()
    remove(run)
    assert not root.exists()


def test_install_rejects_removed_run_under_registration_lock(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "registration_state": "removed"})
    try:
        install(run, project, "codex")
    except Exception as error:
        assert getattr(error, "code", None) == "registration-not-installable"
    else:
        raise AssertionError("a removed audit cannot recreate its hook")
    assert not (project / ".codex" / "hooks.json").exists()


def test_existing_empty_hook_config_is_preserved_on_remove(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    config = project / ".codex" / "hooks.json"
    config.parent.mkdir(parents=True)
    config.write_text('{"hooks":{}}', encoding="utf-8")
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False})
    install(run, project, "codex")
    assert load_manifest(run)["registration_config_created"] is False
    remove(run)
    assert config.exists()
    assert json.loads(config.read_text(encoding="utf-8")) == {"hooks": {}}


def test_install_records_the_interpreter_used_by_hook_templates(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False})
    install(run, project, "codex")
    manifest = load_manifest(run)
    assert manifest["hook_interpreter"] == sys.executable
    assert Path(manifest["lifecycle_cli_path"]).name == "auditctl.py"


def test_codex_install_temporarily_trusts_exact_project_then_removes_it(tmp_path):
    project = tmp_path / "worktrees" / "repo-feature"
    run = tmp_path / "audit-runs" / "one"
    codex_config = tmp_path / "codex-home" / "config.toml"
    codex_config.parent.mkdir()
    codex_config.write_text('model = "gpt-6.1-sol"\n')
    save_manifest(run, {"run_id": "one", "runtime": "codex", "project_root": str(project), "armed": False})

    installed = install(run, project, "codex")

    assert installed["restart_required"] is True
    assert installed["trust"] == "added"
    parsed = tomllib.loads(codex_config.read_text())
    assert parsed["projects"][str(project)]["trust_level"] == "trusted"
    assert str(project.parent) not in parsed["projects"]
    removed = remove(run)
    assert removed["owned_trust_absent"] is True
    assert removed["restart_required"] is True
    assert tomllib.loads(codex_config.read_text()) == {"model": "gpt-6.1-sol"}


def test_codex_install_refuses_to_replace_explicitly_untrusted_path(tmp_path):
    project = tmp_path / "repo"
    run = tmp_path / "audit-runs" / "one"
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(f'[projects.{project.as_posix()!r}]\ntrust_level = "untrusted"\n')
    before = config.read_bytes()
    save_manifest(run, {"run_id": "one", "runtime": "codex", "project_root": str(project), "armed": False})

    with pytest.raises(Exception) as error:
        install(run, project, "codex")

    assert getattr(error.value, "code", None) == "trust-conflict"
    assert config.read_bytes() == before


def test_codex_remove_preserves_preexisting_trusted_path(tmp_path):
    project = tmp_path / "repo"
    run = tmp_path / "audit-runs" / "one"
    codex_home = tmp_path / "codex-home"
    codex_home.mkdir()
    config = codex_home / "config.toml"
    config.write_text(f'[projects.{project.as_posix()!r}]\ntrust_level = "trusted"\n')
    before = config.read_bytes()
    save_manifest(run, {"run_id": "one", "runtime": "codex", "project_root": str(project), "armed": False})

    assert install(run, project, "codex")["trust"] == "preexisting"
    remove(run)

    assert config.read_bytes() == before


def test_remove_recovers_intent_journal_when_owner_and_config_were_not_written(tmp_path):
    from runtime import render_handlers

    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    entry = render_handlers("codex", run / "scripts" / "record.py")["PreToolUse"][0]
    save_manifest(
        run,
        {
            "run_id": "one",
            "runtime": "codex",
            "project_root": str(project),
            "registration_root": str(project / ".codex"),
            "registration_state": "removing",
            "owned_entries": [{"event": "PreToolUse", "entry": entry}],
            "cleanup_required": True,
        },
    )
    result = remove(run)
    assert result["registration_state"] == "removed"
    assert result["config_absent"] is True
