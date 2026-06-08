# AGENTS.md

Scope: `codex-marketplace/`

This scope covers the Codex marketplace source root, including the marketplace
manifest and the plugin source tree beneath it.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Treat `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json`
  as coupled surfaces; a plugin add, remove, or rename must stay aligned across
  both exports and the validator.
- Flag broken plugin root paths, missing `.codex-plugin/plugin.json` files, and
  category or install-policy drift in the marketplace manifest.
- Flag missing `SOURCE.md`, `LICENSE`, or bundle-manifest references when a
  plugin root claims to expose them.
- Flag generated-export mismatches that would let the registry or bundle source
  drift silently from the tracked marketplace source tree.
- Prefer serious packaging and discoverability issues over stylistic concerns.
