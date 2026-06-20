# Source

This plugin replaces the vendored `unslop` plugin as a combined third/first-party projection. It composes the upstream `mshumer/unslop` workflow engine (verbatim third-party custody) with thirteen first-party portable profiles (projected from first-party source custody).

## Upstream Basis

- Repo: `mshumer/unslop`
- URL: <https://github.com/mshumer/unslop.git>
- Pinned commit: `edcb62386d129c65e4395f0cfcc9168eb1ba2148`
- License: `MIT`
- Source custody: `sources/third_party/unslop/upstream/`
- Projection: engine scripts copied verbatim into `skills/unslop-plus/scripts/`

## First-Party Profile Source Custody

- Profile author: Harley Bartles (Asset Marketplace)
- Profile source: MARK-265 Linear issue requirements
- Profile license: MIT (same as upstream engine)
- Canonical source custody: `sources/first_party/skills/unslop-plus/profiles/`
- Projection: profiles projected verbatim into `skills/unslop-plus/profiles/`

## Marketplace Composition

- Replaces the vendored `unslop` plugin root in `plugin-roots.json`
- Third-party Unslop engine scripts projected verbatim from upstream custody
- Thirteen first-party portable profiles projected verbatim from first-party source custody
- Each profile is portable across repos with no Asset Marketplace-specific nouns
- Provenance clearly distinguishes third-party engine custody from first-party profile authorship

## Install Shape

- GPT skill package: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/`
- Codex plugin route: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Marketplace registry: `.agents/plugins/marketplace.json`
