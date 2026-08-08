# node-preflight

## Purpose
Run the consumer's canonical preflight on the branch and gate on a clean result.

## Inputs
- Branch working tree
- Consumer's canonical preflight command from `AGENTS.md` or `.devin/rules`
- `<scan_findings>` file path

## Recipe
1. Run the consumer's canonical preflight on the branch; for this repo use `py -3 tools/run.py ci --check`.
2. Count the deterministic findings and update `review-metrics.json`:
   - `findings_by_node.preflight` = number of findings (0 if clean)
3. Do not proceed until the preflight is clean or its findings are converted to a `fast-fix` and re-checked.

## Outputs
- Updated `<scan_findings>` file
- `review-metrics.json` with `findings_by_node.preflight`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
