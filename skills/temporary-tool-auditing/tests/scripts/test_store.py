import json
import subprocess
import sys
from pathlib import Path

import pytest

from store import AuditStoreError, append_record, load_manifest, save_manifest
import store


def test_manifest_round_trip_is_atomic_and_restrictive(tmp_path):
    save_manifest(tmp_path, {"run_id": "run-1"})
    assert load_manifest(tmp_path) == {"run_id": "run-1"}
    assert not list(tmp_path.glob("*.tmp"))
    if sys.platform != "win32":
        assert (tmp_path / "manifest.json").stat().st_mode & 0o077 == 0


def test_append_sanitises_before_persisting_and_returns_redactions(tmp_path):
    record = append_record(tmp_path, "events", {"arguments": {"password": "disk-SENTINEL"}})
    contents = (tmp_path / "events.jsonl").read_bytes()
    assert b"disk-SENTINEL" not in contents
    assert b"[REDACTED]" in contents
    assert record["redactions"]
    assert json.loads(contents.splitlines()[0]) == record


def test_append_rejects_path_traversal_without_leaking_payload(tmp_path):
    with pytest.raises(AuditStoreError) as error:
        append_record(tmp_path, "../outside", {"password": "error-SENTINEL"})
    assert error.value.code == "invalid-record-name"
    assert "error-SENTINEL" not in str(error.value)
    assert not (tmp_path.parent / "outside.jsonl").exists()


def test_append_rejects_unmanaged_log_names(tmp_path):
    with pytest.raises(AuditStoreError, match="invalid-record-name"):
        append_record(tmp_path, "unbounded-extra", {"payload": "data"})


def test_parallel_process_appends_are_complete_and_unique(tmp_path):
    store_file = Path(__file__).resolve().parents[2] / "scripts" / "store.py"
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from store import append_record; "
        "append_record(sys.argv[2], 'events', {'worker': sys.argv[3]})"
    )
    processes = [
        subprocess.Popen([sys.executable, "-c", code, str(store_file.parent), str(tmp_path), str(i)]) for i in range(12)
    ]
    assert [process.wait(timeout=15) for process in processes] == [0] * 12
    rows = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text().splitlines()]
    assert len(rows) == 12
    assert {row["worker"] for row in rows} == {str(i) for i in range(12)}


def test_atomic_manifest_failure_keeps_old_manifest(tmp_path, monkeypatch):
    import store

    save_manifest(tmp_path, {"run_id": "old"})

    def fail_replace(*_args):
        raise OSError("raw diagnostic must not escape")

    monkeypatch.setattr(store.os, "replace", fail_replace)
    with pytest.raises(AuditStoreError) as error:
        save_manifest(tmp_path, {"run_id": "new"})
    assert error.value.code == "manifest-write-failed"
    assert load_manifest(tmp_path) == {"run_id": "old"}
    assert "raw diagnostic" not in str(error.value)


def test_lock_timeout_is_a_safe_error(tmp_path, monkeypatch):
    import store

    save_manifest(tmp_path, {"run_id": "run-1"})
    calls = iter([0, 0, 11])
    monkeypatch.setattr(store.time, "monotonic", lambda: next(calls))
    monkeypatch.setattr(store.time, "sleep", lambda _seconds: None)
    if sys.platform == "win32":
        import msvcrt

        monkeypatch.setattr(msvcrt, "locking", lambda *_args: (_ for _ in ()).throw(OSError()))
    else:
        import fcntl

        monkeypatch.setattr(fcntl, "flock", lambda *_args: (_ for _ in ()).throw(BlockingIOError()))
    with pytest.raises(AuditStoreError) as error:
        load_manifest(tmp_path)
    assert error.value.code == "lock-timeout"


def test_event_log_has_a_finite_storage_ceiling(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "MAX_EVENT_LOG_BYTES", 100)
    append_record(tmp_path, "events", {"event": "pre", "tool_name": "Bash", "call_id": "one"})
    with pytest.raises(AuditStoreError, match="event-log-limit-reached"):
        append_record(tmp_path, "events", {"event": "pre", "tool_name": "Bash", "call_id": "two"})
    assert (tmp_path / "events.jsonl").stat().st_size <= 100


def test_auxiliary_logs_are_bounded_with_reserved_cleanup_space(tmp_path, monkeypatch):
    ordinary = {"code": "ordinary"}
    cleanup = {"code": "recorder-health-control"}

    probe = tmp_path / "probe"
    append_record(probe, "controls", ordinary)
    ordinary_size = (probe / "controls.jsonl").stat().st_size
    probe_cleanup = tmp_path / "probe-cleanup"
    append_record(probe_cleanup, "controls", cleanup)
    cleanup_size = (probe_cleanup / "controls.jsonl").stat().st_size
    monkeypatch.setattr(store, "CONTROL_LOG_CLEANUP_RESERVE_BYTES", cleanup_size)
    monkeypatch.setattr(store, "MAX_CONTROL_LOG_BYTES", ordinary_size * 2 + cleanup_size)

    append_record(tmp_path, "controls", ordinary)
    append_record(tmp_path, "controls", ordinary)
    with pytest.raises(AuditStoreError, match="control-log-limit-reached"):
        append_record(tmp_path, "controls", ordinary)
    append_record(tmp_path, "controls", cleanup)
    assert (tmp_path / "controls.jsonl").stat().st_size <= store.MAX_CONTROL_LOG_BYTES


def test_manifest_has_a_size_limit_and_cleanup_reserve(tmp_path, monkeypatch):
    active = {"run_id": "x" * 90}
    removed = {"run_id": "x" * 90, "registration_state": "removed"}
    verified = {"run_id": "x" * 90, "registration_state": "teardown-verified"}
    verified_size = len(store._safe_json(verified, "encode-failed")[0])
    monkeypatch.setattr(store, "MAX_MANIFEST_BYTES", 200)
    monkeypatch.setattr(store, "MANIFEST_CLEANUP_RESERVE_BYTES", 50)

    with pytest.raises(AuditStoreError, match="manifest-size-limit-reached"):
        save_manifest(tmp_path, active)
    save_manifest(tmp_path, removed)
    save_manifest(tmp_path, verified)
    assert (tmp_path / "manifest.json").stat().st_size == verified_size
