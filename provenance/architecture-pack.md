# Architecture Pack Provenance

## Summary

The Architecture Pack projects first-party architecture skills and retained `NickCrew/Claude-Cortex` event-driven skills into a Codex marketplace pack.

## Source Custody

### First-Party Custody

- `sources/first_party/skills/clean-architecture/`
- `sources/first_party/skills/cqrs/`
- `sources/first_party/skills/database-design-patterns/`
- `sources/first_party/skills/ddd/`
- `sources/first_party/skills/event-sourcing/`
- `sources/first_party/skills/hexagonal-architecture/`

### Retained Upstream

- `NickCrew/Claude-Cortex` upstream:
  - `sources/third_party/claude-cortex/upstream/skills/event-driven-architecture/`

## Projection Surfaces

- `codex-marketplace/plugins/architecture-pack/skills/clean-architecture/`
- `codex-marketplace/plugins/architecture-pack/skills/cqrs/`
- `codex-marketplace/plugins/architecture-pack/skills/database-design-patterns/`
- `codex-marketplace/plugins/architecture-pack/skills/ddd/`
- `codex-marketplace/plugins/architecture-pack/skills/event-driven-architecture/`
- `codex-marketplace/plugins/architecture-pack/skills/event-sourcing/`
- `codex-marketplace/plugins/architecture-pack/skills/hexagonal-architecture/`

## Generated Install Units

- `generated/skill-zips/architecture-pack/clean-architecture/skill.zip`
- `generated/skill-zips/architecture-pack/cqrs/skill.zip`
- `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`
- `generated/skill-zips/architecture-pack/ddd/skill.zip`
- `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`
- `generated/skill-zips/architecture-pack/event-sourcing/skill.zip`
- `generated/skill-zips/architecture-pack/hexagonal-architecture/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `architecture-pack`
- **Display name**: `Architecture Pack`
- **Marketplace category**: `Productivity`
- **Content mode**:
  - `verbatim` for first-party skills
  - `verbatim` for retained upstream skills

## Rights and Attribution

- First-party skills are MIT-licensed by Harley Bartles.
- `event-driven-architecture` is used under NickCrew/Claude-Cortex MIT terms.

## Boundary

Only the retained architecture skills are projected. Later Claude-Cortex candidates stay out of scope for the current pack boundary.
