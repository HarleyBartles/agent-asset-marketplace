# Data Platform Pack

This plugin bundle projects retained ECC data/platform skills into an installable Codex marketplace pack.

## Bundle contents

- ECC data/platform skills:
  - `postgres-patterns`
  - `quality-nonconformance`
  - `scientific-db-pubmed-database`
  - `scientific-thinking-literature-review`
  - `scientific-thinking-scholar-evaluation`
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary

- `postgres-patterns` carries PostgreSQL database patterns and best practices.
- `quality-nonconformance` carries quality nonconformance handling patterns and guidance.
- `scientific-db-pubmed-database` carries PubMed database access patterns and best practices.
- `scientific-thinking-literature-review` carries scientific literature review patterns and guidance.
- `scientific-thinking-scholar-evaluation` carries scholarly evaluation patterns and guidance.
- The pack is sourced from retained `affaan-m/ECC` data/platform skills under the retained `ecc` custody root.
- The bundle does not own language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under:

- `generated/skill-zips/data-platform-pack/postgres-patterns/skill.zip`
- `generated/skill-zips/data-platform-pack/quality-nonconformance/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-db-pubmed-database/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-thinking-literature-review/skill.zip`
- `generated/skill-zips/data-platform-pack/scientific-thinking-scholar-evaluation/skill.zip`

and can be installed directly from those artifacts.
