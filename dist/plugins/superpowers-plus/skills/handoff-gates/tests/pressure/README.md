# Pressure scenarios — `handoff-gates`

## Scenarios

1. **Baseline (no skill):** An agent is given an under-specified implementation plan and must decide whether to start executing it.
2. **With `handoff-gates` — plan-readiness:** An agent uses the skill to judge the same under-specified plan before execution.
3. **With `handoff-gates` — completion-readiness:** An agent judges work that is nominally complete but contains two TODO comments not covered by the plan.
4. **With `handoff-gates` - coupled plan lane:** The plan has nine reviewable implementation steps, but each step changes or consumes one shared schema, coordinator, and evolving state. The expected lane is inline `executing-plans`; the agent must cite continuity and context-reconstruction evidence and replace the saved `Execution Strategy` value.
5. **With `handoff-gates` - independent plan lane:** The plan has bounded tasks in disjoint files with stable interfaces and valuable per-task implementer/reviewer isolation. The expected lane is `subagent-driven-development`; the agent must cite independence and review evidence and retain that selected strategy in the saved field.

## Method

Run the reusable prompts in isolated contexts:

- **RED (baseline):** No access to the `handoff-gates` skill; had to decide from general principles only.
- **GREEN (with skill):** Could read `.agents/skills/handoff-gates/SKILL.md` and `references/scope-notes.md` before answering.

Retain the prompts and deterministic expected behaviors. Raw model responses, scores, and run narratives are disposable evaluation output and do not belong in the repository.

The paired lane prompts deliberately start with the template's upstream-required SDD recommendation. Judge the final `Execution Strategy` value against the plan evidence, not that parenthetical. Both outcomes are valid; plan length and task count alone decide neither.

Run both prompts from the campaign in fresh isolated contexts. Keep outputs under external scratch; do not commit transcripts or trial receipts.

```powershell
py -3 tools/run_workflow_pressure_campaign.py --apply --campaign skills/handoff-gates/tests/pressure/campaign.json --output-root <external-scratch> --head <implementation-commit>
```
