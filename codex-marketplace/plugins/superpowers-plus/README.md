# Superpowers+

This bundle projects the mixed Superpowers+ workflow and routing helpers.

## Bundle contents
### House Skills skills
- `inspecting-the-environment`

### Superpowers skills
- `brainstorming`
- `dispatching-parallel-agents`
- `executing-plans`
- `finishing-a-development-branch`
- `receiving-code-review`
- `requesting-code-review`
- `subagent-driven-development`
- `systematic-debugging`
- `test-driven-development`
- `using-git-worktrees`
- `using-superpowers`
- `verification-before-completion`
- `writing-plans`
- `writing-skills`

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- This bundle mixes first-party helpers, retained third-party Superpowers skills, and adapter-backed projections.
- `superpowers-plus` is the retained mixed projection-lane bundle for this source family.
- `codex-marketplace/custody-pack-registry.json` determines whether any Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is not a maintained active marketplace bundle.

## Install shape

The installable skill zips are generated under `generated/skill-zips/superpowers-plus/<skill-name>/skill.zip` and can be installed directly from those artifacts.
