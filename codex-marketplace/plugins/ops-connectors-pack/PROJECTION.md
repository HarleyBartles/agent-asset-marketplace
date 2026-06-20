# Projection

This root is the Codex-facing marketplace projection of selected ECC connector/ops workflow skills from MARK-251.

## Layer Model

This repository uses two distinct layers for the ECC Ops Connectors bundle:

- Source custody keeps the retained third-party ECC snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected ECC skills are materialized from `sources/third_party/ecc/upstream/skills/...`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `ops-connectors-pack` is the third-party plugin projection with ECC connector/ops workflow skills selected for MARK-251.
- The active plugin contains three ECC skills: `automation-audit-ops`, `email-ops`, and `jira-integration`.
- These skills follow the categorization defined in `docs/superpowers/plans/mark-241-skill-categorization.json`, which is the authoritative source for skill categorization.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`

## Excluded from the active install surface

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/ecc/upstream/` as support provenance and retained source custody.
- Other ECC skills not selected for MARK-251 remain in the source custody only.
