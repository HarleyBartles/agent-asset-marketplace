# Security Runbook

Use this runbook for repo-specific security posture when working in `agent-asset-marketplace`.

## Before you begin

- Read [`REVIEW.md`](../../REVIEW.md) and [`.agents/runbooks/code-review.md`](./code-review.md) for review expectations.
- Invoke `/using-superpowers-plus` once and follow its security-review handoff.

## When to use

- Handling credentials, secrets, or sensitive data.
- Validating external input in scripts or tooling.
- Reviewing third-party source custody or adapter imports.
- Assessing generated artifacts for disclosure risk.

## Repo-specific guidance

- Do not commit secrets, API keys, connection strings, or credentials. Use environment variables or secret managers.
- Do not log sensitive user data or secrets.
- Validate all inputs in `tools/` scripts; prefer parameterized commands over shell string concatenation.
- When importing or retaining third-party source, verify provenance and license before merge.
- Generated installed skill surfaces under `.agents/skills/` are downstream outputs, not canonical source. Do not hand-edit them to bypass source review.
