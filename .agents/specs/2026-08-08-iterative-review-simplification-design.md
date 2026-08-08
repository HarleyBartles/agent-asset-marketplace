# Simplify the `iterative-review` skill surface

## Goal

Keep the full iterative review graph and subagent loop, but make the skill easy for an orchestrator to run one step at a time without holding the entire graph, walkthrough, and every node recipe in context.

## Problem

The current `iterative-review/SKILL.md` is a single, long walkthrough that an orchestrator must load and interpret at every turn. It mixes:
- the canonical state graph,
- the per-node recipes,
- subagent input packaging,
- file formatting rules,
- metrics bookkeeping,
- and the new `next_node.py`/`resolved_ledger.py` gates.

That makes it easy for an orchestrator to lose its place, dispatch out of order, or skip the mechanical gates. The graph is robust by design, but the skill surface is more complex than necessary.

## Proposed design

### 1. `SKILL.md` becomes a thin orchestrator

The body of `SKILL.md` shrinks to:

1. Determine `<base>`, `<branch>`, and create the off-repo scratch workspace.
2. Create an empty `review-metrics.json` in the scratch.
3. Run the mechanical next-node validator:
   ```
   py -3 .agents/skills/iterative-review/scripts/next_node.py --metrics <scratch_dir>/review-metrics.json
   ```
4. Open `references/node-<node>.md` for the node printed by `next_node.py` and follow it exactly.
5. Return to step 3 after the node is done.
6. Stop when `next_node.py` prints `ready` or `blocked`.

That is the entire routine. No other node logic lives in `SKILL.md`.

### 2. New `references/node-*.md` files (one per graph node)

Each `references/node-<name>.md` is a self-contained recipe for a single graph node. The template:

- `# node-<name>`
- `## Purpose` — one sentence.
- `## Inputs` — the exact files and variables needed.
- `## Recipe` — the concrete steps, shell commands, and `run_subagent` calls.
- `## Outputs` — files to write and `review-metrics.json` fields to update.
- `## Next check` — the `next_node.py` command to run before leaving.

Initial set:

- `node-setup.md`
- `node-preflight.md`
- `node-fast-fix.md`
- `node-orchestrator-self-review.md`
- `node-lens-dispatch.md`
- `node-lens-triage.md`
- `node-finding-fix.md`
- `node-reviewer-fixes.md`
- `node-regression-scan.md`
- `node-resolved-ledger.md`
- `node-final-strong.md`
- `node-closeout.md`
- `node-ready.md`
- `node-blocked.md`

### 3. `next_node.py` is the single source of truth for routing

`next_node.py` remains the mechanical gate. It reads `review-metrics.json` and prints the one allowed next node. No node reference should ever contradict it. If a node reference finishes and the orchestrator is tempted to dispatch the next subagent, it must call `next_node.py` first.

### 4. What does not change

- `references/review-state-graph.md` stays the canonical graph.
- `references/review-metrics-schema.json` stays the metrics contract.
- `references/review-log-orchestrator-self-review.md` and `references/review-log-resolved-ledger.md` stay.
- `scripts/next_node.py`, `scripts/resolved_ledger.py`, and `scripts/normalize_review_inputs.py` stay as-is.
- The `reviewer-*.md` subagent profiles stay as-is.
- The consumer's `ci --check` contract stays as-is.

### 5. Benefits

- An agent running the skill only needs to hold one node recipe in context at a time.
- The `SKILL.md` cannot become stale with respect to the graph because it does not describe the graph; it delegates to `next_node.py` and the node references.
- Node recipes can be tested and versioned independently.
- The `next_node.py` gate is impossible to skip because the skill explicitly re-runs it every turn.
- Progressive discovery: a user can read the skill for the orchestrator pattern, then open the node they actually need.

## Acceptance criteria

1. `iterative-review/SKILL.md` is reduced to the 6-step orchestrator above.
2. Every current node section in `SKILL.md` is extracted into a `references/node-<name>.md` file that matches the template.
3. `next_node.py` still validates the graph and can still be called with `--propose`.
4. `py -3 tools/run.py ci --check` passes after the refactor.
5. A test walkthrough of a trivial PR follows the new structure successfully.

## Out of scope

- Changing the graph itself.
- Adding new scripts or new subagent profiles.
- Changing `reviewer-strong.md` or the `final-strong` guard.
