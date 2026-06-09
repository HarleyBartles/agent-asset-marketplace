# OpenAI Agents SDK Python

Use this skill when the target implementation is Python and the workflow needs agents, tools, tracing, MCP-backed tools, or a reproducible developer loop.

## Core posture

- Start with the smallest agent that can complete the task.
- Keep tool definitions narrow and typed.
- Treat tracing as part of development, not as an afterthought.
- Prefer explicit handoffs or specialist agents over one oversized general agent.

## Build flow

1. Define the agent role and the minimum instruction set.
2. Add only the tools that the agent actually needs.
3. If a capability already exists as an MCP server, connect to that server rather than reimplementing the same boundary.
4. Use the SDK's tracing and example patterns to validate the behavior before expanding the workflow.

## Practical checks

- Make sure every tool has a stable name, a short description, and a predictable schema.
- Keep side effects isolated behind tools so they can be tested without a full conversation loop.
- If the agent output will be consumed by code, validate the schema before using the result.
- If the agent fails on a tool call, inspect whether the failure belongs in the tool, the agent, or the surrounding orchestration.

## Debug loop

- Reproduce the failure with one input.
- Run the agent with tracing enabled.
- Inspect tool calls, model messages, and handoffs in order.
- Patch the smallest layer that owns the bug.
- Re-run the same input and one nearby variant.

## Useful references

- OpenAI Agents SDK Python docs
- Tools guide
- MCP guide
- Tracing guide
- Examples directory

