# Pressure testing with subagents

This directory holds reusable pressure-test inputs for first-party skills. Each
subdirectory defines a scenario and the behavior to inspect. A run is transient
evidence for the current handoff; its model output, scores, transcripts, and
result records do not belong in Git.

## When to pressure-test a skill

Pressure tests are advisory. Add one when:

- The skill prevents a common failure mode.
- The skill routes the agent to a specific, non-obvious action.
- The wrong choice is costly (rework, token waste, destructive side effects).

Pure reference skills or skills without a concrete failure mode usually do not need a pressure test.

## How to run a pressure test

### 1. Identify the failure mode

Write the pressure scenario as a realistic task where an agent is likely to choose the wrong tool or action.

### 2. Prepare the scenario file

Add `assets/pressure-tests.md` to the skill. This scenario file ships with the skill so any consumer can run the test; proof records do not ship with the skill. It should include:

- A short task description.
- A **RED** path: what an agent without the skill is likely to do.
- A **GREEN** path: what an agent with the skill does.
- The exact tool, inputs, and reasoning that prove the skill's value.

Example: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/assets/pressure-tests.md`

### 3. Run RED and GREEN subagents

Launch two `subagent_general` runs in parallel:

- **RED:** The subagent may not read the skill files. It can call MCP tools (e.g., `mcp_list_tools`) and use general reasoning.
- **GREEN:** The subagent reads the skill's `SKILL.md`, `references/`, and `assets/pressure-tests.md` files and applies them as if it had invoked the skill.

Subagents cannot invoke skills directly, but they can read skill files from disk and act on them. They may also call any tools they have access to, including MCP tools.

### 4. Do not pre-bake fixtures

Let the subagents experience the real tool surface. For example:

- **Do not** create truncated `mcp_list_tools` fixture files and pass them to the RED subagent.
- **Do** let the RED subagent call `mcp_list_tools` on the real MCP server. If the output is truncated, the subagent must deal with the same discovery cost a real agent would.

If a tool is gated, expensive, or unsafe to call, replace it with a faithful read-only equivalent (e.g., a dumped schema) and document the substitution in the test.

### 5. Judge the run

Inspect:

- The exact prompts given to each subagent.
- The chosen tool or action for each run.
- Reasoning and any rationalizations relevant to the current decision.
- The final RED/GREEN judgment.

Report that judgment in the current handoff. Do not commit run output or a
results ledger. Change the reusable prompt, rubric, campaign configuration, or
deterministic assertion only when the run exposes a contract defect.

### 6. Validate

Run the canonical commands before claiming the campaign is done:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py ci --check
```

## References

- `.agents/doctrine/skill-standards-policy.md` — policy and advisory.
- `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/testing-skills-with-subagents.md` — RED/GREEN methodology.
