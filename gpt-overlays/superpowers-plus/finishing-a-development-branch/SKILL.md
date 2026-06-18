---
name: finishing-a-development-branch
description: Use when implementation is done and the work needs a clean closeout path.
---

# Finishing a Development Branch

Verify the change first, then decide how to land it. The usual choices are to
merge, open a pull request, keep the branch around for later, or discard it if
the work is no longer wanted.

If the work used a written plan, treat plan verification as part of the closeout
decision: reread the plan, confirm checked steps have evidence, confirm open
steps are intentionally open or blocked, and do not present PR/merge/ready-for-
review options when boxes and evidence disagree.

## Quick Pattern

1. Re-run the relevant tests or validations.
2. Confirm the branch state and the base branch.
3. If a written plan exists, reconcile checkbox state with evidence before
   presenting closeout options.
4. Choose merge, PR, keep, or discard.
5. Preserve the workspace if the work should stay available for follow-up.

## Guardrails

- Do not treat a branch as done until verification has been rerun.
- Keep the closeout decision aligned with the repository's publication rules.
- Do not delete work before the user has chosen that outcome.

