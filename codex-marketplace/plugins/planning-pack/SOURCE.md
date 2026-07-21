# Source

This plugin projects 5 planning-related skills from the retained Claude-Cortex
custody root into a Codex marketplace pack.

## Source custody (Claude-Cortex)

- Upstream repo: `NickCrew/Claude-Cortex`
- URL: <https://github.com/NickCrew/Claude-Cortex.git>
- Pinned commit: `7892d00e7cb6adf00144a535103b930c772fb2c0`
- License: `MIT`
- Manifest: `sources/third_party/claude-cortex/upstream/manifest.json`
- Skill root: `sources/third_party/claude-cortex/upstream/skills/`
- Projected skills:
  - requirements-discovery
  - mermaid-diagramming
  - development-estimation
  - release-prep
  - release-analysis

## Pack shape

- Codex plugin root: `codex-marketplace/plugins/planning-pack/`
- Skill root: `codex-marketplace/plugins/planning-pack/skills/`
- Generated install units: `generated/skill-zips/<skill-name>.zip`

## Boundary

Only the retained planning skills are projected. Later Claude-Cortex candidates
stay out of scope.
