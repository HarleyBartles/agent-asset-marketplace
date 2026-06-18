# Projection

This root is the Codex-facing marketplace projection of `obra/superpowers`
`v5.1.0`, plus the source-backed House Skills `linear-superpowers`,
`github-superpowers`, `unslop-superpowers`, `codex-receipts-superpowers`, and
`architecture-superpowers` skills.

## Projection contract

- `superpowers` is a third-party plugin projection with selected first-party
  compositional skills projected into the vendored marketplace plugin.
- The active plugin may contain upstream Superpowers skills plus the selected
  first-party wrapper skills `linear-superpowers`, `github-superpowers`,
  `unslop-superpowers`, `codex-receipts-superpowers`, and
  `architecture-superpowers`.
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
- Any future first-party skill proposed for projection into `superpowers` must
  be justified as a compositional wrapper over Superpowers, not as an expert
  skill being relocated into the third-party plugin.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `skills/linear-superpowers/`
- `skills/github-superpowers/`
- `skills/unslop-superpowers/`
- `skills/codex-receipts-superpowers/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/codex-marketplace-compatibility.md`
- `references/bundle-manifest.json`
- `references/provenance-map.json`

`skills/linear-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/core/linear-superpowers/`.
`skills/github-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/skills/github-superpowers/`.
`skills/unslop-superpowers/` is copied from the canonical House Skills source
at `sources/first_party/skills/unslop-superpowers/`.
`skills/codex-receipts-superpowers/` is copied from the canonical House Skills
source at `sources/first_party/skills/codex-receipts-superpowers/`.
`skills/architecture-superpowers/` is copied from the canonical House Skills
source at `sources/first_party/skills/architecture-superpowers/`.

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

Those files remain in `sources/third_party/superpowers/obra-superpowers/v5.1.0/`
as support provenance and retained source custody.
