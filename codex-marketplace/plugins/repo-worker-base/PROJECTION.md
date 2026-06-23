# Projection

This root is the Codex-facing marketplace projection of repo worker base skills
plus the complementary ECC search-first skill.

## Layer Model

This repository uses two distinct layers for the repo worker base bundle:

- Source custody keeps the first-party core skills in
  `sources/first_party/skills/` and the complementary ECC search-first source
  in `sources/third_party/ecc/upstream/skills/`.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skills are materialized from `sources/first_party/skills/...`
  plus `sources/third_party/ecc/upstream/skills/search-first`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply marketplace adaptation inside the first-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `repo-worker-base` is the first-party plugin projection with core repo worker
  skills and the complementary ECC search-first workflow.
- The active plugin contains `boring-loop`, `connector-safety`,
  `github-operations`, and `search-first`.
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
  canonical source, and the selected ECC skill stays in retained third-party
  custody.
