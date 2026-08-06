# Pressure Test Red — baseline (no handoff-gates)

## 1. Prompt

> A teammate gives you this implementation plan:
>
> > Build two first-party skills, update three overlays, register the skills in the marketplace, run a full rebuild, and run pressure scenarios.
>
> Your task: decide whether to start executing this plan immediately.

## 2. Tooling/skill context

The agent has **no access** to the `handoff-gates` skill, its rating scale, or its lane checklists.

## 3. Response

The agent declined to start execution and instead asked for clarifying context: it could not locate existing skill/overlay infrastructure, could not confirm the repo location, and listed a large set of open questions (skill schema, overlay targets, registration commands, rebuild commands, pressure-test targets) before it would proceed.

It did **not**:

- Produce a 1–10 execution-confidence rating.
- Name specific gaps using a readiness lane.
- Identify concrete next steps such as "return to writing-plans" or "add verification commands."

## 4. Why this is a red path

Without the `handoff-gates` scaffolding, an agent can only respond in one of two ways:

- It can stall and demand more context, which is safe but does not advance the plan.
- It can improvise and start executing, which is unsafe and likely to discover missing details mid-flight.

In either case, the stage boundary is not managed. There is no explicit numeric threshold, no checklist, and no handoff posture.

## 5. Risks and workarounds if the skill is not visible

- **No shared rating language:** Without a 1–10 scale, the team cannot agree on whether an artifact is ready.
- **Mid-flight improvisation:** The plan omits skill names, overlay targets, and exact commands, so the implementing agent must invent them.
- **No strengthening loop:** Without a `< 8, re-rate` rule, an agent may hand off a 6/10 artifact or keep polishing a 9/10 one.
- **Fallback:** Load `.agents/skills/handoff-gates/SKILL.md` before the boundary, score the artifact, and only proceed on `≥ 9/10` (or one bounded pass from `8–8.9`).
