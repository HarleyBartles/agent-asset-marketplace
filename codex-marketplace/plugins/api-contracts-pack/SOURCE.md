# Source

This plugin projects the MARK-204 `api-design-patterns` contract-doctrine slice
and the MARK-205 `openapi-specification` companion slice from the retained Codex
Cortex custody plugin into a Codex marketplace pack.

## Source custody plugin

- Plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill roots: `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/`
  and `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/`
- Source map: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/api-contracts-pack/`
- Skill root: `codex-marketplace/plugins/api-contracts-pack/skills/`
- Skill roots: `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/`
  and `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/`
- Generated install units:
  - `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`
  - `generated/skill-zips/api-contracts-pack/openapi-specification/skill.zip`

## Boundary

`api-design-patterns` remains the umbrella contract-doctrine slice. The
`openapi-specification` companion stays focused on OpenAPI syntax, schema
composition, emission, linting, and validation.
