# Engineering Pack

This bundle projects first-party engineering skills into a focused topical
home.

## Bundle contents

### First-party skills
- `release-engineering`
- `observability`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- The pack covers implementation flow, release readiness, deployment patterns, and observability.
- `release-engineering` and `observability` are projected from first-party source custody.
- `ai-first-engineering` has been removed from the active projection set; the ECC
  upstream snapshot remains in `sources/third_party/ecc/upstream/skills/ai-first-engineering/`.
- The pack stays out of workflow dispatch, research, and security homes.

## Install shape

The installable skill zips are generated under
`generated/skill-zips/<skill-name>.zip` and can be
installed directly from those artifacts.
