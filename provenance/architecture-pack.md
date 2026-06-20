# Architecture Pack Provenance

## Summary

The Architecture Pack projects the MARK-172 `cqrs-event-sourcing` seed, the MARK-200 `event-driven-architecture` candidate, and the MARK-201 `database-design-patterns` candidate from the retained NickCrew/Claude-Cortex custody plugin into a Codex marketplace pack.

It also projects 8 architecture skills from the ECC (affaan-m/ECC) upstream as part of MARK-241 ECC projection.

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

### Third-Party Custody (ECC)

- **Upstream repository**: affaan-m/ECC
- **Upstream commit**: ceca28852e5b31edbbf66ebccc8fd163dd14208e
- **Source custody record**: `sources/third_party/ecc/upstream/source-custody.md`
- **Upstream manifest**: `sources/third_party/ecc/upstream/manifest.json`
- **Provenance note**: MARK-241 ECC projection
- **Projected skills**:
  - architecture-decision-records
  - backend-patterns
  - docker-patterns
  - hexagonal-architecture
  - intent-driven-development
  - kubernetes-patterns
  - mcp-server-patterns
  - mle-workflow

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

- **Upstream sources**:
  - NickCrew/Claude-Cortex (Codex Cortex skills)
  - affaan-m/ECC (ECC architecture skills)
- **License**: MIT
- **First-party selection**: MARK-172, MARK-200, and MARK-201 decision records (Codex Cortex)
- **Third-party projection**: MARK-241 ECC projection (ECC architecture skills)
- **Redistribution rights**: Per upstream license terms with first-party selection provenance and third-party custody evidence

## Boundary

Only the retained architecture skills are projected. Later Claude-Cortex candidates stay out of scope for MARK-172, MARK-200, and MARK-201. Only the 8 ECC architecture skills listed in MARK-241 are projected; other ECC skills are out of scope for this pack.