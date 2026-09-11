# ADR 0003: Off-repo completed-plan custody

**Status:** Accepted

## Context

Completed plans are execution scratch. Retaining them in a tracked `completed/`
tree creates a mutable historical shadow that drifts from current source,
doctrine, and issue state.

## Decision

Keep only in-flight plans under `.agents/plans/`. On completion, promote any
enduring architecture decision to an ADR or current doctrine, copy the plan to
the verified off-repo cold store, then remove it from Git. Git history is the
immutable receipt; the cold store is convenience retrieval.

## Consequences

No tracked `.agents/plans/completed/` archive exists. Completed specifications
are not governed by this decision; each requires a separate durability decision.

## Current authority

`.agents/doctrine/completed-plans.md`, `.agents/runbooks/completing-plans.md`,
and the repo-standards completed-plan custody convention.
