# House Skills Plugin Bundle

This plugin is the repo-local marketplace projection for the reviewed House Skills source catalog.
It uses unversioned active House Skill roots, with current version and provenance recorded in each skill's metadata and version-history reference.
It is first-party Harley-owned source prepared to stay clean enough for a future permissive publication decision, with no unlicensed third-party bundled content.
It now also projects `connector-safety` as a shared base/control-plane safety component for side-effecting connector/tool work and `rooms-canon-buster` as a Rooms canon-pressure overlay.

Bundle identity:

- plugin name: `house-skills`
- bundle version: `1.0.0`
- marketplace source: `.agents/plugins/marketplace.json`
- bundle root: `plugins/house-skills/`
- human registry source: `sources/house-skills/decisions.md`
- structured registry mirror: `sources/house-skills/decisions.json`
- generator: `tools/generate_marketplace.py`
- validator: `tools/validate_marketplace.py`

What lives here:

- `.codex-plugin/plugin.json` gives the bundle its installable identity.
- `skills/house-skills/SKILL.md` explains the bundle control plane.
- `skills/house-skills/references/bundle-manifest.json` captures the bundle-to-source mapping.
- `provenance/house-skills.md` records the projection note alongside the source ledger.
- `tools/generate_marketplace.py` regenerates the marketplace export from the local source ledger and bundle metadata.
- `tools/validate_marketplace.py` checks the export, plugin manifest, bundle manifest, and local path references.

The bundle is intentionally a projection, not the source of truth. The active House Skills inventory lives under unversioned roots in `gpt-skills/house-skills/`, and the source ledger remains the authoritative map of which reviewed skills are imported.
