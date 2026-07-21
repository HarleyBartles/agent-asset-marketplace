# Language Patterns Pack Provenance

## Summary

The Language Patterns Pack projects the first-party `typescript` skill and retained `NickCrew/Claude-Cortex` Python language/runtime skills into a Codex marketplace pack.

## Source Custody

### First-Party Custody

- `sources/first_party/skills/typescript/`

### Retained Upstream

- **Upstream root**: `sources/third_party/claude-cortex/upstream/`
- **Retained skill roots**:
  - `sources/third_party/claude-cortex/upstream/skills/async-python-patterns/`
  - `sources/third_party/claude-cortex/upstream/skills/python-testing-patterns/`
  - `sources/third_party/claude-cortex/upstream/skills/python-performance-optimization/`

### First-Party Ledgers and Provenance

- **Selection/provenance ledger**: `sources/first_party/skills/codex-cortex/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/codex-cortex/decisions.md`
- **Intake record**: `sources/first_party/skills/codex-cortex/intake.json`
- **Provenance note**: `provenance/codex-cortex.md`

## Projection Surfaces

- **Codex plugin root**: `codex-marketplace/plugins/language-patterns-pack/`
- **Skill root**: `codex-marketplace/plugins/language-patterns-pack/skills/`
- **Skill roots**:
  - `codex-marketplace/plugins/language-patterns-pack/skills/typescript/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/async-python-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-testing-patterns/`
  - `codex-marketplace/plugins/language-patterns-pack/skills/python-performance-optimization/`

## Generated Install Units

- `generated/skill-zips/language-patterns-pack/typescript/skill.zip`
- `generated/skill-zips/language-patterns-pack/async-python-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-testing-patterns/skill.zip`
- `generated/skill-zips/language-patterns-pack/python-performance-optimization/skill.zip`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `language-patterns-pack`
- **Display name**: `Language Patterns Pack`
- **Marketplace category**: `Productivity`
- **Content mode**:
  - `verbatim` for the first-party `typescript` skill
  - `normalised` from NickCrew/Claude-Cortex custody for Python skills (metadata and path rewrites)
  - `adapted` for `python-performance-optimization` (skill-root-relative reference paths and canonical `agents/openai.yaml` metadata)

## Rights and Attribution

- `typescript` is MIT-licensed first-party content by Harley Bartles.
- Python skills are used under NickCrew/Claude-Cortex MIT terms.

## Boundary

Only the retained TypeScript and Python language/testing/async/performance guidance is kept here. The pack does not absorb frontend, architecture, CQRS, database, security, repo governance, CI, or other non-language guidance.

The `python-testing-patterns` retained source snapshot also contains `validation/rubric.yaml`; that rubric stays in retained source custody and is not projected into the installable pack.
