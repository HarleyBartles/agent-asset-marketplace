# Planning Runbook

## When

Use when approved requirements need an executable repository plan.

## Required skills

- `writing-plans`
- `handoff-gates`
- `completing-planning-artifacts`

## Composition

After refreshing `main` and creating the slice worktree, run the
`completing-planning-artifacts` successor-slice ingress lane before substantive
edits. Write the committed, in-flight plan before implementation. Source and
overlay edits precede regeneration and validation.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Plans live under `.agents/plans/`. Use `py -3 tools/run.py mesh --apply` after adding one.

## Evidence contract

Eligible predecessor artifacts are retired in the first commit of this
eventual PR. The committed in-flight plan names exact files, test cycles,
generation, validation, and publication proof.

## Prohibited combinations

Do not hand off an uncommitted plan, call it durable repository truth, or open a cleanup-only PR.

## Playbook routing

- [Repository doctrine](../playbooks/repo-doctrine.md) - when the plan changes repository doctrine, standards, or routing.
