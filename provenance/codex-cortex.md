# Codex Cortex Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Default branch: `main`
- Resolved commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: MIT

## Custody surface

- Retained snapshot root: `sources/third_party/codex-cortex/upstream/`
- First-party import ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- First-party intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/architecture-pack/`
- Generated install unit: `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`
- Generated install unit: `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`

## Boundary

The retained custody surface seeds `cqrs-event-sourcing` and
`event-driven-architecture`. `database-design-patterns` remains out of scope
for MARK-200.

