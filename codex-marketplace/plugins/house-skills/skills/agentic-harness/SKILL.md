---
name: agentic-harness
description: Use when designing, reviewing, or debugging agent loops, harness construction, tool/action spaces, or multi-agent orchestration.
metadata:
  source-id: agentic-harness
  source-path: sources/first_party/skills/agentic-harness/SKILL.md
  provenance-name: Agentic Harness first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when designing, reviewing, or debugging agent loops, harness construction, tool/action spaces, or multi-agent orchestration.
  use_when:
  - Use when designing or reviewing an agent loop.
  - Use when choosing or constructing a harness for tools and actions.
  - Use when orchestrating multiple agents or merging parallel results.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - agent-evaluation
  - research-ops
  - release-engineering
license: MIT
---

# Agentic Harness

Use this skill when designing or reviewing agent loops, harness construction, tool/action spaces, and multi-agent orchestration.

## When to Use

- Designing or reviewing an agent loop.
- Choosing or constructing a harness for tools and actions.
- Orchestrating multiple agents or merging parallel results.

## Core Pattern

1. Model the loop explicitly: input, plan, tool call, observation, output, stop check.
2. Define tools with typed schemas and documented side effects; keep the action space small and composable.
3. Isolate state between parallel agents (for example, git worktrees or sandboxed contexts) and merge through explicit handoff.
4. Set iteration and error budgets to prevent silent infinite loops.
5. Test the harness against deterministic trajectories before scaling to open-ended work.

## Common Mistakes

- Leaking shared mutable state between parallel agents. → Isolate contexts and merge explicitly.
- Implicit infinite loops. → Set iteration and error budgets.
- Opaque tool failures. → Normalize errors into structured observations.

Load `references/operational-guidance.md` for deeper coverage of loop design, tool spaces, orchestration, and harness construction.
