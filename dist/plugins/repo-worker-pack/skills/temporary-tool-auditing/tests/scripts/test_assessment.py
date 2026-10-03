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
    return {
        "run_id": "run-1",
        "event": kind,
        "call_id": call,
        "session_id": session,
        "received_at": time.time(),
        **extra,
    }


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


def test_missing_session_identity_is_not_silently_excluded(tmp_path):
    row = event("pre", "uncorrelated")
    row["session_id"] = None
    make_run(tmp_path, [row])
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert "missing-session-id" in result["limitations"]
    assert result["claim_supported"] is False


def test_unmatched_post_and_duplicate_pre_are_visible(tmp_path):
    make_run(
        tmp_path,
        [
            event("pre", "call-1"),
            event("pre", "call-1"),
            event("post", "orphan"),
        ],
    )
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert "duplicate-pre" in result["limitations"]
    assert "unmatched-pre" in result["limitations"]
    assert "unmatched-post" in result["limitations"]


def test_late_post_pairs_with_attempt_inside_coverage(tmp_path):
    now = time.time()
    make_run(
        tmp_path,
        [
            event("pre", "call-1", received_at=now - 3),
            event("post", "call-1", received_at=now + 2),
        ],
        intervals=[{"start": now - 10, "end": now}],
        subject_completed_at=now,
    )
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert result["paired_count"] == 1
    assert "unmatched-pre" not in result["limitations"]


def test_lifecycle_control_calls_are_excluded_but_need_a_separate_positive_control(tmp_path):
    make_run(
        tmp_path,
        [
            event("pre", "control-1", "control-session"),
            event("pre", "auditctl-1", control_operation="start"),
            event("post", "auditctl-1", control_operation="start"),
        ],
    )
    result = assess(tmp_path, {"session_id": "subject-1"})
    assert result["attempt_count"] == 0
    assert result["claim_supported"] is True


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
    make_run(
        tmp_path,
        [
            event("pre", "control-1", "control-session"),
            event("post", "control-1", "control-session"),
            event("pre", "dispatch-1", tool_name="run_subagent"),
            event("pre", "dispatch-2", tool_name="run_subagent"),
            event("post", "dispatch-1", tool_name="run_subagent"),
            event("post", "dispatch-2", tool_name="run_subagent"),
        ],
        runtime="devin",
    )
    result = assess(tmp_path, {"dispatch_call_id": "dispatch-1", "kind": "child"})
    assert result["claim_supported"] is False
    assert "devin-child-attribution-ambiguous" in result["limitations"]


def test_devin_child_counts_tools_inside_one_serialized_dispatch(tmp_path):
    now = time.time()
    make_run(
        tmp_path,
        [
            event("pre", "control-1", "control-session"),
            event("post", "control-1", "control-session"),
            event("pre", "dispatch-1", tool_name="run_subagent", received_at=now - 8),
            event("pre", "child-tool", received_at=now - 6),
            event("post", "child-tool", received_at=now - 5),
            event("post", "dispatch-1", tool_name="run_subagent", received_at=now - 4),
        ],
        runtime="devin",
    )
    result = assess(tmp_path, {"dispatch_call_id": "dispatch-1", "kind": "child"})
    assert result["attempt_count"] == 1
    assert "devin-child-attribution-ambiguous" not in result["limitations"]
