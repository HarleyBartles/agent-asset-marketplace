# Superpowers+ Source Map

This bundle harmonizes the retained upstream `obra/superpowers` `v5.1.0`
release with the repo-authored `ecc-superpowers` wrapper and the source-backed
House Skills projections.

Harmonization notes:

- `using-superpowers` stays as the adapted front-door router for workflow
  selection.
- `finishing-a-development-branch` stays as the adapted closeout gate.
- `verification-before-completion` stays as the adapted completion backstop.
- `linear-superpowers` stays at the Linear shaping layer.
- `github-superpowers` stays at the GitHub proof and publication layer.
- `unslop-superpowers` stays at the repo-specific anti-slop layer.
- `architecture-superpowers` stays at the architecture review and composition
  boundary layer.
- `ecc-superpowers` stays as the thin router wrapper that points to the
  dedicated `superpowers-ecc` pack.
- Detailed file-level projections and source-file inventories are captured in
  `references/bundle-manifest.json`.

Retained third-party custody:

- `sources/third_party/superpowers/obra-superpowers/v5.1.0/`

Retained first-party custody:

- `sources/first_party/skills/linear-superpowers/`
- `sources/first_party/skills/github-superpowers/`
- `sources/first_party/skills/unslop-superpowers/`
- `sources/first_party/skills/architecture-superpowers/`
- `sources/first_party/skills/ecc-superpowers/`

Projected pack skills:

| Skill | Source path | Pack path | Notes |
| --- | --- | --- | --- |
| linear-superpowers | `sources/first_party/skills/linear-superpowers/` | `codex-marketplace/plugins/superpowers-plus/skills/linear-superpowers/` | Source-backed first-party Linear shaping skill. |
| github-superpowers | `sources/first_party/skills/github-superpowers/` | `codex-marketplace/plugins/superpowers-plus/skills/github-superpowers/` | Source-backed first-party GitHub proof skill. |
| unslop-superpowers | `sources/first_party/skills/unslop-superpowers/` | `codex-marketplace/plugins/superpowers-plus/skills/unslop-superpowers/` | Source-backed first-party anti-slop skill. |
| architecture-superpowers | `sources/first_party/skills/architecture-superpowers/` | `codex-marketplace/plugins/superpowers-plus/skills/architecture-superpowers/` | Source-backed first-party architecture review skill. |
| ecc-superpowers | `sources/first_party/skills/ecc-superpowers/` | `codex-marketplace/plugins/superpowers-plus/skills/ecc-superpowers/` | Repo-authored wrapper that routes ECC workflow-shaped work to `superpowers-ecc`. |
| using-superpowers | `sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/using-superpowers` | `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers/` | Adapted front-door router with marketplace-specific routing. |
| finishing-a-development-branch | `sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/finishing-a-development-branch` | `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/` | Adapted closeout gate with marketplace-specific publication guidance. |
| verification-before-completion | `sources/third_party/superpowers/obra-superpowers/v5.1.0/skills/verification-before-completion` | `codex-marketplace/plugins/superpowers-plus/skills/verification-before-completion/` | Adapted completion backstop with plan/evidence reconciliation. |

The bundle root is an installable Codex plugin projection. It does not replace
the retained upstream snapshot or the dedicated `superpowers-ecc` pack.
