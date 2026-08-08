# node-preflight

## Purpose
Run the consumer's canonical preflight on the branch and gate on a clean result.

## Inputs
- Branch working tree
- Consumer's canonical preflight command from `AGENTS.md` or `.devin/rules`
- `<scan_findings>` file path

## Recipe
1. Run the consumer's canonical preflight on the branch; for this repo use `py -3 tools/run.py ci --check`.
2. Do not proceed until the preflight is clean or its findings are converted to a `fast-fix` and re-checked.

## Outputs
- Updated `<scan_findings>` file

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
