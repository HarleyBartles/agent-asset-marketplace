# Runbook Composition Model Design

## Context

`repo-standards` ships runbook templates and shape requirements to consumer
repositories. The current standard defines a runbook as a "thin repo-specific
overlay" retaining "only repository paths, commands, custody, exceptions, and
local evidence requirements." That definition under-specifies the runbook role:
it never says a runbook *composes* skills. When a topic needs more than
commands there is no lawful home for it, so content collapses into
method-duplication or restated doctrine.

Observed evidence in this repository:

- The completed-artifacts binding is stated four times:
  `repo-standards/templates/completed-artifacts.md`,
  `repository-shape-standard.md` section "Completed artifacts",
  `scratch-workspace-policy.md` section "Cleanup", and
  `.agents/runbooks/completing-plans.md`.
- `scratch-workspace-policy.md` uses `cleanup-custody` vocabulary
  (`delete_now`) without naming the owning capability.
- The shipped `completed-artifacts` template encodes custody procedure
  ("before removal, promote enduring architecture decisions into ADRs") that
  `cleanup-custody` does not itself state, and never names the skill as owner.
- The "do not run `ci --check` immediately before a normal commit" rule is
  restated in `ci-validation-pipeline.md`, root `AGENTS.md`, and
  `.agents/runbooks/pr.md`.
- `.agents/doctrine/non-repo-locations-policy.md` restates portable
  worktree/scratch layout rules owned by `using-git-worktrees`,
  `scratch-workspace-policy.md`, and `worktree-and-branch-policy.md`.

## Decision

Adopt the capability-versus-composition model:

- **Skills own focused capabilities** - one coherent verb or judgment.
- **Runbooks compose** skills, doctrine, contracts, tools, and gates into a
  legitimate repository workflow for a class of change.
- **Doctrine** states stable repository truth and never orchestrates.
- **Contracts** define shapes independent participants must exchange.

The primary distinction is atomic capability versus orchestration, not
portable versus local. A skill can be repo-local; a runbook's job is
composition regardless of where its skills come from.

## Surface taxonomy

The shipped standard will state the five-way routing test:

| Question | Owning surface |
| --- | --- |
| What must remain true? | doctrine (`.agents/doctrine/`) |
| What exact shape must participants exchange? | contract (`.agents/contracts/`) |
| How do I perform one focused judgment or work? | capability skill |
| How does this repo combine capabilities for this class of change? | runbook (`.agents/runbooks/`) |
| Can a machine enforce it cheaply? | code or configuration |

## Skill shapes

The standard will name four skill shapes so consumers can classify their own:

1. **Router** - bootstrap composition and stage routing
   (`using-superpowers-plus`).
2. **Stage/workflow skill** - portable orchestration of a generic stage or a
   bounded artifact workflow (`brainstorming`, `writing-plans`,
   `executing-plans`, `subagent-driven-development`, `iterative-review`,
   `requesting-code-review`, `finishing-a-development-branch`, `writing`).
   Legal because it owns a portable stage verb and delegates repo specifics to
   the local runbook.
3. **Capability skill** - one focused verb or judgment (`cleanup-custody`,
   `generating-agent-mesh`, `verification-before-completion`, `risk-gates`).
4. **Doctrine/policy carrier** - portable doctrine shipped in skill packaging
   (`base-doctrine`, `repo-worker-base`). A carrier routes to policy
   references; it does not own a workflow verb.

## Composition rule

- Runbooks may compose peer skills.
- Capability skills may delegate to a narrower prerequisite but must not
  sequence a repository delivery lifecycle.
- Stage/workflow skills orchestrate a portable stage and read the local
  runbook for binding; they never restate repo specifics.
- Doctrine and contracts never orchestrate.

## Runbook contract

A runbook is the repository's composition manifest for a class of change.
Required skeleton sections:

- `When` - the change class or trigger this runbook covers.
- `Required skills` - the skills this composition invokes (owning stage skill
  for stage runbooks; the composed set for workflow runbooks).
- `Composition` - order or conditions under which the skills apply.
- `Doctrine and contracts` - the local truths and shapes that constrain the
  composition.
- `Local commands and paths` - repository commands, paths, and exceptions.
- `Evidence contract` - what the combined workflow must prove.
- `Prohibited combinations` - combinations explicitly not legitimate here.

Runbooks still must not repeat portable doctrine or skill internals; they name
and sequence owners rather than restating them.

## Boundary rulings

1. The "promote durable content to owning surfaces before removal" step moves
   up into `cleanup-custody` as canonical method. The repo binding keeps a
   one-line pointer plus this repo's promotion destinations (`adr/`,
   `.agents/doctrine/`, `.agents/runbooks/`).
2. `templates/completed-artifacts.md` becomes doctrine-only (stable truth: not
   retained, git history is the record, not authority, promotion destination
   map) plus a line naming `cleanup-custody` as owning capability and the
   completion runbook as owning composition.
3. The completion runbook (`completing-plans.md`) becomes a standard-listed
   additional runbook so the mandatory doctrine node has a shipped composition
   home. `RUNBOOK_TITLES` and the policy template gain the entry.
4. `repository-shape-standard.md` sections "Completed artifacts" and
   "SDD scratch" compress to pointers at the owning surfaces.
5. `scaffold_runbooks.py` emits the composition-manifest skeleton instead of
   the freeform stub.
6. `repo_standards.py --check` gains a WARN-level check: every
   `.agents/runbooks/*.md` (excluding `AGENTS.md`) must contain a
   `## Required skills` section. Warnings print as `WARN:` lines and never
   fail the gate.
7. Local instances align in the same change: `.agents/runbooks/*.md` gain
   `## Required skills` sections (`completing-plans.md` recast as a full
   composition manifest; `marketplace-generation.md` gains Required skills and
   an evidence contract), root `AGENTS.md` publication-proof section trims to
   the local binding, `.agents/runbooks/pr.md` compresses the `ci --check`
   rule to a pointer, and `non-repo-locations-policy.md` reduces to local
   deltas plus a pointer to the canonical policies.

## Out of scope

- `ci-validation-pipeline.md` worker-method sections and the
  `agents-md.template.md` heading invitation (separate follow-up).
- Refactoring stage/workflow skills or doctrine carriers; this design names
  them rather than restructuring them.
- FAIL-level enforcement of runbook sections or skill-shape linting.

## Acceptance evidence

- `tests/test_repo_standards.py` covers the scaffold skeleton and the WARN
  check (fires on missing section, silent when present).
- `.agents/doctrine/completed-artifacts.md` remains byte-identical to the
  shipped template (manifest `check_content`).
- `py -3 tools/run.py ci --check --diagnostics` reports the WARN check output
  with zero warnings for this repo's runbooks and all gates green.
- Changes publish through the normal hooked commit on the plan's draft PR.
