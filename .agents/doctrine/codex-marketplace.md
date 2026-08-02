
## Scope

`codex-marketplace/`

This scope covers the Codex marketplace source root, including the marketplace manifest and the plugin source tree beneath it.

Codex plugin first.

Mesh-wise, this scope owns marketplace source and plugin-curation law, not repo-wide navigation. Keep `AGENTS.md` compact and let generated `INDEX.md` files carry tree coverage.

The active plugin roots in this scope are defined by `codex-marketplace/plugin-roots.json` and validated against the protected marketplace manifests and plugin surfaces.

The canonical skill source lives under `codex-marketplace/plugins/<plugin>/skills/`; third-party upstream provenance is recorded under `provenance/` and any adaptation overlays live under `adapters/codex/`.

The marketplace plugin roots are the canonical install surface. Use `py -3 tools/run.py marketplace --apply` to regenerate all derived surfaces, `py -3 tools/run.py marketplace --check` to verify freshness, and `py -3 tools/run.py ci --check` as the non-mutating CI gate. `py -3 tools/run.py mesh --check` proves the repo-wide navigation mesh is current.

Deterministic pack rule: the editable pack metadata is `codex-marketplace/plugins/<plugin>/.codex-plugin/plugin.json` and the pack bundle manifest is `codex-marketplace/plugins/<plugin>/references/bundle-manifest.json`. Do not hand-edit bundle manifests, bundled skill trees, or installed skill surfaces; regenerate them from the canonical tooling.

## Skill-to-pack assignment chain

When a skill needs to move between packs, be added to a pack, or be removed from a pack, the editable source of truth is the `references/bundle-manifest.json` `entries` array inside each plugin. Each entry has a `canonical_name`, `canonical_source_path`, `local_path`, `content_mode`, and `provenance_note`. The chain from edit to published plugin is:

1. **Edit the plugin bundle** — add, remove, or move the entry in `codex-marketplace/plugins/<pack>/references/bundle-manifest.json`. Update `content_mode` and `provenance_note` to reflect the new pack context.
2. **Run `py -3 tools/run.py marketplace --apply`** — this regenerates all derived surfaces: plugin skill trees under `codex-marketplace/plugins/<pack>/skills/`, bundle manifests, the marketplace manifest, repo index, and the index mesh.
3. **Run `py -3 tools/run.py ci --check`** — CI gate proves all surfaces are current.

Do not hand-edit the derived surfaces (`bundle-manifest.json`, installed skill trees under `.agents/skills/`, repo index, index mesh). They are regenerated from the canonical plugin source by the rebuild pipeline.

`codex-marketplace/plugin-roots.json` defines which plugin roots exist and their order, but does not define skill-to-pack assignments — those live in each plugin's `references/bundle-manifest.json`.

Defer to the repository root `AGENTS.md` for global doctrine, publication rules, and upstream-drain policy.

## Review guidelines

- Treat `codex-marketplace/manifest.json` and `.agents/plugins/marketplace.json` as coupled surfaces; a plugin add, remove, or rename must stay aligned across both exports and the validator.
- Treat any plugin root under `codex-marketplace/plugins/` not listed in `plugin-roots.json` as inactive unless a new issue explicitly changes the marketplace shape.
- Flag broken plugin root paths, missing `.codex-plugin/plugin.json` files, and category or install-policy drift in the marketplace manifest.
- Flag missing `SOURCE.md`, `LICENSE`, or bundle-manifest references when a plugin root claims to expose them.
- Flag generated-export mismatches that would let the bundle source drift silently from the tracked marketplace source tree or Codex overlay source.
- Flag any source-tree install archive that is not a generated marketplace artifact; canonical installs come from the staged Codex plugin.
- Prefer serious packaging and discoverability issues over stylistic concerns.

## Maintenance responsibility

This file must stay aligned with the marketplace structure defined in `codex-marketplace/plugin-roots.json`. When the marketplace shape changes or when validation rules evolve, review and update this file to reflect current expectations. Do not let this file become stale—if agents are following patterns that contradict this document, either update the document or update the repo conventions to match.
