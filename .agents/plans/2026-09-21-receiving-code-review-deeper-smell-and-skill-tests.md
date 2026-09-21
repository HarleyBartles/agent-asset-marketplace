# Receiving Code Review Deeper-Smell Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded deeper-smell inspection to code-review reception and prove it with a blinded local-repository RED/GREEN exercise.

**Architecture:** The canonical `receiving-code-review` skill owns the guidance and a lightweight fixture under its root `tests/` lane. A deterministic materializer creates an ordinary local Git repository for paired blinded runs; the baseline and treatment differ only in installed skill content. Marketplace and installed-skill trees remain generated projections.

**Tech Stack:** Markdown skills, Python 3, pytest, Git CLI, repository generation and validation commands.

**Spec:** `.agents/specs/2026-09-21-receiving-code-review-deeper-smell-and-skill-tests-design.md`

**Execution Strategy:** `subagent-driven-development` — the proof requires fresh blinded subagents, while sequential task order prevents treatment leakage and establishes RED before the skill changes.

**State:** deferred to a fresh PR after draft PR #328

## Global Constraints

- Start the future slice from fresh `main` after PR #328 lands; its skill-test custody contract is a prerequisite, not work to repeat.
- Edit canonical source under `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/`; never hand-edit `.agents/skills/receiving-code-review/`.
- Establish competent-local-fix RED before changing `receiving-code-review/SKILL.md`.
- Keep fixture, patch, prompt, comment, rubric, worker selection, reasoning, and tools equal across RED/GREEN; only installed skill content may differ.
- Ship fixture inputs and rubric under `tests/`; keep repositories, transcripts, scores, caches, and run records off-repo.
- Cap the fixture at 24 files and 65,536 bytes, excluding the installed behavioral skill.
- Do not add retries, timeouts, telemetry, a general subprocess framework, network behavior, or a permanent GitHub fixture.

## Review Focus

- Non-empty destinations fail before mutation; Task 1 tests this.
- Fixture growth beyond either limit fails `--check`; Task 1 tests both limits.
- Isolated findings without evidence remain local fixes; Task 3 tests this branch.
- Consequential prevention becomes an evidence-backed follow-up; Task 3 tests this branch.
- Paired-run identities are compared before adjudication; Tasks 2 and 4 record and compare digests.

______________________________________________________________________

### Task 1: Ship the deterministic blinded fixture

**Files:**

- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/{README.md,materialize.py,test_materialize.py,review-comment.md,rubric.md,feature.patch}`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/pyproject.toml`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/src/signal_exporter/{__init__.py,commands.py}`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/tests/test_commands.py`

**Interfaces:**

- Consumes: an empty destination and explicit baseline/candidate skill tree.

- Produces: `FixtureStats(file_count: int, total_bytes: int)`, `MaterializedRepo(destination: Path, base_commit: str, head_commit: str, fixture_sha256: str, skill_sha256: str)`, `validate_fixture_tree(Path) -> FixtureStats`, `materialize(Path, Path) -> MaterializedRepo`; CLI `--check` and `--apply --destination PATH --skill-source PATH`.

- [ ] **Step 1: Write failing materializer tests**

Test limits, symlink/NUL/cache rejection, non-empty-destination refusal without mutation, deterministic hashes, no remotes, clean `main...HEAD`, exclusion of the installed skill's `tests/`, and passing fixture tests.

- [ ] **Step 2: Run the focused test and verify RED**

```powershell
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
```

Expected: FAIL because the fixture does not exist.

- [ ] **Step 3: Implement fixture and materializer**

Make three sibling wrappers infer success from output/error text. The patch adds `export_metrics()` with the same defect and a happy-path test. The review comment is exactly:

```text
Blocking: `export_metrics()` reports success when the subprocess exits non-zero
without writing stderr. Use the process return code as the success condition and
add a regression for that case.
```

Validate before writing; copy the fixture; install only the behavioral skill surface; initialize and commit `main`; create `review/subprocess-export`; apply and commit the patch; leave a clean tree. Reject unsafe entries. On failure, remove only a destination created by this invocation.

- [ ] **Step 4: Document the prompt and rubric**

The prompt reveals only the repository, installed skill, and comment. GREEN requires the local fix, sibling inspection, named duplicated process-result semantics, one shared checked-execution boundary, wrapper-family migration, a boundary regression, and no unrelated redesign. Clean RED is competent local repair and verification that stops without inspecting or naming the mechanism.

- [ ] **Step 5: Prove GREEN and commit**

Run the focused test and `materialize.py --check`; materialize once to a unique temporary directory; prove clean status, no remotes, intended diff only, and passing fixture tests. Commit with `test: add deeper-smell review fixture`.

### Task 2: Establish the blinded baseline RED

**Files:**

- Read: Task 1 README; read the rubric only after worker completion.
- Transient: off-repo repository, baseline skill snapshot, and JSON run record.

**Interfaces:**

- Consumes: Task 1 fixture and committed pre-change skill.

- Produces: a transient RED record with treatment-independent digests, Git identities, worker selection, verification, and rubric outcome.

- [ ] **Step 1: Freeze paired identities**

Select one worker model/profile/reasoning combination. Record digests for fixture, patch, comment, prompt, rubric, and baseline skill plus base/head commits. Retain the baseline skill snapshot off-repo through Task 4.

- [ ] **Step 2: Dispatch a fresh blinded worker**

Tell it to read the installed skill, inspect `git diff main...HEAD`, verify the supplied comment, correct it, test, and report. Disclose none of the parent repo, design, recipe, rubric, expected smell, or RED/GREEN terminology.

- [ ] **Step 3: Adjudicate clean RED**

Accept only a correct local fix plus focused verification that neither inspects sibling occurrences nor names duplicated semantics. If ordinary reception fails or GREEN already appears, refine Task 1 and repeat; do not edit the skill or weaken the rubric.

- [ ] **Step 4: Record and clean up**

Add concise evidence to the off-repo record and remove the materialized repository. Commit no run artifact.

### Task 3: Add bounded deeper-smell guidance

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**

- Consumes: clean RED from Task 2.

- Produces: `READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY` and the spec's three branches.

- [ ] **Step 1: Write the failing prose-contract test**

Normalize whitespace and assert the response sequence, exact competent-implementer question, local/small-prevention/consequential-follow-up branches, causal mechanism plus evidence, rejection of mandatory root-cause work and silent scope expansion, the specimen-only mistake, and manifest-drift example.

- [ ] **Step 2: Run it and verify RED**

Run the single test. Expected: FAIL because `INSPECT` is absent.

- [ ] **Step 3: Make the minimal skill edit**

Add the exact question and three outcomes from the spec. Prefer removing the opportunity, mechanical detection, or an easier correct path over reminders. Preserve skepticism, clarification, YAGNI, and no-performative-agreement behavior.

- [ ] **Step 4: Prove GREEN and commit**

Run the new test and all `tests/test_workflow_contracts.py`; inspect the diff; commit with `feat: inspect deeper smells during review reception`.

### Task 4: Prove paired GREEN

**Files:**

- Read: Task 1 fixture and rubric.
- Transient: fresh candidate repository and paired record.

**Interfaces:**

- Consumes: frozen Task 2 identities and Task 3 candidate skill.

- Produces: equality-checked paired evidence and GREEN decision.

- [ ] **Step 1: Materialize and compare identities**

Use the same recipe. Verify fixture, patch, prompt, comment, rubric, Git shape, worker selection, reasoning, and tools match RED; only `skill_sha256` may differ. Rematerialize on any other mismatch.

- [ ] **Step 2: Dispatch a fresh blinded worker**

Use the exact Task 2 prompt with no inherited context.

- [ ] **Step 3: Adjudicate GREEN**

Require every rubric outcome. Mention alone is insufficient; unrelated redesign fails. If it stops locally or overreaches, refine Task 3 and rerun both equal arms.

- [ ] **Step 4: Close transient custody**

Capture concise evidence, then remove both repositories, skill snapshot, and run records. Commit no transcript or generated repository.

### Task 5: Regenerate, validate, and publish

**Files:**

- Regenerate: `.agents/skills/receiving-code-review/**`, manifests, indexes, and mesh-owned files.
- Modify: this plan for completion state.

**Interfaces:**

- Consumes: Task 4 GREEN and canonical Task 1/3 source.

- Produces: truthful projections, hooked-gate evidence, whole-branch review, and draft PR.

- [ ] **Step 1: Regenerate projections**

Run `py -3 tools/run.py marketplace --apply`, `installed-skills --apply`, `repo-index --apply`, and `mesh --apply`. Prove canonical/installed skill equality and that invocation does not load `tests/`.

- [ ] **Step 2: Run focused preflight**

Run materializer tests, workflow contracts, installed-skill refresh tests, and `py -3 tools/run.py review-preflight --check`. Do not run standalone `ci --check` immediately before a normal hooked commit.

- [ ] **Step 3: Complete the plan and make the hooked commit**

Use `completing-planning-artifacts`, set state to `completed-awaiting-retirement`, regenerate mesh if needed, stage intended files, and commit. The hook owns complete staged apply/check validation; never bypass it.

- [ ] **Step 4: Self-review and fresh whole-branch review**

Review `git diff origin/main...HEAD` for blinded-data leakage, unsafe materialization, treatment mismatch, over-broad guidance, and projection honesty. Resolve findings and re-run affected tests.

- [ ] **Step 5: Push and open a draft PR**

Link spec and plan; summarize RED/GREEN without transcripts; record focused and hooked validation; state transient artifacts were removed. Return the draft PR URL; Ready and merge remain human decisions.
