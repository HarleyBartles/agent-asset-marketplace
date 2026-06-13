# Adventures Pack

This plugin bundle is the project-scoped marketplace projection for the clean
Adventures House Skills line.

## Bundle contents

- clean Adventures skills under `skills/`
- boring generic dependencies needed for project use, including `connector-safety` for safe connector/tool writes
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Projection rules

- The bundle is a projection over canonical House Skills sources, not a new
  source of truth.
- The clean active Adventures line lives in `plugins/house-skills/skills/`.
- Historical v1 imports remain historical and are not bundled as active
  inventory.
- Stage boundaries stay explicit: planning, source discovery, QA, image
  readiness, generation/editing, asset compilation, package work, and
  acceptance are separate lanes.
- `connector-safety` is included as a dependency so connector-side effects stay narrow, auditable, and recoverable.

## Provenance

- Canonical source root: `plugins/house-skills/skills`
- Bundle source ledger: `sources/house-skills/decisions.json`
- Human registry: `sources/house-skills/decisions.md`
- Structured registry mirror: `sources/house-skills/intake.json`

The copied skill docs stay in their own directories and are exposed through the
plugin manifest only after they exist locally.
