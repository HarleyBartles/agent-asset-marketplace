# Source

This plugin projects the first-party repo worker base skills only.

## Source custody
### First_Party custody
- `sources/first_party/skills/repo-worker-base/`
- `sources/first_party/skills/boring-loop/`
- `sources/first_party/skills/connector-safety/`
- `sources/first_party/skills/github-operations/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/repo-worker-base/`
- Skill root: `codex-marketplace/plugins/repo-worker-base/skills/`
- Skill roots:
  - `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/`
  - `codex-marketplace/plugins/repo-worker-base/skills/boring-loop/`
  - `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/`
  - `codex-marketplace/plugins/repo-worker-base/skills/github-operations/`

## Generated install units
- `generated/skill-zips/repo-worker-base/repo-worker-base/skill.zip`
- `generated/skill-zips/repo-worker-base/boring-loop/skill.zip`
- `generated/skill-zips/repo-worker-base/connector-safety/skill.zip`
- `generated/skill-zips/repo-worker-base/github-operations/skill.zip`

## Boundary
- Only the first-party repo worker skills are projected.
- The bundle stays narrow and does not absorb ECC workflow skills.
