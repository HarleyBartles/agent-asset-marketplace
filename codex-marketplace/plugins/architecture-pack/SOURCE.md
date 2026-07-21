# Source

This plugin projects the retained Codex Cortex architecture skills plus the
first-party `database-design-patterns` skill.

## Source custody
### First-party custody
- `sources/first_party/skills/clean-architecture/`
- `sources/first_party/skills/cqrs/`
- `sources/first_party/skills/database-design-patterns/`
- `sources/first_party/skills/ddd/`
- `sources/first_party/skills/event-sourcing/`
- `sources/first_party/skills/hexagonal-architecture/`

### Retained upstream
- `NickCrew/Claude-Cortex` upstream:
  - `sources/third_party/claude-cortex/upstream/skills/cqrs-event-sourcing/`
  - `sources/third_party/claude-cortex/upstream/skills/event-driven-architecture/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/architecture-pack/`
- Skill root: `codex-marketplace/plugins/architecture-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/architecture-pack/skills/clean-architecture/`
  - `codex-marketplace/plugins/architecture-pack/skills/cqrs/`
  - `codex-marketplace/plugins/architecture-pack/skills/database-design-patterns/`
  - `codex-marketplace/plugins/architecture-pack/skills/ddd/`
  - `codex-marketplace/plugins/architecture-pack/skills/event-driven-architecture/`
  - `codex-marketplace/plugins/architecture-pack/skills/event-sourcing/`
  - `codex-marketplace/plugins/architecture-pack/skills/hexagonal-architecture/`

## Generated install units
- `generated/skill-zips/architecture-pack/clean-architecture/skill.zip`
- `generated/skill-zips/architecture-pack/cqrs/skill.zip`
- `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`
- `generated/skill-zips/architecture-pack/ddd/skill.zip`
- `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`
- `generated/skill-zips/architecture-pack/event-sourcing/skill.zip`
- `generated/skill-zips/architecture-pack/hexagonal-architecture/skill.zip`

## Boundary
- Only the retained architecture skills are projected.
- Later Claude-Cortex or ECC candidates stay out of scope until a follow-up issue rebuilds them from fresh source inspection.
- The bundle is a projection over retained source custody, not a new source of truth.
