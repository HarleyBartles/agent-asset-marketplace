# Golden Gate

Read before delegating a Linear issue to Codex Cloud, nudging a Codex worker, or treating a planning issue as executable worker work.

## Decision

Delegate to Codex only when all answers are yes:

1. The latest user message authorizes execution or dispatch, not just discussion.
2. The target is a repo-backed coding/docs/config surface that Codex Cloud can clone, edit, validate, and publish as a PR.
3. The Linear issue identifies the repo or implementation surface clearly enough for a worker.
4. The task can be completed inside the Codex Cloud environment without private ChatGPT skill-library mutation, manual UI-only actions, unavailable local resources, or hidden credentials.
5. The expected output can return through Linear comments plus a Codex/GitHub PR publication path.
6. The issue body is bounded enough that Codex is executing, not deciding product strategy or architecture from scratch.
7. Any required human gate is explicit.

If any answer is no, do not delegate. Route to planning, native skill maintenance, connector setup, UI instructions, research, or a legacy fallback as appropriate.

## Blip catchers

Block Codex delegation when the work is mainly:

- creating, updating, validating, or packaging ChatGPT native skills, unless the editable skill source is known to live in a Codex-accessible repo;
- changing ChatGPT custom instructions, memory, project instructions, or connector settings;
- researching docs or product behavior without repo edits;
- asking Harley to click a UI control, install an app, grant permissions, or configure an account;
- requiring local-only files, private desktop state, or secrets unavailable to Codex;
- deciding broad doctrine before the doctrine has been shaped into concrete repo-backed edits.

Crew, project routers, and native skill-maintenance routes are allowed to stop the dispatch before this skill delegates. Treat that as correct friction, not a failure.

## Gate result language

Use one of these outcomes:

- `pass_delegate`: issue is executable by Codex and current user authorized dispatch.
- `hold_native_route`: the task belongs to GPT-native skill, connector, UI, research, or planning work.
- `hold_shape_issue`: the task may be Codex-executable but the Linear issue is not worker-ready.
- `hold_unavailable_surface`: the task target is not accessible/publishable from Codex Cloud.
- `legacy_plan_b`: Linear/Codex is unavailable or explicitly not in use.

For holds, name the next concrete action. Do not delegate "just to see."
