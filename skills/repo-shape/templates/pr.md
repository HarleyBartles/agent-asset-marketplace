# Pull request runbook

Use this runbook for pull-request workflow and publication proof in this repo.

## When

Opening, updating, or publishing a pull request in this repository.

## Required capabilities

- Choose and carry out the authorized publication path.
- Use repository worktree, source-custody, validation, and publication procedures.
- Obtain independent review of consequential changes.
- Evaluate review findings against source and evidence.
- Verify current source and validation evidence before claiming completion.
- Maintain plan and specification status through successor-slice ingress and completion.

## Optional capabilities

None.

## Required repository-owned skills

None.

## Optional repository-owned skills

None.

## Composition

Follow the publication capability selected for this workflow. The agent resolves suitable skills at runtime; Draft lifecycle, commit discipline, review sequencing, and publication handoff belong to those portable capabilities; this runbook records only the consumer repository's commands, CI behavior, proof surface, and exceptions.

Before Ready, complete the repository's plan and specification closeout procedure: promote enduring content, mark governed artifacts `completed-awaiting-retirement`, retain them in the PR, and verify the published head contains them.

Draft is normally a commercial and CI posture, not evidence that implementation is unfinished. When the agent hands off a fully reviewable Draft, every agent-owned plan item is complete and human-owned Ready or merge actions must not remain unchecked. Keep the plan open only when the Draft is explicitly declared incomplete. Whoever later changes the PR state applies the repository's Ready preflight at that time.

## Doctrine and contracts

- Read root [`AGENTS.md`](../../AGENTS.md) `## Publication proof for repo work`.
- Read [`.devin/rules/tools.md`](../../.devin/rules/tools.md) for validation commands.

## Local commands and paths

- Base branch: <!-- name the repository base branch -->
- Local validation command: <!-- exact command -->
- Remote check command or surface: <!-- exact command or URL owner -->
- Draft-aware CI behavior: <!-- local workflow trigger/gate -->
- Publication proof surface: root `AGENTS.md`
- Exceptions: <!-- repository-specific exceptions, or none -->

## Evidence contract

A valid publication-proof form as declared by root `AGENTS.md` `## Publication proof for repo work`.

## Prohibited combinations

none

## Playbook routing

None by default.
