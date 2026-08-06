# Pressure-test proof — `handoff-gates`

## Scenarios

1. **Baseline (no skill):** An agent is given an under-specified implementation plan and must decide whether to start executing it.
2. **With `handoff-gates` — plan-readiness:** An agent uses the skill to rate the same under-specified plan before execution.
3. **With `handoff-gates` — completion-readiness:** An agent uses the skill to rate work that is nominally complete but contains two TODO comments not covered by the plan.

## Method

Two isolated agents were given the same prompts:

- **RED (baseline):** No access to the `handoff-gates` skill; had to decide from general principles only.
- **GREEN (with skill):** Could read `.agents/skills/handoff-gates/SKILL.md` and `references/scope-notes.md` before answering.

Both agents wrote their own reports:

- [red.md](red.md)
- [green.md](green.md)

## Results

### Plan-readiness scenario

- **RED path:** The agent did not produce a numeric rating and refused to start executing, listing the missing context it needed before it could proceed. It was safe, but it did not advance the artifact or identify the specific gaps in a handoff-ready way.
- **GREEN path:** The agent produced a **2/10** plan-readiness rating and a bounded, checklist-driven list of seven gaps to close before execution. It explicitly recommended returning to `writing-plans` rather than improvising.

### Completion-readiness scenario

- **GREEN path:** The agent produced a **7/10** completion-readiness rating and refused to hand off to code review because two TODO comments remained that were not part of the plan. It recommended one bounded strengthening pass to resolve or document the TODOs and re-rate.

## Conclusion

The `handoff-gates` skill turns stage-boundary decisions from subjective "looks good" or context-seeking stalls into a shared 1–10 scale with explicit strengthening steps. In these scenarios it prevented an under-specified plan from entering execution and prevented work with untracked TODOs from entering code review.
