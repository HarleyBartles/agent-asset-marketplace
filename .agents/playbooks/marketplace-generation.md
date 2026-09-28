# Marketplace Generation Playbook

## When

Use when canonical plugin source, bundle manifests, marketplace inventory, or generated projections change.

## Required skills

- `generating-agent-mesh`
- `refreshing-installed-skills`
- `verification-before-completion`

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)

## Local commands and paths

Run `py -3 tools/run.py marketplace --apply` after changes to canonical plugin skills, per-pack provenance, bundle manifests, or plugin manifests. Then run `py -3 tools/run.py installed-skills --apply` for installed projections and the repository-owned index/mesh apply targets when files move.

Editable inputs are canonical trees under `codex-marketplace/plugins/<plugin>/skills/`, per-pack `SOURCE.md`, and plugin metadata. Derived manifests, indexes, bundle manifests, and `.agents/skills/` stay generator-owned. `py -3 tools/run.py ci --apply` is the full reconciliation route used by the commit hook; focused apply targets remain explicit rather than being attributed to `marketplace --apply` alone.

## Evidence contract

Marketplace manifests and installed projections contain the intended current source behavior; installed-skills, mesh, and canonical validation checks are current.

## Prohibited combinations

Do not hand-edit generated manifests, indexes, bundle manifests, or installed skills. Do not treat a generator change as proof until its output changes as intended.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
