# Evidence-Based Execution Lane Recommendations Implementation Plan

**State:** implementation in progress; paired pressure scenarios are authored, but execution is blocked by the local runner's connector preflight.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make plan-readiness handoff compare execution lanes from the saved plan, then make the selected lane authoritative in the plan's `Execution Strategy` field.

**Architecture:** Keep the upstream-required subskill header intact. Strengthen the first-party `handoff-gates` plan-readiness checklist to compare the current recommendation with its nearest credible alternative using plan-specific evidence, then revise the saved `Execution Strategy` field before handoff. Clarify `writing-plans` so its self-review and execution handoff use that gate result rather than treating the template's SDD recommendation as evidence.

**Tech Stack:** Markdown skill sources, pytest workflow-contract tests, handoff-gates pressure prompts, marketplace projections, repository mesh.

**Spec:** Linear issue [MARK-374](https://linear.app/harleys-workspace/issue/MARK-374/require-evidence-based-execution-lane-recommendations-at-plan-handoff).

**Execution Strategy:** `executing-plans`, because the plan gate, planner handoff, generated projections, and paired outcome fixtures form one sequentially coupled contract. Inline execution preserves a single decision model while tests and fixtures evolve; separate task implementers would reconstruct the same rationale without buying useful isolation.

## Global Constraints

- Keep the upstream-required `subagent-driven-development (recommended)` subskill header unchanged.
- Do not make SDD or inline execution a universal default.
- Do not select a lane from plan length or task count alone.
- Base the comparison on task independence, dependency order, shared context, state coupling, review burden, context reconstruction, and consequence.
- Keep comparative reasoning and readiness ratings in the current handoff, not as private diagnostics persisted in the plan.
- Edit canonical Superpowers Plus sources; regenerate installed projections through owning commands.

## Review Focus

- A long plan with many reviewable steps but shared state and sequential dependencies selects inline execution when continuity outweighs per-task isolation.
- A plan with genuinely independent tasks and valuable fresh implementer/reviewer context can still select SDD.
- The final saved `Execution Strategy` field and the handoff recommendation agree, while the upstream subskill header remains intact.

______________________________________________________________________

### Task 1: Add and cover plan-specific lane selection

**Files:**

- Modify: `tests/pressure/handoff-gates/README.md`
- Create: `tests/pressure/handoff-gates/campaign.json`
- Create: `tests/pressure/handoff-gates/prompts/coupled-plan-lane.md`
- Create: `tests/pressure/handoff-gates/prompts/independent-plan-lane.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md` only where needed to make the gate result authoritative.
- Regenerate: `.agents/skills/superpowers-plus/` through owning commands.
- Regenerate: pressure prompt indexes through the owning mesh command.

**Interfaces:**

- Consumes: current plan-readiness and writing-plans handoff contract.

- Produces: paired pressure scenarios with opposite justified lane outcomes and a saved plan strategy controlled by plan-readiness evidence.

- [x] Add the coupled-plan pressure prompt: nine individually reviewable steps share one schema, coordinator, and cross-step state; expect inline execution with concrete continuity evidence.

- [x] Add the independent-plan pressure prompt: bounded tasks have disjoint files/interfaces and benefit materially from fresh implementer and reviewer context; expect SDD with concrete isolation evidence.

- [x] Document the paired scenarios and deterministic expected outcomes in the existing handoff-gates pressure README.

- [x] Add both pressure prompts to a scoped campaign using the repository's existing pressure runner schema.

- [x] Add a plan-readiness check after reviewing task order that compares the proposed lane with its nearest credible alternative using task independence, dependencies, shared implementation context, state coupling, review burden, context reconstruction, and consequence.

- [x] Require concrete evidence from the saved plan and a clear statement of why the selected lane wins; plan length and task count alone are insufficient.

- [x] Require the planner to update the saved `Execution Strategy` field after the comparison and before handoff. Leave the upstream-required subskill header untouched.

- [x] Clarify the writing-plans self-review and handoff wording so the completed gate result, not the template's parenthetical recommendation, determines the lane and the saved field.

- [x] Generate the installed skill projections and confirm the canonical sources and projections agree.

- [x] Review both handoff-gates pressure fixtures against their expected outcomes and the updated gate criteria.

### Task 2: Verify and publish

**Files:**

- Regenerate: repository mesh/index surfaces only when the owning commands report them stale.
- Update: this plan's checkboxes and state as work completes.

**Interfaces:**

- Consumes: canonical skill changes, tests, and pressure evidence from Task 1.

- Produces: validated source/projections and a reviewable Draft PR for MARK-374.

- [x] Review the complete diff against MARK-374 guardrails, including unchanged upstream header and opposing lane outcomes. Self-review confirmed the canonical/projection diff is scoped to the recommendation contract and preserves both lane outcomes.

- [x] Run `py -3 -m pytest tests/test_workflow_contracts.py -q` and all relevant marketplace, installed-skills, and mesh checks; the tracked pre-commit hook also passed the complete staged gate (1097 passed, 6 skipped).

- [ ] Run both scenarios in `tests/pressure/handoff-gates/campaign.json` against the committed implementation head and assess their responses. The runner exited before any trial because preflight found an exposed MCP/plugin inventory; connector-safety forbids bypassing that guard.

- [ ] Commit normally through the tracked hook, push the branch, open a Draft PR, and verify its published head and checks.
