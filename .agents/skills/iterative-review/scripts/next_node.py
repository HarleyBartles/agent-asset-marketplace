#!/usr/bin/env python3
"""next_node.py  -  mechanical next-node validator for the iterative-review graph.

Classification (read-only/mutating/mixed): mixed.
- --check                 read-only self-check; exits 0
- --metrics <path>        discovery (read-only) or commit gate (mutating)
- --ledger <path>         path to review-log-resolved-ledger.md (default: sibling of --metrics)
- --propose <node>        commit gate; if <node> is the allowed next node, exits 0 and
                          merges current_node/previous_node into review-metrics.json
- --json                  machine-readable discovery; emits {"node": "...", "reason": "..."}
- no --propose            read-only discovery; prints the allowed next node

The orchestrator must call this before any node recipe (use --propose to advance
state) and must not proceed if it exits 1. The script is the mechanical source of
truth for the graph; it returns the single allowed next node given the state in
review-metrics.json.

State contract: when --propose succeeds, _save_metrics re-reads the on-disk
review-metrics.json and updates only previous_node and current_node, preserving
all other fields (findings_by_node, rounds_per_finding, regressions, custom).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# Canonical graph transitions. Each key is a completed node; the value is a list
# of (condition, next_node) tuples. The first matching condition wins. If no
# condition matches, the default linear next node is used.
#
# Conditions are one of:
#   - "always": unconditional
#   - "green": the previous step has no remaining work (see _green)
#   - "red": the previous step has remaining work (see _red)
#   - "findings": unresolved blocking/important findings exist
#   - "no_findings": no unresolved blocking/important findings exist
#   - "regressions": unresolved regressions exist
#   - "clean": the previous lens pass reported nothing to fix
#   - "trivial": only trivial/deferred findings remain
#   - "contested": a contested/load-bearing finding exists
#   - "ledger_missing": the resolved-ledger evidence file is missing
#   - "ready": the resolved-ledger evidence file is present and clean
#   - "more_findings": unresolved findings remain in the queue
#   - "all_resolved": all findings are resolved

GRAPH: dict[str, list[tuple[str, str]]] = {
    "setup": [("always", "normalize-inputs")],
    "preflight": [
        ("red", "fast-fix"),
        ("green", "scope-honesty"),
    ],
    "fast-fix": [("always", "preflight")],
    "scope-honesty": [("always", "orchestrator-self-review")],
    "orchestrator-self-review": [("always", "lens-dispatch")],
    "lens-dispatch": [("always", "normalize-inputs")],
    "normalize-inputs": [
        ("after_lens_dispatch", "lens-triage"),
        ("after_setup", "preflight"),
    ],
    "lens-triage": [
        ("contested", "blocked"),
        ("findings", "metrics-track"),
        ("trivial", "final-strong"),
        ("clean", "final-strong"),
    ],
    "metrics-track": [("always", "finding-fix")],
    "finding-fix": [
        ("round_cap", "blocked"),
        ("always", "re-preflight"),
    ],
    "re-preflight": [
        ("red", "fast-fix"),
        ("green", "reviewer-fixes"),
    ],
    "reviewer-fixes": [
        ("contested", "blocked"),
        ("new_issue", "metrics-track"),
        ("non_trivial", "regression-scan"),
        ("fixed", "resolved-ledger"),
        ("not_fixed", "finding-fix"),
    ],
    "regression-scan": [
        ("clean", "resolved-ledger"),
        ("new_issue", "metrics-track"),
    ],
    "resolved-ledger": [
        ("more_findings", "finding-fix"),
        ("all_resolved", "final-strong"),
    ],
    "final-strong": [
        ("contested", "blocked"),
        ("findings", "metrics-track"),
        ("clean", "closeout"),
    ],
    "closeout": [("always", "ready")],
    "ready": [("always", "ready")],  # terminal
    "blocked": [("always", "blocked")],  # terminal
}


def _load_metrics(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save_metrics(path: Path, metrics: dict) -> None:
    # Merge-write: re-read the on-disk file and overwrite only the node pointers
    # so that externally-updated fields (findings_by_node, rounds_per_finding,
    # regressions, custom fields) are never clobbered.
    existing = _load_metrics(path)
    existing["previous_node"] = metrics.get("previous_node")
    existing["current_node"] = metrics.get("current_node")
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def _unresolved_severities(metrics: dict) -> list[str]:
    rounds = metrics.get("rounds_per_finding", [])
    return [
        f.get("finding_id", "?")
        for f in rounds
        if f.get("severity") in ("blocking", "important") and not f.get("resolved_at_node")
    ]


def _condition_holds(condition: str, metrics: dict, ledger: Path, current_node: str) -> bool:
    unresolved = _unresolved_severities(metrics)
    regressions = metrics.get("regressions", [])
    findings_by_node = metrics.get("findings_by_node", {})
    ledger_missing = not ledger.exists()
    previous_node = metrics.get("previous_node", "")

    if condition == "always":
        return True
    if condition == "after_lens_dispatch":
        return previous_node == "lens-dispatch"
    if condition == "after_setup":
        return previous_node == "setup"
    if condition == "ready":
        return not ledger_missing
    if condition == "ledger_missing":
        return ledger_missing
    if condition == "findings":
        return bool(unresolved)
    if condition == "no_findings":
        return not unresolved
    if condition == "regressions":
        return bool(regressions)
    if condition == "contested":
        # A blocked flag in the metrics means a finding was contested/load-bearing.
        return any(f.get("contested") for f in metrics.get("rounds_per_finding", []))
    if condition == "more_findings":
        # Used from resolved-ledger when additional findings remain queued.
        return bool(unresolved)
    if condition == "all_resolved":
        return not unresolved and not ledger_missing
    if condition == "clean":
        # After a lens/scan, "clean" means no unresolved blocking/important.
        return not unresolved
    if condition == "trivial":
        # trivial/deferred only: there are rounds but none are blocking/important and no unresolved.
        rounds = metrics.get("rounds_per_finding", [])
        has_unresolved = bool(unresolved)
        has_trivial = any(f.get("severity") in ("trivial", "deferred") for f in rounds)
        return not has_unresolved and has_trivial
    if condition == "red":
        # preflight/re-preflight is "red" when the node has findings.
        return findings_by_node.get(current_node, 0) > 0
    if condition == "green":
        return findings_by_node.get(current_node, 0) == 0
    if condition == "round_cap":
        # finding-fix is blocked if any finding has exceeded the round cap.
        return any(
            (f.get("fix_round", 0) or 0) >= 4
            for f in metrics.get("rounds_per_finding", [])
            if not f.get("resolved_at_node")
        )
    if condition == "fixed":
        # reviewer-fixes reached a clean outcome for the original finding.
        return not unresolved and not regressions
    if condition == "not_fixed":
        # Original finding is not resolved.
        return bool(unresolved)
    if condition == "new_issue":
        # reviewer-fixes or regression-scan discovered a new issue.
        return bool(unresolved) or bool(regressions)
    if condition == "non_trivial":
        # Flag set by the reviewer-fixes recipe for non-trivial/cross-cutting fixes.
        return metrics.get("non_trivial_fix", False)

    return False


def _next_node(metrics: dict, ledger: Path) -> tuple[str, str]:
    current = metrics.get("current_node")
    if not current or current not in GRAPH:
        return "setup", "no current_node in review-metrics.json yet"

    transitions = GRAPH[current]
    for condition, next_node in transitions:
        if _condition_holds(condition, metrics, ledger, current):
            return next_node, f"from {current}: {condition} -> {next_node}"

    # Fall back to the old guard for unresolved / regressions / ledger if the
    # state machine has not yet covered the current node.
    unresolved = _unresolved_severities(metrics)
    if unresolved:
        return "finding-fix", f"unresolved important/blocking: {', '.join(unresolved)}"
    if metrics.get("regressions", []):
        return "regression-scan", f"{len(metrics['regressions'])} unresolved regression(s)"
    if not ledger.exists():
        return "resolved-ledger", "resolved-ledger evidence file is missing"
    return "final-strong", "all important findings resolved and ledger evidence present"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Return or validate the allowed next node. (mixed)")
    parser.add_argument("--check", action="store_true", help="self-check; exits 0 if ready")
    parser.add_argument("--metrics", help="path to review-metrics.json")
    parser.add_argument("--ledger", help="path to review-log-resolved-ledger.md")
    parser.add_argument("--propose", help="proposed next node to validate")
    parser.add_argument("--json", action="store_true", help="emit machine-readable discovery JSON")
    args = parser.parse_args(argv)

    if not args.check and not args.metrics:
        print("--metrics is required when not using --check", file=sys.stderr)
        return 2

    if args.check:
        print("next_node.py is ready")
        return 0

    metrics_path = Path(args.metrics)
    ledger_path = Path(args.ledger) if args.ledger else metrics_path.parent / "review-log-resolved-ledger.md"
    metrics = _load_metrics(metrics_path)
    node, reason = _next_node(metrics, ledger_path)

    if not args.propose:
        # Discovery is read-only: it reports the allowed next node from the
        # current state without advancing state.
        if args.json:
            print(json.dumps({"node": node, "reason": reason}, ensure_ascii=False))
        else:
            print(f"{node}\n# {reason}")
    elif args.propose == node:
        print(f"ALLOWED: {args.propose}  -  {reason}")
        # The validator advances state on a successful dispatch gate so the
        # next discovery call continues from the just-authorized node.
        metrics["previous_node"] = metrics.get("current_node", "")
        metrics["current_node"] = node
        _save_metrics(metrics_path, metrics)
    else:
        print(f"BLOCKED: proposed {args.propose}; allowed next node is {node}  -  {reason}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
