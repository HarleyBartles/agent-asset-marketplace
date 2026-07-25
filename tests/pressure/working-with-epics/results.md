# Pressure scenario results

## Summary

All five subagent pressure scenarios completed. The RED baselines show behavior without the new skills; the GREEN tests show behavior with `working-with-epics` and `handoff-gates` installed and read as if invoked.

## working-with-epics

### RED: oversized request (no skill)

The subagent produced a single end-to-end plan for the full e-commerce site covering user accounts, product catalog, shopping cart, checkout, admin dashboard, technical architecture, and deployment — all in one plan. It did not create a roadmap or sequence of plans.

**Verdict:** Expected failure — single giant plan.

### GREEN: oversized request (with skill)

The subagent detected the epic scope, created `Z:\_agent-worktrees\agent-asset-marketplace\working-with-epics\.agents\superpowers\roadmaps\2026-07-25-ecommerce-site.md` with a plan sequence table, and wrote Plan 1 (`2026-07-25-ecommerce-user-accounts.md`) scoped only to user accounts and application foundation. It left the remaining subsystems (catalog, cart, checkout, admin, deployment) as `pending` future plans.

**Verdict:** Expected pass — roadmap + first plan, not a single giant plan.

## handoff-gates

### RED: plan-readiness (no skill)

The subagent rated the vague plan 2/10 and decided not to execute. It did not use the `handoff-gates` lane name or the 8/10 floor / 9/10 target language, and it used a 7/10 threshold.

**Verdict:** Expected failure — rating without `handoff-gates` lane discipline.

### GREEN: plan-readiness (with skill)

The subagent used the `handoff-gates` plan-readiness lane, scored the plan 3/10, stated it would not execute below 8/10 (target ≥ 9/10), and listed specific gaps (skill identity, standards, overlays, marketplace registration, rebuild command, pressure scenarios, acceptance criteria, dependencies, validation notes).

**Verdict:** Expected pass — lane-named rating with explicit gaps and threshold.

## Combined GREEN: blocked plan (working-with-epics + handoff-gates)

The subagent read both skills, identified the 6/10 rating and the unresolved API contract, marked the roadmap item as `blocked`, and asked the human one focused question about the API contract schema, authentication, and error format. It did not proceed to execution.

**Verdict:** Expected pass — ask focused question and stop below 8/10.
