# Language Patterns Pack Provenance

## Summary

The Language Patterns Pack projects the MARK-212 TypeScript slice and the MARK-213 Python language/runtime slice from retained Claude-Cortex source custody into a Codex marketplace pack.

## Source Custody

### Retained Upstream Root

- **Upstream root**: `sources/third_party/codex-cortex/upstream/`
- **Retained skill roots**:
  - `sources/third_party/codex-cortex/upstream/skills/typescript-advanced-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/python-testing-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/async-python-patterns/`
  - `sources/third_party/codex-cortex/upstream/skills/python-performance-optimization/`

### First-Party Ledgers and Provenance

- **Selection/provenance ledger**: `sources/first_party/skills/codex-cortex/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/codex-cortex/decisions.md`
- **Intake record**: `sources/first_party/skills/codex-cortex/intake.json`
- **Provenance note**: `provenance/codex-cortex.md`

## Projection Surfaces

- **Codex plugin root**: `codex-marketplace/plugins/language-patterns-pack/`
- **Skill root**: `codex-marketplace/plugins/language-patterns-pack/skills/`
- **Skill roots**:
  - `codex-marketplace/plugins/language-patterns-pack/skills/typescript-advanced-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-testing-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/async-python-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-performance-optimization/`

## Generated Install Units

- `generated/skill-zips/language-patterns-pack/typescript-advanced-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-testing-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/async-python-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-performance-optimization/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `language-patterns-pack`
- **Display name**: `Language Patterns Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `adapted` from Codex Cortex custody
- **Adaptation note**: Projected from retained Codex Cortex custody with first-party selection ledger

## Rights and Attribution

- **Upstream source**: Codex Cortex (OpenAI)
- **License**: Per Codex Cortex license terms
- **First-party selection**: MARK-212 and MARK-213 decision records
- **Redistribution rights**: Per upstream license terms with first-party selection provenance

## Boundary

Only the retained TypeScript and Python language/testing/async/performance guidance is kept here. The pack does not absorb frontend, architecture, CQRS, database, security, repo governance, CI, or other non-language guidance.

The `python-testing-patterns` retained source snapshot also contains `validation/rubric.yaml`; that rubric stays in retained source custody and is not projected into the installable pack.