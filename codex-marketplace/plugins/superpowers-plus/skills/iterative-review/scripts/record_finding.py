#!/usr/bin/env python3
"""record_finding.py — append a finding event to the review log. (mixed)"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = {"finding_id", "lens", "discovered_at_node", "discovered_at_round", "severity"}


def _load_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Record a new iterative-review finding. (mixed)"
    )
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--state", help="path to review-state.json")
    parser.add_argument("--data", help="JSON finding object")
    args = parser.parse_args(argv)

    if args.check:
        print("record_finding.py is ready")
        return 0

    if not args.state or not args.data:
        parser.error("the following arguments are required: --state, --data")
        print("record_finding.py is ready")
        return 0

    state_path = Path(args.state)
    state = _load_state(state_path)
    finding = json.loads(args.data)

    missing = REQUIRED - finding.keys()
    if missing:
        print(f"ERROR: missing keys {missing}", file=sys.stderr)
        return 1

    scratch = Path(state["scratch_dir"])
    log = scratch / "findings.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)

    existing = set()
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.add(json.loads(line).get("finding_id"))

    if finding["finding_id"] in existing:
        print("record_finding.py: finding already recorded; no change")
        return 0

    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(finding, ensure_ascii=False) + "\n")

    print(f"record_finding.py: recorded {finding['finding_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
