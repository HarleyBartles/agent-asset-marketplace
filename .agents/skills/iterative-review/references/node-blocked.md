# node-blocked

## Purpose
Record an unresolvable blocker and hand the review to a human.

## Inputs
- Contested or load-bearing finding
- `review-metrics.json`

## Recipe
1. Record the blocker in `review-metrics.json` and hand to a human.
2. If the human says "carry on", resume from `metrics-track`.
3. If `next_node.py` or `resolved_ledger.py` returns a `BLOCKED` result, treat it as a graph error: do not override it, do not dispatch `final-strong` out of order, and resume from the allowed node.

## Outputs
- Update `review-metrics.json` blocker fields

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
