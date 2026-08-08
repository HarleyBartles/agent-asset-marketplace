# Superpowers+

This bundle contains the first-party Superpowers+ workflow skills, including the `using-superpowers-plus` workflow-selection entrypoint.

## Bundle contents

### Documentation
- provenance and source mapping in `SOURCE.md`
- bundle inventory in `references/bundle-manifest.json`

## Boundary
- `superpowers-plus` is the first-party plugin bundle for the
  Superpowers+ workflow skill family.
- Editable custody lives in `codex-marketplace/plugins/superpowers-plus/skills/<name>/`. The upstream
  `obra/superpowers` v6.2.0 MIT snapshot is recorded in `SOURCE.md` as reference only; it is not the editable
  surface and no adapter overlay is applied.
- `codex-marketplace/plugin-roots.json` lists the active plugin roots.
- `superpowers-mega-pack` is retired and is not a maintained active marketplace
  bundle.

## Install shape

Skills are installed from the Codex plugin root under `codex-marketplace/plugins/superpowers-plus/skills/<skill>/`.
