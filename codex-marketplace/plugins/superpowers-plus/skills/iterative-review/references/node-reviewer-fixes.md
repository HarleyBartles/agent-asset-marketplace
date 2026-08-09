# node-reviewer-fixes

## Purpose
Verify a fix against the originating lens's checklist, tightly scoped to the blast radius.

## Inputs
- `review-log-<lens>.md` from the original lens that produced the finding
- `review-log-implementer-report.md` (if an `implementer` fixed the finding) or the inline fix diff
- The affected file(s) only — do not re-review the whole branch

## Recipe
1. Load the original lens checklist from `review-log-<lens>.md`.
2. Re-apply that checklist to the changed surface and one step of blast radius only.
3. Confirm the original finding is resolved and no new same-lens issues appear in the blast radius.
4. Write `review-log-reviewer-fixes.md` and end it with exactly one of:
   - `reviewer-fixes: PASS`
   - `reviewer-fixes: FAIL`
5. On `PASS`:
   - Record the resolution:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/record_resolution.py \
         --state <scratch_dir>/review-state.json \
         --data '{"finding_id": "<finding_id>", "resolved_at_node": "reviewer-fixes", "resolved_at_round": <round>}'
     ```
   - Set `non_trivial_fix` to the appropriate value in `<scratch_dir>/review-state.json` (`false` for a typical pass, `true` if the fix should trigger `regression-scan`).
   - Regenerate the metrics file:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/compile_metrics.py \
         --state <scratch_dir>/review-state.json \
         --metrics <scratch_dir>/review-metrics.json
     ```
   - If `non_trivial_fix` is `true`, route to `regression-scan`:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/next_node.py \
         --state <scratch_dir>/review-state.json \
         --metrics <scratch_dir>/review-metrics.json \
         --propose regression-scan
     ```
   - Otherwise, route to `resolved-ledger`:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/next_node.py \
         --state <scratch_dir>/review-state.json \
         --metrics <scratch_dir>/review-metrics.json \
         --propose resolved-ledger
     ```
6. On `FAIL`, do **not** increment `fix_round` (`finding-fix` owns that on the next pass):
   - If the original finding is still unresolved, no new record is needed. Regenerate the metrics file and route back to `finding-fix`:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/compile_metrics.py \
         --state <scratch_dir>/review-state.json \
         --metrics <scratch_dir>/review-metrics.json
     py -3 .agents/skills/iterative-review/scripts/next_node.py \
         --state <scratch_dir>/review-state.json \
         --propose finding-fix
     ```
   - If a new same-lens issue was found, record it and its relationship to the original finding:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/record_finding.py \
         --state <scratch_dir>/review-state.json \
         --data '{"finding_id": "<new_finding_id>", "lens": "<lens>", "discovered_at_node": "reviewer-fixes", "discovered_at_round": <round>, "severity": "<severity>"}'
     py -3 .agents/skills/iterative-review/scripts/record_regression.py \
         --state <scratch_dir>/review-state.json \
         --data '{"fix_for": "<original_finding_id>", "new_finding": "<new_finding_id>", "discovered_at_node": "reviewer-fixes", "discovered_at_round": <round>, "regression_class": "same-lens-blast-radius", "severity": "<severity>"}'
     ```
     Then regenerate the metrics file and route to `metrics-track`:
     ```bash
     py -3 .agents/skills/iterative-review/scripts/compile_metrics.py \
         --state <scratch_dir>/review-state.json \
         --metrics <scratch_dir>/review-metrics.json
     py -3 .agents/skills/iterative-review/scripts/next_node.py \
         --state <scratch_dir>/review-state.json \
         --propose metrics-track
     ```

## Outputs
- `review-log-reviewer-fixes.md` ending with exactly one of:
  - `reviewer-fixes: PASS`
  - `reviewer-fixes: FAIL`
- `<scratch_dir>/review-metrics.json` regenerated from `<scratch_dir>/review-state.json` and the recorded logs

## Next check
```bash
py -3 .agents/skills/iterative-review/scripts/next_node.py \
    --state <scratch_dir>/review-state.json \
    --propose <next-node>
```
