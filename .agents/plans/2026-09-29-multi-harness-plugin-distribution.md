# Multi-Harness Plugin Distribution Implementation Plan

> **Artifact status:** Active planning handoff. Implementation has not started; the unchecked tasks below describe future work. This planning-only Draft PR is intentionally incomplete until a worker executes the plan.
>
> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let Codex and Devin consumers declare repo-scoped Git plugin dependencies, let AOM scaffold and validate the opt-in standard that each repo owns, and give ACP workers a harness-native way to refresh plugins for the current repo.

**Architecture:** Keep plugin source and composition in this Marketplace and publish complete packages from `main`. Consumers keep native Codex and Devin declarations that point at Git subdirectories and moving published branches by default; plugin payloads are fetched and cached by the harness, never projected into consumer `.agents/skills/`. AOM ships the deployable subscription-standard scaffold and conformance validator; ACP ships the ambient `refreshing-installed-plugins` capability. Remove the former projection updater only after its other callers and responsibilities have explicit owners.

**Tech Stack:** Python 3, JSON and Markdown source, the existing Marketplace generator and CI, Codex repo marketplaces, Devin repo plugin manifests, Git branches and worktrees.

**Spec:** `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md`

**Execution Strategy:** `executing-plans` - the work is sequential and contract-coupled: native behavior gates the subscription contract; AOM scaffolding and validation define the declaration shape ACP consumes; the old updater and worktree callers can be retired only after those replacement surfaces exist. One executor preserves that shared context; subagent handoffs would add reconstruction without useful parallelism. A fresh whole-branch review follows implementation.

## Global Constraints

- Ambient installation and refresh remain harness and operator responsibilities; AOM does not manage ambient plugins.
- Codex's current Marketplace remains valid and its existing plugin catalog identity remains updateable through the native Marketplace flow.
- A consumer repo records its own native declarations; it does not check in Marketplace plugin payloads or project their skills into `.agents/skills/`.
- Marketplace subscriptions default to the published `main` branch; a fixed commit SHA is an explicit consumer choice.
- AOM artifacts scaffold an opt-in standard and validate conformance; a consumer owns the adopted implementation and its native config.
- ACP provides `refreshing-installed-plugins` as an ambient capability that acts only on the current repo's declarations.
- Public product display name becomes Agent Capability Pack. Retain the existing machine catalog key `repo-worker-pack` during this change to preserve existing Codex installs; do not add a duplicate catalog entry.
- Wild Bunch migration is a handoff to a responsible agent in Wild Bunch. This plan does not edit that repository.
- Claude Code-only packages and metadata are out of scope.
- Do not remove repo-authored `.agents/skills/`, generic submodule support, or `repo-shape` vendor-profile deployment as collateral to removing plugin projections.

## Review Focus

- Codex project configuration must refresh a moved Git `ref` and scope skill availability to the declaring repo and its worktrees (Task 1).
- Devin's repo `requiredPlugins` must use repo scope and floating refs without becoming a user-level install (Tasks 3 and 5).
- Retiring plugin projections must preserve declared repo-authored skills and independent vendor-profile deployment (Task 6).
- Renaming the ambient pack's display name must not orphan existing Codex installs (Task 2).
- Missing or invalid native declarations must fail AOM validation with an actionable path and finding, without downloading plugin payloads (Task 3).

## File Structure

The implementation edits canonical source, then regenerates shipped Marketplace packages.

- **Codex/Devin package source:** `src/marketplace/build.py`, `src/marketplace/definitions.py`; `src/plugin-definitions/repo-worker-pack/plugin.json`, `src/plugin-definitions/repo-worker-pack/contents.json`, and `src/plugin-definitions/repo-worker-pack/files/{README.md,SOURCE.md,package.json}`; generated `dist/plugins/repo-worker-pack/` and catalog/inventory surfaces.
- **AOM standard source:** `skills/repo-shape/references/operating-standards-catalog.json`, its schema, `repository-shape-manifest.json`, standard documentation/templates, and a focused validator plus tests under `skills/repo-shape/`. Update `skills/repo-shape/scripts/deploy_operating_standards.py` to scaffold from the installed AOM plugin package as well as the Marketplace source checkout.
- **AOM capability guidance:** `skills/repo-agent-assets/SKILL.md` and its declared source/composition in `src/plugin-definitions/agent-operating-model/contents.json`.
- **ACP capability source:** new `skills/refreshing-installed-plugins/SKILL.md` and its behavior-focused tests; `src/plugin-definitions/repo-worker-pack/contents.json` replaces the old skill membership.
- **Legacy projection retirement:** remove `skills/refreshing-installed-skills/`; update `tools/run.py`, `tests/repository/test_run_cli.py`, `skills/using-git-worktrees/scripts/new_worktree.py`, and `skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py`. Keep generic submodule initialization/handling and the standalone vendor-profile deployment contract.
- **Consumer handoff evidence:** update the active spec/plan with verified Game Studio and Architecture Pack source coordinates and the bounded Wild Bunch handoff. Do not edit Wild Bunch.

______________________________________________________________________

### Task 1: Prove Codex repo-scoped moving-ref refresh

**Files:**

- Modify: `.agents/plans/2026-09-29-multi-harness-plugin-distribution.md` - record the tested Codex version, repo marketplace declaration, exact refresh operation, result, and whether the proof passed.
- Scratch only: a disposable source Git repository, a disposable consumer repository, and one disposable linked worktree. Do not add the fixtures to Marketplace source.

**Interfaces:**

- Consumes: the accepted spec's Codex `git-subdir` source with `ref: main` and project activation via `.codex/config.toml`.

- Produces: a verified native refresh sequence and a go/no-go decision. No later task may assume moving-ref support if this task fails.

- [x] **Step 1: Create a disposable Git plugin source.** Created `main` with a root `plugin.json` and a `proof-marker` skill containing `proof-v1`, then served it from a bare Git remote over local HTTPS.

- [x] **Step 2: Declare the source in a disposable consumer.** Added `.agents/plugins/marketplace.json` with a `git-subdir` source at `ref: main` and enabled it in `.codex/config.toml`. Codex CLI 0.158.0-alpha.2.1 reported the plugin `enabled: true` in the trusted consumer. The plugin was installed into Codex's profile cache from the Git source. `codex debug prompt-input` does not expose the plugin skill, so direct prompt invocation was not used as evidence.

- [x] **Step 3: Prove isolation.** With the profile-level plugin disabled, `codex plugin list --json` reported `enabled: true` in both the consumer and its linked worktree, and `enabled: false` in an unrelated trusted repo with no plugin setting. The linked worktree carried the consumer's `.codex/config.toml` and produced the same enabled state.

- [x] **Step 4: Move the published ref and refresh.** Changed the marker to `proof-v2` and advanced only the plugin source's `main`. Ran `codex plugin marketplace upgrade proof-marketplace --json`; Codex refreshed the managed marketplace snapshot and the installed plugin cache. The cached skill contains only `proof-v2`. No desktop UI interaction was needed for the CLI proof.

- [x] **Step 5: Record and gate.** Codex CLI `0.158.0-alpha.2.1`; marketplace source `https://127.0.0.1:9419/consumer-marketplace.git#main`; plugin source `https://127.0.0.1:9419/source.git`, path `./plugins/proof-plugin`, `ref: main`; project activation `[plugins."proof-plugin@proof-marketplace"] enabled = true`; refresh command `codex plugin marketplace upgrade proof-marketplace`. The managed marketplace root appeared under `<CODEX_HOME>/.tmp/marketplaces/proof-marketplace`, and the installed plugin under `<CODEX_HOME>/plugins/cache/proof-marketplace/proof-plugin/1.0.0`. The moving ref refreshed, and enablement followed repo/worktree config while the unrelated repo remained disabled. The proof used an isolated Codex profile and a local HTTPS Git fixture; certificate verification was disabled only for that disposable local fixture. The CLI's `debug prompt-input` diagnostic did not list plugin skills, so it is not treated as a skill invocation test.

- [x] **Step 6: Commit the proof update.** Committed the plan's proof result as `4fe4ea632`; the tracked hook and `git diff --check` passed.

### Task 2: Publish portable plugin packages for Devin and preserve Codex identity

**Files:**

- Modify: `src/marketplace/build.py` and `src/marketplace/definitions.py`.
- Modify: `src/plugin-definitions/repo-worker-pack/plugin.json`, `src/plugin-definitions/repo-worker-pack/contents.json`, `src/plugin-definitions/repo-worker-pack/files/README.md`, `src/plugin-definitions/repo-worker-pack/files/SOURCE.md`, and `src/plugin-definitions/repo-worker-pack/files/package.json`.
- Modify: `tests/build/test_plugin_definition_contract.py`, `tests/build/test_plugin_assembly.py`, `tests/shipping/test_isolated_plugin.py`, `tests/shipping/test_jev_mcp_plugin_contract.py`, and `tests/shipping/test_pilot_install_closure.py` where they assert plugin package shape and marketplace identity.
- Generated by `py -3 tools/run.py marketplace --apply`: `dist/plugins/repo-worker-pack/`, `src/plugin-definitions/catalog.json`, `.agents/plugins/marketplace.json`, and `dist/plugin-roots.json` / `dist/manifest.json` when changed by the generator.

**Interfaces:**

- Consumes: Task 1's proof and current Codex package-generation contracts.

- Produces: packages with root Agent Plugins `plugin.json` and `skills/` accepted by both Codex and Devin; preserve `.codex-plugin/plugin.json` only if needed as the documented Codex compatibility fallback. Codex marketplace plugin key stays `repo-worker-pack`; displayed name is `Agent Capability Pack`.

- [x] **Step 1: Add package-shape tests.** Build and shipping tests require the portable root manifest, bundled skills, the stable Codex compatibility overlay, and no Claude-specific package directory.

- [x] **Step 2: Confirm the red state.** Ran `py -3 -m pytest tests/build tests/shipping -q`; the new package-shape assertions failed against the old `.codex-plugin`-only output as expected.

- [x] **Step 3: Implement manifest generation.** Canonical definitions now use Agent Plugins `plugin.json` with Codex presentation under `extensions.com.openai`. The build emits the portable root manifest and derives the legacy Codex overlay from it, avoiding a second authored manifest. Codex-only fields remain namespaced in the portable file.

- [x] **Step 4: Update ACP display metadata.** Changed the visible display name and descriptions to Agent Capability Pack while preserving machine name `repo-worker-pack`, catalog identity, and plugin path.

- [x] **Step 5: Regenerate and verify.** Ran `py -3 tools/run.py marketplace --apply` and `py -3 -m pytest tests/build tests/shipping -q` (15 passed). Inspected the skill-only Architecture Pack and the Jev MCP package with portable root manifests; Jev's MCP server uses root `mcp.json`.

- [ ] **Step 6: Commit the package slice.** Stage source and generated output together; let the tracked hook run.

### Task 3: Define the AOM repo-plugin-subscription standard artifact

**Files:**

- Create: `skills/repo-shape/references/repo-plugin-subscriptions-standard.md`.
- Create: `skills/repo-shape/templates/repo-plugin-subscriptions/codex-marketplace.json`, `codex-config.toml`, and `devin-config.json`.
- Modify: `skills/repo-shape/scripts/deploy_operating_standards.py` and `skills/repo-shape/tests/scripts/test_operating_standards_deployment.py` to resolve standard resources from the installed AOM plugin package without a consumer Marketplace source submodule.
- Modify: `skills/repo-shape/references/operating-standards-catalog.json`, `operating-standards-catalog.schema.json`, `repository-shape-manifest.json`, `repository-shape-standard.md`, and `templates/operating-standards.json`.
- Modify: `skills/repo-agent-assets/SKILL.md` and `src/plugin-definitions/agent-operating-model/contents.json` to route subscription adoption to this opt-in standard.
- Test: new `skills/repo-shape/tests/scripts/test_repo_plugin_subscriptions.py` and existing catalog/deployment suites.

**Interfaces:**

- Consumes: Task 1's Codex source and refresh sequence; Task 2's package paths.

- Produces: optional standard ID `repo-plugin-subscriptions` in the AOM standards catalog. Opt-in is declared only through the existing `.agents/contracts/operating-standards.json` composition. There is no additional neutral plugin manifest. Applying the scaffold creates missing native Codex marketplace/project config and Devin `.devin/config.json` examples; consumers own those files and any local implementation after adoption. The native Codex marketplace entry and Devin `requiredPlugins` entry are the sole source of plugin identity, path, ref, and SHA.

- [ ] **Step 1: Define native-config examples and validation cases.** Add the three declared templates and cases for Codex Git-subdirectory `ref: main`, Codex fixed `sha`, Devin `requiredPlugins` Git-subdirectory `ref`, Devin fixed `sha`, and malformed source/path/selector pairs. Require that no example writes plugin skill payloads under `.agents/skills/`.

- [ ] **Step 2: Add standard conformance tests.** Test that the standard accepts the native examples, rejects missing paths, mutually present `ref` and `sha`, invalid source URLs, duplicate plugin identities, malformed TOML/JSON, and Codex enablement keys that reference no marketplace entry. Test that the empty scaffold is valid and leaves consumer-authored skills untouched. Preserve the existing `repo.local_skills` declaration and validate each declared directory's `SKILL.md` frontmatter without copying or deleting its files. Extend `test_operating_standards_deployment.py` to verify resources can be scaffolded from the installed AOM plugin root.

- [ ] **Step 3: Implement the scaffold and validator.** Add a read-only `--check` that validates native Codex and Devin declarations against the standard and an `--apply` that creates only missing native config files from templates without overwriting repo-authored config. Resolve plugin paths within their declared repository, preserve unrelated config fields, and report exact failing file/entry. Do not fetch Git sources or alter refs during validation.

- [ ] **Step 4: Register and deploy the standard.** Add the catalog entry and resource declarations so AOM can scaffold local standard resources into the consumer repo, where they are tracked and owned by that repo. Add the standard to repo-shape dispatch only when the consumer explicitly opts in. Resolve resources from the installed AOM plugin root when available; the Marketplace source checkout is only a development fallback and is not a consumer prerequisite.

- [ ] **Step 5: Verify standard behavior.** Run `py -3 -m pytest skills/repo-shape/tests/scripts/test_repo_plugin_subscriptions.py skills/repo-shape/tests/scripts/test_operating_standards_catalog.py skills/repo-shape/tests/scripts/test_operating_standards_deployment.py skills/repo-shape/tests/scripts/test_repo_standards.py -q` and confirm only explicitly adopted fixtures invoke the new validator.

- [ ] **Step 6: Commit the AOM standard slice.** Stage source and tests; let the tracked hook run.

### Task 4: Add the ambient ACP `refreshing-installed-plugins` capability

**Files:**

- Create: `skills/refreshing-installed-plugins/SKILL.md` and `skills/refreshing-installed-plugins/tests/` cases for Codex, Devin, SHA pins, missing subscriptions, and refresh failure.
- Modify: `src/plugin-definitions/repo-worker-pack/contents.json` to remove `refreshing-installed-skills` and include `refreshing-installed-plugins`.
- Modify: package docs from Task 2 only where needed to explain the capability bundle.
- Generated by marketplace regeneration: `dist/plugins/repo-worker-pack/skills/refreshing-installed-plugins/` and bundle manifests.

**Interfaces:**

- Consumes: Task 1's tested Codex refresh procedure; Task 3's standard and native declaration examples.

- Produces: one portable ambient skill that checks the current repository's native configs and uses Codex's proven repo marketplace refresh or Devin's supported local `devin plugins update` behavior. It never manages user-level installs, fetches plugin files itself, changes a branch/SHA, or projects skills.

- [ ] **Step 1: Add instruction-review cases and a failing baseline.** Create the new skill folder with a short baseline instruction that explicitly says the capability is not yet available. Add `skills/refreshing-installed-plugins/tests/pressure/campaign.json` and prompts `prompts/codex-moving-ref.md`, `prompts/devin-repo-ref.md`, `prompts/repo-isolation.md`, `prompts/sha-pin.md`, `prompts/refresh-failure.md`, and `prompts/running-session.md`. Expected outcomes must name observable instructions, not scores.

- [ ] **Step 2: Commit the baseline.** Commit only the new skill test inputs and baseline skill so the pressure runner's immutable `HEAD` contains its inputs.

- [ ] **Step 3: Run the red pressure campaign.** Run `py -3 tools/run_workflow_pressure_campaign.py --campaign skills/refreshing-installed-plugins/tests/pressure/campaign.json --output-root skills/refreshing-installed-plugins/tests/pressure/runs --head HEAD --family sol --apply`. Keep outputs under ignored `runs/`; verify the baseline misses the expected host routing, refresh, and scope outcomes.

- [ ] **Step 4: Write the skill instructions.** Include current-repo discovery, the Codex refresh operation established in Task 1, provisional Devin refresh guidance grounded in its official CLI docs, verification of loaded content, and safe failure behavior. Task 5 verifies and finalizes Devin-specific instructions before the skill is considered complete. Do not add a universal downloader or helper script.

- [ ] **Step 5: Add ACP composition.** Replace old composition metadata for `refreshing-installed-skills` with the new capability and update its provenance note.

- [ ] **Step 6: Regenerate and run the green pressure campaign.** Run `py -3 tools/run.py marketplace --apply`, then rerun the command from Step 3 against the new `HEAD`; verify all expected outcomes and inspect the generated skill package.

- [ ] **Step 7: Commit the ACP capability slice.** Stage source and generated package together; let the tracked hook run.

### Task 5: Prove Devin repo scope and native update behavior

**Files:**

- Modify: `.agents/plans/2026-09-29-multi-harness-plugin-distribution.md` with Devin CLI/Desktop version and proof outcome.
- Scratch only: disposable plugin and consumer repositories; do not change `%APPDATA%\Devin` or install a user-level plugin.

**Interfaces:**

- Consumes: Tasks 2-4 and the Devin `requiredPlugins` contract.

- Produces: verified repo-scope and update steps for the ACP skill and the AOM standard.

- [ ] **Step 1: Declare a Git subdirectory plugin in a disposable `.devin/config.json`.** Point `requiredPlugins` at the test source and `ref: main`; verify Devin CLI and Devin Desktop expose it only while operating in that consumer repo and its worktree.

- [ ] **Step 2: Advance the disposable ref and refresh.** Change the skill marker, move `main`, run the documented local Devin refresh operation, start a new session, and verify the new marker. Then open a separate repo without a `requiredPlugins` declaration and verify the plugin is unavailable there; confirm its user-level manifest is unchanged.

- [ ] **Step 3: Record evidence.** Record exact config and operations in this plan. If repo-scope behavior diverges between Devin Desktop and CLI, update Task 4's instructions to describe each actual supported surface and update the standard's validation accordingly.

- [ ] **Step 4: Finalize ACP refresh guidance.** Update `skills/refreshing-installed-plugins/SKILL.md` with the verified Devin operation and scope.

- [ ] **Step 5: Commit the Devin proof and skill update.** Commit the evidence in this plan and the corrected skill so the next pressure run uses the exact reviewed `HEAD`; let the tracked hook run.

- [ ] **Step 6: Rerun the pressure campaign.** Run `py -3 tools/run_workflow_pressure_campaign.py --campaign skills/refreshing-installed-plugins/tests/pressure/campaign.json --output-root skills/refreshing-installed-plugins/tests/pressure/runs --head HEAD --family sol --apply` and verify both Codex and Devin expected outcomes.

- [ ] **Step 7: Close the Devin proof.** If the pressure campaign exposes a missed instruction, commit a focused correction and rerun against that new `HEAD`; repeat only for a failing scenario. Stop when all scenarios pass, then commit the final proof update in this plan.

### Task 6: Retire the old skill-projection updater without losing independent behavior

**Files:**

- Delete: `skills/refreshing-installed-skills/` after all owned residual responsibilities have been mapped.
- Modify: `tools/run.py` to remove the `installed-skills` and `refresh-skills` projection commands, or retain a renamed local-skill validation command only if its behavior is defined and covered by AOM Task 3.
- Modify: `tests/repository/test_run_cli.py` to assert removed commands are no longer advertised and current CI target resolution remains intact.
- Modify: `skills/using-git-worktrees/scripts/new_worktree.py` to stop finding/running the old refresh script after worktree creation; retain generic `.gitmodules` initialization and submodule behavior.
- Modify: `skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py` to prove worktree creation preserves repo-local files and no longer projects Marketplace skills.
- Modify: `skills/using-git-worktrees/SKILL.md` and `skills/using-git-worktrees/references/` text that promises automatic skill projection after worktree creation.
- Inspect, preserve, or reroute: `skills/repo-shape/scripts/deploy_vendor_profiles.py`, `skills/repo-shape/references/vendor-profile-deployment.md`, and their tests; they remain owned by repo-shape unless the source audit proves they have no separate supported use.

**Interfaces:**

- Consumes: Tasks 3-5's repo-local native config contract and ambient refresh capability.

- Produces: no Marketplace plugin skill projections in consumer `.agents/skills/`; existing `repo.local_skills` declaration and frontmatter validation move to the AOM repo-agent-assets validator without copying or deleting local files; vendor-profile deployment remains a separate repo-shape capability; creating a worktree does not mutate the plugin cache or install skills.

- [ ] **Step 1: Audit residual behavior and callers.** Search only `skills/refreshing-installed-skills/`, `tools/run.py`, `skills/using-git-worktrees/`, `skills/repo-shape/scripts/deploy_vendor_profiles.py`, and their named tests for local-skill validation, projection provenance, profile deployment, and submodule rolling. Record each surviving owner in this plan before deleting code.

- [ ] **Step 2: Add worktree regression cases.** Update worktree tests to cover repos with and without native plugin declarations and with declared local skills; assert the worktree creator doesn't copy or remove `.agents/skills/` content. Keep the generic submodule tests.

- [ ] **Step 3: Remove updater call paths.** Delete old updater invocations from worktree creation and `tools/run.py`. Remove any CLI target that has no post-migration owner; keep generic CI commands and Marketplace generation independent of plugin refresh.

- [ ] **Step 4: Remove projection implementation.** Delete the old skill, plugin projection/provenance implementation, shell/PowerShell wrappers, and their tests. Keep `repo.local_skills` declaration and `SKILL.md` frontmatter validation in the Task 3 AOM validator without projection; keep vendor-profile deployment only in repo-shape and remove only the now-unused invocation/provenance adapter.

- [ ] **Step 5: Verify no legacy production references remain.** Run `rg -n "refreshing-installed-skills|refresh_installed_skills|installed-skills|refresh-skills" skills tools tests src .agents --glob '!dist/**'`; each remaining result must be a deliberate migration note or historical test assertion, not a live caller. Run focused `py -3 -m pytest tests/repository/test_run_cli.py skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py -q` and relevant `skills/repo-shape/tests/scripts/test_operating_standards_deployment.py` tests.

- [ ] **Step 6: Regenerate and commit the retirement slice.** Run `py -3 tools/run.py marketplace --apply`; confirm generated packages no longer ship the old skill and retain the new one. Stage source/generated outputs together and let the tracked hook run.

### Task 7: Prepare the bounded Wild Bunch migration handoff

**Files:**

- Modify: `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md` with verified Game Studio and Architecture Pack repository URLs, subdirectory paths, and published refs.
- Modify: this plan with handoff scope, migration acceptance evidence, and the open Marketplace-submodule responsibility check.
- Do not modify: `Z:/wild-bunch` or any Wild Bunch worktree.

**Interfaces:**

- Consumes: Tasks 1-6's verified harness behavior, package location, standard adoption, and ACP refresh instructions.

- Produces: a self-contained task brief for an agent operating in Wild Bunch.

- [ ] **Step 1: Verify source coordinates.** Inspect `Z:/wild-bunch`'s current plugin catalog and Game Studio repository remotes; verify plugin subdirectory and published branch directly from the source repository. Resolve Architecture Pack to this Marketplace's published Git path and branch. Confirm Devin accepts the same source forms.

- [ ] **Step 2: Write migration acceptance checks.** Require Codex and Devin declarations for only Game Studio and Architecture Pack, no checked-in plugin payloads or plugin-skill projections, repo/worktree-only availability, native refresh to changed branch content, preservation of authored local skills, and an explicit decision about any remaining Marketplace submodule responsibilities.

- [ ] **Step 3: Update the spec and plan with verified coordinates.** Include repository URLs, subdirectory paths, branch names, and the responsible Wild Bunch agent boundary; do not copy plugin content into this repository.

- [ ] **Step 4: Commit the handoff materials.** Stage only the spec and plan updates; let the tracked hook run.

### Task 8: Final integration proof and planning-artifact publication

**Files:**

- Verify: `src/plugin-definitions/`, `src/marketplace/`, `skills/repo-shape/`, `skills/repo-agent-assets/`, `skills/refreshing-installed-plugins/`, `skills/using-git-worktrees/`, `tools/run.py`, `tests/build/`, `tests/repository/`, and `tests/shipping/`.
- Generated: all Marketplace outputs owned by `py -3 tools/run.py marketplace --apply`.
- Planning artifacts: `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md` and `.agents/plans/2026-09-29-multi-harness-plugin-distribution.md`.

**Interfaces:**

- Consumes: all prior tasks.

- Produces: implementation acceptance evidence, updated planning artifact statuses, and a reviewed handoff to the Wild Bunch owner. This final implementation task completes only when all acceptance criteria in the spec have evidence.

- [ ] **Step 1: Run focused behavior checks.** Run changed skill tests and the native Codex/Devin proof procedures recorded in Tasks 1 and 5.

- [ ] **Step 2: Regenerate then check generated Marketplace output.** Run `py -3 tools/run.py marketplace --apply` followed by `py -3 tools/run.py marketplace --check`. Do not run the full CI check immediately before a normal commit; let the tracked hook prove the staged tree.

- [ ] **Step 3: Review spec coverage.** Check every spec acceptance criterion against a named test, native proof, or generated-artifact inspection. Correct gaps before publication.

- [ ] **Step 4: Complete artifact closeout.** Promote any durable decision to `docs/decisions/` only if the implementation established a durable architecture decision; mark the spec and plan `completed-awaiting-retirement` for the implementation PR and retain both there.

- [ ] **Step 5: Commit, push, and open the implementation Draft PR.** Let the tracked hook verify the staged snapshot, push the task branch, open the Draft PR, and verify the PR head SHA contains the generated packages and both completed artifacts.

## Planning-PR Boundary

This plan and its spec are being published in a planning-only Draft PR before implementation. Keep this plan `active` and its implementation task checkboxes unchecked in that PR. The plan becomes `completed-awaiting-retirement` only in the later implementation PR after Task 8; retire both planning artifacts in the first commit of the next substantive slice under `.agents/doctrine/completed-artifacts.md`.

## Out of Scope

- Changing or migrating the Wild Bunch repository.
- Automating user-level ambient plugin installation or refresh through AOM.
- Building a Marketplace downloader, cache, background updater, or SHA-bump bot.
- Copying installed plugin payloads into consumer repos or projecting plugin skills into `.agents/skills/`.
- Removing generic Git submodule support or unrelated Marketplace submodules.
- Changing skill behavior or plugin membership, except replacing the old projection skill with the agreed plugin-refresh capability.
- Generating Claude Code-only packages or marketplaces.
