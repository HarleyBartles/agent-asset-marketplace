# Source

This plugin projects the mixed Superpowers+ workflow and routing helpers.

## Source custody
### House Skills custody
- `sources/first_party/skills/inspecting-the-environment/`

### Superpowers custody
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/brainstorming/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/dispatching-parallel-agents/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/executing-plans/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/finishing-a-development-branch/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/receiving-code-review/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/requesting-code-review/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/subagent-driven-development/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/systematic-debugging/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/test-driven-development/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/using-git-worktrees/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/using-superpowers/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/verification-before-completion/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/writing-plans/`
- `sources/third_party/superpowers/obra-superpowers/v6.1.0/skills/writing-skills/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/superpowers-plus/`
- Skill root: `codex-marketplace/plugins/superpowers-plus/skills/`
- Skill roots:
  - `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/`
  - `codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/`
  - `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/`
  - `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/`
  - `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/`
  - `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/`
  - `codex-marketplace/plugins/superpowers-plus/skills/requesting-code-review/`
  - `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/`
  - `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/`
  - `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/`
  - `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/`
  - `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/`
  - `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/`

## Generated install units
- `generated/skill-zips/brainstorming.zip`
- `generated/skill-zips/dispatching-parallel-agents.zip`
- `generated/skill-zips/executing-plans.zip`
- `generated/skill-zips/finishing-a-development-branch.zip`
- `generated/skill-zips/inspecting-the-environment.zip`
- `generated/skill-zips/receiving-code-review.zip`
- `generated/skill-zips/requesting-code-review.zip`
- `generated/skill-zips/subagent-driven-development.zip`
- `generated/skill-zips/systematic-debugging.zip`
- `generated/skill-zips/test-driven-development.zip`
- `generated/skill-zips/using-git-worktrees.zip`
- `generated/skill-zips/using-superpowers.zip`
- `generated/skill-zips/verification-before-completion.zip`
- `generated/skill-zips/writing-plans.zip`
- `generated/skill-zips/writing-skills.zip`

## Boundary
- This bundle mixes first-party helpers, retained third-party Superpowers skills, and adapter-backed projections.
- `superpowers-plus` is the retained mixed projection-lane bundle for this source family.
- `codex-marketplace/custody-pack-registry.json` determines whether any Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is not a maintained active marketplace bundle.
