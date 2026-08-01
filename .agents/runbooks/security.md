# Security Guide

Use this guide for repo-specific security posture when working in `agent-asset-marketplace`.

## Before you begin

- Read [`REVIEW.md`](../../REVIEW.md) and [`.agents/runbooks/code-review.md`](./code-review.md) for review expectations.
- Invoke `/unslop-profiles` with the `security-review` profile for concrete security analysis.

## When to use

- Handling credentials, secrets, or sensitive data.
- Validating external input in scripts or tooling.
- Reviewing third-party source custody or adapter imports.
- Assessing generated artifacts for disclosure risk.

## Repo-specific guidance

- Do not commit secrets, API keys, connection strings, or credentials. Use environment variables or secret managers.
- Do not log sensitive user data or secrets.
- Validate all inputs in `tools/` scripts; prefer parameterized commands over shell string concatenation.
- When modifying `sources/third_party/`, verify provenance and license before import.
- Generated `skill.zip` files in `generated/skill-zips/` are downstream outputs, not canonical source. Do not hand-edit them to bypass source review.

## Routing to skills

- For concrete security analysis, invoke `/unslop-profiles` with the `security-review` profile.
- For code review, invoke `/requesting-code-review` and `/risk-gates`.
- For repo hygiene and publication, invoke `/repo-worker-base`.
