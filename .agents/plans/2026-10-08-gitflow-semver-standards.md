# Gitflow and SemVer Standards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish independently selectable AOM Gitflow and SemVer standards with development checkpoint cadence, one authored product version, build propagation, and truthful adoption guidance.

**Architecture:** Two canonical standard skills, `gitflow` and `semver`, own their definitions and operational adoption guidance. The existing repo-standards catalog and AOM plugin composition expose both choices. Each standard stands alone; their definitions explicitly compose development checkpoint obligations when both are adopted. Consumers own their implementation, immutable subscriptions, and semantic certification.

**Tech Stack:** Markdown, JSON, YAML, existing Python Marketplace builders and pytest shipping checks, isolated instruction-behavior evaluation.

**Requirements:** The approved requirements and transition table below are the design basis for this plan. Read the [implementation runbook](../runbooks/implementing.md), [skill authoring playbook](../playbooks/skill-authoring.md), and [skill test contract](../contracts/skill-tests.md) before execution.

**Execution Strategy:** `executing-plans`, inline in the same worktree. Both definitions share version transitions and adoption boundaries; sequential authoring and a whole-branch review preserve that contract without repeated implementation handoffs.

Status: planned, awaiting execution.

## Working Boundary

Worktree: `Z:/_agent-worktrees/agent-asset-marketplace/codex/gitflow-semver-standards`. Branch: `codex/gitflow-semver-standards`. Refreshed main baseline: `a9d9f280316a87ac66cb2653384bc30a683603f0`. PR base: `main`.

This repository publishes the standards and does not adopt either one in this slice. Do not introduce `develop`, application versioning, release machinery, or subscriptions here. Do not change Sheg, Wild Bunch, installed user plugins, or the agent executing Wild Bunch's epic. Their live guidance informed the design but is not portable authority.

## Approved Requirements

- Publish standard IDs `gitflow` and `semver` as independently selectable AOM choices. Plugin availability does not establish adoption or upgrade an immutable consumer pin.
- Gitflow declares the stable and integration branches, feature/release/hotfix routes, stabilization scope, promotion, and reconciliation. Use `main`, `develop`, `release/<version>`, and `hotfix/<version>` in examples. Preserve repository-owned feature prefixes such as `codex/`; do not require `feature/*` names.
- Ordinary development branches start from current integration state and target integration. Releases start from integration and promote to stable; hotfixes start from released stable state. Return fixes to continuing integration and any affected active release line. Ordinary feature work must not go directly to stable.
- Preserve release/hotfix ancestry through merge commits for promotion and reconciliation. Feature PRs may squash. Branch names, hosting adapters, required checks, and protection implementations remain repository-owned and must be declared and verified rather than inferred from documentation.
- SemVer requires a declared public compatibility contract, meaningful bump decisions, SemVer 2.0.0 syntax and precedence, prerelease handling, and immutable released identity. Explicitly describe initial-development compatibility and the contract required for 1.0.0; three numeric fields alone do not establish compliance.
- Each independently versioned product has exactly one authored product-version source. A build step propagates it to every required manifest, lockfile root, runtime identity, package, or artifact identity. Copies are derived outputs and are not hand-maintained. Independently versioned dependencies, datastore schemas, or payload contracts are not duplicate product versions.
- Version validation rejects missing, stale, conflicting, malformed, or unexpectedly independently authored product identities. Validation does not repair maintained files; propagation is explicit build/preparation. Do not require a particular language, file, command bus, CI provider, starter, or shared runtime.
- When both standards are adopted, each ordinary development merge into `develop`, including documentation/tooling work, establishes one distinct `MAJOR.MINOR.PATCH-dev.N` landmark. Commits within its PR share the assigned checkpoint; they do not each advance N. Start at positive N=1 and advance monotonically within the intended release. A squash counts as one integration, not as each source commit.
- Select the next intended release from compatibility and release scope, not an unconditional patch increment. After changing the intended release core, start that core's checkpoint sequence at dev.1. Serialize or revalidate competing PR allocations against current integration state so duplicate or stale checkpoint identities cannot land. Rebuild derived identities after reconciliation.
- A development checkpoint is not a stable release or publication. Repositories can identify checkpoints from merged source and build metadata without creating Git tags or hosted Releases for every merge.
- Release stabilization uses the intended stable core and `rc.N`, starting at rc.1 and advancing for changed candidates. Stable promotion removes the prerelease suffix after verification. Tag spelling such as `v0.2.0` is a declared repository convention; the product version is `0.2.0`.
- A release or hotfix reconciliation that leaves integration at the released baseline uses that stable version. It does not invent dev.1. The first subsequent development merge diverges from the baseline and assigns the next intended release's dev.1.
- If integration already contains future development, release/hotfix reconciliation preserves that intended release and advances its dev.N. Do not overwrite future development identity with an older released version or erase post-cut work. Reconciliation must preserve source and version authority together.
- Bind releases to verified source and matching artifact identities, reject tag/version mismatches and inappropriate source routing, and never move or reuse published version identities to represent changed contents. Deployment and artifact format are consumer choices.
- Certification explains actual implementation, mechanical checks, judgment-based compatibility decisions, and continuing drift controls. Incomplete adoption stays accurately incomplete. No ambient skill or template may silently add subscriptions, create remote branches, alter protections, tag, publish, or merge.

## Version Transition Acceptance Table

| Starting integration state | Event | Resulting integration identity |
|---|---|---|
| Released baseline `0.2.0` | First ordinary merge, intended next release `0.3.0` | `0.3.0-dev.1` |
| `0.3.0-dev.4` | Next ordinary development merge | `0.3.0-dev.5` |
| `0.3.0-dev.4` | Several additional commits inside its unmerged PR | No per-commit advancement; final checkpoint is assigned against current integration |
| Development tree for `0.2.0`, no future divergence | Reconcile released `0.2.0` | `0.2.0` |
| `0.3.0-dev.4` | Reconcile released hotfix `0.2.1` | `0.3.0-dev.5` |
| `0.3.0-dev.4` | Reconcile released `0.2.0` while future work remains | `0.3.0-dev.5` |
| `0.3.0-dev.5` | Cut release branch and prepare first candidate | Candidate `0.3.0-rc.1`; integration changes only through its own merge events |
| Candidate `0.3.0-rc.1` | Candidate changes | Candidate `0.3.0-rc.2` |
| Qualified candidate `0.3.0-rc.2` | Stable promotion | Stable `0.3.0`, with integration reconciliation assessed as above |

## Review Focus

- Release reconciliation incorrectly invents dev.1, or hotfix reconciliation overwrites future work. Task 1's transition pressure fixture covers both states with independent source-change evidence.
- Two PRs allocate the same dev.N, or an ordinary main-targeting PR is accepted. Task 1's competing-PR and invalid-route cases require rejection/reconciliation before integration.
- Five matching hand-maintained versions are incorrectly certified. Task 2 tests authority and build derivation, not merely equality.
- Missing or stale generated runtime/package metadata is accepted, or a check silently repairs it. Task 2's negative cases require failure and an explicit build/recheck route.
- A consumer adopting only SemVer is required to create develop, or an ambient refresh silently upgrades it. Task 3 extends independent-selection behavior cases.

## Task 1: Ship the Gitflow Standard and Its Development Landmark Contract

**Files:** Create `skills/gitflow/SKILL.md`, `skills/gitflow/agents/openai.yaml`, `skills/gitflow/references/standard.md`, `skills/gitflow/references/adoption-and-workflow.md`, `skills/gitflow/tests/pressure/integration-and-reconciliation.md`, and `skills/gitflow/tests/evaluator-only/integration-and-reconciliation.md`. Source-backed citation scaffolding under `skills/gitflow/assets/authority/` is generated by the authoring helper and reconciled to the actual operational references.

**Consumes:** Approved requirements and transition table above, existing v2 adoption/certification method. **Produces:** The Gitflow definition, its independent adoption method, and conditional composition with SemVer.

- [ ] Read `writing-skills` and its authoring checklist. Use a clean-room `skills-with-citation` lane, citing the original Gitflow description without copying its prose or diagram. Record the additional AOM checkpoint/reconciliation rules as original requirements from this approved design. Authority assets identify derivation boundaries; they contain no run receipts.
- [ ] Before authoring the operational skill, create one narrow pressure fixture covering stable-baseline reconciliation and already-divergent hotfix reconciliation. Include actual branch/source state, one version authority, a deadline, and misleading encouragement to reset every merge-back. The blinded baseline must decide routing and resulting identity from the supplied state. Keep expected decisions only in evaluator-only material and current outputs in external scratch.
- [ ] Run the baseline without the new skill in a fresh context. Inspect the decisions for an observable failure rather than assuming RED from an absent file. If the baseline already handles the transitions, use the concurrent-PR or feature-to-main negative case to establish the genuine behavior gap. Do not create a task-size/model matrix.
- [ ] Scaffold only after RED:

```powershell
py -3 skills/writing-skills/scripts/new_skill.py --name gitflow --custody marketplace --lane skills-with-citation --check
py -3 skills/writing-skills/scripts/new_skill.py --name gitflow --custody marketplace --lane skills-with-citation
```

- [ ] Replace scaffold examples with discovery metadata, a short operational router, the standard pledge, required/conditional obligations, semantic self-certification, and adoption guidance. Describe branch bases and targets, promotion, release scope, hotfix return routes, merge strategy, checkpoint concurrency, and both reconciliation outcomes. Link the SemVer owner for syntax and authoritative build identity. Do not infer adoption from existing branch names.
- [ ] Keep the Gitflow-only obligation about branch lifecycle independent from SemVer. Put the dev.N/rc.N composition under an explicit both-adopted condition in the definition; cross-reference the identical condition in SemVer.
- [ ] Run the same blinded scenario with the new skill and its normal references. GREEN requires correct routes and stable/future checkpoint identities; extend reusable cases for stale competing allocations, feature-to-main rejection, and fixes needed on an active release branch. Do not expose evaluator-only material to the worker. Retain reusable cases, not transcripts or scores.

## Task 2: Ship the SemVer Standard and Single-Source Build Identity

**Files:** Create `skills/semver/SKILL.md`, `skills/semver/agents/openai.yaml`, `skills/semver/references/standard.md`, `skills/semver/references/adoption-and-versioning.md`, `skills/semver/tests/pressure/single-version-authority.md`, and `skills/semver/tests/evaluator-only/single-version-authority.md`. Reconcile citation scaffolding under `skills/semver/assets/authority/` to actual references.

**Consumes:** Approved compatibility/version-authority requirements and Task 1's combined-adoption transition contract. **Produces:** The SemVer definition, version-ownership/build method, and independent adoption guidance.

- [ ] Create a narrow fixture where package, lockfile root, plugin manifest, runtime, and artifact versions currently agree but are separately authored. Provide a proposed bump that omits one copy and an instruction to certify by checking equality alone. The expected decision requires consolidation into one authored source, build propagation, and validation that rejects missing/stale copies. Include a dependency version and schema version to prove that unrelated version domains remain independent.
- [ ] Run the no-skill baseline before writing operational guidance. Inspect whether it mistakes matching numbers for compliant ownership. If it already consolidates ownership, use the stale runtime identity or check-time repair negative to find the actual behavior gap.
- [ ] Scaffold with the same custody/lane as Gitflow:

```powershell
py -3 skills/writing-skills/scripts/new_skill.py --name semver --custody marketplace --lane skills-with-citation --check
py -3 skills/writing-skills/scripts/new_skill.py --name semver --custody marketplace --lane skills-with-citation
```

- [ ] Cite SemVer 2.0.0 as external semantic authority and distinguish the AOM single-source/build/cadence additions. Keep operational prose original, with source-backed authority records and no vendored external text.
- [ ] Author short discovery/adoption instructions and the definition. Cover public compatibility, initial development and 1.0.0, justified bump decisions, numeric prerelease ordering, stable/prerelease distinction, one authored product source, derived identities, explicit propagation, immutable source/artifact identity, and mechanical-versus-semantic certification limits.
- [ ] Require consumers to identify all product-version destinations and the build/check measures that keep them derived and current. An equality-only check does not prove consolidation. For independently versioned products, document distinct authorities and scopes instead of forcing all products and dependencies onto one number.
- [ ] Describe the combined dev.N and rc.N transitions consistently with Task 1, including stable-baseline reconciliation and future-development preservation. A SemVer-only adopter is not required to adopt Gitflow, create develop, or use this merge cadence.
- [ ] Run the blinded GREEN scenario with the completed skill. Exercise missing/stale output, separately authored equal versions, a mismatched release tag, and independent schema/dependency versions through the same reusable case package. If guidance requires refinement, fix the owner and rerun only affected cases. Keep run evidence off-repo.

## Task 3: Expose, Package, Validate, and Publish the Standards

**Files:** Modify `skills/repo-standards/references/standards-catalog.json`, `skills/repo-standards/SKILL.md`, `skills/repo-standards/tests/behavior/standard-selection.md`, `skills/repo-standards/tests/evaluator-only/standard-selection.md`, `src/plugin-definitions/agent-operating-model/contents.json`, and `src/plugin-definitions/agent-operating-model/files/README.md`. Extend `tests/build/test_aom_standard_skill_discovery.py` and `tests/shipping/test_aom_standard_authority.py` to apply their existing installed-discovery and isolated-reference contracts to both new skills. Regenerate generator-owned `dist/` and catalog projections. Update this plan through completion.

**Consumes:** Complete canonical Gitflow and SemVer skill trees and definitions. **Produces:** Discoverable selectable catalog entries, self-contained AOM packages, passing validation, and a fully reviewable Draft PR into main.

- [ ] Add catalog entries with IDs/skills `gitflow` and `semver` and definition paths `skills/gitflow/references/standard.md` and `skills/semver/references/standard.md`. Add the corresponding first-party skill inclusions to AOM contents using the existing provenance schema. Route branch/release concerns and version-identity concerns from repo-standards to their smallest owners.
- [ ] Extend selection cases: SemVer only with no develop; Gitflow only with no SemVer cadence; both standards with the full transition table; installed capability with no adoption; existing older immutable pins; transitional implementation that cannot yet self-certify. Judge the decision, not exact prose.
- [ ] Extend the existing discovery and installed-reference loops to the new owners rather than add a fixed-content detector. Build/distribution tests establish that an isolated installed package can discover both choices and resolve every normal reference inside its boundary. Do not introduce a generic versioning script, scaffolder, or consumer runtime unless a witnessed behavior gap makes it necessary and the scope is separately agreed.
- [ ] Regenerate and run the focused distribution checks:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/build_marketplace.py --check
py -3 -m pytest tests/build/test_aom_standard_skill_discovery.py tests/shipping/test_aom_standard_authority.py -q
```

- [ ] Inspect source, metadata, citation records, generated packages, and unchanged Marketplace subscriptions together. Reconcile generated changes through their owner; never hand-edit dist. Re-run only changed pressure cases or focused checks when new changes justify them.
- [ ] Stage the intended source, tests, generated output, and plan. Commit normally with `feat: publish optional Gitflow and SemVer standards`; the tracked hook runs the complete staged gate. On failure, use the reported focused repair/recheck command, inspect/stage the repair, and retry. Never bypass the hook or repeat the complete gate around a successful normal commit.
- [ ] Review the complete branch against the approved requirements and repository review runbook in fresh context. Correct actionable findings, regenerate when needed, rerun focused proofs, commit normally, and obtain a fresh review of each corrected final diff.
- [ ] Complete agent-owned plan items and set this plan to `completed-awaiting-retirement` when the implementation is fully reviewable. Keep it through its completing PR. Durable consumer rules live in the two definitions and references, not in this plan.
- [ ] Push `codex/gitflow-semver-standards`, create a Draft PR into `main`, attach it to this chat, and verify GitHub's exact head against local HEAD. The PR describes published optional standards, the version transitions and authority consolidation, validation, and unchanged consumer adoption. Wait for hosted checks at the actual final SHA; do not infer them from local success.
- [ ] Report the PR URL, head SHA, focused behavior/distribution evidence, normal hooked commit and hosted check state, final review result, and material limitations. Ready, merge, and post-merge worktree retirement remain later human-owned actions. Keep this worktree for execution and handoff.

## Plan Ingress and Handoff

Retire only the completed `2026-10-07-aom-check-only-gates` plan and design in this slice's first commit. Their full scope is on refreshed main through merged PR #348, and enduring behavior is owned by the canonical hook/bus standards, implementation, tests, and current repository doctrine. Preserve other active, mixed, or uncertain planning artifacts. No remaining tracked inbound references to this retired pair were found at ingress.

This planning turn ends with the saved, normally committed plan. Execution remains in this worktree through `executing-plans` after human review. No implementation, consumer adoption, branch protection change, stable tag, or release publication is implied by writing the plan.
