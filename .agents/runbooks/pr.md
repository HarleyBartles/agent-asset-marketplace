# PR Runbook

Use this runbook for pull-request workflow and publication proof in `agent-asset-marketplace`.

## Before you begin

- Read root [`AGENTS.md`](../../AGENTS.md) `## Publication proof for repo work` and `## Draft PR policy` for the durable doctrine.
- Read [`.devin/rules/pr.md`](../../.devin/rules/pr.md) for the conditional rule trigger that loads this runbook.
- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for validation commands.
- Invoke `/repo-worker-base`.

## When to use

- Preparing a branch for review.
- Creating or updating a PR.
- Providing publication proof for repo work.

## Draft PR policy

This repo's rules:

- Open pull requests as **draft**.
- Keep a PR in draft while iterating, running local validation, and performing self-review.
- Only flip a PR out of draft when:
  - self-review is complete,
  - the preflight (`tools/run ci --check` on the staged tree) passes,
  - the branch is ready for review or merge.
- This repo's CI must not run on draft pull requests. The `marketplace-validation` workflow skips draft PRs and runs once a PR is no longer draft; it is gated by `github.event.pull_request.draft == false`.
- After flipping a PR to ready, monitor CI and address failures before requesting human review.
- The PR body must include publication proof per root `AGENTS.md`.

Consumer-canonical variant:

- Repos that adopt the `repo-standards` skill inherit the same policy from `codex-marketplace/plugins/repo-worker-pack/skills/repo-standards/templates/pr.md`: open as draft for WIP, flip to ready only after self-review and a green preflight, and gate `pull_request` workflows so CI does not run on drafts.
- Consumer repos substitute their own preflight command for `tools/run ci --check`; the lifecycle (draft while WIP, ready when preflight is green) is identical.
- Consumer repos with no draft-aware CI should still follow the draft-while-iterating convention so reviewers are not notified until the author signals readiness.
- The review (`/requesting-code-review`) and closeout (`/finishing-a-development-branch`) skills consult this policy before changing a PR's draft state.

## Repo-specific guidance

- Work in an isolated worktree on a task branch.
- Run the relevant validation before **every** commit:
  - `tools/run marketplace --apply` (regenerates derived surfaces), then `git add`.
  - `tools/run ci --check` (the preflight) on the staged tree before committing.
  - Run the preflight manually before committing; if the pre-commit hook is installed it will re-run the same checks. Do not use `git commit --no-verify` to bypass the hook.
- Commit focused changes. Do not commit generated artifacts unless the generator produced them.
- Push the branch and open a **draft** PR into `main` unless direct-main work is explicitly authorized.
- A valid repo-work return must include one of:
  1. an open PR URL with branch name and full head SHA;
  2. a verified direct-main commit SHA;
  3. a concrete publication blocker.

## Routing to skills

- `/repo-worker-base` for worktree, branch, and publication boundaries.
- `/using-github-mcp` for PR evidence and GitHub proof.
- `/verification-before-completion` before claiming the PR is green.
