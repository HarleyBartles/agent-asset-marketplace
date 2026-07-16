# Architecture Pack

This bundle projects the three retained Codex Cortex architecture skills only.

## Bundle contents
### Claude Cortex skills
- `cqrs-event-sourcing`
- `database-design-patterns`
- `event-driven-architecture`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- Only the retained architecture skills from Codex Cortex are projected.
- Later Claude-Cortex or ECC candidates stay out of scope until a follow-up issue rebuilds them from fresh source inspection.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under `generated/skill-zips/architecture-pack/<skill-name>/skill.zip` and can be installed directly from those artifacts.
