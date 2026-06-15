# github-superpowers Projection Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-party `github-superpowers` compositional skill in House Skills and project it into Superpowers while preserving `github-operations` as the specialist GitHub proof/write-boundary skill.

**Architecture:** Keep `codex-marketplace/plugins/house-skills/skills/github-superpowers/` as the canonical editable source. Project the same skill into `codex-marketplace/plugins/superpowers/skills/github-superpowers/` using the existing source-backed projection pattern from `linear-superpowers`, then update the House Skills and Superpowers bundle manifests, provenance notes, generated skill zips, and validation so the new projection is treated as a first-party source-backed skill rather than a second source of truth.

**Tech Stack:** Markdown skill sources, YAML skill metadata, JSON manifests/ledgers, Python validation and packaging scripts, generated `skill.zip` artifacts.

---

### Task 1: Add the first-party source skill

**Files:**
- Create: `codex-marketplace/plugins/house-skills/skills/github-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/house-skills/skills/github-superpowers/agents/openai.yaml`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/skills/house-skills/references/source-map.md`
- Modify: `provenance/house-skills.md`

- [ ] **Step 1: Add the new source skill**

Create a House Skills `github-superpowers` entry that starts with `@using-superpowers`, names `github-operations` as the specialist proof/write-boundary skill, and keeps the composition narrow to GitHub proof, review routing, publication proof, and verification.

- [ ] **Step 2: Register the source record**

Add matching decision/intake rows so the canonical source path is recorded as the House Skills file and the provenance notes explain that this is a first-party compositional skill.

- [ ] **Step 3: Update the House Skills inventory**

Increment the bundle manifest skill count, add the new live root to the inventory, and add the corresponding source-map row.

- [ ] **Step 4: Record provenance**

Add a provenance entry that points at the new House Skills source path and explains that `github-operations` remains the specialist skill rather than being replaced.

### Task 2: Project the skill into Superpowers

**Files:**
- Create: `codex-marketplace/plugins/superpowers/skills/github-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers/skills/github-superpowers/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`

- [ ] **Step 1: Mirror the projected skill**

Copy the House Skills `github-superpowers` skill into the Superpowers bundle so the projection stays source-backed and editable in House Skills.

- [ ] **Step 2: Update bundle metadata**

Add a first-party projection entry in the Superpowers bundle manifest and provenance map that points back to the House Skills canonical source path.

- [ ] **Step 3: Refresh the bundle docs**

Update `SOURCE.md` and `PROJECTION.md` to explain that Superpowers now carries a second source-backed first-party projection alongside `linear-superpowers`.

### Task 3: Teach validation and generation about the new projection

**Files:**
- Modify: `tools/validate_marketplace.py`
- Modify: `generated/skill-zips/registry.json`
- Regenerated: `generated/skill-zips/house-skills/github-superpowers/skill.zip`
- Regenerated: `generated/skill-zips/superpowers/github-superpowers/skill.zip`

- [ ] **Step 1: Extend the superpowers validator**

Allow `github-superpowers` as a first-party source-backed Superpowers projection when it points at the House Skills canonical source and the projected skill tree matches the source tree.

- [ ] **Step 2: Regenerate the artifacts**

Run the targeted skill artifact update so the generated registry and `skill.zip` artifacts include the new House Skills and Superpowers exports.

- [ ] **Step 3: Validate the full marketplace**

Run the repo validation ladder and `git diff --check` to confirm the manifests, projections, and generated artifacts are internally consistent.

### Task 4: Publish the branch

**Files:**
- No new files; commit the validated source, projection, and generated outputs.

- [ ] **Step 1: Review the diff**

Check the final file list for only the intended source, projection, manifest, and generated changes.

- [ ] **Step 2: Commit and push**

Create a focused commit, push the branch, and open a PR against `main`.

- [ ] **Step 3: Record publication proof**

Capture the branch name, head SHA, PR URL, validation commands, and any remaining GitHub or Linear follow-up needed for closeout.
