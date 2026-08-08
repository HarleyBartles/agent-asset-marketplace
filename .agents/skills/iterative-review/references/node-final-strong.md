# node-final-strong

## Purpose
Run one whole-branch `reviewer-strong` pass after all `blocking/important` findings are resolved.

## Inputs
- Full branch diff
- `<pr_description>`
- All lens logs
- `review-log-resolved-ledger.md`
- `review-metrics.json`
- `reviewer-strong` profile
- `<log_path>`

## Recipe
1. Validate the dispatch:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --propose final-strong --metrics <scratch_dir>/review-metrics.json
   ```
2. Build the input package and `run_subagent` `reviewer-strong` to the `<log_path>`.
3. If `reviewer-strong: clean` and the preflight is clean, go to `closeout`.
4. If findings are reported, update `rounds_per_finding` in `review-metrics.json` and go to `metrics-track` to start a new fix loop.
5. If a `contested` or `load-bearing` finding is reported, set `contested: true` on the finding and go to `blocked`.

## Outputs
- Write `review-log-strong.md`
- Update `review-metrics.json` if findings are reported

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
