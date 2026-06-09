# ChatGPT Apps SDK

Use this skill when you are planning or scaffolding a ChatGPT app that combines MCP-style tools with in-chat UI.

## What this skill covers

- App planning
- Widget and tool boundary design
- Metadata and discovery fields
- Auth and privacy posture
- ChatGPT UI bridge decisions

## Recommended order

1. Write the app's purpose and the user action it enables.
2. Decide which work happens in the server and which work happens in the widget.
3. Define the tool inputs and outputs before the UI details.
4. Add metadata that makes the app understandable to ChatGPT users.
5. Add auth only where the app actually needs it.

## Design rules

- Keep widgets presentational and state-light where possible.
- Keep tool definitions boring, explicit, and honest about side effects.
- Favor standard MCP Apps fields first; use ChatGPT-specific extensions only when they add real value.
- If the app reads or writes user data, plan the auth flow before building the UI.

## Safety checks

- Do not hard-code secrets into the app scaffold.
- Do not expose write actions without a clear user-visible confirmation path.
- Do not design around undocumented platform behavior.
- Do not copy the proprietary OpenAI platform-connector workflow into this pack.

## Scaffolding notes

- Register the server tools.
- Register the UI resources.
- Wire metadata and content security boundaries.
- Test the bridge in the actual ChatGPT runtime, not just in a local mock.

