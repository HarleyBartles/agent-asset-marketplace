# Reference: Best Practices

## Command Design

- express intent, not technical operations;
- validate before mutation;
- keep commands immutable;
- include correlation metadata when it matters;
- support idempotency.

## Event Design

- use past-tense event names;
- never modify published events;
- include the data consumers need;
- plan for schema evolution;
- keep events focused.

## Projection Design

- denormalize for the query being answered;
- make handlers idempotent;
- track the last processed version;
- support rebuilds from the event stream.

## Event Store Management

- append only;
- snapshot long streams when useful;
- index for stream and replay access;
- watch for lag and replay errors.

