# Frontend Pack Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Upstream commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: retained upstream license in source custody

## Custody surface

- Retained snapshot root: `sources/third_party/claude-cortex/upstream/`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/frontend-pack/`
- Generated install unit: `generated/skill-zips/frontend-pack/react-performance-optimization/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/accessibility-audit/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/ux-review/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/interaction-design/skill.zip`
- Generated install unit: `generated/skill-zips/frontend-pack/webapp-testing/skill.zip`

## Boundary

The retained custody surface seeds the exact MARK-214 first-wave frontend skills:
`react-performance-optimization`, `accessibility-audit`, `ux-review`,
`interaction-design`, and `webapp-testing`.

These skills are imported from retained upstream custody under
`sources/third_party/claude-cortex/upstream/` and projected into
`codex-marketplace/plugins/frontend-pack/` with pack-relative paths. Game-studio
or browser-game material is intentionally excluded from this pack boundary.
