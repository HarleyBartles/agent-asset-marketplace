# Repo-Scoped Plugin Distribution Design

> **Status:** completed-awaiting-retirement. Codex is the first consumer target: preserve the working Marketplace, let consumer repos declare native repo-scoped Git plugin sources, and rely on the Codex Marketplace Upgrade action to refresh the marketplace snapshot and plugin payload. AOM provides the opt-in subscription standard and validation; it does not manage ambient installs. Devin-compatible portable packages remain in scope, while Devin repo installation and refresh proof is follow-up work. Consumer repos do not vendor plugin files or project plugin skills into `.agents/skills/`. The Wild Bunch migration is handed to an agent working in Wild Bunch. Claude Code packaging is out of scope.

## Problem

This repository is a Codex marketplace with generated, self-contained plugin packages under `dist/plugins/`. Consumers currently have a mixture of whole-repository submodule subscriptions, repo-local plugin bundles, and generated skill projections. That mixes distribution with activation and creates update machinery for files the harnesses can already fetch from Git.

The intended boundary is a repo-owned subscription to a plugin source and version. Codex and Devin each have repo-level plugin configuration that can point to Git-backed plugin sources. The harness fetches and caches plugin files, but the repo's declaration controls where the plugin is enabled. A plugin used by Wild Bunch should therefore not become ambient in Codex or Devin when working in Portfolio or Rooms.

## Goals

- Keep canonical skill source, shared resources, product composition, and generated plugin packages owned by this Marketplace.
- Keep Marketplace plugin packages compatible with the existing Codex marketplace and Devin's native plugin format. Ambient installation and refresh are owned by each harness, not by AOM.
- Let consumer repos declare selected plugin sources and moving branch refs in their own repo configuration, without a whole-Marketplace submodule or checked-in copy of the plugin.
- Keep repo-only plugins available in that repo and its worktrees, without making them ambient in other repos.
- Keep `.agents/skills/` for skills authored by the consumer repo. Plugin skills stay in their plugin package and are loaded as part of the installed plugin.
- Provide an AOM deployable artifact for the repo plugin subscription standard. A consuming repo opts in by adopting the artifact to scaffold the standard, then owns its local implementation; AOM provides validation against the standard.
- Use the native Codex Marketplace Upgrade action to refresh the marketplace snapshot and installed plugin payload. Do not duplicate this operation in an ACP skill. Revisit whether Devin needs a reusable ambient refresh capability after a Devin consumer proof.
- Treat plugin changes merged to Marketplace `main` as published. Repo consumers track the publication branch by default and refresh through the native harness; SHA pins are available when a consumer requires controlled adoption.
- Use one portable Agent Plugins root `plugin.json` and `skills/` package for Codex and Devin when possible. Add harness-specific metadata only for capabilities that need it. Do not produce Claude Code-only packages.

## Existing constraints and source facts

- `skills/` and `shared/` are canonical source; `src/plugin-definitions/` owns Marketplace product composition; `dist/plugins/` is generated distribution output.
- Plugins carry skills; plugins do not own canonical skill source. A skill may appear in more than one plugin package.
- Codex reads repo marketplaces from `.agents/plugins/marketplace.json`. A marketplace entry can point to a Git subdirectory and select a `ref` or `sha`. `.codex/config.toml` controls whether that repo-marketplace plugin is enabled for the project. The harness may keep fetched files in its plugin cache; project configuration still defines activation scope.
- Devin reads repo-level `requiredPlugins`, `optionalPlugins`, and `forbiddenPlugins` from `.devin/config.json`, walking up from the working directory. Plugin dependencies support GitHub, Git URL, and Git-subdirectory sources with `ref` or `sha`. A `ref` tracks a branch or tag and is re-resolved on refresh; a `sha` is fixed. The installed plugin contributes skills under the plugin namespace. Devin user-level installs can be made from Git sources, are recorded in the personal manifest in Devin Cloud, are available across projects, and are updated with `devin plugins update`; official docs say plugins work in Devin Desktop as well as CLI and cloud sessions.
- Devin also has project-scoped skill directories (`.agents/skills/` and `.devin/skills/`), but this design does not copy plugin skills into them.
- Devin's `devin plugins install --local` is a machine-scoped link to a local folder. Do not use it for repo-isolated subscriptions or ambient source installs.
- `repo-agent-assets` owns consumer plugin/skill declarations and provenance in the AOM product. The proposed repo plugin subscription standard replaces its marketplace-plugin-to-`.agents/skills/` projection workflow; authored repo-local skills remain distinct.
- The former `refreshing-installed-skills` capability projected plugin skills into `.agents/skills/`, tracked projection provenance, delegated vendor-profile installation, validated repo-local skills, and could roll `marketplace-source`. Worktree creation also called it. The projection utility and skill are retired; repo-shape owns vendor-profile deployment, while `skill_link_contract.py` retains local-skill validation. Worktree creation keeps generic pinned-submodule initialization and no longer advances submodules or projects plugin skills.

## Proposed model

Separate plugin **publication**, **subscription**, and **activation**:

1. **Publication:** This repository builds complete plugin packages. A merge to `main` publishes the package at its Git path. An external plugin such as Game Studio can be referenced from its own upstream Git repository.
2. **Subscription:** A consumer repo records the source repository, plugin subdirectory, and a moving branch ref in its harness configuration. By default the ref tracks the source repository's publication branch, `main`. The repo does not contain the downloaded plugin files. This is the repository's dependency declaration and is reviewed like other config changes.
3. **Activation and refresh:** Each harness resolves its native repo-scoped declaration when working in that repo and makes the plugin's skills invocable there. A branch move changes the available plugin content; the harness picks it up on its native refresh or next session. User-level plugin installations remain ambient and apply across projects.

Codex uses a repo marketplace entry with a Git-backed plugin source, plus the project plugin setting in `.codex/config.toml`. Devin uses a Git-backed repo plugin requirement in `.devin/config.json`. Both point to the same logical plugin source and publication branch by default; each harness resolves the commit when it refreshes the plugin. The default package profile is the portable Agent Plugins root `plugin.json` and `skills/` layout: both Codex and Devin document support for it. Devin gives its native `.devin-plugin/plugin.json` precedence when present, so add that or other harness-specific files only when the shared package cannot express a needed capability.

The supported Codex repo marketplace source shape is `git-subdir` with repository URL, plugin path, and optional `ref` or `sha`. Devin repo and user plugin sources support GitHub, Git URL, and Git-subdirectory forms with `ref` or `sha`; `ref` follows a moving branch or tag, while `sha` locks exact content. These native records provide project scope; no `.agents/skills/` projection is needed for plugin invocation.

### Ambient and repo-only examples

- Superpowers Plus and Agent Operating Model are installed at user scope in Codex and Devin when they should be available across projects.
- Wild Bunch requires `game-studio` and `architecture-pack` at repo scope. Codex and Devin should load them while an agent works in Wild Bunch, including its worktrees, without making them ambient in Portfolio or Rooms.
- Other consumer repos declare only their own plugin dependencies. Repo-authored skills remain under their normal project skill directory and are not confused with skills bundled inside a plugin.

### Ambient installation and updates (harness-owned)

Ambient plugins are installed at user scope and intentionally available across repositories. Codex ambient installs already work through this repository's Codex marketplace; preserve its validity and existing native refresh path. Devin users can install Git-backed Marketplace plugins through `devin plugins install <owner/repo>#<plugin-path>` and refresh them with `devin plugins update [plugin]`. Devin records these installs in its personal manifest, and the native plugin system supports Devin Desktop. Do not manually copy Marketplace skills into Devin's user `skills/` folder or introduce a separate Devin marketplace.

Ambient installation, selection, and refresh belong to the harness and operator. AOM does not manage ambient plugins. This section records package compatibility and operational context only.

### AOM deployable repo plugin subscription standard

The AOM artifact defines the standard for declaring and optionally SHA-pinning plugin dependencies in native consumer repo files: Codex marketplace/project configuration and Devin `.devin/config.json`. It scaffolds the repo's opt-in implementation and provides validation that the implementation and declarations conform. The consuming repo owns that implementation after adoption. New Marketplace subscriptions track `ref: main` by default; external plugins track their published branch. Plugin payloads remain in their source repos and are fetched/cached by the harness. Do not write plugin skills into `.agents/skills/`. A custom neutral subscription manifest or downloader is not part of the design.

### ACP refresh capability: deferred

Codex's native Marketplace Upgrade action refreshes the Marketplace snapshot and installed plugin payload. Task 1 proved that a moved `main` ref loads new content without changing the consumer declaration, so an ACP refresh skill is redundant for the Codex path. Revisit an ACP capability only if Devin proof shows a reusable operation that its native harness does not already provide.

The former `refreshing-installed-skills` script also served worktree creation and contained local-skill validation, projection provenance, and vendor-profile deployment responsibilities. The implementation removes its callers and assigns local-skill validation to `skill_link_contract.py` and vendor-profile deployment to repo-shape. Worktree creation retains generic submodule initialization but removes Marketplace rolling and plugin-skill projection.

### Pin and publication policy

Every plugin update merged to Marketplace `main` is published. Consumer declarations track `ref: main` by default, so their config does not need a SHA change when Marketplace content advances. The harness resolves the branch during its native refresh/session fetch; a running session keeps the content it loaded at start. A consumer can instead pin a SHA when it needs reproducibility or wants to review and adopt updates deliberately. Plugin `version` remains human-facing metadata, while the commit SHA identifies the bytes.

## Acceptance criteria

- The Codex marketplace remains valid and existing user-level Codex plugin installs can still be refreshed through Codex's native marketplace flow.
- Devin-compatible portable plugin packaging is produced; Devin ambient and repo-scoped install/refresh behavior remains follow-up validation.
- A Codex consumer can declare a plugin source in its native repo configuration, with the source repository, plugin subdirectory, and moving published branch explicit. Marketplace plugins default to `main`; consumers can choose a fixed SHA.
- Plugin payloads remain outside consumer repos. A repo subscription does not require the Marketplace repository as a submodule, a checked-in plugin copy, or generated plugin-skill files in `.agents/skills/`.
- Codex repo declarations scope plugin availability to the declaring repo and its worktrees. They do not create a user-level ambient installation.
- AOM provides a deployable artifact that scaffolds repo opt-in to the subscription standard and validation against it; the consuming repo owns the adopted implementation. Codex Marketplace upgrade refreshes the installed payload. Any additional ACP capability requires evidence of a gap in the native mechanism.
- Codex refresh uses the Marketplace Upgrade action, does not change refs or SHAs, and makes updated plugin content available to subsequent agent work.
- Plugin packages use the portable Agent Plugins root manifest and layout; harness-specific metadata is added only for an evidenced incompatibility or required feature.
- The former plugin projection and Marketplace-source rolling workflow is removed from the plugin lifecycle. Any independent responsibilities formerly sharing its implementation have explicit owners and updated callers before retirement.
- The Marketplace change produces a bounded Wild Bunch handoff with verified source coordinates and repo-scoped acceptance checks. Wild Bunch files are changed only by the responsible agent working in that repo.

## Wild Bunch consumer handoff

This Marketplace work makes the plugin packages and AOM artifact for opting into the repo subscription standard available for Wild Bunch. The Marketplace implementation does not edit Wild Bunch. Its current Game Studio manifest identifies `https://github.com/openai/plugins`, and the official plugin package path is `plugins/game-studio`; use `ref: main`. Architecture Pack is published by `https://github.com/HarleyBartles/agent-asset-marketplace` at `dist/plugins/architecture-pack`; use `ref: main`. A responsible agent in Wild Bunch should adopt the artifact, own the resulting local implementation, and replace the local Game Studio plugin bundle and plugin-skill projections with Codex repo-scoped Git plugin declarations for Game Studio and Architecture Pack. The Codex Marketplace Upgrade action is the refresh path. That agent also determines whether the Marketplace source submodule has remaining non-plugin responsibilities.

The Codex repo-scoped moving-ref refresh spike is complete and establishes the native declaration and Marketplace upgrade behavior for `ref: main`. The Wild Bunch agent should field-test repo scope and refresh in Codex using the source coordinates above. Devin source-form proof is follow-up work and does not block this handoff.

## Planning gates and verification inputs

1. Start the plan with a bounded proof that Codex resolves and refreshes a repo-scoped Git-subdirectory plugin tracking `ref: main` in the target project and its worktrees. This confirms the native Marketplace Upgrade refresh operation. Treat failure as a design blocker requiring a revised native-compatible repo subscription model before implementation.
2. Validate the portable root `plugin.json` package against representative shipped plugins in Codex and Devin, and identify only the genuine harness-specific exceptions.
3. Inventory all callers and responsibilities of the former `refreshing-installed-skills`; assign local-skill validation and vendor-profile deployment to their existing owners, then retire the updater and its worktree call. Preserve generic pinned-submodule initialization.
4. Confirm Game Studio’s Git source/path/branch, then prepare the Codex-focused Wild Bunch agent handoff, including the submodule responsibility question. Devin source-form proof can follow separately.

## Out of scope

- Installing repo-only plugins into the harness's ambient/user scope.
- Copying Marketplace plugin files into consumer repos or generating plugin skill projections under `.agents/skills/`.
- Editing or migrating the Wild Bunch checkout; that consumer change is owned by its responsible in-repo agent after the Marketplace/AOM capability is ready.
- Automating ambient Codex or Devin plugin installation, selection, or refresh through AOM.
- Changing skill behavior or plugin membership.
- Claude Code packages or Claude-specific marketplace metadata.

## Research basis

- OpenAI's plugin docs describe Codex local/personal marketplaces, Git-backed marketplace sources, marketplace refresh, the portable root `plugin.json` package, repo marketplaces in `.agents/plugins/marketplace.json`, and project-level activation through `.codex/config.toml`: https://developers.openai.com/plugins/build/plugins
- OpenAI's Codex skill docs distinguish project skill discovery from skills distributed in plugins: https://developers.openai.com/codex/skills/
- Devin's plugin docs describe native package formats, repo and user scopes, Git-backed sources, floating `ref` versus fixed `sha`, Devin Desktop support, and CLI update behavior: https://docs.devin.ai/cli/extensibility/plugins/overview
- Devin's plugin update guide states that tracked branch content reaches new sessions and distinguishes cloud fetch, local CLI refresh, and Customize reindex: https://docs.devin.ai/product-guides/plugins
- Devin's skill docs list `.agents/skills/` and `.devin/skills/` as project-scoped skill directories: https://docs.devin.ai/cli/extensibility/skills/overview
- The local Wild Bunch tree has a tracked `game-studio` plugin folder, a local Codex catalog entry, generated skill projections, and a remote `architecture-pack` catalog entry. Its current `repo-skills-policy.md` defines authored plugin source separately from projected `.agents/skills/` output.
- Databricks' contributor guide describes generating self-contained, harness-specific plugin bundles from shared metadata: https://github.com/databricks/databricks-agent-skills/blob/main/CONTRIBUTING.md#plugin-metadata-metapluginpluginmetajson
