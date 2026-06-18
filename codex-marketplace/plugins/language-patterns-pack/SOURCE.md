# Source

This plugin projects the MARK-212 `typescript-advanced-patterns` slice from the
retained Claude-Cortex custody plugin into a Codex marketplace pack.

## Source custody plugin

- Plugin root: `sources/third_party/codex-cortex/upstream/`
- Skill root:
  `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/`

## First-party custody

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`
- Provenance note: `provenance/codex-cortex.md`

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/language-patterns-pack/`
- Skill root: `codex-marketplace/plugins/language-patterns-pack/skills/`
- Skill root:
  `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/`
- Generated install unit:
  `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`

## Boundary

Only the retained TypeScript language/runtime guidance is kept here. The pack
does not absorb React or frontend-architecture doctrine, CQRS, database,
security, or other non-language guidance.
