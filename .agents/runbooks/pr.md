# PR Runbook

Use this runbook for pull-request workflow and publication proof in `agent-asset-marketplace`.

## Before you begin

- Read root [`AGENTS.md`](../../AGENTS.md) `## Publication proof for repo work` and `## Draft PR policy` for the durable doctrine.
- Read [`.devin/rules/pr.md`](../../.devin/rules/pr.md) for the conditional rule trigger that loads this runbook.
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

## Pre-flip procedure

1. **Fast preflight first.**
   - `py -3 tools/run.py review-preflight --check`
   - `py -3 tools/run.py ci --check`
   - If either is red, fix the findings and re-run. Do not proceed past preflight while it is red.

2. **Scope honesty.**
   - Compare the branch diff to the PR description, the linked spec, and any linked plan.
   - If the implemented scope differs, update the spec/plan or PR body to match before reviewers see the diff.

3. **Iterative review.**
   - Once preflight is green, invoke `/iterative-review` and follow the graph in `references/review-state-graph.md` one node at a time.
   - Do not flip the PR to ready until the `iterative-review` graph reaches `ready` and remote CI passes.

## Repo-specific guidance

- Work in an isolated worktree on a task branch.
- Do not run `py -3 tools/run.py ci --check` before every commit. It is an explicit CI-should-pass check on the working tree, not a pre-pre-commit step. The pre-commit hook already applies mechanical fixes and then runs `ci --check` on the staged tree; running it manually first is wasteful.
- If you are confident the working change is correct, commit it. The pre-commit hook will keep you honest: it applies what it can, stages the result, and fails the commit if a non-mechanical check is broken.
- If the pre-commit hook is not installed, run `py -3 tools/run.py ci --apply` and then `py -3 tools/run.py ci --check` manually before committing.
- Only run `py -3 tools/run.py ci --check` deliberately when you want to know whether the working tree would pass CI (for example, before pushing or flipping the PR to ready).
- `py -3 tools/run.py marketplace --apply` regenerates derived surfaces; stage any generated changes before committing.
- Do not use `git commit --no-verify` to bypass the pre-commit hook.
- Commit focused changes. Do not commit generated artifacts unless the generator produced them.
- Push the branch and open a **draft** PR into `main` unless direct-main work is explicitly authorized.
- A valid repo-work return must include one of:
  1. an open PR URL with branch name and full head SHA;
  2. a verified direct-main commit SHA;
  3. a concrete publication blocker.

## Routing to skills

- `/repo-worker-base` for worktree, branch, and publication boundaries.
- `/iterative-review` for the review process.
- `/using-github-mcp` for PR evidence and GitHub proof.
- `/verification-before-completion` before claiming the PR is green.
