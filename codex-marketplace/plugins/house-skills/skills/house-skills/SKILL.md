---
name: house-skills
description: Repo-local Codex marketplace bundle for the current House Skills plugin root. Use this bundle when you need the installable current roots, bundle version, or source map for the House Skills marketplace surface. Treat the live plugin root as the source of truth for current skills and the archive ledger as historical custody.
metadata:
  source-id: house-skills
  source-path: codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md
  provenance-name: House Skills current root migration
license: "MIT"
---
# House Skills Bundle

This skill is the installable bundle control plane for the current House Skills plugin root.
It governs the 42 active first-party House Skills roots as real skill folders under `codex-marketplace/plugins/house-skills/skills/<skill-name>/`.

Use it when you need to understand:

- the plugin identity and current shape;
- where the local marketplace entry lives;
- which current skill roots live in the plugin tree;
- how to separate historical archive custody from the live plugin surface.

## Bundle contract

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace registry: `.agents/plugins/marketplace.json`
- Current skill roots: `codex-marketplace/plugins/house-skills/skills/`
- Historical custody: `gpt-skills/house-skills/`
- Plugin manifest: `codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json`
- Bundle manifest: `references/bundle-manifest.json`
- Human source map: `references/source-map.md`

## Source boundary

The bundle's live source surface is `codex-marketplace/plugins/house-skills/skills/`, with `gpt-skills/house-skills/` retained only as historical archive custody.

The historical source ledger remains:

- `sources/house-skills/decisions.json`
- `sources/house-skills/decisions.md`
- `sources/house-skills/intake.json`
- `provenance/house-skills.md`

The bundle does not replace the archived source ledger. Current version lives in each skill's root `SKILL.md` frontmatter, with historical residue folded into `CHANGELOG.md` and preserved support files instead of live `v*` package directories.

Marketplace exports are generated, not hand-edited:

- edit the live plugin roots in `codex-marketplace/plugins/house-skills/skills/<skill-name>/`;
- keep the historical registry in `sources/house-skills/decisions.md` and `sources/house-skills/decisions.json` as archive/provenance;
- regenerate `.agents/plugins/marketplace.json` with `tools/generate_marketplace.py`;
- verify the result with `tools/validate_marketplace.py`.

## Versioning rule

Bundle versioning is separate from component versioning.

- Component history remains in changelogs and archived source custody.
- The source map keeps the current root set boring and explicit.

## Lane map

The bundle intentionally groups the current House Skills in the same three boring lanes used by the historical source ledger:

- Base and control plane
- Adventures
- Rooms

The base/control-plane lane also carries the shared `connector-safety` component so connector and tool work stays narrow, recoverable, and auditable.

The Rooms lane also carries `rooms-canon-buster` as the Rooms canon-pressure overlay alongside the existing Rooms project and source-routing skills.

For the exact current component list, open `references/bundle-manifest.json` or `references/source-map.md`.
