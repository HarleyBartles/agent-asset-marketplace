# Data Platform Pack Provenance

## Summary

The Data Platform Pack now projects the first-party `database-engines` skill
into a Codex marketplace pack. The historical ECC data-platform slice and the
PlanetScale PostgreSQL skill have been removed from the active projection set;
the ECC material remains in source custody for historical record only.

## Source Custody

### Active First-Party Source

- **First-party skill root**: `sources/first_party/skills/database-engines/`
- **Vendored reference snapshots**:
  - `sources/first_party/skills/database-engines/assets/authority/reference-source/postgresql-docs/postgresql-18.4-docs.tar.gz`
  - `sources/first_party/skills/database-engines/assets/authority/reference-source/sqlite-docs/sqlite-doc-3530300.zip`
- **Authority record**: `sources/first_party/skills/database-engines/assets/authority/CITATIONS.md`
- **Source map**: `sources/first_party/skills/database-engines/assets/authority/source-map.yaml`

### Historical ECC Upstream (removed from active projection)

- **Upstream root**: `sources/third_party/ecc/upstream/`
- **Removed skill roots** (retained in source custody for historical record only):
  - `sources/third_party/ecc/upstream/skills/clickhouse-io/`
  - `sources/third_party/ecc/upstream/skills/content-hash-cache-pattern/`
  - `sources/third_party/ecc/upstream/skills/dashboard-builder/`
  - `sources/third_party/ecc/upstream/skills/kafka-integration/`
  - `sources/third_party/ecc/upstream/skills/realtime-analytics/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-literature-review/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-scholar-evaluation/`

### Historical PlanetScale Upstream (removed)

- The PlanetScale PostgreSQL skill snapshot under
  `sources/third_party/planetscale/database-skills/upstream/skills/postgres/`
  was removed from this pack's projection set. Any future PostgreSQL-first
  reprojection should start with fresh source inspection.

## Projection Surfaces

### Active Projection

- `codex-marketplace/plugins/data-platform-pack/skills/database-engines/`
- **Data Platform Pack source map**: `codex-marketplace/plugins/data-platform-pack/references/source-map.md`

### Historical Projections (no longer in active pack)

- `codex-marketplace/plugins/data-platform-pack/skills/clickhouse-io/`
- `codex-marketplace/plugins/data-platform-pack/skills/content-hash-cache-pattern/`
- `codex-marketplace/plugins/data-platform-pack/skills/dashboard-builder/`
- `codex-marketplace/plugins/data-platform-pack/skills/kafka-integration/`
- `codex-marketplace/plugins/data-platform-pack/skills/realtime-analytics/`
- `codex-marketplace/plugins/data-platform-pack/skills/postgres/`
- `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-literature-review/`
- `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-scholar-evaluation/`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `data-platform-pack`
- **Display name**: `Data Platform Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `verbatim` from first-party `database-engines` source
- **Adaptation note**: Vendored PostgreSQL and SQLite documentation archives
  are included as authority reference material. MS-SQL and MySQL are
  selectable-option citations only and are not vendored in this repository.

## Rights and Attribution

### First-Party Content

- **Author**: Harley Bartles
- **License**: MIT

### Vendored Reference Material

- PostgreSQL documentation is used under the PostgreSQL License.
- SQLite documentation is in the public domain.

### Historical ECC Content

- **Upstream source**: ECC (Enterprise Contract Copilot)
- **License**: Per ECC license terms
- **Redistribution rights**: Per upstream license terms with first-party selection provenance
- **Provenance note**: `provenance/ecc.md`

## Boundary

The active bundle focuses on first-party relational database-engine guidance
(PostgreSQL, SQLite, and selectable MS-SQL). The removed ECC slice is recorded
here for historical custody only:

- Data storage and processing (ClickHouse, Kafka, realtime analytics)
- Data visualization and dashboarding
- Scientific literature review and scholar evaluation
- Caching patterns for data-intensive applications

The PlanetScale PostgreSQL skill is no longer projected by this pack.
