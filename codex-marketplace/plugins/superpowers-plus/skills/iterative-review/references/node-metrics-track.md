# node-metrics-track

## Purpose
Record the discovery context for each finding in `review-metrics.json`.

## Inputs
- Findings from the current node
- Round number
- Originating lens
- Severity classification

## Recipe
1. For each finding, record the node that discovered it, the round, the lens, and the severity in `review-metrics.json`.

## Outputs
- Update `review-metrics.json` fields:
  - `findings_by_node`
  - `rounds_per_finding`
  - `regression_class`
  - `regression_of`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
