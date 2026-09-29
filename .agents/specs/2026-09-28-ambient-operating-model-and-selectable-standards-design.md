# Ambient Operating Model and Selectable Standards Design

## Problem

Agent Operating Model currently behaves partly like an ambient capability catalog and partly like a mandatory consumer standard. Its shape validator requires subscriptions to Agent Operating Model, Superpowers+, and Repo Worker Pack, and its shape/runbook contracts assume particular consumer surfaces and exact workflow-skill names. This makes a consumer install and refresh broad plugin copies merely to use a subset of portable guidance. It also makes a lean repository adopt an operating model it did not choose.

The five plugins intended to be ambient are Agent Operating Model, Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+. This design changes Agent Operating Model into the ambient catalog of deployable standards and separately audits the four companion packs, whose roles and repository assumptions must remain distinct. Unslop+ has a different relationship to repository-deployed profiles that the audit must examine explicitly. PR #334 fixed one concrete Superpowers+ assumption about repository guidance discovery; the other assumptions in the four companion packs have not yet been audited as part of this design.

There is a consumer migration dependency: Rooms-Mostly's canonical validation runner currently calls refresh and mesh scripts supplied by Repo Worker Pack. Removing that subscription before replacing those runner dependencies would break its hook and hosted CI.

## Goal

Make Agent Operating Model an ambient catalog of capabilities and deployable operating standards. Let each repository explicitly choose which marketplace standards it adopts, define its own standards independently, and run checks and scaffolding only for its declared composition. Provide an incremental migration that allows consumers such as Rooms-Mostly to remove ambient-pack subscriptions without losing their existing validation behavior.

## Design decisions

### 1. Separate ambient capability from consumer adoption

Agent Operating Model is an ambient plugin available to agents. It provides skills to discover, assess, compose, and deploy its available standards and implementation resources. Availability of the plugin does not mean a repository implements the Agent Operating Model, and no consumer is required to subscribe to or install a copy of it.

The ambient catalog may include deployable implementation material such as templates, validators, command-bus entries, and supporting contracts. These are source inputs an agent can use to implement a selected standard in the consumer repository; they are not runtime dependencies that require the ambient plugin to exist in consumer CI.

The ambient packs have distinct roles and must not be collapsed into one operating-model layer:

- **Superpowers+** is workflow-based. It helps an agent select and carry out a suitable workflow, with stage and process skills.
- **Repo Worker Pack** is a set of general-purpose agent capabilities available when needed for repository work, such as source custody, worktrees, validation, and publication. These skills are ambient tools an agent can rely on being available in its harness; they do not define a repository's standards and do not own Superpowers+'s workflow routing.
- **Agent Operating Model** is a catalog of deployable standards and their implementation resources. It is not a mandatory consumer standard or the owner of general worker capabilities.
- **MCP Usage Pack** is ambient guidance for using available MCP surfaces; it must not impose a consumer's connector configuration or repository layout.
- **Unslop+** supplies ambient writing-quality capabilities and profile tooling. Its relationship to consumer-owned or explicitly deployed writing profiles must be defined without making the whole plugin a mandatory repository subscription.

A consumer must not need to copy whole ambient plugins just to access their guidance. Their sources must not impose consumer standards, names, directory layouts, or marketplace subscription choices unless the consumer has explicitly adopted the corresponding standard. The four-pack audit must preserve these distinct roles while identifying and removing cross-layer assumptions.

### 2. A repository composes adopted and repository-owned standards

Each consumer declares the standards it has chosen to implement. A declaration can include:

- standards selected from the Agent Operating Model catalog, identified as marketplace-sourced and with the source/version information required to reproduce their deployed checker and scaffolding;
- standards authored and owned by the consumer, identified as repository-owned; and
- relationships between selected standards where one genuinely depends on another.

The declaration does not require the consumer to adopt all, or any, catalog standards. A repository may implement catalog standards `x` and `z`, decline `y`, and add repository-owned standards `a`, `b`, and `c`. Omitted catalog entries are simply unadopted; a mandatory declined-list is not required. A consumer may choose its own homes and entrypoints subject to the deployed standard's stated interface, rather than inheriting a fixed directory layout by virtue of using one other standard.

The implementation will define a machine-readable consumer composition contract and its migration from current marketplace plugin subscription metadata and `.agents/contracts/agent-operating-model.json`. Exact field names and schema version are implementation-plan decisions; the semantic ownership and selection behavior above are binding.

### 3. Adoption deploys an owned, reproducible implementation

Adopting a standard is an explicit deployment or migration action. The agent uses ambient catalog material to place the chosen standard's required contracts, validators, templates, command-bus entries, and support files into the consumer's declared locations. The consumer's declaration and deployed validation inputs then become the source CI can execute.

Deployed content must have provenance sufficient to identify its catalog standard and source revision. Updating a catalog standard in a consumer is deliberate and scoped to that standard. Refreshing ambient workflow skills must not update, add, or remove consumer standards or unrelated deployed files.

The deployed implementation must remain operable if Codex ambient plugins are unavailable. In particular, hosted CI must not resolve a standard checker by looking up an ambient skill or plugin. A consumer's canonical runner invokes only the checkers for its declared standards using consumer-controlled, pinned material. Standards may declare dependencies, but those dependencies must be explicit, validated, and limited to the selected composition.

### 4. Standard enforcement is selective and composition-driven

The consumer's canonical check/apply runner reads the declared composition and dispatches only the selected standards' declared checks or scaffolding actions. No global operating-model profile is implicitly enabled. A repository adopting no marketplace standards does not receive marketplace-standard checks or scaffolds merely because Agent Operating Model or another ambient pack is available to its agents.

Checks and scaffolds must have a declared owner and stable invocation contract. The implementation plan will determine how existing `repo-standards` evolves: it may remain as a coordinator over declared standards, but it must not retain a hidden fixed surface inventory that forces adoption. A standard's checker must distinguish read-only validation from mutation and must honor consumer-owned paths and explicit exceptions defined by that standard's contract.

### 5. Portable workflow contracts request capabilities, not ambient skill names

Portable runbooks and playbooks describe the capability needed at each workflow step. At runtime, the agent inspects the skills actually available and selects a suitable provider. An exact skill name remains valid when it identifies a genuinely consumer-owned skill or a capability whose exact identity is part of an explicitly adopted local contract.

If a workflow marks a capability as required and no suitable provider is available, the agent stops and reports the missing capability. It must not silently omit the step, substitute an unrelated skill, or infer that a plugin subscription is required. Existing consumers may retain exact ambient skill references during a compatibility transition, but the portable contract and newly deployed templates must use capability requirements.

The companion-pack audit will classify each relevant instruction or reference as ambient workflow guidance, general worker capability, deployable standard material, consumer-specific policy, or an invalid consumer-layout/subscription assumption. It covers Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+, using PR #334 as evidence for the fixed Superpowers+ case rather than as evidence that the broader audit is complete. Agent Operating Model is covered by the primary catalog and deployment redesign in this spec, not omitted from the ambient-plugin set.

### 6. Preserve consumers through a staged compatibility migration

The marketplace release must support a consumer transition in which existing runner contracts continue to work while dependency-providing scripts are moved or replaced. In particular:

1. Identify the exact refresh function Rooms-Mostly calls, its ownership, and its hook/CI behavior. The index mesh and its generator/validator were retired in Plan 1; Rooms removes those calls and files with no replacement mesh entrypoint.
2. Provide a supported refresh entrypoint that does not require the consumer to subscribe to Repo Worker Pack. The pinned `.agents/plugins/marketplace-source` submodule may provide this utility directly, provided the consumer's hosted runner is pinned and the utility remains independent of ambient skill projections.
3. Migrate the relevant marketplace consumer contract and validator so the selected standard deployment and refresh entrypoint are recognized and validated.
4. Only after the bridge is available may Rooms remove Repo Worker Pack and Superpowers+ subscriptions while preserving its hook and hosted check behavior.

The compatibility path must not silently change what the runner refreshes, generates, or validates. A consumer migration guide will state ordering, expected intermediate states, how to validate each step, and how to recover if a consumer cannot adopt the new composition immediately.

## Runtime and validation boundaries

The design has three distinct runtime surfaces:

1. **Agent runtime:** ambient plugins expose skills and catalog resources to Codex agents. Skill discovery is runtime-dependent and governs how an agent carries out work.
2. **Consumer repository:** its declared standards, deployed templates/checkers, local standards, and canonical runner define what that repository adopts and enforces.
3. **Hosted CI:** runs the consumer's canonical runner from checked-in or otherwise pinned consumer-controlled sources. It does not install or assume ambient Codex plugins.

The consumer's adopted composition is the authority for which validators and scaffolds run. Installed plugin projections may support agent discovery, but their presence alone is not proof of standard adoption and their refresh must not mutate the adopted composition.

## Non-goals

- Requiring every consumer to implement Agent Operating Model or any default bundle of its standards.
- Replacing repository-owned standards with marketplace standards or requiring consumers to publish their own standards back to the marketplace.
- Installing or copying whole ambient capability packs into consumer repositories as a prerequisite for using their portable guidance.
- Making hosted CI depend on Codex, ambient plugin installation, or runtime skill discovery.
- Migrating Rooms-Mostly or other consumer repositories in this marketplace change, beyond providing and documenting a safe supported transition path.
- Defining consumer-specific policy, directory layout, commands, exceptions, or standards on behalf of the consumer.

## Acceptance criteria

- No validator or scaffold treats Agent Operating Model, Superpowers+, or Repo Worker Pack as mandatory marketplace subscriptions solely because a consumer uses the operating-model tooling.
- A consumer can declare any supported subset of catalog standards and additional repository-owned standards, including an empty catalog-standard set.
- The consumer's check/apply runner invokes only checks and scaffolds in its declared composition and validates declared dependencies.
- A hosted CI run can validate an adopted standard using the consumer's pinned implementation without ambient plugins installed.
- Ambient skill refresh does not alter the consumer's standard composition or deployed standards.
- Portable runbook/playbook contracts select skills by capability, preserve exact references for genuine repo-owned skills, and stop clearly when a required capability has no provider.
- The four companion ambient packs have a documented assumption audit, with findings, disposition, and source locations; Agent Operating Model's catalog and deployment assumptions are addressed by its primary redesign.
- Rooms has a documented and technically viable sequence to move refresh off the Repo Worker Pack installed-skill path, remove the retired mesh calls entirely, and only then remove ambient-pack subscriptions, with unchanged hook and hosted validation intent.
- Existing consumers have a compatibility and migration path with explicit validation and recovery guidance.

## Planning handoff

The implementation plan should first map current plugin subscriptions, standard surfaces, consumer runner entrypoints, source-version/provenance mechanisms, and generated projections. It should then sequence the work so the Rooms runner compatibility bridge and selective declaration/checker contract land before any consumer is asked to remove ambient subscriptions. The plan must assign the four-pack assumption audit, capability-based runbook/playbook contract, Agent Operating Model catalog/deployment changes, hosted-CI behavior, consumer migration documentation, and generated output regeneration to explicit tasks with acceptance evidence.

Do not implement consumer migrations in this marketplace slice. Use the current marketplace source/build ownership model; do not hand-edit generated `dist/` or installed `.agents/skills/` projections.
