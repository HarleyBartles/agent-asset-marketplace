# ADR 0002: Derived agent-mesh navigation

**Status:** Accepted

## Context

Agent-facing surfaces need discoverable navigation, but hand-maintained index
files drift as the repository changes.

## Decision

The repository generates `INDEX.md` mesh navigation and JSON index sidecars
from the live tree. Index output is derived and must be refreshed after
structure changes rather than edited as a parallel source of truth.

## Consequences

Adding, moving, or removing governed files requires mesh regeneration and index
validation. Navigation files do not preserve historical plan archives.

## Current authority

`.agents/doctrine/mesh-policy.md` and the canonical mesh generator.

## Historical origin context

Completed plans `2026-07-12-agents-mesh-discoverability.md` and
`2026-08-09-zone-index-json-sidecars-phase-1.md`.
