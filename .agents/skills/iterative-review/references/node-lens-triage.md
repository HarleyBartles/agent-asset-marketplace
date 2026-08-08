# node-lens-triage

## Purpose
Normalize lens reports and classify every finding into a severity-based routing bucket.

## Inputs
- Off-repo `<scratch_dir>` containing `review-log-<lens>.md` files
- `## Checklist` severity language from each lens profile

## Recipe
1. Run `py -3 .agents/skills/iterative-review/scripts/normalize_review_inputs.py --apply <scratch_dir>` to ensure all lens reports are plain UTF-8.
2. Classify every finding from the lens reports:
   - `blocking/important` -> `metrics-track` then `finding-fix`
   - `trivial/deferred` -> `final-strong`
   - `contested` or `load-bearing` -> `blocked`
   - `clean` (no lens findings) -> `final-strong`

## Outputs
- Routing decision
- `review-metrics.json` is not directly modified

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
