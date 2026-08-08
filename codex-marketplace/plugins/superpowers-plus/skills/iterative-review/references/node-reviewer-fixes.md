# node-reviewer-fixes

## Purpose
Verify a fix against the originating lens's checklist, tightly scoped to the blast radius.

## Inputs
- `original_finding`
- `fix_diff_path` (`git diff <pre-fix-sha>...<post-fix-sha>`)
- `full_diff_slice_path` (blast radius slices of the full branch diff)
- `lens` and `lens_checklist` from the originating `reviewer-*.md`
- Concrete `<log_path>` (e.g., `$scratch/review-log-fixes.md`)

## Recipe
1. `run_subagent` `reviewer-fixes` with the lens-aware package and the `<log_path>`.
2. Confirm the original finding is resolved.
3. Route by result:
   - Fixed and clean -> `resolved-ledger`
   - Not fixed -> `finding-fix` for the same finding
   - New same-lens/blast-radius issue -> `metrics-track` with `regression_class: same-lens-blast-radius`
   - Non-trivial fix (multi-file, generated surfaces, security/tooling boundary, public interface change) -> `regression-scan`

## Outputs
- Write `review-log-fixes.md`
- Update `review-metrics.json` `regression_class` and `regression_of` when a new issue is found

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
