# architecture-superpowers Pre-Fork Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `architecture-superpowers` as the final authorized pre-fork Superpowers projection, mirror it into the `superpowers` marketplace bundle, and publish a durable freeze record that blocks any further direct Superpowers wrapper projection until the fork/overlay custody model exists.

**Architecture:** Keep `architecture-superpowers` as a compositional router/gate, not a doctrine dump. The first-party source lives under `sources/first_party/skills/architecture-superpowers/` and is mirrored into `codex-marketplace/plugins/superpowers/skills/architecture-superpowers/` using the existing source-backed first-party projection pattern. Update the `superpowers` bundle metadata, provenance map, repo index, generated skill zips, and validation allowlist together so the new wrapper is treated as the final pre-fork addition rather than a new expert surface.

**Tech Stack:** Markdown skill files, YAML agent manifests, JSON bundle/provenance/index artifacts, `py -3` repo tooling.

---

### Task 1: Add the first-party source skill and projected mirror

**Files:**
- Create: `sources/first_party/skills/architecture-superpowers/SKILL.md`
- Create: `sources/first_party/skills/architecture-superpowers/agents/openai.yaml`
- Create: `codex-marketplace/plugins/superpowers/skills/architecture-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers/skills/architecture-superpowers/agents/openai.yaml`

- [ ] **Step 1: Write the source skill as a compositional router**

The skill must start with `/using-superpowers`, route to `/connector-safety`, `/linear-superpowers`, `/github-superpowers`, `/unslop-superpowers`, `/codex-receipts-superpowers`, and the relevant architecture-pack skills only when the problem warrants them, and explicitly say not to treat CQRS/Event Sourcing as the default answer.

- [ ] **Step 2: Mirror the source skill into the Superpowers projection**

Keep the projected `SKILL.md` byte-for-byte aligned with the canonical source skill and create the matching `agents/openai.yaml` mirror so the bundle installs cleanly as a directory-level skill.

- [ ] **Step 3: Verify the new source/projection trees exist**

Run:

```powershell
Get-ChildItem -Recurse sources/first_party/skills/architecture-superpowers
Get-ChildItem -Recurse codex-marketplace/plugins/superpowers/skills/architecture-superpowers
```

Expected: both trees contain `SKILL.md` and `agents/openai.yaml`.

### Task 2: Update the Superpowers bundle surfaces and validator allowlist

**Files:**
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Modify: `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- Modify: `tools/validate_marketplace.py`
- Modify: `repo-index/repo-index.json` if the generator does not update it cleanly

- [ ] **Step 1: Add `architecture-superpowers` to the projection contract text**

Update `SOURCE.md` and `PROJECTION.md` so the live pre-fork wrapper set is explicitly listed as `linear-superpowers`, `github-superpowers`, `unslop-superpowers`, `codex-receipts-superpowers`, and `architecture-superpowers`.

- [ ] **Step 2: Register the new first-party source-backed entry**

Add the new `architecture-superpowers` entry to the Superpowers bundle manifest and provenance map with its canonical source path pointing at `sources/first_party/skills/architecture-superpowers/`.

- [ ] **Step 3: Extend the validator allowlist**

Add `architecture-superpowers` to the first-party Superpowers source map in `tools/validate_marketplace.py` so bundle validation accepts the new projection.

- [ ] **Step 4: Verify the bundle still validates before generation**

Run:

```powershell
py -3 tools/validate_marketplace.py
```

Expected: validation passes once the new entry and source mirror are in place.

### Task 3: Publish the freeze record and the matching implementation record

**Files:**
- Create: `docs/superpowers/records/2026-06-18-mark-173-architecture-superpowers-pre-fork.md`
- Create: `docs/superpowers/records/2026-06-18-mark-173-architecture-superpowers-pre-fork.md` content must include the final wrapper set and the freeze statement

- [ ] **Step 1: Write the freeze record**

Record that this is the final allowed pre-fork Superpowers wrapper projection and that any further wrapper requires the Superpowers fork/overlay custody model to exist first.

- [ ] **Step 2: Write the implementation record after validation**

Capture the issue, branch, starting main SHA, final head SHA, PR URL, changed files, generated artifacts, validation commands/results, skipped checks, and any follow-up issues.

- [ ] **Step 3: Confirm the record files are present**

Run:

```powershell
Get-ChildItem docs/superpowers/records | Select-Object Name
```

Expected: both the freeze record and implementation record are present.

### Task 4: Regenerate generated artifacts and validate the repo

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/superpowers/architecture-superpowers/skill.zip`
- Modify: `repo-index/repo-index.json` if regenerated output changes it

- [ ] **Step 1: Regenerate the affected skill zip**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --skill superpowers/architecture-superpowers
```

Expected: the `generated/skill-zips/superpowers/architecture-superpowers/skill.zip` artifact and registry entry are updated by tooling, not hand edits.

- [ ] **Step 2: Regenerate and validate marketplace surfaces**

Run:

```powershell
py -3 tools/validate_repo_index.py
py -3 tools/validate_marketplace.py
git diff --check
```

Expected: repo index and marketplace validation pass and the diff has no whitespace or patch formatting errors.

- [ ] **Step 3: Review the final diff for scope**

Confirm the diff is limited to the new wrapper, the existing Superpowers projection surfaces, the freeze/implementation records, and the generated outputs required by tooling.
