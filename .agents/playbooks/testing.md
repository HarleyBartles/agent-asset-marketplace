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

Run focused tests from the changed skill's `skills/<skill-id>/tests/` directory. Pressure cases are evaluated with the relevant skill; their run results remain transient. The commit and PR gate runs `tests/build/`, `tests/repository/`, and `tests/shipping/` as separate suites. The pressure-runner unit suite is `tests/evaluation-harness/` and runs when its tooling changes. Marketplace generation correctness requires `py -3 tools/build_marketplace.py --check`; normal commits rely on the tracked hook for the complete repository gate. Default pytest discovery covers only the three commit-gated suites.

## Evidence contract

New behavior has a witnessed red-green cycle and the relevant focused or complete gate passes.

## Prohibited combinations

Do not substitute a green unrelated test for the changed behavior.

## Runbook routing

- [Implementation](../runbooks/implementing.md)
- [Code review](../runbooks/code-review.md)
