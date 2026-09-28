# Agent Evaluation operational guidance

## When to apply

Use when the agent-evaluation skill is loaded and the task requires evaluating agent outputs, designing benchmarks, or building self-evaluation rubrics.

## Benchmark design

1. Choose tasks that match the real deployment distribution, not only easy positives.
2. Define pass/fail criteria before running the evaluation; avoid moving the goalposts after seeing results.
3. Use containerized or reproducible environments so scores are comparable across runs.

## Scoring agent outputs

1. Score end outcomes, not intermediate text length or politeness.
2. Compare outputs against a rubric or reference solution, not just model self-ratings.
3. Report confidence intervals and failure modes alongside headline metrics.

## Self-evaluation rubrics

1. Rate each dimension separately: correctness, completeness, safety, concision.
2. Use a 0-1 or 0-4 scale with concrete anchors, not adjectives.
3. Require the agent to quote evidence for each score and cite sources.

## Common mistakes

- Reporting a single aggregate score without task-level breakdown. → Report per-task and per-dimension results.
- Letting the evaluator share weights with the evaluated model. → Separate evaluation harness and scorer.
- Reusing the test set as a development target. → Hold out a final evaluation set.

## Related references

- SWE-bench: https://github.com/SWE-bench/SWE-bench
- SWE-bench paper: https://arxiv.org/abs/2310.06770
- MLCommons AILuminate Agentic: https://mlcommons.org/ailuminate/agentic/
- OpenAI Evals: https://github.com/openai/evals
