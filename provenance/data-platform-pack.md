# Data Platform Pack Provenance

## Summary

The Data Platform Pack historically projected retained ECC data platform and scientific thinking skills into a Codex marketplace pack, plus an adapted PlanetScale PostgreSQL skill. MARK-295 removed the active ECC slice and left the PlanetScale skill in place.

## Source Custody

### Historical ECC Upstream

- **Upstream root**: `sources/third_party/ecc/upstream/`
- **Retained skill roots**:
  - `sources/third_party/ecc/upstream/skills/clickhouse-io/`
  - `sources/third_party/ecc/upstream/skills/content-hash-cache-pattern/`
  - `sources/third_party/ecc/upstream/skills/dashboard-builder/`
  - `sources/third_party/ecc/upstream/skills/kafka-integration/`
  - `sources/third_party/ecc/upstream/skills/realtime-analytics/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-literature-review/`
  - `sources/third_party/ecc/upstream/skills/scientific-thinking-scholar-evaluation/`
- **Retained PlanetScale upstream**:
  - `sources/third_party/planetscale/database-skills/upstream/skills/postgres/`

### First-Party Ledgers

- **Selection/provenance ledger**: `sources/first_party/skills/ecc/decisions.json`
- **Human-readable ledger**: `sources/first_party/skills/ecc/decisions.md`
- **Intake record**: `sources/first_party/skills/ecc/intake.json`
- **Provenance notes**:
  - `provenance/ecc.md`

## Projection Surfaces

### Historical ECC Projection

- `codex-marketplace/plugins/data-platform-pack/skills/clickhouse-io/`
- `codex-marketplace/plugins/data-platform-pack/skills/content-hash-cache-pattern/`
- `codex-marketplace/plugins/data-platform-pack/skills/dashboard-builder/`
- `codex-marketplace/plugins/data-platform-pack/skills/kafka-integration/`
- `codex-marketplace/plugins/data-platform-pack/skills/realtime-analytics/`
- `codex-marketplace/plugins/data-platform-pack/skills/postgres/`
- `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-literature-review/`
- `codex-marketplace/plugins/data-platform-pack/skills/scientific-thinking-scholar-evaluation/`

- **Data Platform Pack source map**: `codex-marketplace/plugins/data-platform-pack/references/source-map.md`

## Marketplace Adaptation

- **Status**: `projected`
- **Plugin name**: `data-platform-pack`
- **Display name**: `Data Platform Pack`
- **Marketplace category**: `Productivity`
- **Content mode**: `historical verbatim` from ECC custody; `adapted` for PlanetScale Postgres
- **Adaptation note**: The ECC slice was removed in MARK-295; the remaining PlanetScale overlay stays in place

## Rights and Attribution

### Historical ECC Content

- **Upstream source**: ECC (Enterprise Contract Copilot)
- **License**: Per ECC license terms
- **Redistribution rights**: Per upstream license terms with first-party selection provenance
- **Provenance note**: `provenance/ecc.md`

## Boundary

The bundle now focuses on the retained PlanetScale PostgreSQL skill; the removed ECC slice is recorded here for historical custody only:
- Data storage and processing (ClickHouse, Kafka, realtime analytics)
- Data visualization and dashboarding
- Scientific literature review and scholar evaluation
- Caching patterns for data-intensive applications
