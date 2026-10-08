# SemVer 1.0.0 Contract Timing Correction

**Goal:** Remove the AOM SemVer adoption prerequisite to declare future `1.0.0` compatibility guarantees, while preserving an explicit current `0.y.z` policy and requiring a stable contract when preparing the first `1.0.0` release.

**Execution strategy:** Execute inline in this worktree. The two canonical references express one linked obligation and must be corrected together before the plugin is regenerated.

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
