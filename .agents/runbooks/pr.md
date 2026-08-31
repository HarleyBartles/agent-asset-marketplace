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
  - the latest committed tree has passed the pre-commit hook on the staged snapshot,
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
   - If the pre-commit hook is not available, run `py -3 tools/run.py ci --check` only as an explicit CI-parity or diagnostic step.
   - If either is red, fix the findings and re-run. Do not proceed past preflight while it is red.

2. **Scope honesty.**
   - Compare the branch diff to the PR description, the linked spec, and any linked plan.
   - If the implemented scope differs, update the spec/plan or PR body to match before reviewers see the diff.

3. **Self-review and optional legacy assistance.**
   - Perform an ordinary whole-change self-review once preflight is green.
   - A harness-designated frontier orchestrator, including `gpt-5.6-sol`, must not invoke `/iterative-review`.
   - A non-frontier or unknown-capability orchestrator may offer `/iterative-review` as legacy review assistance, but must explain its limitations and obtain explicit human approval for this PR before invoking it.
   - A legacy graph `ready` result proves only sequence completion. It does not authorize a green claim or a draft-to-ready transition; use the ordinary self-review, scope-honesty, and canonical-validation gates.

## Repo-specific guidance

- Work in an isolated worktree on a task branch.
- Do not run `py -3 tools/run.py ci --check` immediately before a normal commit or immediately after a successful hooked commit. It is a complete CI/PR gate, not a pre-pre-commit step. The pre-commit hook already materializes the staged snapshot, runs `ci --apply`, stages only the owned generated surfaces, and runs `ci --check --diagnostics`; running `ci --check` manually first is wasteful.
- If you are confident the working change is correct, stage the intended tree and commit it. The pre-commit hook will keep you honest: it applies mechanical fixes to the staged snapshot, reports every failing check, and fails the commit if any check is broken.
- If the pre-commit hook is not installed, run `py -3 tools/run.py ci --apply` manually before committing. Then commit normally; the hook (or `ci --check --diagnostics` if the hook is absent) proves the staged tree. Do not run `ci --check` separately unless no commit follows.
- Only run `py -3 tools/run.py ci --check` deliberately for uncommitted verification, pipeline diagnosis, or explicit CI-parity work.
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
- `/iterative-review` only for human-approved legacy assistance on a non-frontier or unknown-capability orchestrator; never for a harness-designated frontier orchestrator.
- `/using-github-mcp` for PR evidence and GitHub proof.
- `/verification-before-completion` before claiming the PR is green.
