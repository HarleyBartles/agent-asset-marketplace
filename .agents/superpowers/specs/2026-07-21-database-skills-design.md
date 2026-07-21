# Database skills design

**Date:** 2026-07-21
**Status:** Proposed
**Scope:** Replace the third-party PlanetScale `postgres` skill and the Claude-Cortex `database-design-patterns` skill with two first-party database skills, introduce a `skills-with-mixed-source` lane to support multiple vendored references plus clean-room citations, and migrate the existing `writing-with-clarity` skill's vendored source from `references/source/` to `assets/authority/reference-source/` for consistency.

## Problem

The marketplace currently relies on:

- A third-party PlanetScale `postgres` skill in `data-platform-pack` that carries PlanetScale-specific marketing and only covers PostgreSQL.
- A third-party Claude-Cortex `database-design-patterns` skill in `architecture-pack` and `rooms-project-pack` that is generic but not grounded in a tracked authoritative source.

There is no first-party skill that covers multiple SQL engines or cross-engine design patterns, and the existing two-lane authority model (`skills-with-source` and `skills-with-citation`) forces a choice between one vendored source and no vendored source, which is too restrictive for a multi-engine skill.

## Goals

- Deliver a first-party `database-engines` skill that treats PostgreSQL and SQLite as first-class engines, MS-SQL as a selectable option, and MySQL as a low-priority citation only.
- Deliver a first-party `database-design-patterns` skill that covers data modeling, normalization, keys/constraints, views, stored procedures, transactions/concurrency, and query-tuning fundamentals.
- Replace/retire the third-party `postgres` and `database-design-patterns` skills.
- Introduce a `skills-with-mixed-source` lane so a skill can vendor multiple licensable references while still citing non-vendorable ones.
- Migrate `writing-with-clarity` from its ad-hoc `references/source/` layout to the standard `assets/authority/reference-source/` custody shape.

## New lane: skills-with-mixed-source

`skills-with-mixed-source` extends the existing source-backed model.

- `assets/authority/reference-source/` may contain multiple vendored source snapshots, each in its own labelled subdirectory. Each snapshot is retained as the downloaded file or archive (e.g., a `.tar.gz` or `.zip` of documentation HTML, or a single PDF) to keep the recorded SHA-256 stable and reproducible.
- `authority.yaml` `authority` is a mapping of source labels to per-source authority records. Each record has the same fields as `skills-with-source` (`title`, `canonical_url`, `pinned_source_url`, `latest_check_url`, `revision`, `retrieved_at`, `content_sha256`, `license`, `license_url`).
- `authority.yaml` `decomposition.reconciled_against` and `source-map.yaml` `reconciled_against` are mappings of source labels to SHA-256 values:

  ```yaml
  reconciled_against:
    postgresql-docs: <sha256>
    sqlite-docs: <sha256>
  ```
- `assets/authority/CITATIONS.md` records the vendored sources and any non-vendored citations.
- `decomposition.references` use `content_mode: licensed_adaptation` when operational guidance is adapted from a vendored source, and `content_mode: first_party_synthesis` when the guidance is clean-room synthesis supported only by citations. For `skills-with-mixed-source`, `source_sections` entries are prefixed with the source label (e.g., `postgresql: Server Administration`, `sqlite: WAL Mode`) when the reference is derived from a vendored source.
- Existing lanes stay unchanged: `skills-with-source` continues to accept a single vendored source and a `CITATIONS.md` for supplementary references, and `skills-with-citation` continues to prohibit vendored source.
- `tools/validate_authority_assets.py` is extended to accept the new lane and validate the mapping shape.
- `mark-skill-authoring/references/source-grounded-authoring.md` and `docs/skill-standards-policy.md` are updated to document the lane.

## Skill 1: database-engines

**Lane:** `skills-with-mixed-source`
**Pack home:** `data-platform-pack` (replaces the PlanetScale `postgres` skill)

### Vendored sources

- `postgresql-docs` — `postgresql-18.4-docs.tar.gz` from <https://download.postgresql.org/pub/latest/postgresql-18.4-docs.tar.gz> (PostgreSQL License), canonical page <https://www.postgresql.org/docs/18.4/>, retained as the downloaded tarball under `reference-source/postgresql-docs/`.
- `sqlite-docs` — `sqlite-doc-3530300.zip` (SQLite 3.53.3) from <https://sqlite.org/2026/sqlite-doc-3530300.zip> (public domain), canonical page <https://sqlite.org/docs.html>, retained as the downloaded zip under `reference-source/sqlite-docs/`.

### Citations

- Microsoft SQL Server documentation (proprietary) — selectable-option citation.
- MySQL Reference Manual (Oracle proprietary) — low-priority citation only, no dedicated operational section.

### Scope

- PostgreSQL first-class: connection/drivers, schema/data types, indexing, query patterns, transactions, backups, replication.
- SQLite first-class: connection/drivers, schema/data types, indexing, query patterns, transactions, backups, WAL.
- MS-SQL selectable: engine-specific guidance when the user explicitly selects SQL Server, including T-SQL differences, tooling, and Windows/ Azure deployment notes.
- MySQL: omitted from operational guidance; retained only as a citation in `CITATIONS.md` for cases where MariaDB/MySQL semantics overlap with PostgreSQL.
- `SKILL.md` body stays under 500 words and acts as an engine-selection router.
- `agents/openai.yaml` `interface.default_prompt` asks the user which engine they are using.
- `decomposition.references` use `content_mode: licensed_adaptation` for PostgreSQL- and SQLite-derived guidance and `content_mode: first_party_synthesis` for MS-SQL/MySQL citation-backed guidance.

### Expected file targets

- `sources/first_party/skills/database-engines/SKILL.md`
- `sources/first_party/skills/database-engines/agents/openai.yaml`
- `sources/first_party/skills/database-engines/references/operational-guidance.md` (engine router and shared concepts)
- `sources/first_party/skills/database-engines/references/postgresql/*.md` (PostgreSQL-specific references)
- `sources/first_party/skills/database-engines/references/sqlite/*.md` (SQLite-specific references)
- `sources/first_party/skills/database-engines/references/mssql/*.md` (MS-SQL-specific references)
- `sources/first_party/skills/database-engines/assets/authority/authority.yaml`
- `sources/first_party/skills/database-engines/assets/authority/source-map.yaml`
- `sources/first_party/skills/database-engines/assets/authority/CITATIONS.md`
- `sources/first_party/skills/database-engines/assets/authority/reference-source/postgresql-docs/postgresql-18.4-docs.tar.gz`
- `sources/first_party/skills/database-engines/assets/authority/reference-source/sqlite-docs/sqlite-doc-3530300.zip`

### Retirement

- Remove the PlanetScale `postgres` third-party entry from `codex-marketplace/custody-pack-registry.json`.
- Remove the projected `codex-marketplace/plugins/data-platform-pack/skills/postgres/` tree.
- Remove `postgres` from any mega-pack that aggregates the `planetscale` source family. Because `postgres` is the only `planetscale` skill projected into a marketplace surface, the source family becomes empty once it is removed.
- Drain the full `sources/third_party/planetscale/database-skills/` upstream snapshot after the first-party `database-engines` skill is validated, since nothing remains projected from it.

## Skill 2: database-design-patterns

**Lane:** `skills-with-source` (single vendored source plus supplementary citations)
**Pack home:** `architecture-pack` and `rooms-project-pack` (replaces the Claude-Cortex `database-design-patterns` skill)

### Vendored source

- `database-design-2e` — *Database Design – 2nd Edition* by Adrienne Watt and Nelson Eng (BCcampus Open Textbook Project), available at <https://opentextbc.ca/dbdesign01/> and downloaded as the BCcampus PDF from <https://opentextbc.ca/dbdesign01/open/download?type=pdf>, licensed under CC BY 4.0. Retained as the downloaded PDF under `reference-source/database-design-2e/`.

### Citations

- *Use The Index, Luke* (Markus Winand, CC BY-NC-ND) for indexing and query-tuning depth.
- *Readings in Database Systems* / Red Book (Bailis / Hellerstein / Stonebraker, CC BY-NC-SA) for database architecture and history.
- PostgreSQL and SQLite documentation for engine-specific examples.

### Scope

- Data modeling: conceptual, logical, and physical models; ER and relational models.
- Normalization: functional dependencies, 1NF through 3NF and higher normal forms, decomposition.
- Keys and constraints: primary keys, foreign keys, unique constraints, check constraints, domains.
- Views, stored procedures, functions, and triggers.
- Transactions, isolation levels, concurrency, locking, and deadlock handling.
- Indexing strategy and query-plan fundamentals.
- Partitioning and sharding basics.
- `SKILL.md` body stays under 500 words and acts as a topic router.
- `decomposition.references` use `content_mode: licensed_adaptation` for topics derived from the textbook and `content_mode: first_party_synthesis` for topics built only from the supplementary citations.

### Expected file targets

- `sources/first_party/skills/database-design-patterns/SKILL.md`
- `sources/first_party/skills/database-design-patterns/agents/openai.yaml`
- `sources/first_party/skills/database-design-patterns/references/operational-guidance.md`
- `sources/first_party/skills/database-design-patterns/references/*.md` (topic-specific references)
- `sources/first_party/skills/database-design-patterns/assets/authority/authority.yaml`
- `sources/first_party/skills/database-design-patterns/assets/authority/source-map.yaml`
- `sources/first_party/skills/database-design-patterns/assets/authority/CITATIONS.md`
- `sources/first_party/skills/database-design-patterns/assets/authority/reference-source/database-design-2e/Database-Design-2nd-Edition.pdf` (exact filename recorded after download)

### Retirement

- Remove the Claude-Cortex `database-design-patterns` third-party entries from `codex-marketplace/custody-pack-registry.json` in `architecture-pack` and `rooms-project-pack`.
- Because `codex-cortex` is the mega-pack that aggregates the `claude-cortex` source family, the skill is also removed from the mega-pack projection once it is removed from the topical packs.
- Remove the `sources/third_party/claude-cortex/upstream/skills/database-design-patterns/` source directory after validation, since no pack will reference it after the replacement. The rest of the `claude-cortex` upstream snapshot remains because other skills still project from it.

## Pack and registry changes

- `codex-marketplace/custody-pack-registry.json`:
  - Remove the PlanetScale `postgres` entry from `data-platform-pack`.
  - Add the first-party `database-engines` entry to `data-platform-pack` with `source_category: first_party`, `source_family: first_party`, `content_mode: verbatim`, and `copy_expectation: byte_identical`.
  - Remove the Claude-Cortex `database-design-patterns` entry from `architecture-pack` and `rooms-project-pack`.
  - Add the first-party `database-design-patterns` entry to `architecture-pack` and `rooms-project-pack` with `source_category: first_party`, `source_family: first_party`, `content_mode: verbatim`, and `copy_expectation: byte_identical`. The `rooms-project-pack` entry keeps `lane: "Base and control plane"`.
  - `codex-cortex` is a mega-pack that aggregates the `claude-cortex` source family; it will drop `database-design-patterns` automatically once the topical entries are removed.
- Source drainage:
  - After validation, drain `sources/third_party/planetscale/database-skills/` because no `planetscale` skill will be projected.
  - After validation, drain `sources/third_party/claude-cortex/upstream/skills/database-design-patterns/` because the first-party skill replaces all projections.
- `codex-marketplace/plugin-roots.json`: no change.
- `.agents/plugins/marketplace.json`: no change to plugin roots; `data-platform-pack` and `architecture-pack` remain `AVAILABLE`.

## Consistency cleanup: writing-with-clarity

The `writing-with-clarity` skill currently vendors its public-domain historical source as `references/source/elements-of-style-1918.html` with a manual `references/source/source-map.md`. This is the only first-party skill that does not follow the `assets/authority/reference-source/` convention.

### Migration

- Move `references/source/elements-of-style-1918.html` to `assets/authority/reference-source/elements-of-style-1918.html`.
- Add `assets/authority/authority.yaml` with `lane: skills-with-source` and the upstream custody record.
- Add `assets/authority/source-map.yaml` mapping each operational reference to the relevant rules/chapters in the historical source.
- Add `assets/authority/CITATIONS.md` with the public-domain authority record.
- Remove `references/source/source-map.md` and the `references/source/` directory.
- Update `SKILL.md` to point to `assets/authority/reference-source/` and `assets/authority/source-map.md` instead of `references/source/`.

### Expected file targets

- `sources/first_party/skills/writing-with-clarity/assets/authority/authority.yaml`
- `sources/first_party/skills/writing-with-clarity/assets/authority/source-map.yaml`
- `sources/first_party/skills/writing-with-clarity/assets/authority/CITATIONS.md`
- `sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918.html`
- `sources/first_party/skills/writing-with-clarity/SKILL.md` (source pointer updates)
- Remove `sources/first_party/skills/writing-with-clarity/references/source/`

## Validation

- `py -3 tools/validate_authority_assets.py` must pass for `database-engines`, `database-design-patterns`, and `writing-with-clarity`.
- `py -3 tools/rebuild_marketplace.py` regenerates all derived surfaces.
- `py -3 tools/check_marketplace.py` must pass.
- `py -3 tools/install_agent_skills.py --check` reports no unexpected drift.

## Out of scope

- MongoDB and other document/NoSQL databases (explicitly excluded).
- Vendor-specific cloud-managed service operations (e.g., RDS provisioning, Azure SQL Elastic Pool tuning) beyond engine selection.
- Full source code of database engines.
- MySQL as a first-class engine.
