# Source

This bundle projects selected ECC Superpowers-style workflow skills into a
dedicated Codex marketplace pack.

## Source custody

- Retained ECC upstream root: `sources/third_party/ecc/upstream/`
- Retained ECC skill roots:
  - `sources/third_party/ecc/upstream/skills/agent-harness-construction/`
  - `sources/third_party/ecc/upstream/skills/ai-first-engineering/`
  - `sources/third_party/ecc/upstream/skills/deployment-patterns/`
  - `sources/third_party/ecc/upstream/skills/dmux-workflows/`
  - `sources/third_party/ecc/upstream/skills/messages-ops/`
  - `sources/third_party/ecc/upstream/skills/ml-adoption-playbook/`
  - `sources/third_party/ecc/upstream/skills/prediction-market-oracle-research/`
  - `sources/third_party/ecc/upstream/skills/recursive-decision-ledger/`
  - `sources/third_party/ecc/upstream/skills/research-ops/`
  - `sources/third_party/ecc/upstream/skills/safety-guard/`
  - `sources/third_party/ecc/upstream/skills/search-first/`
  - `sources/third_party/ecc/upstream/skills/team-agent-orchestration/`
  - `sources/third_party/ecc/upstream/skills/team-builder/`
  - `sources/third_party/ecc/upstream/skills/token-budget-advisor/`
- Provenance note:
  - `provenance/superpowers-ecc.md`

## Projection surfaces

- `codex-marketplace/plugins/superpowers-ecc/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/superpowers-ecc/README.md`
- `codex-marketplace/plugins/superpowers-ecc/SOURCE.md`
- `codex-marketplace/plugins/superpowers-ecc/assets/icon.svg`
- `codex-marketplace/plugins/superpowers-ecc/references/bundle-manifest.json`
- `codex-marketplace/plugins/superpowers-ecc/references/source-map.md`
- `codex-marketplace/plugins/superpowers-ecc/skills/`
- Thin Superpowers+ wrapper:
  - `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/SKILL.md`

## Notes

The retained upstream snapshot stays in third-party custody. This pack is the
dedicated home for the ECC workflow slice named in MARK-244, while
`superpowers-plus` keeps only the small router wrapper needed to expose it.
