# node-scope-honesty

## Purpose
Compare the branch diff to the plan, spec, PR body, and linked issues and reconcile any scope drift.

## Inputs
- Full branch `<diff_path>`
- Plan, spec, and roadmap files
- `<pr_description>`
- Linked issues

## Recipe
1. Compare the branch diff to the PR body, the linked Linear issue body, the plan, the spec, and the roadmap if those inputs were found during `normalize-inputs`.
2. If the implemented scope has drifted, record a `scope-drift` finding with `record_finding.py` or fix the diff to match the documents.
3. If the diff is honest, no record is needed.

## Outputs
- `review-log-scope-honesty.md` with the comparison result
- Any `scope-drift` finding recorded in `findings.jsonl`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json
