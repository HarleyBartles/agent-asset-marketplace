# Source

This bundle projects the selected ECC Superpowers-style workflow skills into a
Codex marketplace projection pack.

The plugin shell is authored by Harley Bartles. The projected skill roots
retain their upstream source author, source license, and source path in the
bundle manifest and source map so verbatim content stays attributable. The
local projection is mirrored from
`codex-marketplace/plugins/superpowers-ecc/skills/` instead of from the
upstream ECC repository directly.

## Source custody

- Retained ECC upstream root: `sources/third_party/ecc/upstream/`
- Retained ECC upstream license: `sources/third_party/ecc/upstream/LICENSE`
- Source projection root:
  - `codex-marketplace/plugins/superpowers-ecc/skills/`
- Selected ECC skill roots mirrored into this pack:
  - `codex-marketplace/plugins/superpowers-ecc/skills/agent-harness-construction/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/ai-first-engineering/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/deployment-patterns/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/dmux-workflows/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/messages-ops/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/ml-adoption-playbook/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/prediction-market-oracle-research/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/recursive-decision-ledger/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/research-ops/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/safety-guard/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/search-first/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/team-agent-orchestration/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/team-builder/`
  - `codex-marketplace/plugins/superpowers-ecc/skills/token-budget-advisor/`
- Provenance note:
  - `provenance/everything-codex-code.md`

## Projection surfaces

- `codex-marketplace/plugins/everything-codex-code/.codex-plugin/plugin.json`
- `codex-marketplace/plugins/everything-codex-code/README.md`
- `codex-marketplace/plugins/everything-codex-code/SOURCE.md`
- `codex-marketplace/plugins/everything-codex-code/LICENSE`
- `codex-marketplace/plugins/everything-codex-code/assets/icon.svg`
- `codex-marketplace/plugins/everything-codex-code/references/bundle-manifest.json`
- `codex-marketplace/plugins/everything-codex-code/references/source-map.md`
- `codex-marketplace/plugins/everything-codex-code/skills/`

## Notes

The retained upstream snapshot stays in third-party custody. This pack is an
installable projection home for the ECC workflow slice already selected into
the dedicated `superpowers-ecc` marketplace projection. The downstream skill
zips and registry outputs are generated from this checked-in root. It does not
replace that projection or create a new source of truth.
