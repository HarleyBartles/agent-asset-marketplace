# Projection

This root is the Codex-facing marketplace projection of selected ECC Superpowers-style workflow skills, mirrored from the superpowers-ecc projection.

## Layer Model

This repository uses three distinct layers for the ECC Superpowers bundle:

- Source custody keeps the retained third-party ECC snapshot verbatim.
- Primary projection layer is `codex-marketplace/plugins/superpowers-ecc/`.
- Secondary projection layer is this root, which mirrors selected skills from the primary projection.
- Installation/export layer is derived from the secondary projection and is produced only by canonical tooling.
- The custody flow is `source custody -> primary projection -> secondary projection -> installation/export layer`.
- The projected ECC skills are mirrored from `codex-marketplace/plugins/superpowers-ecc/skills/...`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- The primary projection (`superpowers-ecc`) is the authoritative ECC projection.
- This secondary projection (`everything-codex-code`) is a downstream mirror for install convenience.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `everything-codex-code` is a secondary projection that mirrors selected ECC skills from `superpowers-ecc`.
- The active plugin contains the same ECC workflow skills as `superpowers-ecc`.
- This pack does not replace `superpowers-ecc` as the authoritative ECC projection.
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
