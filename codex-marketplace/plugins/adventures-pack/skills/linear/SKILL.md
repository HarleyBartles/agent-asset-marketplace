---
name: linear
description: "Use for Linear connector mechanics: reading, creating, updating, commenting, and organizing Linear issues, projects, documents, labels, and statuses. Use when the user asks to inspect or mutate Linear objects, capture side notes durably, create planning issues/projects, or recover from Linear connector quirks. Do not use as the coding dispatch control plane: Linear/Codex worker routing, Codex status checks, PR-gate handling, and dispatch decisions belong to worker-dispatch-linear-v1; GitHub proof belongs to the repo/GitHub proof surface."
---

# Linear

Use this skill for Linear object operations through the available Linear connector. This is a connector-mechanics skill, not the coding dispatch controller.

## Core boundary

Linear is a durable planning and workflow surface. It can hold issues, projects, initiatives, documents, comments, labels, priorities, statuses, relationships, and imported GitHub links.

For coding work after Linear/Codex adoption:

- Use `worker-dispatch-linear-v1` for issue-to-Codex routing, worker-state checks, human `Create PR` gate handling, and deciding whether a task is Codex Cloud-executable.
- Use this skill only when the current action is to read or mutate Linear objects.
- Use the repo/GitHub proof surface after a GitHub PR, branch, commit, review, merge, status, or file-state question exists.
- Do not revive GitHub issue or legacy dispatch doctrine from this skill.

## Read-before-write rule

Before creating, updating, moving, assigning, commenting, or deleting anything in Linear, inspect the smallest relevant Linear surface unless Harley supplies a current identifier and asks for a direct write.

For simple durable capture requests such as `side note for later`, a direct comment is allowed when the target issue/project is clear from the conversation.

## Quick workflow

1. Classify the Linear operation: read, shape, create, update, comment, relationship, project assignment, status change, cleanup, or summarize.
2. Inspect the smallest relevant Linear object first when the target or current state is not already known.
3. Use stable identifiers where possible: issue IDs such as `HAR-241`, project IDs, team IDs, or exact slugs.
4. Mutate only the requested fields. Do not resend large descriptions unless editing the description is the task.
5. After mutation, use the tool response or a readback to report the exact changed object and any remaining residue.

## Source-truth split

- Linear owns planning/control-plane truth only for objects actually present and verified in Linear.
- GitHub/live repo routes own source code, commits, branches, PRs, CI/statuses, and landed-main proof.
- Chat, session busters, worker reports, and comments are context until verified from the durable surface they claim to describe.

## Project status rule

Project status must reflect child issue reality. Keep a project `In Progress` only when at least one child issue is actively in progress. If every child issue is `Backlog` or `Todo`, prefer `Planned`. Use `Completed` only when the project outcome is done, and `Canceled` only when deliberately abandoned.

## Mutation discipline

For ordinary issue updates, prefer `save_issue` with explicit fields only. For comments, use `save_comment` on the exact issue. For test changes, include an obvious marker such as `CLEARLY TEST -`; for durable planning changes, do not use test markers.

Do not delete, archive, or destructively rewrite imported issues during exploratory work unless Harley explicitly asks in the latest turn.

## Connector compatibility

Load `references/connector-compatibility.md` before project assignment, taxonomy migration, sync verification, cleanup of test residue, or recovery from a blocked Linear tool call.

Known high-signal quirks:

- Project assignment by project ID has worked where project-name assignment blocked.
- Clearing an issue project with `project: null` was rejected by the exposed schema.
- Some calls were blocked until Harley refreshed the tool, then worked.

## Legacy overlays

`references/wild-bunch-linear-overlay.md` is legacy/import-trial context. Do not load it for normal Wild Bunch coding dispatch, worker status, PR gate, or GitHub verification. Use it only for historical Linear taxonomy migration or imported-GitHub cleanup questions.

## Stop rule

Once the current Linear operation is classified and the needed object has been fetched or mutated, stop. Do not load dispatch, GitHub, validation, or project-wrapper skills unless the next unresolved decision is outside Linear connector mechanics.
