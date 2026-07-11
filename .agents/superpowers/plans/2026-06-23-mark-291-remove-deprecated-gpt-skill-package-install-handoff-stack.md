# MARK-291 Remove Deprecated GPT Skill Package/Install/Handoff Stack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the retired `skill-installer` / `skill-validator` / `skill-packager` / `skill-handoff` stack from active marketplace source, projection, and guidance surfaces while preserving historical records and rebuilding every derived surface through repo tooling.

**Architecture:** The four deprecated skills are first-party source custody under `sources/first_party/skills/` and are projected verbatim into the `house-skills` bundle and generated GPT zip corpus. The implementation should delete the active source trees, remove the bundle-manifest entries that drive projection, clean the active routing docs that still teach the retired lifecycle, and then regenerate the derived marketplace, projection, index, provenance/source map, and zip surfaces so the repo ends in a checkable state. Historical ledgers and provenance stay intact unless a line is still acting like live guidance.

**Tech Stack:** PowerShell on Windows, `py -3`, existing marketplace generators and validators under `tools/`, Markdown/JSON skill docs, and generated `skill.zip` artifacts.

## Global Constraints

- Keep scope to MARK-291.
- Do not edit `writing-skills`.
- Do not create a replacement installer, validator, packager, or handoff stack under a new name.
- Do not hand-edit generated zip contents or generated registry output.
- Preserve historical records when they are clearly historical.
- Use repo tooling for all derived surfaces.
- Keep the workspace on `main` until implementation starts.

---

### Task 1: Remove the deprecated stack from first-party custody and the House Skills bundle source

**Files:**
- Delete: `sources/first_party/skills/skill-installer/`
- Delete: `sources/first_party/skills/skill-validator/`
- Delete: `sources/first_party/skills/skill-packager/`
- Delete: `sources/first_party/skills/skill-handoff/`
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `sources/first_party/skills/house-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`

**Interfaces:**
- Consumes: the current `house-skills` bundle-manifest entry list and the live House Skills bundle docs.
- Produces: a House Skills source tree whose active root list no longer advertises the retired stack, plus a bundle-manifest that no longer projects those four skills.

- [ ] Delete the four deprecated first-party source trees under `sources/first_party/skills/`.
- [ ] Remove the four bundle-manifest entries from `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`.
- [ ] Update the House Skills bundle docs so the active root list and root count no longer claim `skill-installer`, `skill-validator`, `skill-packager`, or `skill-handoff` are live roots.
- [ ] Leave `sources/first_party/skills/house-skills/decisions.*`, `sources/first_party/skills/house-skills/intake.json`, and `provenance/house-skills.md` intact unless a line in them is still phrased as active routing doctrine.

### Task 2: Remove retired-stack routing language from active guidance

**Files:**
- Modify: `sources/first_party/skills/bootstrap-router/SKILL.md`
- Modify: `sources/first_party/skills/work-mode-router/SKILL.md`
- Modify: `sources/first_party/skills/crew/SKILL.md`
- Modify: `sources/first_party/skills/crew-buster/SKILL.md`
- Modify: `sources/first_party/skills/asset-market/SKILL.md`
- Modify: `sources/first_party/skills/boring-loop/SKILL.md`
- Modify: `sources/first_party/skills/session-buster-ingress/SKILL.md`

**Interfaces:**
- Consumes: the current route descriptions that still mention the retired `skill-creator -> skill-validator -> skill-packager -> skill-handoff` flow.
- Produces: active guidance that points GPT-native skill work to the current, repo-backed boundaries and keeps the retired lifecycle in historical-only wording where it must remain documented.

- [ ] Replace any live routing text that sends new work through the retired stack with the current direct boundary language or with explicit historical-only wording.
- [ ] Remove any active instructions in `asset-market`, `crew`, `crew-buster`, `bootstrap-router`, `work-mode-router`, `boring-loop`, or `session-buster-ingress` that still present the retired stack as the normal route.
- [ ] Keep the wording narrow and preserve non-goals, historical notes, and provenance where they are not acting as live guidance.

### Task 3: Regenerate the derived marketplace, projection, index, provenance, and zip surfaces

**Files:**
- Modify: `codex-marketplace/manifest.json`
- Modify: `.agents/plugins/marketplace.json`
- Modify: `repo-index/repo-index.json`
- Modify: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/house-skills/skill-installer/skill.zip`
- Modify: `generated/skill-zips/house-skills/skill-validator/skill.zip`
- Modify: `generated/skill-zips/house-skills/skill-packager/skill.zip`
- Modify: `generated/skill-zips/house-skills/skill-handoff/skill.zip`
- Modify: the projected House Skills skill trees under `codex-marketplace/plugins/house-skills/skills/`

**Interfaces:**
- Consumes: the updated source custody and bundle-manifest from Tasks 1 and 2.
- Produces: regenerated marketplace manifests, repo index data, House Skills source/projection maps, and a zip registry that no longer advertises the retired stack.

- [ ] Run `py -3 tools/update_skill_artifacts.py --all` to rebuild the projected House Skills skill trees and the generated `skill.zip` corpus from the edited source.
- [ ] Run `py -3 tools/generate_marketplace.py` to refresh the active marketplace manifests.
- [ ] Run `py -3 tools/generate_repo_index.py` to refresh the repo index.
- [ ] Run `py -3 tools/generate_provenance_maps.py` and `py -3 tools/generate_source_maps.py` if the House Skills map surfaces changed with the bundle-manifest removal.

### Task 4: Validate the retired-stack removal and preserve only historical residue

**Files:**
- No edits expected unless validation exposes one stale active reference in the smallest affected source or generated file.

**Interfaces:**
- Consumes: the regenerated repository state from Tasks 1 through 3.
- Produces: a validated repo state where remaining mentions of the retired stack are historical-only, compatibility-only, or otherwise justified in the PR notes.

- [ ] Run `py -3 tools/validate_marketplace.py`.
- [ ] Run `py -3 tools/validate_repo_index.py`.
- [ ] Run `py -3 tools/materialize_projection.py --check`.
- [ ] Run `py -3 tools/validate_skill_zips.py`.
- [ ] Run `git diff --check`.
- [ ] Re-run `rg -n "skill-(installer|validator|packager|handoff)|package/install/handoff|skill-creator, then skill-validator, then skill-packager, then skill-handoff" sources codex-marketplace docs provenance repo-index generated` and confirm any remaining hits are historical-only.
- [ ] If a validation failure points to one stale active reference, patch the smallest matching doc or generated file and rerun the same checks.

## Self-Review

### Spec Coverage

- The four deprecated skills are removed from first-party custody and the House Skills bundle source.
- Active routing docs are cleaned without touching `writing-skills`.
- Derived marketplace, projection, index, provenance/source maps, and zip outputs are regenerated through repo tooling.
- Validation is explicit and checkable.

### Placeholder Scan

- No TBDs.
- No vague "handle edge cases" language.
- Every file group and command is named explicitly.

### Type Consistency

- `py -3` is used for all local generation and validation commands.
- The same retired stack names are used consistently across the source, projection, and validation steps.
