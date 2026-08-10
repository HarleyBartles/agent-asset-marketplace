# node-orchestrator-self-review

## Purpose
Run a cheap, mechanical prediction pass by the orchestrator over the full diff using each relevant lens checklist.

## Actor
Orchestrator only. Do not use `run_subagent`, `subagent_explore`, `implementer`, `reviewer-*`, or any other subagent in this node. The orchestrator must perform the cheap mechanical scan itself.

## Tools
Use shell/pattern tools such as `grep`, `py -3 -c`, `Select-String`, `ripgrep`, or the repository's deterministic `ci --check` targets to scan `<diff_path>` for checklist patterns. If the diff is too large for a quick full scan, narrow to the patterns in each `## Checklist` and still record predictions. Do not expand the scope by delegating the scan to a subagent.

## Inputs
- Full branch `<diff_path>`
- `reviewer-*.md` lens profiles from the Devin Desktop agents search path
- `references/review-log-orchestrator-self-review-template.md` for the log skeleton
- Off-repo `<scratch_dir>`

## Recipe
1. Read `references/review-log-orchestrator-self-review-template.md` to get the log skeleton.
2. For each relevant `reviewer-*.md` profile, read its `## Checklist` and `## Applies to` sections.
3. Use `## Applies to` only to decide relevance; still scan the full diff for checklist patterns. The orchestrator must perform this scan with the tools above. Do not call a subagent to do a full lens review; `lens-dispatch` will run the parallel lens reviewers after this node.
4. Fix predictable issues with high confidence.
5. Record the completed self-review in `review-log-orchestrator-self-review.md` in the off-repo scratch by appending the filled template with `record_orchestrator_log.py`. Save the filled template to a temporary file and pass it via `--data-file`:
   ```bash
   py -3 .agents/skills/iterative-review/scripts/record_orchestrator_log.py \
       --state <scratch_dir>/review-state.json \
       --node orchestrator-self-review \
       --data-file <temp_filled_template.md> \
       --apply
   ```
6. Update `<scan_findings>` after the fixes.

## Outputs
- Write `review-log-orchestrator-self-review.md`
- Update `<scan_findings>`

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
