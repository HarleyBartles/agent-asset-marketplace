# Pressure scenarios — `handoff-gates`

## Scenarios

1. **Baseline (no skill):** An agent is given an under-specified implementation plan and must decide whether to start executing it.
2. **With `handoff-gates` — plan-readiness:** An agent uses the skill to judge the same under-specified plan before execution.
3. **With `handoff-gates` — completion-readiness:** An agent judges work that is nominally complete but contains two TODO comments not covered by the plan.

## Method

Run the reusable prompts in isolated contexts:

- **RED (baseline):** No access to the `handoff-gates` skill; had to decide from general principles only.
- **GREEN (with skill):** Could read `.agents/skills/handoff-gates/SKILL.md` and `references/scope-notes.md` before answering.

Retain the prompts and deterministic expected behaviors. Raw model responses,
scores, and run narratives are disposable evaluation output and do not belong
in the repository.
