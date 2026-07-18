# MARK-336 final-review fix report

## Status

GREEN for the bounded follow-up review wave: the guide/helper corrections are
verified, and the controller-orchestrated fresh-context evidence is recorded
in the structured pressure campaign.
The earlier implementation commit
is `cc49e597b87af43baa3003ce13d655189c92984c` on
`harleydbartles/mark-336-add-focused-repository-hygiene-references-to-repo-worker`.
It is published through
[PR #200](https://github.com/HarleyBartles/agent-asset-marketplace/pull/200)
and passed remote Marketplace validation run
[29643154881](https://github.com/HarleyBartles/agent-asset-marketplace/actions/runs/29643154881).

The branch started from current `origin/main` at
`c7e3273410a73376182d994bee1849a973c323c5`; the final-review wave was applied
in the registered linked worktree named in MARK-336. Portfolio was not touched.

## Follow-up review corrections

- Replaced both occurrences of the unsupported
  `generate_index_mesh.py --validate` command in the canonical marketplace
  generation guide with `--check`.
- Added a regression assertion that rejects `--validate` and requires the
  supported check mode.
- Reordered the behavioral Git helper so
  `git rev-parse --show-superproject-working-tree` runs from the supplied start
  path before top-level/common-dir resolution; the new test records and checks
  that call order.
- The focused contract suite is now 22 passed.

## Pressure campaign execution status

The controller-orchestrated evidence is recorded in
`tests/pressure/repo-worker-base/campaign.json`. Its `runtime_results` array
contains exactly 11 fresh Codex subagent contexts: six scenario contexts
(three no-guidance controls and three guided variants) plus five independent
micro-test contexts. Each result preserves its source rollout filename,
judgment, and raw response excerpt for audit. The report makes no claim about
additional repetitions or RED/GREEN/REFACTOR phase execution beyond these
recorded contexts.

## Confirmed blocker resolutions

### 1. Published SDD mesh

The repository's mesh generator uses Git-tracked files and directories as its
source of truth. The chosen contract therefore publishes the generated child
`INDEX.md` instead of suppressing the tracked SDD session directory from the
parent mesh:

- `.agents/superpowers/sdd/.gitignore` keeps ordinary SDD briefs, reports,
  review packages, and other session scratch ignored;
- directory traversal and generated `INDEX.md` files are explicitly unignored;
- this requested final report is explicitly unignored as durable closeout
  evidence;
- the required generated child `INDEX.md` is tracked, and the parent index is
  regenerated from the same tracked-file inventory used in CI.

This preserves intentional session-artifact custody while making every
published mesh edge reproducible in a clean clone. The prior remote failure,
`missing: .agents/superpowers/sdd/2026-07-18-repo-worker-base-hygiene-and-composition/INDEX.md`,
is closed by green run 29643154881.

### 2. Portable worktree algorithm

`worktree-and-branch-policy.md` now derives repository locations only from
Git-anchored commands:

1. reject a non-empty `git -C <start-path> rev-parse
   --show-superproject-working-tree` result;
2. resolve `--show-toplevel` from the actual start path;
3. resolve absolute `--git-common-dir` and `--git-dir` from that checkout;
4. derive the main checkout from `parent(common-git)` and sibling
   `_agent-worktrees` / `_agent-scratch` roots from the main checkout's parent;
5. refuse the shared main checkout by default, allowing the explicit approved
   override only after submodule rejection.

The policy forbids derivation from `Path(__file__)`, the process directory, or
filesystem parent searches. Behavioral tests create real temporary Git
repositories, linked worktrees, nested paths, and a real submodule. They cover
main root, nested main, linked root, nested linked, shared-checkout refusal and
override, and unconditional submodule rejection.

### 3. Guide migration integrity

All moved guide links under `.agents/guides/` were rebased to their actual
targets. The local-link integrity test now parses every moved guide plus the
relevant `.agents` mesh and `AGENTS.md` router surfaces. It also verifies the
declared router targets exist. `.agents/docs/guides/` remains retired.

### 4. Router authority

The router no longer says a repository guide can override the canonical
Superpowers mapping. Local guide authority is limited to repository-specific
paths, commands, exclusions, CI, and exceptions. The mandatory sequence is:

`repo-worker-base -> matching baseline -> local guide -> Superpowers lane`

The focused references use the same non-bypassable authority boundary.

### 5. Worker gates

The original portable worker gates were moved out of the thin `SKILL.md` and
into focused references. They now preserve fresh-main discipline, worktree
verification, branch and PR publication, validation evidence, GREEN criteria,
required return evidence, and stop signs. The sibling worktree and per-branch
scratch contract remains Git-derived and contains no absolute drive
assumption.

### 6. Pressure and retrieval fixtures

The two answer-key-only Markdown files were replaced by
`tests/pressure/repo-worker-base/campaign.json`, validated by pytest and
documented by its README. It contains:

- three combined-pressure scenarios, each with separate no-guidance and guided
  variants;
- explicit RED, GREEN, and REFACTOR evidence fields;
- six micro-test cases;
- a fresh-context execution contract and explicit evidence-shape schema;
- exactly 11 recorded `runtime_results` entries: six scenario contexts and
  five independent micro-test contexts.

### 7. Plan receipts

Delivered plan checkboxes are marked complete only where the corresponding
source, generated output, validation, commit, publication, or remote evidence
exists. The plan also records the corrected Git-anchored algorithm and the
structured pressure-fixture contract.

## TDD and validation evidence

The correction began with a RED contract run:

- `py -3 -m pytest tests/test_repo_worker_base_contract.py -q`
- result before production edits: 5 failed, 15 passed;
- failures mapped to the worktree policy, guide links, router authority,
  published SDD mesh, and pressure fixture.

The final scoped contract is GREEN:

- `py -3 -m pytest tests/test_repo_worker_base_contract.py -q`
- result: 20 passed.

Marketplace regeneration and validation completed successfully:

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 tools/generate_marketplace.py --check`
- `py -3 tools/generate_repo_index.py --check`
- `py -3 tools/generate_pack_manifests.py --check`
- `py -3 tools/materialize_projection.py --check`
- `py -3 tools/generate_index_mesh.py --check`
- `py -3 tools/validate_generated_drift.py --base origin/main`
- `git diff --check`

Both marketplace projections and both repo-worker-base zip artifacts contain
`SKILL.md`, `agents/openai.yaml`, and all ten references. A source/test import
sweep found no runtime dependency on installed skill trees or user caches.

The broader listed pytest command completed with 42 passes and two failures in
`tests/test_generator_check_modes.py`. Those failures are unchanged outside
this fix wave: one test patches the removed
`SOURCE_DECISIONS_JSON_PATH` attribute, and one expects the old
`validate_generated_drift` call shape without
`skip_content_validation=False`. No files involved in those two expectations
differ from `origin/main`; they are reported here rather than broadened into
MARK-336.

## Publication evidence

- PR: https://github.com/HarleyBartles/agent-asset-marketplace/pull/200
- implementation commit: `cc49e597b87af43baa3003ce13d655189c92984c`
- remote workflow: Marketplace validation run 29643154881
- remote job: marketplace-validation 88076870584
- result: success, including the previously failing Marketplace check step
- merge target: `main`

The report/plan evidence commit is intentionally separate from the
implementation commit. Its current-head remote check and the synchronized PR
body and MARK-336 evidence are external closeout proof, avoiding a
self-referential commit SHA inside this tracked report.

## Concerns and follow-up

- The two pre-existing generator-check unit-test failures remain visible and
  are not caused by this branch.
- GitHub emitted a Node.js 20 deprecation annotation for upstream
  `actions/checkout@v4` and `actions/setup-python@v5`; it did not affect the
  successful workflow.
- The controller-supplied pressure evidence is recorded in the checked-in
  fixture; no additional repetitions or RED/GREEN/REFACTOR phase execution is
  inferred beyond those 11 results.
- MARK-337 and any Portfolio refresh remain outside this bounded fix wave.
