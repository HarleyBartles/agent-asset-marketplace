# Source

This plugin projects the MARK-204 `api-design-patterns` contract-doctrine slice
from the retained Codex Cortex custody plugin into a Codex marketplace pack.

## Source custody plugin

- Plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/`
- Source map: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/api-contracts-pack/`
- Skill root: `codex-marketplace/plugins/api-contracts-pack/skills/`
- Skill root: `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/`
- Generated install unit: `generated/skill-zips/api-contracts-pack/api-design-patterns/skill.zip`

## Boundary

Only the retained contract-doctrine slice is projected. The `openapi-specification`
companion slice stays out of scope for MARK-204.
