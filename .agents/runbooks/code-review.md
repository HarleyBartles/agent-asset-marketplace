# Code Review Runbook

## When

Use for final whole-branch review and focused review of repository changes.

## Required skills

- `requesting-code-review`
- `receiving-code-review`
- `unslop-profiles`

## Composition

Review the actual diff against the plan, applicable playbooks, doctrine, and consumer safety.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)

## Local commands and paths

Use `py -3 tools/run.py ci --check` only for uncommitted verification or diagnosis; the normal commit hook proves the staged tree.

## Evidence contract

Findings cite current source, all applicable topical constraints are checked, and generated outputs reflect canonical changes.

## Prohibited combinations

Do not treat installed projections, worker reports, or stale summaries as source truth.

## Playbook routing

- [Code style](../playbooks/code-style.md) - when reviewing Python or Markdown.
- [Testing](../playbooks/testing.md) - when reviewing behavior or validation.
- [Security](../playbooks/security.md) - when the diff has a security surface.
- [Skill authoring](../playbooks/skill-authoring.md) - when a skill changes.
- [Marketplace generation](../playbooks/marketplace-generation.md) - when vendored outputs change.
- [Repository doctrine](../playbooks/repo-doctrine.md) - when standards or routing change.
