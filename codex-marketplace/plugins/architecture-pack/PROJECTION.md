# Projection

This root is the Codex-facing marketplace projection of selected Codex Cortex architecture skills.

## Layer Model

This repository uses three distinct layers for the architecture bundle:

- Source custody keeps the retained third-party Claude-Cortex snapshot verbatim.
- Primary projection layer is `codex-marketplace/plugins/codex-cortex/`.
- Secondary projection layer is this root, which mirrors selected architecture skills from the primary projection.
- Installation/export layer is derived from the secondary projection and is produced only by canonical tooling.
- The custody flow is `source custody -> primary projection -> secondary projection -> installation/export layer`.
- The projected architecture skills are mirrored from `codex-marketplace/plugins/codex-cortex/skills/...`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the third-party source custody root.
- The primary projection (`codex-cortex`) is the authoritative Claude-Cortex projection.
- This secondary projection (`architecture-pack`) is a downstream mirror for architecture skills.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `architecture-pack` is a secondary projection that mirrors selected architecture skills from `codex-cortex`.
- The active plugin contains `cqrs-event-sourcing`, `event-driven-architecture`, and `database-design-patterns` mirrored from `codex-cortex`.
- This pack does not replace `codex-cortex` as the authoritative Claude-Cortex projection.
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
- Other Claude-Cortex skills remain in the primary projection only.
