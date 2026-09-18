# Agent Operating Model Design

## Context

`repo-standards` began as a focused repository-shape capability. It now owns a
large collection of distinct concerns: repository shape, root routing,
runbook and playbook composition, command-bus conventions, validation
pipelines, tracked pre-commit hooks, hosted-CI parity, repository-local skill
installation, vendor profiles, scratch validation, and multiple scaffolds.

This concentration creates three problems:

- agents must load one broad skill even when they need only one capability;
- source, tests, references, templates, and scripts accumulate behind a single
  trigger and ownership boundary;
- `repo-worker-pack` increasingly looks like both a worker-safety pack and the
  home of the repository operating system, making its purpose ambiguous.

The current `repo-standards` source includes a 700-plus-line coordinator,
eight scaffold scripts, a tracked hook template, repository-shape manifests,
validation guidance, scratch policy, vendor-profile deployment, and
skill-script validation. These are related, but they are not one capability.

## Decision

Create a first-party Codex plugin named `agent-operating-model`, displayed as
**Agent Operating Model**.

The plugin defines the portable repository structure, workflows, commands,
validation, and execution contracts that enable agents to work coherently
inside a repository. It is distinct from `repo-worker-pack`:

- `repo-worker-pack` owns how an individual worker performs repository work
  safely: worktrees, source custody, risk gates, publication, and closeout.
- `agent-operating-model` owns how a repository presents itself and operates
  for agents: repository shape, workflow composition, command dispatch,
  validation, hooks, and installed agent capabilities.

The existing `repo-standards` name remains as the plugin's thin public router.
It identifies the applicable standard, loads the owning capability skill, and
reads the consumer repository's local policy. It does not retain the combined
implementation of every standard.

## Plugin boundary

The initial plugin contains these skills:

| Skill | Ownership |
| --- | --- |
| `repo-standards` | Thin router across the operating-model capabilities and consumer policy. |
| `repo-shape` | Required agent-facing surfaces, root `AGENTS.md`, pointers, manifests, exceptions, and structural checks. |
| `repo-composition` | Runbooks, playbooks, composition sections, optional routing relationships, scaffolds, and composition-graph validation. |
| `command-bus` | Named command targets, standard flags, dispatch, help behaviour, exit semantics, orchestration, and command-bus tests. |
| `repository-validation` | Focused checks, complete gates, apply/check convergence, diagnostics, evidence, and generated-drift detection. |
| `tracked-repo-hooks` | Tracked pre-commit hooks, staged-snapshot execution, linked-worktree activation, and hosted-CI parity. |
| `repo-agent-assets` | Repository-local skills, marketplace subscription declarations, installed projections, provenance, and refresh boundaries. |
| `python` | Python language, typing, testing, concurrency, compatibility, and profiling guidance used by Python repositories and command buses. |

These skills are available capabilities, not a mandatory invocation chain.
`repo-standards` composes them only when a broad standards migration requires
several owners.

Examples:

- editing a runbook or playbook invokes `repo-composition`;
- adding a command target invokes `command-bus` and, for a Python command bus,
  `python`;
- diagnosing a complete repository gate invokes `repository-validation`;
- adopting local/hosted hook parity invokes `tracked-repo-hooks` and
  `repository-validation`;
- changing installed repository capabilities invokes `repo-agent-assets`;
- performing a complete operating-model migration enters through
  `repo-standards` and composes every applicable owner.

Playbooks remain available topical workflows. They do not require a runbook
parent and may compose or hand off to other playbooks. When a runbook/playbook
routing edge is declared, both sides record it consistently.

## Skill boundaries

### `repo-standards`

The router answers three questions:

1. Which operating-model capability owns this request?
2. Which local policy or exception binds the portable standard?
3. Does the request cross enough boundaries to require a composed migration?

It keeps only routing guidance and a compact capability map. It does not own
scaffold implementations, hook templates, command-bus mechanics, or detailed
validation method.

### `repo-shape`

This skill owns the declared repository surface model and the coordinator that
checks or applies that model. It may call narrower scaffold helpers supplied by
other skills, but it does not absorb their policy. Its manifest describes
surface presence, dependencies, content checks, and explicit exceptions.

### `repo-composition`

This skill owns the distinction between lifecycle runbooks and topical
playbooks. It owns their templates, policy mapping, headings, indexes, and
declared routing-edge checks. It permits standalone playbooks and
playbook-to-playbook composition.

### `command-bus`

This skill owns the portable command-bus contract, not one repository's target
names. A conforming command bus provides:

- a thin, documented entrypoint;
- named targets with deterministic dispatch;
- consistent `--help`, `--check`, `--apply`, and diagnostic semantics where
  those modes are applicable;
- non-zero exit status for failed or unresolved work;
- stable orchestration order and visible child-command failure;
- focused tests for discovery, dispatch, mode handling, and exit behaviour.

Consumer repositories retain authority over their target inventory and the
commands behind each target.

### `repository-validation`

This skill owns the difference between focused validation, the complete local
gate, staged-snapshot proof, and hosted proof. It defines evidence requirements
and apply/check convergence without assuming that every consumer uses Python,
Ruff, or this repository's `tools/run.py` spelling.

### `tracked-repo-hooks`

This skill owns the portable tracked-hook implementation and its activation
contract. The hook materializes the staged tree, invokes consumer-declared
apply and check vectors, restores unrelated working state, and provides the
same execution boundary to hosted CI. Consumer command definitions remain
outside the hook.

### `repo-agent-assets`

This skill owns the repository's declared plugin subscriptions and local skill
inventory. It distinguishes canonical plugin source from installed
projections, refreshes projections through the declared generator, records
provenance, and prevents orphaned installed skills. It does not own general
marketplace publication.

### `python`

The existing first-party `python` skill moves from `language-patterns-pack`
into `agent-operating-model`. It is bundled because Python is a standard
implementation capability for repositories using the shared command-bus
model. The skill remains independently invocable; using `command-bus` does not
make Python mandatory for non-Python consumers.

`python-frameworks` and `typescript` remain in `language-patterns-pack` unless
a later design changes their custody.

## Material leaving `repo-standards`

The migration also corrects existing misplaced ownership:

- scratch-workspace policy moves to `subagent-workspace`;
- vendor subagent-profile deployment moves to `selecting-a-subagent` or the
  installed-skill refresh owner;
- skill-script authoring validation moves to `writing-skills`;
- generic worktree, branch, publication, and source-custody guidance remains
  in `repo-worker-pack`;
- marketplace-wide generation remains under the marketplace-generation
  workflow rather than the operating-model plugin.

Shared helper code may be packaged once inside the plugin, but a helper's
physical location does not transfer policy ownership to `repo-standards`.

## Source custody and generated surfaces

Canonical source lives under:

`codex-marketplace/plugins/agent-operating-model/`

The plugin has its own manifest, source notes, bundle manifest, icon, and
skill tree. `.agents/skills/` remains a generated installed projection.

The migration moves canonical skills rather than copying them. A capability
has one canonical source home. Bundle manifests, marketplace manifests,
installed skills, indexes, and mesh files are regenerated after each custody
move.

`agent-operating-model` becomes installed by default for this repository.
Consumer repositories opt into the plugin through their own marketplace
policy. Adoption remains explicit; creating the plugin does not silently
change every consumer repository.

## Migration sequence

The migration proceeds in behaviour-preserving slices:

1. Resolve PR #321 as part of this programme. The preferred route is to remove
   the abandoned standalone-Python-plugin work from its worktree, retain and
   finish the approved runbook/playbook corrections, validate its exact
   committed tree, push the repaired head, and take the PR through its normal
   review and merge gate. Those corrections include directory separation,
   removal of duplicate playbook classification, directly available
   playbooks, optional runbook routing, and legal playbook-to-playbook
   composition.
2. If #321 cannot be completed, explicitly supersede it: port its entire
   runbook/playbook separation and corrections into the first
   `agent-operating-model` implementation branch, publish replacement proof,
   and close #321 only after the replacement contains every intended change.
   Do not abandon #321 informally or leave its accepted taxonomy unimplemented.
3. Update the operating-model implementation branch onto the merged or
   superseding taxonomy before changing plugin custody.
4. Scaffold and register `agent-operating-model` without moving capabilities.
5. Move `repo-standards` from `repo-worker-pack` unchanged and prove source,
   bundle, and installed-projection parity.
6. Extract `command-bus` and its tests from the monolithic skill.
7. Extract `tracked-repo-hooks` and `repository-validation`, preserving the
   staged-snapshot and hosted-parity contract.
8. Extract `repo-composition`, followed by `repo-shape`.
9. Extract `repo-agent-assets` and route misplaced supporting material to its
   proper external owners.
10. Move `python` from `language-patterns-pack` into the new plugin.
11. Reduce `repo-standards` to the router and run repository-wide pressure,
   projection, and compatibility validation.
12. Migrate consumer repositories through separate, repository-owned changes.

Each slice must leave the marketplace and this repository installable. No
intermediate commit may publish duplicate canonical custody for a skill.

## Compatibility

Existing consumers invoking `repo-standards` keep that public skill name. The
plugin move changes distribution custody, not the invocation contract.

The initial extraction preserves command-line entrypoints and consumer-facing
environment variables. Renaming scripts or commands is a later decision and
requires explicit compatibility handling. The tracked-hook contract remains
language-agnostic: consumers continue to declare their own apply and check
vectors.

## Validation

The implementation must prove:

- every moved skill has one canonical source and one bundle owner;
- installed projections match canonical source byte-for-byte where declared;
- the plugin manifest and bundle manifest validate;
- `repo-standards` routes each concern to the intended capability;
- focused tests cover every extracted capability boundary;
- command-bus tests cover discovery, dispatch, standard modes, orchestration,
  and exit propagation;
- tracked-hook tests preserve staged-snapshot, linked-worktree, and hosted-CI
  behaviour;
- standalone playbooks and playbook-to-playbook composition remain valid;
- marketplace, repository index, mesh, and complete local CI checks pass;
- a hooked commit validates the exact staged tree before publication.

## Non-goals

- Merging `repo-worker-pack` into the new plugin.
- Making Python mandatory for non-Python consumer repositories.
- Automatically migrating consumer repositories in the plugin-source PR.
- Redesigning the Superpowers stage workflow.
- Renaming every existing command-bus entrypoint.
- Turning playbooks into children that require runbook reachability.
- Combining the architectural migration with PR #321.

The last point means #321 stays a focused taxonomy PR when it can be finished;
it does not mean the programme may ignore, strand, or silently replace it.

## Planning handoff

After this specification passes readiness review and receives human approval,
`writing-roadmaps` will divide the migration into consecutive PR-sized plans
and write Plan 1. The roadmap must preserve a green marketplace after each
custody move, identify generated surfaces separately from canonical source,
and begin with an executable #321 finish-or-supersede lane before the
`repo-composition` extraction. Each later plan passes through `writing-plans`
only when its predecessor's required state is available.
