---
name: finishing-a-development-branch
description: Use when implementation is done and the work needs a clean closeout path.
---

# Finishing a Development Branch

Verify the change first, then decide how to land it. The usual choices are to
merge, open a pull request, keep the branch around for later, or discard it if
the work is no longer wanted.

## Quick Pattern

1. Re-run the relevant tests or validations.
2. Confirm the branch state and the base branch.
3. Choose merge, PR, keep, or discard.
4. Preserve the workspace if the work should stay available for follow-up.

## Guardrails

- Do not treat a branch as done until verification has been rerun.
- Keep the closeout decision aligned with the repository's publication rules.
- Do not delete work before the user has chosen that outcome.

