# Projection

This root is the Codex-facing marketplace projection of `obra/superpowers`
`v6.0.3`, branded in the marketplace as `Superpowers+`, plus the
source-backed House Skills `linear-superpowers`, `github-superpowers`,
`unslop-superpowers`, and `architecture-superpowers` skills, plus the
first-party `ecc-superpowers` router wrapper that points to `superpowers-ecc`,
plus the first-party `inspecting-the-environment` skill.

## Layer Model

This repository uses three distinct layers for the Superpowers bundle:

- Source custody keeps the retained third-party snapshot verbatim.
- Projection layer holds the source-controlled marketplace copy and any
  Codex-marketplace adaptations.
- Installation/export layer is derived from the projection plus overlays and
  is produced only by canonical tooling.
- The custody flow is `source custody -> projection layer -> installation/export layer`.
- The adapted Superpowers+ skills are materialized from
  `sources/third_party/superpowers/obra-superpowers/v6.0.3/skills/...` plus
  `adapters/codex/superpowers-plus/...`.
- Frontmatter contract: [docs/contracts/skill-frontmatter.md](../../../docs/contracts/skill-frontmatter.md)
- OpenAI agent contract: [docs/contracts/openai-agent-yaml.md](../../../docs/contracts/openai-agent-yaml.md)

The split is deliberate:

- Do not apply Codex-safe wording, frontmatter normalization, or marketplace
  adaptation inside the third-party source custody root.
- Do apply projection-layer adaptations in the marketplace copy where they can
  be reviewed, documented, and regenerated.
- Do treat generated zips, registry entries, and GPT exports as derived
  install surfaces, not hand-edited sources.

## Projection contract

- `superpowers-plus` is the third-party plugin projection with selected
  first-party compositional skills projected into the vendored marketplace
  plugin.
- The active plugin may contain upstream Superpowers skills plus the selected
  first-party wrapper skills `linear-superpowers`, `github-superpowers`,
  `unslop-superpowers`, `architecture-superpowers`, `ecc-superpowers`, and
  `inspecting-the-environment`.
- Those first-party skills are compositional and complementary. They compose
  Superpowers workflow guidance with first-party expert skills that live
  outside the Superpowers plugin.
- Do not place first-party expert or domain skills directly in the Superpowers
  plugin.
- Do not use this plugin as a dumping ground for House Skills, project doctrine,
  verification experts, GitHub/Linear mechanics, or other first-party expert
  surfaces.
- Keep repo-specific overlay and adaptation text intact. Do not overwrite or
  reset the GPT-safe, Codex-marketplace-safe, or repo-policy-safe projection
  wording.
- The adapted `using-superpowers`, `finishing-a-development-branch`, and
  `verification-before-completion` projections are materialized from source
  custody plus adaptation overlays; the upstream source snapshot remains
  verbatim.
- `ecc-superpowers` is a verbatim first-party wrapper projection that
  routes to the dedicated `superpowers-ecc` pack without folding ECC doctrine
  into the upstream Superpowers source.
- Any future first-party skill proposed for projection into `superpowers-plus`
  must be justified as a compositional wrapper over Superpowers, not as an
  expert skill being relocated into the third-party plugin.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `skills/linear-superpowers/`
- `skills/github-superpowers/`
- `skills/unslop-superpowers/`
- `skills/architecture-superpowers/`
- `skills/ecc-superpowers/`
- `skills/inspecting-the-environment/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/codex-marketplace-compatibility.md`
- `references/source-map.md`
- `references/bundle-manifest.json`
- `references/provenance-map.json`

`skills/linear-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/skills/linear-superpowers/`.
`skills/github-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/skills/github-superpowers/`.
`skills/unslop-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/skills/unslop-superpowers/`.
`skills/architecture-superpowers/` is copied from the canonical House Skills
source at `sources/first_party/skills/architecture-superpowers/`.
`skills/ecc-superpowers/` is copied from the canonical first-party source at
`sources/first_party/skills/ecc-superpowers/`.
`skills/inspecting-the-environment/` is copied from the canonical first-party
source at `sources/first_party/skills/inspecting-the-environment/`.

Each first-party projection is a directory-level skill spec, so the copied
tree includes both `SKILL.md` and `agents/openai.yaml` when the canonical
source provides them.

## Excluded from the active install surface

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `gemini-extension.json`
- `CLAUDE.md`
- `GEMINI.md`
- `hooks/`
- `README.md`
- `package.json`

Those files remain in `sources/third_party/superpowers/obra-superpowers/v6.0.3/`
as support provenance and retained source custody.
