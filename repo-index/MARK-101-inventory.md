# MARK-101 Repo Inventory

## Method

I scanned the repo doctrine and the current marketplace/source surfaces directly:

- `AGENTS.md`
- `gpt-skills/AGENTS.md`
- `gpt-skills/house-skills/AGENTS.md`
- `codex-marketplace/AGENTS.md`
- `codex-marketplace/plugins/AGENTS.md`
- `plugins/house-skills/AGENTS.md`
- `repo-index/README.md`
- `repo-index/repo-index.json`
- `.agents/plugins/marketplace.json`
- `codex-marketplace/manifest.json`
- `sources/house-skills/decisions.md`
- `sources/house-skills/decisions.json`
- `sources/house-skills/intake.json`
- `provenance/house-skills.md`
- `tools/validate_repo_index.py`
- `tools/validate_marketplace.py`
- `tools/marketplace_utils.py`
- `tools/generate_marketplace.py`

I also checked path existence and support-file presence for the registry-backed plugin roots and the immediate skill roots under:

- `gpt-skills/house-skills/`
- `plugins/house-skills/skills/`
- `codex-marketplace/plugins/*/skills/`

I did not normalize, delete, move, flatten, package, reinstall, reset, quarantine, or otherwise clean up assets.

## Executive assessment

- The marketplace registry is currently stable and mirrored: `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` both expose 354 plugins.
- The House Skills source tree is healthy at the active-root level: 42 immediate roots under `gpt-skills/house-skills`, and every one has `SKILL.md` plus frontmatter metadata.
- The highest-signal projections are `plugins/house-skills`, `codex-marketplace/plugins/adventures-pack`, `codex-marketplace/plugins/game-studio`, and `codex-marketplace/plugins/wild-bunch-project-pack`.
- `adventures-pack` and `plugins/house-skills` are projections over canonical source roots.
- `game-studio` is an imported upstream plugin pack.
- `wild-bunch-project-pack` is a first-party pack that reuses `game-studio` skills and shared helpers, so it is a derived projection rather than canonical source.

## Source surfaces

| Surface | Role | Observed state |
| --- | --- | --- |
| `.agents/plugins/marketplace.json` | Runtime registry mirror | Matches `codex-marketplace/manifest.json` and the plugin scan. |
| `codex-marketplace/manifest.json` | Source marketplace manifest | Matches the runtime registry mirror. |
| `sources/house-skills/decisions.md` | Human source ledger | Lists 42 imported House Skills records and the boundary row. |
| `sources/house-skills/decisions.json` | Structured source ledger mirror | Mirrors the markdown ledger. |
| `sources/house-skills/intake.json` | Intake/projection mirror | Records the same imported set used by the bundle projection. |
| `provenance/house-skills.md` | Evidence and traceability | Documents source/projection history and the current bundle projection. |
| `plugins/house-skills/` | Repo-local House Skills projection | Installable bundle control plane, not source of truth. |
| `codex-marketplace/plugins/adventures-pack/` | Project-scoped House Skills projection | Installable Adventures bundle with version-suffixed component paths. |
| `codex-marketplace/plugins/game-studio/` | Imported upstream plugin pack | Adapted vendor root with copied skill tree. |
| `codex-marketplace/plugins/unslop/` | Adapted upstream plugin pack | Reimplemented skill package with vendor custody and a bundle manifest. |
| `codex-marketplace/plugins/wild-bunch-project-pack/` | First-party project pack | Self-contained pack that copies selected marketplace skills and adds first-party guidance. |

## Plugin root inventory

### Registry-wide summary

- Total plugin roots exposed by the current marketplace registry: `354`
- Plugin roots with `.codex-plugin/plugin.json`: `354`
- Plugin roots with `README.md`: `354`
- Plugin roots with `SOURCE.md`: `353`
- Plugin roots with `LICENSE`: `353`
- Plugin roots with `assets/`: `354`
- Plugin roots with `skills/`: `243`
- Plugin roots with `references/bundle-manifest.json`: `228`
- Plugin roots with a local `AGENTS.md`: `3`

### Notable roots

| Plugin root | `.codex-plugin/plugin.json` | `README.md` | `SOURCE.md` | `LICENSE` | `assets/` | `skills/` | `references/bundle-manifest.json` | Local `AGENTS.md` | Assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `plugins/house-skills` | yes | yes | no | no | yes | yes | no | yes | Aggregate House Skills projection. Intentionally thin and not canonical source. |
| `codex-marketplace/plugins/adventures-pack` | yes | yes | yes | yes | yes | yes | yes | no | Project-scoped House Skills projection. Bundle manifest and source map carry the contract. |
| `codex-marketplace/plugins/game-studio` | yes | yes | yes | yes | yes | yes | yes | no | Imported upstream plugin pack. Thin copied skill tree with normalized marketplace packaging. |
| `codex-marketplace/plugins/unslop` | yes | yes | yes | yes | yes | yes | yes | no | Adapted upstream plugin pack. Vendor custody and bundle manifest are explicit. |
| `codex-marketplace/plugins/wild-bunch-project-pack` | yes | yes | yes | yes | yes | yes | no | no | First-party project pack that copies marketplace skills and adds its own guidance. |

### Notable plugin-root observations

- `plugins/house-skills` is the only plugin root missing both `SOURCE.md` and `LICENSE`. That is expected for an aggregate projection surface, not a source package.
- `codex-marketplace/plugins/adventures-pack` and `codex-marketplace/plugins/game-studio` both have bundle manifests, but they differ in purpose: Adventures is a local projection over House Skills, while Game Studio is a copied upstream market plugin.
- `codex-marketplace/plugins/unslop` is an adapted upstream package, but it still keeps a clear vendor custody path and a bundle manifest, so it is protected rather than disposable.
- `codex-marketplace/plugins/wild-bunch-project-pack` has a clear first-party purpose even though it does not carry a bundle manifest. Its provenance map documents the copied marketplace skill split.

## Skill root inventory

### House Skills source tree

| Surface | Immediate roots | `SKILL.md` | Frontmatter | `references/` | `assets/` | `scripts/` | `CHANGELOG.md` | Assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gpt-skills/house-skills/` | 42 | 42 | 42 | 41 | 24 | 2 | 0 | Active House Skills source tree. Unversioned roots are the active surface. |
| `plugins/house-skills/skills/` | 1 | 1 | 1 | 1 | 0 | 0 | 0 | Bundle wrapper only. The skill root is a projection control plane, not source of truth. |

Immediate House Skills roots with version folders beneath them:

- `adventures-asset-sheet-compiler`
- `adventures-bootstrap`
- `adventures-frame-buster`
- `adventures-github-operations`
- `adventures-image-qa`
- `adventures-project-doctrine`
- `adventures-storyboard-preflight`
- `adventures-visual-bible-creator`
- `adventures-visual-bible-interpreter`
- `adventures-visual-preproduction`
- `gpt-base-doctrine`
- `session-buster`
- `session-buster-ingress`

Immediate House Skills roots without version folders beneath them:

- `ambiguity-buster`
- `analogy-buster`
- `boring-buster`
- `buster-framework`
- `canon-buster`
- `cleanup-custody`
- `connector-safety`
- `crew`
- `crew-buster`
- `don-logan-boundary`
- `invariant-buster`
- `linear`
- `rooms-ambiguity-buster`
- `rooms-analogy-buster`
- `rooms-bootstrap`
- `rooms-canon-buster`
- `rooms-character-investigation`
- `rooms-image-sidecars`
- `rooms-project-doctrine`
- `rooms-sheet-creator`
- `rooms-source-partitioning`
- `rooms-zoom-outs-buster`
- `skill-buster`
- `skill-packager`
- `skill-validator`
- `tps-ingress`
- `tps-reporting`
- `work-mode-router`
- `worker-dispatch-linear`

### Project and imported skill roots

| Surface | Immediate roots | `SKILL.md` | Frontmatter | `references/` | `assets/` | `scripts/` | `agents/` | Assessment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `codex-marketplace/plugins/adventures-pack/skills/` | 18 | 18 | 18 | 0 | 0 | 0 | 0 | Thin bundle wrapper plus 17 version-suffixed components. The support contract lives in the bundle manifest and source map. |
| `codex-marketplace/plugins/game-studio/skills/` | 9 | 9 | 9 | 0 | 0 | 0 | 9 | Thin copied upstream skill tree. Every skill has `agents/` and no local `references/` or `assets/`. |
| `codex-marketplace/plugins/wild-bunch-project-pack/skills/` | 15 | 15 | 15 | 7 | 1 | 0 | 15 | First-party project pack with copied marketplace skills and first-party Wild Bunch guidance. |
| `codex-marketplace/plugins/unslop/skills/unslop` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | Adapted skill package with scripts, profiles, references, and vendor-backed evidence. |

## Versioning and projection residue

The current repo convention is consistent: the active House Skills live at unversioned roots in `gpt-skills/house-skills/`, while versioned material lives under nested historical folders or projected bundle paths.

Observed residue patterns:

- `gpt-skills/house-skills` has 13 roots with nested version folders.
- Those version folders use `v1`, `v1.1`, or `v0.1`.
- The active root name stays unversioned even when the historical folder is versioned.
- `codex-marketplace/plugins/adventures-pack` intentionally projects version-suffixed local paths like `skills/adventures-visual-preproduction-v1.1/SKILL.md`.
- `codex-marketplace/plugins/game-studio` and `codex-marketplace/plugins/wild-bunch-project-pack` both mirror upstream or copied skill trees without needing version-suffixed local paths in the same way.

Sampled historical folders that carry the richer package shape:

- `gpt-skills/house-skills/adventures-visual-preproduction/v1/adventures-visual-preproduction-v1`
- `gpt-skills/house-skills/gpt-base-doctrine/v1.1/gpt-base-doctrine-v1.1`
- `gpt-skills/house-skills/session-buster/v0.1/session-buster-v0.1`

Those sampled folders still carry `agents/`, `assets/`, and `references/` alongside `SKILL.md`, which confirms they are archive-style versioned packages rather than fresh active roots.

## First-party House Skills assessment

| Classification | Roots | Assessment |
| --- | --- | --- |
| Current active root appears complete | 42/42 | Every active House Skills root has `SKILL.md` and frontmatter. No malformed immediate root was found. |
| Current active root appears thin or support-file incomplete | 1/42 | `connector-safety` is the leanest active root because it has no `references/`. That looks intentional, but it is the first one I would compare by hand if a child issue wants a content review. |
| Projected copy differs from source root | 0 in `gpt-skills/house-skills` itself | Projection differences live in `plugins/house-skills` and the marketplace packs, not in the source tree. |
| Source ledger/projection path is ambiguous | 0 obvious cases | The source ledger, intake mirror, and bundle manifest all point at the same active unversioned roots. |
| Needs deeper manual comparison | A few history-sensitive roots | `gpt-base-doctrine`, `session-buster`, `rooms-bootstrap`, and `rooms-canon-buster` have extra provenance/history notes and are worth a direct diff if version drift matters. |

Observed first-party pattern:

- The current source tree is source-complete at the root level.
- The versioned folders are historical residue, not active source identities.
- The source ledger and bundle projection agree on the active unversioned root names.

## Adventures pack assessment

`codex-marketplace/plugins/adventures-pack` is a project-scoped projection over the canonical House Skills source tree.

Observed facts:

- Bundle name: `adventures-pack`
- Bundle version: `1.0.0`
- Bundle type: `project-scoped-codex-plugin-projection`
- Marketplace source: `.agents/plugins/marketplace.json`
- Plugin root: `codex-marketplace/plugins/adventures-pack`
- Canonical source root: `gpt-skills/house-skills`
- Source-of-truth files: `sources/house-skills/decisions.json`, `sources/house-skills/decisions.md`, `sources/house-skills/intake.json`, `provenance/house-skills.md`
- Projected components in `references/bundle-manifest.json`: 17
- Adventures components: 10
- Dependency components: 7

Important shape details:

- The bundle manifest uses version-suffixed local paths for the projected components, such as `skills/adventures-visual-preproduction-v1.1/SKILL.md`.
- The local skill tree contains 18 roots total: 17 projected component directories plus the wrapper skill `skills/adventures-pack/SKILL.md`.
- The local skill directories are thin wrappers: they have `SKILL.md` and frontmatter, but no local `references/`, `assets/`, or `scripts/` at the skill-root level.
- The support contract for the pack lives in `SOURCE.md`, `README.md`, `references/bundle-manifest.json`, and `references/source-map.md`.

Validator behavior that matters here:

- `tools/validate_marketplace.py` hard-codes the Adventures bundle shape.
- It requires exactly 10 Adventures components and 7 dependency components.
- It also requires the projected component directories to match the source ledger order.
- That means the current version-suffixed local paths are enforced packaging shape, not an invitation to treat the versioned names as active source roots.

## Protected third-party/adapted assets

| Plugin | Upstream repo | Pinned commit | Source root | Vendor custody path | Bundle status | Imported skill count | Adaptation note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `codex-marketplace/plugins/unslop` | `mshumer/unslop` | `edcb62386d129c65e4395f0cfcc9168eb1ba2148` | `.` | `sources/vendor/mshumer/unslop/edcb62386d129c65e4395f0cfcc9168eb1ba2148/` | `references/bundle-manifest.json` present | 3 | Reimplemented the useful workflow for local sample orchestration, deterministic profile generation, output manifests, validators, and optional visual smoke checks. |
| `codex-marketplace/plugins/game-studio` | `openai/plugins` | `c33199897758cab145bb7fdab1ca8fb1cbd9de50` | `plugins/game-studio` | `sources/vendor/openai/plugins/c33199897758cab145bb7fdab1ca8fb1cbd9de50/plugins/game-studio/` | `references/bundle-manifest.json` present | 9 | Copied the upstream root tree into the marketplace surface and normalized the packaging metadata for local compatibility. |

These are protected assets for now. I documented them but did not mutate them.

## Duplicated project projections

| Relationship | Classification | Evidence |
| --- | --- | --- |
| `gpt-skills/house-skills` -> `plugins/house-skills` | Likely canonical source vs projection | The bundle README and source map say the repo-local bundle is a projection over unversioned House Skills roots, while the source ledger remains authoritative. |
| `gpt-skills/house-skills` -> `codex-marketplace/plugins/adventures-pack` | Likely projection | The bundle manifest projects 10 clean Adventures roots plus 7 dependencies and intentionally uses version-suffixed local paths. |
| `codex-marketplace/plugins/game-studio` -> `codex-marketplace/plugins/wild-bunch-project-pack` | Likely source plugin vs derived pack | Wild Bunch explicitly copies `game-studio` skills and adds first-party guidance plus copied browser-game and architecture helpers. |
| `codex-marketplace/plugins/game-studio` -> `codex-marketplace/plugins/game-studio` itself | Likely canonical adapted package | The game-studio pack is the upstream-adapted plugin that the Wild Bunch pack copies from. |
| `codex-marketplace/plugins/harley-repo-ops` -> `gpt-skills/house-skills` | Likely projection | It reuses House Skills control-plane skills, but I did not treat it as canonical source. |

Do not delete any of these on the basis of this inventory alone. They are all useful in different roles.

## Third-party/chaff candidates

The strongest candidate class is the no-skill plugin root set.

Observed counts:

- Plugin roots with no `skills/`: 111
- Plugin roots with no `references/bundle-manifest.json`: 126

Examples of no-skill roots that look like wrappers, app surfaces, or placeholder-like plugin shells:

- `actively`
- `aiera`
- `alation`
- `alpaca`
- `amplitude`
- `apollo`
- `asana`
- `attio`
- `binance`
- `biorender`

These are not automatically junk. They are just the first class I would queue for a keep/reset/quarantine review because they lack installable skill trees.

## Validator and AGENTS.md architecture assessment

### Doctrine files

| File | What it encodes | Observed consequence |
| --- | --- | --- |
| `AGENTS.md` | Repo-wide doctrine: start from fresh `main`, preserve custody, publish before claiming completion, do not cleanup/move/delete by default. | This issue correctly stayed docs-only and published only a new inventory artifact. |
| `gpt-skills/AGENTS.md` | GPT skill tree rules, including first-party-only House Skills territory. | Active House Skills remain in unversioned roots. |
| `gpt-skills/house-skills/AGENTS.md` | House Skills root rules and version-history guidance. | Imported versions are treated as historical records, not active source names. |
| `codex-marketplace/AGENTS.md` | Marketplace manifest and plugin-root review rules. | Missing `SOURCE.md`, `LICENSE`, or `.codex-plugin/plugin.json` would be a real packaging issue. |
| `codex-marketplace/plugins/AGENTS.md` | Plugin-root review rules. | Missing support files or registry drift would be flagged before stylistic concerns. |
| `plugins/house-skills/AGENTS.md` | Projection-bundle review rules. | It explicitly says the bundle is a projection and that the source ledger stays authoritative. |

### Tooling

| File | What it enforces | Notes |
| --- | --- | --- |
| `tools/validate_repo_index.py` | Repo-index paths, registry parity, and vendor guidance text. | Treats `repo-index` as navigation metadata, not source truth. |
| `tools/validate_marketplace.py` | Registry parity, source-ledger parity, bundle manifests, plugin support files, and source-map checks. | It is the current enforcement surface for the marketplace shape. |
| `tools/marketplace_utils.py` | Shared path constants and bundle manifest helpers. | It encodes the active source roots the validators expect. |
| `tools/generate_marketplace.py` | Regenerates `.agents/plugins/marketplace.json` and `codex-marketplace/manifest.json` from the source ledger. | The marketplace manifests are generated, not hand-edited. |

### Architecture notes and contradictions

- The validators intentionally teach a versioned projection shape for the bundle packs, especially `adventures-pack`.
- That is not a contradiction with the House Skills doctrine, which says the active source roots stay unversioned.
- `provenance/house-skills.md` still includes historical version-suffixed paths for archive records. That is evidence, not active inventory.
- `wild-bunch-project-pack` is the only notable local pack I found that does not carry a bundle manifest. Its provenance map is strong enough for now, but a child issue could decide whether that is an acceptable permanent shape.
- Only three plugin roots currently have local `AGENTS.md` files: `plugins/house-skills`, `codex-marketplace/plugins/pr-to-spec`, and `codex-marketplace/plugins/zoom`.

## Risks and unknowns

- The no-skill plugin class is broad. Some roots are probably real app shells, while others may be placeholders or low-value wrappers. They need child issues if anyone wants to cleanly separate keepers from reset candidates.
- `connector-safety` is the only active House Skills root without `references/`. It looks intentional, but it is the first root I would compare by hand if a content review is needed.
- `wild-bunch-project-pack` has a clear first-party purpose, but its lack of a bundle manifest means it relies on provenance notes more than the other project packs do.
- I did not deep-diff every historical version folder against the active House Skills root. The inventory only confirms the residue is present and consistent with current source-ledger paths.

## Proposed child issue boundaries

### 1. House Skills residue audit

- Title: `House Skills version-residue audit`
- Scope: Compare the 13 versioned history folders beneath `gpt-skills/house-skills` with the active unversioned roots and the source ledger.
- Paths involved: `gpt-skills/house-skills/*`, `sources/house-skills/decisions.*`, `sources/house-skills/intake.json`, `provenance/house-skills.md`
- Expected mutation class: Docs/provenance only, or no mutation if the residue is already intentional.
- Validation commands: `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_marketplace.py`, `git diff --check HEAD~1 HEAD`
- Closeout evidence: Open PR URL plus head SHA.
- Why it is boring and bounded: It is a finite 13-root comparison against one source ledger.

### 2. Adventures pack shape review

- Title: `Adventures pack wrapper and version-path review`
- Scope: Decide whether the current wrapper skill and version-suffixed local paths are the desired permanent shape for `adventures-pack`.
- Paths involved: `codex-marketplace/plugins/adventures-pack/`, `gpt-skills/house-skills/adventures-*`
- Expected mutation class: Docs and bundle-map adjustments only.
- Validation commands: `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check HEAD~1 HEAD`
- Closeout evidence: Open PR URL plus head SHA.
- Why it is boring and bounded: The pack has one manifest, one wrapper skill, and 17 projected components.

### 3. Wild Bunch projection audit

- Title: `Wild Bunch pack provenance and packaging audit`
- Scope: Reconcile the copied `game-studio` roots, the first-party Wild Bunch skill set, and the missing bundle-manifest shape.
- Paths involved: `codex-marketplace/plugins/wild-bunch-project-pack/`, `codex-marketplace/plugins/game-studio/`
- Expected mutation class: Docs/projection packaging only.
- Validation commands: `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check HEAD~1 HEAD`
- Closeout evidence: Open PR URL plus head SHA.
- Why it is boring and bounded: It is one derived pack with one copied upstream source and one first-party overlay.

### 4. No-skill plugin triage

- Title: `No-skill plugin root triage`
- Scope: Classify the 111 plugin roots that have no `skills/` directory into keep, reset, or quarantine candidates.
- Paths involved: `codex-marketplace/plugins/*`
- Expected mutation class: Docs first, then manifests only if a follow-up issue justifies a real packaging change.
- Validation commands: `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check HEAD~1 HEAD`
- Closeout evidence: Open PR URL plus head SHA.
- Why it is boring and bounded: The class is large, but the criterion is simple and machine-checkable.

## Appendix: raw path inventory

### Active House Skills roots

- `gpt-skills/house-skills/adventures-asset-sheet-compiler`
- `gpt-skills/house-skills/adventures-bootstrap`
- `gpt-skills/house-skills/adventures-frame-buster`
- `gpt-skills/house-skills/adventures-github-operations`
- `gpt-skills/house-skills/adventures-image-qa`
- `gpt-skills/house-skills/adventures-project-doctrine`
- `gpt-skills/house-skills/adventures-storyboard-preflight`
- `gpt-skills/house-skills/adventures-visual-bible-creator`
- `gpt-skills/house-skills/adventures-visual-bible-interpreter`
- `gpt-skills/house-skills/adventures-visual-preproduction`
- `gpt-skills/house-skills/ambiguity-buster`
- `gpt-skills/house-skills/analogy-buster`
- `gpt-skills/house-skills/boring-buster`
- `gpt-skills/house-skills/buster-framework`
- `gpt-skills/house-skills/canon-buster`
- `gpt-skills/house-skills/cleanup-custody`
- `gpt-skills/house-skills/connector-safety`
- `gpt-skills/house-skills/crew`
- `gpt-skills/house-skills/crew-buster`
- `gpt-skills/house-skills/don-logan-boundary`
- `gpt-skills/house-skills/gpt-base-doctrine`
- `gpt-skills/house-skills/invariant-buster`
- `gpt-skills/house-skills/linear`
- `gpt-skills/house-skills/rooms-ambiguity-buster`
- `gpt-skills/house-skills/rooms-analogy-buster`
- `gpt-skills/house-skills/rooms-bootstrap`
- `gpt-skills/house-skills/rooms-canon-buster`
- `gpt-skills/house-skills/rooms-character-investigation`
- `gpt-skills/house-skills/rooms-image-sidecars`
- `gpt-skills/house-skills/rooms-project-doctrine`
- `gpt-skills/house-skills/rooms-sheet-creator`
- `gpt-skills/house-skills/rooms-source-partitioning`
- `gpt-skills/house-skills/rooms-zoom-outs-buster`
- `gpt-skills/house-skills/session-buster`
- `gpt-skills/house-skills/session-buster-ingress`
- `gpt-skills/house-skills/skill-buster`
- `gpt-skills/house-skills/skill-packager`
- `gpt-skills/house-skills/skill-validator`
- `gpt-skills/house-skills/tps-ingress`
- `gpt-skills/house-skills/tps-reporting`
- `gpt-skills/house-skills/work-mode-router`
- `gpt-skills/house-skills/worker-dispatch-linear`

### Versioned House Skills residue

- `gpt-skills/house-skills/adventures-asset-sheet-compiler/v1/adventures-asset-sheet-compiler-v1`
- `gpt-skills/house-skills/adventures-bootstrap/v1/adventures-bootstrap-v1`
- `gpt-skills/house-skills/adventures-frame-buster/v1/adventures-frame-buster-v1`
- `gpt-skills/house-skills/adventures-github-operations/v1/adventures-github-operations-v1`
- `gpt-skills/house-skills/adventures-image-qa/v1/adventures-image-qa-v1`
- `gpt-skills/house-skills/adventures-project-doctrine/v1/adventures-project-doctrine-v1`
- `gpt-skills/house-skills/adventures-storyboard-preflight/v1/adventures-storyboard-preflight-v1`
- `gpt-skills/house-skills/adventures-visual-bible-creator/v1/adventures-visual-bible-creator-v1`
- `gpt-skills/house-skills/adventures-visual-bible-interpreter/v1/adventures-visual-bible-interpreter-v1`
- `gpt-skills/house-skills/adventures-visual-preproduction/v1/adventures-visual-preproduction-v1`
- `gpt-skills/house-skills/gpt-base-doctrine/v1.1/gpt-base-doctrine-v1.1`
- `gpt-skills/house-skills/session-buster/v0.1/session-buster-v0.1`
- `gpt-skills/house-skills/session-buster-ingress/v0.1/session-buster-ingress-v0.1`

### Projected skill roots

- `plugins/house-skills/skills/house-skills`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-pack`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-project-doctrine-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-bootstrap-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-github-operations-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-visual-preproduction-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-storyboard-preflight-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-visual-bible-creator-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-visual-bible-interpreter-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-image-qa-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-asset-sheet-compiler-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/adventures-frame-buster-v1.1`
- `codex-marketplace/plugins/adventures-pack/skills/don-logan-boundary-v1`
- `codex-marketplace/plugins/adventures-pack/skills/gpt-base-doctrine-v1`
- `codex-marketplace/plugins/adventures-pack/skills/worker-dispatch-linear-v1`
- `codex-marketplace/plugins/adventures-pack/skills/connector-safety-v1`
- `codex-marketplace/plugins/adventures-pack/skills/linear-v1`
- `codex-marketplace/plugins/adventures-pack/skills/tps-reporting-v1`
- `codex-marketplace/plugins/adventures-pack/skills/tps-ingress-v1`
- `codex-marketplace/plugins/game-studio/skills/game-playtest`
- `codex-marketplace/plugins/game-studio/skills/game-studio`
- `codex-marketplace/plugins/game-studio/skills/game-ui-frontend`
- `codex-marketplace/plugins/game-studio/skills/phaser-2d-game`
- `codex-marketplace/plugins/game-studio/skills/react-three-fiber-game`
- `codex-marketplace/plugins/game-studio/skills/sprite-pipeline`
- `codex-marketplace/plugins/game-studio/skills/three-webgl-game`
- `codex-marketplace/plugins/game-studio/skills/web-3d-asset-pipeline`
- `codex-marketplace/plugins/game-studio/skills/web-game-foundations`
- `codex-marketplace/plugins/unslop/skills/unslop`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/agent-browser`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/aspnet-core`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/connector-safety`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/game-playtest`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/game-studio`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/game-ui-frontend`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/linear-reference-architecture`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/phaser-2d-game`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/sprite-pipeline`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/web-game-foundations`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-browser-game`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-domain-modeling`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-dotnet-architecture`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-project-doctrine`
- `codex-marketplace/plugins/wild-bunch-project-pack/skills/wild-bunch-worker-verification`

