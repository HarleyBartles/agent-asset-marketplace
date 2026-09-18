# Security Playbook

## When

Use when changes affect secrets, permissions, connector mutations, dependencies, or trust boundaries.

## Required skills

- `risk-gates`
- `connector-safety`
- `unslop-profiles`

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)

## Local commands and paths

Use current source, the selected security review profile, and configured tools for proof. When importing or retaining third-party source, verify provenance and license before merge. Treat `.agents/skills/` as downstream output, never as a source-edit bypass.

## Evidence contract

Review identifies trust boundaries, authority, secret handling, and consumer impact with current evidence.

## Prohibited combinations

Do not infer mutation authority or disclose secrets.

## Runbook routing

- [Code review](../runbooks/code-review.md)
