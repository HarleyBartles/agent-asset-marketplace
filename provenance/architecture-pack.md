# Architecture Pack Provenance

## Summary

The Architecture Pack projects the MARK-172 `cqrs-event-sourcing` seed, the MARK-200 `event-driven-architecture` candidate, and the MARK-201 `database-design-patterns` candidate from the retained NickCrew/Claude-Cortex custody plugin into a Codex marketplace pack.

## Source Custody

### Source Custody Plugin

- **Plugin root**: `codex-marketplace/plugins/codex-cortex/`
- **Skill roots**:
  - `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/`
  - `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/`
  - `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/`
- **Source map**: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

### First-Party Custody

- **Selection/provenance ledger**: `sources/first_party/skills/codex-cortex/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/codex-cortex/decisions.md`
- **Intake record**: `sources/first_party/skills/codex-cortex/intake.json`
- **Provenance note**: `provenance/codex-cortex.md`

## Pack Shape

- **Codex plugin root**: `codex-marketplace/plugins/architecture-pack/`
- **Skill root**: `codex-marketplace/plugins/architecture-pack/skills/`
- **Generated install units**: `generated/skill-zips/architecture-pack/<skill-name>/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `architecture-pack`
- **Display name**: `Architecture Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `adapted` from NickCrew/Claude-Cortex custody
- **Adaptation note**: Projected from retained NickCrew/Claude-Cortex custody with first-party selection ledger

## Rights and Attribution

- **Upstream source**: NickCrew/Claude-Cortex
- **License**: MIT
- **First-party selection**: MARK-172, MARK-200, and MARK-201 decision records
- **Redistribution rights**: Per upstream license terms with first-party selection provenance

## Boundary

Only the retained architecture skills are projected. Later Claude-Cortex candidates stay out of scope for MARK-172, MARK-200, and MARK-201.