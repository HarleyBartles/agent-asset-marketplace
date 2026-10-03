import json
import os
import sys
import time
from pathlib import Path
import pytest

from auditctl import execute
from record import record_event
from store import append_record, load_manifest, save_manifest


def base_run(path, **updates):
    manifest = {
        "run_id": "run-1",
        "hook_interpreter": sys.executable,
        "runtime": "codex",
        "lifecycle_cli_path": str(Path(__file__).parents[2] / "scripts" / "auditctl.py"),
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


def install_test_recorder(run):
    import shutil
    from pathlib import Path

    scripts = Path(__file__).parents[2] / "scripts"
    (run / "scripts").mkdir()
    for name in ("record.py", "runtime.py", "store.py", "sanitize.py"):
        shutil.copyfile(scripts / name, run / "scripts" / name)


def test_prepare_preview_does_not_mutate_and_apply_defaults_to_30_minutes(tmp_path):
    args = {
        "operation": "prepare",
        "run_dir": str(tmp_path / "run"),
        "runtime": "codex",
        "project": str(tmp_path / "project"),
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
    assert manifest["activation_verified"] is False
    assert manifest["coverage_gaps"]


def test_start_after_expired_lease_renewal_requires_new_activation_probe(tmp_path):
    run = tmp_path / "run"
    base_run(run, expires_at=100, activation_verified=True, intervals=[{"start": 50, "end": 100}])
    execute({"operation": "renew", "run_dir": str(run), "duration_minutes": 5, "apply": True}, now=101)
    with pytest.raises(Exception) as error:
        execute({"operation": "start", "run_dir": str(run), "apply": True}, now=102)
    assert getattr(error.value, "code", None) == "activation-unverified"


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


def test_activation_rejects_a_control_captured_before_the_current_probe(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="installed", activation_verified=False)
    append_record(
        run,
        "events",
        {"run_id": "run-1", "event": "pre", "call_id": "old-control", "session_id": "s1", "received_at": 99},
    )
    execute({"operation": "verify", "run_dir": str(run), "apply": True}, now=100)
    with pytest.raises(Exception) as error:
        execute(
            {"operation": "verify", "run_dir": str(run), "control_call_id": "old-control", "apply": True},
            now=101,
        )
    assert getattr(error.value, "code", None) == "activation-control-not-captured"
    assert load_manifest(run)["activation_verified"] is False


def test_stop_records_operator_completion_within_closed_coverage(tmp_path):
    run = tmp_path / "run"
    base_run(
        run,
        activation_verified=True,
        armed=True,
        controls=[{"call_id": "positive", "session_id": "s1", "role": "positive"}],
        intervals=[{"start": 50, "end": None, "expires_at": 500}],
    )
    record_event(
        run,
        {"hook_event_name": "PreToolUse", "session_id": "s1", "tool_use_id": "positive", "tool_name": "Bash"},
        60,
    )
    execute({"operation": "stop", "run_dir": str(run), "apply": True}, now=100)
    manifest = load_manifest(run)
    assert manifest["subject_completed_at"] == 100
    result = execute({"operation": "assess", "run_dir": str(run), "subject": "session:s1"}, now=101)
    assert result["claim_supported"] is True


def test_apply_and_check_together_are_rejected(tmp_path):
    run = tmp_path / "run"
    base_run(run)
    with pytest.raises(Exception) as error:
        execute({"operation": "stop", "run_dir": str(run), "apply": True, "check": True}, now=100)
    assert getattr(error.value, "code", None) == "conflicting-modes"


def test_devin_parent_idle_attestation_requires_apply_and_is_persisted(tmp_path):
    run = tmp_path / "run"
    base_run(run, runtime="devin-desktop", subject={"kind": "child", "dispatch_call_id": "dispatch-1"})
    with pytest.raises(Exception) as error:
        execute(
            {"operation": "assess", "run_dir": str(run), "subject": "child:dispatch-1", "parent_idle_confirmed": True},
            now=100,
        )
    assert getattr(error.value, "code", None) == "parent-idle-attestation-requires-apply"
    execute(
        {
            "operation": "assess",
            "run_dir": str(run),
            "subject": "child:dispatch-1",
            "parent_idle_confirmed": True,
            "apply": True,
        },
        now=101,
    )
    assert json.loads((run / "controls.jsonl").read_text()) == {
        "code": "devin-parent-idle-attestation",
        "dispatch_call_id": "dispatch-1",
        "run_id": "run-1",
        "confirmed_at": 101,
        "redactions": [],
    }


def test_devin_parent_idle_attestation_cannot_recreate_purged_controls(tmp_path):
    run = tmp_path / "run"
    base_run(
        run,
        runtime="devin-desktop",
        subject={"kind": "child", "dispatch_call_id": "dispatch-1"},
        registration_state="cleaned",
        logs_purged=True,
        cleanup_required=False,
    )

    with pytest.raises(Exception) as error:
        execute(
            {
                "operation": "assess",
                "run_dir": str(run),
                "subject": "child:dispatch-1",
                "parent_idle_confirmed": True,
                "apply": True,
            },
            now=101,
        )

    assert getattr(error.value, "code", None) == "control-write-window-closed"
    assert not (run / "controls.jsonl").exists()


def test_prepare_rejects_run_directory_inside_project_and_existing_run(tmp_path):
    base = {
        "operation": "prepare",
        "runtime": "codex",
        "project": str(tmp_path / "project"),
        "question": "Did the selected agent avoid tools?",
        "subject": "session:s1",
        "detail": "status",
        "apply": True,
    }
    with pytest.raises(Exception) as error:
        execute({**base, "run_dir": str(tmp_path / "project" / "audit-run")}, now=100)
    assert getattr(error.value, "code", None) == "run-directory-must-be-outside-project"
    run = tmp_path / "run"
    execute({**base, "run_dir": str(run)}, now=100)
    with pytest.raises(Exception) as error:
        execute({**base, "run_dir": str(run)}, now=101)
    assert getattr(error.value, "code", None) == "run-directory-exists"


def test_prepare_run_directory_is_outside_project_and_private_on_posix(tmp_path):
    import os

    if os.name == "nt":
        pytest.skip("POSIX permission bits are not authoritative on Windows")
    project = tmp_path / "project"
    run = tmp_path / "private-run"
    execute(
        {
            "operation": "prepare",
            "run_dir": str(run),
            "runtime": "codex",
            "project": str(project),
            "question": "scenario",
            "subject": "session:s1",
            "detail": "status",
            "apply": True,
        },
        now=100,
    )
    assert (run.stat().st_mode & 0o777) == 0o700
    assert not project.exists()


def test_lifecycle_start_transition_is_atomic_under_concurrency(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    run = tmp_path / "run"
    base_run(run, activation_verified=True, expires_at=500)
    barrier = Barrier(2)

    def start():
        barrier.wait()
        try:
            execute({"operation": "start", "run_dir": str(run), "apply": True}, now=100)
            return "started"
        except Exception as error:
            return getattr(error, "code", "unexpected")

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(lambda _: start(), range(2)))
    assert sorted(outcomes) == ["already-armed", "started"]
    assert len(load_manifest(run)["intervals"]) == 1


@pytest.mark.parametrize("operation", ["start", "renew"])
def test_capture_cannot_restart_after_registration_removal(tmp_path, operation):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", activation_verified=True)
    with pytest.raises(Exception) as error:
        execute({"operation": operation, "run_dir": str(run), "apply": True, "duration_minutes": 5}, now=100)
    assert getattr(error.value, "code", None) == "registration-not-installed"


def test_teardown_probe_succeeds_when_direct_control_works_and_no_hook_fires(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    install_test_recorder(run)
    begin_at = time.time()
    begin = execute(
        {"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True},
        now=begin_at,
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
        now=begin_at + 1,
    )
    assert result["teardown_verified"] is True
    manifest = load_manifest(run)
    assert manifest["cleanup_required"] is True
    assert manifest["armed"] is False
    assert (run / "controls.jsonl").exists()
    events = [json.loads(line) for line in (run / "events.jsonl").read_text().splitlines()]
    assert any(item.get("control_operation") == "verify-teardown" for item in events)
    assert not (run / "health.jsonl").exists()


def test_purge_requires_verified_teardown_and_removes_audit_logs(tmp_path):
    run = tmp_path / "run"
    base_run(
        run,
        registration_state="removed",
        cleanup_required=True,
        teardown_verified_at=100,
        question="sensitive question",
        controls=[{"call_id": "secret-call-id", "session_id": "runtime-session", "role": "positive"}],
    )
    for name in ("events", "health", "controls"):
        append_record(run, name, {"payload": f"{name}-SECRET-SENTINEL"})
    scripts = run / "scripts"
    scripts.mkdir()
    for name in ("record.py", "runtime.py", "store.py", "sanitize.py"):
        (scripts / name).write_text("# owned recorder helper", encoding="utf-8")

    with pytest.raises(Exception) as error:
        execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=101)
    assert getattr(error.value, "code", None) == "teardown-not-verified"

    manifest = load_manifest(run)
    manifest["registration_state"] = "teardown-verified"
    save_manifest(run, manifest)
    result = execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=102)

    assert result["logs_purged"] is True
    assert all(not (run / f"{name}.jsonl").exists() for name in ("events", "health", "controls"))
    final = load_manifest(run)
    assert final["cleanup_required"] is False
    assert final["evidence_purged_at"] == 102
    assert "question" not in final
    assert not final.get("controls")
    assert not scripts.exists()


def test_purge_is_previewable_and_retries_missing_logs_idempotently(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="teardown-verified", cleanup_required=True, teardown_verified_at=100)
    append_record(run, "events", {"call_id": "call-1"})
    preview = execute({"operation": "purge", "run_dir": str(run), "apply": False}, now=101)
    assert preview["applied"] is False
    assert (run / "events.jsonl").exists()
    execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=102)
    result = execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=103)
    assert result["logs_purged"] is True


def test_purge_failure_keeps_cleanup_pending_and_reports_safe_error(tmp_path, monkeypatch):
    run = tmp_path / "run"
    base_run(run, registration_state="teardown-verified", cleanup_required=True, teardown_verified_at=100)
    append_record(run, "events", {"call_id": "call-1"})
    original_unlink = Path.unlink

    def fail_events(path, *args, **kwargs):
        if path.name == "events.jsonl":
            raise PermissionError("do not echo filesystem details")
        return original_unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", fail_events)
    with pytest.raises(Exception) as error:
        execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=101)
    assert getattr(error.value, "code", None) == "log-purge-failed"
    assert load_manifest(run)["cleanup_required"] is True
    assert (run / "events.jsonl").exists()


def test_purge_preserves_unowned_run_files_and_keeps_cleanup_pending(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="teardown-verified", cleanup_required=True, teardown_verified_at=100)
    scripts = run / "scripts"
    scripts.mkdir()
    (scripts / "operator-note.txt").write_text("keep this unowned file", encoding="utf-8")

    with pytest.raises(Exception) as error:
        execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=101)

    assert getattr(error.value, "code", None) == "run-helper-purge-failed"
    assert load_manifest(run)["cleanup_required"] is True
    assert (scripts / "operator-note.txt").read_text(encoding="utf-8") == "keep this unowned file"


def test_purge_preserves_unowned_root_files_before_deleting_logs(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="teardown-verified", cleanup_required=True, teardown_verified_at=100)
    append_record(run, "events", {"call_id": "call-1"})
    note = run / "operator-note.txt"
    note.write_text("keep this unowned file", encoding="utf-8")

    with pytest.raises(Exception) as error:
        execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=101)

    assert getattr(error.value, "code", None) == "run-purge-unowned-entry"
    assert load_manifest(run)["cleanup_required"] is True
    assert note.read_text(encoding="utf-8") == "keep this unowned file"
    assert (run / "events.jsonl").exists()


@pytest.mark.skipif(os.name != "nt" or not hasattr(Path, "is_junction"), reason="Windows junction behavior")
def test_purge_rejects_scripts_junction_without_touching_target_or_logs(tmp_path):
    import subprocess

    run = tmp_path / "run"
    base_run(run, registration_state="teardown-verified", cleanup_required=True, teardown_verified_at=100)
    append_record(run, "events", {"call_id": "call-1"})
    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "record.py"
    sentinel.write_text("leave outside data intact", encoding="utf-8")
    scripts = run / "scripts"
    subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(scripts), str(outside)], check=True, capture_output=True)
    assert scripts.is_junction()

    with pytest.raises(Exception) as error:
        execute({"operation": "purge", "run_dir": str(run), "apply": True}, now=101)

    assert getattr(error.value, "code", None) == "run-helper-purge-failed"
    assert load_manifest(run)["cleanup_required"] is True
    assert sentinel.read_text(encoding="utf-8") == "leave outside data intact"
    assert (run / "events.jsonl").exists()
    scripts.unlink()


def test_teardown_fails_when_direct_control_log_works_but_event_log_does_not(tmp_path, monkeypatch):
    from types import SimpleNamespace

    import auditctl

    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    install_test_recorder(run)
    execute({"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True}, now=100)

    def controls_only(command, **_kwargs):
        assert command[1] == "-B"
        nonce = command[-1]
        append_record(run, "controls", {"code": "recorder-direct-control", "nonce": nonce})
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(auditctl.subprocess, "run", controls_only)
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
            now=101,
        )
    assert getattr(error.value, "code", None) == "teardown-control-failed"
    assert load_manifest(run)["cleanup_required"] is True


def test_teardown_probe_detects_cached_hook_and_leaves_cleanup_pending(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    install_test_recorder(run)
    begin_at = time.time()
    execute(
        {"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True},
        now=begin_at,
    )
    record_event(
        run,
        {
            "hook_event_name": "PreToolUse",
            "session_id": "s1",
            "tool_use_id": "stale-hook-call",
            "tool_name": "Bash",
        },
        begin_at + 1,
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
            now=begin_at + 2,
        )
    assert getattr(error.value, "code", None) == "cached-hook-still-active"
    manifest = load_manifest(run)
    assert manifest["armed"] is False
    assert manifest["cleanup_required"] is True


def test_teardown_requires_current_restart_probe_and_fails_closed_on_expiry(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    install_test_recorder(run)
    execute({"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True}, now=100)
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
            now=221,
        )
    assert getattr(error.value, "code", None) == "teardown-probe-expired"
    manifest = load_manifest(run)
    assert manifest["cleanup_required"] is True


def test_teardown_does_not_clear_cleanup_when_recorder_health_failed(tmp_path):
    run = tmp_path / "run"
    base_run(run, registration_state="removed", cleanup_required=True)
    install_test_recorder(run)
    begin_at = time.time()
    execute({"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True}, now=begin_at)
    (run / "health.jsonl").write_text(json.dumps({"code": "record-failed", "received_at": begin_at + 1}) + "\n")
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
            now=begin_at + 2,
        )
    assert getattr(error.value, "code", None) == "teardown-recorder-health-failed"
    assert load_manifest(run)["cleanup_required"] is True


def test_teardown_does_not_clear_cleanup_while_owned_hook_config_remains(tmp_path):
    from runtime import render_handlers

    run = tmp_path / "run"
    project = tmp_path / "project"
    root = project / ".codex"
    root.mkdir(parents=True)
    handlers = render_handlers("codex", run / "scripts" / "record.py")
    entry = handlers["PreToolUse"][0]
    config = root / "hooks.json"
    config.write_text(json.dumps({"hooks": {"PreToolUse": [entry]}}))
    owner = root / ".temporary-tool-auditing-owner.json"
    owner.write_text(json.dumps({"run_id": "run-1", "run_dir": str(run)}))
    base_run(
        run,
        project_root=str(project),
        registration_root=str(root),
        registration_state="removed",
        cleanup_required=True,
        owned_entries=[{"event": "PreToolUse", "entry": entry}],
    )
    install_test_recorder(run)
    execute({"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True}, now=100)
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
            now=101,
        )
    assert getattr(error.value, "code", None) == "teardown-registration-still-present"
    manifest = load_manifest(run)
    assert manifest["cleanup_required"] is True
    assert manifest["armed"] is False


def test_teardown_uses_persisted_hook_interpreter_and_fails_closed_if_missing(tmp_path):
    run = tmp_path / "run"
    base_run(
        run, registration_state="removed", cleanup_required=True, hook_interpreter=str(tmp_path / "missing-python.exe")
    )
    install_test_recorder(run)
    execute({"operation": "verify-teardown", "run_dir": str(run), "phase": "begin", "apply": True}, now=100)
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
            now=101,
        )
    assert getattr(error.value, "code", None) == "teardown-control-failed"
    assert load_manifest(run)["cleanup_required"] is True


def test_explicit_disarm_disables_late_outcome_capture(tmp_path):
    run = tmp_path / "run"
    base_run(run, armed=True, expires_at=500, intervals=[{"start": 50, "end": None, "expires_at": 500}])
    execute({"operation": "disarm", "run_dir": str(run), "apply": True}, now=100)
    manifest = load_manifest(run)
    assert manifest["late_outcomes_allowed"] is False
    assert manifest["armed"] is False
