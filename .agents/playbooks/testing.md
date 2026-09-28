# Testing Playbook

## When

Use when behavior changes, tests are authored, or validation is selected.

## Required skills

- `test-driven-development`
- `verification-before-completion`

## Composition

Apply the named capability skills under the binding doctrine and local evidence requirements. This playbook does not own a lifecycle stage.

## Doctrine and contracts

- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Run focused tests with `py -3 -m pytest tests/<file>.py -v`. Contract tests live under `tests/`. Marketplace generation correctness requires `py -3 tools/run.py marketplace --apply`; the complete local gate is `py -3 tools/run.py ci --check`, while normal commits rely on the tracked hook. Source-custody, plugin-shape, manifest, provenance, or generated-zip changes require the full marketplace rebuild.

## Evidence contract

New behavior has a witnessed red-green cycle and the relevant focused or complete gate passes.

## Prohibited combinations

Do not substitute a green unrelated test for the changed behavior.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
