# Planning Pack Provenance

## Source anchor

- Upstream repository: `NickCrew/Claude-Cortex`
- Upstream commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: retained upstream license in source custody

## Custody surface

- Retained snapshot root: `sources/third_party/claude-cortex/upstream/`

## Projection surface

- Installable plugin projection: `codex-marketplace/plugins/planning-pack/`
- Generated install unit: `generated/skill-zips/requirements-discovery.zip`
- Generated install unit: `generated/skill-zips/mermaid-diagramming.zip`
- Generated install unit: `generated/skill-zips/development-estimation.zip`
- Generated install unit: `generated/skill-zips/release-prep.zip`
- Generated install unit: `generated/skill-zips/release-analysis.zip`

## Boundary

The retained custody surface seeds the exact planning skills:
`requirements-discovery`, `mermaid-diagramming`, `development-estimation`,
`release-prep`, and `release-analysis`.

These skills are imported from retained upstream custody under
`sources/third_party/claude-cortex/upstream/` and projected into
`codex-marketplace/plugins/planning-pack/` with pack-relative paths.
