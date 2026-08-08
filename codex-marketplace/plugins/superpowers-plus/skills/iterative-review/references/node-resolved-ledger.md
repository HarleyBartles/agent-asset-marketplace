# node-resolved-ledger

## Purpose
Mark findings resolved and generate the resolved-ledger evidence gate.

## Inputs
- `review-metrics.json`
- Off-repo `<scratch_dir>`

## Recipe
1. When `reviewer-fixes` or `regression-scan` is clean, mark the original finding `resolved` and record `resolved_at_node` and `resolved_at_round` in `review-metrics.json`.
2. When the queue is empty, run:
   ```
   py -3 .agents/skills/iterative-review/scripts/resolved_ledger.py --apply --metrics <scratch_dir>/review-metrics.json
   ```
3. If the command exits 1, do not proceed to `final-strong`; return to `finding-fix` or `regression-scan`.
4. If more findings remain in the queue, choose the next one and go to `finding-fix`.
5. If the queue is empty, proceed to `final-strong`.

## Outputs
- Write `review-log-resolved-ledger.md` when every `important`/`blocking` finding has a `resolved_at_node` and `regressions` is empty
- Update `review-metrics.json` fields `resolved_at_node`, `resolved_at_round`, and `regressions`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
