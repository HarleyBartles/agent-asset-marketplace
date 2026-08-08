# node-scope-honesty

## Purpose
Compare the branch diff to the plan, spec, PR body, and linked issues and reconcile any scope drift.

## Inputs
- Full branch `<diff_path>`
- Plan, spec, and roadmap files
- `<pr_description>`
- Linked issues

## Recipe
1. Compare the branch diff to the plan, spec, PR body, and linked issues.
2. If the implemented scope has drifted, update the documents to match the real diff or fix the diff to match the documents.
3. Commit the scope-honesty update.

## Outputs
- Updated plan/spec/PR text or fixed diff
- New commit recording the scope-honesty update

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
