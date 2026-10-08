# SemVer 1.0.0 Contract Timing and Draft CI Correction

**Goal:** Remove the AOM SemVer adoption prerequisite to declare future `1.0.0` compatibility guarantees, preserve an explicit current `0.y.z` policy, and skip hosted validation jobs for draft PR events.

**Execution strategy:** Execute inline in this worktree. The SemVer source and generated projection form one documentation change; the workflow guard remains isolated in its own file and the tracked commit hook validates the complete staged tree.

Status: completed-awaiting-retirement.

## Task 1: Correct canonical SemVer guidance

**Files:** `skills/semver/references/standard.md` and `skills/semver/references/adoption-and-versioning.md`.

- [x] Clarify that an adopter below `1.0.0` documents the current initial-development compatibility and version policy; it is not required to define or promise the future stable API in advance.
- [x] Clarify that the repository publishes the compatibility contract when preparing its first `1.0.0` release, and do not imply calendar time or a version string proves readiness.
- [x] Keep SemVer's current `0.y.z` compatibility semantics and all independent version-source/build obligations intact.

## Task 2: Regenerate and validate

**Files:** Generated AOM plugin output under `dist/plugins/agent-operating-model/`.

- [x] Run `py -3 tools/run.py marketplace --apply` and inspect the generated SemVer references.
- [x] Run focused SemVer/skill-authority validation and the repository canonical `py -3 tools/run.py ci --check`.
- [x] Confirm no remaining normative text makes advance declaration of future `1.0.0` guarantees an adoption or certification prerequisite.

## Task 3: Skip hosted validation while a pull request is draft

**Files:** `.github/workflows/marketplace-validation.yml`.

- [x] Add a job condition that skips only `pull_request` events whose PR is draft while retaining validation for Ready PR events and non-PR events.
- [x] Run the focused hosted workflow test and preserve the full repository check result from the tracked commit hook.
