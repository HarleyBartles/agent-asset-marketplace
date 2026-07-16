# linear-superpowers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Add a first-party `linear-superpowers` skill under House Skills and project it into Superpowers only if the repo already has a clean, source-backed projection path.

**Architecture:** House Skills remains the canonical source custody for the new skill. The House Skills bundle/source-map/provenance ledgers stay authoritative, and the Superpowers surface is treated as an optional projection that may be omitted if it would require a second editable source root or an invented cross-pack mechanism. GPT overlay/export metadata stays out unless the current exporter needs a GPT-safe variant.

**Tech Stack:** Markdown skill sources, Codex marketplace manifests, JSON source/bundle ledgers, generated skill zip tooling, repo validation scripts.

---

### Task 1: Add the canonical House Skills source root

**Files:**
- Create: `codex-marketplace/plugins/house-skills/skills/linear-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/house-skills/skills/linear-superpowers/agents/openai.yaml`

- [x] **Step 1: Write the new skill source**

Create a compact skill that:
- positions `@using-superpowers` as the workflow-selection entrypoint;
- composes with `@writing-plans`, `@executing-plans`, `@connector-safety`, and `@linear-issue-compactor`;
- requires parent/child DOD coverage, vertical slices of provable value, read-before-write discipline, narrow Linear payloads, and verified-result reporting;
- keeps worker dispatch, GitHub proof, and Codex publication claims outside the skill.

- [x] **Step 2: Add the skill metadata**

Create `agents/openai.yaml` with the display name, short description, and default prompt that points to `linear-superpowers` as a compositional Linear workflow skill.

- [x] **Step 3: Keep the root compact**

Do not add a duplicate editable source root for Superpowers. Do not add GPT overlay files unless a later exporter check proves they are required.

### Task 2: Update House Skills source/projection ledgers

**Files:**
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/SKILL.md`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- Modify: `codex-marketplace/plugins/house-skills/README.md`
- Modify: `provenance/house-skills.md`

- [x] **Step 1: Register the new first-party source in the ledgers**

Add a `MARK-139` row in the House Skills decisions ledger and mirror it in the JSON ledger with:
- `source_path` pointing to `codex-marketplace/plugins/house-skills/skills/linear-superpowers/SKILL.md`;
- `public_name` of `linear-superpowers`;
- first-party scope notes that match the issue intent.

- [x] **Step 2: Update the bundle inventory**

Add `linear-superpowers` to the House Skills bundle manifest and source map, and bump the live root count from 50 to 51 in the bundle docs that describe the active first-party inventory.

- [x] **Step 3: Record provenance cleanly**

Add a short provenance note explaining that `linear-superpowers` is a new Harley-owned first-party skill, and that it composes Linear issue shaping with the existing Superpowers workflow skills.

### Task 3: Decide and, if clean, add the Superpowers projection

**Files:**
- Modify: `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Create only if cleanly supported: `codex-marketplace/plugins/superpowers/skills/linear-superpowers/SKILL.md`

- [x] **Step 1: Verify whether a clean projection path already exists**

Confirm whether the repo already has a source-backed projection pattern for placing a first-party skill into the Superpowers surface without introducing a second editable source root.

- [x] **Step 2: Project only if the path is clean**

If a mirrored/generated copy with provenance back to the House Skills root is already consistent with repo conventions, add the Superpowers projection and point its provenance back to the House Skills source.

- [x] **Step 3: Otherwise leave Superpowers untouched**

If the only workable route would be a new editable source root or an invented cross-pack mechanism, do not project the skill into Superpowers. Record that constraint in the final return evidence.

### Task 4: Regenerate exports and validate

**Files:**
- Regenerated: `generated/skill-zips/**`
- Regenerated: `generated/skill-zips/registry.json`

- [x] **Step 1: Regenerate the targeted skill artifacts**

Run the repo’s targeted skill-artifact update for `linear-superpowers` so the generated zip surface and registry stay in sync with the source tree.

- [x] **Step 2: Run repository validation**

Run the repository’s canonical validation commands:

```bash
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_generated_drift.py
py -3 tools/validate_export_skill_zips.py
```

- [x] **Step 3: Check the diff**

Run:

```bash
git diff --check
```

Expected: no whitespace or patch-format errors.

- [x] **Step 4: Commit**

Commit the House Skills source, any clean Superpowers projection, and the regenerated artifacts together so the provenance and generated outputs stay aligned.
