# House Skills Plugin Bundle

This plugin is the current first-party House Skills plugin root.
It exposes the 45 first-party skill roots as real plugin folders under
`skills/<skill-name>/`, with each current skill root carrying its own
references, assets, scripts, and changelog notes.
It is first-party Harley-owned source prepared to stay clean enough for a future
permissive publication decision, with no unlicensed third-party bundled
content.
It includes `connector-safety` as a shared base/control-plane safety component
for side-effecting connector/tool work, `rooms-canon-buster` as a Rooms
canon-pressure overlay, and the newly landed `asset-market`,
`skill-installer`, and `skill-handoff` base/control-plane skill roots.

Bundle identity:

- plugin name: `house-skills`
- bundle version: `1.0.0`
- marketplace source: `.agents/plugins/marketplace.json`
- bundle root: `codex-marketplace/plugins/house-skills/`
- human registry source: `sources/house-skills/decisions.md`
- structured archive ledger: `sources/house-skills/decisions.json`
- generator: `tools/generate_marketplace.py`
- validator: `tools/validate_marketplace.py`

What lives here:

- `.codex-plugin/plugin.json` gives the plugin its installable identity.
- `SOURCE.md` records the current-source shape and archive boundary.
- `LICENSE` captures the first-party rights notice for the plugin surface.
- `CHANGELOG.md` records bundle-level shape changes.
- `skills/house-skills/SKILL.md` explains the bundle control plane.
- `skills/<skill-name>/` contains the real current first-party skill roots.
- `skills/house-skills/references/bundle-manifest.json` captures the current skill inventory.
- `provenance/house-skills.md` records the archive note and source-history context.
- `tools/generate_marketplace.py` regenerates the marketplace export from the local plugin metadata.
- `tools/validate_marketplace.py` checks the export, plugin manifest, bundle manifest, and current plugin-root path references.

The active House Skills inventory lives in `codex-marketplace/plugins/house-skills/skills/`.
