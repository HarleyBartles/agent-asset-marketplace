# Superpowers Provenance

## Source anchor

- Upstream repository: `https://github.com/obra/superpowers`
- Release tag: `v6.2.0`
- Release commit: `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`
- Tag object: `0e5cc50e782429b95f933e46443898435b8b37a8`
- License: MIT

## Custody

The upstream release snapshot is retained in third-party source custody at
`sources/third_party/superpowers/obra-superpowers/v6.2.0/`.

## Marketplace projection

The Codex-facing marketplace projection lives at
`codex-marketplace/plugins/superpowers-plus/`.

`superpowers-plus` is now a first-party authored skill bundle. The upstream
`obra/superpowers` v6.2.0 MIT snapshot is retained under
`sources/third_party/superpowers/` as immutable reference and provenance.

The bundle projects the first-party skills listed in
`codex-marketplace/custody-pack-registry.json` from their
`sources/first_party/skills/<name>/` roots into
`codex-marketplace/plugins/superpowers-plus/skills/<name>/`.

Do not place first-party expert or domain skills directly in the Superpowers
plugin that are not already justified as compositional workflow wrappers.
Keep the upstream license and attribution intact in every skill provenance
surface.

## Excluded from the active projection

- `.claude-plugin/`
- `.cursor-plugin/`
- `.opencode/`
- `gemini-extension.json`
- `CLAUDE.md`
- `GEMINI.md`
- `hooks/`

Those surfaces remain source evidence for the upstream package boundary and are
not part of the Codex install surface on this pass.
