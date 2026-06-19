# Source

This pack projects the MARK-212 TypeScript slice and the MARK-213 Python language/runtime slice from retained Claude-Cortex source custody into a Codex marketplace pack.

## Source custody

- Retained upstream root: `sources/third_party/codex-cortex/upstream/`
- Retained skill roots:
  - `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/async-python-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/`

## First-party ledgers and provenance

- Selection/provenance ledger: `sources/first_party/skills/codex-cortex/decisions.json`
- Human-readable ledger: `sources/first_party/skills/codex-cortex/decisions.md`
- Intake record: `sources/first_party/skills/codex-cortex/intake.json`
- Provenance note: `provenance/codex-cortex.md`

## Projection surfaces

- Codex plugin root: `codex-marketplace/plugins/language-patterns-pack/`
- Skill root: `codex-marketplace/plugins/language-patterns-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-testing-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/async-python-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-performance-optimization/`

## Generated install units

- `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-testing-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/async-python-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-performance-optimization/skill.zip`

## Boundary

Only the retained TypeScript and Python language/testing/async/performance guidance is kept here. The pack does not absorb frontend, architecture, CQRS, database, security, repo governance, CI, or other non-language guidance.

The `python-testing-patterns` retained source snapshot also contains `validation/rubric.yaml`; that rubric stays in retained source custody and is not projected into the installable pack.

## Authorship

The plugin shell is authored by Harley Bartles. The projected skill roots retain their upstream source author, source license, and source path in the bundle manifest and source map so verbatim content stays attributable.
