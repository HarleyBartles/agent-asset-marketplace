#!/usr/bin/env python3
"""PostToolUse transcript recorder for the iterative-review hooks pack.

Reads the hook payload as JSON on stdin (or argv[1] fallback) and appends it
verbatim as one JSONL line to ``<transcript_root>/<session_id>.jsonl``. Never
exits nonzero: a recorder failure must not break the session; malformed input
is logged to ``hook-errors.jsonl`` instead.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _env() -> dict:
    env_path = os.environ.get("IR_HOOK_ENV") or str(Path(__file__).parent / "hook-env.json")
    try:
        return json.loads(Path(env_path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _transcript_root(env: dict) -> Path:
    configured = env.get("transcript_root")
    return Path(configured) if configured else Path(__file__).parent / "transcripts"


def _log_error(root: Path, message: str) -> None:
    try:
        root.mkdir(parents=True, exist_ok=True)
        with (root / "hook-errors.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "hook-error": message,
                "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }, separators=(",", ":")) + "\n")
    except Exception:
        pass


def _payload() -> dict:
    raw = sys.stdin.read()
    if not raw.strip() and len(sys.argv) > 1:
        raw = sys.argv[1]
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("hook payload is not an object")
    return parsed


def main() -> int:
    env = _env()
    root = _transcript_root(env)
    try:
        rec = _payload()
    except Exception as exc:
        _log_error(root, f"malformed payload: {exc}")
        return 0
    session = rec.get("session_id")
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(session)) if session else "unknown-session"
    try:
        root.mkdir(parents=True, exist_ok=True)
        with (root / f"{safe}.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, separators=(",", ":")) + "\n")
    except Exception as exc:
        _log_error(root, f"transcript write failed: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
