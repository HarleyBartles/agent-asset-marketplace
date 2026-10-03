"""Hook entrypoint that records sanitized, normalized runtime observations."""

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

from runtime import normalize_event
from store import AuditStoreError, append_record, append_record_if, load_manifest


def record_event(run: Path, payload: dict, now: float) -> bool:
    try:
        manifest = load_manifest(run)
        if not isinstance(manifest.get("expires_at"), (int, float)):
            return False
        normalized = normalize_event(
            manifest.get("runtime", ""),
            payload,
            manifest.get("detail", "status"),
            run_dir=run,
            lifecycle_cli_path=manifest.get("lifecycle_cli_path"),
        )
        normalized.update(
            {
                "run_id": manifest.get("run_id"),
                "received_at": now,
                "runtime": manifest.get("runtime"),
            }
        )

        def currently_eligible(current: dict, event: dict) -> bool:
            if not isinstance(current.get("expires_at"), (int, float)):
                return False
            event["run_id"] = current.get("run_id")
            event["runtime"] = current.get("runtime")
            active_until = current.get("expires_at")
            if current.get("activation_probe_until") is not None:
                active_until = min(active_until, current["activation_probe_until"])
            if current.get("teardown_probe_until") is not None:
                active_until = current["teardown_probe_until"]
            if current.get("armed") and now < active_until:
                return True
            if (
                not current.get("late_outcomes_allowed", True)
                or current.get("registration_state") in {"removing", "removed", "teardown-verified", "cleaned"}
                or event.get("event") != "post"
                or not event.get("call_id")
            ):
                return False
            try:
                event_text = (Path(run) / "events.jsonl").read_text(encoding="utf-8")
                previous = [json.loads(row) for row in event_text.splitlines()]
            except FileNotFoundError:
                return False
            except Exception:
                return False
            paired = any(
                item.get("event") == "pre"
                and item.get("call_id") == event["call_id"]
                and item.get("run_id") == current.get("run_id")
                for item in previous
            )
            if paired:
                event["late_outcome"] = True
            return paired

        return append_record_if(run, "events", normalized, currently_eligible) is not None
    except AuditStoreError as error:
        _record_health(run, error.code)
        return False
    except (ValueError, TypeError):
        _record_health(run, "record-failed")
        return False


def _record_health(run: Path, code: str) -> None:
    try:
        existing = Path(run) / "health.jsonl"
        if existing.exists():
            for line in existing.read_text(encoding="utf-8").splitlines():
                if json.loads(line).get("code") == code:
                    return
        append_record_if(
            run,
            "health",
            {"code": code, "received_at": time.time()},
            lambda manifest, _record: manifest.get("registration_state") not in {"teardown-verified", "cleaned"}
            and not manifest.get("logs_purged"),
        )
    except AuditStoreError:
        pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Append one sanitized hook observation. (mutating)")
    parser.add_argument("--run-dir")
    parser.add_argument("--control-nonce")
    parser.add_argument("--health-control-nonce")
    parser.add_argument("--check", action="store_true", help="validate invocation without recording")
    args = parser.parse_args(argv)
    if args.check:
        return 0
    if not args.run_dir:
        parser.error("--run-dir is required unless --check is used")
    try:
        if args.control_nonce:
            nonce = str(uuid.UUID(args.control_nonce))
            now = time.time()
            run = Path(args.run_dir)
            manifest = load_manifest(run)
            helper = manifest.get("lifecycle_cli_path")
            if not isinstance(helper, str):
                raise AuditStoreError("lifecycle-helper-unavailable")
            command = " ".join(
                (
                    json.dumps(sys.executable),
                    json.dumps(helper),
                    "verify-teardown --phase finish --apply --run-dir",
                    json.dumps(str(run)),
                )
            )
            if not record_event(
                run,
                {
                    "hook_event_name": "PreToolUse",
                    "session_id": "audit-control",
                    "tool_use_id": nonce,
                    "tool_name": "Bash",
                    "tool_input": {"command": command},
                },
                now,
            ):
                raise AuditStoreError("recorder-event-control-failed")
            append_record(
                run,
                "controls",
                {
                    "code": "recorder-direct-control",
                    "nonce": nonce,
                    "received_at": time.time(),
                },
            )
            return 0
        if args.health_control_nonce:
            nonce = str(uuid.UUID(args.health_control_nonce))
            run = Path(args.run_dir)
            manifest = load_manifest(run)
            if manifest.get("registration_state") not in {"removed", "installed"}:
                raise AuditStoreError("health-control-window-closed")
            append_record(
                run,
                "controls",
                {
                    "code": "recorder-health-control",
                    "nonce": nonce,
                    "received_at": time.time(),
                    "run_id": manifest.get("run_id"),
                },
            )
            return 0
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError
        record_event(Path(args.run_dir), payload, time.time())
    except Exception:
        _record_health(Path(args.run_dir), "payload-invalid")
    # Empty stdout is neutral across the supported command-hook contracts and
    # avoids emitting unsupported PreToolUse control fields in Codex.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
