# Superpowers+

This bundle projects the first-party Superpowers+ workflow skills, including the `using-superpowers-plus` workflow-selection entrypoint.

## Bundle contents
<!-- BEGIN GENERATED: bundle-contents -->
### First Party skills
- `brainstorming`
- `dispatching-parallel-agents`
- `executing-plans`
- `finishing-a-development-branch`
- `handoff-gates`
- `inspecting-the-environment`
- `receiving-code-review`
- `requesting-branch-review`
- `requesting-code-review`
- `selecting-a-subagent`
- `subagent-driven-development`
- `systematic-debugging`
- `test-driven-development`
- `using-git-worktrees`
- `using-superpowers-plus`
- `verification-before-completion`
- `working-with-epics`
- `writing-plans`
- `writing-skills`

Manifest entry count: 19.
<!-- END GENERATED: bundle-contents -->

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`
- canonical source mapping in `references/source-map.md`

## Boundary
- `superpowers-plus` is the first-party projection-lane bundle for the
  Superpowers+ workflow skill family.
- Editable custody lives in `sources/first_party/skills/<name>/`. The upstream
  `obra/superpowers` v6.2.0 MIT snapshot is retained under
  `sources/third_party/superpowers/` as reference only; it is not the editable
  surface and no adapter overlay is applied.
- `codex-marketplace/custody-pack-registry.json` determines whether any
  Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is retired and is not a maintained active marketplace
  bundle.

## Install shape

Skills are installed from the Codex plugin root under `codex-marketplace/plugins/superpowers-plus/skills/<skill>/`.
