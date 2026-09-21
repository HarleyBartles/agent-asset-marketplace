# Receiving Code Review Deeper-Smell and Skill Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded deeper-smell inspection to code-review reception, prove it with a blinded local-repository RED/GREEN exercise, and establish skill-root `tests/` as the marketplace's maintainer-verification lane.

**Architecture:** The canonical `receiving-code-review` skill owns the behavioral guidance and a complete, lightweight Python fixture under its own `tests/` tree. A deterministic materializer copies that fixture into off-repo scratch, installs either the baseline or candidate skill, and creates ordinary `main` and feature commits for blinded subagent runs. Repository doctrine and focused contract tests define the general `tests/` convention; normal marketplace generation then projects the complete canonical skill trees into `.agents/skills/`.

**Tech Stack:** Markdown skills and doctrine, Python 3 standard library, pytest, Git CLI, repository `tools/run.py` generators and validation.

**Spec:** `.agents/specs/2026-09-21-receiving-code-review-deeper-smell-and-skill-tests-design.md`

**Execution Strategy:** `subagent-driven-development` — tasks have reviewable boundaries, the behavioral proof explicitly requires fresh blinded subagents, and fresh implementer/reviewer context reduces leakage between fixture authorship, RED observation, skill wording, and GREEN evaluation. Tasks remain sequential because the RED must precede the skill edit and GREEN must use the settled candidate.

**State:** active

## Global Constraints

- Edit canonical skill sources under `codex-marketplace/plugins/`; never hand-edit `.agents/skills/` projections.
- Establish and record a competent-local-fix RED before changing `receiving-code-review/SKILL.md`.
- Keep RED and GREEN equal in fixture tree, feature patch, prompt, model/profile, reasoning, tools, review comment, and rubric; the selected skill content is the sole intentional treatment difference.
- Keep generated repositories, transcripts, score folders, and run output off-repo; retain only concise evidence in the execution handoff.
- Ship the complete fixture tree under the skill's `tests/` directory, capped at 24 files and 65,536 total bytes, excluding the installed skill copied into a materialized repository.
- The fixture contains source, tests, and minimum project metadata only: no dependency trees, build output, binaries, caches, remote configuration, or network/connector behavior.
- `tests/` is maintainer-facing verification, ships with canonical and installed skill directories, and is not loaded during ordinary skill invocation.
- Apply the standards principle verbatim in substance: skills are code, code ships with tests, and neither code nor skills ship test results. A skill without test material need not gain low-value placeholder tests in this slice.
- Do not move behavioral references or runtime data merely because their names contain `test`, `pressure`, `golden`, or `scenario`.
- Do not retain a permanent GitHub fixture repository or broaden the fixture into retries, timeouts, telemetry, or a general subprocess framework.

## Review Focus

- A non-empty materialization destination must fail before copying or initializing Git; covered in Task 1's materializer tests.
- Fixture growth beyond either 24 files or 65,536 bytes must fail `--check`; covered in Task 1's weight-limit tests.
- A correct isolated review finding with no evidenced repeatable mechanism must remain a local fix, not force speculative redesign; covered in Task 3's prose-contract test.
- A credible but consequential prevention must produce an evidence-backed follow-up rather than silent scope expansion; covered in Task 3's prose-contract test.
- Nested skill test files must survive installation byte-for-byte without becoming runtime discovery inputs; covered in Task 5's projection test and Task 6's generated-tree comparison.

______________________________________________________________________

### Task 1: Build the lightweight local-PR fixture and materializer

**Files:**

- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/README.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/materialize.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/review-comment.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/rubric.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/feature.patch`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/pyproject.toml`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/src/signal_exporter/__init__.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/src/signal_exporter/commands.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/fixture/tests/test_commands.py`

**Interfaces:**

- Consumes: canonical baseline or candidate skill directory supplied with `--skill-source`; an empty destination supplied with `--destination`; local Git and Python only.

- Produces: `FixtureStats(file_count: int, total_bytes: int)`, `MaterializedRepo(destination: Path, base_commit: str, head_commit: str, fixture_sha256: str, skill_sha256: str)`, `validate_fixture_tree(fixture_root: Path) -> FixtureStats`, `copy_behavioral_skill(skill_source: Path, destination: Path) -> None`, and `materialize(destination: Path, skill_source: Path) -> MaterializedRepo`. CLI `--check` validates the shipped fixture without writing; `--apply --destination PATH --skill-source PATH` creates the repository and prints the result as JSON.

- [ ] **Step 1: Write failing materializer contract tests**

Add pytest cases that import `materialize.py` by file path and assert:

```python
def test_validate_fixture_tree_accepts_shipped_fixture():
    stats = materialize.validate_fixture_tree(FIXTURE_ROOT)
    assert 1 <= stats.file_count <= 24
    assert 1 <= stats.total_bytes <= 65_536

def test_validate_fixture_tree_rejects_file_count_and_byte_overflow(tmp_path):
    # Create 25 tiny files, then one 65_537-byte file in separate trees.
    # Each call must raise FixtureValidationError naming the violated limit.

def test_materialize_requires_empty_destination(tmp_path):
    # Put keep.txt in destination and assert no .git directory or copied file appears.

def test_materialize_creates_reviewable_repository(tmp_path):
    # Assert branches main and review/subprocess-export exist, status is clean,
    # main...HEAD contains only the feature patch, no remotes exist, the installed
    # behavioral skill is present in both commits, its tests/ tree is absent,
    # and both fixture tests pass on HEAD.
```

Also run the CLI with no mode, `--check`, incomplete `--apply` arguments, and a valid `--apply` invocation. Assert default/explicit check is non-mutating and apply emits parseable JSON.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```powershell
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
```

Expected: FAIL because `materialize.py` and the fixture do not exist yet.

- [ ] **Step 3: Add the complete base fixture and feature patch**

Make `commands.py` expose a small `CommandResult` value and two sibling wrappers that each incorrectly infer success from empty `stderr`. Base tests document their ordinary successful-output behavior without exposing the hidden class-level answer. Make `feature.patch` add `export_metrics()` by copying the same faulty pattern plus a focused happy-path test. The review comment must identify the added wrapper and the precise defect:

```text
Blocking: `export_metrics()` reports success when the subprocess exits non-zero
without writing stderr. Use the process return code as the success condition and
add a regression for that case.
```

The fixture must remain credible as a small package: use only `pyproject.toml`, `src/signal_exporter/`, and `tests/`; use `unittest.mock` and standard-library `subprocess.CompletedProcess`; require no install or network step to run `py -3 -m pytest -q` from the materialized root.

- [ ] **Step 4: Implement deterministic validation and materialization**

Implement the declared dataclasses/functions and CLI with these operations, in order:

```python
validate_fixture_tree(FIXTURE_ROOT)
require_empty_destination(destination)
shutil.copytree(FIXTURE_ROOT, destination, dirs_exist_ok=True)
(destination / ".agents/skills").mkdir(parents=True)
copy_behavioral_skill(skill_source, destination / ".agents/skills/receiving-code-review")
git("init", "-b", "main")
git("config", "user.name", "Fixture Author")
git("config", "user.email", "fixture@example.invalid")
git("add", "--all")
git("commit", "-m", "chore: establish signal exporter")
git("switch", "-c", "review/subprocess-export")
git("apply", FEATURE_PATCH)
git("add", "--all")
git("commit", "-m", "feat: add metrics export command")
```

Hash files in sorted relative-path order with path separators normalized to `/`. `copy_behavioral_skill` copies `SKILL.md` plus any `agents/`, `assets/`, `references/`, and `scripts/` content, but must exclude top-level `tests/` so the hidden harness cannot leak into the worker repository. Reject symlinks, `__pycache__`, `.pyc`, binary/NUL-bearing fixture files, and any fixture entry outside the size limits. Do not add a remote. On a failed apply, remove only a destination that this invocation created; never delete a pre-existing path.

- [ ] **Step 5: Write the maintainer README and hidden rubric**

Document exact check/materialize commands, scratch-only output custody, the blinded worker prompt, and cleanup. The worker prompt may reveal only the working repository, installed skill path, and `review-comment.md`; it must not name RED/GREEN, duplicated semantics, shared boundaries, rubric, or expected prevention.

Score GREEN only when the worker: fixes and verifies the reviewed wrapper; inspects sibling wrappers; identifies duplicated process-result semantics; introduces one shared checked-execution boundary; migrates the small wrapper family; adds a boundary-level non-zero/empty-stderr regression; and avoids retries, telemetry, timeouts, or framework redesign. Define the clean RED exactly as competent local repair plus focused verification that stops without inspecting or naming the repeatable mechanism.

- [ ] **Step 6: Run focused tests and inspect the generated diff**

Run:

```powershell
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
py -3 codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/materialize.py --check
```

Materialize once into a unique off-repo temporary path, then run:

```powershell
$fixtureRepo = Join-Path ([System.IO.Path]::GetTempPath()) ("receiving-review-fixture-" + [guid]::NewGuid())
py -3 codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/materialize.py --apply --destination $fixtureRepo --skill-source codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review
git -C $fixtureRepo status --short
git -C $fixtureRepo diff --stat main...HEAD
git -C $fixtureRepo remote -v
Push-Location $fixtureRepo; py -3 -m pytest -q; Pop-Location
```

Expected: focused tests PASS; status and remotes are empty; the diff contains only the intended wrapper/test addition; fixture tests PASS.

- [ ] **Step 7: Commit the fixture**

```powershell
git add codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell
git commit -m "test: add deeper-smell review fixture"
```

### Task 2: Establish the blinded baseline RED

**Files:**

- Read: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/README.md`
- Read after worker completion only: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/rubric.md`
- Transient: resolved off-repo scratch directories for the repository and run record

**Interfaces:**

- Consumes: Task 1 materializer, the committed pre-change `receiving-code-review` skill, exact blinded prompt, review comment, rubric, and a fresh subagent selected once for both arms.

- Produces: transient RED record containing fixture digest, baseline behavioral-skill digest, base/head commits, model/profile and reasoning, prompt/rubric digests, worker patch summary, verification commands, and rubric outcome; plus an off-repo baseline behavioral-skill snapshot retained only through Task 4.

- [ ] **Step 1: Freeze treatment-independent identities**

Resolve one subagent profile/model/reasoning combination with `selecting-a-subagent` and use it unchanged for both arms. Copy the baseline behavioral skill surface to off-repo scratch, materialize the baseline repository from the committed Task 1 tree, and retain that baseline copy only until the paired campaign ends. Record SHA-256 digests for the complete fixture tree, feature patch, review comment, blinded prompt, rubric, and installed baseline behavioral skill plus the base/head commit IDs. Store the JSON record off-repo.

- [ ] **Step 2: Dispatch a fresh blinded worker**

Give the worker only this instruction, substituting the actual review-comment contents and repository path:

```text
You are receiving blocking code-review feedback on the current feature branch.
Work in the supplied repository. Read and follow the installed
`.agents/skills/receiving-code-review/SKILL.md`, inspect `git diff main...HEAD`,
verify the feedback against the code, implement the justified correction, run
focused tests, and report what you changed and verified. Review feedback:
Blocking: `export_metrics()` reports success when the subprocess exits non-zero
without writing stderr. Use the process return code as the success condition and
add a regression for that case.
```

Do not disclose the parent repository, design/spec, fixture source, rubric, expected smell, RED/GREEN terminology, or prior conversation.

- [ ] **Step 3: Adjudicate the run against the clean-RED definition**

After the worker finishes, inspect its patch, searches/tool trace available to the harness, focused test output, and final report. Accept RED only if all five local-competence conditions pass and the worker neither inspects sibling occurrences nor names duplicated process-result semantics. Reject the fixture rather than weakening the rubric if the worker misunderstands, patches incorrectly, omits normal verification, cannot discover siblings, or already performs the desired inspection.

- [ ] **Step 4: Record and report the checkpoint without committing run artifacts**

Update the transient JSON with the rubric decision and concise evidence. Remove the materialized repository after evidence capture, but retain the off-repo JSON and baseline behavioral-skill snapshot through Task 4. In the execution commentary, state whether clean RED was established and the local fix/tests observed. Do not commit the repository, transcript, JSON record, or generated skill copy. If clean RED is not established, stop implementation and return to Task 1 fixture refinement before touching the skill.

### Task 3: Add the bounded deeper-smell behavior to review reception

**Files:**

- Modify: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**

- Consumes: approved three-branch decision and clean RED from Tasks 1-2.

- Produces: response sequence `READ -> UNDERSTAND -> VERIFY -> EVALUATE -> INSPECT -> RESPOND -> IMPLEMENT -> VERIFY`, the competent-implementer smell test, and bounded local/prevention/follow-up branches.

- [ ] **Step 1: Add failing prose-contract tests**

Add `TestRepositoryCallersAndPressure.test_receiving_code_review_has_bounded_deeper_smell_inspection` in `tests/test_workflow_contracts.py`. Normalize whitespace and assert the canonical skill contains:

```python
assert "evaluate -> inspect -> respond -> implement -> verify" in normalized
assert "could another competent implementer" in normalized
assert "no credible deeper smell" in normalized
assert "small" in normalized and "in-scope prevention" in normalized
assert "consequential" in normalized and "evidence-backed follow-up" in normalized
assert "causal mechanism" in normalized and "repository evidence" in normalized
assert "fixing only the reviewed specimen" in normalized
```

Also assert the text rejects mandatory root-cause work and silent scope expansion, and contains a compact manifest-drift example that distinguishes generated truth from hand-maintained representation.

- [ ] **Step 2: Run the single test and verify RED**

Run:

```powershell
py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure::test_receiving_code_review_has_bounded_deeper_smell_inspection -q
```

Expected: FAIL because the current response pattern has no `INSPECT` step or branches.

- [ ] **Step 3: Make the minimal skill edit**

Insert `INSPECT` after `EVALUATE`, using this governing question verbatim:

```text
Could another competent implementer, using the repository's current interfaces,
workflow, and guidance, plausibly make the same class of mistake?
```

Define the three outcomes: local correction when no credible mechanism exists; local correction plus the smallest durable in-scope prevention when evidence supports it; or independently safe correction plus an evidence-backed follow-up when prevention is consequential/out of scope. State that a smell is a causal mechanism evidenced in the repository, not an imagined future risk. Prefer removing the opportunity, mechanical detection, or an easier correct path over reminders. Add one manifest-drift example and the specimen-only common mistake without changing the skill's skepticism, clarification, YAGNI, or no-performative-agreement rules.

- [ ] **Step 4: Run focused skill contracts**

Run:

```powershell
py -3 -m pytest tests/test_workflow_contracts.py::TestRepositoryCallersAndPressure::test_receiving_code_review_has_bounded_deeper_smell_inspection -q
py -3 -m pytest tests/test_workflow_contracts.py -k "receiving_code_review or vendored_skill_metadata" -q
```

Expected: PASS, including the canonical skill's frontmatter contract.

- [ ] **Step 5: Commit the behavioral treatment**

```powershell
git add codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/SKILL.md tests/test_workflow_contracts.py
git commit -m "feat: inspect deeper smells in review feedback"
```

### Task 4: Prove blinded GREEN against the unchanged fixture

**Files:**

- Read: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/README.md`
- Read after worker completion only: `codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/rubric.md`
- Transient: new off-repo scratch repository and paired run record

**Interfaces:**

- Consumes: the frozen Task 2 identities and subagent configuration, unchanged fixture/prompt/comment/rubric, and Task 3 candidate skill.

- Produces: paired transient GREEN evidence proving the skill digest is the sole intentional treatment difference.

- [ ] **Step 1: Verify comparison equality before dispatch**

Materialize a new repository with the candidate skill. Recompute all Task 2 digests and fail closed unless fixture tree, feature patch, review comment, prompt, rubric, model/profile, reasoning, tools, and base/head tree content match the RED arm. The skill digest must differ. Record the candidate skill digest and new commit IDs.

- [ ] **Step 2: Dispatch a new blinded worker with the identical prompt**

Use a fresh subagent and the exact prompt from Task 2. Do not provide RED output, rubric, expected shared boundary, or hints about sibling wrappers.

- [ ] **Step 3: Adjudicate all GREEN requirements**

Require observable evidence for every rubric item: reviewed wrapper fixed; non-zero/empty-stderr regression passes; sibling patterns inspected; duplicated process-result semantics named; one shared checked-execution boundary introduced; the small wrapper family migrated; boundary-level proof added; unrelated subprocess redesign avoided. A mere mention of possible systemic risk is not GREEN.

- [ ] **Step 4: Handle failure without corrupting the comparison**

If the worker fixes only the specimen, make one minimal wording refinement in `SKILL.md`, commit it, then rematerialize RED from the retained baseline behavioral-skill snapshot and GREEN from the refined candidate and rerun the pair. If the worker overreaches, tighten the evidence/authority branches and rerun both arms. Never edit the fixture or rubric between paired arms; a required fixture change invalidates both prior runs and returns execution to Task 2.

- [ ] **Step 5: Report and clean transient evidence**

Record the paired verdict and exact passing test commands in the transient JSON, report the comparison in execution commentary, then remove both generated repositories and transient run records. Commit only a wording refinement if Task 4 required one; otherwise make no repository commit.

### Task 5: Establish and enforce skill-root test custody

**Files:**

- Modify: `.agents/doctrine/skill-standards-policy.md`
- Modify: `tests/pressure/README.md`
- Modify: `tests/pressure/using-playwright-mcp/README.md`
- Move: `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/assets/pressure-tests.md` to `codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp/tests/pressure-tests.md`
- Move: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/test-academic.md` to `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/academic.md`
- Move: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/test-pressure-1.md` to `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-1.md`
- Move: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/test-pressure-2.md` to `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-2.md`
- Move: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/test-pressure-3.md` to `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/scenarios/pressure-3.md`
- Move: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/CREATION-LOG.md` to `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/tests/evidence/creation-log.md`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_refresh_installed_skills.py`

**Interfaces:**

- Consumes: complete canonical skill directories and existing whole-directory installed-skill sync.

- Produces: documented `tests/` meaning, rejection of retired placements, and byte-for-byte nested test-tree installation proof.

- [ ] **Step 1: Add failing doctrine and custody tests**

In `tests/test_workflow_contracts.py`, add a test that checks the policy states that skills are code, code ships with tests, and neither code nor skills ship test results. It must also name `tests/` as optional maintainer verification; say it ships but is not part of ordinary invocation; distinguish `assets/`, `references/`, and `scripts/`; keep transcripts, scores, verdicts, generated repositories, and other run output off-repo; and name complete lightweight fixture trees plus materialization helpers. Assert `tests/pressure/README.md` points to skill-root `tests/` and no longer requires `assets/pressure-tests.md`.

Add an inventory test over every declared skill directory that rejects `assets/pressure-tests.md`, root `test-*.md`, and root `CREATION-LOG.md`, while explicitly asserting the six new destinations exist. Do not reject existing behavioral paths identified as non-test material in the spec.

In `tests/test_refresh_installed_skills.py`, create a temporary source skill with `tests/fixture/nested.txt` containing non-ASCII text and CRLF bytes, invoke `_copy_skill_directory`, and assert the installed file bytes are identical. This proves the existing copy seam; change the copier only if this test exposes a real omission.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```powershell
py -3 -m pytest tests/test_workflow_contracts.py -k "skill_tests or test_material_custody" -q
py -3 -m pytest tests/test_refresh_installed_skills.py -k "nested_test_tree" -q
```

Expected: FAIL on the old doctrine/locations and any missing projection assertion.

- [ ] **Step 3: Update doctrine and pressure orchestration guidance**

Lead the testing contract with: skills are code; code ships with its tests; code does not ship test results; the same boundary applies to skills. Add `tests/` to the directory tree and define it as optional only in the sense that a skill with no test material need not contain an empty or invented suite. When tests exist, their automated checks, evaluation scenarios, complete lightweight fixtures, materializers, rubrics, and stable expectations ship in `tests/`. State that arbitrary extra directories are permitted but undefined by the Agent Skills specification; this is marketplace-local doctrine. State that `tests/` ships in canonical/installed skills but ordinary invocation neither requires nor directs loading it. Explicitly exclude run-specific transcripts, scores, verdicts, generated repositories, and other execution output.

Revise repository-root pressure guidance so it owns shared orchestration and generic campaign instructions, while each skill-root `tests/` owns portable prompts, fixture trees, rubrics, and deterministic assertions. GREEN may load `SKILL.md` and behavioral resources only; evaluators/materializers may load the hidden test material. Point the Playwright campaign README at its moved skill-root scenario.

- [ ] **Step 4: Move the six inventoried files without rewriting their meaning**

Use `git mv` for all six paths. Update links that become broken, but do not edit scenario prose merely to modernize style and do not move `iterative-review/tests/` or any behavioral/golden/profile material excluded by the spec.

- [ ] **Step 5: Make projection tests pass with the smallest necessary change**

Run the focused tests. If `_copy_skill_directory` already preserves nested `tests/` byte-for-byte, retain the passing regression with no production change. If it fails, modify only `.agents/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` at the whole-directory copy/comparison seam and add cases for apply and check mode before rerunning.

- [ ] **Step 6: Commit doctrine, migration, and contracts**

```powershell
git add .agents/doctrine/skill-standards-policy.md tests/pressure tests/test_workflow_contracts.py tests/test_refresh_installed_skills.py codex-marketplace/plugins/mcp-usage-pack/skills/using-playwright-mcp codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging
git commit -m "refactor: standardize skill test custody"
```

### Task 6: Regenerate projections, verify the complete slice, and publish review evidence

**Files:**

- Modify generated: `.agents/skills/receiving-code-review/`
- Modify generated: `.agents/skills/systematic-debugging/`
- Modify generated: `.agents/skills/using-playwright-mcp/`
- Modify generated as selected by commands: `codex-marketplace/manifest.json`, plugin bundle manifests, repository indexes, and mesh indexes
- Modify at completion: `.agents/plans/2026-09-21-receiving-code-review-deeper-smell-and-skill-tests.md`

**Interfaces:**

- Consumes: all canonical source commits and paired RED/GREEN evidence.

- Produces: current generated projections, complete repository verification, a completed-awaiting-retirement plan, self-review evidence, and a reviewable draft PR.

- [ ] **Step 1: Regenerate from canonical sources**

Run:

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py repo-index --apply
py -3 tools/run.py mesh --apply
```

Inspect generated changes. Confirm no generated file became an authored edit point and no unrelated plugin content changed.

- [ ] **Step 2: Prove canonical-to-installed test-tree equality**

Compare every file and relative path under the changed canonical skill trees with `.agents/skills/receiving-code-review/`, `.agents/skills/systematic-debugging/`, and `.agents/skills/using-playwright-mcp/` using the repository's tree canonicalization rules. Explicitly assert the new receiving-code-review fixture, moved systematic-debugging tests, and moved Playwright pressure scenario exist byte-for-byte in the installed copies. Confirm ordinary skill discovery still keys on `SKILL.md` and does not enumerate or auto-load `tests/`.

- [ ] **Step 3: Run focused and complete validation**

Run:

```powershell
py -3 -m pytest codex-marketplace/plugins/superpowers-plus/skills/receiving-code-review/tests/deeper-smell/test_materialize.py -q
py -3 -m pytest tests/test_workflow_contracts.py -q
py -3 -m pytest tests/test_refresh_installed_skills.py -q
py -3 tools/run.py review-preflight --check
```

Expected: all focused checks and review preflight pass. Do not run a standalone `ci --check` here; the normal commit in Step 4 owns the complete staged-snapshot gate.

- [ ] **Step 4: Complete the in-flight plan and commit the final tree**

Use `completing-planning-artifacts`: promote any enduring decision not already captured by the approved spec or doctrine, mark this plan `completed-awaiting-retirement`, regenerate the mesh if the status edit changes it, stage all intended authored/generated files, and commit:

```powershell
git commit -m "chore: finalize deeper-smell review workflow"
```

The hooked commit must pass. Record the commit SHA and `git status --short --branch`; the worktree must be clean.

- [ ] **Step 5: Self-review the branch and resolve findings**

Review `git diff origin/main...HEAD` with the repository review guidance. Check especially: blinded-data leakage into worker inputs, destructive destination handling, fixture weight enforcement, exact RED/GREEN equality, over-broad skill language, stale links after moves, and generated projection honesty. Fix and commit any finding, then obtain one fresh whole-branch review through the execution lane. Re-run only the focused checks affected by fixes; the final hooked commit supplies the complete gate.

- [ ] **Step 6: Publish a draft PR with evidence**

Push the branch and open a draft PR into `main`. The PR body must link the approved spec and committed plan; summarize the clean RED and GREEN observations without transcripts; list focused commands and hooked-gate result; name the six custody moves; state that generated repositories/run records were removed; and disclose any fixture or wording iteration. Return the PR URL as publication proof and leave Ready/merge decisions to the human reviewer.
