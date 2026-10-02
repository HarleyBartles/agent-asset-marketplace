import json
import time

from assessment import assess
from store import save_manifest


def make_run(path, events, **updates):
    now = time.time()
    manifest = {
        "run_id": "run-1",
        "runtime": "codex",
        "armed": False,
        "activation_verified": True,
        "intervals": [{"start": now - 20, "end": now + 1}],
        "subject_completed_at": now,
        "controls": [{"call_id": "control-1"}],
        "health": [],
    }
    manifest.update(updates)
    save_manifest(path, manifest)
    (path / "events.jsonl").write_text("".join(json.dumps(row) + "\n" for row in events))


def event(kind, call, session="subject-1", **extra):
    return {"run_id": "run-1", "event": kind, "call_id": call, "session_id": session, **extra}


def test_no_attempt_claim_requires_positive_control_and_completed_coverage(tmp_path):
    make_run(tmp_path, [event("pre", "control-1", "control-session")])
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert result["claim_supported"] is True
    assert result["attempt_count"] == 0


def test_missing_control_cannot_prove_no_tools(tmp_path):
    make_run(tmp_path, [], controls=[])
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert result["claim_supported"] is False
    assert "missing-positive-control" in result["limitations"]


def test_attempts_are_paired_and_controls_excluded(tmp_path):
    make_run(
        tmp_path,
        [
            event("pre", "control-1", "control-session"),
            event("pre", "tool-1"),
            event("post", "tool-1", outcome_status="success"),
        ],
    )
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert result["attempt_count"] == 1
    assert result["paired_count"] == 1
    assert result["claim_supported"] is False


def test_unmatched_attempt_redactions_and_health_prevent_clean_claim(tmp_path):
    make_run(tmp_path, [event("pre", "tool-1", redactions=["$.arguments.token"])])
    (tmp_path / "health.jsonl").write_text('{"code":"recorder-unavailable"}\n')
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert "unmatched-pre" in result["limitations"]
    assert "redactions-present" in result["limitations"]
    assert "recorder-health-failure" in result["limitations"]


def test_gap_or_late_post_does_not_repair_coverage(tmp_path):
    now = time.time()
    make_run(
        tmp_path,
        [event("pre", "control-1", "control-session"), event("post", "control-1", "control-session")],
        intervals=[{"start": now - 20, "end": now - 10}, {"start": now - 5, "end": now + 1}],
        coverage_gaps=[{"start": now - 10, "end": now - 5}],
    )
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert "coverage-gap" in result["limitations"]
    assert result["claim_supported"] is False


def test_devin_child_needs_serialized_dispatch_boundaries(tmp_path):
    now = time.time()
    make_run(
        tmp_path,
        [event("pre", "control-1", "control-session"), event("post", "control-1", "control-session")],
        runtime="devin",
        dispatches=[{"call_id": "dispatch-1", "start": now - 8, "end": now - 4, "serialized": False}],
    )
    result = assess(tmp_path, {"agent_id": "child-1", "kind": "child"})
    assert result["claim_supported"] is False
    assert "devin-child-attribution-ambiguous" in result["limitations"]
