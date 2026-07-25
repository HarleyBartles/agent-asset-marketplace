# Pressure scenario results

## Summary

All seven subagent pressure scenarios completed. The RED baselines show behavior without the new skills; the GREEN tests show behavior with `working-with-epics` and `handoff-gates` installed and read as if invoked.

## working-with-epics

### RED: oversized request (no skill)

The subagent produced a single end-to-end plan for the full e-commerce site covering user accounts, product catalog, shopping cart, checkout, admin dashboard, technical architecture, and deployment — all in one plan. It did not create a roadmap or sequence of plans.

**Verdict:** Expected failure — single giant plan.

### GREEN: oversized request (with skill)

The subagent detected the epic scope, ran `handoff-gates` spec-readiness (rated 6/10, then strengthened by pinning missing tech-stack assumptions and raised to 9/10), created a roadmap at `.agents/superpowers/roadmaps/2026-07-25-ecommerce-site.md` with a plan sequence table, used `writing-plans` to write Plan 1 scoped to project scaffold, DB schema, and authentication, then ran `handoff-gates` plan-readiness and rated it 9/10. It left the remaining subsystems (catalog, cart, checkout, admin, deployment) as `pending` future plans.

**Verdict:** Expected pass — roadmap + first plan + explicit handoff-gates ratings, not a single giant plan.

### GREEN: scope change mid-epic (with skill)

The subagent read both skills, stated it would update the roadmap inline to remove the admin-dashboard plan and insert a lightweight wishlist plan before the catalog plan, renumber the remaining pending plans, and document the rationale in `Handoff Notes`. It did not proceed to rewrite plans before updating the roadmap, and it asked one focused handoff question about whether to finish Plan 1 first or switch immediately.

**Verdict:** Expected pass — roadmap updated before replanning, focused question asked.

## handoff-gates

### RED: plan-readiness (no skill)

The subagent rated the vague plan 2/10 and decided not to execute. It did not use the `handoff-gates` lane name or the 8/10 floor / 9/10 target language, and it used a 7/10 threshold.

**Verdict:** Expected failure — rating without `handoff-gates` lane discipline.

### GREEN: plan-readiness (with skill)

The subagent used the `handoff-gates` plan-readiness lane, scored the plan 3/10, stated it would not execute below 8/10 (target ≥ 9/10), and listed specific gaps (skill identity, standards, overlays, marketplace registration, rebuild command, pressure scenarios, acceptance criteria, dependencies, validation notes).

**Verdict:** Expected pass — lane-named rating with explicit gaps and threshold.

### GREEN: completion-readiness (with skill)

The subagent used the `handoff-gates` completion-readiness lane, scored the completed Plan 1 7/10, and refused to hand off to code review. It identified the two TODO comments (not part of the plan) as deferred-work hygiene items and stated they must be triaged or tracked before re-rating to 9/10.

**Verdict:** Expected pass — below-9/10 rating with a clear hygiene gap and no premature handoff.

## Combined GREEN: blocked plan (working-with-epics + handoff-gates)

The subagent read both skills, identified the 6/10 rating and the unresolved API contract, marked the roadmap item as `blocked`, and asked the human one focused question about the API contract schema, authentication, and error format. It did not proceed to execution.

**Verdict:** Expected pass — ask focused question and stop below 8/10.
