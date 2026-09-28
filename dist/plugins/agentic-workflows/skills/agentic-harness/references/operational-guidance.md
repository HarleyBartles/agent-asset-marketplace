# Agentic Harness operational guidance

## When to apply

Use when the agentic-harness skill is loaded and the task involves designing, reviewing, or debugging agent loops, harness construction, tool/action spaces, or multi-agent orchestration.

## Agent loop design

1. Keep the loop state explicit: input, plan, tool calls, observations, output.
2. Terminate on completion, error budget, or user interruption; never loop silently.
3. Log every iteration with tool inputs and outputs for replay and debugging.

## Tool and action spaces

1. Define tools as typed functions with input schemas and documented side effects.
2. Keep the action space small enough to be predictable; compose complex actions from primitives.
3. Validate tool outputs and surface failures as structured observations, not hidden retries.

## Multi-agent orchestration

1. Partition work by role or sub-task; assign one goal per agent.
2. Use a dispatcher or supervisor to route tasks and merge results.
3. Isolate state between agents (for example, git worktrees or sandboxed contexts) and merge through explicit handoff.

## Harness construction

1. Start with a minimal loop: planner -> executor -> observer -> stop check.
2. Add concurrency only after the sequential loop is reliable.
3. Test harnesses against deterministic trajectories before scaling to open-ended tasks.

## Common mistakes

- Leaking shared mutable state between parallel agents. → Isolate worktrees or contexts and merge explicitly.
- Implicit infinite loops. → Set iteration and error budgets.
- Tool schemas that return opaque failures. → Normalize errors into observations.

## Related references

- dmux: https://github.com/standardagents/dmux
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- Anthropic building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic multi-agent research: https://www.anthropic.com/engineering/multi-agent-research-system
