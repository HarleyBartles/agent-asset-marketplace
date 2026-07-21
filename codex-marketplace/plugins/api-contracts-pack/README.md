# API Contracts Pack

This plugin bundle projects the MARK-204 `api-design-patterns` contract-doctrine
slice and the MARK-205 `openapi-specification` companion slice from the retained
Codex Cortex custody plugin into an installable Codex marketplace pack.

## Bundle contents

- `api-design-patterns`
- `openapi-specification`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `api-design-patterns` carries the umbrella contract doctrine.
- `openapi-specification` carries the OpenAPI-specific companion slice.
- The bundle is a projection over retained source custody, not a new source of
  truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/api-design-patterns.zip`
- `generated/skill-zips/openapi-specification.zip`
