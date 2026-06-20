# Architecture Pack

This plugin bundle projects the MARK-172 `cqrs-event-sourcing` seed, the
MARK-200 `event-driven-architecture` candidate, and the MARK-201
`database-design-patterns` follow-on from the retained Codex Cortex custody
plugin into an installable Codex marketplace shape.

It also projects 8 architecture skills from the ECC (affaan-m/ECC) upstream
as part of MARK-241 ECC projection.

## Bundle contents

### Codex Cortex skills
- `cqrs-event-sourcing`
- `event-driven-architecture`
- `database-design-patterns`

### ECC skills (MARK-241)
- `architecture-decision-records`
- `backend-patterns`
- `docker-patterns`
- `hexagonal-architecture`
- `intent-driven-development`
- `kubernetes-patterns`
- `mcp-server-patterns`
- `mle-workflow`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained architecture skills from Codex Cortex and the categorized
  architecture skills from ECC are projected.
- Later Claude-Cortex candidates stay out of scope.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zips are generated under
`generated/skill-zips/architecture-pack/<skill-name>/skill.zip`
and can be installed directly from those artifacts.
