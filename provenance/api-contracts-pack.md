# API Contracts Pack Provenance

## Summary

The API Contracts Pack projects the first-party `openapi-specification` skill and the retained `NickCrew/Claude-Cortex` `api-design-patterns` skill into a Codex marketplace pack.

## Source Custody

### First-Party Custody

- `sources/first_party/skills/openapi-specification/`

### Retained Upstream

- `NickCrew/Claude-Cortex` upstream: `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/`

## Projection Surfaces

- `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/`
- `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/`

## Generated Install Units

- `generated/skill-zips/openapi-specification.zip`
- `generated/skill-zips/api-design-patterns.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `api-contracts-pack`
- **Display name**: `API Contracts Pack`
- **Marketplace category**: `Productivity`
- **Content mode**:
  - `verbatim` for the first-party `openapi-specification` skill
  - `normalised` from NickCrew/Claude-Cortex custody for `api-design-patterns` (metadata and path rewrites)

## Rights and Attribution

- `openapi-specification` is MIT-licensed first-party content by Harley Bartles.
- `api-design-patterns` is used under NickCrew/Claude-Cortex MIT terms.

## Boundary

`api-design-patterns` remains the umbrella contract-doctrine slice. The `openapi-specification` companion stays focused on OpenAPI syntax, schema composition, emission, linting, and validation.
