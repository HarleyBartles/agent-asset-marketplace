# OpenAI API App Development

Use this skill when you are starting an OpenAI API-backed app, choosing an API surface, or untangling app behavior before any SDK-specific framework is involved.

## What to do first

1. Decide whether the work is a single-call API flow, a tool-using workflow, or an agentic app.
2. Prefer the Responses API for direct model calls plus application-owned orchestration.
3. Move to the Agents SDK only when you need multi-step orchestration, tool routing, handoffs, or tracing as first-class runtime behavior.
4. Keep model-visible input and output contracts small and explicit.

## Build order

- Write the user task in one sentence.
- Define the payload shape before writing the prompt.
- Choose the least powerful API surface that solves the task.
- Add logs for request IDs, tool calls, and failure paths.
- Add one deterministic smoke test before broadening the feature set.

## Design checks

- If the task is mostly classification, transformation, or generation, keep the app thin and let your code own the state.
- If the task needs sequential decision-making, put the steps into an agent or a narrow tool chain.
- If the task must surface structured data, define the schema up front and validate the response at the boundary.

## Troubleshooting

- Check whether the issue is in the prompt, the tool contract, the model choice, or the app state.
- Reproduce with the smallest input that still fails.
- Compare the raw model output against the parsed or rendered result.
- If a behavior changed after a prompt edit, run the same test set before and after the change.

## Docs-first rule

- Use `openai-docs` or the live OpenAI docs when a model name, endpoint, or platform behavior may have changed.
- Do not rely on memory for current OpenAI product behavior.

