# Projection

This root is the Codex-facing marketplace projection of the first-party Superpowers+ workflow skills, including the `using-superpowers-plus` workflow-selection entrypoint.

## Layer Model

This repository uses two distinct layers for the Superpowers+ bundle:

- Source custody keeps the first-party skills in `sources/first_party/skills/<name>/`.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skills are materialized from `sources/first_party/skills/...`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply marketplace adaptation inside the first-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `superpowers-plus` is the first-party projection-lane bundle for the Superpowers+ workflow skill family.
- The retained `obra/superpowers` v6.2.0 MIT snapshot under `sources/third_party/superpowers/` is reference-only; it is not the editable surface and no adapter overlay is applied.
<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (18):
  - `brainstorming`
  - `dispatching-parallel-agents`
  - `executing-plans`
  - `finishing-a-development-branch`
  - `handoff-gates`
  - `inspecting-the-environment`
  - `receiving-code-review`
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
<!-- END GENERATED: projection-contract -->
- `codex-marketplace/custody-pack-registry.json` determines whether any Superpowers-derived root is actively projected.
- `superpowers-mega-pack` is retired and is not a maintained active projection surface.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- The retained upstream `obra/superpowers` v6.2.0 snapshot stays in
  `sources/third_party/superpowers/` as reference-only source custody and is
  not part of the active install surface.
- No separate `superpowers-mega-pack` root is part of the active install surface.
