---
name: using-superpowers
description: Use when starting work and deciding which workflow skill should guide the next step.
---

# Using Superpowers

This is the entry point for the workflow. Look at the task, decide whether you
need brainstorming, planning, implementation, debugging, verification, review,
or closeout help, then open the relevant skill before you act.

This overlay is the Asset Marketplace `Superpowers+` adaptation layer, not
upstream/base Superpowers doctrine. It routes to the core Superpowers workflow
skills plus `inspecting-the-environment`.
If the task has or needs a written plan, route it through the verified-plan
adapter path: `writing-plans` -> `executing-plans` ->
`verification-before-completion`.

## Adapted Routing

- Brainstorming and task framing: use `brainstorming`.
- Plan creation and plan execution: use `writing-plans` for route review and
  `executing-plans` for implementation.
- Verified-plan adapter path: use `writing-plans` to make the plan checkable,
  `executing-plans` to update verified checkboxes as work lands, and
  `verification-before-completion` before any completion or ready-for-review
  claim.
- Test-disciplined implementation: use `test-driven-development`.
- Debugging and unexpected behavior analysis: use `systematic-debugging`.
- Verification and completion claims: use `verification-before-completion`.
- Review and redline workflows: use `requesting-code-review` and
  `receiving-code-review`.
- Branch completion and publication closeout: use
  `finishing-a-development-branch`.
- Environment inspection before action when constraints matter: use
  `inspecting-the-environment`.
- Parallel agent dispatch or worktree setup when those are the smallest useful
  helpers: use `subagent-driven-development`, `dispatching-parallel-agents`, or
  `using-git-worktrees`.
- Writing or updating skill content: use `writing-skills`.

## Quick Pattern

1. Read the current request and surrounding context.
2. Choose the smallest skill that fits the moment.
3. If the task is unclear, start with brainstorming.
4. If a plan already exists, move to planning or execution.
5. If the work is nearly done, switch to verification or closeout.

## Guardrails

- Do not skip the skill selection step.
- Do not force one workflow onto every task.
- Keep the chosen workflow aligned with the actual stage of work.
