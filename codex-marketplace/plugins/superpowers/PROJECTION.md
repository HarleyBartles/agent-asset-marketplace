# Projection

This root is the Codex-facing marketplace projection of `obra/superpowers`
`v5.1.0`, plus the source-backed House Skills `linear-superpowers` and
`github-superpowers` and `unslop-superpowers` skills.

## Included in the active install surface

- `.codex-plugin/plugin.json`
- `skills/`
- `skills/linear-superpowers/`
- `skills/github-superpowers/`
- `skills/unslop-superpowers/`
- `skills/codex-repo-receipts/`
- `assets/app-icon.png`
- `assets/superpowers-small.svg`
- `LICENSE`
- `SOURCE.md`
- `PROJECTION.md`
- `references/codex-marketplace-compatibility.md`
- `references/bundle-manifest.json`
- `references/provenance-map.json`

`skills/linear-superpowers/` is copied from the canonical House Skills source
at `codex-marketplace/plugins/house-skills/skills/linear-superpowers/`.
`skills/github-superpowers/` is copied from the canonical House Skills source
at `codex-marketplace/plugins/house-skills/skills/github-superpowers/`.
`skills/unslop-superpowers/` is copied from the canonical House Skills source
at `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/`.
`skills/codex-repo-receipts/` is copied from the canonical House Skills source
at `codex-marketplace/plugins/house-skills/skills/codex-repo-receipts/` and
provides repo-resident plan and implementation-record guidance.

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
