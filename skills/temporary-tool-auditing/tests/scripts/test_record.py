import json
import io
import time
from unittest.mock import patch

from record import record_event
from store import save_manifest


def make_run(path, **updates):
    manifest = {
        "run_id": "run-1",
        "runtime": "codex",
        "expires_at": time.time() + 60,
        "armed": True,
        "detail": "status",
        "health": [],
    }
    manifest.update(updates)
    save_manifest(path, manifest)


def test_record_event_sanitizes_and_persists_normalized_event(tmp_path):
    make_run(tmp_path)
    ok = record_event(
        tmp_path,
        {
            "hook_event_name": "PreToolUse",
            "session_id": "s1",
            "tool_use_id": "c1",
            "tool_name": "Bash",
            "tool_input": {"password": "pw-SENTINEL"},
        },
        time.time(),
    )
    assert ok
    contents = (tmp_path / "events.jsonl").read_text()
    assert "pw-SENTINEL" not in contents
    assert json.loads(contents)["arguments"]["password"] == "[REDACTED]"


def test_expired_or_disarmed_run_does_not_record(tmp_path):
    make_run(tmp_path, expires_at=100, armed=True)
    assert not record_event(tmp_path, {"hook_event_name": "PreToolUse"}, 100)


def test_hook_entrypoint_emits_no_control_output(tmp_path):
    from record import main

    output = io.StringIO()
    with patch("record.sys.stdin", io.StringIO('{"hook_event_name":"PreToolUse"}')), patch("record.sys.stdout", output):
        assert main(["--run-dir", str(tmp_path)]) == 0
    assert output.getvalue() == ""


def test_late_outcome_is_kept_only_for_an_observed_in_window_attempt(tmp_path):
    make_run(tmp_path, expires_at=100, armed=True)
    assert record_event(
        tmp_path,
        {"hook_event_name": "PreToolUse", "session_id": "s", "tool_use_id": "late-1", "tool_name": "Bash"},
        99,
    )
    make_run(tmp_path, expires_at=100, armed=False)
    assert record_event(
        tmp_path,
        {"hook_event_name": "PostToolUse", "session_id": "s", "tool_use_id": "late-1", "tool_name": "Bash"},
        101,
    )
    assert not record_event(
        tmp_path,
        {"hook_event_name": "PostToolUse", "session_id": "s", "tool_use_id": "unpaired", "tool_name": "Bash"},
        101,
    )
    rows = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text().splitlines()]
    assert rows[-1]["late_outcome"] is True
    make_run(tmp_path, expires_at=200, armed=False)
    assert not record_event(tmp_path, {"hook_event_name": "PreToolUse"}, 100)


def test_explicit_disarm_makes_retained_recorder_inert(tmp_path):
    make_run(tmp_path, expires_at=200, armed=True)
    assert record_event(
        tmp_path,
        {"hook_event_name": "PreToolUse", "session_id": "s", "tool_use_id": "disarm-1", "tool_name": "Bash"},
        100,
    )
    make_run(tmp_path, expires_at=200, armed=False, late_outcomes_allowed=False, registration_state="removed")
    assert not record_event(
        tmp_path,
        {"hook_event_name": "PostToolUse", "session_id": "s", "tool_use_id": "disarm-1", "tool_name": "Bash"},
        101,
    )


def test_inflight_event_rechecks_disarm_before_append(tmp_path):
    make_run(tmp_path, lifecycle_cli_path="C:/auditctl.py")

    def disarm_during_normalization(*_args, **_kwargs):
        make_run(
            tmp_path,
            armed=False,
            late_outcomes_allowed=False,
            registration_state="removed",
            lifecycle_cli_path="C:/auditctl.py",
        )
        return {
            "event": "pre",
            "session_id": "s1",
            "call_id": "inflight",
            "tool_name": "Bash",
            "arguments": {},
            "outcome_status": "observed-unknown",
        }

    with patch("record.normalize_event", side_effect=disarm_during_normalization):
        assert not record_event(tmp_path, {"hook_event_name": "PreToolUse"}, time.time())

    assert not (tmp_path / "events.jsonl").exists()
