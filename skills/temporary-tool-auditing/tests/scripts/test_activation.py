"""Capture-time isolation for the global dispatcher."""

import json
import sys
import types
import shutil
import time
from pathlib import Path
import pytest

from activation import ACTIVATION_ENV, current_registry_path, dispatch, enable, disable
from store import AuditStoreError, create_manifest, load_manifest


def install_global_fixtures(registry):
    root = Path(registry).resolve().parent
    source = Path(__file__).resolve().parents[2] / "scripts"
    names = ("activation.py", "record.py", "runtime.py", "store.py", "sanitize.py")
    for name in names:
        shutil.copyfile(source / name, root / name)
    shutil.copyfile(source / "activation.py", root / "dispatch.py")
    hashes = {name: __import__("hashlib").sha256((root / name).read_bytes()).hexdigest() for name in names}
    hashes["dispatch.py"] = __import__("hashlib").sha256((root / "dispatch.py").read_bytes()).hexdigest()
    (root / "owner.json").write_text(json.dumps({"state": "installed", "file_hashes": hashes}))


def make_run(tmp_path, name, session, project):
    run = tmp_path / name
    create_manifest(
        run,
        {
            "run_id": name,
            "runtime": "codex",
            "project_root": str(project),
            "capture_session_id": session,
            "global_dispatcher": True,
            "expires_at": time.time() + 3600,
            "armed": True,
            "detail": "status",
            "registration_state": "installed",
        },
    )
    helpers = run / "scripts"
    helpers.mkdir()
    source = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("record.py", "runtime.py", "store.py", "sanitize.py"):
        shutil.copyfile(source / name, helpers / name)
    return run


def test_dispatch_filters_before_any_persistence(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    run = make_run(tmp_path, "run", "parent", project)
    registry = tmp_path / "activation.json"
    install_global_fixtures(registry)
    enable(registry, run, "parent", manage_switch=False)
    baseline = set(run.iterdir())
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": "other",
        "cwd": str(project),
        "tool_use_id": "foreign",
        "tool_name": "Bash",
    }
    assert dispatch(registry, payload, time.time()) is False
    assert set(run.iterdir()) == baseline
    payload["session_id"] = "parent"
    payload["cwd"] = str(tmp_path / "other-project")
    assert dispatch(registry, payload, time.time()) is False
    payload["cwd"] = str(project)
    payload.pop("session_id")
    assert dispatch(registry, payload, time.time()) is False
    assert not (run / "events.jsonl").exists()
    assert not (run / "executed").exists()


def test_same_worktree_sessions_and_children_remain_isolated(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    first = make_run(tmp_path, "first", "parent-1", project)
    second = make_run(tmp_path, "second", "parent-2", project)
    registry = tmp_path / "activation.json"
    install_global_fixtures(registry)
    enable(registry, first, "parent-1", manage_switch=False)
    enable(registry, second, "parent-2", manage_switch=False)
    for session, child in [("parent-1", None), ("parent-1", "child-1"), ("parent-2", None)]:
        assert dispatch(
            registry,
            {
                "hook_event_name": "PreToolUse",
                "session_id": session,
                "agent_id": child,
                "cwd": str(project),
                "tool_use_id": session + str(child),
                "tool_name": "Bash",
                "tool_input": {"password": "never-persist-me"},
            },
            time.time(),
        )
    rows = [json.loads(row) for row in (first / "events.jsonl").read_text().splitlines()]
    assert len(rows) == 2
    assert {row["session_id"] for row in rows} == {"parent-1"}
    assert "never-persist-me" not in (first / "events.jsonl").read_text()
    assert len((second / "events.jsonl").read_text().splitlines()) == 1
    disable(registry, first, manage_switch=False)
    assert dispatch(registry, {"session_id": "parent-1", "cwd": str(project)}, time.time()) is False
    assert len((first / "events.jsonl").read_text().splitlines()) == 2
    assert len(json.loads(registry.read_text())["entries"]) == 1
    assert load_manifest(first)["run_id"] == "first"


def test_expired_activation_and_missing_registry_are_inert(tmp_path):
    registry = tmp_path / "activation.json"
    assert dispatch(registry, {}, 100) is False
    project = tmp_path / "project"
    project.mkdir()
    run = make_run(tmp_path, "run", "parent", project)
    enable(registry, run, "parent", manage_switch=False)
    assert dispatch(registry, {"session_id": "parent", "cwd": str(project)}, load_manifest(run)["expires_at"]) is False
    assert not (run / "events.jsonl").exists()


def test_second_run_cannot_replace_active_run_for_same_session_and_worktree(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    first = make_run(tmp_path, "first", "parent", project)
    second = make_run(tmp_path, "second", "parent", project)
    registry = tmp_path / "activation.json"
    enable(registry, first, "parent", manage_switch=False)
    with pytest.raises(AuditStoreError, match="activation-conflict"):
        enable(registry, second, "parent", manage_switch=False)
    entries = json.loads(registry.read_text())["entries"]
    assert [item["run_id"] for item in entries] == ["first"]


def test_dispatcher_reads_current_environment_pointer_each_time(tmp_path, monkeypatch):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    monkeypatch.setattr("activation.sys.platform", "linux")
    monkeypatch.setenv(ACTIVATION_ENV, str(first))
    assert current_registry_path() == first
    monkeypatch.setenv(ACTIVATION_ENV, str(second))
    assert current_registry_path() == second
    monkeypatch.delenv(ACTIVATION_ENV)
    assert current_registry_path() == Path.home() / ".codex" / "tool-auditing" / "activations.json"


def test_windows_dispatcher_uses_fresh_user_registry_value_not_stale_process_env(tmp_path, monkeypatch):
    value = {"path": str(tmp_path / "active.json")}

    class FakeKey:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    def open_key(*_args):
        return FakeKey()

    def query_value(_key, _name):
        if value["path"] is None:
            raise FileNotFoundError
        return value["path"], 2

    fake_winreg = types.SimpleNamespace(HKEY_CURRENT_USER=1, OpenKey=open_key, QueryValueEx=query_value)
    monkeypatch.setitem(sys.modules, "winreg", fake_winreg)
    monkeypatch.setattr("activation.sys.platform", "win32")
    monkeypatch.setenv(ACTIVATION_ENV, str(tmp_path / "stale.json"))
    assert current_registry_path() == Path(value["path"])
    value["path"] = None
    assert current_registry_path() is None


def test_windows_enable_disable_flips_owned_current_user_switch(tmp_path, monkeypatch):
    value = {"path": None}

    class FakeKey:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    def open_key(*args):
        if len(args) == 4:
            assert args[3] == (2 | 4)
        return FakeKey()

    def query_value(_key, _name):
        if value["path"] is None:
            raise FileNotFoundError
        return value["path"], 2

    def set_value(_key, _name, _reserved, _kind, new_value):
        value["path"] = new_value

    def delete_value(_key, _name):
        value["path"] = None

    fake_winreg = types.SimpleNamespace(
        HKEY_CURRENT_USER=1,
        KEY_SET_VALUE=2,
        KEY_QUERY_VALUE=4,
        REG_EXPAND_SZ=3,
        OpenKey=open_key,
        QueryValueEx=query_value,
        SetValueEx=set_value,
        DeleteValue=delete_value,
        CloseKey=lambda _key: None,
    )
    monkeypatch.setitem(sys.modules, "winreg", fake_winreg)
    monkeypatch.setattr("activation.sys.platform", "win32")
    project = tmp_path / "project"
    project.mkdir()
    run = make_run(tmp_path, "run", "parent", project)
    registry = tmp_path / "activation.json"
    enable(registry, run, "parent")
    assert Path(value["path"]) == registry
    assert current_registry_path() == registry
    disable(registry, run)
    assert value["path"] is None
    assert current_registry_path() is None


def test_global_dispatcher_cli_exposes_help_and_check():
    import subprocess

    script = Path(__file__).resolve().parents[2] / "scripts" / "activation.py"
    help_result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, check=False)
    check_result = subprocess.run([sys.executable, str(script), "--check"], capture_output=True, text=True, check=False)
    assert help_result.returncode == 0
    assert "usage:" in help_result.stdout.lower()
    assert check_result.returncode == 0
