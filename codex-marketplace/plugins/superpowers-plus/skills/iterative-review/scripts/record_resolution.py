#!/usr/bin/env python3
"""record_resolution.py - append a resolution event to the review log. (mixed)"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {"finding_id", "resolved_at_node", "resolved_at_round"}


def _load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record a new iterative-review resolution. (mixed)")
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--state", help="path to review-state.json")
    parser.add_argument("--data", help="JSON resolution object")
    args = parser.parse_args(argv)

    if args.check:
        print("record_resolution.py is ready")
        return 0

    if not args.state or not args.data:
        parser.error("the following arguments are required: --state, --data")

    state_path = Path(args.state)
    state = _load_state(state_path)
    try:
        resolution = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid resolution JSON: {e}", file=sys.stderr)
        return 1

    missing = REQUIRED - resolution.keys()
    if missing:
        print(f"ERROR: missing keys {missing}", file=sys.stderr)
        return 1

    try:
        scratch = Path(state["scratch_dir"])
    except KeyError as e:
        print(f"ERROR: missing state key {e}", file=sys.stderr)
        return 1
    log = scratch / "resolutions.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)

    existing = set()
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("finding_id"))

    if resolution["finding_id"] in existing:
        print("record_resolution.py: resolution already recorded; no change")
        return 0

    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(resolution, ensure_ascii=False) + "\n")

    print(f"record_resolution.py: recorded resolution for {resolution['finding_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
