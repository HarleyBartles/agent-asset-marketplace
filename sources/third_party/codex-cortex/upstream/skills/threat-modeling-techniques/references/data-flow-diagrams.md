# Data Flow Diagrams

Use DFDs to visualize how data moves through the system and where trust
boundaries change.

## DFD Elements

- External entity: user, external system, or third-party service outside the
  system boundary.
- Process: application component or function that transforms data.
- Data store: database, cache, file system, or message queue.
- Data flow: movement of data between elements.
- Trust boundary: security context change that requires validation.

## Example

```text
[User Browser] --(HTTPS Request)--> [Web Server]
        |                             |
        | (Query)                     | (SQL)
        v                             v
   [Application Server] ---------> [Database]
        |
        | (Logs)
        v
   [Audit Log Store]
```

## STRIDE Questions

- Spoofing: can an attacker pretend to be the sender?
- Tampering: can data be changed in transit or at rest?
- Repudiation: can the action be denied later?
- Information disclosure: can data leak at a boundary?
- Denial of service: can the flow be exhausted or blocked?
- Elevation of privilege: can the flow grant more access than intended?

