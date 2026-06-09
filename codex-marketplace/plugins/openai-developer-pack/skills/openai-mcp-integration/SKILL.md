# OpenAI MCP Integration

Use this skill when the app needs to expose tools through MCP or consume tools from an MCP server inside an OpenAI workflow.

## Goal

- Keep the MCP boundary explicit.
- Make the tool contract small enough that the model can understand it.
- Preserve a clean separation between transport, auth, and the business action behind the tool.

## Build order

1. Decide whether the server is read-only, user-scoped, or write-capable.
2. Define the tool list before writing implementation code.
3. Map each tool to one responsibility.
4. Add approval or auth gates for any action that mutates state.
5. Add error handling that helps the model recover instead of collapsing the whole run.

## Good MCP habits

- Keep names stable.
- Keep descriptions specific.
- Return data that is easy to validate.
- Use the server logs to diagnose request shape and auth failures.
- Prefer a narrow adapter around an existing internal service over a second copy of the same logic.

## Security posture

- Authenticate before exposing customer data or write actions.
- Treat environment variables as local configuration, not as a secret store.
- Prefer short-lived credentials or scoped tokens when the platform supports them.
- If the tool is not safe for unattended execution, make that explicit in the tool contract and in the surrounding app policy.

