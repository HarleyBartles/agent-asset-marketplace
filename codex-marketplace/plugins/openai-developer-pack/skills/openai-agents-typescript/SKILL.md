# OpenAI Agents SDK TypeScript

Use this skill when the implementation target is JavaScript or TypeScript and the app needs agent orchestration, tool definitions, or SDK-backed workflow boundaries.

## Core posture

- Keep the agent graph explicit.
- Treat the model as a planner inside a constrained program, not as the program itself.
- Separate transport, tool execution, and user-facing UI concerns.
- Use the SDK's examples as shape references, not as a substitute for local validation.

## Build flow

1. Define the agent's job in one short paragraph.
2. Add only the tools that support that job.
3. Use typed inputs and outputs for anything the rest of the app depends on.
4. If the workflow spans more than one specialist, split the work into separate agents or handoffs.
5. Add a small end-to-end test that exercises the full path, not just the happy-path prompt.

## Checks that matter

- Verify that tool names match their actual behavior.
- Verify that the agent can recover from a tool failure without losing the conversation state.
- Verify that structured output parsing fails loudly when the model deviates from the expected shape.
- Verify that any sandbox or filesystem access is limited to the intended workspace.

## Common failure modes

- The model asks for a tool that does not exist.
- A tool returns data the UI cannot render.
- Handoff routing becomes ambiguous because the agents are too broad.
- A state mutation leaks out of the tool boundary and becomes hard to replay.

## Docs-first rule

- Use the current official Agents SDK JS docs for syntax and runtime details.
- Do not transpose Python examples into TypeScript without checking the JS SDK shape.

