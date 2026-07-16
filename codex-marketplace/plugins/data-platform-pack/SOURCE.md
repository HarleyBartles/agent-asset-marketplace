# Source

This plugin projects the retained PlanetScale PostgreSQL skill only.

## Source custody
### Planetscale custody
- `sources/third_party/planetscale/database-skills/upstream/skills/postgres/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/data-platform-pack/`
- Skill root: `codex-marketplace/plugins/data-platform-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/data-platform-pack/skills/postgres/`

## Generated install units
- `generated/skill-zips/data-platform-pack/postgres/skill.zip`

## Boundary
- Only the retained PostgreSQL guidance is kept here.
- The removed ECC data-platform slice is deferred to a follow-up reprojection issue with fresh source inspection and pack-by-pack design.
- The bundle is a projection over retained source custody, not a new source of truth.
