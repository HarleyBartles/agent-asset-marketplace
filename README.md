# agent-asset-marketplace

Canonical source of truth for an agent/plugin asset marketplace.

Primary deliverables are market-consumable assets, especially Codex plugin-market
assets where applicable. Supporting surfaces such as provenance, catalogs,
ledgers, reports, doctrine notes, and indexes exist to preserve source,
traceability, and review context. They do not substitute for vendored marketplace
assets.

A repository-browser-discoverable markdown note is not a completed marketplace
asset.

## Source Of Truth

This repo is the authoring and review source of truth.

Deployment targets, exports, and runtime packaging outputs are downstream
artifacts. They should be derived from the tracked sources here, never edited as
the primary copy.

## GPT-Native Skill Flow

GPT-native skills live under `gpt-skills/` as source assets and supporting
metadata.

Expected flow:

1. Author or update the skill in source form here.
2. Record provenance and license notes in `provenance/` when needed.
3. Generate any deployment-specific output into a downstream target, not back
   into the source tree.

No skill packaging is performed in this initialization.

First-party worker playbooks and workflow habits live in `docs/worker-playbooks.md`.
They adapt the reusable Superpowers workflow core from
`sources/vendor/obra/superpowers/v5.1.0/` into repo-local guidance without
copying the upstream harness prose wholesale.

## Codex Plugin Marketplace Flow

Codex marketplace assets live under `codex-marketplace/`.

Expected flow:

1. Keep the canonical marketplace source layout in this repo.
2. Store plugin and agent metadata in the marketplace source directories.
3. Keep `codex-marketplace/manifest.json` and the bundle manifests aligned with
   the actual plugin source tree.
4. Preserve provenance alongside any adapted or vendored plugin asset.

The marketplace source tree includes real market-consumable plugin assets under
`codex-marketplace/plugins/`, with `codex-marketplace/manifest.json` exposing the
current plugin inventory.

## Repo Overlay Role

`repo-overlays/` is for repository-specific adjustments that adapt a canonical
asset to a destination repo without mutating the upstream source asset.

Use overlays for small, explicit deltas:

- path mapping
- naming adjustments
- workspace-specific glue
- deployment-time overrides

If an asset needs to change for everyone, change the source asset instead of
adding a broad overlay.

## Provenance, License, And Trust

`provenance/` is where we track where an asset came from, what license or usage
constraints apply, and what trust assumptions are acceptable.

Default posture:

- prefer first-party or clearly attributable inputs
- do not store secrets or credentials
- do not assume an imported asset is safe without review
- keep trust notes explicit and lightweight

## Generated Artifact Policy

`generated/` is for derived outputs only.

Policy:

- generated files are not the source of truth
- generated reports may be ignored by default
- committed generated outputs should be rare and intentional
- temporary packages, caches, and local tooling artifacts stay out of source

## Directory Map

- `gpt-skills/` - GPT-native skill sources and supporting notes
- `codex-marketplace/.agents/plugins/` - Codex-native agent/plugin source shape
- `codex-marketplace/plugins/` - marketplace plugin source shape
- `repo-overlays/` - destination-specific overlays
- `sources/` - upstream references and source snapshots
- `tools/` - small helper scripts only, if needed
- `generated/reports/` - derived reports and validation output
- `provenance/` - license, attribution, and trust records

## Initialization Boundary

This commit only establishes the canonical repository shape and conventions.
It does not ingest external assets, build a framework, or add runtime tooling.
