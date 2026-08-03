# Epic: Remove the projection layer

> **Status:** Completed and merged in PR #253 (`feat/remove-projection-layer`, `417e7f97b80803437f2d1a9966200874291d0021`) on 2026-08-01. This roadmap is a historical record; the original Phase 1 plan and this roadmap live in `.agents/plans/completed/`.

**Goal:** Delete the `sources/` custody and projection machinery; make the vendored `codex-marketplace/plugins/*/skills/` directories the canonical homes for all skills. Consumers still install skills from plugins as before, but there is no separate source/projection split inside this repo.

| # | Title | Status | Plan File | Commit | PR | Rating | Notes |
|---|-------|--------|-----------|--------|----|--------|-------|
| 1 | Demolition pass: delete `sources/` and the custody registry | done | `.agents/plans/completed/2026-08-01-remove-projection-layer.md` | `1e580775646307f007508f6ec3a7da1e79123480` | #253 | 8/10 | Merged to `main` as part of PR #253. |
| 2 | Retool marketplace validation and `tools/run` | done | `.agents/plans/completed/2026-08-01-remove-projection-layer-roadmap.md` | `85b1edd50118179d30c916a3e17be8cd6f413b1d` | #253 | 8/10 | Validator and `run` targets were retooled in the same PR. |
| 3 | Rewrite or delete custody/projection doctrine | done | `.agents/plans/completed/2026-08-01-remove-projection-layer-roadmap.md` | `a881f48a520dd8c65ddbb68e7b184fce212301f4` | #253 | 8/10 | Doctrine and provenance updated; custody/projection doc removed. |
| 4 | Final green CI and mesh regeneration | done | `.agents/plans/completed/2026-08-01-remove-projection-layer-roadmap.md` | `e927c3ff00b0c783a2866d668850d6967d431b18` | #253 | 8/10 | `ci --check` and `mesh --apply` passed before merge. |

---

## Scope decisions (locked)

- `sources/first_party/skills/` is removed. All first-party skills move to `codex-marketplace/plugins/<plugin>/skills/<skill-name>/`.
- `sources/third_party/` is removed. The vendored plugin copies are the only retained copies. Release pins move to plugin manifest metadata.
- `codex-marketplace/custody-pack-registry.json` is removed. The `codex-marketplace/plugin-roots.json` registry and each plugin's own `.codex-plugin/plugin.json` become the source of truth.
- Generated provenance/source maps that were derived from the custody registry are removed. Simpler plugin-level `references/source-map.md` and `references/provenance-map.json` are retained only if still generated from plugin manifests.
- `docs/custody-and-projection-doctrine.md` is deleted; the repo no longer separates custody and projection.
