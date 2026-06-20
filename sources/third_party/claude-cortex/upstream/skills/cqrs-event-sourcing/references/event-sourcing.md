# Reference: Event Sourcing

Event sourcing records state changes as immutable events instead of storing only
the current state.

## Event Store

- Store events in append-only order.
- Keep aggregate version numbers so optimistic concurrency can be enforced.
- Capture metadata such as correlation IDs and causation IDs.

## Snapshots

- Snapshot long event streams when replay cost grows too large.
- Rebuild the aggregate from the latest snapshot plus later events.

## Temporal Queries

- Reconstruct state at a specific point in time by replaying only events up to
  the target timestamp or version.
- Keep event timestamps and stream versions available for diagnostics and
  replay tooling.

