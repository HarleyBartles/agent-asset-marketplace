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
1. Run the routing validator:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --propose final-strong --metrics <scratch_dir>/review-metrics.json
   ```
2. If exit 1, do not dispatch `reviewer-strong`; route to the allowed node.
3. If exit 0, build the input package and `run_subagent` `reviewer-strong` to the `<log_path>`.
4. If `reviewer-strong: clean` and the preflight is clean, go to `closeout`.
5. If findings are reported, go to `metrics-track` to start a new fix loop.
6. If a `contested` or `load-bearing` finding is reported, go to `blocked`.

## Outputs
- Write `review-log-strong.md`
- Update `review-metrics.json` if findings are reported

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
