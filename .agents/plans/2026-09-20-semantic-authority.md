# Semantic Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent agents from turning implementation details, environment markers, or reproduced failures into unauthorized workflow semantics.

**Architecture:** Put the cross-project authority invariant in base doctrine, bind it into bootstrap and debugging behavior, and state the staged-snapshot boundary in its owning hook skill. Tighten the existing validation choreography rather than creating a competing workflow. Protect the behavior with focused contract tests and one bounded pressure scenario derived from the observed Portfolio failure.

**Tech Stack:** Markdown skill/doctrine sources, Python pytest contract tests, marketplace projection generators, Git tracked pre-commit hook.

**Scope:** Canonical marketplace sources and their generated projections only. No new command-line flags, environment variables, validation modes, or consumer-specific Portfolio changes.

**State:** completed-awaiting-retirement

## Task 1: Specify the failing boundary

**Files:**
- Modify: `tests/test_workflow_contracts.py`
- Add: `tests/pressure/workflow-contracts/prompts/semantic-authority.md`
- Modify: `tests/pressure/workflow-contracts/campaign.json`

- [x] Add focused assertions for the authority-provenance rule, bounded bootstrap, debugging semantic-delta stop, staged-snapshot semantic firewall, and cheap commit loop.
- [x] Add one pressure scenario reproducing the temptation to infer “staged snapshot means do not roll marketplace source.”
- [x] Run the focused tests and record the expected RED failures before changing canonical instruction sources.

## Task 2: Implement the canonical authority contract

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/base-doctrine/references/operating-contract.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/using-superpowers-plus/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/systematic-debugging/SKILL.md`
- Modify: `codex-marketplace/plugins/agent-operating-model/skills/tracked-repo-hooks/SKILL.md`
- Modify: `codex-marketplace/plugins/repo-worker-pack/skills/repo-worker-base/references/repository-validation-contract.md`

- [x] Add the model-neutral distinction: evidence changes belief; only authority changes workflow meaning.
- [x] Require provenance for any new mode, branch, exception, flag, ceremony, or validation semantics.
- [x] Stop bootstrap expansion when no unresolved question can change the next lawful action.
- [x] Make semantic expansion a debugging red flag and clarify that reproduced failure authorizes repair, not new policy.
- [x] State that staged-snapshot markers identify the candidate tree and do not alter consumer command or marketplace-refresh semantics.
- [x] Express the existing cheap commit loop without creating a second validation path.
- [x] Run the focused tests and confirm GREEN.

## Task 3: Regenerate, pressure-check, validate, and publish

**Files:**
- Regenerate: marketplace manifests, installed `.agents/skills/` projections, and mesh/index surfaces owned by repository generators.
- Update: this plan’s checklist and lifecycle state.

- [x] Run `py -3 tools/run.py marketplace --apply`.
- [x] Run `py -3 tools/run.py installed-skills --apply` and `py -3 tools/run.py mesh --apply`.
- [x] Run the focused workflow-contract tests.
- [x] Run one GREEN pressure trial for `semantic-authority` and inspect its output against the rubric.
- [x] Review the diff against the scope and authority invariants.
- [x] Mark this plan `completed-awaiting-retirement` with every agent-owned item checked.
- [x] Stage the intended tree and make a normal hooked commit.
- [x] Push `codex/semantic-authority` and open a Draft PR into `main`.
- [x] Verify the remote PR head matches the committed local head and report the PR URL.
