import json
from unittest.mock import patch

from registration import install, remove
from store import load_manifest, save_manifest


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


def test_removal_deletes_empty_registration_root_created_by_helper(tmp_path):
    project = tmp_path / "repo"
    run = project / ".audit-runs" / "one"
    save_manifest(run, {"run_id": "one", "runtime": "codex", "armed": False, "cleanup_required": False})
    install(run, project, "codex")
    root = project / ".codex"
    assert root.exists()
    remove(run)
    assert not root.exists()
