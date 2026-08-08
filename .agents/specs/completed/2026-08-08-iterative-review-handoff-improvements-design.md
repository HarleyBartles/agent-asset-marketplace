# Iterative Review Handoff and Router Improvements

## Context

The `iterative-review` skill was simplified to a thin orchestrator: a small graph of `node-*.md` recipes, driven by `next_node.py` and `review-metrics.json`. This spec hardens the handoffs between the orchestrator, `next_node.py`, the `implementer` subagent, and the `reviewer-fixes` lens so the fast-fix loop can run end-to-end without state loss or ambiguous dispatch.

## Scope

This spec covers the items in the implementation plan:

1. `next_node.py` merge-write and `--json` machine-readable output.
2. `finding-fix` decision table and the `implementer` brief template.
3. `reviewer-fixes` fast scoped re-review.
4. `lens-dispatch` explicit dispatch table.
5. Full dogfood of the `implementer` / `reviewer-fixes` fast-fix loop on a real PR.

## Out of scope

- No new graph nodes.
- No changes to the graph topology or routing edges.
- No contract changes to `final-strong` or the terminal review node.

## Acceptance criteria

- [ ] `next_node.py` preserves all fields in `review-metrics.json` other than `current_node` and `previous_node` on every `--propose` write.
- [ ] `next_node.py --json` emits exactly `{"node": "...", "reason": "..."}` on discovery and exits cleanly.
- [ ] `node-finding-fix.md` contains a working `implementer` vs inline decision table and references the `implementer` brief template.
- [ ] The `implementer` brief template includes finding, fix instructions, out-of-scope, verification, and output sections.
- [ ] `node-reviewer-fixes.md` defines a fast scoped re-review of only the surface changed by the fix, with a terminal `reviewer-fixes: PASS` or `reviewer-fixes: FAIL` verdict.
- [ ] On `reviewer-fixes: PASS`, the recipe sets `resolved_at_node` in `review-metrics.json` to the node that fixed the finding.
- [ ] `node-lens-dispatch.md` lists, in a single explicit table, the subagent profile, focus, and output file for each lens, including `reviewer-mesh`.
- [ ] A dogfood PR uses `implementer` at least once and `reviewer-fixes` at least once.
- [ ] All script changes keep `next_node.py --help` and `next_node.py --check` responding correctly.
- [ ] `py -3 tools/run.py ci --check` passes before the final commit.

## Router state contract

`next_node.py` is the single writer of `current_node` and `previous_node` in `review-metrics.json`. When invoked with `--propose <node> --metrics <path>`, it must:

1. Read the existing `review-metrics.json` if it exists.
2. Merge the proposed `current_node` and `previous_node` values into the existing state.
3. Write the file back with all other fields intact, creating the file only when it does not already exist.

No other step, recipe, or subagent may modify `current_node` or `previous_node`.

## Handoff contracts

### `implementer` brief

Input package passed by `node-finding-fix.md` to the `implementer` subagent:

- `finding_id`: stable identifier of the finding.
- `lens`: the lens that produced the finding.
- `surface`: files, functions, or behavior to change.
- `fix_instructions`: exact change to make.
- `out_of_scope`: adjacent code that must not change.
- `verification_command`: the command that confirms the fix.

Outputs:

- Edits to the repository surface.
- A short `fix-report.md` or inline log entry with what changed and why.

### `reviewer-fixes` input/output

Input:

- `review-metrics.json` showing the original finding, the fix node, and the changed surface.
- The original lens checklist, scoped to the changed surface only.

Output:

- A terminal line of either `reviewer-fixes: PASS` or `reviewer-fixes: FAIL`.
- On `PASS`, `resolved_at_node` is set to the node that produced the fix.
- On `FAIL`, the finding is re-queued for another `node-finding-fix` cycle with an updated rationale.
