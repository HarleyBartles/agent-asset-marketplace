# Projection

This root is the Codex-facing marketplace projection of the retained ECC
workflow mechanics.

## Layer Model

- Source custody keeps the retained ECC snapshots.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced
  only by canonical tooling.
- The custody flow is `source custody -> projection layer ->
  installation/export layer`.

## Projection contract

- `agentic-workflows` is the marketplace projection for the retained skills
  listed in `references/bundle-manifest.json`.
- The active plugin contains `agent-harness-construction`,
  `autonomous-agent-harness`, `continuous-agent-loop`,
  `dynamic-workflow-mode`, `dmux-workflows`, and `agentic-os`.
- Keep the skill bodies intact unless the bundle manifest says a skill is
  normalized or adapted.

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

- Upstream harness surfaces, tests, docs, and package metadata remain in
  source custody as support provenance and retained source custody.
