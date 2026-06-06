# House Skills Plugin Bundle

This plugin is the repo-local marketplace projection for the reviewed House Skills source catalog.
It is first-party Harley-owned source prepared to stay clean enough for a future permissive publication decision, with no unlicensed third-party bundled content.

Bundle identity:

- plugin name: `house-skills`
- bundle version: `1.0.0`
- marketplace source: `.agents/plugins/marketplace.json`
- bundle root: `plugins/house-skills/`

What lives here:

- `.codex-plugin/plugin.json` gives the bundle its installable identity.
- `skills/house-skills/SKILL.md` explains the bundle control plane.
- `skills/house-skills/references/bundle-manifest.json` captures the bundle-to-source mapping.
- `provenance/house-skills.md` records the projection note alongside the source ledger.

The bundle is intentionally a projection, not the source of truth. The active House Skills inventory still lives under `gpt-skills/house-skills/` and the source ledger remains the authoritative map of which reviewed skills are imported.
