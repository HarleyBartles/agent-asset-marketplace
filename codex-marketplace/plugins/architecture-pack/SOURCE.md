# Source

This plugin projects the MARK-172 `cqrs-event-sourcing` seed from the retained
Codex Cortex custody surface into a Codex marketplace pack.

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

- Codex plugin root: `codex-marketplace/plugins/architecture-pack/`
- Skill root: `codex-marketplace/plugins/architecture-pack/skills/`
- Generated install units: `generated/skill-zips/architecture-pack/<skill-name>/skill.zip`

## Boundary

Only the single seed skill is projected. Later Claude-Cortex candidates stay
out of scope for MARK-172.

