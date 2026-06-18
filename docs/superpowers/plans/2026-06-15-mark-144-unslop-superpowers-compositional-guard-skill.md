# unslop-superpowers Compositional Guard Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a first-party `unslop-superpowers` guard skill in House Skills and project it into Superpowers so `linear-superpowers` and `github-superpowers` can use repo-specific anti-slop controls without replacing the existing `@unslop` profile generator.

**Architecture:** Keep `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/` as the canonical editable source. Project the same skill into `codex-marketplace/plugins/superpowers/skills/unslop-superpowers/` using the existing source-backed Superpowers projection pattern, then update the house-skills and superpowers bundle metadata, provenance notes, validator coverage, and generated `skill.zip` artifacts. Do not add a GPT overlay unless validation proves a concrete GPT-only compatibility gap.

**Tech Stack:** Markdown skill sources, YAML skill metadata, JSON manifests/ledgers, Python validation and packaging scripts, generated `skill.zip` artifacts.

---

### Task 1: Add the first-party House Skills source

**Files:**
- Create: `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/agents/openai.yaml`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- Modify: `codex-marketplace/plugins/house-skills/README.md`
- Modify: `provenance/house-skills.md`

- [x] **Step 1: Add the new source skill**

Create a House Skills `unslop-superpowers` entry that starts with `@using-superpowers`, names `@unslop` as the specialist profile-analysis engine, and keeps the composition narrow to profile discovery, smallest-safe action selection, repo-specific anti-slop controls, non-goals, and evidence requirements.

- [x] **Step 2: Register the source record**

Add matching decision and intake rows so the canonical source path is recorded as the House Skills file and the provenance notes explain that this is a first-party compositional guard skill rather than a replacement for `unslop`.

- [x] **Step 3: Update the House Skills inventory**

Increment the bundle manifest skill count, add the new live root to the inventory, add the corresponding source-map row, and adjust the House Skills README wording if it still reports the old skill total or omits the new guard skill.

- [x] **Step 4: Record provenance**

Add a provenance entry that points at the new House Skills source path and explains that `@unslop` remains the profile generator while `unslop-superpowers` is the compositional guard.

### Task 2: Project the skill into Superpowers

**Files:**
- Create: `codex-marketplace/plugins/superpowers/skills/unslop-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`

- [x] **Step 1: Mirror the projected skill**

Copy the House Skills `unslop-superpowers` skill into the Superpowers bundle so the projection stays source-backed and editable in House Skills.

- [x] **Step 2: Update bundle metadata**

Add a first-party projection entry in the Superpowers bundle manifest and provenance map that points back to `codex-marketplace/plugins/house-skills/skills/unslop-superpowers/SKILL.md` as the canonical source path.

- [x] **Step 3: Refresh the bundle docs**

Update `SOURCE.md` and `PROJECTION.md` to explain that Superpowers now carries three source-backed first-party projections: `linear-superpowers`, `github-superpowers`, and `unslop-superpowers`.

- [x] **Step 4: Confirm GPT overlay need**

Check whether the new projection requires a `gpt-overlays/` entry. If no GPT-only incompatibility is found, leave the overlay manifest untouched and record that the export is GPT-safe without an overlay.

### Task 3: Teach validation and generation about the new projection

**Files:**
- Modify: `tests/test_validate_marketplace.py`
- Modify: `tools/validate_marketplace.py`
- Modify: `generated/skill-zips/registry.json`
- Regenerated: `generated/skill-zips/house-skills/unslop-superpowers/skill.zip`
- Regenerated: `generated/skill-zips/superpowers/unslop-superpowers/skill.zip`

- [x] **Step 1: Write the failing validator test**

Add `test_superpowers_bundle_accepts_first_party_unslop_superpowers_projection()` to `tests/test_validate_marketplace.py`, mirroring the existing `linear-superpowers` and `github-superpowers` cases but using `unslop-superpowers` as the projected entry. Run `py -3 -m pytest tests/test_validate_marketplace.py -q` and confirm the new test fails until the validator is updated.

- [x] **Step 2: Update the validator**

Extend `validate_superpowers_bundle_manifest()` so `unslop-superpowers` is accepted as a first-party source-backed Superpowers projection when the House Skills source tree and projected tree match the established pattern.

- [x] **Step 3: Regenerate the artifacts**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill house-skills/unslop-superpowers
py -3 tools/update_skill_artifacts.py --skill superpowers/unslop-superpowers
```

Expect the generated registry and both `skill.zip` artifacts to pick up the new skill.

- [x] **Step 4: Validate the full marketplace**

Run:

```bash
py -3 tools/validate_marketplace.py
git diff --check HEAD~1 HEAD
```

Confirm the validator passes and the diff has no whitespace or patch-format issues.

### Task 4: Publish the branch

**Files:**
- No new files; commit the validated source, projection, manifest, provenance, test, and generated-output changes.

- [x] **Step 1: Review the diff**

Check the final file list for only the intended source, projection, ledger, validation, and generated-artifact changes.

- [x] **Step 2: Commit and push**

Create a focused commit, push the branch, and open a PR against `main`.

- [x] **Step 3: Record publication proof**

Capture the branch name, starting `main` SHA, head SHA, PR URL, validation commands, and any remaining Linear or GitHub follow-up needed for closeout.
