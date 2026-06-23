# Data Platform Pack

This bundle projects the retained PlanetScale PostgreSQL skill only.

## Bundle contents
### Planetscale skills
- `postgres`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- Only the retained PostgreSQL guidance is kept here.
- The removed ECC data-platform slice is deferred to a follow-up reprojection issue with fresh source inspection and pack-by-pack design.
- The bundle is a projection over retained source custody, not a new source of truth.

## Install shape

The installable skill zips are generated under `generated/skill-zips/data-platform-pack/<skill-name>/skill.zip` and can be installed directly from those artifacts.
