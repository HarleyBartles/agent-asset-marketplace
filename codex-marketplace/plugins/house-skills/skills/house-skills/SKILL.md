---
name: house-skills
description: Use when repo-local Codex marketplace bundle for the current House Skills
  plugin root. Use this bundle when you need the installable current roots, bundle
  version, or source map for the House Skills marketplace surface. Treat the live
  plugin root as the source of truth for current skills and the archive ledger as
  historical custody.
metadata:
  source-id: house-skills
  source-path: sources/first_party/skills/house-skills/SKILL.md
  provenance-name: House Skills first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when repo-local Codex marketplace bundle for the current House Skills
    plugin root. Use this bundle when you need the installable current roots, bundle
    version, or source map for the House Skills marketplace surface. Treat the live
    plugin root as the source of truth for current skills and the archive ledger as
    historical custody.
  use_when:
  - Use when repo-local Codex marketplace bundle for the current House Skills plugin
    root. Use this bundle when you need the installable current roots, bundle version,
    or source map for the House Skills marketplace surface. Treat the live plugin
    root as the source of truth for current skills and the archive ledger as historical
    custody.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# House Skills Bundle

This skill is the installable bundle control plane for the current House Skills plugin root.
It governs the active first-party House Skills projection roots as real skill folders under `codex-marketplace/plugins/house-skills/skills/<skill-name>/`.

Use it when you need to understand:

- the plugin identity and current shape;
- where the local marketplace entry lives;
- which current skill roots live in the plugin tree;
- the `github-operations`, `asset-market`, `linear-issue-shaping`, and `verification-before-completion` roots that now live as current control-plane skills;
- how to separate historical archive custody from the live plugin surface.

## Bundle contract

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace registry: `.agents/plugins/marketplace.json`
- Current projection roots: `codex-marketplace/plugins/house-skills/skills/`
- Plugin manifest: `codex-marketplace/plugins/house-skills/.codex-plugin/plugin.json`
- Bundle manifest: `references/bundle-manifest.json`
- Human source map: `references/source-map.md`

## Source boundary

The bundle's live projection surface is `codex-marketplace/plugins/house-skills/skills/`.

The historical source ledger remains:

- `sources/first_party/skills/house-skills/intake.json`
- `provenance/house-skills.md`

The bundle does not replace the archived source ledger. Current version lives in each skill's root `SKILL.md` frontmatter, with historical residue folded into `CHANGELOG.md` and preserved support files instead of live `v*` package directories.

## Shared loop control

- `sources/first_party/skills/verification-before-completion`

Marketplace exports are generated, not hand-edited:

- edit the live plugin roots in `codex-marketplace/plugins/house-skills/skills/<skill-name>/`;
- regenerate `.agents/plugins/marketplace.json` with `tools/generate_marketplace.py`;
- verify the result with `tools/validate_marketplace.py`.

## Versioning rule

Bundle versioning is separate from component versioning.

- Component history remains in changelogs and archived source custody.
- The source map keeps the current root set boring and explicit.

## Lane map

The bundle intentionally groups the current House Skills in the current boring lanes used by the historical source ledger:

- Base and control plane
- Rooms
- Wild Bunch

The base/control-plane lane also carries the shared `connector-safety` component so connector and tool work stays narrow, recoverable, and auditable.

The Rooms lane also carries `risk-gates` (rooms canon gate) as the Rooms canon-pressure overlay alongside the existing Rooms project and source-routing skills.

For the exact current component list, open `references/bundle-manifest.json` or `references/source-map.md`.
