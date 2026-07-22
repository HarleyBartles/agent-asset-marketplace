# Rooms Project Pack

Marketplace wrapper for the Rooms project pack.

## Bundle contents

### Rooms skills
- `rooms-bootstrap`
- `rooms-project-doctrine`
- `rooms-source-partitioning`
- `risk-gates`
- `rooms-character-investigation`
- `rooms-sheet-creator`
- `rooms-image-sidecars`

### Generic database guidance
- `database-design-patterns`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `cleanup-custody` stays in `repo-worker-pack`.
- `superpowers-plus` stays in its own workflow bundle.
- `unslop-plus` stays in its own pack.
- `architecture-pack` stays separate.
- The pack is intentionally narrow and project-specific.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/rooms-bootstrap.zip`
- `generated/skill-zips/rooms-project-doctrine.zip`
- `generated/skill-zips/rooms-source-partitioning.zip`
- `generated/skill-zips/risk-gates.zip`
- `generated/skill-zips/rooms-character-investigation.zip`
- `generated/skill-zips/rooms-sheet-creator.zip`
- `generated/skill-zips/rooms-image-sidecars.zip`
- `generated/skill-zips/database-design-patterns.zip`

and can be installed directly from those artifacts.
