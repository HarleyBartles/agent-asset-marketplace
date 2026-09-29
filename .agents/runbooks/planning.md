# Planning Runbook

## When

Use when approved requirements need an executable repository plan.

## Required capabilities

- Create a concrete implementation plan from approved requirements.
- Check readiness at a planning or review handoff.
- Maintain plan and specification status through completion.

## Optional capabilities

None.

## Required repository-owned skills

None.

## Optional repository-owned skills

None.

## Composition

After refreshing the repository base and creating the slice worktree, complete the repository's plan-ingress procedure before substantive edits. Write the committed, in-flight plan before implementation. Source and overlay edits precede regeneration and validation.

## Doctrine and contracts

- [Custody and marketplace doctrine](../doctrine/custody-and-marketplace-doctrine.md)
- [Repository command contract](../contracts/repo-standards-commands.json)

## Local commands and paths

Plans live under `.agents/plans/`. Link the current plan from the task conversation or the relevant scoped `AGENTS.md` guidance.

## Evidence contract

Eligible predecessor artifacts are retired in the first commit of this eventual PR. The committed in-flight plan names exact files, test cycles, generation, validation, and publication proof.

## Prohibited combinations

Do not hand off an uncommitted plan, call it durable repository truth, or open a cleanup-only PR.

## Playbook routing

- [Repository doctrine](../playbooks/repo-doctrine.md) - when the plan changes repository doctrine, standards, or routing.
