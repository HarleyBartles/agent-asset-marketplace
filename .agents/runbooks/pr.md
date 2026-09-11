# PR Runbook

Use this runbook for pull-request workflow and publication proof in `agent-asset-marketplace`.

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

- Do not run `py -3 tools/run.py ci --check` immediately before a normal commit or immediately after a successful hooked commit. It is a complete CI/PR gate, not a pre-pre-commit step. The pre-commit hook already materializes the staged snapshot, runs `ci --apply`, stages only the owned generated surfaces, and runs `ci --check --diagnostics`; running `ci --check` manually first is wasteful.
- If the pre-commit hook is not installed, run `py -3 tools/run.py ci --apply` manually before committing. Then commit normally; the hook (or `ci --check --diagnostics` if the hook is absent) proves the staged tree. Do not run `ci --check` separately unless no commit follows.
- Only run `py -3 tools/run.py ci --check` deliberately for uncommitted verification, pipeline diagnosis, or explicit CI-parity work.
- `py -3 tools/run.py marketplace --apply` regenerates derived surfaces; stage any generated changes before committing.

The routed publication skill owns generic Draft lifecycle, review sequencing,
commit discipline, and publication handoff.
