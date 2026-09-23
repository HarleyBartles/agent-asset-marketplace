# Jev MCP Plugin Plan

**Goal:** Publish a Codex marketplace plugin that connects the community Jev MCP and teaches agents to use its six decision tools, with model routing as the first concrete use case.

**State:** completed-awaiting-retirement

## Scope

- Create a `jev-mcp` plugin in the canonical marketplace tree, with an authenticated remote MCP declaration and a `using-jev-mcp` skill.
- Keep existing `selecting-a-subagent` policy authoritative. The skill may consult Jev for a bounded route judgment but must validate live availability, Astra's exceptional status and low-effort ceiling, reasoning, and context constraints before dispatch.
- Do not install a key, change user config, or make Jev mandatory for delegation.

## Execution

1. Retire the completed predecessor plan and commit this plan before implementation.
2. Define a focused RED check for MCP configuration, tool routing, and hard policy boundaries; then scaffold the plugin and skill.
3. Run focused validation, regenerate marketplace outputs, inspect the generated inventory, and use the tracked pre-commit gate.
4. Review the committed diff, publish a draft PR to `main`, and verify its head and checks. Mark this plan `completed-awaiting-retirement` when agent-owned work is complete.

## Completion evidence

- The focused MCP contract test passed after a RED failure for the missing declaration.
- Marketplace and mesh generation completed; the staged pre-commit gate passed for the implementation commit.
- The package was reviewed as a draft-PR handoff. A live Jev decision call requires a personal key and an installed MCP connection in the consuming runtime.
