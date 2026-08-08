# node-fast-fix

## Purpose
Fix deterministic preflight findings and return to the `preflight` node.

## Inputs
- `<scan_findings>`
- Branch working tree
- Consumer preflight command

## Recipe
1. Read the deterministic findings from `<scan_findings>`.
2. Apply the cheapest fixes for each finding.
3. Return to `preflight` and re-run the consumer's canonical preflight.

## Outputs
- Edited working tree and/or new commit
- Updated `<scan_findings>`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
