# AOM Standard Adoption and Shipping Roadmap

**Status:** In flight, planning only. Execution requires review of the applicable plan.

**Design authority:** [Approved specification](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), approved by the human on 2026-09-30; recorded in commit `c380a60e8`.

**Workspace:** `Z:/_agent-worktrees/agent-asset-marketplace/codex/open-runbook-playbook-composition`, branch `codex/open-runbook-playbook-composition`. Continue this planning slice here. Do not switch the primary checkout or discard existing future plans.

## Goal

Ship AOM as independently selectable standard skills with immutable source authority, repository-owned implementation, continuing self-certification, effective routing, and explicit agent-led adoption. Reconcile this Marketplace's own implementation after the new capabilities exist. Other repositories remain untouched unless separately authorized.

## Sequence

|   # | Title                                                     | Status  | Plan File                                         | Commit | PR  | Rating | Notes                                                                                                                                                                                      |
| --: | --------------------------------------------------------- | ------- | ------------------------------------------------- | ------ | --- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|   1 | Standard authority packages and subscription records      | ready   | [Plan 1](2026-09-30-plan-1-standard-authority.md) | -      | -   | -      | Ship all agreed definitions, the subscription contract, pinned local-source reading, and coordination guidance. Preserve current consumer runtime until explicit migration.                |
|   2 | Optional adoption assets and document compliance          | pending | Not written yet                                   | -      | -   | -      | Agent-guided adoption, root entrypoint, selected starters, native plugin bindings, AGENTS/doctrine checks, independent book adoption, REVIEW and CONTRIBUTING.                             |
|   3 | Portable command bus and complete hook/CI gate            | pending | Not written yet                                   | -      | -   | -      | Language-independent CLI contract, Python starter, hook candidate snapshot, Windows/Linux parity, infrastructure requirements, and text normalization.                                     |
|   4 | Semantic planning-artifact custody                        | pending | Not written yet                                   | -      | -   | -      | Replace exact-marker-only discovery, preserve future work, route mandatory next-slice retirement only where adopted, and reconcile worker capability guidance.                             |
|   5 | Unslop maintenance across agents                          | pending | Not written yet                                   | -      | -   | -      | Effective profile routing, durable occurrence records, scalable repo.md format, dynamic management, and ambient-capability-independent fallback.                                           |
|   6 | Marketplace adoption and retirement of obsolete machinery | pending | Not written yet                                   | -      | -   | -      | Explicitly select this repo's subscriptions, certify its owned implementation, retire copied scaffolders/provenance checks and obsolete standards, move Markdown guidance to writing-pack. |
|   7 | Distribution and adoption closure                         | pending | Not written yet                                   | -      | -   | -      | Isolated install and mixed-subscription pilots, pinned historical authority after refresh, complete Windows/Linux evidence, and migration guidance.                                        |

Readiness ratings are reported in the conversation only; the schema column is intentionally unpopulated. Pending plans are written just in time against the preceding delivered state, not fabricated upfront.

## Delivery boundaries

### Plan 1: standard authority packages

The installed AOM contains the eleven target standard definitions, each owned by a focused skill, plus a coordinator and structural subscription validation. Reading a local Git-pinned definition works independently of the currently installed definition. Neither record validation nor plugin refresh scaffolds consumer files, runs declared commands, upgrades records, or certifies semantics. Existing v1 deployments and this repo's normal gate still work. The new model is usable for understanding and independently authored adoption; no future starter is claimed to exist.

### Plan 2: optional adoption assets

Every asset is attached to its owning standard and classified as definition, optional starter, or plugin-side deployment support. An agent can adopt a single standard into a minimal fixture, initialize root AGENTS when absent, preserve existing authored files, and record certification only after obligations are met. Runbooks/playbooks support arbitrary useful inventories and no required headings. Native Codex/Devin bindings express Git dependencies without a source submodule or `repo.local_skills` declaration. AGENTS and doctrine/contracts adopters receive optional repo-owned checkers that assess declared local policies and disclose semantic limits. REVIEW and CONTRIBUTING can stand alone with inline guidance. No automatic cross-bus registration or dependency resolver.

### Plan 3: bus and hook/CI

The optional Python bus obeys explicit mode selection, truthful target help, faithful argument/output/status propagation, and meaningful check/apply/dry-run semantics. Agent-led integration works without an import ABI. The hook starter preserves unrelated work and proves the committed candidate; hosted CI proves its counterpart. Required integration services run in both Windows and Linux, and missing prerequisites fail. Normalization prevents platform-driven line/final-newline churn. No shared-checkout intent flag obligation survives in the new bus or hook standard.

### Plan 4: artifact custody

Agents discover semantically completed plans without depending on exact keywords, distinguish whole-scope completion from partially finished future work, and promote enduring content before removal. The next substantive slice retires eligible artifacts in its first commit. Existing marker guidance remains useful state recording, not a deletion prerequisite. Update canonical `skills/completing-planning-artifacts/` and any necessary `skills/cleanup-custody/` routes, then regenerate their owning repo-worker-pack projection. Do not turn checkbox counting into an automatic deletion tool.

### Plan 5: unslop

Profiles and observations can coexist in `.agents/unslop/repo.md` or split by class. Subsequent agents can connect distinct incidents, avoid counting duplicate reports as recurrence, and distinguish absent routing from ineffective or ignored guards. Update canonical `skills/unslop-profiles/` and related owning capabilities only where required; keep the standard's management guide usable without ambient Unslop+. No mandatory eight-section schema, skill invocation, reciprocal links, or telemetry service.

### Plan 6: explicit Marketplace migration

Before drafting this plan, present the proposed repo subscription set for review. Translate existing selected standards without silently adding command-bus or doctrine/contracts subscriptions merely because facilities exist. Preserve repository-owned standards and documents. Pin new subscriptions to an already published definition commit; do not create a record that must reference its own future commit. Replace steady-state vendor-byte enforcement with the repo's actual compliance chain and readable certification. Retire the old exception record, stale SDD standard, source-submodule installation requirement, copied one-time scaffolders, and superseded composition obligations. Remove formatter/wheel machinery only after identifying retained owners; adopt writing-pack paragraph guidance. Any necessary removal of this repo's actual submodule follows checked ownership and containment, not deletion by name. No migration of Sheg, Wild Bunch, Portfolio, Rooms-Mostly, or Patch in this roadmap.

### Plan 7: closure

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
