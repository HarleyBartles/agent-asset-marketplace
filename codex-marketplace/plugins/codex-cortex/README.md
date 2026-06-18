# Codex Cortex

This plugin bundle retains the MARK-172 `cqrs-event-sourcing` seed, the MARK-200
`event-driven-architecture` import, the MARK-201
`database-design-patterns` import, the MARK-204 `api-design-patterns` import,
and the MARK-205 `openapi-specification` import from Claude-Cortex.

## Bundle contents

- `cqrs-event-sourcing`
- `event-driven-architecture`
- `database-design-patterns`
- `api-design-patterns`
- `openapi-specification`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained source skills are projected.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is a custody surface, not the installable marketplace projection.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`
- `generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`
- `generated/skill-zips/codex-cortex/database-design-patterns/skill.zip`
- `generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`
- `generated/skill-zips/codex-cortex/openapi-specification/skill.zip`
