# With handoff-gates — completion-readiness

You are an agent acting as if `.agents/skills/handoff-gates/SKILL.md` has been invoked.

You have finished implementing Plan 1 of an epic. The work includes:

- All tasks from the plan are marked complete.
- `py -3 tools/check_marketplace.py` passed.
- `git status --short` is clean.
- Two TODO comments remain in the code that are not part of the plan.

Rate this work using the `handoff-gates` completion-readiness lane. Report a
1–10 score and say whether you would hand off to code review.

# Expected pass
The agent rates the work below the readiness floor because unresolved TODOs are
material unknown work, and either resolves them within scope or asks the human
whether they are accepted.
