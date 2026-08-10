# node-lens-triage

## Purpose
Normalize lens reports and classify every finding into a severity-based routing bucket.

## Inputs
- Off-repo `<scratch_dir>` containing `review-log-<lens>.md` files
- `## Checklist` severity language from each lens profile

## Recipe
1. Run `py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>` to ensure all lens reports are plain UTF-8.
2. Classify every finding from the lens reports. For each finding, call:
   ```bash
   py -3 .agents/skills/iterative-review/scripts/record_finding.py \
       --state <scratch_dir>/review-state.json \
       --data '{"finding_id": "<finding_id>", "lens": "<lens>", "discovered_at_node": "lens-triage", "discovered_at_round": <round>, "severity": "<severity>", "contested": <true|false>}'
   ```
   Then regenerate the metrics file:
   ```bash
   py -3 .agents/skills/iterative-review/scripts/compile_metrics.py \
       --state <scratch_dir>/review-state.json \
       --metrics <scratch_dir>/review-metrics.json
   ```
3. Route:
   - Any `contested`/`load-bearing` finding -> `blocked`
   - Any `blocking/important` finding -> `metrics-track` then `finding-fix`
   - Only `trivial/deferred` findings -> `final-strong`
   - No findings -> `final-strong`

## Outputs
- Routing decision
- `<scratch_dir>/review-metrics.json` regenerated from `<scratch_dir>/review-state.json` and the recorded finding logs

## Next check
```bash
py -3 .agents/skills/iterative-review/scripts/next_node.py \
    --state <scratch_dir>/review-state.json \
    --propose <next-node>
```
