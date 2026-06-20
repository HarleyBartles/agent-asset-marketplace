# Source

This pack projects the MARK-252/255 ECC media/content skills slice from retained ECC source custody into a Codex marketplace pack.

## Source custody

### ECC retained skills

- Retained upstream root: `sources/third_party/ecc/upstream/`
- Retained skill roots:
  - `sources/third_party/ecc/upstream/skills/fal-ai-media/`
  - `sources/third_party/ecc/upstream/skills/seo/`

## First-party ledgers and provenance

### ECC

- Upstream manifest: `sources/third_party/ecc/upstream/manifest.json`
- Categorization: `docs/superpowers/plans/mark-241-skill-categorization.json`
- Provenance note: `provenance/ecc.md`

## Projection surfaces

- Codex plugin root: `codex-marketplace/plugins/media-content-pack/`
- Skill root: `codex-marketplace/plugins/media-content-pack/skills/`
- Skill roots:
  - `codex-marketplace/plugins/media-content-pack/skills/fal-ai-media/`
  - `codex-marketplace/plugins/media-content-pack/skills/seo/`

## Generated install units

- `generated/skill-zips/media-content-pack/fal-ai-media/skill.zip`
- `generated/skill-zips/media-content-pack/seo/skill.zip`

## Boundary

Only the retained media, content, document, brand, and publishing guidance is kept here. The pack does not absorb language patterns, frontend, architecture, security, repo governance, CI, or generic engineering doctrine. The pack is a projection over retained ECC source custody, not a new source of truth.
