# Planning Runbook

## When

Use when approved requirements need an executable repository plan.

## Required skills

- `writing-plans`
- `handoff-gates`

## Composition

Write the durable plan before implementation. Source and overlay edits precede regeneration and validation.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Plans live under `.agents/plans/`. Use `py -3 tools/run.py mesh --apply` after adding one.

## Evidence contract

The committed plan names exact files, test cycles, generation, validation, and publication proof.

## Prohibited combinations

Do not hand off an uncommitted plan.

## Playbook routing

- [Repository doctrine](../playbooks/repo-doctrine.md) - when the plan changes repository doctrine, standards, or routing.
