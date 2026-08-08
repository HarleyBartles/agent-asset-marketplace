# node-regression-scan

## Purpose
Widen review to the touched area for non-trivial or cross-cutting fixes to catch regressions.

## Inputs
- Fix diff
- Full branch diff blast radius
- `reviewer-strong` profile
- `review-metrics.json`

## Recipe
1. Dispatch `reviewer-strong` on the touched area with `<log_path>` set to `$scratch/review-log-strong.md`.
2. If the scan is clean, go to `resolved-ledger`.
3. If it finds a new issue, classify it:
   - `same-lens-blast-radius` if in the same lens and blast radius
   - `cross-lens-blast-radius` if in a different lens and blast radius
   - `outside-blast-radius` if outside the blast radius
4. Record the new finding in `metrics-track` with `regression_class` and `regression_of` set to the original finding.
5. Return to `finding-fix`.

## Outputs
- Write `review-log-strong.md`
- Update `review-metrics.json` `regression_class` and `regression_of`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
