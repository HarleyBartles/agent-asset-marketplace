# AGENTS.md

Scope: `.agents/superpowers/plans/`

Defer to the repository root [AGENTS.md](../../../AGENTS.md) for global repo and
publication rules.

- Agents must check off completed plan steps before publishing a completed
  plan.
- Use `[x]` in place of `[ ]` for completed steps.
- If a plan is intentionally incomplete or left open, say why inside the plan
  itself.
- This is local worker guidance, not a future PR-blocker doctrine.
- Do not invent receipt requirements.

## Example

```markdown
## Plan

- [x] Step 1: Read the source issue and repo context.
- [x] Step 2: Make the scoped change.
- [x] Step 3: Run validation.
- [x] Step 4: Publish the PR with return evidence.
```

## Maintenance responsibility

This file must stay aligned with the repo's plan documentation practices. When
plan formats change or new guidance is needed for plan structure, review and
update this file to reflect current expectations. Completed implementation plans
must be checked off and committed with their implementation PR (see
`.agents/guides/implementing-guide.md`) so reviewers can compare planned vs.
delivered work. Once the plan is merged and no longer the active source of
truth, it may be archived; it must not be left open or uncommitted as stale
in-progress guidance.
