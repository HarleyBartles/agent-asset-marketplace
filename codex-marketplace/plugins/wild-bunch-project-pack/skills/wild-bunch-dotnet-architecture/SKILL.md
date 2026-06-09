---
name: wild-bunch-dotnet-architecture
description: Apply Wild Bunch .NET architecture guardrails for domain ownership, persistence, CQRS, and snapshots.
---

# Wild Bunch .NET Architecture

## Overview

Use this skill for structure decisions in the C#/.NET codebase. Protect the
domain first, keep application code as orchestration, and persist runtime state
in a shape that matches the live session model.

## Rules

- The domain owns rules and invariants.
- The application or use-case layer coordinates commands and queries but does
  not become the source of domain truth.
- Infrastructure persists snapshots or read models and should not leak
  framework objects into the domain.
- Persist runtime session state as strongly typed aggregate state suitable for
  JSON snapshots unless the issue explicitly says otherwise.
- Do not normalize live session runtime state into many database tables too
  early.
- Static content, read models, projections, editor or admin needs, and
  cross-session data may justify tables later.
- CQRS is allowed as a read/write separation tool, not a mandate to split
  everything.
- Event-sourcing concepts may inform audit or replay thinking, but do not
  convert persistence to full event sourcing unless the issue scopes it.
- Onion or clean architecture only matters when it protects domain rules from
  UI, database, or framework leakage.

## References

- [Wild Bunch .NET architecture notes](references/dotnet-architecture.md)
