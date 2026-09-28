# Implementing Runbook

## When

Use for repository-backed implementation.

## Required skills

- `executing-plans` or `subagent-driven-development`
- `test-driven-development`
- `verification-before-completion`

## Composition

Work from the committed plan in an isolated worktree. Edit canonical source, exercise each applicable playbook, then regenerate owned projections.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Canonical plugin source lives under `codex-marketplace/plugins/<plugin>/skills/`. Use `py -3 tools/run.py marketplace --apply` after source changes, then `py -3 tools/run.py installed-skills --apply` to refresh installed projections.

When repo-local runtime subagent profiles under `.agents/agents/` change, run `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout` from the worktree and restart the IDE before dispatching a changed profile.

## Evidence contract

Focused tests pass, generated marketplace and mesh surfaces are current, and the normal hooked commit proves the staged tree.

## Prohibited combinations

Do not hand-edit installed `.agents/skills/` projections or implement from the shared checkout.

## Playbook routing

- [Code style](../playbooks/code-style.md) - when Python or Markdown changes.
- [Testing](../playbooks/testing.md) - when behavior changes or validation is required.
- [Marketplace generation](../playbooks/marketplace-generation.md) - when vendored assets or manifests change.
- [Skill authoring](../playbooks/skill-authoring.md) - when a skill changes.
- [Repository doctrine](../playbooks/repo-doctrine.md) - when standards, doctrine, contracts, or routing change.
