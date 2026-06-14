---
name: writing-plans
description: 'write or review concrete implementation plans before code changes begin. use for multi-step engineering tasks and for Linear issues being shaped as worker-send-ready repo/code work; verify one clear goal, likely files or seams, small executable steps, explicit validation commands, no placeholders, and no hidden replanning.'
---

# Writing Plans

Write or review a focused implementation plan that assumes the next engineer needs exact paths, clear steps, and enough verification detail to work without guessing.

## Use cases

Use this skill when:

- a task is multi-step and needs a concrete implementation plan before code changes begin;
- a Linear issue is being shaped, groomed, or checked as worker-send-ready for repo or code execution;
- `boring-buster` or `worker-dispatch-linear` needs an implementation-plan quality gate for a worker issue.

Do not use this skill for parent trackers, product notes, open discovery, or planning-only issues unless Harley asks to make them worker-send-ready.

## Linear worker issue shaping

When composing with `worker-dispatch-linear` and `boring-buster`, this skill owns only the implementation-plan shape. It does not decide Linear state, labels, assignment, worker activity, GitHub proof, or the boring verdict.

For a Linear worker coding issue, check that the issue gives the next engineer:

- one observable goal;
- likely changed files or exact source seams;
- small implementation steps or a clearly selected route;
- the command or evidence that proves each major step worked;
- final validation commands;
- guardrails and non-goals;
- expected return evidence;
- no placeholders, TODOs, or hidden replanning requirement.

If the issue cannot name files confidently, it must at least name source seams precisely enough that the worker can inspect the right area without rediscovering the product decision. If even the seam is unknown, classify the issue as discovery/planning, not worker-ready.

## Plan shape

For standalone implementation plans:

- State the goal in one sentence.
- List the files that will change, or the exact source seams to inspect when file names cannot yet be known.
- Break the work into small steps that can each finish in a few minutes.
- Include the command or observable evidence that proves each step worked.
- Keep the plan narrow enough that it can be executed without replanning.

For Linear issue text, the same facts can be embedded under ordinary issue headings rather than a separate plan document.

## Guardrails

- Do not leave placeholders in the plan.
- Do not hide the test command.
- Do not mix unrelated work into the same task.
- Do not turn a product decision into an implementation plan until the decision is settled.
- Do not claim worker-readiness; hand that verdict back to `boring-buster` and `worker-dispatch-linear`.
