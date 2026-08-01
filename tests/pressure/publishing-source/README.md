# publishing-source pressure test

This pressure test evaluates whether the `publishing-source` skill directs an
agent to the right publication sequence when a human partner presents a source
change and asks for the fastest way to make it visible.

## Files

- `prompts/source-publication-decision.md` — pressure prompt that pits speed
  against the repo's publication proof requirement.
- `results.md` — recorded subagent response and judgment.

## Status

Completed. The agent is expected to refuse to hand-wave and instead invoke
`/publishing-source`, choose the PR sequence, and report the branch/PR URL as
publication proof.
