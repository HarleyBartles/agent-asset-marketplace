---
name: handoff-gates
description: Use when a stage-boundary artifact (spec, plan, or completed work) needs a readiness check before handoff.
metadata:
  source-id: handoff-gates
  source-path: sources/first_party/skills/handoff-gates/SKILL.md
  provenance-name: Handoff Gates first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Readiness gates for brainstorming, planning, execution, and code-review handoffs.
  use_when:
  - Use when a spec is ready to move from brainstorming to planning.
  - Use when a plan is ready to move from writing-plans to execution.
  - Use when completed work is ready to move from executing-plans to code review.
  do_not_use_when:
  - Do not use when the artifact is not clearly at a stage boundary. (see references/scope-notes.md for boundary cases)
  - Do not use as a substitute for risk-gates when the question is pre-action risk.
  related_skills:
  - risk-gates
  - writing-plans
  - executing-plans
  - subagent-driven-development
  - working-with-epics
  use_after:
  - brainstorming
  - writing-plans
  - executing-plans
  use_before:
  - writing-plans
  - executing-plans
  - subagent-driven-development
  - finishing-a-development-branch
  - requesting-code-review
license: MIT
---

# Handoff Gates

## Overview

Rate stage-boundary artifacts for execution confidence. Never hand off below 8/10. Target 9/10+.

## Lanes

- **spec-readiness** (brainstorming → planning): Can a planning agent expand this spec into a full plan without improvising or discovering seams mid-flight?
- **plan-readiness** (planning → execution): Can the implementing agent or orchestrator plus subagents execute this plan without improvising mid-flight?
- **completion-readiness** (execution → code review): What will a code reviewer find when they review this work against the plan and the repo's code review guide?

## Rating Scale

1–10 execution-confidence scale.

- **< 8:** Identify gaps, strengthen, re-rate. Never proceed below 8.
- **8–8.9:** Try one bounded strengthening pass to reach 9+.
- **≥ 9:** Proceed to handoff. Report the final rating in the handoff and record it in the roadmap.

For completion-readiness, 9/10 means high confidence the work passes code review with no findings or only minor nits.

## How to Use

1. Read the artifact produced by the previous stage.
2. Pick the lane matching the boundary.
3. Score the artifact against the lane question.
4. Strengthen gaps until the score is ≥ 8 (target ≥ 9).
5. Report the final rating and hand off to the next stage.

## Plan-Readiness Checklist

When the `plan-readiness` lane is for a `subagent-driven-development` (SDD) plan, rate the artifact against these items. A plan that fails any item should be strengthened before handoff.

- [ ] **Dependency-order coherence.** For each task, the `Consumes` block names only outputs from tasks that appear earlier in the plan. No task may consume an output from a task scheduled later. If a later task's output is needed earlier, either move the producer earlier, split an intermediate step, or add an explicit bridge/proxy.

- [ ] **Task ordering.** The general rule is that producers come before consumers. In this repo, that means all source and adapter/overlay edits are scheduled before any `tools/run * --apply` regeneration step.

- [ ] **Overlay health gate.** `tools/run heal --check` is scheduled after overlay edits and before `marketplace`/`project`/`installed-skills` regeneration.

- [ ] **Plan-step tracking.** Each task includes a final sub-step for the implementer to mark the task's own checklist boxes `[x]` in the plan file.

- [ ] **Clean CI gate.** `tools/run ci --check` is not scheduled on an uncommitted working tree; the plan commits and lets the pre-commit hook run it, or commits with `--no-verify` and then runs it.

- [ ] **Explicit verification.** Each regeneration or projection task names the exact `tools/run <target> --apply` command and any follow-up `ci --check`.

- [ ] **No temporary validation drift.** If a task is expected to leave the tree in a temporarily unbuildable state, it is explicitly documented so the implementer and reviewer know it is expected.

## Boundary cases

If the artifact is intentionally thin, depends on an external blocker, or the handoff touches `verification-before-completion` or `requesting-code-review`, load `references/scope-notes.md` and follow its guidance. Only proceed when the reference gives a green path.

## Common Mistakes

- Rushing to hand off at 7/10 because the plan is "good enough." → Scores below 8 are blocked.
- Chasing a 10 forever. → One bounded strengthening pass from 8–8.9 is enough.
