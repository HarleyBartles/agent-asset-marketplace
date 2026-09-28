# PR Instructions Runbook

## When

Use after implementation and review are complete and source needs publication.

## Required skills

- `publishing-source`
- `repo-worker-base`
- `verification-before-completion`
- `completing-planning-artifacts`

## Composition

Before Ready, use the `completing-planning-artifacts` completing-slice lane: promote enduring content, mark governed artifacts `completed-awaiting-retirement`, retain them in the PR, and verify the published head contains them. Commit through the tracked hook, push the task branch, open a Draft PR, and verify the published head.

Draft is normally a commercial and CI posture, not evidence that implementation is unfinished. When the agent hands off a fully reviewable Draft, every agent-owned plan item is complete and human-owned Ready or merge actions must not remain unchecked. Keep the plan open only when the Draft is explicitly declared incomplete. Whoever later changes the PR state applies the repository's Ready preflight at that time.

## Doctrine and contracts

- [Repository command contract](../contracts/repo-standards-commands.json)
- [Completed artifacts](../doctrine/completed-artifacts.md)

## Local commands and paths

The base branch is `main`. Hosted proof comes from GitHub checks for the exact pushed SHA.

## Evidence contract

Return the verified PR URL, head SHA, validation boundary, and any blocker.

## Prohibited combinations

Do not publish directly to `main` without explicit authorization or bypass the pre-commit hook.

## Playbook routing

None.
