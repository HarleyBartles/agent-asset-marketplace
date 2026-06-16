# House Skills Plugin Bundle

This plugin is the current first-party House Skills plugin root.
It exposes the 58 first-party skill roots as real plugin folders under
`skills/<skill-name>/`, with each current skill root carrying its own
references, assets, scripts, and changelog notes.
It is first-party Harley-owned source prepared to stay clean enough for a future
permissive publication decision, with no unlicensed third-party bundled
content.
It includes `github-operations` as the generic GitHub proof base skill,
`github-superpowers` as the GitHub-facing compositional workflow skill,
`unslop-superpowers` as the repo-specific anti-slop guard skill,
`codex-repo-receipts` as the durable repo-receipt skill,
`codex-receipts-superpowers` as the repo-backed planning and receipt
composition skill,
`boring-loop` as the shared boring-loop coordinator,
`connector-safety` as a shared base/control-plane safety component for
side-effecting connector/tool work, `base-doctrine` and
`bootstrap-router` as the shared base/control-plane routers,
`rooms-canon-buster` as a Rooms canon-pressure overlay, the newly landed
`asset-market`, `skill-installer`, `skill-handoff`, `linear-superpowers`,
and `unslop-superpowers` base/control-plane skill roots, and the hydrated
Wild Bunch first-party roots.

Bundle identity:

- plugin name: `house-skills`
- bundle version: `1.0.0`
- marketplace source: `.agents/plugins/marketplace.json`
- bundle root: `codex-marketplace/plugins/house-skills/`
- human registry source: `sources/first_party/skills/house-skills/decisions.md`
- structured archive ledger: `sources/first_party/skills/house-skills/decisions.json`
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
