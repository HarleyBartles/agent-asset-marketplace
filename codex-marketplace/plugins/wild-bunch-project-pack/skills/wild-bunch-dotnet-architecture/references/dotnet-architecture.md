# .NET Architecture Notes

- Let the domain own rules and invariants.
- Use the application layer for command/query orchestration.
- Keep infrastructure responsible for persistence details and read models.
- Favor strongly typed aggregate snapshots that serialize cleanly to JSON for
  live session state.
- Do not prematurely fan the runtime state out into many tables.
- Add tables later when static content, projections, admin needs, or
  cross-session data justify them.
- Use CQRS when it helps separate reads from writes; do not make it a blanket
  requirement.
- Treat event-sourcing concepts as guidance for replay and audit, not as a
  default persistence mandate.
- Apply onion or clean architecture only insofar as it keeps framework leakage
  out of the domain.
