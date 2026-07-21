# Architecture Pack

This bundle projects first-party architecture skills plus the retained Codex
Cortex `event-driven-architecture` skill.

## Bundle contents
### First-party skills
- `clean-architecture`
- `cqrs`
- `database-design-patterns`
- `ddd`
- `event-sourcing`
- `hexagonal-architecture`

### Retained upstream skills
- `event-driven-architecture` (NickCrew/Claude-Cortex)

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- Only the retained architecture skills are projected.
- Later Claude-Cortex or ECC candidates stay out of scope until a follow-up issue rebuilds them from fresh source inspection.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under `generated/skill-zips/architecture-pack/<skill-name>/skill.zip` and can be installed directly from those artifacts.
