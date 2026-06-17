# Architecture Pack

This plugin bundle projects the MARK-172 `cqrs-event-sourcing` seed, the
MARK-200 `event-driven-architecture` candidate, and the MARK-201
`database-design-patterns` follow-on from the retained Codex Cortex custody
plugin into an installable Codex marketplace shape.

## Bundle contents

- `cqrs-event-sourcing`
- `event-driven-architecture`
- `database-design-patterns`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained architecture skills are projected.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zips are generated under
`generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip` and
`generated/skill-zips/architecture-pack/event-driven-architecture/skill.zip`,
and `generated/skill-zips/architecture-pack/database-design-patterns/skill.zip`,
and can be installed directly from those artifacts.
