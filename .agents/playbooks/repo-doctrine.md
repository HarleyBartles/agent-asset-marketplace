# Repository Doctrine Playbook

## When

Use when repository standards, doctrine, contracts, routing, or agent-facing policy change.

## Required capabilities

- Apply the repository standards that this repository explicitly adopts.
- Respect cross-project operating invariants and authority boundaries.
- Write clear human-facing repository guidance.

## Optional capabilities

None.

## Required repository-owned skills

None.

## Optional repository-owned skills

None.

## Composition

Resolve the stated capabilities against skills available at runtime, under the binding doctrine and local evidence requirements. Stop and report if a required capability has no suitable provider. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Repository runbook policy](../doctrine/repo-runbook-policy.md)

## Local commands and paths

Edit the owning canonical marketplace source when consumers should inherit the change. Regenerate the marketplace after source edits. Root `AGENTS.md` and scoped doctrine remain law surfaces; this playbook contains procedures and pointers, not operative law.

Canonical validation is `py -3 tools/run.py ci --check`; marketplace reconciliation is `py -3 tools/run.py marketplace --apply`. Review entry is `REVIEW.md`, contribution entry is `CONTRIBUTING.md`, and publication proof is an open PR or explicitly authorized direct-main commit.

## Evidence contract

The owning surface is explicit, links resolve, consumer projections are current, and no stale competing authority remains.

## Prohibited combinations

Do not place procedure in doctrine or durable truth in a workflow artifact.

## Runbook routing

- [Planning](../runbooks/planning.md)
- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
