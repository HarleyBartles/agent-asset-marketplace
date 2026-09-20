# Agent Operating Model Contract Audit and Redesign

**Status:** ready-for-review

## Goal

Turn `agent-operating-model` into a contract-first plugin that can seed a
repository's operating surfaces, preserve legitimate repository ownership,
and enforce the portable invariants those surfaces must satisfy without
drifting into template synchronization, presence-only validation, or a second
skill-installation system.

The resulting model must be easy for future marketplace contributors to
understand and difficult to regress accidentally. Its source, schemas,
validators, CLI behavior, tests, and consumer diagnostics must all express the
same ownership and enforcement model.

## Problem statement

The current operating model mixes several concerns:

- templates seed consumer files but can also trigger permanent byte-identity
  checks and destructive replacement;
- some scaffold checks prove only that files exist, while other checks reject
  valid repository-specific content;
- `--apply` can report success without proving the reported drift converged;
- `--force` does not adequately distinguish deliberate template restoration
  from ordinary repair;
- the tracked hook is described in behavioral terms but is ultimately checked
  for exact template identity;
- plugin prerequisites, skill installation, and runbook/playbook references
  are not modelled at their correct ownership boundaries; and
- the current documentation does not give an agent one authoritative answer
  for what the operating model deploys, what the consumer owns, what is
  checked, and what an apply operation may mutate.

The immediate observed defect is
`.agents/doctrine/completed-artifacts.md`: the standard describes it as
repository-local custody truth, but the manifest and coordinator compare it
byte-for-byte with the seed and can overwrite it. The design treats that as
evidence of a systemic modelling problem rather than a one-field patch.

## Approved design principles

### The operating model is an ordinary plugin

`agent-operating-model` is a marketplace plugin and may contain skills. Its
plugin manifest and bundle manifest own its skill inventory. Installing the
plugin installs its skills by definition.

The operating model must not maintain prose or validators that independently
enumerate its bundled skills as things a consumer must install. It must not
copy or repair one bundled skill at a time. Plugin installation health belongs
to the plugin installation system.

### Marketplace packaging and consumer conformance are separate systems

Marketplace generation owns canonical plugin sources, bundle membership,
packaged projections, and consistency when a skill appears in more than one
plugin. Consumer operating-model validation does not reconstruct those
decisions.

A consumer repository owns its own generated indexes and generators. The
operating model may require that the repository provide and run an index
generation capability, but this marketplace's generated indexes do not define
the consumer's index contents or ownership.

### Templates are seeds, not continuing owners

A template answers one question: what valid starting content should be created
when a consumer surface is missing?

The presence of a template must not implicitly determine:

- continuing ownership;
- byte-identity validation;
- whether local changes are allowed;
- ordinary apply behavior; or
- destructive reset behavior.

Once seeded, runbooks, playbooks, doctrine, tracked hooks, repository routers,
review/contribution entrypoints, and similar consumer surfaces are
repository-owned implementations of shared contracts.

### Conformance targets invariants

For a consumer-owned surface, the standard enforces the mandatory structure
and behavior needed for interoperability. Valid repository-specific additions
must survive check and apply.

Neither exact-template comparison nor presence alone is sufficient evidence of
conformance.

### Apply must be safe and convergent

Ordinary apply may:

- create a missing surface from its seed;
- perform an explicitly defined, preservation-first migration; and
- regenerate a consumer-declared mechanical output through the consumer's
  owning generator.

Ordinary apply must not replace an existing consumer-owned file wholesale.
After apply, the coordinator reruns the complete check. It exits successfully
only when the resulting state conforms. If safe convergence is impossible, it
fails with the required human action.

### Force reset is deliberately destructive

Force reset may restore a selected surface from the current seed. It must emit
a prominent warning that repository-local customisations will be overwritten
and require an additional acknowledgement beyond the ordinary mutation
confirmation.

Interactive wording must include:

> Are you sure? This will force overwrite any repo-local customisations in
> `<path>`.

Non-interactive use requires a separately named acknowledgement flag. A plain
`--force`, even combined with the ordinary `--yes`, is insufficient.

## Plugin subscription contract

### Hard prerequisites

Conforming consumers must subscribe to:

- `agent-operating-model`;
- `superpowers-plus`; and
- `repo-worker-pack`.

The latter two supply capabilities assumed by the standard lifecycle
runbooks. Their absence is a conformance failure reported at plugin level.

### Fleet baseline warning

Consumers are expected to subscribe to `writing-pack`. Its absence produces a
non-blocking warning so an agent sees that the repository is missing the normal
writing capability baseline without being prevented from committing.

### Conditional prerequisite

If a repository contains any governed unslop profile under its declared
unslop contract locations, it must subscribe to `unslop-plus`. Profiles without
that subscription are a conformance failure. Subscribing to `unslop-plus`
without a profile remains valid.

### Additional subscriptions

Repositories may subscribe to any other plugins. The operating model does not
restrict the remainder of the subscription set.

### No duplicated skill installation policy

The subscription validator checks plugin subscriptions. It does not enumerate
the skills contained by those plugins and does not validate or repair them
individually.

The initial redesign reads subscription state from the consumer's existing
`.agents/plugins/marketplace.json` contract. Redesigning how the marketplace
catalogue itself represents or installs subscriptions is outside this work.

## Runbook and playbook skill-link contract

`## Required skills` is the authoritative skill dependency section for a
runbook or playbook. Each active reference must name an exact skill identifier
and state its role or activation condition.

For consumer conformance, every referenced skill must exist in the
consumer-visible skill namespace. It may be:

- supplied through the repository's installed plugin subscriptions; or
- a repository-local skill declared through the repository's local-skill
  contract.

The operating model reports dead links with the source document and missing
skill name. It does not reason about which or how many plugins supplied the
skill, plugin deduplication, or cross-plugin skill versions. Those are
marketplace packaging and installation concerns.

The validator must also reject a composition that operationally invokes a
skill without declaring it in `## Required skills`. Placeholder-only required
skill sections do not satisfy a required dependency contract.

## First-class consumer surface model

The repository-shape manifest must replace implicit behavior with explicit,
schema-validated fields. Every surface declares independently:

- stable surface ID;
- consumer path or path pattern;
- presence rule: required, optional, or forbidden;
- ownership: consumer-authored or consumer-generated;
- optional seed used only for missing-surface creation and force reset;
- named semantic validator;
- ordinary apply strategy;
- force-reset availability; and
- dependency or exception relationships.

No ownership-affecting field may have an implicit default. In particular,
`source` or `seed` must never imply byte comparison, and `check_content` must
be removed rather than retained as a safer-looking boolean.

Conceptual consumer-owned entry:

```json
{
  "id": "completed-artifacts-doctrine",
  "path": ".agents/doctrine/completed-artifacts.md",
  "presence": "required",
  "ownership": "consumer-authored",
  "seed": "templates/completed-artifacts.md",
  "validator": "completed-artifacts-contract-v1",
  "apply": "create-or-safe-migrate",
  "force_reset": "confirmed-template-restore"
}
```

Conceptual forbidden entry:

```json
{
  "id": "retired-plans-completed-dir",
  "path": ".agents/plans/completed",
  "presence": "forbidden",
  "ownership": "consumer-authored",
  "validator": "must-be-absent",
  "apply": "manual-remediation",
  "force_reset": "unavailable"
}
```

The manifest schema rejects incomplete and incompatible combinations,
including:

- consumer-owned surfaces with identity validators;
- consumer-owned surfaces with unconditional overwrite apply modes;
- a seed without explicit ownership, validator, apply, and reset semantics;
- forbidden surfaces without an explicit remediation strategy;
- unregistered validators or migration IDs; and
- dependency relationships that cannot be satisfied.

## Audit ledger

Before implementation changes behavior, inventory every current operating
surface and command in a checked-in design ledger or spec appendix. Each entry
records:

| Field | Meaning |
|---|---|
| Thing | File, directory, command, generator, or configuration surface |
| Current deployer | What currently creates or updates it |
| Current checker | What currently accepts or rejects it |
| Current owner | Who currently has practical custody |
| Desired owner | Consumer-authored or consumer-generated |
| Mandatory invariants | What must remain true |
| Ordinary apply | Safe creation or migration behavior |
| Force reset | Whether and how template restoration is allowed |
| Current defect | Over-enforcement, under-enforcement, unsafe mutation, or unclear ownership |

The audit includes at least:

- marketplace subscription configuration;
- the repository-shape manifest and exception mechanism;
- the consumer command declaration;
- tracked pre-commit and hosted-parity execution;
- shared-checkout support;
- root and scoped `AGENTS.md` routers;
- lifecycle runbooks and topical playbooks;
- repository runbook/playbook policy;
- completed-artifact doctrine;
- `REVIEW.md` and `CONTRIBUTING.md`;
- `.gitignore` migrations;
- consumer index and mesh capability declarations;
- local skills and installed plugin projections at their correct ownership
  boundaries;
- vendor profiles and runtime-agent staging boundaries;
- scratch validation; and
- forbidden legacy paths.

The implementation plan must assign every ledger row to a validator, migrator,
generator owner, documented manual action, or explicit removal.

## Semantic validators

Each meaningful surface has a named validator with focused diagnostics.
Validators may share parsing primitives, but failures name the violated
contract rather than generic textual drift.

### Runbooks and playbooks

Validate:

- mandatory composition sections;
- non-placeholder content for mandatory bindings;
- required skill links;
- resolvable local Markdown links;
- reciprocal runbook/playbook routing where declared;
- playbook composition target existence;
- absence of composition cycles; and
- separation of lifecycle runbooks from topical playbooks.

Repository prose, commands, paths, conditional routes, and additional sections
remain customizable.

### Completed-artifact doctrine

Validate baseline lifecycle semantics without prescribing exact prose:

- active/in-flight versus complete custody is distinguishable;
- completion includes explicit completion or abandonment;
- completion does not occur merely because scratch or rejected outputs exist;
- the completing slice records completion before retirement;
- retirement occurs in a later substantive slice;
- durable decisions promote before retirement;
- Git history is the durable record; and
- repository-specific artifact types, paths, commands, and evidence bindings
  are permitted.

This validator must accept Portfolio's image-brief lifecycle extension when it
satisfies those invariants.

### Tracked hook

Validate the behavioral contract rather than file identity:

- shell safety guards;
- materialization of the exact staged candidate tree;
- required submodule/gitlink cleanliness checks;
- preservation and restoration of unrelated work;
- consumer-declared apply before check;
- staging limited to originally staged paths and consumer-declared generated
  outputs;
- failure on unexpected authored mutations;
- hosted detached-tree parity; and
- unchanged hosted commit tree after validation.

The consumer may reorganize or strengthen the implementation while preserving
these invariants.

### Routers and entrypoints

Validate required sections, resolvable routing coverage, and entry into the
operating workflow. Optional files may be absent, but if present they must
conform.

### Plugin and skill links

Validate hard prerequisite subscriptions, the `writing-pack` warning,
conditional `unslop-plus` activation, and absence of dead skill links in
runbooks and playbooks. Do not inspect cross-plugin provider multiplicity or
versions.

## Command behavior

The standards command exposes clear modes:

### Check

- read-only;
- reports failures and warnings separately;
- exits nonzero only for failures;
- names the contract, surface, evidence, and repair route; and
- emits the `writing-pack` baseline diagnostic as a warning.

### Apply

- requires ordinary mutation approval;
- creates missing seeded surfaces;
- runs only registered preservation-first migrations;
- delegates consumer-generated outputs to their declared generators;
- never performs an implicit whole-file replacement;
- reruns the complete check after mutation; and
- succeeds only when no failures remain.

### Force template deployment

- uses `--force <surface-id>` for each explicit surface to restore;
- previews every file that will be replaced;
- warns that repo-local customisations will be overwritten;
- requires `--confirm-local-customisations-will-be-overwritten` in
  non-interactive use, or the equivalent interactive confirmation;
- refuses surfaces without a seed or force-reset contract; and
- reruns complete conformance after replacement.

Bare `--force` and `--apply --force` are invalid. The flag is a distinct,
targeted template-deployment mode rather than an ambiguous modifier on
ordinary apply.

## Hook and hosted CI integration

The tracked hook remains the local complete gate over the exact staged
snapshot. Hosted CI invokes the same hook contract against the checked-out
commit.

The hook obtains apply/check commands and generated-output ownership from the
consumer's declared command contract. It must not hard-code this marketplace
repository's generated paths as universal consumer outputs.

Warnings, including a missing `writing-pack` fleet baseline, remain visible in
hook and hosted output but do not block the commit or CI. Contract failures do.

## Exception model

Exceptions to the operating standard must not be hidden inside an unrelated
runbook mapping merely because that was a convenient parser location.

The redesign introduces
`.agents/contracts/agent-operating-model.json` as the focused consumer
conformance declaration. It contains:

- operating-model schema/version;
- plugin prerequisite exceptions, if any are permitted;
- surface exceptions and rationale;
- conditional profile locations where repository policy permits variants.

The existing `.agents/contracts/repo-standards-commands.json` remains the
consumer command declaration and gains the consumer-generated output patterns
used by the tracked hook. Keeping mutation commands and their owned outputs
together lets the hook validate one execution boundary without turning the
operating-model policy into a command bus.

Neither contract duplicates the marketplace catalogue. Plugin subscription
state remains in `.agents/plugins/marketplace.json`, and runbook/playbook
mapping remains in `.agents/doctrine/repo-runbook-policy.md`.

## Diagnostics

Diagnostics distinguish ownership-level remedies:

- missing prerequisite plugin: subscribe to the plugin;
- missing expected `writing-pack`: warning with subscription guidance;
- dead workflow skill link: install/subscribe to a plugin that supplies it,
  declare a repo-local skill, or correct the reference;
- missing consumer surface: run ordinary apply to seed it;
- invariant violation: edit the consumer-owned surface or run a registered
  safe migration;
- destructive reset requested: show the overwrite confirmation;
- generated-output drift: run the consumer's owning generator;
- marketplace plugin projection defect: report it as a marketplace problem,
  not a consumer operating-model repair.

## Migration strategy

1. Add the canonical ownership and conformance doctrine, manifest schema, and
   audit-ledger tests without changing consumer behavior.
2. Complete the full audit ledger and classify every current surface.
3. Introduce named semantic validators alongside existing checks and prove
   them against customized consumer fixtures.
4. Introduce explicit plugin prerequisite and dead-skill-link checks.
5. Replace implicit manifest semantics and `check_content` with the new schema.
6. Split ordinary apply from confirmed `--force <surface-id>` template
   deployment and add mandatory post-apply
   convergence checking.
7. Convert the hook from template identity to behavioral validation and move
   generated-output ownership into the consumer contract.
8. Provide a read-only migration audit for existing consumers.
9. Exercise safe migrations against reduced fixtures representing Portfolio,
   Adventures of Patch, Rooms Mostly, and this marketplace.
10. Update consumer repositories deliberately; do not mutate live consumers
    from marketplace tests.
11. Remove compatibility fields, wrappers, and validators only after every
    supported consumer has an explicit migration route.

## Anti-regression test contract

Marketplace CI must prove at least:

- every manifest surface has explicit ownership, validation, apply, and reset
  semantics;
- adding a seed does not activate identity checking;
- no consumer-authored surface uses byte identity;
- customized valid doctrine, hook, runbook, playbook, router, review, and
  contribution fixtures pass;
- missing or hollow mandatory invariants fail;
- ordinary apply preserves unrelated consumer content;
- safe migrations change only their declared contract seam;
- apply followed by check converges;
- a second apply is idempotent;
- apply cannot report success with remaining drift;
- force reset refuses without the additional destructive acknowledgement;
- confirmed force reset replaces only explicitly selected surfaces;
- hard prerequisite plugin absence fails;
- missing `writing-pack` warns and exits successfully when no failure exists;
- governed unslop profiles without `unslop-plus` fail;
- runbook/playbook skill references resolve or report dead links;
- plugin contents are not independently enumerated as required installed
  skills by the operating model;
- hook and hosted parity tests accept behaviorally conformant customized hooks;
  and
- repository-generated indexes are validated through the consumer's declared
  capability, never compared with this marketplace's indexes.

## Non-goals

- Redesigning marketplace-wide canonical skill authorship or cross-plugin
  skill deduplication.
- Selecting which plugin supplies a skill when multiple plugins package the
  same marketplace skill.
- Version arbitration among plugin-packaged skills.
- Restricting repositories from subscribing to additional plugins.
- Standardizing the contents of every consumer-generated index.
- Weakening staged-snapshot, hosted-parity, or publication-proof guarantees.
- Bypassing validation to unblock Portfolio's current branch.

## Acceptance criteria

The redesign is complete when:

1. A future contributor can identify every deployed consumer surface, its
   owner, its validator, ordinary apply behavior, and reset behavior from one
   canonical model.
2. Portfolio can extend completed-artifact doctrine with its image-brief
   lifecycle and pass without an exception or bypass.
3. A customized behaviorally conformant pre-commit hook passes.
4. Ordinary apply cannot erase repository-authored customisation.
5. Force reset cannot overwrite customisation without the additional explicit
   acknowledgement.
6. Apply-check convergence is enforced mechanically.
7. Required plugin subscriptions and conditional `unslop-plus` dependencies
   fail accurately; absent `writing-pack` warns without blocking commits.
8. Every active runbook/playbook skill reference resolves in the consumer
   namespace, with dead links reported precisely.
9. The operating model contains no second inventory or per-skill installation
   validator for skills already owned by plugin installation.
10. Hook and hosted CI exercise the same consumer contract on the same
    candidate tree.
11. Tests make template synchronization, presence-only validation, implicit
    ownership defaults, unsafe overwrite, and false apply success explicit
    regression failures.

## Implementation handoff

This design requires a multi-step implementation plan. Planning must begin by
turning the audit ledger into an exact file-level inventory before scheduling
schema, validator, CLI, hook, fixture, generation, and consumer-migration work.
The first implementation task must establish failing architectural tests for
the approved ownership and command semantics before changing production code.

The implementation plan must preserve this design's boundary: marketplace
packaging concerns are not pulled into consumer operating-model validation,
and consumer conformance is not weakened into template or presence checks.
