# MARK-292 PlanetScale Postgres Skill Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vendor and adapt PlanetScale's PostgreSQL skill into `data-platform-pack` as a neutral, installable marketplace skill named `postgres`, while preserving useful PostgreSQL guidance and source provenance.

**Architecture:** Keep the retained PlanetScale snapshot under `sources/third_party/planetscale/database-skills/upstream/`. Project one adapted Codex skill into `codex-marketplace/plugins/data-platform-pack/skills/postgres/`, keep the generic Postgres reference docs, and rewrite or drop the PlanetScale-specific operational docs so the marketplace skill stays neutral. Regenerate the bundle manifest, source map, generated skill zip, and provenance notes from the updated source tree.

**Tech Stack:** Markdown skill files, YAML frontmatter, existing marketplace projection scripts, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_skill_zips.py`, `py -3 tools/validate_generated_drift.py`.

## Global Constraints

- Preserve MIT license attribution to PlanetScale and keep the retained upstream snapshot pinned in source custody.
- Do not rename, replace, or otherwise disturb the existing `postgres-patterns` skill.
- Keep the new skill under the existing `data-platform-pack` bundle; do not add a new plugin root.
- The marketplace skill frontmatter must use `content_mode: adapted` and structured provenance metadata.
- Strip PlanetScale product-default copy from the marketplace projection; keep only neutral PostgreSQL guidance.
- Treat `sources/third_party/` as source custody and `codex-marketplace/plugins/` as the installable projection.
- Regenerate derived artifacts instead of hand-editing generated zips or registry entries.

### Task 1: Capture the upstream PlanetScale source snapshot

**Files:**
- Create: `sources/third_party/planetscale/database-skills/upstream/README.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/LICENSE`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/SKILL.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/backup-recovery.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/index-optimization.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/indexing.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/memory-management-ops.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/monitoring.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/mvcc-transactions.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/mvcc-vacuum.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/optimization-checklist.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/partitioning.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/pgbouncer-configuration.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/process-architecture.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-cli-api-insights.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-cli-commands.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-connection-pooling.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-connections.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-extensions.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/ps-insights.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/query-patterns.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/replication.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/schema-design.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/storage-layout.md`
- Create: `sources/third_party/planetscale/database-skills/upstream/skills/postgres/references/wal-operations.md`

**Interfaces:**
- Consumes: the public PlanetScale `database-skills` repository snapshot and license text.
- Produces: a retained third-party source tree that preserves the upstream skill and its reference files without marketplace rewriting.

- [ ] **Step 1: Pull the upstream repository content into retained source custody.**

- [ ] **Step 2: Verify the snapshot root and license path match the upstream repo and are not rewritten.**

- [ ] **Step 3: Confirm the retained tree contains the full `skills/postgres` reference set needed for later projection.**

### Task 2: Build the neutral marketplace projection in `data-platform-pack`

**Files:**
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/SKILL.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/backup-recovery.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/index-optimization.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/indexing.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/memory-management-ops.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/monitoring.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/mvcc-transactions.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/mvcc-vacuum.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/optimization-checklist.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/partitioning.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/process-architecture.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/query-patterns.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/replication.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/schema-design.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/storage-layout.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/wal-operations.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/connection-pooling.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/connection-troubleshooting.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/extensions.md`
- Create: `codex-marketplace/plugins/data-platform-pack/skills/postgres/references/query-insights.md`
- Modify: `codex-marketplace/plugins/data-platform-pack/README.md`
- Modify: `codex-marketplace/plugins/data-platform-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/data-platform-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/data-platform-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/data-platform-pack/references/source-map.md`
- Modify: `provenance/data-platform-pack.md`

**Interfaces:**
- Consumes: the retained PlanetScale source tree from Task 1 and the existing `data-platform-pack` projection conventions.
- Produces: a marketplace-ready `postgres` skill with neutral YAML frontmatter, neutralized operational references, and updated bundle/provenance metadata.

- [ ] **Step 1: Rewrite `SKILL.md` to remove PlanetScale marketing, keep the generic Postgres guidance, and point only at neutral reference docs.**

- [ ] **Step 2: Project the generic reference docs verbatim where safe, and rewrite the PlanetScale-only operational docs into neutral Postgres guidance for connection pooling, connection troubleshooting, extensions, and query insights.**

- [ ] **Step 3: Update the bundle README, source ledger, bundle manifest, source map, plugin metadata, and provenance note so the new skill is discoverable and correctly attributed.**

### Task 3: Regenerate the derived artifacts and validate the release shape

**Files:**
- Create or update: `generated/skill-zips/data-platform-pack/postgres/skill.zip`
- Update: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the updated source custody and marketplace projection from Tasks 1 and 2.
- Produces: the canonical generated zip and registry entry for the new `data-platform-pack/postgres` install artifact.

- [ ] **Step 1: Regenerate the targeted skill artifacts.**

Run: `py -3 tools/update_skill_artifacts.py --skill data-platform-pack/postgres`

- [ ] **Step 2: Validate the marketplace projection and bundle shape.**

Run: `py -3 tools/validate_marketplace.py`

- [ ] **Step 3: Validate the generated skill zips and drift state.**

Run: `py -3 tools/validate_skill_zips.py`

Run: `py -3 tools/validate_generated_drift.py`

- [ ] **Step 4: Check for accidental formatting or path drift in the working tree.**

Run: `git diff --check`

## Self-Review

- The upstream source tree is isolated under `sources/third_party/planetscale/database-skills/upstream/` and is not mixed with marketplace projection files.
- The marketplace projection keeps the new skill under `data-platform-pack` and leaves `postgres-patterns` untouched.
- The brand-specific PlanetScale docs are not carried into the marketplace surface as raw copy.
- The validation steps cover regenerated zips, marketplace metadata, and diff hygiene before any completion claim.
