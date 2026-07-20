# Projection

This root is the Codex-facing marketplace projection of the .NET ecosystem pack.

## Layer Model

This repository uses two distinct layers for the dotnet-pack bundle:

- Source custody keeps the first-party `dotnet` skill verbatim.
- Projection layer holds the source-controlled marketplace copy with first-party selection decisions.
- Installation/export layer is derived from the projection and is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The projected skill is materialized from `sources/first_party/skills/dotnet/` per the registry.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording or marketplace adaptation inside the first-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived install surfaces, not hand-edited sources.

## Projection contract

- `dotnet-pack` is the .NET ecosystem plugin projection.
<!-- BEGIN GENERATED: projection-contract -->
- Active manifest entries (1):
  - `dotnet`
<!-- END GENERATED: projection-contract -->
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
