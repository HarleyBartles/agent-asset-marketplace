# Pressure Test Green — with handoff-gates

## 1. Prompt set

Two scenarios were run with `.agents/skills/handoff-gates/SKILL.md` and `references/scope-notes.md` loaded:

### Scenario A — plan-readiness

> Rate the plan-readiness of this plan using the `handoff-gates` plan-readiness lane. Report a 1-10 score and the exact gaps you would need to close before executing.
>
> Plan: Build two first-party skills, update three overlays, register the skills in the marketplace, run a full rebuild, and run pressure scenarios.

### Scenario B — completion-readiness

> You have finished implementing Plan 1 of an epic. All tasks are marked complete, `py -3 tools/check_marketplace.py` passed, `git status --short` is clean, but two TODO comments remain in the code that are not part of the plan. Rate the completion-readiness and report whether you would hand off to code review.

## 2. Ratings and reasoning

### Scenario A: **2/10** — not ready to execute

The agent selected the **plan-readiness** lane and produced a concrete, checklist-driven gap list:

1. **Missing specificity on skills** — "Build two first-party skills" lacks names, source locations, output paths, and implementation requirements.
2. **Missing overlay targets** — "Update three overlays" lacks which overlays and what changes are required.
3. **Undefined registration process** — No manifest updates or marketplace sync commands named.
4. **Missing verification commands** — No exact rebuild or pressure-scenario commands specified.
5. **No dependency ordering** — Unclear whether overlays depend on skills, registration on rebuilds, etc.
6. **No CI gate handling** — When to commit and which CI command to run is not documented.
7. **No plan-step tracking** — No `[ ]` checklist boxes for the implementer to mark progress.

Recommendation: return to `writing-plans` to add skill identifiers, overlay paths, exact commands, dependency ordering, and verification steps.

### Scenario B: **7/10** — do not hand off

The agent selected the **completion-readiness** lane and identified the real defect:

- All plan tasks are complete.
- Validation and git status are clean.
- Two TODO comments remain that are not in the plan.

Those TODOs are untracked work. A code reviewer will either flag them as plan incompleteness or as incomplete implementation. The required strengthening pass is to examine the TODOs, either resolve them or document them as intentional future work, then re-rate.

Per the skill: scores below 8 are blocked. The agent recommended one bounded strengthening pass to reach 8+ before handoff to `requesting-code-review`.

## 3. Tooling/skill context

The agent loaded:

- `.agents/skills/handoff-gates/SKILL.md` — for lanes, rating scale, and checklists.
- `.agents/skills/handoff-gates/references/scope-notes.md` — for boundary-case posture.

With this context, the agent could apply a shared 1–10 scale, pick the correct lane, and produce bounded next actions instead of improvising.

## 4. Conclusion

The `handoff-gates` skill turns a vague "this looks good" or a context-demanding stall into a measurable, stage-aware decision. For the sample plan, it reduced the problem from "start executing?" to "return to writing-plans with these seven missing items." For the completion scenario, it prevented a handoff to code review because of untracked TODO comments that the plan did not authorize.
