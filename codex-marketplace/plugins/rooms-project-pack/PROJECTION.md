# Projection

This root is the Codex-facing marketplace projection of the retained Rooms
project skills plus one database guidance skill.

## Layer Model

This repository uses two distinct layers for the Rooms bundle:

- Source custody keeps the retained first-party Rooms skills and the retained
  Claude-Cortex database skill in their source trees.
- Projection layer holds the source-controlled marketplace copy with the
  selection decision for the Rooms project pack.
- Installation/export layer is derived from the projection and is produced only
  by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply marketplace adaptation inside source custody.
- Do apply projection-layer selection and packaging in the marketplace copy.
- Do treat generated zips, registry entries, and GPT exports as derived install
  surfaces, not hand-edited sources.

## Projection contract

- `rooms-project-pack` is a narrow project pack for Rooms-mostly.
- The active plugin contains the Rooms routing, doctrine, partitioning, ambiguity,
  analogy, zoom-out, character investigation, sheet creation, canon pressure,
  and image-sidecar skills plus `database-design-patterns`.
- The pack intentionally excludes repo-worker, superpowers, unslop, and broad
  architecture bundles.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `assets/icon.svg`
- `LICENSE`
- `README.md`
- `SOURCE.md`
- `PROJECTION.md`
- `references/bundle-manifest.json`
- `references/source-map.md`
- `references/provenance-map.json`

## Excluded from the active install surface

- Source custody trees remain in `sources/first_party/skills/` and
  `sources/third_party/claude-cortex/upstream/`.
- Other Rooms skill decisions stay in the house-skills projection.
