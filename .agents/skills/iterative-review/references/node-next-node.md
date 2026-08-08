# node-next-node

## Purpose
Validate the proposed graph node against the current state before dispatching a subagent.

## Inputs
- `<scratch_dir>/review-metrics.json`
- Proposed `<node>` name

## Recipe
1. Call `next_node.py` without `--propose` at the start of each turn to discover the single allowed next node. Discovery is read-only and does not modify `review-metrics.json`.
2. Before every `run_subagent` dispatch, run:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --propose <node> --metrics <scratch_dir>/review-metrics.json
   ```
3. If exit 0, the dispatch is allowed and `next_node.py` advances `current_node` and `previous_node` to the dispatched node.
4. If exit 1, do not dispatch the subagent; route to the allowed node printed in the output.

## Outputs
- Console routing decision
- The discovery call (no `--propose`) is read-only
- The validation call (`--propose`) advances `current_node` and `previous_node` in `review-metrics.json`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
