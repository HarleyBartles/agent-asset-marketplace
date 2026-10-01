# Hook, CI, and Text Normalization Standard Assets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship useful optional hook, normalization, hosted-gate, and command-bus integration starters for repositories that adopt the tracked hook and CI standard.

**Architecture:** Keep the standard's pledge independent from its optional assets: adopters own one complete Windows pre-commit and Linux hosted gate, the canonical validation path, candidate-state handling, and normalization policy. AOM provides a Bash hook seed, a portable Python text normalizer, policy examples, and a copyable bus-target example; every artifact is adapted by an agent and then becomes repository-owned. The hook seed exposes explicit repository-owned apply/check integration functions that fail closed until filled in, so it does not impose a command manifest, a command bus, or another standard.

**Tech Stack:** Bash for the Git hook entrypoint, Python standard library for portable file normalization and the optional bus-target example, GitHub Actions YAML as one hosted-CI example, pytest and Git Bash for behavior tests, existing Marketplace builder.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), especially sections 4.2, 5.1, 6.6, and 6.7.

**Roadmap:** [AOM adoption and shipping](roadmap.md), Plan 4. Planning baseline is Plan 3 closeout commit `9d2e56fd4`; implementation baseline is Plan 3 reviewed head `6f8862e2d`.

**Execution Strategy:** `executing-plans`, because normalization, candidate-snapshot orchestration, and bus/hosted examples are sequential parts of one deployable standard bundle. The normalizer's behavior informs the hook integration, and the isolated adoption proof must exercise the generated package after all assets are assembled. Parallel task execution would create competing changes to the same skill and overlapping end-to-end fixtures.

## Global Constraints

- The adopted pledge requires a tracked pre-commit hook and hosted CI to run the same complete repository gate, with Windows local and Linux hosted execution, equivalent checks and failure criteria, and no hook skipping by agents.
- The hook evaluates the exact commit candidate, includes any hook-side normalization or generation in that candidate, validates it, and preserves unrelated unstaged and untracked work. Hosted CI evaluates the committed counterpart.
- Required infrastructure must exist on both platforms. Missing prerequisites fail clearly; no checks are deferred exclusively to hosted CI or omitted locally.
- Normalize repository-declared line endings and final-newline conventions, including generated/formatted text. Repositories own file scope, conventions, hook, validation path, and drift controls.
- Command bus remains optional. If adopted, its CLI contract remains authoritative; the hook/CI standard can provide a target example for explicit agent integration. No automatic install, target discovery, module ABI, shared command JSON, or source submodule.
- AOM assets are optional and repository-owned after copying. The hook seed's integration points fail closed until adapted. No asset may imply the adopter is certified merely because it was copied.
- Use Python for portable logic and Bash only for the Git hook/hosted shell boundary. Do not ship parallel PowerShell and shell copies of Python behavior.
- Do not carry forward the retired shared-checkout mutation-intent flag obligation.
- Do not migrate this Marketplace's existing tracked hook, workflow, `.gitattributes`, or old `.agents/standards/tracked-validation-hook` machinery in this plan. Marketplace subscription migration and retirement remain Plan 7.
- Edit canonical skill assets first, regenerate `dist/`, run focused tests, and rely on the normal commit hook for the complete repository gate. Do not redundantly run the full gate before or after a successful hooked commit.

## Review Focus

- A staged change with unrelated unstaged edits must validate only the staged candidate, then restore the unrelated edits byte-for-byte; Task 2 uses a temporary Git repository to prove both states.
- Hook normalization that changes a staged file must be included in the candidate and checked after application; Task 2 asserts the resulting index tree and final check result.
- The hosted example must invoke the same tracked hook/gate against the checked-out commit and fail on a dirty or mismatched candidate; Task 3 checks the workflow text and the hook's hosted mode behavior.
- The optional bus-target example must meet command-bus help/mode/output/exit expectations without being required by the hook or standard; Task 3 tests its standalone CLI and the no-bus adoption probe.
- The normalizer must never corrupt binary, undecodable, or unselected files; Task 1 covers these cases and ensures check mode is read-only.

## File and Interface Map

| Owner                       | Deliverable                                                                                                                                                |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills/tracked-repo-hooks` | Optional Bash candidate hook, Python normalizer, normalization examples, hosted workflow example, copyable bus-target example, and behavior/adoption tests |
| `tests/shipping`            | Isolated generated-package execution proof and standard-asset closure checks                                                                               |
| Generated AOM plugin        | `dist/plugins/agent-operating-model/skills/tracked-repo-hooks/` projection only                                                                            |

## Task 1: Portable text normalization starter

**Files:** Add `skills/tracked-repo-hooks/assets/normalization/normalize_text.py`, `skills/tracked-repo-hooks/assets/normalization/gitattributes.example`, and `skills/tracked-repo-hooks/tests/assets/test_normalize_text.py`.

**Consumes:** Standard normalization obligations in spec section 6.6 and the tracked hook standard.

**Produces:** A standard-library-only normalizer that operates on explicitly supplied paths, supports `--check` and `--apply`, and applies a caller-selected line-ending and final-newline policy without repository-wide guessing.

- [x] Write behavior tests for LF and CRLF conversion, bare-CR normalization, required final newline, check-mode drift reporting, apply-mode convergence, repeated apply idempotence, and paths with spaces.
- [x] Add refusal tests for missing paths, binary/NUL content, and undecodable content; verify check mode does not change file bytes and apply mode does not alter rejected or unselected paths.
- [x] Implement explicit `--check`/`--apply`, `--line-ending {lf,crlf}`, `--final-newline {ensure,forbid}`, and one-or-more path arguments. Preserve an existing UTF-8 BOM, normalize only selected UTF-8 text, and fail clearly rather than guessing on unsupported content.
- [x] Add `gitattributes.example` with a declared text/EOL policy and binary override; label it as an editable example, not a mandatory global configuration.
- [x] Run the focused normalizer suite and Ruff; confirm only standard-library runtime imports. Six behavior tests pass; source and generated normalization asset hashes match.

Run: `py -3 -m pytest -q skills/tracked-repo-hooks/tests/assets/test_normalize_text.py` and `py -3 -m ruff check skills/tracked-repo-hooks/assets/normalization skills/tracked-repo-hooks/tests/assets/test_normalize_text.py`.

**Exit:** A repo can copy or replace the normalizer, explicitly select its text surface and policy, and use the same Python behavior on Windows and Linux.

## Task 2: Candidate-snapshot hook starter

**Files:** Add `skills/tracked-repo-hooks/assets/hooks/pre-commit` and `skills/tracked-repo-hooks/tests/assets/test_pre_commit_starter.py`.

**Consumes:** Task 1 normalizer and repository-owned hook/gate requirements in spec section 6.6.

**Produces:** A portable Bash hook seed that protects the staged candidate while allowing the adopter to wire its own canonical apply and check commands.

- [ ] Create a temporary-repository integration harness using Git Bash. Locate Bash on `PATH` or beside the installed Git for Windows; fail with a clear prerequisite message if neither exists. Cover staged and unstaged edits to the same file, unrelated unstaged edits, untracked files, filenames with spaces, and an apply operation that changes a staged candidate path.
- [ ] Implement the hook's candidate lifecycle: identify staged paths, preserve unstaged/untracked state, materialize the index candidate, invoke apply then check integration functions, stage only allowed candidate updates, verify the final check ran on the resulting candidate, and restore the developer's remaining work on success and failure.
- [ ] Make both repository integration functions fail closed with a clear message until the adopter replaces them. Keep their command choices local to the copied hook; do not add a universal command declaration or assume a command bus.
- [ ] Add a hosted mode that requires a clean detached checkout of the declared commit and proves the gate leaves its committed tree unchanged. Reject dirty hosted state and command failures clearly.
- [ ] Assert candidate tree identity, hook exit status, and restoration of index/worktree/untracked files after success and apply/check callback failures. If restoration itself fails, report the exact recovery location and fail nonzero; do not make an OS-level restore failure a required test case.
- [ ] Run the integration suite under Windows Git Bash and ensure it uses ordinary Bash features available to the hosted Linux example. Do not include OS-specific copies of the same algorithm.

Run: `py -3 -m pytest -q skills/tracked-repo-hooks/tests/assets/test_pre_commit_starter.py` from PowerShell with the installed Git Bash available.

**Exit:** The starter demonstrates safe candidate assessment but remains unusable until a repo-owned apply/check integration is supplied.

## Task 3: Hosted parity example and optional command-bus target

**Files:** Add `skills/tracked-repo-hooks/assets/workflows/github-actions-hosted-gate.yml`, `skills/tracked-repo-hooks/assets/targets/repository_gate.py`, `skills/tracked-repo-hooks/tests/assets/test_bus_target.py`, and `skills/tracked-repo-hooks/tests/assets/test_hosted_workflow.py`.

**Consumes:** Task 2 hook CLI and Task 1 normalizer behavior.

**Produces:** One concrete Linux hosted-CI example that invokes the same tracked hook, plus a separately deployable example for a repository that has also adopted command-bus.

- [ ] Add a hosted workflow example that checks out a proposed commit, provides declared prerequisites, uses a detached clean checkout, and invokes the same hook in hosted mode. Keep provider-specific workflow material clearly marked as optional.
- [ ] Write tests that assert the example invokes the tracked hook in hosted mode for the checked-out commit, does not substitute a narrower workflow-only check, and requires no ambient AOM checkout at runtime. The hook's repository-owned check callback remains the single complete gate.
- [ ] Add a small Python command-bus target example with truthful `--help`, a meaningful `--check` path, explicit supported-mode metadata/instructions, and exact subprocess exit/output propagation. The adopter manually copies and registers or adapts it; it must not install itself or scan for a bus.
- [ ] Prove the bus-target example can be run independently after copying and that command-bus is not required to use the hook starter or hosted example.
- [ ] Document that the sample target is optional, conforms to the command-bus interface when registered, and creates no shared module ABI or command configuration contract.

Run: `py -3 -m pytest -q skills/tracked-repo-hooks/tests/assets/test_bus_target.py skills/tracked-repo-hooks/tests/assets/test_hosted_workflow.py`.

**Exit:** Repositories can use the hook standard with or without command-bus adoption; hosted CI and the Windows hook share the same gate semantics.

## Task 4: Adoption guidance and isolated package proof

**Files:** Update `skills/tracked-repo-hooks/SKILL.md` and `references/standard.md`; add `skills/tracked-repo-hooks/tests/evaluator-only/adoption-scenarios.md` and `tests/shipping/test_aom_tracked_repo_hooks_assets.py`; update generated AOM package.

**Consumes:** Tasks 1-3.

**Produces:** Clear adoption instructions and evidence that optional assets can be copied and adapted without a Marketplace runtime dependency or implied command-bus subscription.

- [ ] Explain the required pledge, repository-owned self-certification, root `AGENTS.md` route, distinction between mandatory invariants and optional assets, explicit Windows/Linux verification, and agent no-skip responsibility.
- [ ] Describe the normalizer's limited file scope and the hook seed's fail-closed integration points; do not suggest that template presence establishes conformance.
- [ ] Add fresh-context scenarios for hook/CI adoption without command bus, adoption with a command bus and optional target module, and an existing repo whose current gate already conforms. Expected decisions must follow the standard, not exact response wording.
- [ ] Copy the generated skill package to an isolated install, copy selected hook/normalizer assets into a temporary consumer, remove Marketplace `PYTHONPATH`, and execute the normalizer, hook behavior harness, and optional bus target from that consumer.
- [ ] Verify internal package links, canonical-to-generated byte parity, evaluator-only exclusion, and that the isolated runtime needs no AOM source checkout.
- [ ] Add `tracked-repo-hooks` to the general AOM standard asset package checks and run the focused asset suites.
- [ ] Run the complete local Windows behavior suite for the new assets, regenerate with `py -3 tools/run.py marketplace --apply`, and inspect source/generated parity. Record that actual hosted Linux execution is deferred to roadmap closure unless a hosted run occurs in this slice.

Run: `py -3 -m pytest -q skills/tracked-repo-hooks/tests/assets tests/shipping/test_aom_tracked_repo_hooks_assets.py tests/shipping/test_aom_standard_assets.py`.

**Exit:** A repo can choose which starter pieces help, implement its own conformance, and certify only after the full Windows/Linux pledge is demonstrably met.

## Task 5: Commit, review, and closeout

**Files:** Task 1-4 canonical source, tests, evaluator-only scenarios, and generated plugin projection.

**Consumes:** Passing focused behavior evidence and adoption scenarios.

**Produces:** Reviewed optional hook/CI starter assets with package-local authority and no implicit command-bus dependency.

- [ ] Inspect staged paths and generated/source parity; commit through the normal hook. Do not rerun the full gate redundantly after a successful hooked commit.
- [ ] Obtain a fresh whole-range review against this plan and the approved spec. Fix Critical and Important findings, regenerate outputs, rerun focused evidence, and get a fresh review after each correction.
- [ ] Mark this plan `completed-awaiting-retirement`; update the roadmap row with implementation head and review outcome.

**Exit:** The tracked hook/CI standard has useful optional deployment support, while repository-owned gate policy and certification remain with each adopting repo.

## Handoff boundaries

- This plan ships optional standard assets only. It does not adopt hook/CI into the Marketplace repo, change its own active Git hook or hosted workflow, or retire `.agents/standards/tracked-validation-hook` machinery.
- No changes to other repositories are in scope.
- Later Marketplace migration explicitly chooses subscriptions and retires old scaffolder copies only after replacement behavior and tests are proven.
- Roadmap Plan 8 remains responsible for end-to-end cross-platform CI proof; a local Windows run or workflow-text test is not hosted Linux evidence.
