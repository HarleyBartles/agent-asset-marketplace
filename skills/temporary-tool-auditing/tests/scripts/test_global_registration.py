"""The stable user hook is installed once and preserves other handlers."""

import json
from pathlib import Path

import pytest

from global_registration import global_install_present, install_global
from store import AuditStoreError


def test_global_install_is_idempotent_and_preserves_unrelated_hook(tmp_path):
    home = tmp_path / "codex"
    home.mkdir()
    config = home / "hooks.json"
    unrelated = {"matcher": "Bash", "hooks": [{"type": "command", "command": "other-hook"}]}
    config.write_text(json.dumps({"description": "keep", "hooks": {"PreToolUse": [unrelated]}}))
    source = Path(__file__).resolve().parents[2] / "scripts"
    first = install_global(home, source)
    dispatcher = home / "tool-auditing" / "dispatch.py"
    original_script = dispatcher.read_bytes()
    second = install_global(home, source)
    data = json.loads(config.read_text())
    assert first["installed"] is True
    assert second["already_installed"] is True
    assert dispatcher.read_bytes() == original_script
    assert data["description"] == "keep"
    assert data["hooks"]["PreToolUse"].count(unrelated) == 1
    assert len(data["hooks"]["PreToolUse"]) == 2
    assert global_install_present(home)
    assert (home / "tool-auditing" / "dispatch.py").is_file()


def test_global_install_refuses_silent_script_replacement(tmp_path):
    home = tmp_path / "codex"
    source = Path(__file__).resolve().parents[2] / "scripts"
    install_global(home, source)
    dispatcher = home / "tool-auditing" / "dispatch.py"
    dispatcher.write_text("# changed without review\n")
    with pytest.raises(AuditStoreError, match="global-install-conflict"):
        install_global(home, source)


def test_global_install_refuses_malformed_configuration(tmp_path):
    home = tmp_path / "codex"
    home.mkdir()
    (home / "hooks.json").write_text("{invalid")
    source = Path(__file__).resolve().parents[2] / "scripts"
    with pytest.raises(AuditStoreError, match="global-hook-config-invalid"):
        install_global(home, source)


def test_install_refreshes_only_owned_helpers_when_source_changes(tmp_path):
    home = tmp_path / "codex"
    source = tmp_path / "source"
    source.mkdir()
    canonical = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("activation.py", "record.py", "runtime.py", "store.py", "sanitize.py"):
        (source / name).write_bytes((canonical / name).read_bytes())
    install_global(home, source)
    config_before = (home / "hooks.json").read_bytes()
    (source / "record.py").write_text((source / "record.py").read_text() + "\n# reviewed helper update\n")
    with pytest.raises(AuditStoreError, match="global-helper-refresh-requires-review"):
        install_global(home, source)
    result = install_global(home, source, refresh_helpers=True)
    assert result["updated_helpers"] is True
    assert (home / "hooks.json").read_bytes() == config_before
    assert global_install_present(home)
    assert (home / "tool-auditing" / "record.py").read_bytes() == (source / "record.py").read_bytes()
