# AGENTS.md

Scope: `codex-marketplace/plugins/`

This scope covers the installable Codex plugin pack roots stored under the
marketplace source tree.

Codex plugin first; generated GPT-safe skill zips second.

The active installable roots under this directory are fixed to
`house-skills/`, `adventures-pack/`, `unslop/`, `game-studio/`,
`wild-bunch-project-pack/`, `superpowers/`, `repo-worker-base/`,
`dotnet-kit/`, and `architecture-pack/`.

That active set is now sourced from `codex-marketplace/plugin-roots.json` and
validated against the protected marketplace manifests and registry surfaces.

These are projection roots. Their source custody is normalized under
`sources/first_party/` and `sources/third_party/`.

Treat these plugin roots as the canonical install surface. Generated
`skill.zip` artifacts are downstream GPT exports; `gpt-overlays/manifest.json`
controls whether a skill is exported direct, via overlay, or excluded.
Everything else in this tree is support custody or historical source material,
not part of the active marketplace inventory for the normalized root pass.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Manifest guidance

Bundle-manifest entries for imported or retained projection content must declare
`content_mode`.

- `verbatim` means the retained source snapshot content and the projected plugin
  content must remain byte/hash equivalent.
- `adapted` means equality is not expected, but the entry must carry an
  explicit adaptation note and a provenance trail.
- Projection roots under `codex-marketplace/plugins/` are not canonical source
  custody; they must stay aligned with the retained source/provenance contract
  declared in the manifest.

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
- Flag any source-tree `skill.zip` file. Canonical install archives belong only
  under `generated/skill-zips/`.
