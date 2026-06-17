# Codex Cortex

This plugin bundle holds the MARK-172 `cqrs-event-sourcing` seed, the
MARK-200 `event-driven-architecture` import, the MARK-201
`database-design-patterns` import, and the MARK-204
`api-design-patterns` import as the retained third-party custody surface for
the Claude-Cortex import.

## Bundle contents

- `cqrs-event-sourcing`
- `event-driven-architecture`
- `database-design-patterns`
- `api-design-patterns`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained source skills are kept here.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is the custody home for the imported seeds, not the projection
  layer.

## Install shape

The installable skill zips are generated under
`generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip`,
`generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`,
`generated/skill-zips/codex-cortex/database-design-patterns/skill.zip`, and
`generated/skill-zips/codex-cortex/api-design-patterns/skill.zip`, and can be
installed directly from those artifacts.
