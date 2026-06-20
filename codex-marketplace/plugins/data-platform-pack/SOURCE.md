# Source

This pack projects the MARK-250 ECC data/platform skills slice from retained ECC source custody into a Codex marketplace pack.

## Source custody

### ECC retained skills

- Retained upstream root: `sources/third_party/ecc/upstream/`
- Retained skill roots:
  - `sources/third_party/ecc/upstream/skills/postgres-patterns/`
  - `sources/third_party/ecc/upstream/skills/quality-nonconformance/`
  - `sources/third_party/ecc/upstream/skills/scientific-db-pubmed-database/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-literature-review/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-scholar-evaluation/`

## First-party ledgers and provenance

### ECC

- Upstream manifest: `sources/third_party/ecc/upstream/manifest.json`
- Categorization: `docs/superpowers/plans/mark-241-skill-categorization.json`
- Provenance note: `provenance/ecc.md`

## Projection surfaces

- Codex plugin root: `codex-marketplace/plugins/data-platform-pack/`
- Skill root: `codex-marketplace/plugins/data-platform-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/data-platform-pack/skills/postgres-patterns/`
  - `codex-marketplace/plugins/data-platform-pack/skills/quality-nonconformance/`
  - `codex-marketplace/plugins/data-platform-pack/skills/scientific-db-pubmed-database/`
  - `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-literature-review/`
  - `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-scholar-evaluation/`

## Generated install units

- `generated/skill-zips/data-platform-pack/postgres-patterns/skill.zip`
- `generated/skill-zips/data-platform-pack/quality-nonconformance/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-db-pubmed-database/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-thinking-literature-review/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-thinking-scholar-evaluation/skill.zip`

## Boundary

Only the retained data, database, analytics, ETL, and ML-platform guidance is kept here. The pack does not absorb language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine. The pack is a projection over retained ECC source custody, not a new source of truth.
