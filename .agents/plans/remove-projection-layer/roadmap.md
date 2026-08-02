# Epic: Remove the projection layer

**Goal:** Delete the `sources/` custody and projection machinery; make the vendored `codex-marketplace/plugins/*/skills/` directories the canonical homes for all skills. Consumers still install skills from plugins as before, but there is no separate source/projection split inside this repo.

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|-------|--------|-----------|--------|----|--------|-------|
| 1 | Demolition pass: delete `sources/` and the custody registry | writing | `.agents/plans/remove-projection-layer/2026-08-01-remove-projection-layer.md` | — | — | — | First concrete plan |
| 2 | Retool marketplace validation and `tools/run` | pending | — | — | — | — | Keep only the plugin-root manifest flow |
| 3 | Rewrite or delete custody/projection doctrine | pending | — | — | — | — | Docs and runbook updates |
| 4 | Final green CI and mesh regeneration | pending | — | — | — | — | `tools/run ci --check` and push |

---

## Scope decisions (locked)

- `sources/first_party/skills/` is removed. All first-party skills move to `codex-marketplace/plugins/<plugin>/skills/<skill-name>/`.
- `sources/third_party/` is removed. The vendored plugin copies are the only retained copies. Release pins move to plugin manifest metadata.
- `codex-marketplace/custody-pack-registry.json` is removed. The `codex-marketplace/plugin-roots.json` registry and each plugin's own `.codex-plugin/plugin.json` become the source of truth.
- Generated provenance/source maps that were derived from the custody registry are removed. Simpler plugin-level `references/source-map.md` and `references/provenance-map.json` are retained only if still generated from plugin manifests.
- `docs/custody-and-projection-doctrine.md` is deleted; the repo no longer separates custody and projection.
