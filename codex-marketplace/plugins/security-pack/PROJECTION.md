# Projection

This root is the Codex-facing marketplace projection of the retained Codex
Cortex security foundations plus the complementary ECC safety and
security-review skills.

## Layer Model

- Source custody keeps the retained Claude Cortex snapshots and the retained
  ECC source custody.
- Projection layer holds the source-controlled marketplace copy.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

## Projection contract
- `security-pack` is the marketplace projection for the retained skills listed
  in `references/bundle-manifest.json`.
- The active plugin contains `owasp-top-10`, `secure-coding-practices`,
  `security-testing-patterns`, `threat-modeling-techniques`, `safety-guard`,
  and `security-review`.
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

- Upstream harness surfaces, tests, docs, and package metadata remain in source
  custody as support provenance and retained source custody.
- The ECC safety and security-review skills stay in this bundle, while the
  removed ECC router or projection material stays out of this bundle.
