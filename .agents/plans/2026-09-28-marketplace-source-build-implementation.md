# Marketplace Source and Build Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate canonical first-party skill/resource source from plugin products, build complete self-contained marketplace plugins into a committed distribution tree, and give skill behavior, build tooling, and shipped-artifact tests distinct homes.

**Architecture:** Use top-level `skills/` and `shared/` as authored source, `src/plugin-definitions/` for product metadata and inclusion lists, `src/` for reusable build code, and `dist/` for complete built plugin packages and their marketplace catalog. The output is committed under `dist/` because it is what this repository distributes. Keep repository command entrypoints under `tools/`, independent runtime package source under `src/packages/`, and the repository's own installed agent mesh under `.agents/`. Build copies selected skills and shared resources into each plugin and carries required provenance/license notices into the shipped package.

**Tech Stack:** Python build and validation tooling, JSON plugin/build manifests, Markdown skills and references, pytest, existing `tools/run.py` task runner and tracked CI/pre-commit pipeline.

**Spec:** [Marketplace Source and Build Design](2026-09-28-marketplace-source-build-design.md).

**Execution Strategy:** `executing-plans`, because source custody, build definitions, artifact location, inventory generation, and migration all share one schema and committed consumer output. Sequential execution with one implementation context reduces transitional states and avoids parallel edits to the marketplace generator and generated-path contracts; the nearest alternative, `subagent-driven-development`, would add repeated context reconstruction without safely isolating the central build contract.

## Global Constraints

- Treat every skill as first-party authored source, including open-source adaptations; record attribution and comply with source licenses rather than separating source roots by origin.
- Plugin packages remain self-contained installable units; runtime references never escape the installed plugin or skill directory.
- Include the same canonical skill in multiple plugins when product definitions request it.
- Copy canonical shared references/resources into each packaged skill at explicitly declared paths.
- Keep generated output generated: never hand-edit `dist/` or compatibility marketplace exports to change product behavior.
- Preserve plugin names, marketplace install policy, authored skill wording, provenance, license notices, and current runtime behavior unless the build contract requires a narrowly documented adjustment.
- Keep `.agents/skills/` as installed operating projections and `packages/` as independently versioned runtime packages.
- Move all root ADR content to `docs/decisions/`, remove the empty root `adr/` directory, and move root `research/` to `docs/research/`. Repair authored links and regenerate projections/indexes that name the old paths. Include these layout changes in the same PR.
- Classify each test by its owner and behavior. The commit and PR gate runs separate repository, build, and shipped-plugin suites. Skill tests and pressure cases live under canonical skill source and run for the changed skill; evaluation-harness tests run when its runner changes. Retire historical campaign assertions and prose change detectors. Runtime is an outcome of the correct suite boundary, not the target.
- Run focused tests for the changed behavior during implementation. Do not run the repository gate at task boundaries. Make one normal implementation commit after the tasks are complete, so the tracked hook runs the repository suites once rather than paying that cost at every task boundary.
- This branch is rebased on current `origin/main` at `bab1d5d7e`, which includes the merged test-sanitization work; preserve that work. Its merged PR reports no pytest runtime, so use the human-reported four-minute baseline rather than rerunning all tests before implementation.
- On the first implementation commit, retire any eligible `completed-awaiting-retirement` plan artifacts from the refreshed `main` base and regenerate the agent mesh, per repository planning/artifact-custody rules.

## Review Focus

- One skill included in two plugin definitions produces complete copies in both packages with no shared filesystem dependency.
- One shared authored reference included by two skills is copied into each skill's package path and each packaged link resolves after isolating the plugin directory.
- Adapted open-source material retains the required attribution and license notice in every plugin that ships it; first-party provenance does not get misrepresented as unadapted upstream source.
- Build check mode identifies missing, stale, escaping, and unexpected output files without mutating the tree; apply mode produces repeatable results.
- Marketplace catalog paths continue to resolve for local and Git marketplace consumers after moving the generated plugin roots.

______________________________________________________________________

### Task 1: Establish current consumer and output contracts

**Files:**

- Inspect: `AGENTS.md`, `README.md`, `.agents/doctrine/custody-and-marketplace-doctrine.md`, `.agents/playbooks/marketplace-generation.md`, `.agents/runbooks/implementing.md`, `docs/decisions/`, `docs/research/`, `dist/plugin-roots.json`, `dist/manifest.json`, `.agents/plugins/marketplace.json`, `tools/run.py`, `tools/marketplace_utils.py`, `tools/generate_marketplace.py`, `tools/validate_marketplace.py`, `tools/generate_repo_index.py`, `tests/`
- Inspect consumer: downstream repository contracts and documentation that pin or consume this repository as marketplace source. This repo has no `.gitmodules`; do not assume its consumers are configured as local submodules.
- Modify: move `adr/*` to `docs/decisions/` and `research/*` to `docs/research/`; update `AGENTS.md`, `README.md`, research-source links, and the canonical generating-agent-mesh skill reference. Keep consumer findings in the off-repo execution ledger, not a new permanent registry.

**Interfaces:**

- Consumes: current `main` after the test-sanitization merge and the approved design.

- Produces: verified list of marketplace consumer paths and generated surfaces that Task 2 must preserve or intentionally replace.

- [x] **Step 1: Verify current base and retire the completed predecessor plan**

Confirm this branch is based on current `origin/main`. Inspect `.agents/plans/2026-09-28-test-suite-smell-reduction.md`: it is marked `completed-awaiting-retirement` on the base, and its test-quality constraints are represented in this approved design and plan. Remove that completed plan as the first implementation change, then run `py -3 tools/run.py mesh --apply` to retire its generated index entry. Do not delete active plans or artifacts lacking the completion state.

- [x] **Step 2: Trace all marketplace consumers**

Inspect downstream repository contracts/docs that consume this repository, `.agents/plugins/marketplace.json`, the current generated manifest, plugin inventory, and repository indexes. `dist/` is the single committed generated output root for the repository's distributed assets. Consumer subscription changes will be handled separately. GitHub's merged PR #336 status checks are marketplace validation only; they provide no pytest timing, so the user-reported suite baseline is retained.

- [x] **Step 3: Map test ownership and runtime without reverting merged sanitation**

Review the merged test tree and its latest complete-hook timing. Identify tests of skill scripts, skill behavior, repository/build tooling, and shipped plugin contracts. Preserve the merged sanitation, then map tests by behavior and signal. Mark duplicated assertions, tautologies, change detectors, and redundant fixtures for removal or consolidation. PR #336's GitHub checks are marketplace validation only and do not report pytest duration; use the human-reported four-minute/1,208-test baseline and do not rerun the complete suite just to measure it.

**Exit:** the completed predecessor plan is retired from this branch and its index regenerated; consumer paths, folder moves, and test migration mapping are concrete.

### Task 2: Define source, shared-resource, and plugin-composition contracts

**Files:**

- Create: `skills/` canonical directories for the pilot skill(s)
- Create: `shared/` canonical pilot resource(s)
- Create: `src/plugin-definitions/<plugin>/plugin.json` and `contents.json` for two pilot plugins
- Create: `src/marketplace/` package skeleton and schema/data contracts
- Test: `tests/build/test_plugin_definition_contract.py`

**Interfaces:**

- Consumes: consumer-path findings and current plugin/provenance data from Task 1.

- Produces: validated data model for plugin identity, skill inclusion, shared-resource destinations, assets, provenance, and license notices.

- [ ] **Step 1: Add behavior tests for definition validation**

Cover valid one-to-one inclusion, one skill included by two plugins, a shared resource copied into a declared skill-relative path, duplicate destination collisions, unknown skill/resource names, and paths that escape the declared source roots. Use real fixture trees and assert observable diagnostics and accepted definitions.

- [ ] **Step 2: Run the focused test to witness failure**

Run `py -3 -m pytest tests/build/test_plugin_definition_contract.py -q` and confirm the contract module is not yet implemented.

- [ ] **Step 3: Implement the definition schema and loader**

Create explicit schemas or typed validation code in `src/marketplace/`. Keep `plugin.json` compatible with current package requirements. Let `contents.json` describe source identifiers and package destinations, not arbitrary filesystem copying. Represent provenance and license/attribution metadata per skill/resource, not as third-party-vs-first-party roots.

- [ ] **Step 4: Re-run the focused contract test**

Run the same pytest command and confirm all valid and invalid definition cases pass.

### Task 3: Implement deterministic self-contained plugin assembly

**Files:**

- Create: `src/marketplace/build.py`, `src/marketplace/paths.py`, `src/marketplace/provenance.py` as responsibilities require
- Create: `tests/build/test_plugin_assembly.py`
- Create: `tests/shipping/` fixture helpers for inspecting isolated plugin outputs
- Modify: `tools/run.py` to route marketplace apply/check through the build command
- Modify: `tools/generate_marketplace.py` and `tools/marketplace_utils.py` only as thin compatibility entrypoints or remove them when callers migrate

**Interfaces:**

- Consumes: validated definitions from Task 2.

- Produces: one complete plugin directory per definition beneath `dist/plugins/`, with `plugin.json`, skills, copied shared resources, required assets, and license/provenance notices; a generated marketplace catalog under `dist/`.

- [ ] **Step 1: Add assembly behavior tests**

Test multi-plugin reuse, shared-reference copies in each target skill, self-contained relative links, preservation of authored file bytes, required notices in each affected plugin, stable plugin metadata, rejection of missing files and destination collisions, and deterministic file lists/content across two builds. Test empty/disabled plugin definitions and zero-skill plugins if current catalog uses them.

- [ ] **Step 2: Run focused tests and verify failure**

Run `py -3 -m pytest tests/build/test_plugin_assembly.py -q` and `py -3 -m pytest tests/shipping -q`; confirm new output contracts fail before assembly exists.

- [ ] **Step 3: Implement apply/check assembly**

Build all declared plugin packages into a temporary staging directory, validate the complete staged tree, then replace the owned `dist/` generated outputs deterministically. Preserve independently authored package sources in `packages/` and any other explicitly declared inputs; the builder must not erase them. Check mode compares expected output and reports stale/missing/unexpected files without writing. Do not remove unrelated files outside the owned output root. Generated plugin paths must never refer back to top-level source.

- [ ] **Step 4: Verify focused tests and build repeatability**

Run both focused pytest commands, apply the build twice, and compare output manifests and file hashes. Confirm check mode is clean after apply and does not change Git status.

### Task 4: Prove the model with a two-plugin pilot

**Files:**

- Create/move: two representative skill source trees under `skills/`
- Create: a shared reference under `shared/references/`
- Create: two plugin definitions that both include one skill and include the shared reference in at least two skills
- Generate: pilot packages under `dist/plugins/` and marketplace catalog under `dist/`
- Test: `tests/shipping/test_pilot_install_closure.py`

**Interfaces:**

- Consumes: builder and definition contracts from Tasks 2-3.

- Produces: demonstrated package contract proving cross-plugin skill reuse and shared reference copying after plugin isolation.

- [ ] **Step 1: Add installer-closure test**

Build the pilot, copy each plugin directory alone to a temporary location, and verify every skill reference resolves there, each plugin contains its own copy, both plugin manifests load, and provenance/license files accompany the relevant content.

- [ ] **Step 2: Run the focused test and verify it detects missing closure**

Run `py -3 -m pytest tests/shipping/test_pilot_install_closure.py -q`; first demonstrate failure with a fixture omitting one copied reference, then restore it for the passing implementation path.

- [ ] **Step 3: Author the pilot definitions and source**

Move only selected representative first-party skills and shared source to canonical roots. Keep exact authored wording and provenance/license obligations. Add definitions for two existing plugin identities so the pilot exercises actual marketplace metadata and policies.

- [ ] **Step 4: Build and inspect the isolated outputs**

Run `py -3 tools/run.py marketplace --apply`, inspect both package trees and catalog entries, then run the focused closure test and marketplace check mode. Do not begin bulk migration until both independent inclusion cases are proven.

### Task 5: Migrate all canonical skill and shared-resource custody

**Files:**

- Move: all currently canonical skill trees out of `dist/plugins/*/skills/` into `skills/<skill-name>/`
- Move/extract: shared canonical references/assets currently synchronized by `tools/sync_skill_shared_references.py` into `shared/`
- Create/update: `src/plugin-definitions/*/contents.json` for the current 20 plugin identities and all 86 bundled skill inclusions
- Update/remove: `SOURCE.md`, `references/bundle-manifest.json`, and source-path fields according to the new provenance/build record contract
- Update: `tools/new_plugin.py` to scaffold canonical skill source or plugin definitions at the new homes
- Test: skill-owned tests under `skills/<skill>/tests/scripts/` and `skills/<skill>/tests/behavior/` for changed or migrated assets

**Interfaces:**

- Consumes: validated pilot and output contract.

- Produces: complete first-party source inventory independent of plugin membership and definitions reproducing every existing product bundle.

- [ ] **Step 1: Define migration mapping from current bundle manifests**

For every current entry, map canonical source, plugin inclusion(s), copied support files, provenance, and license obligations. Use the current manifests and source notes as evidence; do not infer source identity from plugin name or folder location.

- [ ] **Step 2: Add migration acceptance checks before moving the inventory**

Add tests that compare the old and new inventories by plugin identity and skill name, and validate authored content/provenance/license data transfer. Avoid change-detector-only tests: assert semantic package contracts, exact declared membership, license notice presence, and representative source behavior.

- [ ] **Step 3: Move source and shared materials**

Relocate skill source and shared references to their canonical roots; update skill links to be source-relative where appropriate. Store provenance and license metadata alongside the canonical source or in a stable per-source manifest. Preserve necessary upstream attribution for adaptations.

- [ ] **Step 4: Populate product definitions and scaffold behavior**

Create one composition definition per active plugin. Ensure repeated skill identifiers remain legal across plugin definitions. Update `tools/new_plugin.py` and its usage contract so new skills are created as canonical sources and plugin assignment is an explicit separate action.

- [ ] **Step 5: Build and compare all 20 packages**

Run `py -3 tools/run.py marketplace --apply`. Compare the generated plugin inventory against the pre-migration accepted inventory: 20 plugin identities, 86 skill inclusions, install policies/categories, skill content, assets, provenance, and license notices. Investigate every difference; no unexplained content loss or behavioral rewrite is acceptable.

### Task 6: Reorganize tests around the behavior they establish

**Files:**

- Move/add: `skills/<skill>/tests/scripts/` and `skills/<skill>/tests/behavior/`
- Move: repository build tests into `tests/build/`
- Move: generated plugin/catalog contract tests into `tests/shipping/`
- Modify: `pyproject.toml`, `tools/run.py`, CI workflows, pre-commit hooks, and test docs to discover and run all intended suites
- Update: `tests/INDEX.md` or its generated navigation and applicable skill inventories

**Interfaces:**

- Consumes: the sanitized test state merged into the refreshed branch and the new source/output contracts from Tasks 2-5.

- Produces: discoverable test ownership and commands that distinguish skill code, skill behavior, repository tooling, and installed marketplace artifacts.

- [ ] **Step 1: Add suite-discovery and ownership tests**

Test the test runner configuration/command mapping so each suite is discoverable and the canonical CI route runs all required suites. Do not test merely that files moved or directory names exist; prove a representative behavior test, a build test, and a built-package test each execute through the intended command. Inventory overlap and measured duration, then remove duplicate/low-signal cases and merge equivalent fixtures around the strongest behavioral assertion. Keep broad scenario matrices only where they cover distinct consequential outcomes.

- [ ] **Step 2: Run targeted suite discovery tests**

Run the focused runner/configuration tests and verify they fail when a suite is omitted from the registered CI targets.

- [ ] **Step 3: Move tests by subject and ownership**

Skill-script unit tests and pressure cases follow the skill source; build tests live in `tests/build/`, repository tool tests in `tests/repository/`, built-package checks in `tests/shipping/`, and shared evaluation-harness checks in `tests/evaluation-harness/`. Keep shared fixtures at the narrowest scope that owns their semantics. Copy ship-ready skill tests into each built plugin while excluding evaluator-only assets and run results.

- [ ] **Step 4: Wire CI and documentation**

Update `tools/run.py`, pytest discovery/configuration, `.github/workflows/*`, tracked hook commands, `tests/INDEX.md`, `AGENTS.md`, and `.agents/playbooks/testing.md` so focused commands and the complete gate run the right suites once. Preserve test-sanitization changes already merged; resolve overlap by integrating against refreshed `main`.

- [ ] **Step 5: Verify focused ownership and suite runtime**

Run focused tests for each changed suite and confirm that CI names only repository, build, and shipping suites. Run changed-skill and evaluation-harness tests explicitly. Use the single final hooked run to prove the commit gate and inspect its timing, without adding skill tests to that gate.

### Task 7: Move marketplace metadata and generated outputs to the product/build boundary

**Files:**

- Generate: `dist/manifest.json` and `dist/plugins/*`
- Generate or preserve compatibility: `.agents/plugins/marketplace.json`, `dist/manifest.json`, `dist/plugin-roots.json`, `dist/README.md`, `dist/INDEX.*`, root `INDEX.*`, and marketplace submodule exports as justified by Task 1 consumer evidence
- Modify: `tools/generate_plugin_root_inventory.py`, `tools/generate_repo_index.py`, `tools/validate_marketplace.py`, `tools/validate_repo_index.py`, `tools/marketplace_utils.py`, `tools/run.py`
- Modify: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `.agents/doctrine/custody-and-marketplace-doctrine.md`, `.agents/playbooks/marketplace-generation.md`, `.agents/runbooks/implementing.md`, and relevant `.devin/rules/` files
- Test: `tests/shipping/` catalog resolution and generated-surface validation

**Interfaces:**

- Consumes: all canonical sources, product definitions, test taxonomy, and stable build output from prior tasks.

- Produces: one documented authority for source, one generated installed marketplace, and no stale path/policy instructions.

- [ ] **Step 1: Add consumer-path tests**

Verify `.agents/plugins/marketplace.json` entries resolve to the built package root under the actual repo marketplace resolution rules; verify `dist/manifest.json` matches the canonical generated catalog. Verify every catalog entry resolves to a complete plugin under `dist/plugins/`.

- [ ] **Step 2: Implement catalog and inventory generation**

Generate catalog order, categories, install policies, and plugin-root inventory from plugin definitions and manifests. Keep generated documentation and indexes downstream. Remove duplicate catalog generation only after all consumer checks pass.

- [ ] **Step 3: Update authoritative doctrine and routing**

Replace source-custody and BAU claims that skill source lives under plugin directories. State the new `skills/`, `shared/`, `src/plugin-definitions/`, `src/`, and `dist/` responsibilities, build/apply/check commands, output ownership, and test routing in `AGENTS.md`, custody doctrine, marketplace-generation playbook, implementing runbook, contribution docs, and scoped rules. Document `dist/` as generated, committed distribution output. Move ADRs into `docs/decisions/` and research into `docs/research/`, repair the root ADR link and references to the research corpus, and regenerate documentation indexes. Keep source custody, product composition, and output generation as separate concepts.

- [ ] **Step 4: Remove superseded generators and projections**

Delete the old shared-reference copier, source bundle manifests, plugin-root source inventory, or redundant generated surfaces only when their replacement is validated and every consumer is migrated. Remove stale indexes through their owning generators. Do not retain compatibility wrappers without a verified consumer.

- [ ] **Step 5: Regenerate and verify every owned surface**

Run build apply/check, `py -3 tools/run.py mesh --apply`, installed-skill refresh where affected, repository indexes, and relevant marketplace validation. Confirm generated files are reproducible and no docs, scripts, tests, contracts, or installed mesh point at retired canonical source paths.

### Task 8: Complete end-to-end validation and publication

**Files:**

- Modify: this plan state/checklist during execution
- Regenerate: all generated marketplace, inventory, README, indexes, installed mesh and package outputs owned by changed source
- Verify: tests, marketplace consumer paths, repository gate, staged hook

**Interfaces:**

- Consumes: completed source migration and generated marketplace from Tasks 1-7.

- Produces: committed, reviewable Draft PR with build reproducibility and installable plugin evidence.

- [ ] **Step 1: Run design-specific package validations**

Build twice from a clean staging area; compare output hashes. Install or load the local repository marketplace using the supported Codex marketplace flow, and verify representative plugins with shared skill/reference copies work from the isolated installed plugin tree.

- [ ] **Step 2: Run focused checks before the final commit**

Run changed-skill tests, `tests/build/`, `tests/repository/`, `tests/shipping/`, the evaluation-harness tests if its runner changed, `py -3 tools/run.py marketplace --check`, mesh and index checks. The normal tracked hook will run the repository gate on the single final implementation commit. Fix every focused failure before staging that commit.

- [ ] **Step 3: Self-review source custody and package closure**

Review every changed path against the design, confirm all plugin entries are self-contained, provenance/license notices are preserved, old canonical skill source has been removed from plugin package trees, and no active generated output was hand-edited.

- [ ] **Step 4: Make one final commit and publish**

Stage the intended complete tree once and make one normal implementation commit after all plan tasks pass their focused checks. The tracked hook runs the repository, build, and shipping suites plus canonical apply/check validation. Skill and evaluation suites run explicitly for their owners. Do not create intermediate task commits or run full checks before each one. If the hook fails, fix the cause and make a corrected commit through the hook. Push the branch, open a Draft PR into `main`, attach its PR artifact, and verify the published head and checks. Do not bypass the hook.

## Plan Readiness Self-Review

- Task ordering is serial where schemas and outputs are producers for later migrations; the pilot is a gate before inventory-wide moves.
- Test responsibilities are explicitly separated; redundant and low-signal tests are removed or consolidated, and the merged sanitation is preserved.
- Focused skill tests run during skill changes; the three named repository suites run once on the single final commit.
- The built marketplace path is resolved from actual Git/submodule consumers before replacing current surfaces.
- Generated and canonical authorities are named and every removal depends on verified replacement consumers.
- Final generation, marketplace validation, repository CI, hook, Draft PR, and publication evidence are listed.
