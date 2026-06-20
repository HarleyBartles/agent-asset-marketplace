# Source

This plugin projects the MARK-172 `cqrs-event-sourcing` seed, the MARK-200
`event-driven-architecture` candidate, and the MARK-201
`database-design-patterns` candidate from the retained Codex Cortex custody
plugin into a Codex marketplace pack.

It also projects 8 architecture skills from the ECC (affaan-m/ECC) upstream
as part of MARK-241 ECC projection.

## Source custody plugin (Codex Cortex)

- Plugin root: `codex-marketplace/plugins/codex-cortex/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/cqrs-event-sourcing/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/event-driven-architecture/`
- Skill root: `codex-marketplace/plugins/codex-cortex/skills/database-design-patterns/`
- Source map: `codex-marketplace/plugins/codex-cortex/references/source-map.md`

## First-party custody (Codex Cortex)

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`

## Third-party custody (ECC)

- Upstream repo: https://github.com/affaan-m/ECC
- Upstream commit: ceca28852e5b31edbbf66ebccc8fd163dd14208e
- Manifest: `sources/third_party/ecc/upstream/manifest.json`
- Skill root: `sources/third_party/ecc/upstream/skills/`
- Projected skills:
  - architecture-decision-records
  - backend-patterns
  - docker-patterns
  - hexagonal-architecture
  - intent-driven-development
  - kubernetes-patterns
  - mcp-server-patterns
  - mle-workflow

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/architecture-pack/`
- Skill root: `codex-marketplace/plugins/architecture-pack/skills/`
- Generated install units: `generated/skill-zips/architecture-pack/<skill-name>/skill.zip`

## Boundary

Only the retained architecture skills are projected. Later Claude-Cortex
candidates stay out of scope for MARK-172, MARK-200, and MARK-201.
