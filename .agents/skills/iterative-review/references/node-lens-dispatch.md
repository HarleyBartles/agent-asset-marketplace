# node-lens-dispatch

## Purpose
Dispatch only the lens reviewers whose `## Applies to` rules match the PR.

## Inputs
- All `reviewer-*.md` files in the Devin Desktop agents search path
- Full branch `<diff_path>`
- `<pr_description>`
- `<scan_findings>`
- `review-log-orchestrator-self-review.md`
- Lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>`)
- Off-repo `<scratch_dir>`

## Recipe

1. Run `select_lenses.py` to discover matching lenses:
   ```
   py -3 .agents/skills/iterative-review/scripts/select_lenses.py --state <scratch_dir>/review-state.json --apply
   ```
2. Read `<scratch_dir>/lenses.jsonl`; each line is a lens to dispatch.
3. Build the common input package: `<diff_path>`, `<pr_description>`, `<scan_findings>`, and `review-log-orchestrator-self-review.md`.
4. `run_subagent` each lens from `lenses.jsonl` with its `profile_path` and `output_path`.
5. `run_subagent` each selected lens using the `reviewer-*.md` profile content and the off-repo workspace.
6. Wait for all `run_subagent` calls to complete. From each `review-log-<lens>.md`, extract the terminal (last) line.
7. If no lens matches, continue to `lens-triage` with the orchestrator-self-review log.
8. If `run_subagent` is unavailable, route to `blocked`.

## Outputs
- Write `review-log-<lens>.md` for each dispatched lens

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
