# AGENTS.md

Scope: `codex-marketplace/plugins/`

This scope covers the installable Codex plugin pack roots stored under the
marketplace source tree.

Codex plugin first; generated GPT-safe skill zips second.

This scope is projection law, not source custody. Keep the plugin-root
inventory, manifest exports, and generated navigation aligned, but do not add
manual `INDEX.md` files inside skill roots or overlay roots.

The active installable roots under this directory are defined by
`codex-marketplace/plugin-roots.json` and validated against the protected
marketplace manifests and registry surfaces.

These are projection roots. Their source custody is normalized under
`sources/first_party/` and `sources/third_party/`.

Treat these plugin roots as the canonical install surface. Everything else
in this tree is support custody or historical source material, not part of
the active marketplace inventory for the normalized root pass.

Deterministic pack rule: plugin-root membership must come from the central
manifest and the checked-in generator/validator pipeline. Do not hand-edit
projected skill trees, source maps, provenance maps, or bundle-manifest
membership lists, and do not create plugin-specific one-off scripts when the
existing deterministic path can be extended instead.

Skill-to-pack assignments (which skills appear in which plugin pack) are
authored in `codex-marketplace/custody-pack-registry.json` under each pack
bundle's `entries` array. See `../AGENTS.md` "Skill-to-pack assignment chain"
for the edit-to-projection pipeline. Do not hand-edit
`references/bundle-manifest.json` or `references/source-map.md` in plugin
directories — they are regenerated from the registry by
`py -3 tools/rebuild_marketplace.py`.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Routing pointers

- `../AGENTS.md` before plugin-root or bundle-manifest changes
- `../../tools/AGENTS.md` before changing projection or validation behavior
- `../../docs/custody-and-projection-doctrine.md` before any projection or provenance claim changes

## Manifest guidance

Bundle-manifest entries for imported or retained projection content must declare
`content_mode`.

- `verbatim` means the retained source snapshot content and the projected plugin
  content must remain byte/hash equivalent.
- `normalised` means minimal compliance adaptation only (codex-safe shape,
  openai-spec compliance, rich metadata, repointing moved-file links). The skill
  body is unchanged beyond link repointing. Ownership stays with the upstream
  author. The entry must carry an explicit adaptation note naming the
  normalisation scope.
- `adapted` means substantive skill body changes beyond compliance. Equality is
  not expected, but the entry must carry an explicit adaptation note and a
  provenance trail.
- First-party entries are always `verbatim`. If a first-party skill needs to
  change, fix the source under `sources/first_party/` and regenerate.
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
- Flag any source-tree `skill.zip` file. Canonical install archives are
  derived from the staged Codex projection, not committed by hand.

## Maintenance responsibility

This file must stay aligned with `codex-marketplace/plugin-roots.json`. When adding,
removing, or reordering plugin roots, update the JSON inventory first—this AGENTS.md
should not hardcode root names or counts. Review this file when the marketplace shape
changes or when validation rules evolve.
