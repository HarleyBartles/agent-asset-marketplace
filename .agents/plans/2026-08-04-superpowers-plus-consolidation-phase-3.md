# Superpowers Plus Consolidation — Phase 3: Skill Script Contracts and Deployment Ownership

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `.agents/specs/2026-08-04-skill-script-cli-contract-design.md`

**Goal:** Make every skill-bundled script trustworthy through a self-describing CLI contract (`--help`, `--check`, safe-by-default), and move vendor profile deployment ownership to the correct skill (`repo-standards`).

**Architecture:** Skill-bundled scripts under `sources/first_party/skills/*/scripts/` become first-class, machine-discoverable tools. `repo-standards` owns one-shot canonical surface deployment (including `.agents/agents/` vendor profiles); `refreshing-installed-skills` stays responsible for recording `vendorProfiles` provenance.

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
- **Task 3** consumes the audit findings from Task 1 and the validator scaffold from Task 2; it runs after both.
- **Task 4** has no dependencies on Tasks 1–3.
- **Task 5** consumes the `repo-standards` script changes from Task 4; it runs after Task 4.
- **Final integration** runs after all five tasks are committed.

No parallel execution is expected; one subagent (or the orchestrator) runs each task to completion before starting the next.

---

### Task 1: Audit existing skill-bundled scripts

**Files:**
- Read:
  - `sources/first_party/skills/*/scripts/*`
  - `tools/AGENTS.md`
  - `docs/skill-standards-policy.md`
- Create:
  - `.agents/scratch/2026-08-04-skill-script-audit.md` (off-repo scratch, not committed)

**Consumes:** none.

**Interfaces:**
- A list of every first-party skill script that is missing `--help`, `--check`, or an `apply`/`check` mode distinction.
- Classification of each script as read-only, mutating, or mixed.
- A prioritized list of scripts to standardize in Task 2.

- [ ] **Step 1: Inventory all skill-bundled scripts.**

  Find every executable Python and shell script under `sources/first_party/skills/*/scripts/`. Record the path, current argument parser (if any), and whether it already supports `check`/`apply` or read-only mode.

- [ ] **Step 2: Evaluate each script against the CLI contract.**

  For each script, record:
  - Does it respond to `--help` with a description, flags, and mutation classification?
  - Does it support `--check` (or the same default-as-check behavior as `refresh_installed_skills.py`) that reports what it *would* do?
  - Does it have an `--apply` flag for the mutating path?
  - Does its `SKILL.md` document the script and its safe invocation?

- [ ] **Step 3: Produce the audit report.**

  Write the report to `Z:\_agent-worktrees\agent-asset-marketplace\_agents-scratch\consolidate-superpowers-plus-phase-3\2026-08-04-skill-script-audit.md`. Do not commit the scratch file; it is planning input for Task 2.

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

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

- [ ] **Step 1: Refactor the highest-priority scripts first.**

  Start with the scripts that are already invoked from skills (`refreshing-installed-skills`, `using-git-worktrees`, `requesting-code-review` if it has any). Add `argparse` with `--help`, `--check`, and `--apply`. Keep default behavior as `--check`. Classify every flag as read-only or mutating in help text.

- [ ] **Step 2: Add `SKILL.md` documentation for each updated script.**

  Under a new or existing "Bundled scripts" section, list each script, its purpose, and the canonical safe invocation (`<script> --check` or `<script> --help`).

- [ ] **Step 3: Update `docs/skill-standards-policy.md`.**

  Add the skill-bundled script CLI contract to the skill authoring standards. Reference the spec and `refresh_installed_skills.py` as the reference shape.

- [ ] **Step 4: Commit the script and doc changes.**

  Keep each skill's script + doc changes in one commit per skill to keep the history reviewable.

- [ ] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 3: Add a `repo-standards` validator for the script CLI contract

**Files:**
- Edit:
  - `sources/first_party/skills/repo-standards/SKILL.md`
  - `sources/first_party/skills/repo-standards/scripts/` (create `validate_skill_scripts.py` or extend existing `repo_standards.py`)
  - `tools/run` pipeline or `tools/validate_marketplace.py` if the validator should be part of `tools/run ci --check`
- Create:
  - `sources/first_party/skills/repo-standards/references/skill-script-contract-validator.md`

**Consumes:** Task 1 (script inventory) and Task 2 (reference shape).

**Interfaces:**
- `tools/run ci --check` validates that every first-party skill script responds to `--help` and `--check` with the expected exit codes.
- The validator reports which scripts are non-compliant and stops the CI preflight.
- `repo-standards/SKILL.md` tells agents how to run the validator and how to fix a failure.

- [ ] **Step 1: Design the validator.**

  The validator should:
  - Walk `sources/first_party/skills/*/scripts/*`.
  - For each executable script, run `<script> --help` and expect exit `0` plus a description and flag list.
  - Run `<script> --check` and expect a meaningful exit code (`0` if no changes needed, non-zero if the script would need to act, `2` for unknown args).
  - Produce a machine-readable report of `OK` / `FAIL` per script.

- [ ] **Step 2: Implement the validator as a `repo-standards` script.**

  Place it under `sources/first_party/skills/repo-standards/scripts/` and wire it into the `tools/run` target list so `ci --check` calls it. Name it consistently with other `repo-standards` scripts.

- [ ] **Step 3: Update `repo-standards/SKILL.md`.**

  Add the validator to the "Read when" table and a "How to fix" note. Keep the skill body under the 500-word limit; move details to the new `references/skill-script-contract-validator.md`.

- [ ] **Step 4: Run the validator in check mode.**

  Run `tools/run repo-standards --check` (or the equivalent target) against the branch. Fix any newly discovered contract gaps in Task 2 scripts before committing.

- [ ] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/repo-standards tools/run docs/skill-standards-policy.md
  git diff --stat
  git commit -m "feat(repo-standards): add skill-bundled script CLI contract validator"
  ```

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

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

- [ ] **Step 1: Extract the profile deployment logic from `refresh_installed_skills.py`.**

  Move `_vendor_profiles_are_current`, `_vendor_profile_source_dir`, `_install_plugin_vendor_profiles`, and `_clean_orphan_vendor_profiles` out of `refresh_installed_skills.py`. Keep the call to the new `repo-standards` script so `refreshing-installed-skills` still triggers deployment and records provenance.

- [ ] **Step 2: Create the `repo-standards` deployment script.**

  Add a script under `sources/first_party/skills/repo-standards/scripts/` (e.g., `deploy_vendor_profiles.py`) that:
  - Discovers `assets/profiles/*.md` in installed plugin packs.
  - Copies each profile to `.agents/agents/` only if it does not already exist.
  - Removes orphan profiles from `.agents/agents/` that no longer have a source in any pack.
  - Supports `--check` and `--apply`.

- [ ] **Step 3: Update skill docs.**

  Update `refreshing-installed-skills/SKILL.md` and `repo-standards/SKILL.md` to state the new ownership. Keep `selecting-a-subagent/references/vendor-profile-packaging.md` accurate.

- [ ] **Step 4: Test the new split.**

  Run `tools/run installed-skills --check` and the new `repo-standards` check to ensure the profiles are still deployed correctly and provenance is recorded.

- [ ] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/refreshing-installed-skills sources/first_party/skills/repo-standards sources/first_party/skills/selecting-a-subagent
  git diff --stat
  git commit -m "refactor: move vendor profile deployment ownership to repo-standards"
  ```

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

### Task 5: Register new/updated skills and regenerate surfaces

**Files:**
- Generated:
  - `codex-marketplace/plugins/*/references/bundle-manifest.json`
  - `.agents/skills/` installed copies
  - `repo-index/repo-index.json`
  - `codex-marketplace/manifest.json`
  - `.agents/plugins/marketplace.json`
  - mesh `INDEX.md` files

**Consumes:** Tasks 2–4 (source and doc changes).

**Interfaces:**
- All source changes are reflected in the marketplace and installed skills.
- `tools/run ci --check` passes on the fully staged tree.

- [ ] **Step 1: Regenerate the marketplace.**

  ```bash
  .\tools\run.ps1 marketplace --apply
  ```

- [ ] **Step 2: Run CI preflight on the staged tree.**

  Stage all changes and commit. The pre-commit hook will run `tools/run ci --check`.

  ```bash
  git add -A
  git commit -m "chore: regenerate marketplace for phase 3 plan"
  ```

- [ ] **Step 3: Mark this task `[x]` in this plan before reporting back.**

---

## Final integration

- [ ] **Step 1: Run final CI.**

  Ensure `tools/run ci --check` is green after the last commit.

- [ ] **Step 2: Push the branch.**

  ```bash
  git push
  ```

- [ ] **Step 3: Open a draft PR into `main`.**

  Follow `.agents/guides/pr-guide.md` `## Draft PR policy`. The PR body should reference this plan and the script CLI contract spec.

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

## Follow-up and roadmap

The design spec also lists these longer-term items as "Phase 3 and beyond":

- Moving `report-hygiene` into the consolidated Superpowers surface.
- Folding `mark-skill-authoring` into `writing-skills` or retirement with a deprecation note.
- Refreshing the body of `using-superpowers-plus` without renaming it (the name stays; the body changes to match the new routing contract).

These are intentionally **out of scope** for this plan so Phase 3 stays shippable and focused on the script CLI contract and vendor profile ownership.
