# Completing planning artifacts

Use this runbook when an implementation PR completes an in-flight plan,
specification, roadmap, checkpoint, or similar planning artifact.
It defines this repository's custody steps; portable workflow method belongs to
the routed completion skill.

## Completion boundary

Keep in-flight artifacts committed while they govern implementation and review.
Before removing them, promote any decision
that still constrains repository architecture to `adr/`, and any operating rule
to current doctrine or a runbook. Do not use a completed artifact as a durable
record of either.

## Removal

Remove the exact tracked artifacts with Git-aware deletion, regenerate the
mesh, and commit the resulting tree in the completing PR. If a convenience
copy is useful during closeout, place it under the central
`_agent-scratch/<repo-name>/completed/<artifact-type>/` store. This centralized,
disposable location is the only scratch custody for finished paperwork; making
a copy is optional and proves nothing.

## Evidence

Git history is the immutable record. Completion creates no manifest, count,
archive index, or recurring PR-reporting duty.
