"""Hook entrypoint that records sanitized, normalized runtime observations."""

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

from runtime import normalize_event
from store import AuditStoreError, append_record, load_manifest


def record_event(run: Path, payload: dict, now: float) -> bool:
    try:
        manifest = load_manifest(run)
        if not isinstance(manifest.get("expires_at"), (int, float)):
            return False
        normalized = normalize_event(manifest.get("runtime", ""), payload, manifest.get("detail", "status"))
        active_until = manifest.get("expires_at")
        if manifest.get("activation_probe_until") is not None:
            active_until = min(active_until, manifest["activation_probe_until"])
        if manifest.get("teardown_probe_until") is not None:
            active_until = manifest["teardown_probe_until"]
        in_window = manifest.get("armed") and now < active_until
        late_outcome = False
        if not in_window:
            if normalized.get("event") != "post" or not normalized.get("call_id"):
                return False
            events_path = Path(run) / "events.jsonl"
            try:
                previous = [json.loads(row) for row in events_path.read_text(encoding="utf-8").splitlines()]
            except FileNotFoundError:
                return False
            except Exception:
                _record_health(run, "event-log-unreadable")
                return False
            call_id = normalized["call_id"]
            late_outcome = any(
                item.get("event") == "pre"
                and item.get("call_id") == call_id
                and item.get("run_id") == manifest.get("run_id")
                for item in previous
            )
            if not late_outcome:
                return False
        normalized.update(
            {
                "run_id": manifest.get("run_id"),
                "received_at": now,
                "runtime": manifest.get("runtime"),
            }
        )
        if late_outcome:
            normalized["late_outcome"] = True
        append_record(run, "events", normalized)
        return True
    except (AuditStoreError, ValueError, TypeError):
        _record_health(run, "record-failed")
        return False


def _record_health(run: Path, code: str) -> None:
    try:
        append_record(run, "health", {"code": code, "received_at": time.time()})
    except AuditStoreError:
        pass


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Append one sanitized hook observation. (mutating)")
    parser.add_argument("--run-dir")
    parser.add_argument("--control-nonce")
    parser.add_argument("--check", action="store_true", help="validate invocation without recording")
    args = parser.parse_args(argv)
    if args.check:
        return 0
    if not args.run_dir:
        parser.error("--run-dir is required unless --check is used")
    try:
        if args.control_nonce:
            nonce = str(uuid.UUID(args.control_nonce))
            append_record(
                Path(args.run_dir),
                "controls",
                {
                    "code": "recorder-direct-control",
                    "nonce": nonce,
                    "received_at": time.time(),
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
