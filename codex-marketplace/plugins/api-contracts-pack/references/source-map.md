# API Contracts Pack Source Map

This bundle projects the MARK-204 `api-design-patterns` contract-doctrine
slice and the MARK-205 `openapi-specification` companion slice from the retained
Codex Cortex custody plugin into a marketplace surface.

Retained custody evidence:

- `sources/third_party/claude-cortex/upstream/README.md`
- `sources/third_party/claude-cortex/upstream/LICENSE`
- `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/references/design-process.md`
- `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/validation/rubric.yaml`
- `sources/third_party/claude-cortex/upstream/skills/openapi-specification/SKILL.md`
- `sources/third_party/claude-cortex/upstream/skills/openapi-specification/references/spec-patterns.md`
- `sources/third_party/claude-cortex/upstream/skills/openapi-specification/validation/rubric.yaml`

First-party custody:

- `sources/first_party/skills/codex-cortex/intake.json`
- `sources/first_party/skills/codex-cortex/decisions.json`
- `sources/first_party/skills/codex-cortex/decisions.md`
- `provenance/codex-cortex.md`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| api-design-patterns | `sources/third_party/claude-cortex/upstream/skills/api-design-patterns/SKILL.md` | `codex-marketplace/plugins/api-contracts-pack/skills/api-design-patterns/SKILL.md` | Adapted from the retained Codex Cortex custody plugin into the installable API Contracts Pack. |
| openapi-specification | `sources/third_party/claude-cortex/upstream/skills/openapi-specification/SKILL.md` | `codex-marketplace/plugins/api-contracts-pack/skills/openapi-specification/SKILL.md` | Adapted as the OpenAPI-specific companion slice and composed with `api-design-patterns`. |

The pack root is an installable Codex plugin projection. It does not replace the
`codex-cortex` custody plugin or the first-party import ledger.
