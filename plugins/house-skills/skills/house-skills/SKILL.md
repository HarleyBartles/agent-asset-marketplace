---
name: house-skills
description: Repo-local Codex marketplace bundle for reviewed House Skills source records. Use this bundle when you need the installable projection, bundle version, or source map for the House Skills marketplace surface. Do not treat the bundle as the source of truth; use the source catalog for the authoritative inventory.
---

# House Skills Bundle

This skill is the installable bundle control plane for the reviewed House Skills projection.

Use it when you need to understand:

- the bundle identity and version;
- where the local marketplace entry lives;
- which source records the bundle projects;
- how to separate bundle versioning from component skill versioning.

## Bundle contract

- Bundle name: `house-skills`
- Bundle version: `1.0.0`
- Marketplace registry: `.agents/plugins/marketplace.json`
- Plugin manifest: `plugins/house-skills/.codex-plugin/plugin.json`
- Bundle manifest: `references/bundle-manifest.json`
- Human source map: `references/source-map.md`

## Source boundary

The bundle projects reviewed House Skills from `gpt-skills/house-skills/`.

The authoritative source ledger remains:

- `sources/house-skills/decisions.json`
- `sources/house-skills/decisions.md`
- `sources/house-skills/intake.json`
- `provenance/house-skills.md`

The bundle does not replace those files. It only points at them and packages a local marketplace surface around them.

## Versioning rule

Bundle versioning is separate from component versioning.

- Bundle version changes when the marketplace projection changes.
- Component versions remain whatever the imported source records already declare.
- The source map keeps the component set boring and explicit.

## Lane map

The bundle intentionally projects the reviewed House Skills in the same three boring lanes used by the source ledger:

- Base and control plane
- Adventures and PIG
- Rooms

For the exact component list, open `references/bundle-manifest.json` or `references/source-map.md`.
