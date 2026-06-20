# Projection

This root is the Codex-facing marketplace projection of the MARK-166 approved subset of `codewithmukesh/dotnet-claude-kit`.

## Layer Model

This repository uses two distinct layers for the dotnet-kit bundle:

- Source custody keeps the retained third-party dotnet-claude-kit snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected dotnet skills are materialized from `sources/third_party/dotnet-claude-kit/upstream/skills/...` per the first-party selection ledger.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `dotnet-kit` is the third-party plugin projection with selected dotnet-claude-kit skills per the first-party selection ledger.
- The active plugin contains only the six approved technical skills named in the selection ledger (`sources/first_party/skills/dotnet-kit/decisions.json`).
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection wording.
- First-party selection decisions are recorded in `sources/first_party/skills/dotnet-kit/decisions.json` and `decisions.md`.

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

- Upstream harness surfaces, tests, docs, and package metadata remain in `sources/third_party/dotnet-claude-kit/upstream/` as support provenance and retained source custody.
- `tdd` and `verify` skills remain in source custody only and are not projected.
