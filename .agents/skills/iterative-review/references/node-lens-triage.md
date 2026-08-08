# node-lens-triage

## Purpose
Normalize lens reports and classify every finding into a severity-based routing bucket.

## Inputs
- Off-repo `<scratch_dir>` containing `review-log-<lens>.md` files
- `## Checklist` severity language from each lens profile

## Recipe
1. Run `py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>` to ensure all lens reports are plain UTF-8.
2. Classify every finding from the lens reports and append it to `rounds_per_finding` in `review-metrics.json`:
   - `discovered_at_node`: `lens-dispatch`
   - `discovered_at_round`: the current round (1 for first `lens-dispatch`, increment for subsequent rounds)
   - `severity`: `blocking`, `important`, `minor`, or `deferred`
   - `contested`: `true` for contested or load-bearing findings
3. Route:
   - Any `contested`/`load-bearing` finding -> `blocked`
   - Any `blocking/important` finding -> `metrics-track` then `finding-fix`
   - Only `trivial/deferred` findings -> `final-strong`
   - No findings -> `final-strong`

## Outputs
- Routing decision
- `rounds_per_finding` and `total_rounds` updated in `review-metrics.json`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
