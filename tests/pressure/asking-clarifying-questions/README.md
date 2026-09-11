# asking-clarifying-questions pressure test

This pressure test evaluates whether the `asking-clarifying-questions` skill produces a single concrete clarifying question for an ambiguous but reversible instruction, without escalating to `brainstorming` or `risk-gates`.

## Files

- `prompts/baseline-ambiguous-instruction.md` — prompt for the agent reading the skill.
- The expected behavior below is the review rubric.

## Expected behavior

The skill keeps the response to the compact queue (next action, ambiguity,
risk, recommendation/options, one question) and does not perform the rename.
Judge each run in its current handoff; do not commit the response or verdict.
