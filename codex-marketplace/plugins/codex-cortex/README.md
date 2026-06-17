# Codex Cortex

This plugin bundle holds the MARK-172 `cqrs-event-sourcing` seed as the
retained third-party custody surface for the Claude-Cortex import.

## Bundle contents

- `cqrs-event-sourcing`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the single seed skill is retained here.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is the custody home for the imported seed, not the projection
  layer.

## Install shape

The installable skill zip is generated under
`generated/skill-zips/codex-cortex/cqrs-event-sourcing/skill.zip` and can be
installed directly from that artifact.
