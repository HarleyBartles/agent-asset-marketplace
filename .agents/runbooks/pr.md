# PR Runbook

Use this runbook for pull-request workflow and publication proof in `agent-asset-marketplace`.

## Required skills

- `publishing-source` - publication method and proof shape.
- `repo-worker-base` - worktree, branch, and validation boundaries.
- `verification-before-completion` - completion evidence.

## Before you begin

- Read root [`AGENTS.md`](../../AGENTS.md) `## Publication proof for repo work` and `## Draft PR policy` for the durable doctrine.
- Read [`.devin/rules/pr.md`](../../.devin/rules/pr.md) for the conditional rule trigger that loads this runbook.
- Invoke `using-superpowers-plus` once and follow its publication handoff.

## When to use

- Preparing a branch for review.
- Creating or updating a PR.
- Providing publication proof for repo work.

## Draft PR policy

This repo's rules:

- Open pull requests as **draft**.
- This repo's CI must not run on draft pull requests. The `marketplace-validation` workflow skips draft PRs and runs once a PR is no longer draft; it is gated by `github.event.pull_request.draft == false`.
- The published PR is the publication proof; its body describes scope and
  material evidence boundaries rather than restating its own metadata.

## Repo-specific guidance

- The portable rule for when to run the complete gate lives in `repo-standards` `references/ci-validation-pipeline.md`; this repo's command is `py -3 tools/run.py ci --check [--diagnostics]`.
- `py -3 tools/run.py marketplace --apply` regenerates derived surfaces; stage any generated changes before committing.

The routed publication skill owns generic Draft lifecycle, review sequencing,
commit discipline, and publication handoff.
