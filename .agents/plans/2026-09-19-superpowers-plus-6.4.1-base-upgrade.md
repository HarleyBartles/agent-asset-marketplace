# Superpowers+ 6.4.1 Base Upgrade Implementation Plan

**Status:** completed-awaiting-retirement

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` for this tightly coupled Native upgrade. Steps use checkbox syntax for tracking.

**Goal:** Rebase Superpowers+ from the `obra/superpowers` v6.3.0 skill basis to v6.4.1 while preserving the derivative's Codex/Devin workflow, safety, custody, and repository-composition layers.

**Architecture:** Treat upstream v6.3.0, upstream v6.4.1, and current Superpowers+ as a three-way semantic merge. Adopt new core behavior at its natural owner, keep Superpowers+-only skills and contracts layered above it, replace duplicated PowerShell/Bash helper pairs owned by Superpowers+ with Python CLIs, and retain upstream-owned shell helpers as shell scripts invoked through Git Bash on Windows.

**Tech Stack:** Markdown skills and prompts, Python 3.12 helper CLIs, upstream Bash helpers executed with Git Bash on Windows, pytest contract tests, marketplace generators, and the tracked pre-commit gate.

**Spec:** Conversation-approved migration strategy from 2026-09-19; upstream basis `obra/superpowers` v6.4.1 commit `5bf4e78011075bcfc0dc295f0724994cd123ee71`; previous basis v6.3.0 commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`.

**Execution Strategy:** `executing-plans` — this upgrade is one tightly coupled three-way semantic merge. Later tasks depend on the exact contracts and paths established by earlier tasks, so Native inline execution keeps the integration context coherent and uses one fresh whole-branch review at completion.

## Global Constraints

- Superpowers+ supports Codex and Devin Desktop. Do not add unsupported-harness workflow promises merely because upstream v6.4.1 supports more harnesses.
- Preserve all first-party Superpowers+ additions unless this plan explicitly replaces a duplicated behavior with the v6.4.1 owner.
- Keep the planning-handoff review already present in `brainstorming`; v6.4.1 does not supersede it.
- Keep `handoff-gates` limited to plan-readiness and completion-readiness.
- Canonical source lives under `codex-marketplace/plugins/superpowers-plus/`; never hand-edit `.agents/skills/` projections.
- Superpowers+-owned executable helpers use Python 3.12 and the repository's `--help`/`--check`/`--apply` CLI contract where mutation exists.
- Upstream-owned shell helpers remain Bash. On Windows, instructions invoke them through Git Bash rather than creating PowerShell translations.
- Preserve the off-repository, repository-segregated scratch layout owned by `subagent-workspace`; do not adopt upstream's tracked-tree `.superpowers/sdd/` location.
- Preserve human-owned product/canon/privacy/licensing decisions and explicit authority gates from the current derivative.
- Use current repository commands and staged-snapshot hook semantics. Do not copy upstream's repository-specific test commands into portable skills.
- Keep the PR Draft throughout implementation and self-review.

---

### Task 1: Pin the v6.4.1 basis and freeze the combined ownership contract

**Files:**
- Modify: `tests/test_workflow_contracts.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/README.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/codex-marketplace-compatibility.md`

**Interfaces:**
- Consumes: the exact v6.3.0 and v6.4.1 commits named in the plan header plus the current 22-skill Superpowers+ inventory.
- Produces: version/provenance truth for later tasks and contract assertions that distinguish inherited core skills from Superpowers+-only additions.

- [x] **Step 1: Add failing version and inventory assertions**

Extend `TestMarketplacePluginContracts` so it requires plugin and bundle version `6.4.1`, `SOURCE.md` commit `5bf4e78011075bcfc0dc295f0724994cd123ee71`, and continued presence of the eight Superpowers+-only helpers. Task 6 adds the `diagnosing-superpowers` inventory assertion with the skill itself so this task can exit green.

- [x] **Step 2: Run the focused contract and witness RED**

Run: `py -3 -m pytest tests/test_workflow_contracts.py::TestMarketplacePluginContracts -q`

Expected: FAIL on the `6.3.0` version and basis pin.

- [x] **Step 3: Update the canonical basis metadata**

Set the plugin and bundle to `6.4.1`; move v6.3.0 to the audited prior comparison point; name `5bf4e78011075bcfc0dc295f0724994cd123ee71` as the active basis. Keep `source_family: first_party` and do not introduce separate attribution for the user's own Superpowers+ work.

- [x] **Step 4: Run the focused contract GREEN**

Run: `py -3 -m pytest tests/test_workflow_contracts.py::TestMarketplacePluginContracts -q`

Expected: PASS.

- [x] **Step 5: Commit the basis boundary**

```bash
git add tests/test_workflow_contracts.py codex-marketplace/plugins/superpowers-plus
git commit -m "chore(superpowers-plus): pin 6.4.1 upstream basis"
```

### Task 2: Adopt the low-conflict v6.4.1 behavioral improvements

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/test-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/requesting-code-review/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/requesting-code-review/code-reviewer.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/root-cause-tracing.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-skills/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: upstream v6.4.1 suite-wide TDD, reasonable-user review, declined-to-judge, merge-base, and interpreter-invocation changes.
- Produces: portable core behavior that later Native and SDD execution paths can rely on.

- [x] **Step 1: Add failing semantic contract tests**

Require: project-level complete validation before completion; `git merge-base origin/main HEAD` guidance; reasonable-user expectations for spec-silent behavior; a `Declined to judge` section returned to the controller; and interpreter-qualified invocation of bundled shell/Node scripts.

- [x] **Step 2: Run the focused tests and witness RED**

Run: `py -3 -m pytest tests/test_workflow_contracts.py -q`

Expected: FAIL on each missing v6.4.1 behavior.

- [x] **Step 3: Merge the upstream guidance through repository authority**

Adopt the behaviors without hard-coding upstream repository commands. Phrase the TDD final proof as the consumer's declared complete gate; preserve focused RED/GREEN during each task. Keep reviewer findings routed through current `receiving-code-review` and ruling contracts.

- [x] **Step 4: Run focused tests GREEN**

Run: `py -3 -m pytest tests/test_workflow_contracts.py -q`

Expected: PASS.

- [x] **Step 5: Commit the low-conflict base changes**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills tests/test_workflow_contracts.py
git commit -m "feat(superpowers-plus): adopt 6.4.1 core safeguards"
```

### Task 3: Consolidate Superpowers+-owned workspace helpers on Python

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/workspace.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/task_brief.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/review_package.py`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/sdd-workspace`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/sdd-workspace.ps1`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/task-brief`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/task-brief.ps1`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/review-package`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/scripts/review-package.ps1`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace/SKILL.md`
- Create: `tests/test_subagent_workspace.py`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_repo_standards.py`
- Modify: `tests/test_review_preflight.py`
- Modify: `tests/test_review_preflight_extensions.py`
- Modify: `tools/review_preflight.py`

**Interfaces:**
- Consumes: repository/worktree identity, plan path, task number, and `BASE`/`HEAD` revisions.
- Produces: one cross-platform Python implementation for workspace resolution, brief extraction, and review-package creation; exact CLI paths consumed by Tasks 4 and 5.

- [x] **Step 1: Add failing Python-helper tests**

Cover these observable cases:

- two plans with the same basename resolve to different off-repo workspaces using a persisted canonical plan identity;
- a legacy marker-less workspace is adopted once without overwriting another plan;
- branch and repository names remain sanitized and repository-segregated;
- review packaging rejects an empty range and a non-descendant `HEAD` with exit `3`;
- review packages are UTF-8 without BOM and include commits, stat, and contextual diff;
- plan-less review packages still resolve the branch scratch workspace;
- each Python CLI exposes `--help` and defaults to read-only behavior.

- [x] **Step 2: Run the helper contracts and witness RED**

Run: `py -3 -m pytest tests/test_subagent_workspace.py tests/test_repo_standards.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`

Expected: FAIL because the Python helpers do not exist and current basename/range behavior is unsafe.

- [x] **Step 3: Implement `workspace.py`**

Use `pathlib`, `subprocess.run(..., check=True)`, UTF-8 without BOM, and atomic marker writes. Preserve the canonical `<main-checkout>/../_agent-scratch/<repo>/<branch>/<plan>/` layout. Persist the normalized plan identity inside the workspace and add parent/counter disambiguation when the basename is already owned.

- [x] **Step 4: Implement `task_brief.py` and `review_package.py`**

Import the shared workspace resolver rather than invoking another process. `review_package.py` verifies both revisions, checks `merge-base --is-ancestor`, rejects zero commits, and writes the same package contract used by reviewer prompts.

- [x] **Step 5: Remove dual-shell ownership and update references**

Delete the six Superpowers+-owned Bash/PowerShell implementations. Update skill prose, prompt placeholders, `review_preflight.py`, and tests to name the Python CLIs. Do not create replacement `.ps1` or shell wrappers.

- [x] **Step 6: Run helper and repository contracts GREEN**

Run: `py -3 -m pytest tests/test_subagent_workspace.py tests/test_repo_standards.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py -q`

Expected: PASS.

- [x] **Step 7: Commit the Python execution engine**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/subagent-workspace tools/review_preflight.py tests
git commit -m "refactor(superpowers-plus): consolidate workspace helpers on Python"
```

### Task 4: Merge shared intent, Review Focus, and saved-plan review

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/brainstorming/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-roadmaps/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/execution-lane-override.md`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/pressure/workflow-contracts/campaign.json`
- Create: `tests/pressure/workflow-contracts/prompts/shared-intent-before-design.md`
- Create: `tests/pressure/workflow-contracts/prompts/saved-plan-review.md`

**Interfaces:**
- Consumes: the current spike/bounded/architectural model, planning-handoff burden review, plan-readiness gate, and v6.4.1 shared-intent/Review-Focus/plan-review behavior.
- Produces: an approved design-to-plan chain with no duplicate approval, no exposed private burden ledger, and explicit Native/Subagent-driven trade-offs.

- [x] **Step 1: Add failing workflow contracts and pressure prompts**

Require `brainstorming` to discover and reflect intended outcome/audience/success when missing, while preserving already-authorized bounded execution and the planning-handoff review. Require plans to contain a `Review Focus` section whose entries are pinned to owning-task tests. Require the saved plan to be reviewed before execution and preserve any execution method already supplied.

- [x] **Step 2: Run the focused tests and baseline pressure scenarios RED**

Run: `py -3 -m pytest tests/test_workflow_contracts.py -q`

Run: `py -3 tools/run_workflow_pressure_campaign.py --campaign tests/pressure/workflow-contracts/campaign.json --apply --family luna --scenario shared-intent-before-design`

Run: `py -3 tools/run_workflow_pressure_campaign.py --campaign tests/pressure/workflow-contracts/campaign.json --apply --family luna --scenario saved-plan-review`

Expected: deterministic contract failures identify the missing shared-intent and saved-plan-review behavior; retained baseline outputs show the current skill omits at least one required behavior.

- [x] **Step 3: Merge shared intent into the three-path owner**

Add a concise shared-understanding stage before path-specific design. Do not import upstream's universal approval language. Bounded work proceeds when already authorized and no human-owned decision remains; architectural work still requires written-spec and saved-plan review.

- [x] **Step 4: Add Review Focus and the saved-plan handoff**

Keep `Global Constraints`, `Execution Strategy`, plan-readiness, and planning-artifact lifecycle. Add up to five spec-implied untested input classes/failure modes and place each covering test inside the task that owns the code. Present the saved plan for review; recommend an execution lane from the plan and explain its cost.

- [x] **Step 5: Run contracts and pressure scenarios GREEN**

Run: `py -3 -m pytest tests/test_workflow_contracts.py -q`

Run the same two Luna campaign commands from Step 2 against the amended skill.

Expected: contract tests pass and both scenarios satisfy their rubric without weakening bounded-work proportionality.

- [x] **Step 6: Commit the design/planning merge**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/brainstorming codex-marketplace/plugins/superpowers-plus/skills/writing-plans codex-marketplace/plugins/superpowers-plus/skills/writing-roadmaps codex-marketplace/plugins/superpowers-plus/references tests
git commit -m "feat(superpowers-plus): merge 6.4.1 design and planning flow"
```

### Task 5: Rebuild Native execution and reconcile SDD routing

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/scripts/task-start`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/scripts/task-done`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/re-review-prompt.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development/task-reviewer-prompt.md`
- Create: `tests/test_executing_plans_scripts.py`
- Modify: `tests/test_workflow_contracts.py`
- Modify: `tests/test_repo_standards.py`

**Interfaces:**
- Consumes: Task 3 Python workspace/brief/review-package CLIs and Task 4's reviewed plan plus Review Focus.
- Produces: v6.4.1 Native inline execution layered with Superpowers+ baselines, rulings, handoff gates, completion lifecycle, and final publication route; corrected SDD-vs-Native selection.

- [x] **Step 1: Add failing Native/SDD contracts**

Assert that:

- Native means the current session implements tasks and buys one fresh whole-branch review;
- SDD means fresh implementer plus reviewer per task;
- both share the same off-repo ledger and Python helper contracts;
- neither pauses between tasks absent a human-owned/safety/authority/plan-integrity stop;
- Native final review receives Review Focus and every ledgered ruling;
- completion flows through `handoff-gates`, `completing-planning-artifacts`, and `finishing-a-development-branch`;
- Windows instructions run upstream `task-start`/`task-done` through Git Bash rather than PowerShell translations.

- [x] **Step 2: Run focused contracts and witness RED**

Run: `py -3 -m pytest tests/test_executing_plans_scripts.py tests/test_workflow_contracts.py tests/test_repo_standards.py -q`

Expected: FAIL against the current stub-like executor and old “stay in this session” distinction.

- [x] **Step 3: Rebuild `executing-plans` from the v6.4.1 Native owner**

Use upstream's task loop, ledger, TDD completion contract, reasonable-user finding regrade, one fix pass, and final review as the base. Reapply: `implementation-baseline.md`, `.agents/runbooks/implementing.md`, checkpoint-first resume, human/authority stop boundaries, plan lane override, completion-readiness, planning-artifact completion, and branch finishing.

- [x] **Step 4: Add the upstream Bash task helpers without PowerShell copies**

Keep `task-start` and `task-done` recognizable as upstream-owned Bash helpers. Adapt their calls to Task 3's Python CLIs. Document `bash .../task-start` and `bash .../task-done` for Windows/Git Bash execution. Do not add `.ps1` equivalents.

- [x] **Step 5: Reconcile SDD routing and prompts**

Replace “stay in this session?” with the execution-cost distinction. Preserve Superpowers+ model selection, task review, five-round fix loop, adjudication, completion-readiness, and final fix wave. Route all workspace/package calls to Task 3's Python CLIs.

- [x] **Step 6: Run focused contracts GREEN**

Run: `py -3 -m pytest tests/test_executing_plans_scripts.py tests/test_workflow_contracts.py tests/test_repo_standards.py -q`

Expected: PASS.

- [x] **Step 7: Commit the execution-engine merge**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/executing-plans codex-marketplace/plugins/superpowers-plus/skills/subagent-driven-development tests
git commit -m "feat(superpowers-plus): adopt native plan execution"
```

### Task 6: Add `diagnosing-superpowers` for Codex and Devin Desktop

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/analyst-common.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/cost-and-time.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/plan-adherence.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/quality-evidence.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/repeated-work.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/request-conflicts.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/scrub-audit.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/scrub.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/similar-session.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/skill-timeline.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/prompts/stumbles.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/references/context-safety.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/references/github-issues.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/references/redaction-policy.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/references/session-discovery.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/templates/bundle-README.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/templates/case.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/templates/issue.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/templates/report.md`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/README.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`
- Create: `tests/test_diagnosing_superpowers.py`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: Codex and Devin Desktop transcript locations/capabilities, `context-safety`, `selecting-a-subagent`, `dispatching-parallel-agents`, `using-github-mcp`, and `connector-safety`.
- Produces: evidence-cited session reports, optional approval-gated scrubbed bundles, and approval-gated GitHub issue drafts without claiming framework diagnosis.

- [x] **Step 1: Add failing structure and boundary tests**

Require every upstream prompt/reference/template, first-party metadata and wrapper, Codex and Devin Desktop discovery routes, repository-scoped off-repo diagnostic custody, `path:line` findings, read-only transcript handling, and explicit approval before bundle/archive/GitHub mutation.

- [x] **Step 2: Run focused tests and witness RED**

Run: `py -3 -m pytest tests/test_diagnosing_superpowers.py tests/test_workflow_contracts.py -q`

Expected: FAIL because the skill and bundle entry do not exist.

- [x] **Step 3: Import the v6.4.1 skill as first-party base content**

Bring over the complete prompts, references, and templates. Add repository frontmatter and wrapper metadata. Keep the “report evidence; do not diagnose Superpowers” boundary.

- [x] **Step 4: Adapt only the harness and composition seams**

Replace generic/Claude-only session discovery with verified Codex and Devin Desktop routes. Resolve scratch through repository/host policy rather than `~/.superpowers`. Route dispatch, context protection, GitHub reads/writes, and sensitive side effects through their existing Superpowers+ owners. Treat subagent selection as routing rather than delegation authority; when the active runtime or task policy does not permit fan-out, preserve the evidence contract with a clearly disclosed sequential/self-analysis fallback rather than claiming the seven analysts ran.

- [x] **Step 5: Run focused tests GREEN**

Run: `py -3 -m pytest tests/test_diagnosing_superpowers.py tests/test_workflow_contracts.py -q`

Expected: PASS, including the new diagnostic-skill inventory contract added in this task.

- [x] **Step 6: Commit the diagnostic skill**

```bash
git add codex-marketplace/plugins/superpowers-plus/skills/diagnosing-superpowers codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json codex-marketplace/plugins/superpowers-plus/README.md codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus tests/test_workflow_contracts.py
git commit -m "feat(superpowers-plus): add session diagnostics"
```

### Task 7: Regenerate, validate, review, and publish the upgraded base

**Files:**
- Regenerate: `codex-marketplace/manifest.json`
- Regenerate: `.agents/skills/`
- Regenerate: repository indexes and mesh
- Modify: `.agents/plans/2026-09-19-superpowers-plus-6.4.1-base-upgrade.md`
- Modify: PR #324 body and pushed branch head

**Interfaces:**
- Consumes: all six implementation commits and the current Draft PR.
- Produces: converged marketplace/install projections, current validation evidence, a completion-marked plan retained through merge, and verified publication proof.

- [x] **Step 1: Regenerate every owned projection**

Run: `py -3 tools/run.py marketplace --apply`

Run: `py -3 tools/run.py installed-skills --apply`

Run: `py -3 tools/run.py mesh --apply`

Expected: canonical sources, manifests, installed copies, and indexes converge.

- [x] **Step 2: Run the complete focused regression set**

Run: `py -3 -m pytest tests/test_diagnosing_superpowers.py tests/test_executing_plans_scripts.py tests/test_subagent_workspace.py tests/test_workflow_contracts.py tests/test_repo_standards.py tests/test_review_preflight.py tests/test_review_preflight_extensions.py tests/test_tree_canonicalization.py -q`

Expected: PASS.

- [x] **Step 3: Audit version and stale-route residue**

Run: `rg -n "6\\.3\\.0|b36e0829|sdd-workspace\\.ps1|task-brief\\.ps1|review-package\\.ps1|Stay in this session" codex-marketplace/plugins/superpowers-plus .agents/skills tests`

Expected: only deliberately retained prior-comparison history or negative test assertions; no active v6.3.0 basis, dual PowerShell helper, or obsolete routing instruction.

- [x] **Step 4: Review the whole branch against this plan**

Verify every v6.4.1 skill delta is classified as adopted, deliberately adapted, or out of scope; confirm all Superpowers+-only skills remain; confirm Codex/Devin support statements and Python/Git-Bash execution rules agree across canonical and installed surfaces.

- [x] **Step 5: Complete planning-artifact lifecycle**

Promote any enduring execution-engine rule to current skills/doctrine, mark this plan `completed-awaiting-retirement`, regenerate the mesh, and retain the plan in the completing PR.

- [x] **Step 6: Commit through the tracked hook**

```bash
git add --all
git commit -m "chore(superpowers-plus): finalize 6.4.1 base upgrade"
```

Expected: staged-snapshot hook runs apply plus `ci --check --diagnostics` and reports `0 FAIL`.

- [x] **Step 7: Push and verify Draft PR publication**

Push `codex/superpowers-plus-planning-handoff`, update PR #324 with the 6.4.1 base-upgrade summary and current evidence, and verify `headRefOid`, `isDraft: true`, base `main`, and hosted checks for the exact pushed SHA.
