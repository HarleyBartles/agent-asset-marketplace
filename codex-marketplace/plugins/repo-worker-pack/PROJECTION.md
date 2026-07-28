# Projection

This root is the Codex-facing marketplace projection of repo worker baseline skills.

## Layer Model

This repository uses two distinct layers for the repo worker pack:

- Source custody keeps the first-party core skills in
  `sources/first_party/skills/`.
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

- `repo-worker-pack` is the first-party plugin projection with core repo worker
  skills and its compositional entrypoint.
<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (17):
  - `asking-clarifying-questions`
  - `base-doctrine`
  - `cleanup-custody`
  - `connector-safety`
  - `context-safety`
  - `generating-agent-mesh`
  - `linear-issue-shaping`
  - `refreshing-installed-skills`
  - `repo-standards`
  - `repo-worker-base`
  - `risk-gates`
  - `subagent-model-routing`
  - `unslop-profiles`
  - `using-github`
  - `using-linear`
  - `work-mode-router`
  - `writing-with-clarity`
<!-- END GENERATED: projection-contract -->
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/source-map.md`

## Excluded from the active install surface

- First-party source custody remains in `sources/first_party/skills/` as the
  canonical source, and the bundle stays first-party only.
