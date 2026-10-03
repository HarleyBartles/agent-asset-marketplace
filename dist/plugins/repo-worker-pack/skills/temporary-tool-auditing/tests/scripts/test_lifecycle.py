import time
import pytest

from auditctl import execute
from record import record_event
from store import load_manifest, save_manifest


def base_run(path, **updates):
    manifest = {
        "run_id": "run-1",
        "runtime": "codex",
        "project_root": str(path.parent),
        "registration_root": str(path.parent / ".codex"),
        "detail": "status",
        "expires_at": time.time() + 1800,
        "armed": False,
        "cleanup_required": False,
        "registration_state": "installed",
        "activation_verified": True,
        "intervals": [],
        "controls": [],
        "health": [],
        "owned_entries": [],
    }
    manifest.update(updates)
    save_manifest(path, manifest)


def test_prepare_preview_does_not_mutate_and_apply_defaults_to_30_minutes(tmp_path):
    args = {
        "operation": "prepare",
        "run_dir": str(tmp_path / "run"),
        "runtime": "codex",
        "project": str(tmp_path),
        "question": "Did the child avoid tools?",
        "subject": "session:s1",
        "detail": "status",
        "duration_minutes": None,
        "runtime_version": None,
        "apply": False,
    }
    preview = execute(args, now=100)
    assert preview["applied"] is False
    assert not (tmp_path / "run" / "manifest.json").exists()
    args["apply"] = True
    execute(args, now=100)
    manifest = load_manifest(tmp_path / "run")
    assert manifest["expires_at"] == 1900
    assert manifest["cleanup_required"] is False


def test_expiry_does_not_complete_cleanup_and_renewal_closes_gap(tmp_path):
    run = tmp_path / "run"
    base_run(run, expires_at=100, cleanup_required=True, intervals=[{"start": 50, "end": 100}])
    state = execute({"operation": "status", "run_dir": str(run), "apply": False}, now=101)
    assert state["recording_state"] == "expired"
    assert state["cleanup_required"] is True
    execute({"operation": "renew", "run_dir": str(run), "duration_minutes": 5, "apply": True}, now=101)
    manifest = load_manifest(run)
    assert manifest["expires_at"] == 401
    assert manifest["armed"] is False
    assert manifest["coverage_gaps"]


def test_start_requires_activation_and_stop_preserves_cleanup(tmp_path):
    run = tmp_path / "run"
    base_run(run, activation_verified=False, cleanup_required=True)
    with pytest.raises(Exception) as error:
        execute({"operation": "start", "run_dir": str(run), "apply": True}, now=100)
    assert getattr(error.value, "code", None) == "activation-unverified"
    manifest = load_manifest(run)
    manifest["activation_verified"] = True
    save_manifest(run, manifest)
    execute({"operation": "start", "run_dir": str(run), "apply": True}, now=100)
    execute({"operation": "stop", "run_dir": str(run), "apply": True}, now=150)
    stopped = load_manifest(run)
    assert stopped["armed"] is False
    assert stopped["cleanup_required"] is True
    assert stopped["intervals"][0]["end"] == 150


def test_renewal_before_expiry_keeps_active_capture_continuous(tmp_path):
    run = tmp_path / "run"
    base_run(
        run,
        armed=True,
        cleanup_required=True,
        intervals=[{"start": 50, "end": None, "expires_at": 200}],
        expires_at=200,
    )
    execute(
        {"operation": "renew", "run_dir": str(run), "duration_minutes": 5, "apply": True},
        now=100,
    )
    manifest = load_manifest(run)
    assert manifest["armed"] is True
    assert manifest["intervals"][-1]["end"] is None
    assert manifest.get("coverage_gaps", []) == []


def test_activation_verification_requires_a_real_captured_probe_call(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="installed", activation_verified=False)
    started = execute({"operation": "verify", "run_dir": str(run), "apply": True}, now=100)
    assert started["activation_probe"] == "started"
    assert record_event(
        run,
        {
            "hook_event_name": "PreToolUse",
            "session_id": "active-session",
            "tool_use_id": "positive-control",
            "tool_name": "Bash",
        },
        101,
    )
    execute(
        {
            "operation": "verify",
            "run_dir": str(run),
            "control_call_id": "positive-control",
            "apply": True,
        },
        now=102,
    )
    manifest = load_manifest(run)
    assert manifest["activation_verified"] is True
    assert manifest["armed"] is False
    assert manifest["controls"][0]["session_id"] == "active-session"


def test_teardown_probe_succeeds_when_direct_control_works_and_no_hook_fires(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    begin = execute(
        {"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True},
        now=100,
    )
    assert begin["teardown_probe"] == "started"
    result = execute(
        {
            "operation": "verify-teardown",
            "run_dir": str(run),
            "phase": "finish",
            "restart_confirmed": True,
            "canary_performed": True,
            "apply": True,
        },
        now=101,
    )
    assert result["teardown_verified"] is True
    manifest = load_manifest(run)
    assert manifest["cleanup_required"] is False
    assert manifest["armed"] is False
    assert (run / "controls.jsonl").exists()
    assert not (run / "health.jsonl").exists()


def test_teardown_probe_detects_cached_hook_and_leaves_cleanup_pending(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    execute(
        {"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True},
        now=100,
    )
    record_event(
        run,
        {
            "hook_event_name": "PreToolUse",
            "session_id": "s1",
            "tool_use_id": "stale-hook-call",
            "tool_name": "Bash",
        },
        101,
    )
    with pytest.raises(Exception) as error:
        execute(
            {
                "operation": "verify-teardown",
                "run_dir": str(run),
                "phase": "finish",
                "restart_confirmed": True,
                "canary_performed": True,
                "apply": True,
            },
            now=102,
        )
    assert getattr(error.value, "code", None) == "cached-hook-still-active"
    manifest = load_manifest(run)
    assert manifest["armed"] is False
    assert manifest["cleanup_required"] is True
