---
name: cqrs-event-sourcing
description: >
  Use when designing or reviewing CQRS and event sourcing systems that need
  auditability, temporal reconstruction, separate read and write models, or
  projection-based query handling.
keywords:
  - CQRS
  - event sourcing
  - aggregate root
  - command
  - query
  - projection
  - event store
  - temporal query
file_patterns:
  - "**/*event_bus*.*"
  - "**/cqrs/**"
  - "**/event-sourcing/**"
  - "**/eventsourcing/**"
confidence: 0.9
---

# CQRS and Event Sourcing

Use this skill for systems where:

- commands should express intent and mutate state;
- queries should read from purpose-built projections;
- event history must be preserved for replay, audit, or temporal queries;
- aggregate boundaries need to protect invariants; and
- consistency can be split between immediate local rules and eventual read-model
  updates.

## Core Model

- Commands carry intent and are validated before they reach an aggregate.
- Events are immutable facts in the past tense.
- Aggregates enforce consistency boundaries.
- Projections turn event streams into optimized read models.
- Event stores keep append-only history that can be replayed.

## When Not To Use

- simple CRUD systems with no audit or replay requirement;
- broad distributed transactions that span many aggregates;
- workflows that cannot tolerate eventual consistency in read models.

## Quick Reference

| Task | Load reference |
| --- | --- |
| CQRS command/query separation | `references/cqrs-patterns.md` |
| Event streams, snapshots, temporal reconstruction | `references/event-sourcing.md` |
| Store and infrastructure trade-offs | `references/event-store-tech.md` |
| Immediate and eventual consistency | `references/consistency-patterns.md` |
| Implementation checklist | `references/best-practices.md` |

## Workflow

1. Define the aggregate boundary that owns the invariant.
2. Write commands that express the user or system intent.
3. Emit immutable domain events in the past tense.
4. Persist events in an append-only store.
5. Build projections for the read paths that need them.
6. Verify idempotency, versioning, and replay behavior.

## Common Mistakes

- using CQRS for a trivial CRUD feature;
- making aggregates too large;
- mutating published events;
- skipping command validation;
- ignoring versioning and idempotency in handlers;
- coupling aggregates directly instead of by ID.

