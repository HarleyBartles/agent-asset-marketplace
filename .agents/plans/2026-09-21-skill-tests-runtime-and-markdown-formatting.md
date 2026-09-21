# Skill Tests, Helper Runtime, and Markdown Formatting Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to continue this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the completed skill-test, helper-runtime, and Markdown foundation work in PR #328, then replace its repository-local formatter with a portable, explicitly adopted and enforced operating-model capability.

**Architecture:** A canonical `agent-operating-model/markdown-formatting` skill owns pinned formatter dependencies, contract parsing, tracked-file selection, atomic check/apply mechanics, and producer-scoped checking. `repo-shape` owns the optional named surface and its explicit adopted/enforced transitions; the consumer owns its contract, exclusions, dependency integration, and ordered command declaration. This repository migrates its local implementation to the installed skill, binds Markdown producers to check their own output, regenerates projections, and validates through the tracked staged-snapshot hook.

**Tech Stack:** Python 3, pytest, Git, JSON contracts, TOML, `mdformat==1.0.0`, `mdformat-gfm==1.0.0`, `mdformat-frontmatter==2.1.2`, Markdown skills and doctrine.

**Spec:** `.agents/specs/2026-09-21-skill-tests-runtime-and-markdown-formatting-design.md`

**Execution Strategy:** `executing-plans` — the user selected inline implementation, the remaining tasks share command-contract and consumer-migration state, and one fresh whole-branch review will gate completion.

**State:** completed-awaiting-retirement

## Global Constraints

- Preserve all completed PR #328 work and its commit history; do not fold the deferred receiving-code-review deeper-smell change into this plan.
- Edit canonical plugin sources under `codex-marketplace/plugins/`; generated `.agents/skills/`, manifests, indexes, and mesh files are refreshed outputs only.
- The capability is opt-in. Plugin install or refresh must not create policy, install dependencies, reformat Markdown, or enable enforcement.
- The skill owns exact formatter pins; each consumer owns how those requirements enter its environment.
- Core conformance is `wrap = "no"`, `end_of_line = "lf"`, `validate = true`, with `gfm` and `frontmatter` extensions.
- Exclusions name one explicit repository-relative `file` or `tree`, never a glob, and each carries its own non-empty custody reason.
- Every tracked Markdown file, including generated output, is eligible unless a valid exclusion proves its bytes must not change.
- `adopted` and `enforced` are separate human decisions. Adoption causes no formatting or gate change; enforcement applies the full migration before binding check/apply into canonical commands.
- Hooks do not install dependencies or use network-backed ephemeral execution.
- Generators must emit formatter-clean Markdown, run producer-scoped check before success, and remain stable across a second generation.

## Review Focus

- Apply must restore all original bytes if configuration, dependency, contract, or formatter validation fails; Task 6 tests late-batch failure rollback.
- Exclusions that escape the repository, use globs, mismatch their kind, or match zero tracked Markdown fail in check and apply; Task 6 tests each class.
- `adopted` must not alter command gates or Markdown, while `enforced` must normalize before command composition changes; Task 7 tests both transitions.
- Legacy single-vector command declarations must remain valid while ordered multi-command declarations support enforced surfaces; Task 7 tests compatibility and hook order.
- A generator that emits drift must fail at its own boundary and a second run must be clean; Task 9 tests aggregate producer owners.

______________________________________________________________________

### Task 1: Retire the predecessor plan and establish the approved design

**Files:** repository planning/specification surfaces and generated mesh.

**Interfaces:** Produces the approved scope and historical basis for this plan.

- [x] **Step 1: Retire the preceding completed semantic-authority plan** — commit `20321f211`.
- [x] **Step 2: Design and clarify the deeper-smell fixture before scope split** — commits `f12336d19`, `62937eae2`, and `fba0bb5ae`.
- [x] **Step 3: Split the approved specifications so PR #328 excludes deeper-smell implementation** — commit `5507b73f6`.

### Task 2: Harden executing-plan helper runtime resolution

**Files:** canonical executing-plan helpers, tests, and installed projections.

**Interfaces:** Produces an explicit Python fallback ladder and same-environment Bash guard used by later workflow execution.

- [x] **Step 1: Replace the brittle single-launcher assumption with concrete executable resolution.**
- [x] **Step 2: Make callers responsible for proving Bash belongs to the repository's current environment and fail diagnostically across an environment boundary.**
- [x] **Step 3: Run focused and hooked validation and commit** — `deda85ed5`.

### Task 3: Standardize skill-test custody

**Files:** skill standards doctrine/contract, affected canonical skill trees, tests, and installed projections.

**Interfaces:** Produces optional skill-root `tests/` custody and preserves behavioral resources outside it.

- [x] **Step 1: Inventory and move maintainer-only test material by meaning into each skill's root `tests/` lane** — `bceb66411`.
- [x] **Step 2: Add the sibling skill-test custody contract and state that skills are code, code ships tests, and neither ships test results** — `653854d0c`.
- [x] **Step 3: Remove the stale local-skill prefix requirement and preserve arbitrary registered local names.**

### Task 4: Establish repository-local Markdown normalization

**Files:** `.mdformat.toml`, root dependencies, `tools/run.py`, Markdown tests, index generator, exclusions, and normalized tracked Markdown.

**Interfaces:** Produces a working local reference implementation to migrate in Tasks 6-9.

- [x] **Step 1: Pin mdformat plus GFM/frontmatter support and configure no hard wrapping, LF, and validation.**
- [x] **Step 2: Enumerate eligible tracked Markdown through Git, preserve frontmatter semantics, and protect only byte-governed authority evidence plus the invalid scaffold template.**
- [x] **Step 3: Normalize all eligible tracked Markdown and make generated indexes converge** — `e0ca90696`.

### Task 5: Split the implementation plans at the PR boundary

**Files:**

- Modify: `.agents/plans/2026-09-21-receiving-code-review-deeper-smell-and-skill-tests.md`
- Create: `.agents/plans/2026-09-21-skill-tests-runtime-and-markdown-formatting.md`

**Interfaces:** Produces a deferred plan matching the deeper-smell spec and this executable mid-flight PR plan.

- [x] **Step 1: Remove completed test-custody work from the deeper-smell plan and leave its fixture, RED, guidance, GREEN, and publication sequence intact.**
- [x] **Step 2: Record completed PR #328 work and the remaining portable Markdown tasks in this plan.**
- [x] **Step 3: Regenerate the plan index and commit the split in this planning commit**

Run:

```powershell
py -3 tools/run.py mesh --apply
git add .agents/plans .agents/specs .agents/**/INDEX.md .agents/**/INDEX.json
git commit -m "docs: separate markdown implementation plan"
```

Expected: the tracked hook passes; this plan becomes the only active plan for PR #328; the deferred plan remains paired with its standalone spec.

### Task 6: Build the portable Markdown-formatting skill

**Files:**

- Create: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/SKILL.md`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/requirements.txt`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/scripts/format_markdown.py`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/references/markdown-formatting-contract.schema.json`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/tests/test_format_markdown.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/references/bundle-manifest.json` only if the repository generator does not own registration automatically.

**Interfaces:**

- Consumes: repo root discovered by `git rev-parse --show-toplevel`, `.mdformat.toml`, `.agents/contracts/markdown-formatting.json`, and skill-owned exact requirements.

- Produces: `MarkdownContract(state: Literal["adopted", "enforced"], exclusions: tuple[Exclusion, ...])`, `Exclusion(kind: Literal["file", "tree"], path: PurePosixPath, reason: str)`, `load_contract(Path) -> MarkdownContract`, `eligible_markdown(Path, MarkdownContract) -> tuple[Path, ...]`, `verify_toolchain() -> None`, `run_formatter(Path, Sequence[Path], mode: Literal["check", "apply"]) -> None`, and CLI modes `--check`, `--apply`, and `--check-files PATH [PATH ...]`.

- `--check-files` is non-mutating, accepts explicit repository-relative Markdown outputs, rejects paths outside the repository, and uses the same configuration and pins as repository-wide modes.

- [x] **Step 1: Write failing contract and selection tests**

Use a neutral temporary Git repository. Test tracked versus untracked Markdown, authored plus generated files, frontmatter/GFM, file/tree exclusions, independent reasons, no glob syntax, repository escapes, kind mismatch, zero-match entries, and deterministic relative-path diagnostics. Assert `adopted` and `enforced` are the only states.

- [x] **Step 2: Write failing runtime and mutation-safety tests**

Monkeypatch installed distribution versions to cover missing/mismatched pins. Force a formatter failure in a later command-length batch and assert every original byte is restored. Test a path containing spaces, batching below 28,000 command characters, default read-only behavior, explicit modes, and producer-scoped rejection of untracked/non-Markdown inputs.

- [x] **Step 3: Run focused tests and verify RED**

```powershell
py -3 -m pytest codex-marketplace/plugins/agent-operating-model/skills/markdown-formatting/tests/test_format_markdown.py -q
```

Expected: FAIL because the skill implementation does not exist.

- [x] **Step 4: Implement the minimal command**

Parse JSON and TOML with the standard library, validate the schema semantics before any mutation, enumerate `git ls-files -- '*.md'`, and compare `importlib.metadata.version()` with the three exact pins. Invoke `[sys.executable, "-m", "mdformat"]` in bounded batches. For apply, snapshot eligible file bytes before the first invocation and restore all snapshots on any non-zero batch; check mode never writes. Emit one concise diagnostic per invalid contract entry and preserve stable path order.

- [x] **Step 5: Document the skill boundary and pins**

State that the command owns mechanics while the consumer owns adoption, state, exclusions, dependency integration, and command composition. The requirements file contains exactly:

```text
mdformat==1.0.0
mdformat-frontmatter==2.1.2
mdformat-gfm==1.0.0
```

- [x] **Step 6: Prove GREEN and commit canonical source**

Run the focused tests plus frontmatter semantic round-trip coverage. Commit with `feat: add portable markdown formatting skill`. Do not regenerate installed projections yet; Task 8 owns the migration and coherent generated refresh.

### Task 7: Add the optional named repo-standard surface

**Files:**

- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-manifest.json`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-manifest.schema.json`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-standard.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/scaffold_markdown_formatting.py`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/markdown-formatting.json`
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/mdformat.toml`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/code-style.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/pre-commit`
- Modify: `githooks/pre-commit`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**

- Consumes: Task 6 skill command.

- Produces: optional surface id `markdown-formatting`; scaffold CLI `--check`, `--apply --state adopted`, and `--apply --state enforced`; backward-compatible command declaration parsing where `apply` and `check` accept either one legacy command vector (`list[str]`) or an ordered list of vectors (`list[list[str]]`).

- The enforced formatter vectors are `[@python, .agents/skills/markdown-formatting/scripts/format_markdown.py, --apply]` and the matching `--check`; the scaffold prepends them once and never duplicates or reorders the consumer's existing command.

- [x] **Step 1: Write failing command-declaration tests**

Cover legacy vectors, ordered vectors, empty/nested-invalid vectors, `@python` resolution for each command, sequential apply-before-check hook execution, failure propagation, and hosted parity through the same tracked hook template.

- [x] **Step 2: Write failing adoption/enforcement tests**

In neutral repos, assert adoption creates valid config, `state: adopted` contract, code-style guidance, and callable command without changing Markdown or existing command vectors. Assert enforcement first runs formatter apply/check, then changes state and command composition; formatter failure leaves state, commands, and Markdown unchanged. Assert plugin refresh alone creates nothing.

- [x] **Step 3: Run focused tests and verify RED**

```powershell
py -3 -m pytest tests/test_repo_standards.py -q
```

Expected: new tests FAIL because the surface, state transition, and ordered vectors are unsupported.

- [x] **Step 4: Implement the manifest, validator, scaffold, and hook support**

Add the optional surface with its validator/scaffold. Reuse Task 6 contract validation. Adoption writes only absent/migratable surface files and dependency instructions; it does not touch Markdown or gate vectors. Enforcement snapshots contract/declaration/Markdown, runs portable apply then check, writes `enforced`, prepends missing formatter vectors atomically, and restores snapshots on failure. The hook and template execute every declared apply vector in order, stage declared generated paths, then execute every check vector in order; retain legacy flat-vector behavior.

- [x] **Step 5: Prove GREEN and commit**

Run focused repo-standard tests, tracked-hook behavioral tests, and schema validation. Confirm `repo-standards --apply` does not auto-adopt the optional surface. Commit with `feat: add markdown formatting repo standard`.

### Task 8: Migrate this repository to the portable enforced surface

**Files:**

- Create: `.agents/contracts/markdown-formatting.json`
- Modify: `.agents/contracts/repo-standards-commands.json`
- Modify: `.mdformat.toml` only if needed for exact surface conformance.
- Modify: `requirements.txt`
- Modify: `.agents/playbooks/code-style.md`
- Modify: `tools/run.py`
- Modify: `tests/test_run_cli.py`
- Modify: `tests/test_markdown_format.py`
- Regenerate: `.agents/skills/markdown-formatting/**`, manifests, indexes, and mesh files.

**Interfaces:**

- Consumes: Task 6 portable command and Task 7 surface contract.

- Produces: this consumer's `state: enforced` contract, explicit custody exclusions, skill-owned requirement inclusion, and canonical ordered formatter plus CI command vectors.

- [x] **Step 1: Write failing local-wiring tests**

Assert root `requirements.txt` includes `-r .agents/skills/markdown-formatting/requirements.txt` and no duplicate mdformat pins; `tools/run.py` contains no local Markdown enumeration/batching implementation; the declaration invokes portable apply before existing CI apply and portable check before existing CI check; code-style guidance names the portable command; installed skill equals canonical source.

- [x] **Step 2: Author the consumer contract explicitly**

Set version `1`, state `enforced`, and one independent entry for every current byte-governed `assets/authority` tree plus the unrendered `codex-marketplace/plugins/writing-pack/skills/writing-skills/templates/skill/SKILL.md` file. Each entry names `kind`, literal repository-relative `path`, and a custody-specific `reason`; use no glob or blanket generated-Markdown exclusion.

- [x] **Step 3: Regenerate the installed skill before rewiring commands**

Run:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
```

Then integrate the skill-owned requirements into the root environment and prove installed package versions match.

- [x] **Step 4: Replace local mechanics with portable wiring**

Remove `_MARKDOWN_TEMPLATE_SUFFIXES`, `_all_tracked_markdown_files`, and `_run_mdformat` plus their direct lint calls from `tools/run.py`. Preserve the existing CI command as the second ordered vector and add the portable formatter as the first. Update local tests to validate wiring/contract semantics instead of re-testing skill internals.

- [x] **Step 5: Prove the repository migration is already normalized**

Run portable `--apply`, inspect that it produces no unexpected diff beyond contract/wiring work, then run portable `--check`. Run root Markdown and CLI tests. Any excluded entry that no longer needs byte custody must be made compliant and removed instead of retained for convenience.

- [x] **Step 6: Commit the migration through the new hook path**

Stage canonical source, installed projections, consumer contract, commands, requirements, docs, and tests. Commit with `refactor: adopt portable markdown formatting`. The hook must exercise both ordered vectors and leave the tree clean.

### Task 9: Bind Markdown producers to no-churn validation

**Files:**

- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/generating-agent-mesh/scripts/generate_index_mesh.py`
- Modify: `tools/new_plugin.py`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/scripts/repo_standards.py`
- Modify: `tools/sync_skill_shared_references.py`
- Modify: `tests/test_generate_index_mesh.py`
- Modify: `tests/test_repo_standards.py`
- Modify: producer-specific tests for `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`

**Interfaces:**

- Consumes: Task 6 `--check-files` and Task 8 installed skill path.

- Produces: each aggregate producer owner invokes the shared command against the explicit Markdown files it wrote before reporting success; check only, never cleanup.

- [x] **Step 1: Inventory producer ownership in tests**

Pin the four aggregate owners above and assert every tracked Python writer of `.md` is either covered by one owner or named by a test as non-generator/static-template behavior. Fail the inventory when a new unclassified writer appears.

- [x] **Step 2: Write failing producer-boundary tests**

For each owner, monkeypatch the portable checker and assert it receives only that operation's repository-relative Markdown outputs. Make one emitted file drift and assert the producer fails without silently formatting it. Assert non-Markdown outputs are not sent.

- [x] **Step 3: Implement producer-scoped checks**

Collect written Markdown paths during each operation and invoke the installed `format_markdown.py --check-files ...` with the current interpreter before success. `repo_standards.py` aggregates outputs from its scaffold operations; nested scaffold scripts do not double-run the checker.

- [x] **Step 4: Prove generator convergence**

For the index mesh, repo-shape scaffolding, plugin scaffolding, and shared-reference sync, test generation followed immediately by producer check and a second generation with no Markdown diff. Repair producer templates/rendering when drift appears; do not add exclusions.

- [x] **Step 5: Run focused tests and commit**

Run all producer-specific tests plus portable formatter tests. Commit with `fix: validate generated markdown at producer boundaries`.

### Task 10: Regenerate, validate, review, and publish the completed draft

**Files:**

- Regenerate: all marketplace, installed-skill, index, and mesh-owned outputs.
- Modify: this plan only for completion state.

**Interfaces:**

- Consumes: Tasks 6-9.

- Produces: clean generated state, hooked-gate evidence, a whole-branch review, and updated draft PR #328.

- [x] **Step 1: Regenerate all owned outputs**

Run:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py repo-index --apply
py -3 tools/run.py mesh --apply
```

Inspect the diff for authored/generated custody and confirm every generator-owned Markdown file passes its producer check without formatter changes.

- [x] **Step 2: Run focused uncommitted preflight**

Run portable skill tests, repo-standard tests, Markdown/frontmatter tests, command-runner tests, producer tests, installed-skill refresh tests, and `py -3 tools/run.py review-preflight --check`. Run `ci --check` only if diagnosing a failure; the hooked commit owns the complete gate.

- [x] **Step 3: Complete the in-flight plan and make the final hooked commit**

Use `completing-planning-artifacts`, promote any enduring decision not already in the approved spec/contracts, set this plan to `completed-awaiting-retirement`, regenerate mesh, stage all intended files, and commit with `chore: finalize portable markdown formatting`. Record the commit SHA and clean status; never bypass the hook.

- [x] **Step 4: Self-review and obtain one fresh whole-branch review**

Review `git diff origin/main...HEAD` for accidental deeper-smell work, implicit adoption, command-order regressions, unjustified exclusions, dependency duplication, mutation on failure, generator/formatter oscillation, stale local formatter code, and generated projection honesty. Resolve findings in hooked commits and repeat affected focused tests.

- [x] **Step 5: Push and update draft PR #328**

Push the branch, keep the PR draft, and update its body to link this spec and plan; distinguish completed foundation work from portable capability work; list focused commands and final hooked-gate evidence; explain adopted versus enforced behavior and this repository's explicit exclusions. Return the PR URL as publication proof. Ready and merge remain human decisions.
