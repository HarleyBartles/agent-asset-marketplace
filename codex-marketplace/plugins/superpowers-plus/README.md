# Superpowers+

This bundle contains the first-party Superpowers+ workflow skills, including the `using-superpowers-plus` workflow-selection entrypoint.

## Bundle contents

### Documentation
- provenance and source mapping in `SOURCE.md` (see `## Upstream Basis` and `## Plugin custody`)
- bundle inventory in `references/bundle-manifest.json`

## Boundary
- `superpowers-plus` is the first-party plugin bundle for the
  Superpowers+ workflow skill family.
- Editable custody lives in
  `codex-marketplace/plugins/superpowers-plus/skills/<name>/`. The upstream
  `obra/superpowers` v6.3.0 MIT comparison commit is recorded in `SOURCE.md`
  (see `## Upstream Basis` and `## Plugin custody`). Upstream source is not
  vendored or editable here, and no adapter overlay is applied.
- `codex-marketplace/plugin-roots.json` lists the active plugin roots.
- `superpowers-mega-pack` is retired and is not a maintained active marketplace
  bundle.

## Install shape

Skills are installed from the Codex plugin root under `codex-marketplace/plugins/superpowers-plus/skills/<skill>/`.
