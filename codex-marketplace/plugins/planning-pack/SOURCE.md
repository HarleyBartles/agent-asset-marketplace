# Source

This plugin projects first-party planning skills into a Codex marketplace pack.

## Source custody

- First-party skill root: `sources/first_party/skills/`
- Projected skills:
  - `release-engineering`
  - `requirements-elicitation`
  - `estimation`
  - `mermaid-diagramming`

## Retained upstream custody

- Upstream repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: `MIT`
- Manifest: `sources/third_party/claude-cortex/upstream/manifest.json`
- Skill root: `sources/third_party/claude-cortex/upstream/skills/`

The retired planning skills (`requirements-discovery`, `development-estimation`,
`release-prep`, `release-analysis`) remain in retained upstream custody but are
no longer projected by this pack.

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/planning-pack/`
- Skill root: `codex-marketplace/plugins/planning-pack/skills/`
- Generated install units: `generated/skill-zips/<skill-name>.zip`

## Boundary

The pack now projects first-party planning skills. Retained upstream snapshots
are preserved for provenance but are not part of the active projection set.
