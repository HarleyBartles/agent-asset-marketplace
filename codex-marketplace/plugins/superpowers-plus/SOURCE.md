# Source

This plugin projects the first-party Superpowers+ workflow skills, including the `using-superpowers-plus` workflow-selection entrypoint.

## Upstream Basis

- Repo: `obra/superpowers`
- URL: <https://github.com/obra/superpowers>
- Retained snapshot: `sources/third_party/superpowers/obra-superpowers/v6.2.0/`
- License: `MIT`
- The retained upstream snapshot is reference-only. The editable first-party
  skills live under `sources/first_party/skills/<name>/` and are the source of
  truth for projection. No adapter overlay is applied.

## First-Party Source Custody
<!-- BEGIN GENERATED: pack-inventory -->
## Source custody
### First Party custody
- `sources/first_party/skills/brainstorming/`
- `sources/first_party/skills/dispatching-parallel-agents/`
- `sources/first_party/skills/executing-plans/`
- `sources/first_party/skills/finishing-a-development-branch/`
- `sources/first_party/skills/handoff-gates/`
- `sources/first_party/skills/inspecting-the-environment/`
- `sources/first_party/skills/receiving-code-review/`
- `sources/first_party/skills/requesting-code-review/`
- `sources/first_party/skills/selecting-a-subagent/`
- `sources/first_party/skills/subagent-driven-development/`
- `sources/first_party/skills/systematic-debugging/`
- `sources/first_party/skills/test-driven-development/`
- `sources/first_party/skills/using-git-worktrees/`
- `sources/first_party/skills/using-superpowers-plus/`
- `sources/first_party/skills/verification-before-completion/`
- `sources/first_party/skills/working-with-epics/`
- `sources/first_party/skills/writing-plans/`
- `sources/first_party/skills/writing-skills/`

## Projection surfaces
- Codex plugin root: `codex-marketplace/plugins/superpowers-plus/`
- Skill root: `codex-marketplace/plugins/superpowers-plus/skills/`
- Skill roots:
  - `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/`
  - `codex-marketplace/plugins/superpowers-plus/skills/dispatching-parallel-agents/`
  - `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/`
  - `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/`
  - `codex-marketplace/plugins/superpowers-plus/skills/handoff-gates/`
  - `codex-marketplace/plugins/superpowers-plus/skills/inspecting-the-environment/`
  - `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/`
  - `codex-marketplace/plugins/superpowers-plus/skills/requesting-code-review/`
  - `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/`
  - `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/`
  - `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/`
  - `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/`
  - `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/`
  - `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/`
  - `codex-marketplace/plugins/superpowers-plus/skills/working-with-epics/`
  - `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/`
  - `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/`
<!-- END GENERATED: pack-inventory -->

## Generated install units
There are no generated flat skill zip exports. Skills install from the Codex plugin skill trees under `codex-marketplace/plugins/superpowers-plus/skills/`.

## Boundary
- `superpowers-plus` is the first-party projection-lane bundle for the
  Superpowers+ workflow skill family.
- Editable custody lives in `sources/first_party/skills/<name>/`. The retained
  upstream snapshot under `sources/third_party/superpowers/` is reference-only
  and is not the editable surface.
- No adapter overlay is applied; first-party skills are projected verbatim.
- `codex-marketplace/custody-pack-registry.json` determines whether any
  Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is retired and is not maintained as an active
  marketplace bundle.
