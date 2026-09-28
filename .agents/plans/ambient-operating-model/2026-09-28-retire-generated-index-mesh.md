# Retire Generated Index Mesh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the generated index system from the marketplace, its shipped products, and its consumer guidance, including the mesh skill and every tracked `INDEX.md` or `INDEX.json` artifact.

**Architecture:** Retire both generators that produce the repository's generated navigation indexes: `generating-agent-mesh` for Markdown and `generate_repo_index.py` for JSON sidecars. Remove their CLI, CI, worktree, skill-refresh, standard-validation, and packaging integrations; update guidance that requires index files; then delete generated outputs from source and built projections. Preserve distinct marketplace manifests and registries that are not index artifacts.

**Tech Stack:** Python 3, pytest, marketplace source definitions and generators, `tools/run.py` task graph.

**Spec:** `.agents/plans/ambient-operating-model/roadmap.md` (Plan 1 retirement scope); the approved ambient design remains at `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md` for consumer boundaries.

**Execution Strategy:** `executing-plans` - the retirement spans a dependency-ordered CLI, agent-skill, consumer-contract, and generated-output cutover. Those changes need one shared view of what counts as an index artifact, and the final absence check depends on all source generators and references being removed first.

## Global Constraints

- Remove all tracked files named `INDEX.md` or `INDEX.json`; do not replace them with another generated index or parallel table of contents.
- Remove `generating-agent-mesh` from canonical skill source, Repo Worker Pack membership, and shipped output.
- Remove mesh and repo-index generation and validation from normal local, worktree, and hosted CI workflows.
- Do not edit consumer repositories. Update portable marketplace guidance so consumers can remove their generated indexes and mesh commands safely.
- Preserve non-index marketplace manifests, plugin inventories, provenance, and validation needed to build and publish products.
- Edit canonical sources and definitions, then regenerate `dist/` and `.agents/skills/` through their owning commands.
- Do not create tautological or change-detector tests; test runner behavior and consumer contracts at their owning boundaries.

## Review Focus

- The normal CI dependency graph still applies marketplace generation, installed-skill refresh, and substantive validation after both index targets are removed; cover in `tests/repository/test_run_cli.py`.
- A consumer's shape and document checks no longer fail solely because runbook/playbook inventory `INDEX.md` files are absent; cover in repo-shape behavior tests.
- Worktree creation and skill refresh succeed without looking up or invoking the mesh generator; cover in `skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py` and the refresh skill's behavior suite.
- Marketplace and shipped plugin trees contain no generated index artifacts after regeneration; cover with the existing marketplace build/shipping verification path, not a test that merely searches for deleted names.

______________________________________________________________________

### Task 1: Preserve link and doctrine-route validation without indexes

**Files:**

- Create: `tools/validate_markdown_links.py`
- Test: `tests/repository/test_markdown_links.py`
- Modify: `tools/run.py`
- Test: `tests/repository/test_run_cli.py`

**Interfaces:**

- `tools/validate_markdown_links.py --check` checks tracked Markdown links resolve inside the repository and active doctrine files are routed; during transition it accepts current `AGENTS.md` or `INDEX.md` routes, and Task 3 removes the `INDEX.md` fallback after updating guidance.

- The normal `validate` and `ci` paths run this focused validator while the existing mesh tooling remains temporarily available until Task 2.

- [ ] **Step 1: Add link and route behavior tests**

Create repository behavior tests for resolving relative Markdown links and anchors, rejecting broken and repo-escaping links, ignoring external URLs, and requiring active doctrine routes through an ancestor `AGENTS.md`. Add runner coverage showing that `validate` and `ci` invoke the focused link validator.

- [ ] **Step 2: Run focused validator tests and observe the old behavior fail**

Run: `py -3 -m pytest tests/repository/test_markdown_links.py tests/repository/test_run_cli.py -q`

Expected: FAIL because link and doctrine-route behavior is currently bundled in the generator skill, not exposed as a focused validator.

- [ ] **Step 3: Implement the focused validator and runner integration**

Move local-link and doctrine-route validation into `tools/validate_markdown_links.py`, reusing existing parsing behavior where suitable. Include tracked Markdown collection, URL decoding, fragments, and repository-boundary checks. Until Task 3 updates all guidance, permit the current `INDEX.md` route as well as ancestor `AGENTS.md`; wire the command into `_run_validate` without changing generation targets yet.

- [ ] **Step 4: Verify link and route behavior**

Run the focused pytest command from Step 2. Confirm all link and doctrine-route tests pass, `validate` invokes the command, and existing mesh checks still pass during this transitional task.

- [ ] **Step 5: Commit runner retirement**

```powershell
git add tools/run.py tools/validate_markdown_links.py tests/repository/test_run_cli.py tests/repository/test_markdown_links.py
git commit -m "refactor: separate markdown link validation from index mesh"
```

### Task 2: Remove index generators, mesh skill, and capability integrations

**Files:**

- Delete: `tools/generate_repo_index.py`
- Delete: `tools/validate_repo_index.py`
- Modify: `tools/marketplace_utils.py` (remove index path and sidecar helpers only)`r`n- Modify: `tools/validate_marketplace.py` (remove the JSON index validation phase while retaining inventory, project, and shared-reference validation)
- Modify: `tools/run.py`
- Modify: `tools/README.md`
- Delete: `.agents/docs/repo-index.md`
- Test: `tests/repository/test_run_cli.py`
- Test: `tests/build/test_plugin_definition_contract.py`
- Test: `tests/build/test_plugin_assembly.py`
- Delete: `skills/generating-agent-mesh/`
- Modify: `src/plugin-definitions/repo-worker-pack/contents.json`
- Modify: `skills/refreshing-installed-skills/SKILL.md`
- Modify: `skills/using-git-worktrees/scripts/new_worktree.py`
- Test: `skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py`
- Modify: `skills/repo-worker-base/SKILL.md`
- Rename and edit: `skills/repo-worker-base/references/repository-layout-and-mesh.md` to `skills/repo-worker-base/references/repository-layout.md`, retaining useful layout guidance and removing generated-index instructions
- Modify: `skills/selecting-a-subagent/SKILL.md`
- Delete: `skills/selecting-a-subagent/assets/reviewer-mesh.md`
- Modify: `.agents/agents/reviewer-marketplace.md` to remove the generated-index review remit
- Modify: `skills/using-superpowers-plus/references/repo-doctrine.md` to remove mesh-policy routing
- Test: `skills/refreshing-installed-skills/tests/scripts/test_refresh_installed_skills.py`

**Interfaces:**

- `refreshing-installed-skills` refreshes skill projections only and does not generate indexes.

- `using-git-worktrees` creates and prepares a worktree without mesh discovery, mesh scripts, or mesh warning/failure branches.

- Local Markdown link validation remains available as a focused check from Task 1; active doctrine reachability is checked through `AGENTS.md` routes only, never through a generated index.

- Repo Worker Pack retains its other general-purpose worker skills but no longer packages `generating-agent-mesh`.

- [ ] **Step 1: Update behavior tests before removing integrations**

Change `tests/repository/test_run_cli.py` to assert resolving `ci` contains no `repo-index`, `mesh`, or `index-mesh` targets and that it still includes validation. Add a test that explicit retired target names are rejected with the normal unknown-target diagnostic. Cover retained marketplace validation phases and the removed `index` phase. Inspect the JSON index generator and validator for metadata beyond navigation; preserve product and registry metadata in their canonical existing marketplace definitions. Change worktree-script behavior tests to prove worktree preparation no longer dispatches mesh generation while preserving refresh and dependency-install capabilities. Remove mesh-skill tests together with the retired skill rather than relocating tests for deleted behavior. The focused link validator routes active doctrine only through `AGENTS.md` files.

- [ ] **Step 2: Run focused skill tests and observe old behavior fail**

Run: `py -3 -m pytest tests/repository/test_run_cli.py tests/build/test_plugin_definition_contract.py tests/build/test_plugin_assembly.py skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py tests/repository/test_markdown_links.py -q`

Expected: FAIL because worktree preparation and refresh guidance still invoke or expect mesh generation.

- [ ] **Step 3: Remove source, membership, and all integration branches**

Delete the JSON index generator/validator and index-only utilities after confirming whether they carry unique product metadata. Remove the JSON index phase from `tools/validate_marketplace.py`; retain its inventory, project, and shared-reference checks. The `marketplace_plugins` view in `INDEX.json` duplicates canonical plugin registry and manifest data, so drop that navigation-derived view and keep those existing sources canonical. Remove the `repo-index`, `mesh`, and `index-mesh` tasks and their dependencies from `tools/run.py`; update `tools/README.md` and remove `.agents/docs/repo-index.md`. Delete the canonical mesh skill and tests, remove its Repo Worker Pack membership, and adjust the refreshing, worktree, Repo Worker Base, reviewer, and doctrine guidance identified in the file list. Preserve general worktree safety and worker guidance; remove mesh-specific policy, commands, fallback warnings, and reviewer profile behavior.

- [ ] **Step 4: Verify ambient pack and worktree behavior**

Run `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py installed-skills --apply` after source and plugin-definition edits. Then run the focused pytest command from Step 2 and `py -3 tools/run.py installed-skills --check`. Confirm the validator from Task 1 remains in the normal `validate`/`ci` path and retains link/route failures without generating navigation files.

- [ ] **Step 5: Commit skill retirement**

```powershell
git add -A tools skills src/plugin-definitions/repo-worker-pack .agents/agents/reviewer-marketplace.md .agents/docs/repo-index.md tests/repository tests/build
git commit -m "refactor: retire generated index systems"
```

### Task 3: Remove index-file requirements from standards and guidance

**Files:**

- Modify: `skills/repo-shape/scripts/_agents_md.py`
- Modify: `skills/repo-shape/scripts/document_contracts.py`
- Modify: `skills/repo-shape/scripts/repo_standards.py`
- Modify: `skills/repo-shape/templates/agents-md.template.md`
- Modify: repo-shape references that prescribe runbook/playbook `INDEX.md` inventories
- Modify: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, `.agents/doctrine/AGENTS.md`, `.agents/runbooks/AGENTS.md`, `.agents/playbooks/AGENTS.md`, `tools/validate_agents_md.py`, `.agents/doctrine/docs.md`, `.agents/doctrine/first-party-skills.md`, `.agents/doctrine/marketplace-worker-doctrine.md`, `.agents/doctrine/tools.md`, `.agents/playbooks/marketplace-generation.md`, `.agents/playbooks/repo-doctrine.md`, `.agents/README.md`, and any remaining canonical guidance found by the scoped reference search
- Delete: `.agents/doctrine/mesh-policy.md`
- Delete: `docs/decisions/0002-derived-agent-mesh.md`
- Modify: `docs/decisions/README.md` to remove links to deleted generated decision indexes
- Test: `skills/repo-shape/tests/scripts/test_repo_standards.py`
- Test: `skills/repo-shape/tests/scripts/test_repo_composition.py`
- Modify: `skills/repo-shape/references/vendor-profile-deployment.md` and `skills/repo-shape/scripts/deploy_vendor_profiles.py` to remove special handling for a generated index that will no longer exist
- Test: `skills/repo-shape/tests/scripts/test_repo_standards_hooks.py`
- Test: `skills/repo-shape/tests/scripts/test_operating_model_document_contracts.py`

**Interfaces:**

- Repo-shape and document-contract checks validate authored documents and declared standards without requiring generated navigation files or their fixed paths.

- Templates and routing guidance link directly to the authoritative runbooks, playbooks, or doctrine needed for the task; they do not create a substitute generated catalog.

- Consumers may remove their mesh files and generation command without failing the marketplace's portable shape contract.

- [ ] **Step 1: Add missing-index consumer behavior cases**

In existing repo-shape behavior tests, create otherwise-valid fixtures with runbook and playbook content but no `INDEX.md`. Assert checks pass and authored document discovery still excludes `AGENTS.md` and includes the actual runbook/playbook files. Update template assertions to check useful direct routing links rather than inventory links. Update generated-path fixtures to remove index-only paths while preserving other declared generated outputs.

- [ ] **Step 2: Run focused shape/composition tests and observe failure**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_repo_standards.py skills/repo-shape/tests/scripts/test_repo_composition.py skills/repo-shape/tests/scripts/test_repo_standards_hooks.py -q`

Expected: FAIL because current validators, templates, and fixtures treat inventory indexes as required.

- [ ] **Step 3: Remove mandatory index contracts and mesh doctrine**

Update canonical skill code, references, and templates so index presence is not a required standard surface. Change `tools/validate_markdown_links.py` so active doctrine must route through an ancestor `AGENTS.md` and no longer accepts `INDEX.md`. Remove the mesh-policy doctrine and obsolete ADR, and remove their routing pointers. Preserve non-mesh doctrine such as AGENTS.md scope, ownership, and repository navigation that remains useful without generated indexes.

- [ ] **Step 4: Document the consumer cutover in existing portable guidance**

Update the existing Repo Worker Base and repo-shape guidance to tell consumers to remove tracked generated `INDEX.md` and `INDEX.json` files and remove mesh/repo-index commands from local and hosted runners. State that no replacement subscription or generated inventory is needed. Do not edit `Z:\rooms-mostly` or another consumer checkout.

- [ ] **Step 5: Verify the consumer contract without indexes**

Run the focused pytest command from Step 2. Confirm missing generated indexes do not cause shape, document, hook, or CI contract failures in the fixtures.

- [ ] **Step 6: Commit the standards and migration contract**

```powershell
git add -A AGENTS.md .agents skills/repo-shape skills/repo-worker-base docs/decisions
git commit -m "refactor: remove generated index requirements"
```

### Task 4: Remove generated index artifacts and publish clean projections

**Files:**

- Delete through owning generation/removal workflow: every tracked `INDEX.md` and `INDEX.json` under the repository, including canonical navigation files, plugin definition snapshots, and `dist/` projections
- Modify through canonical sources: `src/plugin-definitions/repo-worker-pack/contents.json` and any preserved metadata source found in Task 1
- Regenerate: marketplace distributions and installed skill projections with `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py installed-skills --apply`
- Modify: `docs/decisions/README.md` and other surviving docs to remove links to deleted index files
- Verify: `tests/build/`, `tests/shipping/`, marketplace validation, and full canonical CI

**Interfaces:**

- No `INDEX.md` or `INDEX.json` files remain tracked in canonical marketplace source, plugin definition file snapshots, installed projections, or `dist/`.

- Marketplace output remains discoverable through its existing manifest, plugin roots, package manifests, source definitions, and marketplace validation commands.

- Normal CI no longer calls a removed generator and continues to verify the surviving product metadata.

- [ ] **Step 1: Remove generated artifacts from canonical and product trees**

After Tasks 1-3 have removed their producers and all consumers, delete every tracked file whose basename is exactly `INDEX.md` or `INDEX.json`. Remove links to them from `AGENTS.md`, doctrine, playbooks, README files, and decision indexes. Keep separate files such as `dist/manifest.json`, `plugin-roots.json`, and package `bundle-manifest.json`; these are product manifests, not generated navigation index sidecars.

- [ ] **Step 2: Regenerate marketplace and installed projections**

Run:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
```

Expected: `dist/` and `.agents/skills/` reflect source membership without `generating-agent-mesh` or any generated index files. The marketplace generator must not recreate an index file.

- [ ] **Step 3: Verify package and consumer migration behavior**

Run the touched repo-shape and runner tests from Tasks 1-3, then run `py -3 tools/run.py tests-build tests-shipping --check`. Run `rg --files --hidden -g INDEX.md -g INDEX.json -g '!.git/**'` and confirm it returns no files. Search active source and portable consumer instructions for mesh generator commands; historical references in this implementation plan and roadmap are allowed, but executable commands and active guidance are not.

- [ ] **Step 4: Run the canonical validation path**

Run: `py -3 tools/run.py ci --apply` for explicit uncommitted diagnosis only if needed. For normal publication, stage the intended tree and commit through the tracked hook, which runs the canonical apply/check gate. Do not run the full check immediately before or after a successful hooked commit.

- [ ] **Step 5: Review product output and publish a Draft PR**

Review source and generated diff for complete index removal, preserved non-index marketplace metadata, consumer migration clarity, and no remaining mesh runtime calls. Push the branch and open a Draft PR. Verify the PR head and hosted checks before marking Plan 1 complete in the roadmap.

## Completion boundary

Plan 1 completes when the mesh skill and both generated index layers are retired, no `INDEX.md` or `INDEX.json` files remain in the marketplace repository or shipped plugin outputs, consumer standards no longer require them, and the normal runner and marketplace build work without mesh/index commands. Consumer repositories are not modified in this plan; their agents use the updated portable guidance to migrate each consumer independently.
