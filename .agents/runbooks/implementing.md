# Implementing Runbook

## When

Use for repository-backed implementation.

## Required capabilities

- Execute the approved implementation plan.
- Coordinate independent implementation tasks when useful.
- Use behavior-focused tests to guide changes.
- Verify the completed tree and report evidence.

## Optional capabilities

None.

## Required repository-owned skills

None.

## Optional repository-owned skills

None.

## Composition

Work from the committed plan in an isolated worktree. Edit canonical source, exercise each applicable playbook, then regenerate owned projections.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Canonical skill source lives under `skills/`, reusable resources under `shared/`, and product membership under `src/plugin-definitions/`. Use `py -3 tools/run.py marketplace --apply` after source changes, then refresh installed projections when needed.

When repo-local runtime subagent profiles under `.agents/agents/` change, run `py -3 tools/run.py runtime-agents --apply` from the worktree and restart the IDE before dispatching a changed profile.

## Evidence contract

Focused tests pass, generated marketplace surfaces are current, and the normal hooked commit proves the staged tree.

## Prohibited combinations

Do not copy plugin skills into `.agents/skills/`; use native repo plugin declarations and work from an isolated worktree.

## Playbook routing

- [Code style](../playbooks/code-style.md) - when Python or Markdown changes.
- [Testing](../playbooks/testing.md) - when behavior changes or validation is required.
- [Marketplace generation](../playbooks/marketplace-generation.md) - when vendored assets or manifests change.
- [Skill authoring](../playbooks/skill-authoring.md) - when a skill changes.
- [Repository doctrine](../playbooks/repo-doctrine.md) - when standards, doctrine, contracts, or routing change.

## Unslop profile routing

Read the [repository Unslop profile](../unslop/repository.md) during implementation and result review. If `$unslop-profiles` is available, use it when evidence claims, source-versus-generated ownership, or scope and lifecycle decisions fit its cues; skip unrelated cues.
