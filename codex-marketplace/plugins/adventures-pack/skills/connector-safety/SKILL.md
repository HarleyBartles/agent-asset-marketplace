---
name: connector-safety
description: use this skill to keep connector and tool-side-effect work safe, auditable, and boring when a write is blocked or when a planned action could be sensitive, destructive, permission-changing, or easy to over-bundle.
---

# Connector Safety

Use this skill to keep connector and tool-side-effect work safe, auditable, and boring when a write is blocked or when a planned action could be sensitive, destructive, permission-changing, or easy to over-bundle.

## Core rule

Treat connector or tool safety blocks as signals to narrow, clarify, verify, or stop. Do not frame the safety layer as an adversary and do not try to bypass it.

A blocked mutation is not proof that the mutation happened. A planned mutation is not proof of authorization. A retry is lawful only when it is materially safer, narrower, clearer, or more auditable than the failed call.

## Use this skill when

Use this skill when the task involves:

- a blocked connector/tool write;
- a side-effecting connector action such as creating, updating, deleting, sending, moving, assigning, renaming, archiving, merging, or publishing;
- deciding whether to retry after a tool or connector block;
- reducing a large mutation into smaller safer steps;
- writing or reviewing guidance for connector-safe recovery;
- reporting a blocked action without laundering it into completion.

Do not use this skill for ordinary read-only lookup unless the read is part of a blocked-write recovery or sensitive side-effect plan.

## Safe action ladder

1. Confirm current authority from the latest user request and the relevant durable surface.
2. Inspect the smallest relevant current state before writing when practical.
3. Prefer one side effect per call: create, update body, rename, relate, move, assign, or close as separate steps.
4. Keep payloads narrow and specific. Avoid bundling broad tool-control instructions, unrelated doctrine, and multiple mutations in one call.
5. If a call is blocked, do not claim success. Read back current state when safe to determine whether anything changed.
6. Retry only with a materially safer shape, such as smaller content, fewer fields, a non-destructive read probe, an ID instead of a name, or separate create-then-enrich steps.
7. Stop after repeated narrow failures, destructive ambiguity, unsupported schema errors, or unclear authority.
8. Report the blocker with enough detail for the user or next actor to continue safely.

## Mutation classes

Use stricter posture as side effects increase.

- Low-risk writes: comments, draft notes, non-destructive metadata, or compact document updates. Narrow once, retry once or twice if safe.
- Medium-risk writes: issue status, assignment, labels, project moves, document renames, calendar drafts, email drafts. Separate fields and verify after mutation.
- High-risk writes: sends, deletes, archives, merges, closes, publishes, permission changes, irreversible or externally visible actions. Require clear user authorization and do not retry ambiguously.

## Blocked-write report shape

When a connector/tool action blocks or remains uncertain, report:

Attempted action: <what was attempted>
Target: <system and object>
Authority used: <latest user instruction or durable authorization>
Observed result: <tool response, block, or no response>
Verification: <readback performed or why not>
Safe retry attempted: <narrower retry or none>
Final state: <done / not done / unknown>
Next safe action: <manual action, narrower retry, missing authorization, or blocker>

Keep this report factual. Do not include hidden policy speculation or claim exact classifier triggers.

## Retry guidance

A retry must change the risk shape. Good retries include:

- create a minimal object first, then enrich it;
- update only the title or only the body;
- remove unrelated context from the payload;
- split destructive and non-destructive work;
- use a known stable ID instead of fuzzy name matching;
- do a harmless read probe before another mutation;
- ask for explicit confirmation when authority is ambiguous.

Bad retries include:

- repeating the same blocked payload;
- adding language about bypassing, defeating, or working around safety;
- using another connector surface to smuggle the same blocked mutation;
- claiming completion from a planned action, chat summary, or stale state;
- continuing after destructive ambiguity.

## Handoff and evidence

For durable work, leave compact evidence in the proper return surface only after the action is actually performed or definitively blocked.

Do not update issue closeout, status, or proof surfaces to say a package, mutation, send, merge, close, or install happened until the actual handoff or mutation is complete and verified.

When install, package, or artifact handoff is involved, verify the exact file/path/hash or tool response immediately before presenting it. A planned path is not proof.

## Stop signs

Stop and report instead of retrying when:

- the user has not authorized the side effect;
- the target object is ambiguous;
- the operation is destructive, irreversible, externally visible, or permission-changing and the result is uncertain;
- the connector reports an unsupported schema or missing capability;
- repeated narrower attempts fail;
- readback contradicts the expected result;
- the only available next step would be to bypass, hide, or misrepresent a safety layer.
