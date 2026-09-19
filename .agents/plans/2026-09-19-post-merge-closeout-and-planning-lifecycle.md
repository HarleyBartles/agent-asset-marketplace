# Post-Merge Closeout and Planning-Artifact Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make verified non-ancestry branch retirement, routine submodule teardown, and temporary planning-artifact custody portable across marketplace consumers.

**Architecture:** `finishing-a-development-branch` becomes the workflow owner for post-merge branch/worktree retirement and its removal primitive. A new repo-worker-pack `completing-planning-artifacts` skill owns the two-slice planning-artifact lifecycle; Superpowers+ planning skills and agent-operating-model stage bindings route to that owner. This slice keeps its completed spec and plan in the final PR so squash-merged `main` records them; the next substantive slice retires them.

**Tech Stack:** Markdown skills and doctrine, Python 3.12 helper/tests, repository generators and tracked pre-commit gate.

**Spec:** `.agents/specs/2026-09-19-post-merge-closeout-and-planning-lifecycle-design.md`

**Execution Strategy:** `executing-plans` — the helper move, contract tests, portable guidance, scaffolds, regeneration, and artifact retirement are tightly coupled and must proceed sequentially.

## Global Constraints

- Edit canonical plugin sources before generated `.agents/skills/` projections.
- Preserve consumer-owned dirty-state protections outside submodules.
- Discard non-authoritative submodule checkout dirt during routine teardown.
- Do not automate forge mutations or assume one merge strategy.
- Treat this spec and plan as committed in-flight artifacts, then mark both `completed-awaiting-retirement` and retain them through this completing PR.

---

### Task 1: Commit the in-flight execution package

**Files:**
- Create: `.agents/specs/2026-09-19-post-merge-closeout-and-planning-lifecycle-design.md`
- Create: `.agents/plans/2026-09-19-post-merge-closeout-and-planning-lifecycle.md`

**Interfaces:**
- Consumes: approved conversation requirements and current repository doctrine.
- Produces: committed execution inputs for subsequent tasks.

- [ ] Run `py -3 tools/run.py mesh --apply` and inspect the generated plan/spec indexes.
- [ ] Run the plan-readiness gate and require at least 9/10.
- [ ] Stage and commit the plan package through the tracked hook.

### Task 2: Move and correct the worktree-removal primitive with TDD

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/scripts/remove_worktree.py`
- Delete: `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/scripts/remove_worktree.py`
- Modify: `tests/test_worktree_scripts.py`

**Interfaces:**
- Consumes: branch name or registered absolute worktree path plus `--check`, `--apply`, and explicitly destructive `--force` modes.
- Produces: routine forced submodule deinitialization followed by ordinary worktree removal; worktree force only when explicitly selected.

- [ ] Change focused tests to resolve the helper from its new canonical owner and add cases proving dirty submodule content is discarded without worktree force while dirty consumer-owned files remain protected.
- [ ] Run the focused tests and witness the expected RED caused by the missing moved helper/behavior.
- [ ] Move the helper through an `apply_patch` edit, separate submodule `-f` from worktree `--force`, and keep locked-directory safeguards.
- [ ] Run `py -3 -m pytest tests/test_worktree_scripts.py -v` and require GREEN.

### Task 3: Teach verified post-merge retirement

**Files:**
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/finishing-a-development-branch/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-git-worktrees/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: exact merged PR identity/base/head/merge-result evidence.
- Produces: discoverable post-merge branch/worktree closeout.

- [ ] Add contract tests for the approved proof sequence and ownership pointer; run them to witness RED.
- [ ] Make the minimal canonical skill edits that satisfy the tests without encoding repository-specific commands.
- [ ] Run the focused workflow-contract tests and require GREEN.

### Task 4: Create and pressure-test the portable planning-artifact lifecycle skill

**Files:**
- Create: `codex-marketplace/plugins/repo-worker-pack/skills/completing-planning-artifacts/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/writing-roadmaps/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/executing-plans/SKILL.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/SKILL.md`
- Modify: `tests/test_workflow_contracts.py`

**Interfaces:**
- Consumes: in-flight planning artifacts, completion state, merged-base evidence, and repository-local promotion paths.
- Produces: `completed-awaiting-retirement` completion output and idempotent successor-slice retirement without cleanup-only PRs.

- [ ] Run a pressure scenario without the new skill and record the observed baseline failure/rationalization.
- [ ] Add failing contract tests for committed-in-flight terminology, two-slice ownership, squash-history preservation, successor-slice ingress, and the `cleanup-custody` ambiguity boundary; witness RED.
- [ ] Scaffold and write the minimal first-party marketplace skill plus routing edits that address the observed failures.
- [ ] Re-run the pressure scenario with the skill and require compliant behavior; repair and repeat if a new loophole appears.
- [ ] Run focused workflow-contract tests and require GREEN.

### Task 5: Export the lifecycle through agent-operating-model

**Files:**
- Create: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/planning.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/templates/pr.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-runbook-standard.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/repo-shape/references/repository-shape-standard.md`
- Modify: `.agents/runbooks/planning.md`
- Modify: `.agents/runbooks/pr.md`
- Modify: `.agents/doctrine/repo-runbook-policy.md`
- Delete: `.agents/playbooks/completing-plans.md`
- Modify: `tests/test_repo_shape.py`

**Interfaces:**
- Consumes: portable lifecycle language and completed-artifact doctrine.
- Produces: reusable stage bindings to the portable skill plus aligned local guidance.

- [ ] Add scaffold/contract tests proving the planning template invokes the portable skill, completion is bound into the appropriate stage, and a method-heavy completion playbook is not required; run to witness RED.
- [ ] Add the canonical templates/reference changes and align this repository's local runbook/playbook.
- [ ] Run the focused repo-shape tests and require GREEN.

### Task 6: Regenerate, validate, review, and mark planning artifacts complete

**Files:**
- Regenerate: marketplace manifests, installed skills, and repository indexes/mesh.
- Modify: `.agents/specs/2026-09-19-post-merge-closeout-and-planning-lifecycle-design.md`
- Modify: `.agents/plans/2026-09-19-post-merge-closeout-and-planning-lifecycle.md`

**Interfaces:**
- Consumes: completed canonical source changes and passing focused tests.
- Produces: converged generated surfaces, completion-marked planning artifacts retained through merge, and publication-ready evidence.

- [ ] Run `py -3 tools/run.py marketplace --apply`, `py -3 tools/run.py installed-skills --apply`, and `py -3 tools/run.py mesh --apply`.
- [ ] Review the full diff against the spec and verify enduring decisions live in skills, templates, references, tests, or local compositions.
- [ ] Mark this spec and plan `completed-awaiting-retirement`, verify their enduring content is promoted, and keep them in the final staged tree.
- [ ] Stage the complete intended tree and commit normally so the tracked hook runs `ci --apply` and `ci --check --diagnostics` on the staged snapshot.
- [ ] Run completion-readiness and whole-branch review, repair any findings, push the branch, open a draft PR, verify remote head/state/checks, and flip ready only after the repository PR preflight passes.
