# Source

This plugin projects the first-party repo worker base skills.

## Source custody

### First_Party custody
- `sources/first_party/skills/repo-worker-base/`
- `sources/first_party/skills/work-mode-router/`
- `sources/first_party/skills/linear-issue-shaping/`
- `sources/first_party/skills/boring-loop/`
- `sources/first_party/skills/connector-safety/`
- `sources/first_party/skills/github-operations/`
- `sources/first_party/skills/unslop-plus/`
- `sources/first_party/skills/safe-large-file-writing/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/repo-worker-base/`
- Skill root: `codex-marketplace/plugins/repo-worker-base/skills/`
- Skill roots:
  - `codex-marketplace/plugins/repo-worker-base/skills/repo-worker-base/`
  - `codex-marketplace/plugins/repo-worker-base/skills/work-mode-router/`
  - `codex-marketplace/plugins/repo-worker-base/skills/linear-issue-shaping/`
  - `codex-marketplace/plugins/repo-worker-base/skills/boring-loop/`
  - `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/`
  - `codex-marketplace/plugins/repo-worker-base/skills/github-operations/`
  - `codex-marketplace/plugins/repo-worker-base/skills/unslop-plus/`
  - `codex-marketplace/plugins/repo-worker-base/skills/safe-large-file-writing/`

## Generated install units
- `generated/skill-zips/repo-worker-base/repo-worker-base/skill.zip`
- `generated/skill-zips/repo-worker-base/work-mode-router/skill.zip`
- `generated/skill-zips/repo-worker-base/linear-issue-shaping/skill.zip`
- `generated/skill-zips/repo-worker-base/boring-loop/skill.zip`
- `generated/skill-zips/repo-worker-base/connector-safety/skill.zip`
- `generated/skill-zips/repo-worker-base/github-operations/skill.zip`
- `generated/skill-zips/repo-worker-base/unslop-plus/skill.zip`
- `generated/skill-zips/repo-worker-base/safe-large-file-writing/skill.zip`

## Boundary
- The first-party repo worker skills stay projected alongside the
  compositional repo-worker entrypoint and supporting workflow skills.
- The bundle stays narrow, first-party only, and aligns to the current eight-skill
  repo worker baseline without absorbing broader Superpowers+ or other workflow packs.
