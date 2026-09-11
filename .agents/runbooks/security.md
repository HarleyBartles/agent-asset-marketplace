# Security Runbook

Use this runbook for repo-specific security posture when working in `agent-asset-marketplace`.

## Before you begin

- Read [`REVIEW.md`](../../REVIEW.md) and [`.agents/runbooks/code-review.md`](./code-review.md) for review expectations.
- Invoke `using-superpowers-plus` once and follow its security-review handoff.

## Repo-specific guidance

- When importing or retaining third-party source, verify provenance and license before merge.
- Generated installed skill surfaces under `.agents/skills/` are downstream outputs, not canonical source. Do not hand-edit them to bypass source review.

The selected security profile owns general secret handling, input validation,
logging, and review method. This runbook adds only marketplace-specific source
custody and generated-surface concerns.
