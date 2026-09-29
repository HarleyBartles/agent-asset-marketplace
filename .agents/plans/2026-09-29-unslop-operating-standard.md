# Unslop Operating Standard and Profile Workflows Implementation Plan

> **Artifact status:** `completed-awaiting-retirement` - implementation is committed and handed off in Draft PR #342; retire this plan from the repository in the successor slice.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make consumer-owned Unslop profiles an opt-in, checkable Operating Model standard while Unslop+ supplies ambient profile application and profile maintenance capabilities.

**Architecture:** Add an `unslop` selectable standard to the Agent Operating Model catalog. It owns a machine-readable adoption contract at `.agents/contracts/unslop.json`, operational profile documents under `.agents/unslop/` (and any consumer-declared additional roots), workflow routing guidance, and focused structure/routing checks. Expand the Unslop+ skills so `unslop-profiles` discovers and applies matching consumer or generic profiles, while `unslop-engine` supports reviewable profile lifecycle work and clearly does not evaluate adherence to profiles.

**Tech Stack:** Markdown skill and standard sources, JSON contracts and catalog, Python standard-library validators, Marketplace build and repository CI tooling.

**Spec:** Approved consumer-agent letter and design decisions in the Codex conversation dated 2026-09-29. Binding decisions: the standard is opt-in and separate from repo-shape; consumer profiles live in `.agents/unslop/`; machine-readable adoption configuration remains a contract; profiles are operational guidance subordinate to doctrine; profile adherence is judged through profile-guided review unless a deterministic check is defined.

**Execution Strategy:** `executing-plans` - the standard contract, deployment, profile discovery, and skill routing share one profile interface and generated Marketplace outputs. Sequential in-context execution keeps those interfaces coherent; subagent-driven development would add handoffs across tightly coupled source and generated surfaces without useful parallelism.

## Global Constraints

- The Unslop standard is an explicit optional Operating Model subscription; plugin installation alone does not adopt it.
- Consumer profile documents live under `.agents/unslop/` by default and remain identifiable as operational profiles, not contracts.
- Adoption configuration is machine-readable at `.agents/contracts/unslop.json`; it declares profile roots and defaults to `.agents/unslop/`.
- Doctrine remains authoritative for binding rules. Profiles may link to doctrine and skills but must not restate binding policy as profile rules.
- Profile checks validate declared structure, roots, and workflow routing. They do not claim to decide whether real work followed a profile.
- Unslop+ application is grounded in concrete output or decisions, proportionate, false-positive-aware, and skipped when no profile fits.
- The engine may propose profile creation, revision, or retirement from recurring evidence; it must not automatically rewrite profiles after individual mistakes.
- Edit canonical sources under `skills/` and `src/plugin-definitions/`; regenerate Marketplace outputs with repository tooling.

## Review Focus

- A repository can adopt the Unslop standard without installing Unslop+ or any other ambient skill; standard deployment and validation must remain independently usable (Task 1).
- A repository with no adopted standard or no matching local profile still gets appropriate generic-profile behavior when available, and profile application is skipped when none fits (Task 3).
- Profile language that contains a listed cue intentionally, or a precise term the profile dislikes, must not be mechanically rewritten when meaning and task intent justify it (Task 3).
- Engine/package validation must not report profile adherence or convert a sample-level pattern count into a claim about real work (Task 4).

______________________________________________________________________

### Task 1: Define and validate the opt-in Unslop standard

**Files:**

- Create: `skills/repo-shape/references/unslop-standard.md`
- Create: `skills/repo-shape/references/unslop-contract.schema.json`
- Create: `skills/repo-shape/scripts/unslop_standard.py`
- Create: `skills/repo-shape/tests/scripts/test_unslop_standard.py`
- Modify: `skills/repo-shape/references/operating-standards-catalog.json`
- Modify: `skills/repo-shape/references/operating-standards-catalog.schema.json`
- Modify: `skills/repo-shape/scripts/operating_standards_catalog.py`
- Modify: `skills/repo-shape/references/repository-shape-manifest.json`
- Modify: `skills/repo-shape/references/repository-shape-standard.md`
- Modify: `skills/repo-shape/tests/scripts/test_operating_standards_catalog.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_standards_deployment.py`

**Interfaces:**

- The catalog entry id is `unslop`; its resources include the standard document, contract schema, and validator. It selects a dedicated optional `unslop-contract` surface in the repository-shape manifest and runs only when the consumer explicitly declares it. Add optional catalog field `legacy_migration` with values `infer` (default for existing standards) or `explicit`; set `unslop` to `explicit` so legacy migration never infers adoption from repo-shape surface presence.

- The consumer contract is `.agents/contracts/unslop.json`, version 1, with `profile_roots` as repository-relative paths defaulting to `[".agents/unslop"]`.

- Each profile is a Markdown document with a stable profile id and explicit sections for task trigger/scope, recurring failure pattern, recognition cues, corrective behavior, false-positive/override boundaries, applicable workflow paths, doctrine or skill references, and an application example.

- The validator is the surface scaffold for `.agents/contracts/unslop.json`; read-only `--check` validates the contract, profiles, and workflow routes, while `--apply` creates only a missing default contract and preserves consumer-authored content. The existing Operating Model runner invokes it only for repositories that adopt the standard.

- [x] **Step 1: Add behavior tests for adoption and profile validation**

Add tests proving that the standard accepts the default `.agents/unslop` root and additional safe repository-relative roots; rejects malformed contracts, absolute paths, traversal paths, a declared root that is a file, duplicate profile ids, missing required profile sections, broken local references, and routes to missing workflows; allows an empty or not-yet-created root; and does not require any Unslop+ plugin subscription. Include a valid example whose recognition cue appears intentionally in its application example, proving the validator checks profile structure rather than banning profile vocabulary.

- [x] **Step 2: Run the focused standard test module and observe the expected failures**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_unslop_standard.py -q` Expected: FAIL because the standard validator and its catalog entry do not yet exist.

- [x] **Step 3: Implement the contract parser and standard check/apply behavior**

Implement the JSON contract schema and Markdown-profile checks in `unslop_standard.py`. Resolve declared workflow paths against tracked repository files and require each routed workflow to direct the agent to `$unslop-profiles` at the relevant task stage. Apply creates a missing adoption contract with the default `.agents/unslop` root; it does not invent consumer profile content. Keep profile quality judgment human-readable in the standard and examples; deterministic checks should verify structure, paths, and explicit links only. Register the `unslop` standard in the catalog with its implementation resources and check/apply flags. Remove the old claim in repo-shape that profiles are binding contracts.

- [x] **Step 4: Run the focused standard tests and catalog/deployment tests**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_unslop_standard.py skills/repo-shape/tests/scripts/test_operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards.py -q` Expected: PASS; catalog resource pinning and standard resource deployment include the new validator and standard document.

### Task 2: Move adoption settings out of the general operating-model contract

**Files:**

- Modify: `skills/repo-shape/templates/agent-operating-model.json`
- Modify: `skills/repo-shape/scripts/scaffold_operating_model_contract.py`
- Modify: `skills/repo-shape/scripts/plugin_contracts.py`
- Modify: `skills/repo-shape/scripts/migrate_operating_standards.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_model_surface_contracts.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py`
- Modify: `skills/repo-shape/tests/scripts/test_operating_standards_migration.py`
- Modify: `.agents/contracts/agent-operating-model.json`
- Modify: `.agents/doctrine/contracts.md`

**Interfaces:**

- `.agents/contracts/agent-operating-model.json` retains only general operating-model settings such as `version` and `surface_exceptions`; it no longer carries `unslop_profile_roots`.

- `.agents/contracts/unslop.json` is required only when `unslop` is explicitly adopted in `.agents/contracts/operating-standards.json`.

- Legacy consumers without the `unslop` standard remain valid and do not need Unslop contracts, profile directories, or plugin subscriptions. Migration never selects `unslop` based only on the optional repo-shape surface; explicit adoption occurs in the consumer's operating-standards composition.

- [x] **Step 1: Update focused tests for the general contract and migration boundary**

Change tests so an operating-model contract with no Unslop field is valid; obsolete `unslop_profile_roots` is reported as unsupported drift rather than silently treated as current configuration; plugin contract discovery does not inspect or require consumer profiles; and a legacy migration fixture with the new optional surface enabled does not adopt `unslop` or create a profile requirement implicitly.

- [x] **Step 2: Run the focused repo-shape contract tests and observe the expected failures**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_operating_model_surface_contracts.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py -q` Expected: FAIL against the old required `unslop_profile_roots` behavior.

- [x] **Step 3: Remove Unslop configuration from the generic operating-model contract**

Update its template/scaffold validation and plugin prerequisite code, remove the field from this repository's own contract, and revise contract custody doctrine so profiles are operational guidance under `.agents/unslop/`. Adoption and profile-root checks belong exclusively to the new standard. Honor the catalog's explicit-only legacy migration policy for `unslop`; existing inferred-standard migration behavior remains unchanged for every other standard.

- [x] **Step 4: Run the focused contract and migration tests**

Run the command from Step 2. Expected: PASS with both current contracts and legacy migration behavior covered.

### Task 3: Make Unslop+ apply profiles across consumer and generic sources

**Files:**

- Modify: `skills/unslop-profiles/SKILL.md`
- Modify: `skills/unslop-profiles/agents/openai.yaml`
- Modify: `skills/unslop-profiles/tests/pressure/optional-provider-absent.md`
- Create: `skills/unslop-profiles/tests/pressure/consumer-profile-discovery.md`
- Create: `skills/unslop-profiles/tests/pressure/profile-boundaries-and-skip.md`
- Modify: `src/plugin-definitions/unslop-plus/plugin.json`
- Modify: `src/plugin-definitions/unslop-plus/files/README.md`
- Modify: `src/plugin-definitions/unslop-plus/files/SOURCE.md`

**Interfaces:**

- `unslop-profiles` locates and reads consumer profiles from adopted standard roots when available, then considers applicable bundled generic profiles. It does not require the consumer standard or plugin installation to be present to run using bundled profiles.

- When multiple profiles match, the skill applies compatible guidance together and does not silently reconcile conflicts. Doctrine, evidence, user intent, and profile scope remain the boundaries for resolving a conflict.

- A profile is applied only when its trigger and scope fit the task. Application uses specific cues and corrective moves during work and review, cites concrete output/decisions, and preserves meaning, evidence, clarity, and user intent.

- The skill skips profile use when no profile fits, and handles intentional cue use or justified terminology as false positives rather than keyword violations.

- [x] **Step 1: Add pressure scenarios for local discovery, precedence, boundaries, and skip behavior**

Write scenarios proving that the skill reads a declared consumer profile before use; can apply consumer and generic profiles without conflating their authority; names a concrete observed decision/output before recommending a correction; preserves justified terminology and intentional examples; and skips when no profile matches. Keep the existing optional-provider scenario and clarify that absence of writing-pack does not block applicable Unslop profile use.

- [x] **Step 2: Update the skill instructions and package descriptions**

Replace the static task-to-bundled-file-only router with a discovery and application workflow. Require reading the profile, using it during work and review, grounding findings in concrete evidence, correcting proportionately, and respecting false positives and doctrine precedence. Describe consumer profiles as operational guidance. Update plugin metadata and README/SOURCE so package discovery no longer promises only the current built-in task table.

- [x] **Step 3: Review the resulting skill instructions against each pressure scenario**

Evaluate each skill-owned pressure scenario in a fresh isolated context using the prompt in the scenario and the built `unslop-profiles` skill. Record the scenario and observed pass/fail findings in the implementation handoff; keep transcripts and run metadata out of Git. Expected: each scenario follows the correct discovery, apply, and skip behavior without a mechanical keyword ban.

### Task 4: Bound the engine to profile lifecycle support, not adherence scoring

**Files:**

- Modify: `skills/unslop-engine/SKILL.md`
- Create: `skills/unslop-engine/tests/pressure/profile-maintenance-boundary.md`

**Interfaces:**

- `unslop-engine` supports a consumer-reviewed lifecycle: gather recurring evidence, propose a profile/revision/retirement, validate profile structure, and leave the final decision to the consumer.

- Existing sample analysis and generated-package validation retain their current claims and outputs; neither claims that an agent followed or violated an operational profile.

- No profile is automatically modified after a single mistake, and incident notes are not accumulated as profile content.

- [x] **Step 1: Specify profile lifecycle and scope boundaries in the engine skill**

Document when recurring evidence justifies creation, revision, or retirement; require a consumer-reviewable proposal and operational guidance rather than incident accumulation; link to the Unslop standard/profile shape; and state that real-work adherence is assessed by profile-guided review unless an explicit deterministic check exists.

- [x] **Step 2: Evaluate the engine lifecycle boundary scenario**

In a fresh isolated context, use the engine skill with a single observed mistake and with evidence of a recurring pattern. Confirm the single mistake yields no automatic profile rewrite, while recurring evidence yields a reviewable proposal; confirm neither run claims the agent followed or violated a profile. Record observed findings in the handoff and keep run artifacts out of Git.

### Task 5: Migrate Marketplace-owned profile, route workflows, regenerate, and verify

**Files:**

- Move: `.agents/contracts/unslop/repository.md` to `.agents/unslop/repository.md`
- Create: `.agents/contracts/unslop.json`
- Modify: `.agents/contracts/operating-standards.json` to explicitly adopt `unslop` for this Marketplace repository and pin the current Marketplace revision as required by the catalog contract.
- Modify: `.agents/unslop/repository.md` to use the operational profile shape, reference Marketplace doctrine instead of duplicating its binding rules, and declare routes to `.agents/runbooks/planning.md`, `.agents/runbooks/implementing.md`, `.agents/runbooks/code-review.md`, and `.agents/runbooks/pr.md`.
- Modify: `.agents/runbooks/planning.md`, `.agents/runbooks/implementing.md`, `.agents/runbooks/code-review.md`, and `.agents/runbooks/pr.md` to route applicable work to `$unslop-profiles` at the appropriate stage.
- Modify: generated `dist/` and `.agents/standards/` projections through their owning build/deployment commands; do not hand-edit them.
- Modify: tests that still expect `.agents/contracts/unslop/` or the `unslop_profile_roots` field.

**Interfaces:**

- The Marketplace's own profile is a consumer-owned example of the new standard and remains distinct from bundled generic starter profiles.

- Workflow references resolve to existing profiles and explicitly route to `unslop-profiles`; the skill remains usable in repositories that do not adopt the standard.

- Generated plugin and deployed-standard outputs are reproducible from `skills/` and `src/plugin-definitions/`.

- [x] **Step 1: Write focused migration and route behavior tests**

Update tests to assert the Marketplace profile lives under `.agents/unslop/`, the standard contract declares that root, standard adoption is explicit, each declared workflow route resolves and names `$unslop-profiles`, and no plugin subscription is required by the standard. Remove assertions that profile presence is checked by generic plugin prerequisite validation.

- [x] **Step 2: Migrate the Marketplace consumer surfaces and workflow routes**

Move the local profile, add the Unslop contract, and adopt the pinned standard. Update only the workflows whose stage or task scope uses an applicable profile. Keep binding rules in doctrine and profile failure cues/corrections in the profile. Do not add a global always-on instruction that forces profile use for unrelated tasks.

- [x] **Step 3: Run focused affected test modules**

Run: `py -3 -m pytest skills/repo-shape/tests/scripts/test_unslop_standard.py skills/repo-shape/tests/scripts/test_operating_model_surface_contracts.py skills/repo-shape/tests/scripts/test_operating_model_plugin_contracts.py skills/repo-shape/tests/scripts/test_operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_operating_standards_migration.py -q` Expected: PASS; tests cover standard adoption, deployment, opt-in migration, and the contract boundary.

- [x] **Step 4: Regenerate source-owned Marketplace and standard projections**

Run: `py -3 tools/run.py marketplace --apply` Run: `py -3 tools/run.py repo-standards --apply` Expected: generated `dist/plugins/unslop-plus/` matches the canonical skills and plugin definition; `.agents/standards/` includes the pinned `unslop` standard resources and excludes stale profile-root ownership from repo-shape.

- [x] **Step 5: Verify source, distribution, and repository gates**

Run: `py -3 tools/run.py installed-skills --check` Run: `py -3 tools/build_marketplace.py --check` Run the selected standard directly with `py -3 .agents/standards/_runtime/repo_standards.py --run-standard unslop --check`. For repository-wide validation, stage the intended tree and let the tracked pre-commit hook perform the canonical apply/check gate; use `py -3 tools/run.py ci --apply` followed by `py -3 tools/run.py ci --check --diagnostics` only when diagnosing convergence outside a normal commit. Do not run the full check immediately before or after a successful hooked commit. Expected: source projections are current, the selected standard check passes for this repository, generic legacy consumers remain valid, and the full repository gate passes.

- [x] **Step 6: Review, commit, and hand off the implementation branch**

Review the final diff against the approved letter and this plan. Confirm no generated output was hand-edited, no profile is presented as binding doctrine, and no validator makes an adherence claim. Commit through the tracked hook, push the branch, open a Draft PR, attach the PR artifact, and verify the published head and required checks before handing off.
