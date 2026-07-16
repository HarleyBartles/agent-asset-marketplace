---
name: executing-plans
description: Use when an implementation plan already exists and the work should be carried out step by step.
---

# Executing Plans

Load the plan, review it critically, then execute the tasks in order. Verify
each task the way the plan asks, and stop as soon as you hit a blocker or a
missing requirement.

Plans in the verified-plan adapter path should be treated as live execution
artifacts. Check off each step only after the named evidence is collected, and
leave blocked or intentionally deferred steps open with a short note.

## Quick Pattern

1. Read the plan and confirm it still matches the request.
2. Work one task at a time.
3. Run the verification named in the task.
4. Fix issues before moving on.
5. When all tasks are complete, verify the branch or change set end to end.

## Guardrails

- Do not skip the review step just because the plan looks obvious.
- Keep task scope small enough that each result is independently testable.
- Use helper processes or parallel work only when the environment supports it
  and the tasks are truly independent.
