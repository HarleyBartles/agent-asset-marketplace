# Projection

This root is the Codex-facing marketplace projection of selected Claude-Cortex planning skills.

## Layer Model

This repository uses two distinct layers for the planning bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected planning skills are materialized from `sources/third_party/claude-cortex/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `planning-pack` is the third-party plugin projection with selected Claude-Cortex planning skills per the first-party selection ledger.
- The active plugin contains requirements discovery, mermaid diagramming, development estimation, release preparation, and release analysis skills named in the selection ledger.
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

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/claude-cortex/upstream/` as support provenance and retained source custody.
- Other Claude-Cortex skills remain in source custody only.