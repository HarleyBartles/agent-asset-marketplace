# Codex Cortex

This plugin bundle holds the MARK-172 `cqrs-event-sourcing` seed and the
MARK-200 `event-driven-architecture` import as the retained third-party
custody surface for the Claude-Cortex import.

## Bundle contents

- `cqrs-event-sourcing`
- `event-driven-architecture`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained source skills are kept here.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is the custody home for the imported seed, not the projection
  layer.

## Install shape

The installable skill zips are generated under
`generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip` and
`generated/skill-zips/codex-cortex/event-driven-architecture/skill.zip`, and
can be installed directly from those artifacts.
