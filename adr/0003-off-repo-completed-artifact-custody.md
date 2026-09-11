# ADR 0003: Off-repo completed-artifact custody

**Status:** Accepted

## Context

Completed planning artifacts are execution scratch. Retaining them in tracked
`completed/` trees creates a mutable historical shadow that drifts from current
source, doctrine, and issue state.

## Decision

Keep only in-flight plans, specifications, roadmaps, checkpoints, and similar
artifacts under `.agents/`. On completion, promote enduring architecture
decisions to ADRs and operating rules to current doctrine or runbooks, copy the
artifacts to disposable scratch if useful, then remove them from Git. An
optional copy may live in the central
`_agent-scratch/<repo-name>/completed/<artifact-type>/` store and may be deleted
at any time. It is not partitioned by branch. Git history is the immutable
record.

## Consequences

No tracked completed-artifact archive exists under `.agents/`.

## Current authority

`.agents/doctrine/completed-artifacts.md`, `.agents/runbooks/completing-plans.md`,
and the repo-standards completed-artifact custody convention.
