# Source

This plugin is the MARK-172 and MARK-200 Codex Cortex custody surface for the
retained Claude-Cortex `cqrs-event-sourcing` seed and
`event-driven-architecture` import.

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
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/`
- Generated install units: `generated/skill-zips/codex-cortex/<skill-name>/skill.zip`

## Boundary

Only the retained source skills are kept here. Later Claude-Cortex candidates
stay out of scope for MARK-172 and MARK-200.
