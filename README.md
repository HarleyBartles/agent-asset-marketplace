# agent-asset-marketplace

This repository represents an agent/plugin asset marketplace.

The primary deliverable is market-consumable assets, especially Codex/plugin marketplace assets. Provenance, catalogs, ledgers, reports, doctrine notes, indexes, and discovery records are support evidence only. They do not substitute for vendored marketplace assets.

The boring goal for upstream drains is simple: take useful upstream plugin-market assets and put them into this repo's plugin market when rights and source shape allow it. Preserve license, attribution, source mapping, and validation evidence alongside the assets.

## Source of truth

This repo is the authoring and review source of truth for marketplace assets.

Deployment targets, exports, and runtime packaging outputs are downstream artifacts. They should be derived from the tracked sources here, never edited as the primary copy.

## Marketplace asset flow

Market-facing Codex/plugin assets live under the marketplace/plugin surfaces in this repo.

Expected flow:

1. Preserve upstream plugin/package boundaries by default.
2. Copy legally re-vendorable third-party plugin assets into the marketplace/plugin route with provenance and license evidence.
3. Update the marketplace/runtime registry or manifest required for the asset to be discoverable/installable.
4. Use `provenance/` and `sources/vendor/` to prove origin, rights, and custody.
5. Validate the repo and publish through GitHub before claiming completion.

Repacking upstream skills into a new synthetic plugin is not the default drain route. Do that only when an issue explicitly asks for a curated derivative bundle and defines the transformation contract.

## GPT-native skill flow

GPT-native skills live under `gpt-skills/` as source assets and supporting metadata.

`gpt-skills/house-skills/` is reserved for Harley-authored first-party GPT skills only. Third-party-origin material, including material adapted from upstream plugins or skill repositories, does not belong in House Skills.

## Third-party source custody

`sources/vendor/**` is for third-party source snapshots, references, and custody evidence.

Vendored package files are source evidence and package payload. Nested files from upstream packages should not be treated as this repo's worker doctrine unless this repo explicitly says so.

## Provenance, license, and trust

`provenance/` tracks where assets came from, what license or usage constraints apply, what was copied or excluded, and what validation or trust assumptions apply.

A provenance note can support marketplace preservation. It is not completion by itself unless the issue explicitly asks for provenance-only work or every scoped asset has a concrete blocker.

Default posture:

- preserve attribution and license evidence;
- do not store secrets or credentials;
- do not assume an imported asset is safe without review;
- keep trust notes explicit and lightweight;
- keep source maps strong enough that a reviewer can connect upstream paths to repo-held assets.

## Repo overlay role

`repo-overlays/` is for repository-specific adjustments that adapt a canonical asset to a destination repo without mutating the upstream source asset.

Use overlays for small, explicit deltas such as path mapping, naming adjustments, workspace-specific glue, and deployment-time overrides.

If an asset needs to change for everyone, change the source asset instead of adding a broad overlay.

## Generated artifact policy

`generated/` is for derived outputs only.

Policy:

- generated files are not the source of truth;
- generated reports may be ignored by default;
- committed generated outputs should be rare and intentional;
- temporary packages, caches, and local tooling artifacts stay out of source.

## Directory map

- `codex-marketplace/` - marketplace source layout and plugin source shape.
- `.agents/plugins/` - runtime plugin marketplace registry when used by current tooling.
- `gpt-skills/` - GPT-native skill sources and supporting notes.
- `gpt-skills/house-skills/` - Harley-authored first-party GPT skills only.
- `sources/vendor/` - third-party source custody and source snapshots.
- `provenance/` - license, attribution, source-map, reconciliation, and trust records.
- `repo-overlays/` - destination-specific overlays.
- `tools/` - helper scripts and validation tooling.
- `generated/reports/` - derived reports and validation output.
