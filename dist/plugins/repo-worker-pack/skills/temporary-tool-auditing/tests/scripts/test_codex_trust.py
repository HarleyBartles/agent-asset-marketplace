import hashlib
import os
import shutil
import subprocess
from pathlib import Path

import tomllib

import pytest

import codex_trust
from codex_trust import add_project_trust, preview_project_trust, remove_project_trust
from store import AuditStoreError


def test_add_and_remove_exact_worktree_trust_from_new_config(tmp_path):
    project = tmp_path / "worktrees" / "repo-feature"
    config = tmp_path / "codex-home" / "config.toml"

    installed = add_project_trust(project, config)

    assert installed["state"] == "added"
    assert tomllib.loads(config.read_text())["projects"][str(project)]["trust_level"] == "trusted"
    removed = remove_project_trust(installed)
    assert removed["state"] == "removed"
    assert not config.exists()


def test_add_and_remove_trust_preserves_other_user_config(tmp_path):
    project = tmp_path / "worktrees" / "repo-feature"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n\n[projects."Z:/existing"]\ntrust_level = "trusted"\n')

    installed = add_project_trust(project, config)
    assert tomllib.loads(config.read_text())["model"] == "gpt-6.1-sol"
    remove_project_trust(installed)
    parsed = tomllib.loads(config.read_text())
    assert parsed["model"] == "gpt-6.1-sol"
    assert parsed["projects"]["Z:/existing"]["trust_level"] == "trusted"
    assert str(project) not in parsed["projects"]


def test_preexisting_trust_is_preserved_without_claiming_ownership(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text(f'[projects.{project.as_posix()!r}]\ntrust_level = "trusted"\n')

    installed = add_project_trust(project, config)
    before = config.read_bytes()
    removed = remove_project_trust(installed)

    assert installed["state"] == "preexisting"
    assert removed["state"] == "preserved"
    assert config.read_bytes() == before


def test_setup_refuses_to_override_explicit_untrusted_project(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text(f'[projects.{project.as_posix()!r}]\ntrust_level = "untrusted"\n')
    before = config.read_bytes()

    with pytest.raises(AuditStoreError, match="trust-conflict"):
        add_project_trust(project, config)

    assert config.read_bytes() == before


def test_remove_preserves_operator_change_to_trust_level(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    installed = add_project_trust(project, config)
    config.write_text(config.read_text().replace('trust_level = "trusted"', 'trust_level = "untrusted"'))
    before = config.read_bytes()

    removed = remove_project_trust(installed)

    assert removed["state"] == "conflict"
    assert config.read_bytes() == before


def test_remove_cleans_helper_created_empty_table_after_external_key_removal(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    installed = add_project_trust(project, config)
    config.write_text("")

    removed = remove_project_trust(installed)

    assert removed["state"] == "removed"
    assert not config.exists()


@pytest.mark.skipif(os.name == "nt" or not hasattr(os, "setxattr"), reason="POSIX extended attributes only")
def test_config_rewrite_preserves_existing_extended_attributes(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    try:
        os.setxattr(config, "user.temporary-tool-auditing", b"retain")
    except OSError as error:
        pytest.skip(f"filesystem does not support user xattrs: {error.errno}")

    installed = add_project_trust(project, config)

    assert os.getxattr(config, "user.temporary-tool-auditing") == b"retain"
    remove_project_trust(installed)
    assert os.getxattr(config, "user.temporary-tool-auditing") == b"retain"


@pytest.mark.skipif(os.name != "nt" or not shutil.which("icacls"), reason="Windows ACL verification only")
def test_config_rewrite_preserves_windows_acl(tmp_path, monkeypatch):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')

    def acl_text(path):
        result = subprocess.run(["icacls", str(path)], capture_output=True, text=True, check=True)
        return sorted(line.strip().replace(str(path), "") for line in result.stdout.splitlines() if ":(" in line)

    before = acl_text(config)
    replace_file = codex_trust._replace_windows_file

    def verify_staged_acl(original, replacement):
        assert acl_text(replacement) == before
        replace_file(original, replacement)

    monkeypatch.setattr(codex_trust, "_replace_windows_file", verify_staged_acl)
    installed = add_project_trust(project, config)
    after_add = acl_text(config)
    remove_project_trust(installed)
    after_remove = acl_text(config)

    assert before == after_add == after_remove


def test_concurrent_config_edit_between_read_and_replace_is_preserved(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')

    edited = False

    def concurrent_edit(_ownership):
        nonlocal edited
        if edited:
            return
        config.write_text(config.read_text() + 'theme = "light"\n')
        edited = True

    with pytest.raises(AuditStoreError) as error:
        add_project_trust(project, config, persist_intent=concurrent_edit)

    assert error.value.code == "codex-config-changed"
    assert tomllib.loads(config.read_text()) == {"model": "gpt-6.1-sol", "theme": "light"}


def test_concurrent_config_edit_during_teardown_is_preserved(tmp_path, monkeypatch):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    installed = add_project_trust(project, config)
    atomic_write = codex_trust._atomic_write

    def concurrent_edit(path, text, expected, temporary_path=None):
        path.write_text('theme = "light"\n' + path.read_text())
        atomic_write(path, text, expected, temporary_path=temporary_path)

    monkeypatch.setattr(codex_trust, "_atomic_write", concurrent_edit)
    with pytest.raises(AuditStoreError) as error:
        remove_project_trust(installed)

    assert error.value.code == "codex-config-changed"
    parsed = tomllib.loads(config.read_text())
    assert parsed["projects"][str(project)]["trust_level"] == "trusted"
    assert parsed["theme"] == "light"


@pytest.mark.skipif(os.name != "nt", reason="ReplaceFileW partial-failure recovery is Windows-specific")
def test_replacefile_partial_failure_recovers_replacement_instead_of_deleting_it(tmp_path, monkeypatch):
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    expected = codex_trust._snapshot(config)

    def simulate_incomplete_replace(original, replacement):
        original.unlink()
        raise AuditStoreError("codex-replace-incomplete", {"winerror": 1176})

    monkeypatch.setattr(codex_trust, "_replace_windows_file", simulate_incomplete_replace)
    with pytest.raises(AuditStoreError) as error:
        codex_trust._atomic_write(config, 'model = "gpt-6.1-sol"\n', expected)

    assert error.value.code == "codex-config-recovered"
    assert config.read_text() == 'model = "gpt-6.1-sol"\n'
    assert not list(tmp_path.glob(".config.toml-*.tmp"))


@pytest.mark.skipif(os.name != "nt", reason="ReplaceFileW partial-failure recovery is Windows-specific")
def test_failed_partial_recovery_keeps_staged_config_and_returns_its_path(tmp_path, monkeypatch):
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    expected = codex_trust._snapshot(config)

    def simulate_incomplete_replace(original, replacement):
        original.unlink()
        raise AuditStoreError("codex-replace-incomplete")

    def fail_recovery(source, destination):
        raise OSError("simulated recovery failure")

    monkeypatch.setattr(codex_trust, "_replace_windows_file", simulate_incomplete_replace)
    monkeypatch.setattr(codex_trust.os, "replace", fail_recovery)
    with pytest.raises(AuditStoreError) as error:
        codex_trust._atomic_write(config, 'model = "gpt-6.1-sol"\n', expected)

    assert error.value.code == "codex-config-recovery-failed"
    recovery = os.fspath(error.value.details["recovery_file"])
    assert error.value.details["restore_to"] == str(config)
    assert Path(recovery).read_text(encoding="utf-8") == 'model = "gpt-6.1-sol"\n'


@pytest.mark.skipif(os.name != "nt", reason="ReplaceFileW partial-failure recovery is Windows-specific")
def test_replacefile_1177_restores_original_by_file_identity_without_backup(tmp_path, monkeypatch):
    config = tmp_path / "config.toml"
    displaced = tmp_path / ".config.toml-displaced"
    original_text = 'model = "gpt-6.1-sol"\n'
    config.write_text(original_text)
    expected = codex_trust._snapshot(config)

    def simulate_incomplete_replace(original, replacement):
        original.rename(displaced)
        raise AuditStoreError("codex-replace-incomplete", {"winerror": 1177})

    monkeypatch.setattr(codex_trust, "_replace_windows_file", simulate_incomplete_replace)
    with pytest.raises(AuditStoreError, match="codex-config-recovered"):
        codex_trust._atomic_write(config, 'model = "gpt-6.1-sol"\n', expected)

    assert config.read_text() == original_text
    assert not displaced.exists()
    assert not list(tmp_path.glob("*.backup"))


def test_file_identity_recovery_fails_closed_when_windows_id_is_unavailable(tmp_path):
    unrelated = tmp_path / "notes.txt"
    unrelated.write_text("keep this file")

    matches = codex_trust._find_file_by_identity(tmp_path, (0, 0, len("keep this file")), tmp_path / "replacement.tmp")

    assert matches == []
    assert unrelated.read_text() == "keep this file"


@pytest.mark.skipif(os.name != "nt", reason="Windows file identity recovery is Windows-specific")
def test_teardown_recovers_original_config_displaced_before_process_restart(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    displaced = tmp_path / ".config.toml-displaced"
    original_text = 'model = "gpt-6.1-sol"\n'
    config.write_text(original_text)
    installed = add_project_trust(project, config)

    config.rename(displaced)
    removed = remove_project_trust(installed)

    assert removed["state"] == "removed"
    assert tomllib.loads(config.read_text()) == {"model": "gpt-6.1-sol"}
    assert not displaced.exists()


@pytest.mark.skipif(os.name != "nt", reason="Windows staged-write recovery is Windows-specific")
def test_resume_recovers_displaced_config_and_removes_staged_copy(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    displaced = tmp_path / ".config.toml-displaced"
    config.write_text('model = "gpt-6.1-sol"\n')
    installed = add_project_trust(project, config)
    stage = codex_trust._staging_path(config, installed["run_id"])
    stage.write_text('model = "gpt-6.1-sol"\n')
    config.rename(displaced)
    installed["pending_config_write"] = str(stage)

    codex_trust.recover_pending_trust_write(installed)

    assert tomllib.loads(config.read_text())["projects"][str(project)]["trust_level"] == "trusted"
    assert not displaced.exists()
    assert not stage.exists()
    assert "pending_config_write" not in installed


@pytest.mark.skipif(os.name != "nt", reason="Windows hard-link recovery is Windows-specific")
def test_resume_refuses_ambiguous_hard_link_identity_without_pending_stage(tmp_path):
    config = tmp_path / "config.toml"
    displaced = tmp_path / ".config.toml-displaced"
    alias = tmp_path / "config-alias.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    installed = add_project_trust(tmp_path / "repo", config)
    config.rename(displaced)
    os.link(displaced, alias)

    with pytest.raises(AuditStoreError, match="codex-config-recovery-ambiguous"):
        codex_trust.recover_pending_trust_write(installed)

    assert not config.exists()
    assert displaced.exists() and alias.exists()


@pytest.mark.skipif(os.name != "nt", reason="Windows hard-link recovery is Windows-specific")
def test_resume_refuses_ambiguous_hard_link_identity_with_pending_stage(tmp_path):
    config = tmp_path / "config.toml"
    displaced = tmp_path / ".config.toml-displaced"
    alias = tmp_path / "config-alias.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    installed = add_project_trust(tmp_path / "repo", config)
    installed["pending_config_write"] = str(codex_trust._staging_path(config, installed["run_id"]))
    stage = Path(installed["pending_config_write"])
    stage.write_bytes(b'model = "gpt-6.1-sol"\n')
    installed["pending_config_write_sha256"] = hashlib.sha256(stage.read_bytes()).hexdigest()
    config.rename(displaced)
    os.link(displaced, alias)

    with pytest.raises(AuditStoreError, match="codex-config-recovery-ambiguous"):
        codex_trust.recover_pending_trust_write(installed)

    assert not config.exists()
    assert stage.exists()
    assert displaced.exists() and alias.exists()


def test_resume_refuses_incomplete_staged_config_when_no_original_exists(tmp_path):
    config = tmp_path / "config.toml"
    ownership = {
        "state": "added",
        "config_path": str(config),
        "project_path": str(tmp_path / "repo"),
        "config_created": True,
        "run_id": "run-1",
        "config_identity": None,
    }
    stage = codex_trust._staging_path(config, ownership["run_id"])
    stage.write_text('model = "incomplete')
    ownership["pending_config_write"] = str(stage)
    ownership["pending_config_write_sha256"] = hashlib.sha256(b'model = "complete"\n').hexdigest()

    with pytest.raises(AuditStoreError, match="codex-config-recovery-invalid"):
        codex_trust.recover_pending_trust_write(ownership)

    assert not config.exists()
    assert stage.exists()


def test_install_journals_staging_path_before_writing_full_config(tmp_path, monkeypatch):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    ownership_intent = {}

    def persist(ownership):
        ownership_intent.clear()
        ownership_intent.update(ownership)

    def interrupt_after_stage_write(path, text, expected, temporary_path=None):
        Path(temporary_path).write_bytes(text.encode("utf-8"))
        raise SystemExit("simulated interruption")

    monkeypatch.setattr(codex_trust, "_atomic_write", interrupt_after_stage_write)
    with pytest.raises(SystemExit):
        add_project_trust(project, config, persist_intent=persist, run_id="run-1")

    stage = Path(ownership_intent["pending_config_write"])
    assert stage.exists()
    assert ownership_intent["pending_config_write_sha256"]
    assert config.read_text() == 'model = "gpt-6.1-sol"\n'

    codex_trust.recover_pending_trust_write(ownership_intent)

    assert not stage.exists()
    assert "pending_config_write" not in ownership_intent
    assert config.read_text() == 'model = "gpt-6.1-sol"\n'


@pytest.mark.skipif(os.name != "nt", reason="Windows staged-write recovery is Windows-specific")
def test_resume_restores_complete_stage_after_1176_left_original_missing(tmp_path):
    config = tmp_path / "config.toml"
    stage_text = 'model = "gpt-6.1-sol"\n'
    stage = codex_trust._staging_path(config, "run-1")
    stage.write_bytes(stage_text.encode("utf-8"))
    ownership = {
        "state": "added",
        "config_path": str(config),
        "project_path": str(tmp_path / "repo"),
        "config_created": False,
        "run_id": "run-1",
        "config_identity": [1, 987654321, 23],
        "pending_config_write": str(stage),
        "pending_config_write_sha256": hashlib.sha256(stage_text.encode("utf-8")).hexdigest(),
    }

    codex_trust.recover_pending_trust_write(ownership)

    assert config.read_text() == stage_text
    assert not stage.exists()
    assert "pending_config_write" not in ownership


def test_remove_only_owned_trust_key_when_table_gains_unrelated_setting(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    installed = add_project_trust(project, config)
    config.write_text(config.read_text() + 'model = "gpt-6.1-sol"\n')

    removed = remove_project_trust(installed)

    parsed = tomllib.loads(config.read_text())
    assert removed["state"] == "removed"
    assert parsed["projects"][str(project)]["model"] == "gpt-6.1-sol"
    assert "trust_level" not in parsed["projects"][str(project)]


def test_malformed_user_config_is_not_overwritten(tmp_path):
    project = tmp_path / "repo"
    config = tmp_path / "config.toml"
    config.write_text("[projects\ninvalid = true\n")
    before = config.read_bytes()

    with pytest.raises(AuditStoreError, match="codex-config-invalid"):
        add_project_trust(project, config)

    assert config.read_bytes() == before


def test_preview_names_only_the_exact_path_and_does_not_mutate(tmp_path):
    project = tmp_path / "worktrees" / "repo-feature"
    config = tmp_path / "config.toml"
    config.write_text('model = "gpt-6.1-sol"\n')
    before = config.read_bytes()

    preview = preview_project_trust(project, config)

    assert preview == {
        "config_path": str(config.resolve()),
        "project_path": str(project.resolve()),
        "current_trust": None,
        "action": "add-exact-project-path",
    }
    assert config.read_bytes() == before
