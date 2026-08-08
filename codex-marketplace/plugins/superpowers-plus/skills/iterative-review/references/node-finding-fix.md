# node-finding-fix

## Purpose
Verify and fix a single `blocking/important` lens finding using an `implementer` subagent.

## Inputs
- `original_finding` with exact text and severity
- `lens` name (e.g., `reviewer-security`)
- `lens_checklist` from the originating `reviewer-*.md`
- `diff_slice` of the full branch diff that the finding touches
- `fix_constraints` (what not to break, tests, consumer `ci --check`)
- `<pre-fix-sha>` and branch working tree

## Recipe
1. Use `receiving-code-review` to verify the finding.
2. Build a task brief for the `implementer` with `original_finding`, `lens`, `lens_checklist`, `diff_slice`, and `fix_constraints`.
3. `run_subagent` `implementer` to edit, run the consumer preflight, and commit.
4. Verify the commit and report.
5. Move to `re-preflight`.
6. Use `implementer` for rounds 1-3; if a finding fails `reviewer-fixes` three times, escalate to `implementer-strong` for round 4; if it still fails, route to `blocked`.

## Outputs
- Commit containing the fix
- Updated `rounds_per_finding` in `review-metrics.json`: increment `fix_round` for the finding being fixed

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
