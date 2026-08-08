# node-re-preflight

## Purpose
Re-run the consumer's canonical preflight after a fix to catch newly introduced deterministic issues.

## Inputs
- Post-fix branch working tree
- `<scan_findings>`
- Consumer preflight command

## Recipe
1. Re-run the consumer's canonical preflight over the post-fix range.
2. If it reports new deterministic issues, go to `fast-fix`.
3. If it is clean, go to `reviewer-fixes`.

## Outputs
- Updated `<scan_findings>`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
