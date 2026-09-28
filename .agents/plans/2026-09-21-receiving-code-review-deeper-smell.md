# Receiving Code Review Deeper-Smell Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan inline, task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded deeper-smell inspection to code-review reception and prove it with a blinded local-repository RED/GREEN exercise.

**Architecture:** The canonical `receiving-code-review` skill owns the guidance and a lightweight fixture under its root `tests/` lane. A deterministic materializer creates an ordinary local Git repository for paired blinded runs; the baseline and treatment differ only in installed skill content. Marketplace and installed-skill trees remain generated projections.

**Tech Stack:** Markdown skills, Python 3, pytest, Git CLI, repository generation and validation commands.

**Spec:** `.agents/specs/2026-09-21-receiving-code-review-deeper-smell-design.md`

**Execution Strategy:** `executing-plans` — implementation stays inline and sequential so RED is established before the skill changes. Subagents are used only for the fresh blinded RED/GREEN pressure runs and the final independent review.

**State:** ready-for-execution

## Global Constraints

- The slice starts from merged PR #328 on fresh `main`; its skill-test custody contract is a prerequisite, not work to repeat.
- Edit canonical source under `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/`; never hand-edit `.agents/skills/receiving-code-review/`.
- Establish competent-local-fix RED before changing `receiving-code-review/SKILL.md`.
- Keep fixture, patch, prompt, comment, rubric, worker selection, reasoning, and tools equal across RED/GREEN; only installed skill content may differ.
- Ship fixture inputs and rubric under `tests/`; keep repositories, transcripts, scores, caches, and run records off-repo.
- Cap the complete shipped `tests/deeper-smell/` package at 24 files and 65,536 bytes, excluding only the installed behavioral skill copied into a materialized repository.
- Do not add retries, timeouts, telemetry, a general subprocess framework, network behavior, or a permanent GitHub fixture.
- Resolve the concrete Python 3 executable once per execution environment and use it explicitly; do not assume `py`, `python3`, or `python` is bound.

## Review Focus

- Non-empty destinations fail before mutation; Task 1 tests this.
- Fixture growth beyond either limit fails `--check`; Task 1 tests both limits.
- Isolated findings without evidence remain local fixes; Task 3 tests this branch.
- Consequential prevention becomes an evidence-backed follow-up; Task 3 tests this branch.
- Paired-run identities are compared before adjudication; Tasks 2 and 4 record and compare digests.

## Execution setup

Before Task 1, confirm the Bash used by the execution helpers can operate on this worktree, then run `.agents/skills/executing-plans/scripts/resolve-runtime` from that Bash. Record its absolute output as `<PYTHON>` and use that exact executable in every command below. Resolve the off-repo campaign root with:

```powershell
& "<PYTHON>" .agents/skills/subagent-workspace/scripts/workspace.py --apply .agents/plans/2026-09-21-receiving-code-review-deeper-smell.md
```

Use the returned directory for paired-run records and materialized repositories. Do not place those outputs in the repository.

______________________________________________________________________

### Task 1: Ship the deterministic blinded fixture

**Files:**

- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/{README.md,materialize.py,test_materialize.py,worker-prompt.md,review-comment.md,rubric.md,feature.patch}`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/pyproject.toml`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/src/signal_exporter/{__init__.py,commands.py}`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/tests/test_commands.py`

**Interfaces:**

- Consumes: an empty destination and explicit baseline/candidate skill tree.

- Produces: immutable `FixtureStats(file_count: int, total_bytes: int)` and `MaterializedRepo(destination: Path, review_comment: Path, base_commit: str, head_commit: str, fixture_sha256: str, prompt_sha256: str, comment_sha256: str, rubric_sha256: str, skill_sha256: str)` records; `validate_fixture_tree(Path) -> FixtureStats`; `tree_digest(paths: Sequence[Path], root: Path) -> str`; `materialize(destination: Path, skill_source: Path) -> MaterializedRepo`; CLI `--check` and `--apply --destination PATH --skill-source PATH`.

- [ ] **Step 1: Write failing materializer tests**

Load `materialize.py` with `importlib.util.spec_from_file_location`. Add named tests with these assertions:

```python
def test_materialize_creates_clean_deterministic_review_repo(tmp_path):
    first = materialize(tmp_path / "red", BASELINE_SKILL)
    second = materialize(tmp_path / "same", BASELINE_SKILL)
    assert first.base_commit == second.base_commit
    assert first.head_commit == second.head_commit
    assert first.fixture_sha256 == second.fixture_sha256
    assert git(first.destination, "status", "--porcelain=v1", "-uall") == ""
    assert git(first.destination, "remote") == ""
    assert changed_paths(first.destination, "main...HEAD") == {
        "src/signal_exporter/commands.py",
        "tests/test_commands.py",
    }
    assert not (first.destination / ".agents/skills/receiving-code-review/tests").exists()


def test_materialize_refuses_nonempty_destination_without_mutation(tmp_path):
    destination = tmp_path / "occupied"
    destination.mkdir()
    sentinel = destination / "keep.txt"
    sentinel.write_bytes(b"keep\n")
    with pytest.raises(MaterializeError, match="empty"):
        materialize(destination, BASELINE_SKILL)
    assert sentinel.read_bytes() == b"keep\n"
```

Add parameterized checks that `validate_fixture_tree` rejects a symlink, a filename containing a NUL-equivalent unsafe entry supplied through its internal entry validator, `__pycache__`/`.pytest_cache`, 25 files, and 65,537 bytes. Add a CLI test proving bare `--check` validates without writing, and an apply test that runs `<PYTHON> -m pytest -q` inside the materialized repository.

- [ ] **Step 2: Run the focused test and verify RED**

```powershell
& "<PYTHON>" -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
```

Expected: FAIL because the fixture does not exist.

- [ ] **Step 3: Implement the fixture repository**

The base `commands.py` contains `import_data()`, `validate_data()`, and `publish_data()`. Each independently calls `subprocess.run(..., capture_output=True, text=True, check=False)` and returns `not completed.stderr`, thereby duplicating the defective success rule. Base tests monkeypatch `subprocess.run` and cover only successful zero-exit calls. `feature.patch` adds `export_metrics()` with the same rule and one happy-path test. Keep `pyproject.toml` dependency-free apart from pytest test configuration.

`review-comment.md` names `src/signal_exporter/commands.py` and `export_metrics`; its comment body is exactly:

```text
Blocking: `export_metrics()` reports success when the subprocess exits non-zero
without writing stderr. Use the process return code as the success condition and
add a regression for that case.
```

- [ ] **Step 4: Implement deterministic, fail-closed materialization**

Use frozen dataclasses for both return records. Hash sorted repository-relative POSIX paths as `path bytes + NUL + file bytes + NUL`. `fixture_sha256` covers `fixture/` plus `feature.patch`; the prompt, comment, rubric, and behavioral skill each receive separate digests. The behavioral skill digest and copy exclude every path whose relative parts contain `tests`.

Validate all sources and the empty destination before creating anything. Copy `fixture/`, initialize Git with branch `main`, set local `user.name`, `user.email`, `core.autocrlf=false`, and `core.eol=lf`, and commit with fixed author/committer dates. Add `.agents/skills/` and `.review/` to `.git/info/exclude`, copy the behavioral skill, and copy only `review-comment.md` to `.review/review-comment.md`. Create `review/subprocess-export`, apply `feature.patch`, and commit with a second fixed date. Assert no remotes, clean status, and exactly the two intended changed paths before returning JSON-serializable identities plus the neutral comment path. On failure, remove only a destination first created by this invocation.

- [ ] **Step 5: Document the blinded prompt and rubric**

`worker-prompt.md` tells the worker only to read `.agents/skills/receiving-code-review/SKILL.md`, inspect `git diff main...HEAD`, verify the supplied `review-comment.md`, implement the justified correction, run focused tests, and report evidence. It must not name the parent repository, fixture, rubric, systemic mechanism, or RED/GREEN.

`rubric.md` defines two mutually exclusive successful classifications. `CLEAN_RED` requires a correct `export_metrics()` return-code regression and passing focused tests, with no sibling-pattern inspection, no named duplicated process-result mechanism, and no shared boundary. `GREEN` requires the local correction, an evidenced search of all sibling wrappers, the named duplicated mechanism, exactly one `_run_checked(args: Sequence[str]) -> bool` boundary, migration of the four wrappers, a non-zero/no-stderr boundary regression, passing tests, and no retry/timeout/telemetry/framework expansion. Anything else is `INVALID` with a reason; never weaken a criterion after seeing a run.

- [ ] **Step 6: Prove the fixture tests and commit**

Run:

```powershell
& "<PYTHON>" -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
& "<PYTHON>" codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/materialize.py --check
```

Then materialize once under the resolved scratch root and independently prove clean status, no remotes, the intended diff, and passing fixture tests. Remove that probe repository. Stage only Task 1 authored files and commit with `test: add deeper-smell review fixture`; allow the tracked hook to regenerate and stage its owned installed projection and indexes.

### Task 2: Establish the blinded baseline RED

**Files:**

- Read: Task 1 README; read the rubric only after worker completion.
- Transient: off-repo repository, baseline skill snapshot, and JSON run record.

**Interfaces:**

- Consumes: Task 1 fixture and committed pre-change skill.

- Produces: a transient RED record with treatment-independent digests, Git identities, worker selection, verification, and rubric outcome.

- [ ] **Step 1: Freeze paired identities and the worker route**

Use `selecting-a-subagent` immediately before dispatch. Select the portable `implementer` role with fresh context (`fork_turns: "none"`); under the current Codex V2 mapping this is `gpt-5.6-terra` at `medium`, but the live dispatch schema is authoritative. Record the exact resolved model, reasoning, context mode, tool surface, and role, and reuse them unchanged for GREEN.

Copy the committed pre-change behavioral skill, excluding `tests/`, to `<scratch>/baseline-skill/`. Materialize `<scratch>/red-repo` from that snapshot. Write `<scratch>/paired-run.json` with this shape:

```json
{
  "rubric_version": 1,
  "worker": {"role": "implementer", "model": "...", "reasoning": "...", "fork_turns": "none", "tools": ["..."]},
  "red": {"fixture_sha256": "...", "prompt_sha256": "...", "comment_sha256": "...", "rubric_sha256": "...", "skill_sha256": "...", "base_commit": "...", "head_commit": "...", "classification": null, "evidence": []},
  "green": null
}
```

Populate identities only from `materialize.py` JSON output; do not hand-compute or copy them from conversation text.

- [ ] **Step 2: Dispatch a fresh blinded worker**

Dispatch with `fork_turns: "none"`, the frozen route, `<scratch>/red-repo` as the explicit working directory, and the exact bytes of `worker-prompt.md` plus the materializer-returned `<scratch>/red-repo/.review/review-comment.md` path. Do not send a path into the parent repository, parent history, or a paraphrased prompt. Disclose none of the parent repo, design, recipe, rubric, expected smell, or RED/GREEN terminology.

- [ ] **Step 3: Adjudicate clean RED**

After the worker finishes, inspect its final report, `git diff main...HEAD`, `git status --porcelain=v1 -uall`, and a fresh `<PYTHON> -m pytest -q` run. Read `rubric.md` only now. Record `CLEAN_RED` only when every RED criterion is evidenced. Ordinary reception failure is `INVALID`; systemic inspection or prevention is already `GREEN` and means this fixture has not established the required baseline. In either case, refine Task 1 and rerun with a fresh repository; do not edit the skill or weaken the rubric.

- [ ] **Step 4: Record and clean up**

Add only concise paths, commands, exit codes, changed-path summaries, and the rubric classification to the RED record. Do not copy the full worker transcript. Remove `<scratch>/red-repo`; retain `baseline-skill/` and `paired-run.json` through Task 4. Confirm `git status --short` in the marketplace worktree is unchanged. Commit no run artifact.

### Task 3: Add bounded deeper-smell guidance

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**

- Consumes: clean RED from Task 2.

- Produces: `READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY` and the spec's three branches.

- [ ] **Step 1: Write the failing prose-contract test**

Add `test_receiving_code_review_requires_bounded_deeper_smell_inspection` beside the existing skill-contract tests. Read the canonical skill, normalize whitespace with `" ".join(text.split())`, and assert these stable clauses rather than formatting:

```python
assert "READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY" in normalized
assert "Could another competent implementer" in normalized
assert "No credible deeper smell" in normalized
assert "Credible, small, in-scope prevention" in normalized
assert "Credible but consequential or out of scope" in normalized
assert "causal mechanism" in normalized and "repository evidence" in normalized
assert "mandatory root-cause analysis" in normalized
assert "silently expand" in normalized
assert "reviewed specimen" in normalized
assert "manifest drift" in normalized
```

- [ ] **Step 2: Run it and verify RED**

Run:

```powershell
& "<PYTHON>" -m pytest tests/test_workflow_contracts.py::TestValidationTddPublication::test_receiving_code_review_requires_bounded_deeper_smell_inspection -q
```

Expected: FAIL because `INSPECT` is absent.

- [ ] **Step 3: Make the minimal skill edit**

Change the response-pattern block to the exact eight-step sequence. Add one `## Inspect for a Deeper Smell` section after technical evaluation that contains the competent-implementer question, evidence requirement, and the spec's three branches. State that prevention preference is: remove the opportunity, mechanically detect the class, make the correct action easiest, then use prose only when judgment is unavoidable. Add one manifest-drift example and one Common Mistakes row for stopping at the reviewed specimen. Preserve skepticism, clarification, YAGNI, and no-performative-agreement behavior; do not add a general root-cause workflow.

- [ ] **Step 4: Prove GREEN and commit**

Run the new node, then:

```powershell
& "<PYTHON>" -m pytest tests/test_workflow_contracts.py -q
```

Inspect only the canonical skill and contract-test diff. Stage those two files and commit with `feat: inspect deeper smells during review reception`; allow the tracked hook to run.

### Task 4: Prove paired GREEN

**Files:**

- Read: Task 1 fixture and rubric.
- Transient: fresh candidate repository and paired record.

**Interfaces:**

- Consumes: frozen Task 2 identities and Task 3 candidate skill.

- Produces: equality-checked paired evidence and GREEN decision.

- [ ] **Step 1: Materialize and compare identities**

Materialize `<scratch>/green-repo` from the committed candidate behavioral skill, excluding `tests/`. Append the returned identities to `paired-run.json`. Before dispatch, assert fixture, prompt, comment, rubric, base commit, head commit, worker role, model, reasoning, context mode, and tools equal RED exactly, and assert `skill_sha256` differs. A small one-off comparison command may read the transient JSON, but it must not be committed. Delete and rematerialize both arms on any unexpected mismatch.

- [ ] **Step 2: Dispatch a fresh blinded worker**

Dispatch with the exact Task 2 route, `fork_turns: "none"`, `<scratch>/green-repo` as working directory, and the exact same prompt and comment bytes. Do not summarize the RED result or expose `paired-run.json`.

- [ ] **Step 3: Adjudicate GREEN**

Inspect the final report, `git diff main...HEAD`, clean status, and a fresh `<PYTHON> -m pytest -q` run. Require every `GREEN` criterion in `rubric.md`; a mention without sibling inspection fails, as does unrelated redesign. If the worker stops locally or overreaches, refine only the minimum Task 3 wording, commit it, rematerialize both arms from their frozen baseline/candidate skills, and rerun the equal pair. Do not reuse a worker context.

- [ ] **Step 4: Close transient custody**

Record concise paths, commands, exit codes, changed-path summaries, classification, and the equality comparison. Report the RED/GREEN outcome in the current execution handoff before deleting it. Then remove `red-repo`, `green-repo`, `baseline-skill`, `paired-run.json`, and any worker report from the resolved scratch subdirectory. Confirm no fixture repository, transcript, score, or run record appears in `git status --short`. Commit no transient artifact.

### Task 5: Regenerate, validate, and publish

**Files:**

- Regenerate: `.agents/skills/receiving-code-review/**`, manifests, indexes, and mesh-owned files.
- Modify: this plan for completion state.

**Interfaces:**

- Consumes: Task 4 GREEN and canonical Task 1/3 source.

- Produces: truthful projections, hooked-gate evidence, whole-branch review, and draft PR.

- [ ] **Step 1: Regenerate projections**

Run, in order:

```powershell
& "<PYTHON>" tools/run.py marketplace --apply
& "<PYTHON>" tools/run.py installed-skills --apply
& "<PYTHON>" tools/run.py repo-index --apply
& "<PYTHON>" tools/run.py mesh --apply
```

Use the existing installed-skill equality test to prove canonical and installed bytes match, including `tests/`. Prove ordinary invocation does not direct the agent to read `tests/` through the skill-test contract assertion in `tests/test_workflow_contracts.py`.

- [ ] **Step 2: Run focused preflight**

Run:

```powershell
& "<PYTHON>" -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py tests/test_workflow_contracts.py tests/test_refresh_installed_skills.py -q
& "<PYTHON>" tools/run.py review-preflight --check
```

Fix findings owned by this slice and classify unrelated pre-existing warnings explicitly. Do not run standalone `ci --check` immediately before a normal hooked commit.

- [ ] **Step 3: Complete the plan and make the hooked commit**

Use `completing-planning-artifacts`. Promote any enduring rule discovered during execution to its owning skill or contract, set this plan and its spec to `completed-awaiting-retirement`, run `<PYTHON> tools/run.py mesh --apply`, stage the complete intended tree, and commit with `chore: finalize deeper-smell review reception`. The hook owns complete staged apply/check validation; never bypass it. Record the commit SHA and verify clean status.

- [ ] **Step 4: Self-review and fresh whole-branch review**

Build an off-repo review package for `origin/main...HEAD`. Self-review for blinded-data leakage, unsafe destination cleanup, digest ambiguity, treatment mismatch, over-broad guidance, and projection honesty. Then use `selecting-a-subagent` to dispatch a fresh `reviewer-skills` lens (or the current Codex V2 equivalent) with no inherited context and the review package. Resolve every blocking or important finding, rerun the affected focused tests, and make a normal hooked fix commit.

- [ ] **Step 5: Push and open a draft PR**

Push `codex/receiving-review-deeper-smell` and open a Draft PR against `main`. Link the spec and plan; summarize RED/GREEN without transcripts; record focused, review, and hooked validation; state that transient repositories, snapshot, records, and worker reports were removed. Verify the PR head SHA equals local `HEAD`, attach the PR to the task, and return its URL. Ready and merge remain human decisions.
