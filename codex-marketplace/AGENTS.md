# AGENTS.md

Scope: `codex-marketplace/`

This scope covers the Codex marketplace source root, including the marketplace
manifest and the plugin source tree beneath it.

Codex plugin first; generated GPT-safe skill zips second.

Mesh-wise, this scope owns marketplace source/projection law, not repo-wide
navigation. Keep `AGENTS.md` compact and let generated `INDEX.md` files carry
tree coverage.

The active plugin roots in this scope are defined by
`codex-marketplace/plugin-roots.json` and validated against the protected
marketplace manifests and registry surfaces.

Those roots are installable projections only. Their editable source custody
lives under `sources/first_party/` and `sources/third_party/`.

The marketplace plugin roots are the canonical install surface. Generated
`skill.zip` files under `generated/skill-zips/` are downstream GPT exports, and
`adapters/gpt/manifest.json` decides whether each one is `direct`, `overlay`,
or `excluded`.
Use `py -3 tools/generate_marketplace.py --check` to prove
`.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` are
current, and `py -3 tools/generate_repo_index.py --check` to prove
`repo-index/repo-index.json` is current. `validate_repo_index.py` remains
alignment validation, not the freshness proof. Use
`py -3 tools/generate_index_mesh.py --check` for the repo-wide navigation mesh.

Deterministic pack rule: the editable registry file
`codex-marketplace/custody-pack-registry.json` is the source of truth for
which plugin roots are actively projected. Some nodes declare
`is_mega_pack: true` when they belong to the mega-pack lane, but
`superpowers-plus` remains the retained mixed projection-lane bundle rather
than a maintained `superpowers-mega-pack` install surface. Regenerate the
projection and export surfaces from the checked-in tooling. Do not hand-edit
bundle manifests, projected skill trees, source maps, provenance maps, or zip
artifacts, and do not introduce plugin-specific one-off scripts when the
existing pipeline can be extended or reused.

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

## Maintenance responsibility

This file must stay aligned with the marketplace structure defined in
`codex-marketplace/plugin-roots.json`. When the marketplace shape changes or
when validation rules evolve, review and update this file to reflect current
expectations. Do not let this file become stale—if agents are following patterns
that contradict this document, either update the document or update the repo
conventions to match.
