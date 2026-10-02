"""Hook entrypoint that records sanitized, normalized runtime observations."""

import argparse
import json
import sys
import time
from pathlib import Path

from runtime import normalize_event
from store import AuditStoreError, append_record, load_manifest


def record_event(run: Path, payload: dict, now: float) -> bool:
    try:
        manifest = load_manifest(run)
        if not manifest.get("armed") or not isinstance(manifest.get("expires_at"), (int, float)):
            return False
        if now >= manifest["expires_at"]:
            return False
        normalized = normalize_event(manifest.get("runtime", ""), payload, manifest.get("detail", "status"))
        normalized.update(
            {
                "run_id": manifest.get("run_id"),
                "received_at": now,
                "runtime": manifest.get("runtime"),
            }
        )
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
    parser.add_argument("--check", action="store_true", help="validate invocation without recording")
    args = parser.parse_args(argv)
    if args.check:
        return 0
    if not args.run_dir:
        parser.error("--run-dir is required unless --check is used")
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError
        record_event(Path(args.run_dir), payload, time.time())
    except Exception:
        _record_health(Path(args.run_dir), "payload-invalid")
    # A capture hook observes activity and never influences the tool decision.
    sys.stdout.write('{"continue":true}\n')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
