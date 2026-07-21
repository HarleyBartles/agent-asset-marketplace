# House Skills Plugin Bundle

This plugin is the current first-party House Skills plugin root.
It exposes the 51 first-party skill roots as real plugin folders under
`skills/<skill-name>/`, with each current skill root carrying its own
references, assets, scripts, and changelog notes.
It is first-party Harley-owned source prepared to stay clean enough for a future
permissive publication decision, with no unlicensed third-party bundled
content.
It includes `using-github` as the generic GitHub proof base skill,
`unslop-plus` as the repo-specific anti-slop guard skill,
`linear-issue-shaping` as the Linear issue and track shaping skill,
`risk-gates` as the consolidated pre-action risk gate router,
`connector-safety` as a shared base/control-plane safety component for
side-effecting connector/tool work, `base-doctrine` and
`bootstrap-router` as the shared base/control-plane routers,
the current `asset-market` base/control-plane skill root, and the hydrated Wild Bunch first-party roots.
`connector-safety` and `using-github` now project from `sources/first_party/skills/<skill-name>/`
instead of claiming House Skills as their canonical source authority.

Bundle identity:

- plugin name: `house-skills`
- bundle version: `1.0.0`
- marketplace source: `.agents/plugins/marketplace.json`
- bundle root: `codex-marketplace/plugins/house-skills/`
- generator: `tools/generate_marketplace.py`
- validator: `tools/validate_marketplace.py`

What lives here:

- `.codex-plugin/plugin.json` gives the plugin its installable identity.
- `SOURCE.md` records the current-source shape and archive boundary.
- `LICENSE` captures the first-party rights notice for the plugin surface.
- `CHANGELOG.md` records bundle-level shape changes.
- `skills/house-skills/SKILL.md` explains the bundle control plane.
- `skills/<skill-name>/` contains the real current first-party skill roots.
- `references/bundle-manifest.json` captures the current skill inventory.
- `provenance/house-skills.md` records the archive note and source-history context.
- `tools/generate_marketplace.py` regenerates the marketplace export from the local plugin metadata.
- `tools/validate_marketplace.py` checks the export, plugin manifest, bundle manifest, and current plugin-root path references.

The active House Skills inventory lives in `codex-marketplace/plugins/house-skills/skills/`.
