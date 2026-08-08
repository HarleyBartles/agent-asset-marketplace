# Iterative Review Handoff and Router Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use /subagent-driven-development (recommended) or /executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden `iterative-review` into a fully operational skill by improving the `next_node.py` router I/O, clarifying `implementer` and `reviewer-fixes` subagent handoffs, and dogfooding the full fast-fix loop end-to-end.

**Architecture:** Keep the thin-orchestrator graph, but make the `next_node.py` router safer to drive from scripts and make the `node-*.md` recipes self-contained for subagent dispatch.

**Tech Stack:** Python 3, repository `tools/run.py` validation, `run_subagent` orchestration, existing `.agents/skills/iterative-review` surface.

## Global Constraints

- All script changes must keep `--help` and `--check` responding correctly.
- Marketplace skills must be regenerated with `py -3 tools/run.py installed-skills --apply` after source edits.
- CI preflight `py -3 tools/run.py ci --check` must pass before any commit.
- Source-of-truth for the skill is `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; the `.agents/skills/` copy is generated.
- Generated artifacts are downstream outputs; do not hand-edit the installed copy.

---

### Task 1: Make `next_node.py` merge-write state and emit machine-readable discovery

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Test: scratch `review-metrics.json` walk.

- [ ] **Step 1: Write a failing test shell transcript**.
  Create `Z:\_agent-scratch\test-next-node-merge\review-metrics.json` with `custom_field: preserve_me`. Run `py -3 .agents/skills/iterative-review/scripts/next_node.py --propose setup --metrics <path>`, then check `custom_field`. Expected before fix: missing.
- [ ] **Step 2: Run the test and confirm the failure.**
- [ ] **Step 3: Rewrite `_save_metrics` to merge.** Keep only `current_node` and `previous_node` updates, preserving all other fields.
- [ ] **Step 4: Add `--json` flag.** Discovery emits `{"node": "<node>", "reason": "<reason>"}`.
- [ ] **Step 5: Update the docstring** to mention `--json` and the merge contract.
- [ ] **Step 6: Re-run the test transcript and verify `custom_field` is preserved.**
- [ ] **Step 7: Run `--json` discovery and parse the output.**
- [ ] **Step 8: Run `installed-skills` and `ci --check`.**
- [ ] **Step 9: Commit.**

---

### Task 2: Harden `node-finding-fix.md` with implementer vs inline decision table

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-finding-fix.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-log-implementer-brief-template.md`

- [ ] **Step 1: Replace the `node-finding-fix.md` recipe** with a decision table for `implementer` vs inline.
- [ ] **Step 2: Create the implementer brief template** with finding, fix instructions, out-of-scope, verification, and outputs.
- [ ] **Step 3: Update `node-finding-fix.md` `## Outputs` and `## Next check`.**
- [ ] **Step 4: Regenerate skills and run `ci --check`.**
- [ ] **Step 5: Commit.**

---

### Task 3: Scope `node-reviewer-fixes.md` as a fast re-review of the fix

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-reviewer-fixes.md`

- [ ] **Step 1: Rewrite `node-reviewer-fixes.md` recipe** to re-apply only the original lens's checklist to the changed surface.
- [ ] **Step 2: Add explicit input package** to `## Inputs`.
- [ ] **Step 3: Update `## Outputs`** to require `reviewer-fixes: PASS` or `reviewer-fixes: FAIL` terminal line.
- [ ] **Step 4: Regenerate skills and run `ci --check`.**
- [ ] **Step 5: Commit.**

---

### Task 4: Add explicit dispatch table to `node-lens-dispatch.md`

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/node-lens-dispatch.md`

- [ ] **Step 1: Add a dispatch table** listing each lens profile, focus, and output file.
- [ ] **Step 2: Regenerate skills and run `ci --check`.**
- [ ] **Step 3: Commit.**

---

### Task 5: Write the follow-up spec

**Files:**
- Create: `.agents/specs/2026-08-08-iterative-review-handoff-improvements-design.md`

- [ ] **Step 1: Write the spec** covering scope, out-of-scope, and acceptance criteria for router merge-write, `--json`, `finding-fix` decision table, `reviewer-fixes` contract, `lens-dispatch` table, and full dogfood.
- [ ] **Step 2: Commit the spec.**

---

### Task 6: Dogfood the full fast-fix loop on a real PR

**Files:**
- Off-repo scratch directory: `Z:\_agent-scratch\main\iterative-review-dogfood-1`

- [ ] **Step 1: Find a small real PR to review** with one `blocking` or `important` finding safe to fix.
- [ ] **Step 2: Run the full `iterative-review` loop**, using `next_node.py --json` and intentionally dispatching `implementer` for one finding.
- [ ] **Step 3: Record the result** in `dogfood-report.md` with nodes visited, `implementer`/`reviewer-fixes` use, and final state.
- [ ] **Step 4: Fix any issues the dogfood reveals.**
- [ ] **Step 5: Run `ci --check` on the feature branch.**
- [ ] **Step 6: Commit any remaining skill changes.**

---

## Self-review and handoff

### Spec coverage

| Spec section | Task |
|---|---|
| Router merge-write and `--json` | Task 1 |
| `finding-fix` decision table | Task 2 |
| `reviewer-fixes` fast re-review | Task 3 |
| `lens-dispatch` dispatch table | Task 4 |
| Spec document | Task 5 |
| Full dogfood | Task 6 |

### Placeholder scan

No `TBD`, `TODO`, or vague steps. All shell snippets and file content are literal.

### Execution confidence

8/10 — the router and recipe changes are concrete, but the exact dogfood PR is not chosen yet, tracked as Task 6.1.
