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

### Dispatch table

| Lens profile | Focus | Output file |
|---|---|---|
| reviewer-plans | plan/spec compliance | review-log-plans.md |
| reviewer-skills | skill/portable surface | review-log-skills.md |
| reviewer-scripts | scripts and CLI | review-log-scripts.md |
| reviewer-marketplace | marketplace bundle | review-log-marketplace.md |
| reviewer-security | security posture | review-log-security.md |
| reviewer-strong | final strong review (when requested) | review-log-strong.md |
| reviewer-mesh | generated mesh / INDEX.md / scaffolder | review-log-mesh.md |

### Common package
All dispatched lenses receive: `<diff_path>`, `<pr_description>`, `<scan_findings>`, and `review-log-orchestrator-self-review.md`.

### Procedure
1. Discover every `reviewer-*.md` file in the agents search path.
2. For each lens profile, read its `## Applies to` section and match in this order:
   - If an `inputs` entry is provided by the orchestrator, dispatch the lens.
   - If a `globs` pattern matches a changed file in the diff, dispatch the lens.
   - If a `keywords` string appears in the diff or in `<pr_description>`, dispatch the lens.
3. Build the input package for each matching lens from the common package plus any lens-specific inputs.
4. Assign each lens a concrete `<log_path>` such as `$scratch/review-log-<lens>.md`.
5. `run_subagent` each selected lens using the `reviewer-*.md` profile content and the off-repo workspace.
6. Wait for all `run_subagent` calls to complete. From each `review-log-<lens>.md`, extract the terminal (last) line.
7. If no lens matches, continue to `lens-triage` with the orchestrator-self-review log.
8. If `run_subagent` is unavailable, route to `blocked`.

## Outputs
- Write `review-log-<lens>.md` for each dispatched lens

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
