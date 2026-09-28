# Selectable Standards and Consumer Runner Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let each consumer explicitly select independently adoptable marketplace standards, keep repository-owned standards independent, execute only declared checks and scaffolds, and validate deployed checkers in hosted CI without ambient plugins.

**Architecture:** Agent Operating Model's standard catalog defines stable standard IDs, real dependencies, and the exact deployable resources and invocation contract for each standard. A versioned consumer composition records explicit marketplace and repository-owned standards. A coordinator validates the complete composition before mutation and runs only selected contracts. Consumers deploy pinned selected checker inputs; their local and hosted runners invoke those inputs without resolving skills from ambient Codex plugins. A migration command translates an existing consumer's effective legacy shape into an explicit declaration for review. The Rooms compatibility guide replaces Repo Worker Pack's installed refresh-script path with the same utility under the consumer's pinned marketplace-source submodule. Index mesh is already retired by Plan 1 and has no replacement.

**Tech Stack:** Python 3, JSON Schema, pytest, existing marketplace builder, pinned marketplace-source submodule, and consumer canonical runner/hook contract.

**Spec:** `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md`

**Roadmap context:** Plan 1 retired generated index mesh in commits `b1aaef107`, `ba486ac56`, `2c5848caa`, and `e6a6c7868`; its Draft PR is [#338](https://github.com/HarleyBartles/agent-asset-marketplace/pull/338). The same branch is based on current `main` `d505f31aa`. Mesh generation and validation have no compatibility bridge; only the refresh runner dependency remains to migrate.

**Execution Strategy:** `executing-plans` - catalog, migration, dispatcher, deployment, and runner handoff form a dependent chain with shared schemas and compatibility behavior. Keeping one integration context reduces interface drift; each task still ends with its focused behavior gate and commit.

## Global Constraints

- Agent Operating Model availability never implies consumer adoption. A consumer can choose an empty marketplace-standard set and independently declare repository-owned standards.
- Marketplace standards are individually identifiable and deployable. Do not ship one omnibus `repo-shape` adoption that keeps every current check mandatory under a new name.
- Validate dependencies, ownership, implementation roots, commands, and generated paths before any apply-side mutation. Missing or ambiguous declarations fail clearly; they do not silently mean all or none.
- A migration preview must show the exact standards inferred from current explicit legacy surface exceptions and existing declarations. Applying it requires an explicit apply invocation and preserves the existing consumer runner/hook commands.
- Only selected standards' checks, scaffolds, generated paths, and declared dependencies run. Marketplace plugin subscriptions and installed skill projections do not select standards.
- Hosted CI executes checked-in or gitlink-pinned consumer-controlled checker inputs. It does not need Codex, ambient plugins, or `.agents/skills/` projections.
- Deploy only selected standard resources plus the minimal generic coordinator needed to invoke them. Do not copy entire ambient plugins into consumers.
- For Rooms compatibility, index mesh calls are removed with no replacement. The refresh utility can be invoked from the pinned `.agents/plugins/marketplace-source` submodule, avoiding the Repo Worker Pack installed-skill path. Preserve the intended refresh behavior and canonical `ci --apply` / `ci --check` hook contract.
- Do not edit Rooms or any other consumer checkout. Use a behavior fixture derived from current read-only Rooms evidence.
- Edit canonical source under `skills/` and `src/plugin-definitions/`; regenerate `dist/` and `.agents/skills/` through owning commands. Never hand-edit generated projections.
- Use portable behavioral tests. No exact-prose assertions or tests that merely detect file changes.

## Review Focus

- A consumer can select two distinct standards and omit a third; only the selected checks/scaffolds execute.
- An empty catalog selection runs no marketplace-standard checks or scaffolds, while repository-owned declarations remain possible.
- Missing, unknown, cyclic, or unsatisfied standard dependencies fail before any command marker or generated file changes.
- Plugin subscriptions, including Agent Operating Model, Superpowers+, Repo Worker Pack, and Unslop+, do not affect the selected standard set.
- Migration preview and apply preserve the consumer's effective explicitly excepted legacy surfaces and existing runner commands; ambiguous legacy state is refused.
- A hosted hook fixture passes with no ambient skill projections and with only the selected standard implementations present.
- Skill refresh does not mutate the standard composition or deployed checker bytes.
- Rooms migration instructions remove mesh invocations and route refresh to the pinned submodule source while preserving the outer hook and hosted validation behavior.

______________________________________________________________________

### Task 1: Inventory and define independently adoptable standards

**Files:**

- Create: `skills/repo-shape/references/operating-standards-catalog.json`
- Create: `skills/repo-shape/references/operating-standards-catalog.schema.json`
- Create: `skills/repo-shape/scripts/operating_standards_catalog.py`
- Modify: `skills/repo-standards/SKILL.md`
- Modify: `src/plugin-definitions/agent-operating-model/files/README.md`
- Modify: `src/plugin-definitions/agent-operating-model/files/SOURCE.md`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_catalog.py`

**Interfaces:**

- Catalog IDs are stable, kebab-case, and represent independently adoptable contracts. Catalog entries list the implementation surface IDs they own, deployable resource paths, check/apply capability, and `requires` edges. The catalog is the single ownership mapping; the existing surface manifest remains the implementation inventory.

- Classify every current shape-manifest surface. Split the surfaces into coherent independently adoptable standards; retain `markdown-formatting` as its own standard. Do not group all surfaces under a single required standard. Record the classification in the catalog so the consumer can select individual standards.

- Use these proposed boundaries as the initial catalog vocabulary: `marketplace-skill-management` (marketplace source, marketplace JSON, local skill preservation), `root-agent-router`, `runbook-composition` (policy, runbooks, optional runbook router), `playbook-composition` (playbooks and optional playbook router), `tracked-validation-hook` (command declaration, hook, shared-checkout support), `markdown-formatting`, `review-entrypoint`, `contribution-entrypoint`, `root-gitignore-hygiene`, and `completed-artifact-custody` (doctrine plus forbidden retired archive paths). The legacy `operating-model-contract` exception mechanism is migration input, not an adopted standard. Adjust a boundary only when the current validator behavior proves an actual dependency; encode that dependency as an edge instead of silently merging the standards.

- A standard may depend only on another catalog standard by ID. Reject duplicate IDs, unknown/duplicate surface IDs, uncovered implementation surfaces, unknown dependencies/resources, self-dependencies, and dependency cycles.

- All catalog resources resolve inside the Agent Operating Model plugin source. The catalog itself is shipped with that ambient plugin and does not assert consumer adoption.

- Keep the current surface manifest as an implementation inventory only during the compatibility transition; standard selection becomes authoritative in later tasks.

- [x] **Step 1: Add catalog behavior tests**

Cover the actual current surfaces, independently selectable catalog entries, resource containment, valid dependency edges, and rejection of duplicate IDs, unknown resources, and dependency cycles. Include a representative composition selecting two standards while omitting a third.

- [x] **Step 2: Confirm the focused test fails**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_catalog.py -q`

Expected: FAIL because the catalog contract and validator do not exist.

- [x] **Step 3: Add and package the catalog**

Inventory the live shape-manifest validators, scaffolds, and documentation. Assign every current surface to the smallest independent standard boundary supported by its behavior. Add catalog and schema validation; package the catalog as an Agent Operating Model resource and describe its role as an ambient choice catalog.

- [x] **Step 4: Verify catalog behavior**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_catalog.py tests/build/test_plugin_definition_contract.py tests/build/test_plugin_assembly.py -q`. Expected: PASS for valid independent standards and all invalid-catalog cases. Run `py -3 tools/run.py marketplace --apply` and confirm the catalog and validator appear under `dist/plugins/agent-operating-model/skills/repo-shape/`.

- [x] **Step 5: Commit the catalog**

```powershell
git add skills/repo-shape/references/operating-standards-catalog.json skills/repo-shape/references/operating-standards-catalog.schema.json skills/repo-shape/scripts/operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_catalog.py skills/repo-standards/SKILL.md src/plugin-definitions/agent-operating-model/files/README.md src/plugin-definitions/agent-operating-model/files/SOURCE.md dist/plugins/agent-operating-model .agents/skills/repo-shape .agents/skills/repo-standards
git commit -m "feat: define selectable operating standards"
```

### Task 2: Define consumer composition and explicit legacy migration

**Files:**

- Create: `skills/repo-shape/references/operating-standards.schema.json`
- Create: `skills/repo-shape/templates/operating-standards.json`
- Create: `skills/repo-shape/scripts/scaffold_operating_standards.py`
- Create: `skills/repo-shape/scripts/migrate_operating_standards.py`
- Modify: `skills/repo-shape/scripts/plugin_contracts.py`
- Modify: `skills/repo-shape/references/operating-standards-catalog.json`
- Modify: `skills/repo-shape/references/operating-standards-catalog.schema.json`
- Modify: `skills/repo-shape/scripts/operating_standards_catalog.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_standards_catalog.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_contract.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_migration.py`

**Interfaces:**

- Consumer contract: `.agents/contracts/operating-standards.json`, versioned, with an explicit `standards` array. Empty array is an explicit choice of no marketplace standards.

- Every entry has `id`, `origin` (`marketplace` or `repository`), `implementation_root`, `check` command vector, `apply` command vector (empty only when the standard has no apply action), `generated_paths`, and `requires`. Marketplace entries also have a pinned `revision`; repository-owned entries omit it and own their commands/resources in the consumer tree.

- Validate all entries against the catalog, validate transitive dependencies and path containment, and preserve source/version provenance. Marketplace plugin installation metadata is not consulted to infer adoption.

- Migration `--check` is read-only and reports the exact contract it would write. `--apply` requires explicit invocation and writes only the new contract/provenance; it does not rewrite hook commands, plugin subscriptions, or deployed files.

- Migration maps current explicit surface exceptions and other authoritative declarations to the new catalog units while preserving the currently enabled legacy surface set. If no trustworthy source exists or a mapping is ambiguous, return a diagnostic before writing. A missing new contract is not interpreted as an empty set.

- Catalog migration inputs that are not adopted standards, especially the legacy `operating-model-contract`, are listed separately from adoptable standard surfaces. Migration preserves the old contract untouched and does not emit that legacy surface as a standard.

- [x] **Step 1: Add composition and migration behavior tests**

Cover empty, mixed marketplace/repository-owned, and dependency-bearing compositions; unknown IDs; invalid roots/commands; unsafe generated paths; migration preview/apply; exact preservation of legacy enabled surfaces; refusal of ambiguous legacy state; and proof that preview performs no writes.

- [x] **Step 2: Confirm the focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_contract.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py -q`

Expected: FAIL because the new declaration and migration command do not exist.

- [x] **Step 3: Implement schema, scaffold, and migration**

Implement validation from the packaged catalog. Keep explicit marketplace provenance separate from repository-owned contracts. Make preview output deterministic. Resolve the complete migration before writing, then atomically write the new declaration only after all inputs pass validation.

- [x] **Step 4: Verify contract and migration behavior**

Run the focused command from Step 2. Expected: PASS, including refusal before writes on invalid or ambiguous legacy data.

- [x] **Step 5: Commit the composition contract**

```powershell
git add skills/repo-shape/references/operating-standards.schema.json skills/repo-shape/templates/operating-standards.json skills/repo-shape/scripts/scaffold_operating_standards.py skills/repo-shape/scripts/migrate_operating_standards.py skills/repo-shape/scripts/plugin_contracts.py skills/repo-shape/references/operating-standards-catalog.json skills/repo-shape/references/operating-standards-catalog.schema.json skills/repo-shape/scripts/operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_contract.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py dist/plugins/agent-operating-model .agents/skills/repo-shape
git commit -m "feat: declare consumer operating standards"
```

### Task 3: Dispatch only the declared standards

**Files:**

- Modify: `skills/repo-shape/scripts/repo_standards.py`
- Modify: `skills/repo-shape/scripts/plugin_contracts.py`
- Modify: `skills/repo-shape/scripts/operating_standards_catalog.py`
- Modify: `skills/repo-shape/scripts/migrate_operating_standards.py`
- Create: `skills/repo-shape/scripts/operating_standards_dispatch.py`
- Modify: `skills/repo-shape/references/repository-shape-standard.md`
- Modify: `skills/repo-shape/references/consumer-surface-audit.md`
- Modify: `skills/repo-shape/tests/scripts/test_repo_standards.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py`
- Create: `skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py`

**Interfaces:**

- With a valid new declaration, `repo-standards --check` validates the whole composition and runs only the selected standards' checks. `--apply` validates the whole composition before mutation, then runs only selected apply/scaffold actions.

- Aggregate generated paths only from selected standards. A selected standard's declared prerequisites are included explicitly and deterministically; missing prerequisites fail before execution.

- Marketplace plugin prerequisites and plugin-conditioned warnings are removed from `repo-standards`. Agent Operating Model, Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+ do not select or gate consumer standards. Any profile-specific enforcement must be represented by a declared standard, not inferred from a plugin subscription or directory presence.

- Preserve a compatibility lane for existing consumers with the legacy operating-model contract while providing the explicit migration command. Do not make an absent legacy and new contract silently select all or none.

- Preserve apply/check mutation guards, staged-snapshot behavior, consumer exceptions during legacy migration, and existing command-bus outer entrypoints.

- [x] **Step 1: Add selective-dispatch behavior tests**

Use temporary consumer roots and real marker commands/scaffolds. Prove two selected standards run and an omitted standard does not; empty selection runs no marketplace checks; repository-owned standards still run when selected; invalid dependencies fail before markers; and changing plugin subscriptions has no effect on dispatch.

- [x] **Step 2: Confirm focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py -q`

Expected: FAIL because the current validator uses fixed surfaces and mandatory plugin subscriptions.

- [x] **Step 3: Implement composition-driven validation and apply**

Use the new declaration as the dispatch authority. Validate every selected implementation and its dependencies before running a command. Remove hidden fixed required-surface execution from the new-contract path, retaining only compatibility behavior needed by legacy consumers.

- [x] **Step 4: Verify coordinator and plugin independence**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_repo_standards.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py -q`

Expected: PASS for independent/empty selections, legacy migration diagnostics, plugin independence, and existing mutation safety.

- [ ] **Step 5: Commit selective dispatch**

```powershell
git add skills/repo-shape/scripts/repo_standards.py skills/repo-shape/scripts/plugin_contracts.py skills/repo-shape/references/repository-shape-manifest.json skills/repo-shape/references/repository-shape-manifest.schema.json skills/repo-shape/references/repository-shape-standard.md skills/repo-shape/references/consumer-surface-audit.md skills/repo-shape/tests/scripts/test_repo_standards.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py
git commit -m "feat: dispatch only adopted repository standards"
```

### Task 4: Deploy pinned checker inputs for ambient-free hosted CI

**Files:**

- Create: `skills/repo-shape/scripts/deploy_operating_standards.py`
- Modify: `skills/repo-shape/scripts/repo_standards.py`
- Modify: `skills/repo-shape/references/ci-validation-pipeline.md`
- Modify: `skills/repo-shape/tests/scripts/test_repo_standards_hooks.py`
- Create: `skills/repo-shape/tests/scripts/test_operating_standards_deployment.py`
- Modify: `skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py`

**Interfaces:**

- Deployment resolves the consumer's declared pinned marketplace revision and copies only the selected standards' catalog-declared checker, template, and support resources into consumer-selected implementation roots. During migration, `--prepare-migration` derives the selection from the legacy exception contract, deploys it without activating the new contract, and then the migration `--apply` is safe to run. Record source revision and per-resource provenance.

- The generic dispatcher can run from the pinned marketplace-source submodule; selected checker inputs and templates live in the consumer working tree at declared roots. Do not depend on `.agents/skills/` projections or copy an entire ambient plugin.

- Check mode is read-only. Apply fails closed on unknown resources, source/revision mismatch, path escape, conflicting ownership, or an unconfirmed overwrite. A no-op redeployment is deterministic.

- The hosted hook invokes the same consumer canonical runner and validates only selected standards from tracked/pinned consumer-controlled inputs. It must work after removing all ambient skill projection directories and Codex plugin-install state.

- Skill refresh may update ambient skill projections, but must not change the operating-standards declaration, deployed standard bytes, or their provenance.

- [x] **Step 1: Add deployment and hosted-runner behavior tests**

Use a temporary consumer repository and a local pinned-source fixture. Assert selected-only deployment, provenance, read-only check behavior, refusal of path escapes and ambiguous overwrites, hosted validation after removing ambient projections, and refresh preserving declarations and deployed files.

- [x] **Step 2: Confirm the focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py -q`

Expected: FAIL because standards deployment and ambient-free dispatch are not implemented.

- [x] **Step 3: Implement deployment and hosted execution**

Add a safe deployment command and provenance record. Use only catalog-resolved paths under the pinned source root and consumer-declared destinations. Point consumer check/apply vectors at the pinned generic dispatcher and selected deployed checker inputs. Keep standard adoption explicit and check mode side-effect free.

- [x] **Step 4: Verify deployment and hook behavior**

Run the focused command from Step 2. Expected: PASS with only selected deployed resources present and no ambient skill/plugin state required.

- [ ] **Step 5: Commit pinned deployment and hosted validation**

```powershell
git add skills/repo-shape/scripts/deploy_operating_standards.py skills/repo-shape/scripts/repo_standards.py skills/repo-shape/references/ci-validation-pipeline.md skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py
git commit -m "feat: deploy standards for hosted validation"
```

### Task 5: Provide the post-index-retirement consumer runner migration

**Files:**

- Create: `skills/repo-shape/references/consumer-runner-migration.md`
- Modify: `skills/repo-shape/references/ci-validation-pipeline.md`
- Modify: `skills/repo-shape/scripts/deploy_operating_standards.py`
- Create: `skills/repo-shape/tests/scripts/test_consumer_runner_migration.py`
- Modify: `skills/repo-shape/tests/scripts/test_repo_standards_hooks.py`

**Interfaces:**

- Migration instructions are ordered and reversible: deploy/check selected standard resources; migrate the consumer declaration; point the runner at the deployed checker and generic pinned dispatcher; move refresh invocation from `.agents/skills/refreshing-installed-skills/...` to `.agents/plugins/marketplace-source/skills/refreshing-installed-skills/...`; remove mesh targets/calls and all tracked mesh/index files; then remove ambient-pack subscriptions no longer required.

- The guide preserves the consumer's existing `tools/run.py ci --apply` / `tools/run.py ci --check` outer command contract and its tracked hook/hosted-CI staged-snapshot semantics.

- The refresh entrypoint uses the pinned marketplace submodule utility with `--no-roll-marketplace-source` for deterministic CI. Local mutation still follows explicit apply/shared-checkout safeguards. This path uses the utility's marketplace-owned `tools/shared_checkout.py`, not a consumer-installed Repo Worker Pack copy.

- The test fixture is based on current read-only Rooms runner/hook behavior but lives wholly under marketplace tests. It proves old path fails once Repo Worker Pack skill projection is absent, migrated refresh works from the pinned submodule, mesh is absent, and canonical apply/check hook behavior remains.

- Do not edit `Z:\rooms-mostly` or any other consumer.

- [ ] **Step 1: Add a Rooms-derived runner migration behavior fixture**

Model the live `_repo_standards_cmd`, `_skills_cmd`, `_mesh_generate_cmd`, `_mesh_validate_cmd`, CI apply/check sequence, and hosted hook entrypoint. Assert the old installed-skill path fails when Repo Worker Pack is absent and that the pinned-submodule refresh path and deployed selected-standard dispatcher work with the outer `ci --apply` / `ci --check` commands unchanged.

- [ ] **Step 2: Confirm the focused migration test fails**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_consumer_runner_migration.py -q`

Expected: FAIL because the fixture's old Repo Worker Pack dependency has no supported local migration path.

- [ ] **Step 3: Implement the migration guide and supported path**

Document exact sequencing, runner changes, validation at each transition, and recovery to the current pinned-submodule state. Remove all obsolete mesh migration language; Plan 1's removal requires no mesh replacement. Make the refresh utility's direct submodule invocation and selected-standard deployment the supported bridge.

- [ ] **Step 4: Verify migration and hosted hook behavior**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_consumer_runner_migration.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py -q`

Expected: PASS with no Repo Worker Pack or Agent Operating Model skill projection, no mesh calls, selected deployed standards active, and unchanged outer apply/check intent.

- [ ] **Step 5: Commit the runner migration contract**

```powershell
git add skills/repo-shape/references/consumer-runner-migration.md skills/repo-shape/references/ci-validation-pipeline.md skills/repo-shape/scripts/deploy_operating_standards.py skills/repo-shape/tests/scripts/test_consumer_runner_migration.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py
git commit -m "feat: add ambient-pack runner migration path"
```

### Task 6: Regenerate, review, and publish Plan 2

**Files:**

- Modify: `src/plugin-definitions/agent-operating-model/contents.json`

- Modify: generated `dist/plugins/agent-operating-model/` resources through the marketplace build

- Modify: installed `.agents/skills/` projections through the installed-skill build

- Review: all source and generated output from Tasks 1-5

- [ ] **Step 1: Run focused source tests**

Run the tests introduced or modified in Tasks 1-5, plus the existing repo-shape, repo-standards, operating-model plugin contract, refresh, and hosted-hook suites.

- [ ] **Step 2: Regenerate and validate projections**

Run:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py marketplace --check
py -3 tools/run.py installed-skills --check
```

Expected: Agent Operating Model ships the selectable catalog and deployment tools. Consumer-facing templates do not silently select standards, and generated output contains no index mesh artifacts.

- [ ] **Step 3: Review source and generated outputs**

Review the complete branch diff against the approved spec. Confirm every prior fixed surface has a catalog classification; subscriptions do not select standards; chosen standards alone run; hosted behavior works without ambient skills; refresh is submodule-pinned; no mesh generator or index artifact has returned; and all copied/deployed resources have ownership and source revision evidence.

- [ ] **Step 4: Run canonical validation and commit through the hook**

Stage the intended tree and commit normally. The tracked pre-commit hook is the complete canonical apply/check gate. Do not run the complete CI check immediately before or after a successful hooked commit.

- [ ] **Step 5: Push and verify the Draft PR**

Push the same roadmap branch and verify the PR head SHA and hosted checks. The draft workflow may skip validation; record the local hook evidence and any hosted-check limitation. Keep the existing PR draft while later roadmap plans remain in progress.

## Completion boundary

Plan 2 completes when consumer standard selection is explicit, independently granular, migration from the legacy shape is reviewable, dispatch and scaffolding are composition-driven, hosted CI uses pinned consumer-controlled selected implementations without ambient plugins, and the Rooms-derived fixture proves refresh/runner continuity after mesh removal and ambient-pack unsubscription. It does not edit Rooms or complete the companion-pack audit and capability-based workflow contract; those remain later roadmap work.
