# Source

This plugin projects the MARK-172 `cqrs-event-sourcing` seed from the retained
Codex Cortex custody plugin into a Codex marketplace pack.

## Source custody plugin

- Plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/`
- Source map: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/architecture-pack/`
- Skill root: `codex-marketplace/plugins/architecture-pack/skills/`
- Generated install units: `generated/skill-zips/architecture-pack/<skill-name>/skill.zip`

## Boundary

Only the single seed skill is projected. Later Claude-Cortex candidates stay
out of scope for MARK-172.
