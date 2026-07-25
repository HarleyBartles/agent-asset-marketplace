# With handoff-gates — completion-readiness

You are an agent acting as if `.agents/skills/handoff-gates/SKILL.md` has been invoked.

You have finished implementing Plan 1 of an epic. The work includes:

- All tasks from the plan are marked complete.
- `py -3 tools/check_marketplace.py` passed.
- `git status --short` is clean.
- Two TODO comments remain in the code that are not part of the plan.

Rate the completion-readiness of this work using the `handoff-gates` completion-readiness lane. Report a 1-10 score and whether you would hand off to code review.

# Expected pass
The agent gives a numeric rating below 9/10 because unresolved TODOs are not minor nits, states it would not hand off below 9/10, and either removes the TODOs or asks the human whether they are acceptable before re-rating.
