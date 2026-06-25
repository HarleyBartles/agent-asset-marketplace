# MARK-302 safe-large-file-writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an installable first-party `safe-large-file-writing` skill that keeps Devin/Desktop agents off the interactive editor OOM path for large text writes.

**Architecture:** Put the authoritative skill body in first-party source custody under `sources/first_party/skills/safe-large-file-writing/`. Project that source into the current first-party marketplace bundles that carry worker workflow skills (`house-skills` and `superpowers-plus`) by updating the source-ledger entries and regenerating bundle manifests, source maps, provenance maps, and skill zips through the repo generators. Keep the content compact and operational: detect likely large writes first, route to script/CLI/temp-file/atomic-replace flows, validate size and line count before swap, and keep Windows/Python examples in the skill itself.

**Tech Stack:** Markdown skill source, YAML agent metadata, JSON ledgers/manifests, Python generator/validation scripts, generated `skill.zip` artifacts, PowerShell/Python execution examples.

## Global Constraints

- Use the fresh `origin/main` base and keep the isolated `.worktrees/` checkout as the only edit surface.
- Do not add repo-local instruction files as the primary solution; the durable fix is a first-party marketplace skill.
- Keep the skill compact and practical; this is a behavior guardrail, not a long-form essay.
- Keep any single large text write under 500 lines per manual edit.
- The first-party source is authoritative; generated marketplace/projection/zip surfaces are downstream outputs.
- Preflight note: `py -3 tools/validate_marketplace.py` currently fails in this worktree on a pre-existing missing `adventures-pack` asset at `codex-marketplace/plugins/adventures-pack/skills/adventures-asset-sheet-compiler/assets/templates/template_asset_sheet_3hero_6alt_v4.png`; do not widen MARK-302 to fix that unrelated surface unless future validation requires it.

---

### Task 1: Author the first-party source skill

**Files:**
- Create: `sources/first_party/skills/safe-large-file-writing/SKILL.md`
- Create: `sources/first_party/skills/safe-large-file-writing/agents/openai.yaml`
- Modify: `sources/first_party/skills/house-skills/decisions.json`
- Modify: `sources/first_party/skills/house-skills/decisions.md`
- Modify: `sources/first_party/skills/house-skills/intake.json`
- Modify: `provenance/house-skills.md`

**Interfaces:**
- Consumes: `/using-superpowers`, `/writing-skills`, `/inspecting-the-environment`, `/connector-safety`
- Produces: a first-party source skill with metadata that triggers on large writes and recommends temp-file/atomic-replace workflows.

- [ ] **Step 1: Write the skill body**

Add `SKILL.md` with explicit trigger language for creating, replacing, appending, regenerating, or substantially editing large text files. Keep the core behavior narrow:

```markdown
## Core behavior

- Estimate whether a write will exceed the safe threshold before editing.
- Avoid whole-file editor replacement for large text files.
- Avoid sending 300+ lines as one editor edit.
- Use a script, CLI write, shell redirection, or chunked append path instead.
- Write to a temporary file first.
- Validate byte size and line count before replacement.
- Atomically replace the target only after validation.
- Prefer localized patches for large existing source files.
- Avoid opening generated large files in the editor unless review is required.
- Stop retrying editor writes after memory pressure and switch to the safe write path.
```

- [ ] **Step 2: Include Windows-friendly safe-write examples**

Show a Python temp-file pattern the worker can copy without guessing:

```python
from pathlib import Path

target = Path("output.md")
tmp = target.with_suffix(target.suffix + ".tmp")
payload = "# content\n"

tmp.write_text(payload, encoding="utf-8", newline="\n")
if len(payload.splitlines()) > 300 or tmp.stat().st_size > 256_000:
    raise RuntimeError("switch to a safer chunked write path")
tmp.replace(target)
```

Add a short PowerShell example only if it keeps the skill usable on Windows without turning the skill into a shell cookbook.

- [ ] **Step 3: Add the installable metadata file**

Create `agents/openai.yaml` with the display name, a short description that points at safe large-file writes, and a default prompt that tells the agent to choose script/CLI/temp-file workflows instead of interactive editor replacement when the write is large.

- [ ] **Step 4: Register the source in the house-skills ledgers**

Append the new source root to the house-skills decision/intake/provenance records so validation can see the canonical source path as first-party Harley-owned source custody for large-file write safety.

### Task 2: Project the skill and regenerate the marketplace outputs

**Files:**
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers-plus/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/SKILL.md`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/safe-large-file-writing/agents/openai.yaml`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/skills/safe-large-file-writing/SKILL.md`
- Regenerated: `codex-marketplace/plugins/superpowers-plus/skills/safe-large-file-writing/agents/openai.yaml`
- Regenerated: `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip`
- Regenerated: `generated/skill-zips/superpowers-plus/safe-large-file-writing/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the source skill from Task 1 and the current bundle manifests.
- Produces: installable marketplace projections and direct skill zips for both bundles.

- [ ] **Step 1: Materialize the House Skills projection**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill house-skills/safe-large-file-writing
```

Expected: the House Skills projection surface and `generated/skill-zips/house-skills/safe-large-file-writing/skill.zip` are refreshed from source custody, not hand-copied.

- [ ] **Step 2: Materialize the Superpowers+ projection**

Run:

```bash
py -3 tools/update_skill_artifacts.py --skill superpowers-plus/safe-large-file-writing
```

Expected: the Superpowers+ projection surface and `generated/skill-zips/superpowers-plus/safe-large-file-writing/skill.zip` match the same first-party source skill.

- [ ] **Step 3: Review the generated surfaces**

Confirm the regenerated bundle manifests and source maps show only the new `safe-large-file-writing` entries plus the mechanical projection outputs. Do not broaden the diff into unrelated bundle churn.

### Task 3: Validate, commit, and publish the plan branch

**Files:**
- No new files; validate and publish the plan branch after the diff is checked.

**Interfaces:**
- Consumes: the regenerated marketplace outputs from Task 2.
- Produces: a committed plan branch and draft PR against `main`, ready for approval before implementation starts.

- [ ] **Step 1: Run the repo validation ladder**

Run:

```bash
py -3 tools/generate_marketplace.py --check
py -3 tools/generate_repo_index.py --check
py -3 tools/validate_marketplace.py
git diff --check
```

If `validate_marketplace.py` still fails on the pre-existing `adventures-pack` asset gap, record it as an unrelated baseline blocker and do not expand MARK-302.

- [ ] **Step 2: Commit the plan**

Commit only the plan document and any required metadata updates from Task 1, keeping the commit message scoped to MARK-302.

- [ ] **Step 3: Push a draft PR and stop**

Push the branch and open a draft PR targeting `main`. Do not start implementation until approval lands; the PR is the publication surface for the plan-only handoff.

### Coverage Check

- Source skill and metadata: Task 1
- Marketplace projections and generated zips: Task 2
- Validation and publication proof: Task 3
- Known unrelated baseline blocker: pre-existing `adventures-pack` validation failure noted above
