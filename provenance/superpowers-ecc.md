# Superpowers ECC Provenance

## Source anchor

- Upstream repository: `https://github.com/affaan-m/ECC/tree/main/skills`
- Pinned upstream commit: `ceca28852e5b31edbbf66ebccc8fd163dd14208e`
- Retained custody root: `sources/third_party/ecc/upstream/skills/`
- Retained upstream license: `sources/third_party/ecc/upstream/LICENSE`

## Authorship split

- The `superpowers-ecc` plugin shell is authored by Harley Bartles.
- Verbatim skill projections retain upstream source attribution and MIT
  licensing in the projected skill metadata and bundle manifest.
- The `ecc-superpowers` wrapper is repo-authored and adapted by Harley
  Bartles.

## Projection

The dedicated marketplace projection lives at
`codex-marketplace/plugins/superpowers-ecc/`.

It copies the selected ECC workflow skill trees into the active plugin
surface and keeps the retained third-party source custody untouched.

Selected pack skills:

- `agent-harness-construction`
- `ai-first-engineering`
- `deployment-patterns`
- `dmux-workflows`
- `messages-ops`
- `ml-adoption-playbook`
- `prediction-market-oracle-research`
- `recursive-decision-ledger`
- `research-ops`
- `safety-guard`
- `search-first`
- `team-agent-orchestration`
- `team-builder`
- `token-budget-advisor`

Projection contract:

- `superpowers-ecc` is the dedicated ECC Superpowers workflow pack.
- `superpowers-plus` only keeps the thin `ecc-superpowers` routing wrapper.
- Keep the workflow slice narrow and avoid pulling branding, social, media, or
  unrelated domain-specialist skills into this pack.
- Do not treat this projection as a new source of truth.
