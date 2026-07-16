# Source

This plugin projects the three retained Codex Cortex architecture skills only.

## Source custody
### Claude Cortex custody
- `sources/third_party/claude-cortex/upstream/skills/cqrs-event-sourcing/`
- `sources/third_party/claude-cortex/upstream/skills/database-design-patterns/`
- `sources/third_party/claude-cortex/upstream/skills/event-driven-architecture/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/architecture-pack/`
- Skill root: `codex-marketplace/plugins/architecture-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/architecture-pack/skills/cqrs-event-sourcing/`
  - `codex-marketplace/plugins/architecture-pack/skills/database-design-patterns/`
  - `codex-marketplace/plugins/architecture-pack/skills/event-driven-architecture/`

## Generated install units
- `generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`
- `generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`

## Boundary
- Only the retained architecture skills from Codex Cortex are projected.
- Later Claude-Cortex or ECC candidates stay out of scope until a follow-up issue rebuilds them from fresh source inspection.
- The bundle is a projection over retained source custody, not a new source of truth.
