import json
import time

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
    make_run(tmp_path, expires_at=200, armed=False)
    assert not record_event(tmp_path, {"hook_event_name": "PreToolUse"}, 100)
