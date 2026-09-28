# Selectable Standards and Consumer Runner Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let each consumer explicitly adopt any subset of marketplace standards and repository-owned standards, run only declared checks, and validate deployed checkers in hosted CI without ambient plugins.

**Architecture:** Add a versioned standards catalog and consumer composition contract to Agent Operating Model. Make the repo-shape coordinator validate and apply only declared standard implementations, preserving a deliberate migration from the current bundled shape. Deploy pinned, consumer-controlled runner utilities for refresh and mesh operations so hooks do not depend on Repo Worker Pack skill projections.

**Tech Stack:** Python 3, JSON Schema, pytest, existing marketplace plugin build and repository command bus.

**Spec:** `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md`

**Execution Strategy:** `executing-plans` - contract, coordinator, deployment, and hook/CI behavior share schemas and migration boundaries. One implementation context minimizes interface drift; task exits provide focused review points.

## Global Constraints

- Agent Operating Model is an ambient catalog; its presence does not imply that a repository adopted any standard.
- Consumers may declare an empty marketplace-standard set and any number of repository-owned standards.
- Apply/check behavior and dependencies are limited to declared standards.
- Hosted CI uses pinned, consumer-controlled checker sources and does not require Codex or ambient plugin installation.
- Missing configuration does not silently imply adoption or an empty set; existing consumers get an explicit migration path.
- Do not edit consumer repositories in this plan.
- Canonical source is under `skills/`, reusable packaged resources under `shared/`, and plugin membership under `src/plugin-definitions/`. Regenerate `dist/` and `.agents/skills/` through their owning commands.
- Use portable behavior tests. Do not add exact-prose or change-detector tests.

## Review Focus

- Empty composition invokes no marketplace standard check or scaffold; cover in dispatch tests.
- Missing declared dependency fails before mutation; cover in composition tests.
- Hosted CI runs with no ambient plugin projections; cover in deployment/runner integration.
- Migration makes legacy adoption explicit and preserves existing hook commands; cover in migration and hook tests.
- Ambient skill refresh leaves standard declarations and deployed standard files unchanged; cover in refresh/deployment integration.

______________________________________________________________________

### Task 1: Define independently selectable catalog standards

**Files:**

- Modify: `skills/repo-standards/SKILL.md`
- Create: `skills/repo-standards/references/standards-catalog.json`
- Create: `skills/repo-standards/references/standards-catalog.schema.json`
- Modify: `src/plugin-definitions/agent-operating-model/plugin.json`
- Modify: `src/plugin-definitions/agent-operating-model/files/SOURCE.md`
- Modify: `src/plugin-definitions/agent-operating-model/files/README.md`
- Modify: `src/plugin-definitions/agent-operating-model/contents.json`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_catalog.py`

**Interfaces:**

- Each catalog entry has a stable ID, deployable resource list relative to the Agent Operating Model package root, explicit standard dependencies, and check/apply invocation contract.

- Group current `repository-shape-manifest.json` surfaces into independently adoptable policy/check units. Keep actual dependencies as explicit edges and `markdown-formatting` separate because it already has an independent adoption state.

- The consumer composition contract is versioned and has a `standards` array. Entries identify `id`, `origin` (`marketplace` or `repository`), optional marketplace `revision`, local `implementation_root`, `check` and `apply` command vectors, `generated_paths`, and `requires` standard IDs.

- [ ] **Step 1: Add catalog behavior tests**

Test unique IDs, schema validity, declared resource paths, declared dependencies, cycle rejection, and separate adoption entries for representative current surfaces.

- [ ] **Step 2: Confirm the focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_catalog.py -q` Expected: FAIL because the catalog and validator do not exist.

- [ ] **Step 3: Add catalog, schema, and package membership**

Classify every current shape-manifest surface into a standard; encode only real prerequisite edges. Include current `markdown-formatting` as its own standard. Add the catalog validator and declare its resources in the Agent Operating Model plugin.

- [ ] **Step 4: Verify catalog behavior**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_catalog.py -q` Expected: PASS for valid catalog entries and rejection of duplicate IDs, invalid resources, unknown dependencies, and cycles.

- [ ] **Step 5: Commit the catalog**

```powershell
git add skills/repo-standards/SKILL.md skills/repo-standards/references/standards-catalog.json skills/repo-standards/references/standards-catalog.schema.json src/plugin-definitions/agent-operating-model/plugin.json src/plugin-definitions/agent-operating-model/files/SOURCE.md src/plugin-definitions/agent-operating-model/files/README.md src/plugin-definitions/agent-operating-model/contents.json skills/repo-shape/tests/scripts/test_operating_standards_catalog.py
git commit -m "feat: define selectable operating standards"
```

### Task 2: Add consumer composition and explicit legacy migration

**Files:**

- Create: `skills/repo-shape/references/operating-standards.schema.json`
- Create: `skills/repo-shape/templates/operating-standards.json`
- Create: `skills/repo-shape/scripts/scaffold_operating_standards.py`
- Create: `skills/repo-shape/scripts/migrate_operating_standards.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_contract.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_migration.py`

**Interfaces:**

- Contract path: `.agents/contracts/operating-standards.json`.

- Contract shape: `{"version": 1, "standards": [...]}`. Entries follow Task 1 and include the resolved local implementation root and command vectors.

- `migrate_operating_standards.py --check` reports the explicit adoption set it would write. `--apply` writes that set and source provenance without changing the existing command declaration or hook.

- `standards: []` explicitly means no catalog standards. A missing or invalid file is reported as migration/configuration drift.

- Migration refuses malformed or ambiguous legacy inputs and never silently opts a consumer into an empty set.

- [ ] **Step 1: Add contract and migration behavior tests**

Cover empty and mixed marketplace/repository declarations; unknown standards; missing dependencies; invalid command vectors and generated paths; dependency cycles; migration preview and apply; and refusal of ambiguous inputs.

- [ ] **Step 2: Confirm the focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_contract.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py -q` Expected: FAIL because the contract and migration command do not exist.

- [ ] **Step 3: Implement validation, scaffolding, and migration**

Add schema validation and deterministic migration from current `agent-operating-model.json`, runbook/playbook mappings, and active shape surfaces. Preserve consumer-owned files and command vectors. New scaffolds must not silently opt consumers into standards.

- [ ] **Step 4: Verify contract and migration behavior**

Run the same focused pytest command from Step 2. Expected: PASS, including refusal before writes on ambiguous input.

- [ ] **Step 5: Commit the composition contract**

```powershell
git add skills/repo-shape/references/operating-standards.schema.json skills/repo-shape/templates/operating-standards.json skills/repo-shape/scripts/scaffold_operating_standards.py skills/repo-shape/scripts/migrate_operating_standards.py skills/repo-shape/tests/scripts/test_operating_standards_contract.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py
git commit -m "feat: declare consumer operating standards"
```

### Task 3: Dispatch only declared standards

**Files:**

- Modify: `skills/repo-shape/scripts/repo_standards.py`
- Modify: `skills/repo-shape/scripts/plugin_contracts.py`
- Modify: `skills/repo-shape/references/repository-shape-manifest.json`
- Modify: `skills/repo-shape/references/repository-shape-manifest.schema.json`
- Modify: `skills/repo-shape/references/repository-shape-standard.md`
- Modify: `skills/repo-shape/references/consumer-surface-audit.md`
- Test: `skills/repo-shape/tests/scripts/test_repo_standards.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py`

**Interfaces:**

- `repo-standards --check` validates composition and runs only declared standard checks.

- `repo-standards --apply` runs only declared standard apply commands and scaffolds.

- The existing repository command declaration remains the outer apply/check entrypoint for local hooks and hosted CI.

- While legacy consumers are supported, a missing new contract reports migration-required; it never silently means full or empty adoption.

- Plugin installation metadata does not infer standards. Remove mandatory Agent Operating Model, Superpowers+, Repo Worker Pack, and Unslop+ plugin prerequisites.

- [ ] **Step 1: Add selective-dispatch behavior tests**

Use temporary consumer repos and command marker scripts. Assert empty selection runs nothing, a selected pair runs only those commands in declaration order, missing dependencies fail before markers are written, and plugin subscriptions do not change the result.

- [ ] **Step 2: Confirm focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py -q` Expected: FAIL on current fixed requirements and fixed-surface execution.

- [ ] **Step 3: Implement composition-driven apply/check**

Resolve declarations against the catalog, validate dependencies and paths before mutation, dispatch only selected commands, and aggregate only selected generated paths. Keep each standard's validator responsible for its own contract.

- [ ] **Step 4: Verify coordinator and plugin independence**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_repo_standards.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py -q` Expected: PASS for selection, migration diagnostics, and existing mutation safety behavior.

- [ ] **Step 5: Commit selective dispatch**

```powershell
git add skills/repo-shape/scripts/repo_standards.py skills/repo-shape/scripts/plugin_contracts.py skills/repo-shape/references/repository-shape-manifest.json skills/repo-shape/references/repository-shape-manifest.schema.json skills/repo-shape/references/repository-shape-standard.md skills/repo-shape/references/consumer-surface-audit.md skills/repo-shape/tests/scripts/test_repo_standards.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_dispatch.py
git commit -m "feat: dispatch only adopted repository standards"
```

### Task 4: Deploy pinned standard implementations for hosted CI

**Files:**

- Create: `skills/repo-shape/scripts/deploy_operating_standards.py`
- Modify: `skills/repo-shape/scripts/repo_standards.py`
- Modify: `skills/repo-shape/references/ci-validation-pipeline.md`
- Test: `skills/repo-shape/tests/scripts/test_operating_standards_deployment.py`
- Test: `skills/repo-shape/tests/scripts/test_repo_standards_hooks.py`
- Test: `skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py`

**Interfaces:**

- Deployment resolves resources under the consumer's pinned Agent Operating Model package root, copies only declared resources to selected `implementation_root` paths, and records the marketplace commit and resource provenance.

- Deployment also copies the self-contained standard coordinator runtime into `.agents/standards/_runtime/`; hosted CI uses this local copy rather than `.agents/skills/repo-shape/scripts/repo_standards.py`.

- Check mode is read-only. Apply fails closed on path escape, unknown resources, source mismatch, or ambiguous overwrite.

- Hosted checks invoke deployed local files and the existing canonical runner. They do not import `.agents/skills/*` or require Codex plugin installation.

- [ ] **Step 1: Add deployment and hosted-runner behavior tests**

Use a temporary consumer plus marketplace-source fixture. Assert selected-only deployment and provenance, no writes in check mode, safe refusal of path escape/overwrite, and successful hosted check after removing ambient skill directories and plugin declarations. Run skill refresh with deployed standards present and assert the consumer declaration and deployed standard bytes remain unchanged.

- [ ] **Step 2: Confirm the focused tests fail**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py -q` Expected: FAIL because deployed checker resources and ambient-independent execution do not exist.

- [ ] **Step 3: Implement deployment and local execution**

Resolve the pinned Agent Operating Model package root from the consumer's declared marketplace source; do not assume the retired `codex-marketplace/` path. Copy the standard coordinator runtime and only catalog-declared checkers, templates, and command-bus entries into consumer-selected roots. Point local command vectors at `.agents/standards/_runtime/repo_standards.py` and deployed standard roots. Keep source revision tied to deployed copies and prohibit marketplace rolling during hosted checks.

- [ ] **Step 4: Document and verify the hosted contract**

Update `ci-validation-pipeline.md` while preserving its staged-snapshot and hosted-commit contract. Add the ambient-free hosted case to the hook tests.

- [ ] **Step 5: Run focused deployment and hook tests**

Run the same focused pytest command from Step 2. Expected: PASS, including operation without ambient skills or plugin subscriptions.

- [ ] **Step 6: Commit deployment and hosted validation**

```powershell
git add skills/repo-shape/scripts/deploy_operating_standards.py skills/repo-shape/scripts/repo_standards.py skills/repo-shape/references/ci-validation-pipeline.md skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py
git commit -m "feat: deploy standards for hosted validation"
```

### Task 5: Provide a Rooms-compatible refresh and mesh runner bridge

**Files:**

- Create: `skills/repo-shape/references/consumer-runner-migration.md`
- Modify: `skills/repo-shape/references/ci-validation-pipeline.md`
- Modify: `skills/repo-shape/scripts/deploy_operating_standards.py`
- Test: `skills/repo-shape/tests/scripts/test_consumer_runner_migration.py`
- Test: `skills/repo-shape/tests/scripts/test_repo_standards_hooks.py`

**Interfaces:**

- Migration deploys repository-local refresh and mesh entrypoints from the pinned source, then updates consumer apply/check vectors to use those local entrypoints and `.agents/standards/_runtime/repo_standards.py`. Hook/CI operation does not depend on `.agents/skills/` projections.

- For Rooms, the guide identifies the exact `tools/run.py` helpers to update: `_repo_standards_cmd`, `_skills_cmd`, `_mesh_generate_cmd`, and `_mesh_validate_cmd`. The consumer's outer `repo-standards-commands.json` hook vectors remain stable because they still call `tools/run.py ci`.

- The guide updates the consumer's pinned marketplace source to a release containing the Agent Operating Model package and uses that package root for deployment. It does not depend on a legacy package path or a Codex ambient plugin in CI.

- Existing command-bus apply/check operations and staged-snapshot generated-path behavior remain equivalent.

- Test the migration against a self-contained fixture derived from the live Rooms runner. Do not modify `Z:\rooms-mostly`.

- [ ] **Step 1: Add a fixture matching observed Rooms runner behavior**

Model its current `_repo_standards_cmd`, `_skills_cmd`, `_mesh_generate_cmd`, and `_mesh_validate_cmd` implementations, `ci --apply`/`ci --check` declaration, and hosted hook mode. Assert missing skill projections fail before migration and deployed local entrypoints work after the fixture's runner helpers are updated.

- [ ] **Step 2: Confirm the focused migration test fails**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_consumer_runner_migration.py -q` Expected: FAIL because local deployed entrypoints are unavailable.

- [ ] **Step 3: Implement bridge deployment and migration guidance**

Deploy the exact executables and wrappers needed by the observed runner. Preserve argument vectors, source pin, output, return codes, and staged-snapshot behavior. Document order, intermediate checks, and rollback to current plugin-backed commands.

- [ ] **Step 4: Verify migration and hosted hook behavior**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_consumer_runner_migration.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py -q` Expected: PASS with plugin subscriptions and skill projections removed after deployment, while the declared apply/check sequence is preserved.

- [ ] **Step 5: Commit the runner bridge**

```powershell
git add skills/repo-shape/references/consumer-runner-migration.md skills/repo-shape/references/ci-validation-pipeline.md skills/repo-shape/scripts/deploy_operating_standards.py skills/repo-shape/tests/scripts/test_consumer_runner_migration.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py
git commit -m "feat: bridge consumer runners off ambient skill copies"
```

### Task 6: Regenerate, review, and publish Plan 1

**Files:**

- Modify through generators: `dist/plugins/agent-operating-model/`, `.agents/skills/`, indexes, and marketplace metadata

- Review: all source and generated files from Tasks 1-5

- [ ] **Step 1: Run touched repository tests and skill-owned tests**

Run only suites covering changed behavior; do not substitute exact-prose tests for behavior evidence.

- [ ] **Step 2: Regenerate marketplace and installed projections**

Run: `py -3 tools/run.py marketplace --apply` Run: `py -3 tools/run.py installed-skills --apply` Run: `py -3 tools/run.py mesh --apply`

- [ ] **Step 3: Review source and generated outputs**

Confirm only declared resources ship, plugin membership does not imply standard adoption, package dependencies are self-contained, and generated trees were not hand-edited.

- [ ] **Step 4: Commit through the tracked hook and publish a Draft PR**

Stage intended source and generated files and commit normally. Let the tracked hook run the canonical apply/check gate; do not bypass it or run complete CI immediately before or after a successful hooked commit. Push, open a Draft PR, and verify its head and hosted checks before marking Plan 1 complete in the roadmap.

## Completion boundary

Plan 1 completes when selective standards can be deployed and checked without ambient plugins, fixed plugin prerequisites are removed, and the Rooms-equivalent runner fixture passes with local deployed utilities. It does not change Superpowers+, MCP Usage Pack, or Unslop+ guidance, complete capability-based workflow composition, or migrate Rooms or another consumer.
