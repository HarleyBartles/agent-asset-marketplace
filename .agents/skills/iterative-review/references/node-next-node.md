# node-next-node

## Purpose
Validate the proposed graph node against the current state before dispatching a subagent.

## Inputs
- `<scratch_dir>/review-metrics.json`
- Proposed `<node>` name

## Recipe
1. Before every `run_subagent` dispatch, run:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --propose <node> --metrics <scratch_dir>/review-metrics.json
   ```
2. If exit 0, the dispatch is allowed.
3. If exit 1, do not dispatch the subagent; route to the allowed node printed in the output.
4. Call `next_node.py` without `--propose` at the start of each turn to discover the single allowed next node.

## Outputs
- Console routing decision
- `review-metrics.json` is read but not modified

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
