# Reference: Event Store Technology

This skill is storage-agnostic, but the storage choice affects operational
costs and projection strategy.

## Common Options

- EventStoreDB for a dedicated event stream database.
- Relational storage with append-only event tables.
- Framework-backed stores such as Axon, Marten, or Eventuous when the stack
  already standardizes on them.

## Selection Criteria

- append-only write support;
- optimistic concurrency checks;
- efficient stream reads;
- support for projection rebuilds;
- practical backup and restore behavior.

## Operational Concerns

- index by stream ID, type, correlation ID, and timestamp where needed;
- keep event payloads versioned;
- monitor projection lag and replay throughput.

