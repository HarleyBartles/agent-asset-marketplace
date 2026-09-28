# Marketplace Generation Playbook

## When

Use when canonical plugin source, bundle manifests, marketplace inventory, or generated projections change.

## Required skills

- `refreshing-installed-skills`
- `verification-before-completion`

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)

## Local commands and paths

Run `py -3 tools/run.py marketplace --apply` after changes to `skills/`, `shared/`, or `src/plugin-definitions/`. Then refresh installed skills when their source or membership changes.

Editable inputs are canonical skills under `skills/`, reusable resources under `shared/`, and plugin definitions under `src/plugin-definitions/`. `py -3 tools/build_marketplace.py --apply` assembles complete plugin packages under `dist/plugins/`; the marketplace target also updates catalog and inventory surfaces. Manifests, bundle manifests, built plugin trees, and `.agents/skills/` stay generator-owned. `py -3 tools/run.py ci --apply` is the full reconciliation route used by the commit hook.

## Evidence contract

Marketplace manifests and installed projections contain the intended current source behavior; installed-skill and canonical validation checks are current.

## Prohibited combinations

Do not hand-edit generated manifests, bundle manifests, or installed skills. Do not treat a generator change as proof until its output changes as intended.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
