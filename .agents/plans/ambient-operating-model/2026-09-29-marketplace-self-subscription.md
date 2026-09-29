# Marketplace Self-Subscription and CI Cutover Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Declare this repository's operating standards and remove installed copies of its five ambient plugins.

**Architecture:** Pin and deploy only selected Agent Operating Model checker resources under `.agents/standards/`, then dispatch them through this repository's CI runner. Keep marketplace registry and installed skill projection checks repository-owned. The plugin catalog remains intact and Writing Pack stays installed.

**Tech Stack:** Python, JSON contracts, PowerShell/Git, tracked pre-commit hook.

**Spec:** `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md`

**Execution Strategy:** `executing-plans` because deployment, runner cutover, and projection removal are sequential.

**Status:** executing

**Goal:** Make this marketplace repository declare the Agent Operating Model standards it enforces, run their deployed checker resources through its own CI command bus, and stop installing copies of the five ambient plugins into `.agents/skills/`.

**Context:** PR #338 made standards selectable, but this repository still has no `.agents/contracts/operating-standards.json`. `tools/run.py ci` calls `repo_standards.py` from the installed Agent Operating Model skill. The local marketplace policy marks Agent Operating Model, Superpowers+, Repo Worker Pack, MCP Usage Pack, and Unslop+ as `INSTALLED_BY_DEFAULT`. The repository is itself the marketplace source, so its legacy exemption from a `marketplace-source` submodule makes the automatic standards migration preview fail on a partially enabled `marketplace-skill-management` standard.

**Scope:** Change only this repository's composition, CI runner, local marketplace policy, generated registry, and installed projections. Keep all five products available in the marketplace catalog. Keep `writing-pack` as the locally installed plugin. Keep this repository's existing shape, hook, runbook, playbook, and marketplace checks effective.

## Task 1: Record explicit standards adoption

- [ ] Declare the marketplace standards corresponding to the repo's currently enforced surfaces, excluding the self-submodule standard that cannot apply here. Declare repository-owned marketplace registry and skill projection checks separately.
- [ ] Deploy only selected checker resources into `.agents/standards/` with provenance tied to an immutable marketplace source commit. Preserve the source repo's self-submodule exception.
- [ ] Route `tools/run.py repo-standards` to the deployed dispatcher and verify the declared selection executes without an installed Agent Operating Model skill.

## Task 2: Retire ambient plugin projections

- [ ] Change `src/plugin-definitions/marketplace-policy.json` so the five ambient products are `AVAILABLE` rather than installed by default; keep `writing-pack` installed by default.
- [ ] Regenerate `.agents/plugins/marketplace.json`, `dist/manifest.json`, and `.agents/skills/` through their owners. Verify provenance lists only `writing-pack` and no ambient skill directories remain.
- [ ] Move repository runner and instruction references away from removed installed skill paths. Keep hosted and local check/apply commands owned by this repository.

## Task 3: Prove CI and publish a Draft PR

- [ ] Verify selected standard checks, registry generation, and installed projection refresh on the changed tree. Confirm the canonical source and shipped ambient products remain present.
- [ ] Commit through the tracked hook and inspect the staged-snapshot apply/check result. Review the final diff for ambient runtime dependencies and accidental loss of existing checks.
- [ ] Push and open a Draft PR with the exact head, validation evidence, and the remaining hosted-CI boundary. Leave the PR Draft for review.

## Handoff

Use the existing `codex/remove-ambient-plugin-projections` worktree. The canonical marketplace source under `skills/` remains first-party product source; `.agents/standards/` is the repo-controlled deployed checker surface; `.agents/skills/` is an installed projection. The selected standards and local registry/projection checks must run in hosted CI without Codex ambient plugins.
