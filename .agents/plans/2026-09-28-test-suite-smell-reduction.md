# Test Suite Smell Reduction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce brittle, obsolete, sprawling, and poorly grouped tests while preserving meaningful behavioral coverage.

**Status:** `completed-awaiting-retirement`

**Architecture:** Treat the current test tree as the evidence base. First classify suspected smells against the live production behavior and test history, then make narrow contract-level corrections and split only oversized files along coherent behavior ownership. Do not delete a test solely because it was written during TDD or its implementation has since integrated; removal requires proving another current test covers the same behavior or that the assertion protects no supported contract.

**Tech Stack:** Python 3, pytest, Git history, repository CI runner.

**Spec:** The read-only test audit in the preceding task; concrete leads are `tests/test_workflow_contracts.py`, `tests/test_repo_standards.py`, `tests/test_markdown_format.py`, and `tests/test_executing_plans_scripts.py`. Reconfirm every cited observation against the implementation branch before editing.

**Execution Strategy:** `executing-plans` - the tasks depend on one shared classification and coverage map, and splitting suites plus changing assertions should be reviewed as one coherent test-ownership change. Parallel workers would duplicate history and coverage analysis.

## Global Constraints

- Keep changes limited to tests and their test index or organization metadata; change production behavior only if investigation proves a test exposes a real defect and the human authorizes that scope.
- Do not add tautological or change-detector tests.
- Do not retain a test merely to preserve the history of an implementation step.
- Do not delete behavior coverage without identifying its replacement or proving the tested behavior is unsupported.
- Preserve meaningful portable behavior checks across Windows and Linux.
- Keep test names and module boundaries aligned with behavior under test; avoid splitting one behavior across many tiny files.
- Use `py -3 -m pytest <focused-file-or-node> -v` for focused checks. For uncommitted verification use `py -3 tools/run.py ci --check`; normal commit validation is owned by the tracked pre-commit hook.

## Review Focus

- A provenance assertion tied to one historical commit fails after a valid upstream update: assert the durable provenance relationship and format instead.
- A test asserts source fragments while runtime behavior is the actual contract: exercise the command or output where practical; retain source-shape checks only for explicit structural contracts.
- A large test module mixes unrelated behavior: split by domain ownership without changing test semantics or multiplying helper layers.
- An apparent TDD/history duplicate may protect a distinct edge case: use history and call-path/coverage mapping before removing it.

______________________________________________________________________

### Task 1: Build an evidence-backed smell and coverage inventory

**Files:**

- Inspect: `tests/test_workflow_contracts.py`
- Inspect: `tests/test_repo_standards.py`
- Inspect: `tests/test_markdown_format.py`
- Inspect: `tests/test_executing_plans_scripts.py`
- Inspect: production modules and Git history for each candidate assertion
- Modify: none in this task

**Interfaces:**

- Produces: a task-local map of each candidate test to its observable contract, production owner, and current replacement/unique coverage.

- [x] Identify exact candidate tests for tautology, change detection, integrated-implementation residue, TDD duplication, source-text coupling, and mixed-concern modules.

- [x] For each candidate, inspect the current production behavior and relevant `git log`/`git blame`; classify as keep, rewrite, relocate, or remove, with evidence and replacement coverage recorded.

- [x] Treat the duplicated upstream hash checks as one candidate; repository inspection confirmed `SOURCE.md` deliberately pins the active upstream comparison revision. Preserve the primary version/provenance pin and remove its repeated assertion from the separate custody test.

- [x] Compare candidate behavior coverage before proposing deletion. Do not infer redundancy from similar test names or adjacent commits.

- [x] Proceed only with candidates whose classification is supported by current code and history; record unresolved cases for retention.

### Task 2: Replace brittle source and historical pins with contract assertions

**Files:**

- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_markdown_format.py`
- Modify: `tests/test_executing_plans_scripts.py`
- Modify production tests only where Task 1 identifies a genuine behavioral boundary.

**Interfaces:**

- Consumes: Task 1 candidate inventory.

- Produces: assertions that check stable provenance/CLI/output contracts rather than incidental exact source text, where the behavior can be observed externally.

- [x] Keep the single exact SHA assertion because the active upstream comparison pin is an intentional provenance contract; remove the duplicate SHA assertion from the custody test.

- [x] Remove two negative checks for retired private formatter helper names; retain the canonical dependency, formatter package, and declared command assertions. The other inspected source checks protect explicit routing/portability structure or already have behavioral companions.

- [x] Retain source-level checks only where structure is an explicit contract, including scoped Markdown producer routing and portable shell-helper dispatch.

- [x] Do not create a generic test framework or add cases that simply restate implementation branches without protecting an observable contract.

### Task 3: Split oversized test modules by coherent behavior ownership

**Files:**

- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_repo_standards.py`
- Modify: `tests/INDEX.md` only if the repository index generator does not already update it through the normal gate.

**Interfaces:**

- Consumes: Task 1 module map and Task 2 assertion changes.

- Produces: focused test modules with behavior-based names and shared helpers only where they eliminate genuine duplication.

- [x] Partition `test_workflow_contracts.py` into authority, validation, planning, repository/pressure, and evaluation-campaign modules; keep the pressure-repair test with repository/pressure contracts. Preserve all test bodies except the duplicate pin removal.

- [x] Partition `test_repo_standards.py` into standards/scaffolding, hook/staged-snapshot, and composition-graph modules; keep coupled hook integration scenarios together.

- [x] Move module-local fixtures/helpers with their primary consumers; promote a helper only when at least two new modules need identical setup and the shared location is clear.

- [x] Preserve test IDs where practical and update imports/index generation through the repository-owned mechanism.

- [x] Review each resulting module for grab-bag concerns and avoid splitting merely to hit an arbitrary line-count target.

### Task 4: Remove only proven dead or redundant tests and verify the final suite

**Files:**

- Modify: only test files identified by Task 1 as safely removable or consolidatable.

**Interfaces:**

- Consumes: Task 1 coverage map and Tasks 2-3 changes.

- Produces: a smaller or better-owned suite with no unexplained coverage loss.

- [x] Remove only proven cruft: one duplicate SHA assertion and two negative assertions on retired private formatter names. No behavior tests were removed; the active provenance pin and unique behavior coverage remain.

- [x] Keep tests added around integrated implementation when they still protect a distinct user-visible or repository contract.

- [x] Run the focused affected suite: 188 passed, 1 platform skip; after review fixes the repo standards suite passed 93 tests and both extracted modules collected independently. Final provenance/formatter checks: 3 passed.

- [x] Verify the generated test index and the test inventory. Ruling: repository `AGENTS.md` directs normal commits through the tracked pre-commit hook and prohibits a separate `ci --check` immediately before or after that hooked commit; use the hook as the complete gate.

- [x] Self-review the complete diff against Task 1's candidate map; confirm no production file changed without newly established defect scope.
