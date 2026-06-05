# Linear v1

Use this skill for Linear object operations through the available Linear connector. This is a connector-mechanics and Linear working-state skill, not the coding dispatch controller.

## Core boundary

Linear is a durable planning and workflow surface. It can hold issues, projects, initiatives, documents, comments, labels, priorities, statuses, relationships, agent delegation, and imported GitHub links.

For coding work after Linear/Codex adoption:

- Use `worker-dispatch-linear-v1` for issue-to-Codex routing, worker-state checks, human PR gate handling, GitHub PR verification routing, and deciding whether a task is Codex Cloud-executable.
- Use this skill only when the current action is to read or mutate Linear objects or maintain Linear working-state surfaces.
- GitHub proves repo facts only after a PR, branch, commit, review, merge, status, or file-state question exists.
- Do not revive GitHub Issues or legacy dispatch doctrine from this skill.

## Durable working-state pattern

For issue-scoped work:

- The issue body is the live current-state window.
- Issue-linked Linear documents are lifecycle-scoped longform working surfaces for ledgers, journals, manifests, expanded context, and readable indexes.
- Comments are event history, small durable notes, worker reports, or links to external proof.

Do not use comments as the primary reconstruction surface when the issue body or issue-linked documents should be updated.

## Read-before-write rule

Before creating, updating, moving, assigning, delegating, commenting, linking, or deleting anything in Linear, inspect the smallest relevant Linear surface unless Harley supplies a current identifier and asks for a direct write.

For simple durable capture requests such as `side note for later`, a direct comment is allowed when the target issue/project is clear from the conversation.

## Quick workflow

1. Classify the Linear operation: read, shape, create, update, comment, relationship, project assignment, status change, cleanup, summarize, assignee/delegate change, or linked-document update.
2. Inspect the smallest relevant Linear object first when the target or current state is not already known.
3. Use stable identifiers where possible: issue IDs such as `MARK-15`, project IDs, team IDs, or exact slugs.
4. Mutate only the requested fields. Do not resend large descriptions unless editing the description is the task.
5. After mutation, use the tool response or a readback to report the exact changed object and any remaining residue.

## Assignee and Codex delegation mechanics

Linear agents and human assignees are distinct.

For Codex Cloud coding work in this workspace, the working assignment shape is:

- human assignee: `Harley Bartles`
- human assignee id: `0f41920d-8499-4555-993d-066c003cf580`
- Codex delegate: `Codex`
- Codex delegate id: `a1b0a6a6-48b3-4af6-9a99-744f5ae357d1`

Do not delegate coding work to the Linear agent. The Linear agent and Codex coding delegate are distinct.

Connector mutation is not proof of delegation. After any assignee/delegate mutation, re-fetch the issue and verify observable state before claiming dispatch or assignment success.

Valid delegation evidence includes:

- issue shows `delegate: Codex`;
- issue shows the expected human assignee;
- status moved to Todo or In Progress as appropriate;
- Codex activity appears on the issue;
- a PR attachment appears on the issue.

If GitHub connector binding causes Linear mutation or verification instability, prefer a Linear-only connector/tool context before retrying Linear assignment/delegation. Do not keep blind-retrying unstable mixed-tool calls.

## Source-truth split

- Linear owns planning/control-plane truth only for objects actually present and verified in Linear.
- GitHub/live repo routes own source code, commits, branches, PRs, CI/statuses, and landed-main proof.
- Chat, session busters, worker reports, and comments are context until verified from the durable surface they claim to describe.

## Project status rule

Project status must reflect child issue reality. Keep a project `In Progress` only when at least one child issue is actively in progress. If every child issue is `Backlog` or `Todo`, prefer `Planned`. Use `Completed` only when the project outcome is done, and `Canceled` only when deliberately abandoned.

## Mutation discipline

For ordinary issue updates, prefer `save_issue` with explicit fields only. For comments, use `save_comment` on the exact issue. For documents, use `save_document` on the exact document.

Do not delete, archive, or destructively rewrite imported issues during exploratory work unless Harley explicitly asks in the latest turn.

## Connector compatibility

Known high-signal quirks:

- Project assignment by project ID has worked where project-name assignment blocked.
- Clearing an issue project with `project: null` was rejected by the exposed schema.
- Some calls were blocked until Harley refreshed the tool, then worked.
- Mixed GitHub/Linear connector binding has caused Linear mutation/verification instability; switch to a Linear-only context before retrying critical assignment/delegation if possible.

## Stop rule

Once the current Linear operation is classified and the needed object has been fetched or mutated, stop. Do not load dispatch, GitHub, validation, or project-wrapper skills unless the next unresolved decision is outside Linear connector mechanics.
