# API Contracts Pack

This plugin bundle projects the MARK-204 `api-design-patterns` contract-doctrine
slice from the retained Codex Cortex custody plugin into an installable Codex
marketplace pack.

## Bundle contents

- `api-design-patterns`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- Only the retained contract-doctrine slice is projected.
- `openapi-specification` remains a separate MARK-205 companion slice.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zip is generated under
`generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip` and can
be installed directly from that artifact.
