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
5. On `PASS`, leave `review-metrics.json` unchanged and route to `resolved-ledger`.
6. On `FAIL`, update `review-metrics.json`:
   - Add the original finding to `rounds_per_finding` with `fix_round` incremented by 1.
   - Route back to `finding-fix`.

## Outputs
- `review-log-reviewer-fixes.md` ending with exactly one of:
  - `reviewer-fixes: PASS`
  - `reviewer-fixes: FAIL`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --json --metrics <scratch_dir>/review-metrics.json
