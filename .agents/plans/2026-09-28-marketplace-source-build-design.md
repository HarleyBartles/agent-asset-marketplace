# Marketplace Source and Build Design

## Decision

Organize this repository as a source-and-build monorepo for multiple installable plugin products. Canonical skill source and shared authored resources belong outside plugin package directories. Plugin definitions select which skills and other files each product contains. A conventional build assembles self-contained, Codex-compatible plugin directories and the marketplace catalog from those inputs.

Plugins are the installable unit and carry complete copies of their skills, references, assets, manifests, and required license notices. Plugin membership does not confer ownership of a skill's source. One skill may be included in multiple plugins. A reference or other authored resource may have one canonical source and be copied into multiple packaged skills.

All skill content is first-party source for this repository, including material adapted from other open-source work. Provenance and license obligations are declared honestly and preserved with the relevant source and shipped outputs. Origin/provenance is metadata, not a separate source-custody category or a reason to put source under a plugin.

## Source and output responsibilities

- `skills/<skill-name>/` is the canonical home for authored skill instructions and skill-specific resources.
- `shared/` contains reusable authored resources, such as references, templates, and assets. These are build inputs, not runtime dependencies of installed plugins.
- `src/plugin-definitions/<plugin-name>/` contains the plugin's manifest and an explicit composition definition. It declares inclusion and packaging; it does not contain canonical skill source.
- `src/` contains reusable marketplace build and validation implementation. Existing repository-maintenance commands under `tools/` remain command entrypoints and unrelated repository tooling does not move merely to satisfy a directory convention.
- `dist/` is the committed distribution output, with complete installable plugin trees and built wheels. Each plugin is self-contained and resolves no path back into `skills/`, `shared/`, or `src/plugin-definitions/`.
- `src/packages/` owns independently versioned runtime package source; built wheels are distributed under `dist/wheels/`.
- `.agents/` continues to own this repository's installed operating mesh; it is neither vendored marketplace source nor plugin build output.
- `docs/decisions/` owns the repository's architecture decision records; `docs/research/` owns repository research material. Root-level durable project docs are grouped under `docs/`.

The generated marketplace must remain usable from the repository's Git distribution. `dist/` is the one committed, freshness-checked output root. The root `.agents/plugins/marketplace.json` is Codex's marketplace entry point and refers to built plugin roots under `dist/plugins/`. Keep authored catalog inputs in `src/plugin-definitions/` and generated inventory in `dist/`.

## Test responsibilities

- Skill-owned tests live beside their source under `skills/<skill-name>/tests/`, split into `scripts/` for executable skill-resource unit tests and `behavior/` for tests of instruction behavior.
- Repository tool tests live under `tests/repository/`; build tests live under `tests/build/` and exercise implementation in `src/` and command wiring in `tools/`.
- Shipped-artifact tests live under `tests/shipping/` and inspect a freshly built marketplace as an installer would: manifest resolution, self-containment, skill/reference closure, multi-plugin inclusion, license/provenance preservation, and absence of source-tree dependencies.
- Skill pressure cases live with their canonical skill source under `skills/<skill-name>/tests/pressure/`. Shared pressure-runner tests live in `tests/evaluation-harness/` and run when that harness changes.
- Tests must exercise real behavior or an actual packaging contract. Do not add tautological tests or change-detector tests.
- The merged test-sanitization work is the starting point. Classify each test by the behavior it owns. Retire historical campaign assertions and exact-prose change detectors. The commit and PR gate runs the repository, build, and shipped-artifact suites separately; it does not collect skill or evaluation-harness tests by default.
- Run the changed skill's tests explicitly during skill work. Run evaluation-harness tests when changing its runner. The tracked hook runs the repository gate once for the single final implementation commit.
- The builder copies skill-owned tests into each installed skill. `tests/evaluator-only/`, Python caches, and transient `runs/` directories are excluded from packages.

## Build contract

The build is the supported assembly mechanism, not an ad-hoc projection synchronizer. Its inputs are canonical skills, shared resources, product definitions, package manifests, provenance/license metadata, and static plugin assets. Its outputs are complete plugin packages, the marketplace catalog, and any deliberately retained compatibility exports. The build supports apply and check modes, rejects unresolved or escaping input paths, and can reproduce byte-identical outputs from the same source tree.

The build must copy shared material into each packaged skill at a declared relative path. Packaged skill links resolve within their installed skill directory. Build metadata records source-to-output mapping sufficiently to audit inclusion and attribution without shipping repository-only test/build files.

## Migration boundaries

The refactor replaces the current source-custody assumption in `.agents/doctrine/custody-and-marketplace-doctrine.md` and the generated `dist/plugins/` authoring flow. It also moves root `adr/` contents to `docs/decisions/` and root `research/` to `docs/research/`, updating links and generated indexes. It must update `AGENTS.md`, the marketplace generation playbook, implementation guidance, marketplace manifests/inventory/indexes, plugin scaffolding, validators, tests, CI/task-runner targets, README/contributor documentation, and downstream consumer expectations where the live repo uses them.

Migration proceeds through a representative pilot that proves one skill can be included in two built plugins and one shared reference is copied into each package. After the build contract is verified, migrate the remaining first-party inventory, remove superseded source/build projections, and regenerate every owned output. Preserve public plugin identities, install policies, plugin contents, authored wording, provenance, license terms, and existing runtime behavior unless the approved design explicitly requires a change.

## Research basis

- Codex defines plugins as installable packages that contain skills and their supporting resources; a plugin may group related skills. [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)
- Codex packaging guidance describes a self-contained plugin root with its own manifest and `skills/` tree, and distinguishes marketplace catalog entries from package contents. [Package your plugin](https://developers.openai.com/plugins/build/plugins)
- OpenAI's plugin repository uses one `plugins/<name>/` package directory per installable plugin. [OpenAI plugins repository](https://github.com/openai/plugins)
- Microsoft's Power Platform plugin repo documents canonical shared workflow source copied into each plugin, with each installed plugin remaining complete and portable. [Shared skills guidance](https://github.com/microsoft/power-platform-skills/blob/main/AGENTS.md)
- Sheg is a local source-layout reference for keeping top-level `skills/` beside product `src/`, documentation, and plugin metadata; this design extends that pattern for a multi-plugin catalog with reusable source and a build output.
