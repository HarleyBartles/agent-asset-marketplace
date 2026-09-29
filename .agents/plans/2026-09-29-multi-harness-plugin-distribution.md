# Multi-Harness Plugin Distribution Implementation Plan

> **Artifact status:** completed-awaiting-retirement. Codex refresh proof, portable package shape, AOM subscription standard, and the Wild Bunch Codex handoff are complete. Retain this plan through the implementation Draft PR, then retire it in the first commit of the next substantive slice.
>
> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let Codex consumers declare repo-scoped Git plugin dependencies through an AOM standard, and retire the old plugin-skill projection workflow. Devin-ready package shape remains, while Devin consumer proof is follow-up work.

**Architecture:** Keep plugin source and composition in this Marketplace and publish complete packages from `main`. Codex consumers keep native declarations that point at Git subdirectories and moving published branches by default; Codex fetches and caches plugin payloads, never projecting them into consumer `.agents/skills/`. AOM ships the deployable subscription-standard scaffold and conformance validator. Native Codex Marketplace upgrade refreshes installed plugin payloads, so no ACP refresh skill is needed for this flow. Remove the former projection updater only after its other callers and responsibilities have explicit owners.

**Tech Stack:** Python 3, JSON and Markdown source, the existing Marketplace generator and CI, Codex repo marketplaces, Devin repo plugin manifests, Git branches and worktrees.

**Spec:** `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md`

**Execution Strategy:** `executing-plans` - the work is sequential and contract-coupled: native behavior gates the subscription contract; AOM scaffolding and validation define the declaration shape ACP consumes; the old updater and worktree callers can be retired only after those replacement surfaces exist. One executor preserves that shared context; subagent handoffs would add reconstruction without useful parallelism. A fresh whole-branch review follows implementation.

## Global Constraints

- Ambient installation and refresh remain harness and operator responsibilities; AOM does not manage ambient plugins.
- Codex's current Marketplace remains valid and its existing plugin catalog identity remains updateable through the native Marketplace flow.
- A consumer repo records its own native declarations; it does not check in Marketplace plugin payloads or project their skills into `.agents/skills/`.
- Marketplace subscriptions default to the published `main` branch; a fixed commit SHA is an explicit consumer choice.
- AOM artifacts scaffold an opt-in standard and validate conformance; a consumer owns the adopted implementation and its native config.
- Codex Marketplace upgrade is the refresh operation; Devin repo-scoped refresh proof is deferred and does not block Codex shipping.
- Public product display name becomes Agent Capability Pack. Retain the existing machine catalog key `repo-worker-pack` during this change to preserve existing Codex installs; do not add a duplicate catalog entry.
- Wild Bunch migration is a handoff to a responsible agent in Wild Bunch. This plan does not edit that repository.
- Claude Code-only packages and metadata are out of scope.
- Do not remove repo-authored `.agents/skills/`, generic submodule support, or `repo-shape` vendor-profile deployment as collateral to removing plugin projections.

## Review Focus

- Codex project configuration must refresh a moved Git `ref` and scope skill availability to the declaring repo and its worktrees (Task 1).
- Devin's repo-scoped plugin behavior is a follow-up proof, not a Codex release gate.
- Retiring plugin projections must preserve declared repo-authored skills and independent vendor-profile deployment (Task 6).
- Renaming the ambient pack's display name must not orphan existing Codex installs (Task 2).
- Missing or invalid native declarations must fail AOM validation with an actionable path and finding, without downloading plugin payloads (Task 3).

## File Structure

The implementation edits canonical source, then regenerates shipped Marketplace packages.

- **Codex/Devin package source:** `src/marketplace/build.py`, `src/marketplace/definitions.py`; `src/plugin-definitions/repo-worker-pack/plugin.json`, `src/plugin-definitions/repo-worker-pack/contents.json`, and `src/plugin-definitions/repo-worker-pack/files/{README.md,SOURCE.md,package.json}`; generated `dist/plugins/repo-worker-pack/` and catalog/inventory surfaces.
- **AOM standard source:** `skills/repo-shape/references/operating-standards-catalog.json`, its schema, `repository-shape-manifest.json`, standard documentation/templates, and a focused validator plus tests under `skills/repo-shape/`. Resolve resources from the upgraded Codex Marketplace snapshot without requiring a consumer Marketplace submodule.
- **AOM capability guidance:** `skills/repo-agent-assets/SKILL.md` and its declared source/composition in `src/plugin-definitions/agent-operating-model/contents.json`.
- **ACP capability source:** no plugin refresh skill is required for the Codex flow because native Marketplace upgrade refreshes the installed payload.
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

- [x] **Step 6: Commit the package slice.** Committed source and generated output as `5b4d1ef37`; the tracked hook passed.

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

- Produces: optional standard ID `repo-plugin-subscriptions` in the AOM standards catalog. Opt-in is declared only through the existing `.agents/contracts/operating-standards.json` composition. There is no additional neutral plugin manifest. Applying the scaffold creates missing native Codex marketplace/project config and a starter Devin `.devin/config.json`; consumers own those files and any local implementation after adoption. Codex's native marketplace entry is the source of plugin identity, path, ref, and SHA.

- [x] **Step 1: Define native-config examples and validation cases.** Added Codex marketplace/project config templates and a starter Devin config. Codex cases cover floating `ref`, fixed `sha`, malformed source/path/selector pairs, and no plugin projections into `.agents/skills/`.

- [x] **Step 2: Add standard conformance tests.** Tests accept floating refs, reject malformed paths/selectors/URLs, duplicate identities and unmatched Codex activation keys, and prove scaffolding preserves consumer config and local skills. Deployment tests prove Codex's upgraded Marketplace cache can supply resources without a consumer submodule. Existing local-skill checks remain intact.

- [x] **Step 3: Implement the scaffold and validator.** Added read-only Codex config validation and missing-file scaffolding that preserves existing config. Validation checks local activation references and plugin paths, and never fetches Git sources or alters refs. Devin scaffolding remains lightweight pending consumer proof.

- [x] **Step 4: Register and deploy the standard.** Registered the standard and resources. Repo-shape dispatch runs the validator only when the consumer opts into the operating-standard composition. Deployment resolves resources from the upgraded Codex Marketplace snapshot; a consumer source submodule is not required.

- [x] **Step 5: Verify standard behavior.** Ran the focused command above: 64 passed. Explicit operating-standard composition gates the new validator.

- [x] **Step 6: Include the AOM standard in the integration commit.** The final commit will include source, tests, generated plugin package, spec, and plan; the tracked hook validates the staged snapshot.

### Task 4: Use the native Codex Marketplace upgrade for refresh

Codex's Marketplace Upgrade action (or `codex plugin marketplace upgrade <name>`) refreshes the Marketplace snapshot and installed plugin payload. Task 1 proved a moved `main` ref loads new content without changing the consumer declaration. No ACP refresh skill or helper is required for this Codex flow. Devin repo-scoped refresh remains a separate, deferred proof and does not block Codex shipping.

- [x] Confirm an additional refresh capability is unnecessary for Codex.
- [x] Keep ambient updater scope out of this implementation. AOM does not manage ambient installs; Codex owns Marketplace refresh.
- [x] Defer Devin refresh proof. Do not invoke a user-level Devin update command as part of this Codex release.

### Task 5: Devin consumer integration (follow-up)

Devin-compatible portable plugin packages and starter config are included. Repo-scoped Devin install and refresh behavior is not required for this Codex field-test release. Revisit the Devin proof when a Devin consumer is ready; do not add an ACP refresh capability unless that proof demonstrates a gap in Devin's native operation.

### Task 6: Retire the old skill-projection updater without losing independent behavior

**Files:**

- Delete: `skills/refreshing-installed-skills/` after all owned residual responsibilities have been mapped.
- Modify: `tools/run.py` and this repository's operating-standards composition to remove the `installed-skills` and `refresh-skills` projection commands and adoption.
- Modify: `tests/repository/test_run_cli.py` to assert removed commands are no longer advertised and current CI target resolution remains intact.
- Modify: `skills/using-git-worktrees/scripts/new_worktree.py` to stop finding/running the old refresh script after worktree creation; retain generic `.gitmodules` initialization and submodule behavior.
- Modify: `skills/using-git-worktrees/tests/scripts/test_worktree_scripts.py` to prove worktree creation preserves repo-local files and no longer projects Marketplace skills.
- Modify: `skills/using-git-worktrees/SKILL.md` and `skills/using-git-worktrees/references/` text that promises automatic skill projection after worktree creation.
- Inspect, preserve, or reroute: `skills/repo-shape/scripts/deploy_vendor_profiles.py`, `skills/repo-shape/references/vendor-profile-deployment.md`, and their tests; they remain owned by repo-shape unless the source audit proves they have no separate supported use.

**Interfaces:**

- Consumes: Task 3's repo-local native config contract and Task 1's native Codex refresh proof.

- Produces: no Marketplace plugin skill projections in consumer `.agents/skills/`; existing `repo.local_skills` declaration and frontmatter validation remain consumer-owned without copying or deleting local files; vendor-profile deployment remains a separate repo-shape capability; creating a worktree does not mutate the plugin cache or install skills.

- [x] **Step 1: Audit residual behavior and callers.** Repo-shape's `skill_link_contract.py` retains `repo.local_skills` name/frontmatter validation. `deploy_vendor_profiles.py` remains the vendor-profile owner and runs through Marketplace generation. Worktree creation retains generic `git submodule update --init --recursive` at the consumer-pinned commit but no longer fetches or resets submodules to `origin/main`. The projection updater and Marketplace `refresh-skills` runner targets have no remaining consumer owner.

- [x] **Step 2: Add worktree behavior cases.** Tests prove repo-native Codex config and authored local skills survive worktree creation without plugin projections, and generic pinned submodules initialize without rolling.

- [x] **Step 3: Remove updater call paths.** Removed the worktree projection call and submodule rolling, removed the `installed-skills` and `refresh-skills` runner targets, and removed the Marketplace repo's `installed-skill-projections` standard selection.

- [x] **Step 4: Remove projection implementation.** Deleted the old skill, projection/provenance implementation, wrappers, and tests. Existing `repo.local_skills` frontmatter checks stay in `skill_link_contract.py`; vendor-profile deployment remains in repo-shape and Marketplace generation.

- [x] **Step 5: Verify no legacy production callers remain.** `rg` found only the deliberate migration note, historical CLI rejection assertions, and general documentation about what projections do not establish; there are no updater imports or runtime callers. Focused runner/worktree tests pass (31 and 36); the combined AOM repo-shape suite passes (65).

- [x] **Step 6: Regenerate and verify the retirement slice.** `py -3 tools/run.py marketplace --apply` regenerated the AOM and RWP packages without the old skill; `py -3 tools/run.py marketplace --check` passed. Include generated output with source in the integration commit.

### Task 7: Prepare the bounded Wild Bunch migration handoff

**Files:**

- Modify: `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md` with verified Game Studio and Architecture Pack repository URLs, subdirectory paths, and published refs.
- Modify: this plan with handoff scope, migration acceptance evidence, and the open Marketplace-submodule responsibility check.
- Do not modify: `Z:/wild-bunch` or any Wild Bunch worktree.

**Interfaces:**

- Consumes: Tasks 1-6's verified harness behavior, package location, standard adoption, and ACP refresh instructions.

- Produces: a self-contained task brief for an agent operating in Wild Bunch.

- [x] **Step 1: Verify source coordinates.** Wild Bunch's local Game Studio manifest identifies `https://github.com/openai/plugins`; the official plugin path is `plugins/game-studio`, and its published branch is `main`. Architecture Pack is at `https://github.com/HarleyBartles/agent-asset-marketplace`, path `dist/plugins/architecture-pack`, branch `main`. Devin source-form proof is deferred.

- [x] **Step 2: Write migration acceptance checks.** Require Codex declarations for Game Studio and Architecture Pack and preserve other deliberately selected repo plugins. Require no checked-in plugin payloads or plugin-skill projections, repo/worktree-only availability, Marketplace Upgrade refresh to changed branch content, preservation of authored local skills, and an explicit decision about any remaining Marketplace submodule responsibilities.

- [x] **Step 3: Update the spec and plan with verified coordinates.** Recorded repository URLs, subdirectory paths, branches, and the responsible Wild Bunch agent boundary; no plugin content was copied into this repository.

- [x] **Step 4: Include handoff materials in the integration commit.** The spec and plan will ship with implementation and generated packages in the same Draft PR.

### Task 8: Final integration proof and planning-artifact publication

**Files:**

- Verify: `src/plugin-definitions/`, `src/marketplace/`, `skills/repo-shape/`, `skills/repo-agent-assets/`, `skills/using-git-worktrees/`, `tools/run.py`, `tests/build/`, `tests/repository/`, and `tests/shipping/`.
- Generated: all Marketplace outputs owned by `py -3 tools/run.py marketplace --apply`.
- Planning artifacts: `.agents/specs/2026-09-29-multi-harness-plugin-distribution-design.md` and `.agents/plans/2026-09-29-multi-harness-plugin-distribution.md`.

**Interfaces:**

- Consumes: all prior tasks.

- Produces: implementation acceptance evidence, updated planning artifact statuses, and a reviewed handoff to the Wild Bunch owner. This final implementation task completes only when all acceptance criteria in the spec have evidence.

- [x] **Step 1: Run focused behavior checks.** Changed AOM, runner, worktree, build, and shipping suites pass; the Codex native refresh evidence is recorded in Task 1. Devin consumer proof is deferred.

- [x] **Step 2: Regenerate then check generated Marketplace output.** Ran `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py marketplace --check`; both passed. The tracked hook will prove the staged tree at commit.

- [x] **Step 3: Review spec coverage.** Codex moving-ref behavior is proven in Task 1; package shape in Task 2; scaffold, validation, and no-projection behavior in Task 3/6 tests; generation and freshness in Task 8, Step 2; Wild Bunch coordinates and migration acceptance checks in Task 7. Devin consumer proof is explicitly follow-up.

- [x] **Step 4: Complete artifact closeout.** No separate decision record is required for this delivery. Mark the spec and plan `completed-awaiting-retirement` for the implementation PR and retain both there.

- [x] **Step 5: Commit, push, and update the implementation Draft PR.** Published implementation commit `3d1f1a8c0` to open Draft PR #343. GitHub confirmed the PR head matched the pushed branch. The tracked staged apply/check gate passed; the completed spec and plan remain in the PR. A final documentation closeout records this publication.

## Planning-PR Boundary

The spec and plan ship with the implementation in this Draft PR so a Wild Bunch agent can field-test the Codex consumer path. They are marked `completed-awaiting-retirement`; retire both planning artifacts in the first commit of the next substantive slice under `.agents/doctrine/completed-artifacts.md`.

## Out of Scope

- Changing or migrating the Wild Bunch repository.
- Automating user-level ambient plugin installation or refresh through AOM.
- Building a Marketplace downloader, cache, background updater, or SHA-bump bot.
- Copying installed plugin payloads into consumer repos or projecting plugin skills into `.agents/skills/`.
- Removing generic Git submodule support or unrelated Marketplace submodules.
- Changing skill behavior or plugin membership.
- Generating Claude Code-only packages or marketplaces.
