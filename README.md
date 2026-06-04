# agent-asset-marketplace

Canonical source of truth for agent-facing assets:

- GPT-native skills
- Codex plugins and marketplace metadata
- repo overlays
- provenance, licensing, and trust notes
- worker-enablement assets and generated reports

This repository is intentionally small and boring at first. It exists to define
the repository shape and the conventions that future asset intake and
publishing flows will follow.

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

## Codex Plugin Marketplace Flow

Codex marketplace assets live under `codex-marketplace/`.

Expected flow:

1. Keep the canonical marketplace source layout in this repo.
2. Store plugin and agent metadata in the marketplace source directories.
3. Derive any publishable or installed form from these sources.

The initial manifest is a placeholder only. No third-party plugin content is
included yet.

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
