---
name: writing-plans
description: Use when a task is multi-step and needs a concrete implementation plan before code changes begin.
---

# Writing Plans

Write a focused plan that assumes the next engineer needs exact paths, clear
steps, and enough verification detail to work without guessing.

In the verified-plan adapter path, plans should be checkable execution
artifacts: each step needs named evidence, and intentionally open steps should
stay open with a short reason.

## Linear worker issue shaping

When composing with `linear-issue-shaping` and `boring-buster`, this skill
owns only the implementation-plan shape. It does not decide Linear state,
labels, assignment, worker activity, GitHub proof, or the boring verdict.

For a Linear worker coding issue, check that the issue gives the next engineer:

- one observable goal;
- likely changed files or exact source seams;
- small implementation steps or a clearly selected route;
- the command or evidence that proves each major step worked;
- final validation commands;
- guardrails and non-goals;
- expected return evidence;
- no placeholders, TODOs, or hidden replanning requirement.

If the issue cannot name files confidently, it must at least name source seams
precisely enough that the worker can inspect the right area without
rediscovering the product decision. If even the seam is unknown, classify the
issue as discovery/planning, not worker-ready.

## Plan Shape

- State the goal in one sentence.
- List the files that will change, or the exact source seams to inspect when
  file names cannot yet be known.
- Break the work into small steps that can each finish in a few minutes.
- Include the command or observable evidence that proves each step worked.
- Make each step checkable by naming the validation command, file/path readback,
  or evidence condition that proves the step completed.
- Keep the plan narrow enough that it can be executed without replanning.

## Guardrails

- Do not leave placeholders in the plan.
- Do not hide the test command.
- Do not mix unrelated work into the same task.
- Do not turn a product decision into an implementation plan until the decision
  is settled.
- Do not claim worker-readiness; hand that verdict back to `boring-buster` and
  `linear-issue-shaping`.
