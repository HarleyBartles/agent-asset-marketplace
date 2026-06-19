# API Contracts Pack Provenance

## Summary

The API Contracts Pack projects the MARK-204 `api-design-patterns` contract-doctrine slice and the MARK-205 `openapi-specification` companion slice from the retained NickCrew/Claude-Cortex custody plugin into a Codex marketplace pack.

## Source Custody

### Source Custody Plugin

- **Plugin root**: `codex-marketplace/plugins/codex-cortex/`
- **Skill roots**: 
  - `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/`
  - `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/`
- **Source map**: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

### First-Party Custody

- **Selection/provenance ledger**: `sources/first_party/skills/codex-cortex/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/codex-cortex/decisions.md`
- **Intake record**: `sources/first_party/skills/codex-cortex/intake.json`
- **Provenance note**: `provenance/codex-cortex.md`

## Pack Shape

- **Codex plugin root**: `codex-marketplace/plugins/api-contracts-pack/`
- **Skill root**: `codex-marketplace/plugins/api-contracts-pack/skills/`
- **Skill roots**:
  - `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/`
  - `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/`
- **Generated install units**:
  - `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`
  - `generated/skill-zips/api-contracts-pack/openapi-specification/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `api-contracts-pack`
- **Display name**: `API Contracts Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `adapted` from NickCrew/Claude-Cortex custody
- **Adaptation note**: Projected from retained NickCrew/Claude-Cortex custody with first-party selection ledger

## Rights and Attribution

- **Upstream source**: NickCrew/Claude-Cortex
- **License**: MIT
- **First-party selection**: MARK-204 and MARK-205 decision records
- **Redistribution rights**: Per upstream license terms with first-party selection provenance

## Boundary

`api-design-patterns` remains the umbrella contract-doctrine slice. The `openapi-specification` companion stays focused on OpenAPI syntax, schema composition, emission, linting, and validation.