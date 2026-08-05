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

## Pre-flip robustness procedure

Run the fastest, cheapest checks first so that `iterative-review` and Devin auto-review only see issues that require judgment, not pattern classes the repo can catch deterministically. This runbook follows the `iterative-review` graph in `.agents/skills/iterative-review/references/review-state-graph.md`.

1. **Fast preflight first (`preflight` node).**
   - `py -3 tools/run.py review-preflight --check`
   - `py -3 tools/run.py ci --check`
   - If either is red, fix the findings and re-run. Do not proceed past `preflight` while it is red.

2. **Scope honesty (`scope-honesty` node).**
   - Compare the branch diff to the PR description, the linked spec, and any linked plan.
   - If the implemented scope differs, update the spec/plan or PR body to match before reviewers see the diff.

3. **Orchestrator pre-emptive review (`orchestrator-self-review` node).**
   - Do not dispatch reviewers to catch what you can see yourself. Before `lens-dispatch`, the orchestrating agent reads the branch diff and the relevant `.agents/agents/reviewer-*.md` `## Checklist`. The profile is the checklist for both the orchestrator and the subagent reviewer.
   - For each lens, ask: *What would this lens flag that I can fix with high confidence?* Apply those fixes now.
   - Record the predicted and pre-emptively fixed classes in `review-log-orchestrator-self-review.md` in the off-repo scratch.
   - A clean `orchestrator-self-review` is not a pass. You must still run `lens-dispatch` and `strong-review`.

4. **Iterative review graph (`lens-dispatch` and `strong-review` nodes).**
   - Only after preflight is green and pre-emptive fixes are committed, run the review graph. This is mandatory:
     - `reviewer-plans` for `.agents/plans`, `.agents/specs`, and roadmap honesty.
     - `reviewer-mesh` for mesh/INDEX/scaffold/generated-surface integrity.
     - `reviewer-skills` for `SKILL.md`, reference files, and prompt robustness.
     - `reviewer-marketplace` for `codex-marketplace` pack generation and marketplace tooling.
     - `reviewer-scripts` for `tools/` and script/CLI changes.
     - `reviewer-security` for secrets and real identifiers.
     - `reviewer-strong` for whole-branch design, scope, and gaps in the lens logs.
   - If you cannot dispatch subagents, the review is `blocked`. Do not claim the PR is ready because `orchestrator-self-review` was clean.
   - For each finding, use `receiving-code-review` before applying.

5. **Fix and re-preflight (`re-preflight` node).**
   - After each fix, re-run `py -3 tools/run.py ci --check`.
   - Re-run the relevant lens (`targeted-re-review`) and, for non-trivial fixes, `reviewer-strong` on the touched area (`regression-scan`).

6. **Ready to review (`ready` node).**
   - Only flip the PR out of draft when:
     - `ci --check` is green on the staged tree,
     - `iterative-review` reports no blocking or important issues,
     - the PR body and spec/plan are honest about the final scope.

7. **Wait for remote CI.**
   - GitHub Actions are configured so CI does not run on draft PRs. As soon as the PR is marked ready, it queues the repo's remote gate (here, `marketplace-validation`).
   - After flipping to ready and pushing, wait for the remote run and verify it passes:
     - `gh pr checks <number>`
     - `gh run view <run-id>`
   - Do not report the PR as reviewed or green until the remote CI is actually passing. A green `ci --check` locally does not prove the remote gate passes.
   - In a consumer repo, map this step to the equivalent remote CI check defined in that repo's `.agents/runbooks/pr.md`.

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
