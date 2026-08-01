---
description: "Plan workflow guidance"
trigger: glob
globs: ".agents/plans/**"
---

## Scope

`.agents/plans/`

Defer to the repository root `AGENTS.md` for global repo and publication rules.

- Agents must check off completed plan steps before publishing a completed plan.
- Use `[x]` in place of `[ ]` for completed steps.
- Every task should include a final sub-step instructing the implementer to mark the task's own plan steps `[x]` before reporting back. If a task omits it, the implementer must still do so and the orchestrator must verify it.
- Order implementation tasks so that all source and adapter/overlay edits are complete before any `tools/run * --apply` regeneration step. Run `tools/run heal --check` after overlay edits and before regeneration to catch line-number drift early.
- Do not run `tools/run ci --check` on an uncommitted working tree. Regenerate surfaces, stage all changes, run `tools/run ci --check` on the staged tree before committing, then commit and let the pre-commit hook re-run the CI preflight. Only use `git commit --no-verify` if the hook is unavailable, with a documented reason.
- If a plan is intentionally incomplete or left open, say why inside the plan itself.
- This is local worker guidance, not a future PR-blocker doctrine.
- Do not invent receipt requirements.

## Maintenance responsibility

This file must stay aligned with the repo's plan documentation practices. When plan formats change or new guidance is needed for plan structure, review and update this file to reflect current expectations. Completed implementation plans must be checked off and committed with their implementation PR so reviewers can compare planned vs. delivered work. Plans remain repo resident as historical records and are not removed or archived; they must not be left open or uncommitted as stale in-progress guidance.
