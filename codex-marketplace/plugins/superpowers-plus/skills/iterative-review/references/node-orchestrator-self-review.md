# node-orchestrator-self-review

## Purpose
Run a cheap, mechanical prediction pass over the full diff using each relevant lens checklist.

## Inputs
- Full branch `<diff_path>`
- `reviewer-*.md` lens profiles from the Devin Desktop agents search path
- Off-repo `<scratch_dir>`

## Recipe
1. For each relevant `reviewer-*.md` profile, read its `## Checklist` and `## Applies to` sections.
2. Use `## Applies to` only to decide relevance; still scan the full diff for checklist patterns.
3. Fix predictable issues with high confidence.
4. Record uncertain items in `review-log-orchestrator-self-review.md` in the off-repo scratch.
5. Update `scan_findings` after the fixes.

## Outputs
- Write `review-log-orchestrator-self-review.md`
- Update `<scan_findings>`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
