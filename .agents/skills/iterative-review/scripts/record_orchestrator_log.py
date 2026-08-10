#!/usr/bin/env python3
"""record_orchestrator_log.py - append an orchestrator markdown log for a node. (mixed)"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def _load_state(state_path: Path) -> dict:
    with state_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append an orchestrator markdown log. (mixed)")
    parser.add_argument("--state", help="Path to review-state.json")
    parser.add_argument("--node", help="Node name (used for review-log-<node>.md)")
    parser.add_argument("--data", help="Markdown content to append")
    parser.add_argument("--apply", action="store_true", help="Append the log")
    parser.add_argument("--check", action="store_true", help="Validate CLI contract")
    args = parser.parse_args(argv)

    if args.check:
        print("record_orchestrator_log.py: --check ok")
        return 0

    if not (args.state and args.node and args.data):
        parser.error("the following arguments are required: --state, --node, --data")

    state = _load_state(Path(args.state))
    scratch = Path(state["scratch_dir"])
    log_path = scratch / f"review-log-{args.node}.md"
    round_ = state.get("round", 1)
    now = datetime.now(timezone.utc).isoformat()
    block = f"\n## Round {round_} - {now}\n\n{args.data}\n"

    if not args.apply:
        print(f"Would append to {log_path}:\n{block}")
        return 0

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(block)
    print(f"Appended to {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
