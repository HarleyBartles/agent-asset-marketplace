---
name: agent-evaluation
description: Use when evaluating agent outputs, designing benchmarks, or building self-evaluation rubrics.
metadata:
  source-id: agent-evaluation
  source-path: sources/first_party/skills/agent-evaluation/SKILL.md
  provenance-name: Agent Evaluation first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when evaluating agent outputs, designing benchmarks, or building self-evaluation rubrics.
  use_when:
  - Use when evaluating an agent's output against a rubric.
  - Use when designing or running a benchmark.
  - Use when building a self-evaluation workflow.
  do_not_use_when:
  - Do not use when another more specific skill owns the task.
  related_skills:
  - agentic-harness
  - research-ops
  - observability
license: MIT
---

# Agent Evaluation

Use this skill when evaluating agent outputs, designing benchmarks, or building self-evaluation rubrics.

## When to Use

- Evaluating an agent's output against a rubric.
- Designing or running a benchmark.
- Building a self-evaluation workflow.

## Core Pattern

1. Define the evaluation dimension (correctness, completeness, safety, concision) and scoring anchors before scoring.
2. Build or select benchmark tasks that reflect real deployment conditions and hold out a final test set.
3. Score outputs against rubrics or reference solutions, not just model self-ratings.
4. Report per-task and per-dimension results with failure modes and confidence intervals.
5. Keep the evaluation harness separate from the evaluated agent to avoid leakage.

## Common Mistakes

- Reporting a single aggregate score without a breakdown. → Report per-dimension and per-task results.
- Reusing the test set as a development target. → Hold out a final evaluation set.
- Evaluating on politeness or verbosity instead of outcomes. → Score end results against criteria.

Load `references/operational-guidance.md` for deeper coverage of benchmark design, scoring, and rubrics.
