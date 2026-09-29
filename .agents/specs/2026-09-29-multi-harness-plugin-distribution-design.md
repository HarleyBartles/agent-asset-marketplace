# Repo-Scoped Plugin Distribution Design

> **Status:** Architectural specification, ready for planning handoff. Ambient installation and refresh are owned by each harness and operator; preserve the working Codex marketplace, and use Devin’s native Git-backed user plugin install/update. AOM does not manage ambient plugins. Consumer repos subscribe to plugin Git sources through native repo configuration, tracking the published branch (normally `main`) by default and loading plugins only in that repo. Consumer repos do not vendor plugin files or project plugin skills into `.agents/skills/`. AOM provides deployable artifacts that let a repo opt into and scaffold the repo plugin subscription standard, then own its implementation, plus validation against the standard. The ambient Agent Capability Pack (ACP) owns `refreshing-installed-plugins`, which requests or guides harness-native refresh for the current repo. Use one portable Agent Plugins package when it works for both harnesses, with native metadata only when needed. The Wild Bunch migration is handed to an agent working in Wild Bunch. Claude Code packaging is out of scope.

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
- Provide an ambient ACP skill named `refreshing-installed-plugins` to refresh declared repo plugins through harness-native mechanisms. This capability is available across repos, but operates only on the current repo's declarations.
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
- The existing `refreshing-installed-skills` source is in `skills/refreshing-installed-skills/`, is packaged in Repo Worker Pack, and contains a script that projects plugin skills into `.agents/skills/`, tracks projection provenance, delegates vendor-profile installation, validates repo-local skills, and can roll `marketplace-source`. Worktree creation also calls its script. Those behaviors and callers must be inventoried during the re-purpose; plugin-skill projection and submodule rolling are not part of the new plugin refresh contract.

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

### Ambient Agent Capability Pack (ACP) capability: `refreshing-installed-plugins`

Replace the old plugin-projection behavior with an ambient capability named `refreshing-installed-plugins`, owned and packaged by ACP (the renamed Repo Worker Pack). It acts on the current repo's configured plugin sources and invokes or explains the appropriate native Codex or Devin refresh, then explains how to verify availability in a new session. It does not edit ambient installs, copy plugin payloads, project skills, or advance SHAs when a consumer tracks a branch. SHA pinning remains an explicit opt-in for repos that need controlled adoption. The skill is a reusable capability, not a repo policy: a repo adopts the AOM artifact to scaffold its own subscription implementation and validation, then a worker can use this ambient capability to refresh plugins declared there.

The existing `refreshing-installed-skills` script also serves worktree creation and contains local-skill validation, projection provenance, and vendor-profile deployment responsibilities. The implementation plan must map any still-needed responsibilities to their correct owners and update every caller before retiring the old skill and script. It must remove plugin-skill projection and `marketplace-source` rolling behavior from the plugin refresh path; it must not silently carry forward the old plugin projection contract under a new name.

### Pin and publication policy

Every plugin update merged to Marketplace `main` is published. Consumer declarations track `ref: main` by default, so their config does not need a SHA change when Marketplace content advances. The harness resolves the branch during its native refresh/session fetch; a running session keeps the content it loaded at start. A consumer can instead pin a SHA when it needs reproducibility or wants to review and adopt updates deliberately. Plugin `version` remains human-facing metadata, while the commit SHA identifies the bytes.

## Acceptance criteria

- The Codex marketplace remains valid and existing user-level Codex plugin installs can still be refreshed through Codex's native marketplace flow.
- Devin ambient plugins can be installed and updated through Devin's native Git-backed plugin mechanism; no parallel Marketplace ambient installer or manual skill-copy workflow is introduced.
- A consumer can declare a plugin source in the native Codex and Devin repo configuration, with the source repository, plugin subdirectory, and moving published branch explicit. Marketplace plugins default to `main`; consumers can choose a fixed SHA.
- Plugin payloads remain outside consumer repos. A repo subscription does not require the Marketplace repository as a submodule, a checked-in plugin copy, or generated plugin-skill files in `.agents/skills/`.
- Repo declarations scope plugin availability to the declaring repo and its worktrees according to the harness's native behavior. They do not create a user-level ambient installation.
- AOM provides a deployable artifact that scaffolds repo opt-in to the subscription standard and validation against it; the consuming repo owns the adopted implementation. ACP provides the reusable `refreshing-installed-plugins` capability. Their responsibilities and package names are unambiguous.
- Refresh uses each harness's supported native mechanism, operates on plugin declarations relevant to the current repo, does not change refs or SHAs, and explains when a new session is needed to load updated content.
- Plugin packages use the portable Agent Plugins root manifest and layout where both harnesses support the needed behavior; harness-specific metadata is added only for an evidenced incompatibility or required feature.
- The former plugin projection and Marketplace-source rolling workflow is removed from the plugin lifecycle. Any independent responsibilities formerly sharing its implementation have explicit owners and updated callers before retirement.
- The Marketplace change produces a bounded Wild Bunch handoff with verified source coordinates and repo-scoped acceptance checks. Wild Bunch files are changed only by the responsible agent working in that repo.

## Wild Bunch consumer handoff

This Marketplace work makes the plugin packages, AOM artifact for opting into the repo subscription standard, and ACP refresh capability available for Wild Bunch. The Marketplace implementation does not edit Wild Bunch. Prepare a bounded handoff for a responsible agent working in Wild Bunch to adopt the artifact, own the resulting local implementation, and replace its local Game Studio plugin bundle and plugin-skill projections with repo-scoped Git plugin declarations for Game Studio and Architecture Pack, defaulting to their published branches. That agent also determines whether the Marketplace source submodule has remaining non-plugin responsibilities.

The Codex repo-scoped moving-ref refresh spike is the first plan task and a gate: implementation of repo-scoped refresh must not proceed until the spike establishes the actual native declaration and refresh behavior for `ref: main`. Confirm Game Studio’s source repository, plugin subdirectory, published branch, and Devin source form so the Wild Bunch agent receives concrete declarations and acceptance checks.

## Planning gates and verification inputs

1. Start the plan with a bounded proof that Codex resolves and refreshes a repo-scoped Git-subdirectory plugin tracking `ref: main` in the target project and its worktrees. This confirms the exact native refresh operation the Agent Capability Pack skill should explain. Treat failure as a design blocker requiring a revised native-compatible repo subscription model before implementation.
2. Validate the portable root `plugin.json` package against representative shipped plugins in Codex and Devin, and identify only the genuine harness-specific exceptions.
3. Inventory all callers and responsibilities of `refreshing-installed-skills`; determine which residual duties remain needed, assign them to their actual owners, and update callers before retiring the skill/script. Remove plugin-skill projections and submodule rolling from the plugin lifecycle; preserve unrelated behavior only where the live contract still requires it.
4. Confirm Game Studio’s Git source/path/branch and Devin source form, then prepare the Wild Bunch agent handoff, including the submodule responsibility question.

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
