# Architecture Pack

This plugin bundle projects the MARK-172 `cqrs-event-sourcing` seed from the
retained Codex Cortex custody plugin into an installable Codex marketplace
shape.

## Bundle contents

- `cqrs-event-sourcing`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the single seed skill is projected.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zip is generated under
`generated/skill-zips/architecture-pack/cqrs-event-sourcing/skill.zip` and can
be installed directly from that artifact.
