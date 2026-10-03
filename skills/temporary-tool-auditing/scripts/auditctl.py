"""Lifecycle CLI for bounded temporary tool-audit runs. (mixed)"""

import argparse
import json
import math
import subprocess
import time
import uuid
from pathlib import Path

from assessment import assess
from registration import install, registration_absent, remove
from sanitize import sanitize
from store import AuditStoreError, append_record, create_manifest, load_manifest, save_manifest, update_manifest


def _duration(value, default=30.0) -> float:
    try:
        duration = default if value is None else float(value)
    except (TypeError, ValueError):
        raise AuditStoreError("invalid-duration") from None
    if not math.isfinite(duration) or duration <= 0:
        raise AuditStoreError("invalid-duration")
    return duration


def _close_interval(manifest: dict, now: float) -> None:
    intervals = manifest.setdefault("intervals", [])
    if intervals and intervals[-1].get("end") is None:
        intervals[-1]["end"] = min(now, manifest.get("expires_at", now))
        if intervals[-1]["end"] < now:
            manifest.setdefault("coverage_gaps", []).append({"start": intervals[-1]["end"], "end": now})


def _abort_teardown(run: Path, manifest: dict, now: float, code: str) -> None:
    _close_interval(manifest, now)
    manifest["armed"] = False
    manifest.pop("teardown_probe_until", None)
    save_manifest(run, manifest)
    raise AuditStoreError(code)


def _subject(value: str) -> dict:
    if value.startswith("session:") and len(value) > 8:
        return {"session_id": value[8:]}
    if value.startswith("agent:") and len(value) > 6:
        return {"agent_id": value[6:]}
    if value.startswith("child:") and len(value) > 6:
        return {"kind": "child", "dispatch_call_id": value[6:]}
    raise AuditStoreError("invalid-subject-selector")


def execute(args: dict, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    operation = args.get("operation")
    run = Path(args["run_dir"]).resolve() if args.get("run_dir") else None
    apply = bool(args.get("apply"))
    if apply and args.get("check"):
        raise AuditStoreError("conflicting-modes")
    if operation == "prepare":
        duration = _duration(args.get("duration_minutes"))
        detail = args.get("detail")
        runtime = args.get("runtime")
        if runtime not in {"codex", "devin-desktop"} or detail not in {"status", "full-results"}:
            raise AuditStoreError("invalid-prepare-options")
        subject = _subject(args.get("subject", ""))
        project = Path(args["project"]).resolve()
        if run is None or run == project or project in run.parents:
            raise AuditStoreError("run-directory-must-be-outside-project")
        question, redactions = sanitize(args.get("question", ""))
        if not apply:
            return {"applied": False, "runtime": runtime, "detail": detail, "duration_minutes": duration}
        manifest = {
            "version": 1,
            "run_id": str(uuid.uuid4()),
            "runtime": runtime,
            "runtime_version": args.get("runtime_version"),
            "project_root": str(project),
            "registration_root": None,
            "subject": subject,
            "question": question,
            "detail": detail,
            "expires_at": now + duration * 60,
            "armed": False,
            "cleanup_required": False,
            "registration_state": "not-installed",
            "activation_verified": False,
            "intervals": [],
            "controls": [],
            "health": [],
            "owned_entries": [],
            "redactions": redactions,
        }
        create_manifest(run, manifest)
        return {"applied": True, "run_id": manifest["run_id"], "expires_at": manifest["expires_at"]}
    if run is None:
        raise AuditStoreError("run-directory-required")
    if not apply and operation not in {"status", "assess", "verify"}:
        return {"applied": False, "operation": operation}
    if operation == "install":
        manifest = load_manifest(run)
        return install(run, Path(manifest["project_root"]), manifest["runtime"])
    if operation == "remove":

        def disarm(manifest):
            manifest["armed"] = False
            manifest["activation_verified"] = False
            manifest["late_outcomes_allowed"] = False
            manifest["registration_state"] = "removing"
            _close_interval(manifest, now)

        update_manifest(run, disarm)
        return remove(run)
    if operation == "purge":
        manifest = load_manifest(run)
        if manifest.get("logs_purged") and not manifest.get("cleanup_required"):
            return {"logs_purged": True, "cleanup_required": False, "already_purged": True}
        if manifest.get("registration_state") != "teardown-verified" or not manifest.get("teardown_verified_at"):
            raise AuditStoreError("teardown-not-verified")
        if manifest.get("armed"):
            raise AuditStoreError("recorder-still-armed")
        for name in ("events", "health", "controls"):
            path = run / f"{name}.jsonl"
            try:
                path.unlink(missing_ok=True)
            except OSError:
                raise AuditStoreError("log-purge-failed") from None
            if path.exists():
                raise AuditStoreError("log-purge-failed")
        scripts = run / "scripts"
        if scripts.is_symlink() or (scripts.exists() and not scripts.is_dir()):
            raise AuditStoreError("run-helper-purge-failed")
        if scripts.exists():
            for name in ("record.py", "runtime.py", "store.py", "sanitize.py"):
                try:
                    (scripts / name).unlink(missing_ok=True)
                except OSError:
                    raise AuditStoreError("run-helper-purge-failed") from None
            try:
                scripts.rmdir()
            except OSError:
                raise AuditStoreError("run-helper-purge-failed") from None
        final_manifest = {
            "version": manifest.get("version", 1),
            "run_id": manifest.get("run_id"),
            "runtime": manifest.get("runtime"),
            "registration_state": "cleaned",
            "cleanup_required": False,
            "teardown_verified_at": manifest["teardown_verified_at"],
            "logs_purged": True,
            "evidence_purged_at": now,
        }
        try:
            save_manifest(run, final_manifest)
        except AuditStoreError:
            raise AuditStoreError("log-purge-finalize-failed") from None
        return {"logs_purged": True, "cleanup_required": False, "evidence_purged_at": now}
    if operation == "status":
        manifest = load_manifest(run)
        if now >= manifest.get("expires_at", 0):
            state = "expired"
        else:
            state = "recording" if manifest.get("armed") else "stopped"
        return {"recording_state": state, "cleanup_required": bool(manifest.get("cleanup_required")), **manifest}
    if operation == "verify":
        control_id = args.get("control_call_id")
        if not control_id:
            if not apply:
                return {"activation_probe": "not-started", "requires_apply": True}

            def begin_probe(manifest):
                if manifest.get("registration_state") != "installed":
                    raise AuditStoreError("registration-unverified")
                if now >= manifest.get("expires_at", 0):
                    raise AuditStoreError("lease-expired-renew-first")
                if manifest.get("armed"):
                    raise AuditStoreError("already-armed")
                probe_until = min(manifest["expires_at"], now + 120)
                manifest["activation_probe_until"] = probe_until
                manifest["activation_probe_started_at"] = now
                manifest["armed"] = True
                manifest.setdefault("intervals", []).append(
                    {
                        "start": now,
                        "end": None,
                        "detail": manifest.get("detail"),
                        "expires_at": probe_until,
                        "kind": "activation-probe",
                    }
                )
                return probe_until

            manifest, probe_until = update_manifest(run, begin_probe)
            return {"activation_probe": "started", "expires_at": probe_until}

        def finish_probe(manifest):
            if manifest.get("registration_state") != "installed":
                raise AuditStoreError("registration-unverified")
            events_path = run / "events.jsonl"
            events = (
                [json.loads(row) for row in events_path.read_text(encoding="utf-8").splitlines()]
                if events_path.exists()
                else []
            )
            control = next(
                (
                    item
                    for item in events
                    if item.get("call_id") == control_id
                    and item.get("run_id") == manifest.get("run_id")
                    and item.get("event") == "pre"
                    and isinstance(item.get("received_at"), (int, float))
                    and item["received_at"] >= manifest.get("activation_probe_started_at", float("inf"))
                    and item["received_at"] <= manifest.get("activation_probe_until", float("-inf"))
                ),
                None,
            )
            if control is None:
                raise AuditStoreError("activation-control-not-captured")
            if apply:
                manifest["activation_verified"] = True
                manifest.setdefault("controls", []).append(
                    {
                        "call_id": control_id,
                        "session_id": control.get("session_id"),
                        "agent_id": control.get("agent_id"),
                        "role": "positive",
                        "verified_at": now,
                    }
                )
                manifest.pop("activation_probe_until", None)
                manifest.pop("activation_probe_started_at", None)
                _close_interval(manifest, now)
                manifest["armed"] = False
            return control

        manifest, control = update_manifest(run, finish_probe)
        found = control is not None
        return {"activation_verified": found, "applied": apply}
    if operation in {"start", "stop", "disarm", "renew"}:
        if operation == "start":

            def transition(manifest):
                if manifest.get("registration_state") != "installed":
                    raise AuditStoreError("registration-not-installed")
                if not manifest.get("activation_verified"):
                    raise AuditStoreError("activation-unverified")
                if now >= manifest.get("expires_at", 0):
                    raise AuditStoreError("lease-expired-renew-first")
                if manifest.get("armed"):
                    raise AuditStoreError("already-armed")
                manifest.setdefault("intervals", []).append(
                    {"start": now, "end": None, "detail": manifest.get("detail"), "expires_at": manifest["expires_at"]}
                )
                manifest["armed"] = True
                manifest["late_outcomes_allowed"] = True
        elif operation in {"stop", "disarm"}:

            def transition(manifest):
                _close_interval(manifest, now)
                manifest["armed"] = False
                if operation == "disarm":
                    manifest["late_outcomes_allowed"] = False
                if operation == "stop":
                    manifest["subject_completed_at"] = now
                    manifest["subject_completion_source"] = "operator-stop"
        else:
            duration = _duration(args.get("duration_minutes"))

            def transition(manifest):
                if manifest.get("registration_state") != "installed":
                    raise AuditStoreError("registration-not-installed")
                was_expired = now >= manifest.get("expires_at", 0)
                if was_expired:
                    _close_interval(manifest, now)
                    gap = {"start": manifest.get("expires_at"), "end": now}
                    if gap not in manifest.get("coverage_gaps", []):
                        manifest.setdefault("coverage_gaps", []).append(gap)
                    manifest["armed"] = False
                    manifest["activation_verified"] = False
                elif manifest.get("armed") and manifest.get("intervals"):
                    manifest["intervals"][-1]["expires_at"] = now + duration * 60
                manifest["expires_at"] = now + duration * 60
                manifest.setdefault("renewals", []).append({"at": now, "duration_minutes": duration})

        manifest, _ = update_manifest(run, transition)
        return {
            "operation": operation,
            "applied": True,
            "armed": manifest["armed"],
            "expires_at": manifest["expires_at"],
        }
    if operation == "assess":
        manifest = load_manifest(run)
        if args.get("parent_idle_confirmed"):
            if not apply:
                raise AuditStoreError("parent-idle-attestation-requires-apply")
            subject = _subject(args["subject"]) if args.get("subject") else manifest.get("subject", {})
            if manifest.get("runtime") != "devin-desktop" or subject.get("kind") != "child":
                raise AuditStoreError("parent-idle-attestation-only-for-devin-child")
            append_record(
                run,
                "controls",
                {
                    "code": "devin-parent-idle-attestation",
                    "dispatch_call_id": subject.get("dispatch_call_id"),
                    "run_id": manifest.get("run_id"),
                    "confirmed_at": now,
                },
            )
        return assess(
            run,
            _subject(args["subject"]) if args.get("subject") else manifest.get("subject", {}),
            parent_idle_confirmed=bool(args.get("parent_idle_confirmed")),
        )
    if operation == "verify-teardown":
        manifest = load_manifest(run)
        if manifest.get("registration_state") != "removed":
            raise AuditStoreError("teardown-restart-unverified")
        phase = args.get("phase", "finish")
        if phase == "begin":
            if not apply:
                return {"teardown_probe": "not-started", "requires_apply": True}
            manifest["teardown_probe_started_at"] = now
            manifest["teardown_probe_until"] = now + 120
            manifest["armed"] = True
            manifest.setdefault("intervals", []).append(
                {
                    "start": now,
                    "end": None,
                    "detail": manifest.get("detail"),
                    "expires_at": now + 120,
                    "kind": "teardown-probe",
                }
            )
            save_manifest(run, manifest)
            return {"teardown_probe": "started", "expires_at": now + 120}
        if phase != "finish" or not args.get("restart_confirmed"):
            _abort_teardown(run, manifest, now, "teardown-restart-unverified")
        if not args.get("canary_performed"):
            _abort_teardown(run, manifest, now, "teardown-canary-required")
        if not manifest.get("teardown_probe_started_at"):
            raise AuditStoreError("teardown-probe-not-started")
        if now > manifest.get("teardown_probe_until", 0):
            _abort_teardown(run, manifest, now, "teardown-probe-expired")
        if not registration_absent(run, manifest):
            _abort_teardown(run, manifest, now, "teardown-registration-still-present")
        try:
            nonce = str(uuid.uuid4())
            recorder = run / "scripts" / "record.py"
            interpreter = manifest.get("hook_interpreter")
            if not isinstance(interpreter, str) or not Path(interpreter).is_file():
                raise RuntimeError("hook-interpreter-unavailable")
            result = subprocess.run(
                [interpreter, str(recorder), "--run-dir", str(run), "--control-nonce", nonce],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if result.returncode != 0:
                raise RuntimeError("recorder-control-failed")
            controls = (run / "controls.jsonl").read_text(encoding="utf-8") if (run / "controls.jsonl").exists() else ""
            if not any(json.loads(line).get("nonce") == nonce for line in controls.splitlines() if line.strip()):
                raise RuntimeError("recorder-control-missing")
            events = (run / "events.jsonl").read_text(encoding="utf-8") if (run / "events.jsonl").exists() else ""
            event_rows = [json.loads(line) for line in events.splitlines() if line.strip()]
            if not any(
                item.get("call_id") == nonce and item.get("control_operation") == "verify-teardown"
                for item in event_rows
            ):
                raise RuntimeError("recorder-event-control-missing")
            since = manifest["teardown_probe_started_at"]
            late = False
            for event in event_rows:
                if event.get("call_id") == nonce and event.get("control_operation") == "verify-teardown":
                    continue
                if event.get("received_at", 0) >= since:
                    late = True
        except Exception:
            _abort_teardown(run, manifest, now, "teardown-control-failed")
        if late:
            _abort_teardown(run, manifest, now, "cached-hook-still-active")
        health_path = run / "health.jsonl"
        if health_path.exists():
            try:
                health_rows = [
                    json.loads(line) for line in health_path.read_text(encoding="utf-8").splitlines() if line.strip()
                ]
            except Exception:
                health_rows = [{}]
            if any(
                not isinstance(item, dict)
                or not isinstance(item.get("received_at"), (int, float))
                or item["received_at"] >= manifest["teardown_probe_started_at"]
                for item in health_rows
            ):
                _abort_teardown(run, manifest, now, "teardown-recorder-health-failed")
        _close_interval(manifest, now)
        manifest["armed"] = False
        manifest.pop("teardown_probe_until", None)
        manifest["cleanup_required"] = True
        manifest["late_outcomes_allowed"] = False
        manifest["registration_state"] = "teardown-verified"
        manifest["teardown_verified_at"] = now
        save_manifest(run, manifest)
        return {"cleanup_required": True, "teardown_verified": True, "logs_purge_required": True}
    raise AuditStoreError("unknown-operation")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a bounded temporary tool audit. (mixed)")
    parser.add_argument(
        "--check", dest="global_check", action="store_true", help="validate the command surface without mutation"
    )
    subs = parser.add_subparsers(dest="operation")
    operations = (
        "prepare",
        "install",
        "status",
        "verify",
        "start",
        "stop",
        "renew",
        "assess",
        "disarm",
        "remove",
        "verify-teardown",
        "purge",
    )
    for operation in operations:
        child = subs.add_parser(operation)
        child.add_argument("--apply", action="store_true", help="apply this operation")
        child.add_argument("--check", action="store_true", help="preview without mutation")
        child.add_argument("--run-dir", required=operation != "prepare")
        if operation == "prepare":
            child.add_argument("--runtime", choices=("codex", "devin-desktop"), required=True)
            child.add_argument("--project", required=True)
            child.add_argument("--question", required=True)
            child.add_argument("--subject", required=True)
            child.add_argument("--detail", choices=("status", "full-results"), required=True)
            child.add_argument("--duration-minutes", type=float)
            child.add_argument("--runtime-version")
        if operation == "renew":
            child.add_argument("--duration-minutes", type=float)
        if operation == "verify":
            child.add_argument("--control-call-id")
        if operation == "assess":
            child.add_argument("--subject")
            child.add_argument(
                "--confirm-parent-idle",
                dest="parent_idle_confirmed",
                action="store_true",
                help="attest that the orchestrator made no tool calls during this Devin child dispatch",
            )
        if operation == "verify-teardown":
            child.add_argument("--restart-confirmed", action="store_true")
            child.add_argument("--canary-performed", action="store_true")
            child.add_argument("--phase", choices=("begin", "finish"), default="finish")
    return parser


def main(argv=None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    args.check = bool(args.check or args.global_check)
    if args.check and not args.operation:
        return 0
    if not args.operation:
        parser.print_help()
        return 0
    try:
        result = execute(vars(args))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except AuditStoreError as error:
        print(json.dumps({"error": error.code}, sort_keys=True))
        return 1
    except Exception:
        print(json.dumps({"error": "operation-failed"}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
