---
name: adventures-pack
description: Project-scoped Adventures bundle projection for the clean active House Skills line plus the boring base dependencies required to use it sensibly. This bundle is a projection over canonical House Skills sources, not a new source of truth.
---

# Adventures Pack

Use this bundle when you need the installable Adventures project projection.

## Bundle contract

- Bundle name: `adventures-pack`
- Bundle version: `1.0.0`
- Canonical source root: `plugins/house-skills/skills`
- Marketplace registry: `.agents/plugins/marketplace.json`

## Operating rule

The bundle projects clean active Adventures skills and the generic helper
skills they depend on.

It does not reintroduce retired v1 surface area or any image-generation
scarcity doctrine.

## Stage boundaries

Keep deterministic planning, source discovery, QA, image readiness,
generation/editing, asset-sheet compilation, package work, and acceptance as
separate lanes.

## Source map

Open `references/bundle-manifest.json` for the component list and
`references/source-map.md` for the canonical path mapping.
