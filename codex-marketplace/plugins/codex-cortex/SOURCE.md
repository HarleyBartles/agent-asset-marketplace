# Source

This plugin is the MARK-172, MARK-200, MARK-201, MARK-204, MARK-205, and
MARK-210 Codex Cortex custody surface for the retained Claude-Cortex
`cqrs-event-sourcing` seed, `event-driven-architecture` import,
`database-design-patterns` import, `api-design-patterns` import,
`openapi-specification` import, and `threat-modeling-techniques` import.

## Upstream basis

- Repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: `MIT`
- Retained snapshot root: `sources/third_party/codex-cortex/upstream/`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/api-design-patterns/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/openapi-specification/`
- Skill root:
  `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/`
- Generated install units: `generated/skill-zips/codex-cortex/<skill-name>/skill.zip`

## Boundary

Only the retained source skills are kept here. Later Claude-Cortex candidates
stay out of scope for MARK-172, MARK-200, MARK-201, MARK-204, MARK-205, and
MARK-210.
