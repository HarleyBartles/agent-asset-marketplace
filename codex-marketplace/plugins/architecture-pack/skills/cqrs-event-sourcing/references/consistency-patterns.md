# Reference: Consistency Patterns

CQRS and event sourcing usually combine immediate consistency inside an
aggregate with eventual consistency across aggregates.

## Immediate Consistency

- Enforce invariants inside a single aggregate transaction.
- Reject invalid commands before new events are emitted.

## Eventual Consistency

- Use process managers or sagas to coordinate cross-aggregate workflows.
- Treat read models as derived state that may lag behind the event stream.

## Coordination

- Keep compensating actions explicit.
- Make handlers idempotent.
- Avoid direct aggregate-to-aggregate mutation.

