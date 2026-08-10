# node-lens-dispatch

## Purpose
Dispatch only the lens reviewers whose `## Applies to` rules match the PR.

## Inputs
- All `reviewer-*.md` files in the Devin Desktop agents search path
- Full branch `<diff_path>`
- `<pr_description>`
- `<scan_findings>`
- `review-log-orchestrator-self-review.md` (the filled log, not the template)
- Lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>`)
- Off-repo `<scratch_dir>`

## Recipe

1. Run `select_lenses.py` to discover matching lenses:
   ```
   py -3 .agents/skills/iterative-review/scripts/select_lenses.py --state <scratch_dir>/review-state.json --apply
   ```
2. Read `<scratch_dir>/lenses.jsonl`; each line is a lens to dispatch.
3. Build the common input package: `<diff_path>`, `<pr_description>`, `<scan_findings>`, and `review-log-orchestrator-self-review.md`. If the lens's `## Inputs` section calls for `<plan_path>`, `<spec_path>`, or `<roadmap_path>`, add the requested file to that lens's package.
4. `run_subagent` each lens from `lenses.jsonl` with its `profile_path`, `output_path`, and the lens-specific input package.
5. Wait for all `run_subagent` calls to complete. From each `review-log-<lens>.md`, extract the terminal (last) line.
6. If no lens matches, continue to `lens-triage` with the orchestrator-self-review log.
7. If `run_subagent` is unavailable, route to `blocked`.

`lens-dispatch` is a one-time dispatch. After this node, the graph routes to `normalize-inputs` and then `lens-triage`. Downstream fix handling (`metrics-track` -> `finding-fix` -> `re-preflight` -> `reviewer-fixes`) re-runs only the lens associated with the finding being fixed; do not re-dispatch all lenses.

## Outputs
- Write `review-log-<lens>.md` for each dispatched lens

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
