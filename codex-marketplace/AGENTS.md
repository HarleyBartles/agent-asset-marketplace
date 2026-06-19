# AGENTS.md

Scope: `codex-marketplace/`

This scope covers the Codex marketplace source root, including the marketplace
manifest and the plugin source tree beneath it.

Codex plugin first; generated GPT-safe skill zips second.

The active plugin roots in this scope are defined by
`codex-marketplace/plugin-roots.json` and validated against the protected
marketplace manifests and registry surfaces.

Those roots are installable projections only. Their editable source custody
lives under `sources/first_party/` and `sources/third_party/`.

The marketplace plugin roots are the canonical install surface. Generated
`skill.zip` files under `generated/skill-zips/` are downstream GPT exports, and
`adapters/gpt/manifest.json` decides whether each one is `direct`, `overlay`,
or `excluded`.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Treat `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json`
  as coupled surfaces; a plugin add, remove, or rename must stay aligned across
  both exports and the validator.
- Treat any plugin root under `codex-marketplace/plugins/` not listed in
  `plugin-roots.json` as inactive unless a new issue explicitly changes the
  marketplace shape.
- Flag broken plugin root paths, missing `.codex-plugin/plugin.json` files, and
  category or install-policy drift in the marketplace manifest.
- Flag missing `SOURCE.md`, `LICENSE`, or bundle-manifest references when a
  plugin root claims to expose them.
- Flag generated-export mismatches that would let the registry or bundle source
  drift silently from the tracked marketplace source tree or GPT overlay source.
- Flag any `skill.zip` found inside a source skill tree; canonical install
  archives belong only under `generated/skill-zips/` and must be written by the
  package tool, not by hand.
- Flag stale or unregistered canonical skill.zip artifacts under
  `generated/skill-zips/`, including missing overlay derivation metadata or
  excluded GPT-export records.
- Prefer serious packaging and discoverability issues over stylistic concerns.
