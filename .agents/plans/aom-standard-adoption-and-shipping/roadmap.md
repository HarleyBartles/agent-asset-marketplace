# AOM Standard Adoption and Shipping Roadmap

**Status:** Implementation in progress. Each plan is written just in time and reviewed before execution.

**Design authority:** [Approved specification](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), approved by the human on 2026-09-30; recorded in commit `c380a60e8`.

**Workspace:** `Z:/_agent-worktrees/agent-asset-marketplace/codex/open-runbook-playbook-composition`, branch `codex/open-runbook-playbook-composition`. Continue this planning slice here. Do not switch the primary checkout or discard existing future plans.

## Goal

Ship AOM as independently selectable standard skills with immutable source authority, repository-owned implementation, continuing self-certification, effective routing, and explicit agent-led adoption. Reconcile this Marketplace's own implementation after the new capabilities exist. Other repositories remain untouched unless separately authorized.

## Sequence

|   # | Title                                                 | Status                        | Plan File                                                              | Commit      | PR  | Rating | Notes                                                                                                                                                                                                                                                                                                                                 |
| --: | ----------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------- | ----------- | --- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1 | Standard authority packages and subscription records  | complete                      | [Plan 1](2026-09-30-plan-1-standard-authority.md)                      | `345e39234` | -   | -      | Ship all agreed definitions, the subscription contract, pinned local-source reading, and coordination guidance. Preserve current consumer runtime until explicit migration.                                                                                                                                                           |
|   2 | Optional adoption assets and document compliance      | completed-awaiting-retirement | [Plan 2](2026-10-01-plan-2-optional-adoption-assets.md)                | `d6f8947f1` | -   | -      | Agent-guided adoption, optional starters and consumer-owned checkers; full gate passed and final whole-range review found no Critical or Important issues.                                                                                                                                                                            |
|   3 | Command bus standard assets                           | completed-awaiting-retirement | [Plan 3](2026-10-01-plan-3-command-bus.md)                             | `6f8862e2d` | -   | -      | Optional Python CLI bootstrap and samples, 13 behavior tests, isolated package proof, and three fresh-context adoption probes; Windows hook gate passed. Fresh whole-range review found no Critical or Important issues; final help correction received a clean focused review.                                                       |
|   4 | Hook/CI standard assets and text normalization        | completed-awaiting-retirement | [Plan 4](2026-10-01-plan-4-hook-ci-normalization.md)                   | `6ca3e73a8` | -   | -      | Optional candidate hook, normalization and hosted-gate examples, and bus-target sample shipped. The Windows commit gate and focused tests passed. Initial whole-range review findings were corrected; fresh correction review found none. Linux execution/equivalence remains Plan 8 evidence.                                        |
|   5 | Semantic planning-artifact custody                    | completed-awaiting-retirement | [Plan 5](2026-10-01-plan-5-semantic-planning-artifact-custody.md)      | `535c04253` | -   | -      | Semantic completion and pinned-version boundaries shipped; hook candidate adapter and path-limited commit fixes also landed during whole-range review. Full Windows gate passed. Final whole-range review found no Critical, Important, or Minor findings. Linux gate equivalence remains Plan 8 evidence.                            |
|   6 | Unslop maintenance across agents                      | completed-awaiting-retirement | [Plan 6](2026-10-01-plan-6-unslop-maintenance.md)                      | `2b7f5fe48` | -   | -      | Added durable cross-agent maintenance guidance, exact pin-aware v1/v2 handling, generic profiles without AOM discovery, and evidence-grounded scenarios. Windows commit gate passed; final whole-range review of `3b39cc051..2b7f5fe48` found no Critical, Important, or Minor findings. Linux/hosted parity remains Plan 8 evidence. |
|   7 | Marketplace migration roadmap                         | complete                      | [Plan 7](2026-10-01-plan-7-marketplace-migration-roadmap.md)           | `a35214719` | -   | -      | Split the tightly coupled consumer migration into independently reviewable subscription, compliance-chain, and retirement slices.                                                                                                                                                                                                     |
|   8 | V2 subscription and repository-owned compliance chain | completed-awaiting-retirement | [Plan 8](2026-10-01-plan-8-v2-subscription-and-owned-compliance.md)    | `534ee8400` | -   | -      | Eight selected standards now use immutable pins and repository-owned certification; active gate checks local structure without semantic overclaims. Full Windows hook passed. Exact-commit hosted Linux evidence remains Plan 11.                                                                                                     |
|   9 | Retire legacy standard deployment machinery           | ready                         | [Plan 9](2026-10-01-plan-9-retire-local-standard-deployment-copies.md) | -           | -   | -      | Remove local deployed copies and byte provenance after the v2 transition; retain only the formatter subtree until Plan 10 removes its live consumers.                                                                                                                                                                                 |
|  10 | Obsolete standard and formatter retirement            | pending                       | Not written yet                                                        | -           | -   | -      | Retire obsolete marketplace standards and formatter/wheel machinery after owner-by-owner dependency review; move useful paragraph guidance to writing-pack.                                                                                                                                                                           |
|  11 | Distribution and adoption closure                     | pending                       | Not written yet                                                        | -           | -   | -      | Isolated install and mixed-subscription pilots, pinned historical authority after refresh, complete Windows/Linux evidence, and migration guidance.                                                                                                                                                                                   |

Readiness ratings are reported in the conversation only; the schema column is intentionally unpopulated. Pending plans are written just in time against the preceding delivered state, not fabricated upfront.

## Delivery boundaries

### Plan 1: standard authority packages

The installed AOM contains the eleven target standard definitions, each owned by a focused skill, plus a coordinator and structural subscription validation. Reading a local Git-pinned definition works independently of the currently installed definition. Neither record validation nor plugin refresh scaffolds consumer files, runs declared commands, upgrades records, or certifies semantics. Existing v1 deployments and this repo's normal gate still work. The new model is usable for understanding and independently authored adoption; no future starter is claimed to exist.

### Plan 2: optional adoption assets

Every asset is attached to its owning standard and classified as definition, optional starter, or plugin-side deployment support. An agent can adopt a single standard into a minimal fixture, initialize root AGENTS when absent, preserve existing authored files, and record certification only after obligations are met. Runbooks/playbooks support arbitrary useful inventories and no required headings. Native Codex/Devin bindings express Git dependencies without a source submodule or `repo.local_skills` declaration. AGENTS and doctrine/contracts adopters receive optional repo-owned checkers that assess declared local policies and disclose semantic limits. REVIEW and CONTRIBUTING can stand alone with inline guidance. No automatic cross-bus registration or dependency resolver.

### Plan 3: command bus

The optional Python bus obeys explicit mode selection, truthful target help, faithful argument/output/status propagation, and meaningful check/apply/dry-run semantics. Agent-led integration works without an import ABI. The command bus can be selected alone and does not imply hook/CI adoption.

### Plan 4: hook/CI and text normalization

The hook starter preserves unrelated work and proves the staged candidate; hosted CI proves its committed counterpart. Required integration services run in both Windows and Linux, and missing prerequisites fail. Normalization prevents platform-driven line/final-newline churn. The hook/CI standard remains usable without command-bus adoption; if both standards are selected, an agent explicitly integrates the hook gate as a bus target. No shared-checkout intent flag obligation survives in either standard.

### Plan 5: artifact custody

Agents discover semantically completed plans without depending on exact keywords, distinguish whole-scope completion from partially finished future work, and promote enduring content before removal. The next substantive slice retires eligible artifacts in its first commit. Existing marker guidance remains useful state recording, not a deletion prerequisite. Update canonical `skills/completing-planning-artifacts/` and any necessary `skills/cleanup-custody/` routes, then regenerate their owning repo-worker-pack projection. Do not turn checkbox counting into an automatic deletion tool.

### Plan 6: unslop

Profiles and observations can coexist in `.agents/unslop/repo.md` or split by class. Subsequent agents can connect distinct incidents, avoid counting duplicate reports as recurrence, and distinguish absent routing from ineffective or ignored guards. Update canonical `skills/unslop-profiles/` and related owning capabilities only where required; keep the standard's management guide usable without ambient Unslop+. No mandatory eight-section schema, skill invocation, reciprocal links, or telemetry service.

### Plan 8 result

The v2 subscription and repository-owned compliance chain landed in `5725b79a7` and `534ee8400`. The Windows hook passed on `534ee8400`; hosted Linux evidence remains unclaimed and is assigned to Plan 11. The repo-owned checker is structural only, while semantic certification is readable and truthfully states its remaining evidence gaps.

### Plans 7-10: explicit Marketplace migration

The current migration surface is coupled across subscription identity, the readable certification, the hook contract, old v1 dispatch, deployed resource provenance, formatter ownership, and many one-time scaffolders. Keep the already-passing hook usable at each commit by migrating one boundary at a time. [Plan 7](2026-10-01-plan-7-marketplace-migration-roadmap.md) records the decomposition and current evidence. Plan 8 establishes the explicit selected set and makes the repository-owned compliance chain authoritative. Plan 9 retires the byte-vendor deployment runtime. Plan 10 retires obsolete standards and formatter machinery after all live owners are identified and migrated. Translate existing selected standards without silently adding command-bus or doctrine/contracts subscriptions merely because facilities exist. Preserve repository-owned standards and documents. Pin new subscriptions to an already published definition commit; do not create a record that must reference its own future commit. Any necessary removal of this repo's actual submodule follows checked ownership and containment, not deletion by name. No migration of Sheg, Wild Bunch, Portfolio, Rooms-Mostly, or Patch in this roadmap.

### Plan 11: closure

Run product-level adoption fixtures from an isolated generated plugin, not source checkout convenience paths. Cover one-standard adoption, independent and combined books, edited starters, no ambient capabilities, current-plugin refresh with older subscription authority, failure without silent recertification, and cross-platform gate equivalence. Reconcile source documentation and generated metadata, obtain fresh whole-change review, and publish only when authorized. Hosted evidence must identify the tested commit; local Windows evidence must prove the same logical gate. Do not describe unexecuted tests or documentation-only harness support as runtime proof.

## Epic constraints

- Canonical changes belong in `skills/`, `shared/`, `src/plugin-definitions/`, and owning repository tools. `dist/` is generated.
- Each plan produces a working, independently assessable deliverable. Source changes precede generation. The staged normal commit hook owns the complete repo gate; do not run it redundantly before or after every commit.
- Skills ship useful tests beside source; avoid heading-count, keyword-presence, tautological, and change-detector tests presented as behavior proof.
- No ambient update silently subscribes, migrates, or alarms a repo. Immutable pinned requirements govern assessment.
- No mandatory starter inventory, copied scaffolders, universal module installer, or new exception mechanism.
- Preserve existing future plans. Completing Plan 1 does not complete the overall design or roadmap; the full spec stays live until the overall implementation is done.
- Optional checkers establish only their declared mechanical results. Agent and human review establish semantic certification.
- No implementation, source changes, external publication, or consumer migration is authorized by this planning task alone.

## Handoff notes

- The human approved the full specification and requested planning in the same worktree, then confirmed a roadmap may be appropriate.
- Plan 1 introduces the new authority model alongside the current deployment runtime. This bridge avoids making the repo gate unbuildable before the later migration plan.
- Eleven target standards result from consolidating two plugin entries, retiring Markdown/gitignore entries, and adding command bus and agent doctrine/contracts.
- Later plans may be re-sliced if source inspection exposes coupling, but must retain every approved requirement and report changed delivery boundaries.
