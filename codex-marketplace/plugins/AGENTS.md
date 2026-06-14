# AGENTS.md

Scope: `codex-marketplace/plugins/`

This scope covers the installable Codex plugin pack roots stored under the
marketplace source tree.

The active installable roots under this directory are fixed to
`house-skills/`, `adventures-pack/`, `unslop/`, and `game-studio/`.

These are projection roots. Their source custody is normalized under
`sources/first_party/` and `sources/third_party/`.
Everything else in this tree is support custody or historical source material,
not part of the active marketplace inventory for the normalized four-root pass.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Flag missing or broken `.codex-plugin/plugin.json` files, asset references,
  or `skills/` paths before minor content issues.
- Flag missing `SOURCE.md`, `LICENSE`, `references/bundle-manifest.json`, or
  other support files when the plugin manifest or README claims they exist.
- Flag false provenance claims, especially where a copied or adapted plugin
  root is described as copied verbatim or first-party without evidence.
- Flag registry mismatches when a plugin root changes but the marketplace
  manifest, runtime registry, or repo index is not updated with it.
- Flag unsupported changes to vendored plugin custody material unless the
  change has an explicit adaptation reason and provenance trail.
