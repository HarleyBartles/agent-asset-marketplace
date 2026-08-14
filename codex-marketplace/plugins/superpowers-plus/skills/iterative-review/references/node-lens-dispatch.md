# node-lens-dispatch

## Purpose
Dispatch the cheap `reviewer-fast` pre-lens plus the matching deep lens reviewers.

## Inputs
- All `reviewer-*.md` files in the Devin Desktop agents search path
- Full branch `<diff_path>`
- `<pr_description>`
- `<scan_findings>`
- `review-log-reviewer-fast.md` (the pre-lens report from `reviewer-fast`)
- Lens-specific inputs (`<plan_path>`, `<spec_path>`, `<roadmap_path>`)
- Off-repo `<scratch_dir>`

## Recipe

1. Run `select_lenses.py` to discover matching lenses. `reviewer-fast` matches all diffs and will be included first, but only if `review-log-reviewer-fast.md` does not already exist in the scratch dir:
   ```
   py -3 .agents/skills/iterative-review/scripts/select_lenses.py --state <scratch_dir>/review-state.json --apply
   ```
   If the pre-lens has already run, `select_lenses.py` will skip `reviewer-fast`.
2. Read `<scratch_dir>/lenses.jsonl`; each line is a lens to dispatch.
3. Build the common input package: `<diff_path>`, `<pr_description>`, `<scan_findings>`, and `review-log-reviewer-fast.md`. If the lens's `## Inputs` section calls for `<plan_path>`, `<spec_path>`, or `<roadmap_path>`, add the requested file to that lens's package.
4. `run_subagent` each lens from `lenses.jsonl` with its `profile_path`, `output_path`, and the lens-specific input package.
5. Wait for all `run_subagent` calls to complete. From each `review-log-<lens>.md`, extract the terminal (last) line.
6. If no deep lens matches, `reviewer-fast` still runs; continue to `lens-triage` with its log.
7. If `run_subagent` is unavailable, route to `blocked`.

`lens-dispatch` is a one-time dispatch. `reviewer-fast` is a one-shot preflight and must not be re-dispatched. After this node, the graph routes to `normalize-inputs` and then `lens-triage`. Downstream fix handling (`metrics-track` -> `finding-fix` -> `re-preflight` -> `reviewer-fixes`) re-runs only the lens associated with the finding being fixed; do not re-dispatch all lenses and do not re-run `reviewer-fast`.

## Outputs
- Write `review-log-<lens>.md` for each dispatched lens

## Next check
py -3 .agents/skills/iterative-review/scripts/next_node.py --state <scratch_dir>/review-state.json
