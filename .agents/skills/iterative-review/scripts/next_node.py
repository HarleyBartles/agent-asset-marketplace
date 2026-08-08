#!/usr/bin/env python3
"""next_node.py — mechanical next-node validator for the iterative-review graph.

Contract:
- --help                  prints usage
- --check                 self-check; exits 0
- --metrics <path>        path to review-metrics.json
- --ledger <path>         path to review-log-resolved-ledger.md
- --propose <node>        if given, exits 0 only if <node> is the allowed next node

The orchestrator must call this before every run_subagent dispatch and must not
proceed if it exits 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _unresolved_severities(metrics: dict) -> list[str]:
    rounds = metrics.get("rounds_per_finding", [])
    return [
        f.get("finding_id", "?")
        for f in rounds
        if f.get("severity") in ("blocking", "important") and not f.get("resolved_at_node")
    ]


def _next_node(metrics: dict, ledger: Path) -> tuple[str, str]:
    if not metrics:
        return "setup", "no review-metrics.json yet"
    unresolved = _unresolved_severities(metrics)
    regressions = metrics.get("regressions", [])
    if unresolved:
        return "finding-fix", f"unresolved important/blocking: {', '.join(unresolved)}"
    if regressions:
        return "regression-scan", f"{len(regressions)} unresolved regression(s)"
    if not ledger.exists():
        return "resolved-ledger", "resolved-ledger evidence file is missing"
    return "final-strong", "all important findings resolved and ledger evidence present"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Return or validate the allowed next node for iterative-review.")
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--metrics", help="path to review-metrics.json")
    parser.add_argument("--ledger", help="path to review-log-resolved-ledger.md")
    parser.add_argument("--propose", help="proposed next node to validate")
    args = parser.parse_args(argv)

    if args.check:
        print("next_node.py is ready")
        return 0

    if not args.metrics:
        print("--metrics is required when not using --check", file=sys.stderr)
        return 2

    metrics_path = Path(args.metrics)
    ledger_path = Path(args.ledger) if args.ledger else metrics_path.parent / "review-log-resolved-ledger.md"
    metrics = _load_metrics(metrics_path)
    node, reason = _next_node(metrics, ledger_path)

    if not args.propose:
        print(f"{node}\n# {reason}")
        return 0

    if args.propose == node:
        print(f"ALLOWED: {args.propose} — {reason}")
        return 0

    print(f"BLOCKED: proposed {args.propose}; allowed next node is {node} — {reason}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
