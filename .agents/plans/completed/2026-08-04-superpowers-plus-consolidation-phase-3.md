# Superpowers Plus Consolidation — Phase 3: Skill Script Contracts, Deployment Ownership, and Doctrine Thinning

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Specs:**
- `.agents/specs/2026-08-04-skill-script-cli-contract-design.md`
- `.agents/specs/2026-08-04-superpowers-plus-consolidation-design.md`

**Goal:** In a single phase, deliver (1) the skill-bundled script CLI contract (`--help`, `--check`, safe-by-default) plus `repo-standards` validator and vendor profile deployment ownership, and (2) the doctrine and guide thinning work that the consolidation design spec already assigned to Phase 3.

**Architecture:** Skill-bundled scripts under `sources/first_party/skills/*/scripts/` become first-class, machine-discoverable tools. `repo-standards` owns one-shot canonical surface deployment (including `.agents/agents/` vendor profiles); `refreshing-installed-skills` stays responsible for recording `vendorProfiles` provenance. `report-hygiene` folds into `writing-with-clarity`, `mark-skill-authoring` folds into `writing-skills`, and guide/policy documents are thinned to deltas.

**Tech Stack:** Python skill scripts, argparse, `tools/run` deterministic build pipeline, markdown skill docs.

## Global Constraints

- Do not break existing `check`/`apply` conventions; extend them.
- Do not delete or rename skills already installed in other repos without deprecation notes.
- Edit source first, then regenerate; never hand-edit generated plugin trees, bundle manifests, or index files.
- Every `tools/run * --apply` step must be followed by a commit before the next `tools/run ci --check`.
- All source edits are committed before marketplace regeneration begins.
- Keep each commit focused on one task; the final task is the validation commit.

## Task ordering

Run the tasks in the order listed. The main ordering constraints are:

- **Task 1** has no dependencies.
- **Task 2** consumes the new script contract shape from Task 1; it runs after Task 1.
- **Task 3** consumes the audit findings from Task 1 and the reference shape from Task 2; it runs after both.
- **Task 4** has no dependencies on Tasks 1–3.
- **Tasks 5–7** are the doctrine-thinning work and can run in any order after Task 1; they are listed in the recommended order.
- **Final integration** runs after all source and script work is committed.

No parallel execution is expected; one subagent (or the orchestrator) runs each task to completion before starting the next.

---

### Task 1: Audit existing skill-bundled scripts

**Files:**
- Read:
  - `sources/first_party/skills/*/scripts/*`
  - `tools/AGENTS.md`
  - `docs/skill-standards-policy.md`
- Create:
  - `Z:\_agent-scratch\consolidate-superpowers-plus-phase-3\2026-08-04-skill-script-audit.md` (off-repo scratch, not committed)

**Consumes:** none.

**Interfaces:**
- A list of every first-party skill script that is missing `--help`, `--check`, or an `apply`/`check` mode distinction.
- Classification of each script as **read-only**, **mutating**, or **mixed**.
- A prioritized list of scripts to standardize in Task 2.

**Preliminary inventory (to be verified/updated by the audit):**

The known first-party skill scripts are under these directories:

- `generating-agent-mesh/scripts/`
  - `generate_index_mesh.py` — already supports `--check`/`--apply`
  - `validate_agent_mesh.py` — already supports `--check`/`--apply`
  - `generate-index-mesh.ps1`, `generate-index-mesh.sh`, `validate-agent-mesh.ps1`, `validate-agent-mesh.sh` — shell wrappers
- `refreshing-installed-skills/scripts/`
  - `refresh_installed_skills.py` — already supports `--check`/`--apply`, reference shape for the contract
- `repo-standards/scripts/`
  - `repo_standards.py` — already supports `--check`/`--apply`
  - Many `scaffold_*.py` / `scaffold-*.sh` / `scaffold-*.ps1` scaffolders
- `using-git-worktrees/scripts/`
  - `new_worktree.py` — has `argparse`, needs `--check`/`--apply` distinction
  - `remove_worktree.py` — has `argparse`, needs `--check`/`--apply` distinction
- `subagent-driven-development/scripts/`
  - `sdd-workspace`, `task-brief`, `review-package` and their `.ps1` wrappers
- `systematic-debugging/scripts/`
  - `find-polluter.ps1`
- `unslop-engine/scripts/`
  - `unslop.py`, `validate_package.py`, `validate_unslop_output.py`

- [x] **Step 1: Verify the inventory and classify each script.**

  For every first-party skill script under `sources/first_party/skills/*/scripts/`, record:
  - Path and language (Python, PowerShell, shell).
  - Current argument parser (if any).
  - Whether it already supports `--help`, `--check`, and `--apply`.
  - **Classification:**
    - `read-only` — the script never writes to source, generated surfaces, or the repo when run with any supported flags.
    - `mutating` — the script has an `--apply` mode that writes files or changes repo state.
    - `mixed` — the script supports both read-only (`--check`/`--help`) and mutating (`--apply`) paths; this is the standard shape for skill-bundled tools.

- [x] **Step 2: Produce the prioritized audit report.**

  Write the report to `Z:\_agent-scratch\consolidate-superpowers-plus-phase-3\2026-08-04-skill-script-audit.md`. Do not commit the scratch file; it is planning input for Task 2.

  Priority for Task 2 is: scripts invoked from `SKILL.md` or other skills first, then scaffolders and utilities.

- [x] **Step 3: Mark this task `[x]` in this plan before reporting back.**

---

### Task 2: Standardize the first set of skill-bundled scripts

**Files:**
- Edit (as identified by the audit):
  - `sources/first_party/skills/<skill-name>/scripts/*.py` and `*.sh`
  - `sources/first_party/skills/<skill-name>/SKILL.md` for each updated skill
- Create:
  - `sources/first_party/skills/<skill-name>/references/cli-usage.md` for any non-trivial script

**Consumes:** Task 1 (audit list and prioritization).

**Interfaces:**
- Every updated script follows the contract from `.agents/specs/2026-08-04-skill-script-cli-contract-design.md`.
- Each script's `SKILL.md` references the script and its safe invocation.
- `docs/skill-standards-policy.md` is updated to require the contract for all new skill scripts.

**Scope definition:**

The "first set" is the scripts that are explicitly referenced by skill instructions or by other skill scripts and are not already fully compliant. Start with the following known candidates (confirm against the audit):

- `using-git-worktrees/scripts/new_worktree.py` — add `--help`, make default behavior `--check`, add `--apply`.
- `using-git-worktrees/scripts/remove_worktree.py` — add `--help`, make default behavior `--check`, add `--apply`.
- Any `subagent-driven-development/scripts/*` helpers that are invoked from `SKILL.md`.
- Any `repo-standards/scripts/scaffold_*.py` scripts that currently lack `--help`.

Scaffolders and one-off utilities may be deferred if they are not invoked from active skills.

- [x] **Step 1: Refactor the highest-priority scripts first.**

  Add `argparse` with `--help`, `--check`, and `--apply`. Keep default behavior as `--check`. Classify every flag as `read-only` or `mutating` in help text. Add the `read-only`/`mutating`/`mixed` classification to the help header.

- [x] **Step 2: Add `SKILL.md` documentation for each updated script.**

  Under a new or existing "Bundled scripts" section, list each script, its purpose, and the canonical safe invocation (`<script> --check` or `<script> --help`).

- [x] **Step 3: Update `docs/skill-standards-policy.md`.**

  Add the skill-bundled script CLI contract to the skill authoring standards. Reference the spec and `refresh_installed_skills.py` as the reference shape.

- [x] **Step 4: Commit the script and doc changes.**

  Keep each skill's script + doc changes in one commit per skill to keep the history reviewable.

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 3: Add a `repo-standards` validator for the script CLI contract

**Files:**
- Edit:
  - `sources/first_party/skills/repo-standards/SKILL.md`
  - `sources/first_party/skills/repo-standards/scripts/` (create `validate_skill_scripts.py`)
  - `tools/run` pipeline (add the validator to the `ci --check` target set)
- Create:
  - `sources/first_party/skills/repo-standards/references/skill-script-contract-validator.md`

**Consumes:** Task 1 (script inventory) and Task 2 (reference shape).

**Interfaces:**
- `tools/run ci --check` validates that every first-party skill script responds to `--help` and `--check` with the expected exit codes.
- The validator reports which scripts are non-compliant and stops the CI preflight.
- `repo-standards/SKILL.md` tells agents how to run the validator and how to fix a failure.

**Integration path:**

The validator is a new `repo-standards` script (`validate_skill_scripts.py`) that is invoked by `tools/run ci --check` as one of the standard preflight checks. It is not part of `tools/validate_marketplace.py`.

- [x] **Step 1: Design the validator.**

  The validator should:
  - Walk `sources/first_party/skills/*/scripts/*`.
  - For each executable script, run `<script> --help` and expect exit `0` plus a description and flag list.
  - Run `<script> --check` and expect a meaningful exit code (`0` if no changes needed, non-zero if the script would need to act, `2` for unknown args).
  - Produce a machine-readable report of `OK` / `FAIL` per script.

- [x] **Step 2: Implement the validator as a `repo-standards` script.**

  Place it under `sources/first_party/skills/repo-standards/scripts/` and wire it into the `tools/run` target list so `ci --check` calls it. Name it consistently with other `repo-standards` scripts.

- [x] **Step 3: Update `repo-standards/SKILL.md`.**

  Add the validator to the "Read when" table and a "How to fix" note. Keep the skill body under the 500-word limit; move details to the new `references/skill-script-contract-validator.md`.

- [x] **Step 4: Run the validator in check mode and fix any regressions.**

  Run `tools/run repo-standards --check` (or the equivalent target) against the branch. Fix any newly discovered contract gaps in Task 2 scripts before committing. Add unit or integration tests for the validator in `tests/` if the repo has a testing convention for `repo-standards` scripts.

- [x] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/repo-standards tools/run
  git diff --stat
  git commit -m "feat(repo-standards): add skill-bundled script CLI contract validator"
  ```

- [x] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

### Task 4: Move vendor profile deployment ownership to `repo-standards`

**Files:**
- Edit:
  - `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
  - `sources/first_party/skills/refreshing-installed-skills/SKILL.md`
  - `sources/first_party/skills/repo-standards/SKILL.md`
  - `sources/first_party/skills/repo-standards/scripts/` (create or extend)
  - `sources/first_party/skills/selecting-a-subagent/references/vendor-profile-packaging.md` if needed
- Create:
  - `sources/first_party/skills/repo-standards/references/vendor-profile-deployment.md`

**Consumes:** none.

**Interfaces:**
- `repo-standards` owns the one-shot deployment of `codex-marketplace/plugins/*/assets/profiles/*.md` into `.agents/agents/`.
- `refreshing-installed-skills` still records `vendorProfiles` provenance in `.agents/skills/.provenance.json`.
- The default installed profile set remains the same five canonical profiles.

**Implementation note:**

In `refresh_installed_skills.py` the relevant helpers are `def _vendor_profiles_are_current`, `def _is_vendor_profile_file`, `def _vendor_profile_source_dir`, `def _install_plugin_vendor_profiles`, and `def _clean_orphan_vendor_profiles`. Verify the exact line numbers and signatures before moving; the plan expects these names but treat them as a pointer to the current implementation, not a hard contract.

- [x] **Step 1: Extract the profile deployment logic from `refresh_installed_skills.py`.**

  Move the vendor-profile discovery, install-if-missing, and orphan-cleanup logic out of `refresh_installed_skills.py`. Keep the call to the new `repo-standards` script so `refreshing-installed-skills` still triggers deployment and records provenance.

- [x] **Step 2: Create the `repo-standards` deployment script.**

  Add a script under `sources/first_party/skills/repo-standards/scripts/` (e.g., `deploy_vendor_profiles.py`) that:
  - Discovers `assets/profiles/*.md` in installed plugin packs.
  - Copies each profile to `.agents/agents/` only if it does not already exist.
  - Removes orphan profiles from `.agents/agents/` that no longer have a source in any pack.
  - Supports `--check` and `--apply`.

- [x] **Step 3: Update skill docs.**

  Update `refreshing-installed-skills/SKILL.md` and `repo-standards/SKILL.md` to state the new ownership. Keep `selecting-a-subagent/references/vendor-profile-packaging.md` accurate.

- [x] **Step 4: Test the new split.**

  Run `tools/run installed-skills --check` and the new `repo-standards` check to ensure the profiles are still deployed correctly and provenance is recorded. Add a test or pressure scenario under `tests/pressure/` if appropriate.

- [x] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/refreshing-installed-skills sources/first_party/skills/repo-standards sources/first_party/skills/selecting-a-subagent
  git diff --stat
  git commit -m "refactor: move vendor profile deployment ownership to repo-standards"
  ```

- [x] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

### Task 5: Move `report-hygiene` into `writing-with-clarity`

**Files:**
- Read:
  - `sources/first_party/skills/report-hygiene/SKILL.md`
  - `sources/first_party/skills/writing-with-clarity/SKILL.md`
- Edit:
  - `sources/first_party/skills/writing-with-clarity/SKILL.md`
  - `sources/first_party/skills/writing-with-clarity/references/report-hygiene-checklist.md` (new)
  - `codex-marketplace/custody-pack-registry.json` (retire `report-hygiene` from its pack)
- Create:
  - `provenance/2026-08-04-report-hygiene-retired.md` (or equivalent) noting the retirement

**Consumes:** none.

**Interfaces:**
- `report-hygiene` is no longer a standalone skill.
- `writing-with-clarity` includes a "Hygiene" or "Before publishing" step that covers the same checks.
- No first-party skill references `report-hygiene` after this task.

- [x] **Step 1: Read `report-hygiene` and extract its contract.**

  List the checks and triggers it provides. Keep the content minimal; do not copy the whole body.

- [x] **Step 2: Add a hygiene section to `writing-with-clarity/SKILL.md`.**

  Surface the same checks as a step in the writing/review flow. Move detailed guidance to `references/report-hygiene-checklist.md`.

- [x] **Step 3: Retire `report-hygiene` from the marketplace registry.**

  Remove the skill from `codex-marketplace/custody-pack-registry.json` and add a provenance note documenting the retirement.

- [x] **Step 4: Commit.**

  ```bash
  git add sources/first_party/skills/writing-with-clarity codex-marketplace/custody-pack-registry.json provenance
  git diff --stat
  git commit -m "refactor: fold report-hygiene into writing-with-clarity"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 6: Fold `mark-skill-authoring` into `writing-skills`

**Files:**
- Read:
  - `sources/first_party/skills/mark-skill-authoring/SKILL.md`
  - `sources/first_party/skills/writing-skills/SKILL.md`
- Edit:
  - `sources/first_party/skills/writing-skills/SKILL.md`
  - `sources/first_party/skills/writing-skills/references/skill-authoring-checklist.md` (new)
  - `codex-marketplace/custody-pack-registry.json` (retire `mark-skill-authoring`)
- Create:
  - `provenance/2026-08-04-mark-skill-authoring-retired.md` (or equivalent)

**Consumes:** none.

**Interfaces:**
- `mark-skill-authoring` is no longer a standalone skill.
- `writing-skills` owns the skill-authoring checklist and scaffolder guidance.
- No first-party skill references `mark-skill-authoring` after this task.

- [x] **Step 1: Read `mark-skill-authoring` and extract its contract.**

  Identify the authoring checklist and any scaffolder references. Keep the content minimal.

- [x] **Step 2: Add a skill-authoring section to `writing-skills/SKILL.md`.**

  Surface the authoring workflow inside `writing-skills`. Move detailed guidance to `references/skill-authoring-checklist.md`.

- [x] **Step 3: Retire `mark-skill-authoring` from the marketplace registry.**

  Remove the skill from `codex-marketplace/custody-pack-registry.json` and add a provenance note documenting the retirement.

- [x] **Step 4: Commit.**

  ```bash
  git add sources/first_party/skills/writing-skills codex-marketplace/custody-pack-registry.json provenance
  git diff --stat
  git commit -m "refactor: fold mark-skill-authoring into writing-skills"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 7: Thin `code-review-guide.md` and `skill-standards-policy.md`

**Files:**
- Edit:
  - `docs/code-review-guide.md`
  - `docs/skill-standards-policy.md`
  - `sources/first_party/skills/requesting-code-review/SKILL.md` (if it references the guide)
  - `sources/first_party/skills/writing-skills/SKILL.md` (if it references the policy)
- Create:
  - `docs/code-review-guide.md` delta entries, or move detail to `.agents/guides/code-review-guide.md` if applicable
  - `docs/skill-standards-policy.md` delta entries

**Consumes:** Task 6 (fold `mark-skill-authoring`) and Task 2 (script contract standard, which updates `skill-standards-policy.md`).

**Interfaces:**
- `docs/code-review-guide.md` and `docs/skill-standards-policy.md` are reduced to deltas from the root `AGENTS.md` and skill-specific references. Remove duplicated guidance; point to canonical skills instead.
- No information is lost; it is moved to the appropriate skill `SKILL.md` or `references/` file.

- [x] **Step 1: Audit duplication in both guides.**

  Identify sections that are already stated in root `AGENTS.md`, `.agents/guides/code-review-guide.md`, or first-party skill references.

- [x] **Step 2: Thin `code-review-guide.md`.**

  Remove duplicated content and replace with routing pointers. Keep only repo-local deltas.

- [x] **Step 3: Thin `skill-standards-policy.md`.**

  Remove duplicated content and replace with routing pointers. Keep the script CLI contract (from Task 2) as the primary new content.

- [x] **Step 4: Update skill references.**

  If `requesting-code-review/SKILL.md` or `writing-skills/SKILL.md` points to the old thinned sections, repoint them to the new canonical locations.

- [x] **Step 5: Commit.**

  ```bash
  git add docs sources/first_party/skills/requesting-code-review sources/first_party/skills/writing-skills
  git diff --stat
  git commit -m "docs: thin code-review-guide and skill-standards-policy to deltas"
  ```

- [x] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

## Final integration

- [x] **Step 1: Regenerate the marketplace.**

  ```bash
  .\tools\run.ps1 marketplace --apply
  ```

- [x] **Step 2: Run CI preflight on the staged tree.**

  Stage all changes and commit. The pre-commit hook will run `tools/run ci --check`.

  ```bash
  git add -A
  git commit -m "chore: regenerate marketplace for phase 3 plan"
  ```

- [x] **Step 3: Push the branch.**

  ```bash
  git push
  ```

- [x] **Step 4: Ensure the PR remains in draft until human review.**

  The PR at https://github.com/HarleyBartles/agent-asset-marketplace/pull/248 should stay draft until a human is ready to merge.

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

## Notes for the next consolidation phase

- **Remove the `review-branch-diff` skill.** This skill is a leftover local review helper. The Phase 3 branch review was performed by a `subagent_explore`-based reviewer, not by invoking the skill, and the skill's local source is not part of the repo's first-party or marketplace custody. Plan its retirement, removal from installed skill surfaces, and a short provenance note in the next phase.
