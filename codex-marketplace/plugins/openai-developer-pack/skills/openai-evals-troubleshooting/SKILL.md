# OpenAI Evals and Troubleshooting

Use this skill when model quality drifts, a prompt regresses, tool behavior is inconsistent, or you need a repeatable way to compare changes.

## Workflow

1. Reproduce the failure with the smallest stable test case.
2. Decide whether the defect is in the prompt, the tool contract, the model choice, or the app state.
3. Capture a baseline before changing anything.
4. Add an eval, dataset, or trace-based check that reflects the real failure mode.
5. Change one thing, rerun the same checks, and compare.

## What to measure

- Correctness against the task
- Structured output validity
- Tool-selection accuracy
- Recovery behavior after errors
- Regression rate after prompt or code changes

## Troubleshooting pattern

- If the model is answering but not acting, inspect the tool schema and tool descriptions.
- If the output is shaped incorrectly, inspect the parser or schema validator.
- If the issue only appears on one class of inputs, add a focused eval slice for that class.
- If tracing shows repeated retries or dead ends, simplify the instructions before adding more control logic.

## Current OpenAI guidance

- Use traces early when you are still debugging workflow behavior.
- Use datasets or evals when you need repeatable comparisons.
- Check the live OpenAI docs before choosing a specific evaluation surface, because the platform guidance can change.

