# Writing Pack Ambient Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Writing Pack safe to use as an ambient plugin and leave this repository with no vendored plugin subscriptions or installed skill projection.

**Architecture:** Keep Writing Pack’s canonical skills and shipped plugin package available to ambient agents. Remove it from this repository’s default installation policy, preserve `repo.local_skills: []`, and make zero installed plugins plus zero local skills a supported state in refresh, CI, hooks, and worktree setup. Repository-owned checks must use repository-owned or deployed standard resources rather than installed skill copies.

**Tech Stack:** Python, JSON marketplace and standards contracts, generated plugin outputs, tracked Git hooks, pytest.

**Spec:** `.agents/specs/2026-09-28-ambient-operating-model-and-selectable-standards-design.md`; durable boundaries in `docs/decisions/0005-selectable-agent-operating-standards.md` and `docs/decisions/0007-ambient-plugin-boundaries-and-capability-workflows.md`. This plan extends the earlier five-pack boundary to Writing Pack by explicit user direction.

**Execution Strategy:** `executing-plans`; the policy change, empty projection behavior, and consumer checks form one sequential migration.

**Status:** in-flight

## Global Constraints

- Keep all marketplace products, including Writing Pack, available in the product catalog and generated distribution.
- This repository declares no repository-local skills and subscribes to no marketplace plugin for local skill projection. Ambient runtime access is sufficient.
- Keep CI and hooks owned by this repository. They must not depend on Codex ambient plugins being present in hosted CI.
- Do not replace capability-based use with exact ambient skill names in repository runbooks or playbooks. Genuine missing required capabilities must still stop clearly.
- Do not change consumer repositories in this slice.
- Retire the completed predecessor planning artifacts in the first implementation commit; durable decisions are already recorded in ADRs and current doctrine.

## Review Focus

- Does Writing Pack or any of its four skills assume consumer `.agents/` layout, runbook/playbook names, or marketplace subscription state?
- Does an empty installed-plugin and local-skill selection leave `.agents/skills/` absent and pass check/apply, CI, hook staging, and worktree initialization without creating recurring drift?
- Do all repository-owned formatter, validator, scaffold, and test paths continue to work without `.agents/skills/`?
- Are generated outputs rebuilt from canonical source, with Writing Pack still shipped and listed as available?

______________________________________________________________________

## Task 1: Retire completed predecessor plans

- [x] Remove `.agents/plans/ambient-operating-model/roadmap.md` and the five completed plans in that directory: `2026-09-28-retire-generated-index-mesh.md`, `2026-09-28-selectable-standards-runner-bridge.md`, `2026-09-29-ambient-pack-boundaries-and-capability-workflows.md`, `2026-09-29-marketplace-migration-and-source-release.md`, and `2026-09-29-marketplace-self-subscription.md`.
- [x] Confirm no current tracked guidance points to those retired plan paths; preserve durable policy only in ADRs, doctrine, runbooks, and contracts.

## Task 2: Audit Writing Pack ambient assumptions

- [x] Review `src/plugin-definitions/writing-pack/`, all four canonical skills under `skills/writing/`, `skills/writing-profile-engine/`, `skills/writing-style/`, and `skills/writing-with-clarity/`, plus their shipped tests and plugin README.
- [x] Search for assumptions about consumer directory layout, repository runbooks/playbooks, or installed marketplace subscriptions. Retain internal composition among Writing Pack’s own skills; replace any consumer-specific assumption with runtime capability discovery and an explicit stop when a required capability is unavailable.
- [x] Remove the installed-copy dependency in `skills/writing-profile-engine/tests/scripts/test_writing_profile_engine.py`; exercise the canonical or built self-contained package in a temporary location so source tests do not require this repository to install Writing Pack.
- [ ] Record audit findings in the implementation PR summary, including any assumptions found and their disposition.

## Task 3: Support a repository with no skill projections

- [ ] Change `src/plugin-definitions/marketplace-policy.json` to set `install_defaults` to `[]`; keep `repo.local_skills` empty in `.agents/plugins/marketplace.json` and keep Writing Pack in the catalog as `AVAILABLE`.
- [ ] Update `skills/refreshing-installed-skills/scripts/refresh_installed_skills.py` so an empty plugin selection and empty local-skill declaration cleanly remove stale managed skill projections and provenance, leave `.agents/skills/` absent, and are stable in both `--apply` and `--check` modes.
- [ ] Update the installed-skill projection standard and generated-path declarations so the repository verifies that no vendored or local skills are present without requiring a provenance file or an empty directory.
- [ ] Review `githooks/pre-commit`, `skills/using-git-worktrees/scripts/new_worktree.py`, `.agents/doctrine/skills.md`, `.agents/doctrine/repo-local-plugin-marketplace.md`, and `.agents/doctrine/custody-and-marketplace-doctrine.md`; remove assumptions that a non-empty projection exists while preserving refresh, stale-file cleanup, and worktree behavior.
- [ ] Remove installed-path dependencies from marketplace-owned utilities, including `tools/new_plugin.py`, `tools/sync_skill_shared_references.py`, `skills/repo-shape/scripts/repo_standards.py`, and `skills/repo-shape/scripts/scaffold_markdown_formatting.py`. Use the declared deployed Markdown Formatting standard resource where that is the owning interface.
- [ ] Update repository Markdown Formatting authority paths in `.agents/contracts/markdown-formatting.json` so checks do not expect Writing Pack copies under `.agents/skills/`.

## Task 4: Rebuild and validate the ambient boundary

- [ ] Update focused source tests for empty projection behavior, worktree refresh behavior, and any changed formatter/tool resolution. Keep behavior tests meaningful and avoid tautological or change-detector coverage.
- [ ] Regenerate marketplace registry and plugin distribution from canonical sources with `py -3 tools/run.py marketplace --apply`; reconcile the skill projection through the owning refresh command.
- [ ] Run focused tests for the changed source owners, then the repository’s prescribed complete gate: stage intended changes, commit through the tracked hook, and inspect its staged-snapshot apply/check evidence. Use `py -3 tools/run.py ci --check` only if an uncommitted verification or diagnosis is needed.
- [ ] Verify `.agents/skills/` is absent, `repo.local_skills` and `install_defaults` are empty, Writing Pack remains available and self-contained in `dist/plugins/writing-pack`, and hosted CI uses only repository-owned/deployed resources.
- [ ] Review the full diff and ambient-safety audit findings, then publish a Draft PR with exact head and validation evidence.

## Handoff

Use the `codex/writing-pack-ambient-migration` worktree. This plan covers marketplace source and this repository’s own installation boundary only. Do not implement consumer-repository migrations here.
