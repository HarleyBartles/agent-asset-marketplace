# agent-asset-marketplace

Canonical source of truth for an agent/plugin asset marketplace.

This repository represents an agent/plugin asset marketplace.

Primary deliverables are market-consumable assets, especially Codex plugin-market
assets where applicable. Supporting surfaces such as provenance, ledgers, indexes,
and validation helpers exist to preserve source, traceability, and review
context. They do not substitute for vendored marketplace assets.

Canonical repo-resident `skill.zip` artifacts, when present, live under
`generated/skill-zips/<pack-or-plugin>/<skill-name>/skill.zip` with a registry at
`generated/skill-zips/registry.json`. The package tooling is the normal writer
for that surface.

The active marketplace root inventory is editable at
`codex-marketplace/plugin-roots.json`. Workers should update that inventory,
the relevant source/projection files, and then run
`py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>` for a targeted
refresh. Use `--all` only for an explicit full regeneration.

The boring goal for upstream drains is simple: take useful upstream plugin-market
assets and put them into this repo's plugin market when rights and source shape
allow it. Preserve license, attribution, source mapping, and validation evidence
alongside the assets.

A repository-browser-discoverable markdown note is not a completed marketplace
asset.

## Source of truth

This repo is the authoring and review source of truth for marketplace assets.

Deployment targets, exports, and runtime packaging outputs are downstream artifacts. They should be derived from the tracked sources here, never edited as the primary copy.

## Marketplace asset flow

Market-facing Codex/plugin assets live under the marketplace/plugin surfaces in this repo.
For this normalized pass, the active plugin set is limited to the protected
roots: `codex-marketplace/plugins/house-skills`, `codex-marketplace/plugins/adventures-pack`,
`codex-marketplace/plugins/unslop`, and
`codex-marketplace/plugins/game-studio`, plus
`codex-marketplace/plugins/wild-bunch-project-pack` and
`codex-marketplace/plugins/superpowers`.

Expected flow:

1. Preserve upstream plugin/package boundaries by default.
2. Copy legally re-vendorable third-party plugin assets into the marketplace/plugin route with provenance and license evidence.
3. Update the marketplace/runtime registry or manifest required for the asset to be discoverable/installable.
4. Use `provenance/` and `sources/third_party/` to prove origin, rights, and custody.
5. Validate the repo and publish through GitHub before claiming completion.

Repacking upstream skills into a new synthetic plugin is not the default drain route. Do that only when an issue explicitly asks for a curated derivative bundle and defines the transformation contract.

## Third-party source custody

1. Keep the canonical marketplace source layout in this repo.
2. Store plugin and agent metadata in the marketplace source directories.
3. Keep `codex-marketplace/manifest.json` and the bundle manifests aligned with
   the actual plugin source tree.
4. Preserve provenance alongside any adapted or vendored plugin asset when the
   retained plugin actually depends on it.

The marketplace source tree includes real market-consumable plugin assets under
`codex-marketplace/plugins/`, with `codex-marketplace/manifest.json` exposing
the active protected plugin inventory, including the Codex-facing
`superpowers` projection.

`sources/first_party/**` is for editable first-party source custody. The
normalized House Skills source ledger lives at
`sources/first_party/skills/house-skills/`.

`sources/third_party/**` is for third-party source snapshots, references, and
custody evidence that are still required by the retained marketplace roots.
Vendored package files are source evidence and package payload. Nested files
from upstream packages should not be treated as this repo's worker doctrine
unless this repo explicitly says so.

## Provenance, license, and trust

`provenance/` tracks where assets came from, what license or usage constraints apply, what was copied or excluded, and what validation or trust assumptions apply.

A provenance note can support marketplace preservation. It is not completion by itself unless the issue explicitly asks for provenance-only work or every scoped asset has a concrete blocker.

Default posture:

- preserve attribution and license evidence;
- do not store secrets or credentials;
- do not assume an imported asset is safe without review;
- keep trust notes explicit and lightweight;
- keep source maps strong enough that a reviewer can connect upstream paths to repo-held assets.

## Directory map

- `codex-marketplace/` - marketplace source layout and active plugin source shape.
- `.agents/plugins/` - runtime plugin marketplace registry when used by current tooling.
- `sources/` - source-attribution records and retained upstream snapshots.
- `sources/first_party/` - editable first-party source custody and skill-ledger records.
- `sources/third_party/` - third-party source snapshots, references, and custody evidence for the retained marketplace roots, including the upstream `superpowers` release snapshot.
- `provenance/` - retained license, attribution, source-map, reconciliation, and trust records.
- `tools/` - helper scripts and validation tooling.
- `repo-index/` - machine-readable navigation metadata for repo traversal and future corpus prep.
