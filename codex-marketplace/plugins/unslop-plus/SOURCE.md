# Source

This plugin composes the upstream `mshumer/unslop` workflow engine with thirteen first-party portable profiles for common software development workflows.

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT`
- Source custody: `sources/third_party/unslop/upstream/`

## First-Party Profile Authorship

- Profile author: Harley Bartles (Asset Marketplace)
- Profile source: MARK-265 Linear issue requirements
- Profile license: MIT (same as upstream engine)

## Marketplace Composition

- Retained upstream Unslop engine scripts from `codex-marketplace/plugins/unslop/skills/unslop/scripts/`
- Added thirteen first-party portable profiles under `skills/unslop-plus/profiles/`
- Each profile is portable across repos with no Asset Marketplace-specific nouns
- Provenance clearly distinguishes third-party engine custody from first-party profile authorship

## Install Shape

- GPT skill package: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/`
- Codex plugin route: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Marketplace registry: `.agents/plugins/marketplace.json`
