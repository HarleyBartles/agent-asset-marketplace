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

## Boundary

The retained custody surface only seeds `cqrs-event-sourcing`. Later Claude-
Cortex candidates such as `event-driven-architecture` and
`database-design-patterns` remain out of scope for MARK-172.

