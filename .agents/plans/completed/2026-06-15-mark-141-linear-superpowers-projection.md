# MARK-141 Linear Superpowers Projection Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Expose `linear-superpowers` in the Superpowers marketplace bundle while keeping `codex-marketplace/plugins/house-skills/skills/linear-superpowers/` as the canonical editable source.

**Architecture:** Keep the House Skills root untouched as the source of truth. Add a source-backed Superpowers projection that mirrors the skill into `codex-marketplace/plugins/superpowers/skills/linear-superpowers/`, records the House Skills source path in the Superpowers bundle metadata, and updates validation so the projection is treated as a first-party sourced copy rather than a second editable root.

**Tech Stack:** Markdown skill sources, YAML skill metadata, JSON manifests and ledgers, Python validation scripts, generated skill zip artifacts.

---

### Task 1: Lock the desired validator shape with a failing regression test

**Files:**
- Create: `tests/test_validate_marketplace.py`

- [x] **Step 1: Write the failing test**

```python
def test_superpowers_bundle_accepts_first_party_linear_superpowers_projection():
    ...
```

- [x] **Step 2: Run the test and confirm it fails**

Run: `py -3 -m unittest tests.test_validate_marketplace -v`
Expected: fail because the current Superpowers validator rejects a first-party sourced projection entry.

### Task 2: Add the Superpowers projection and metadata

**Files:**
- Create: `codex-marketplace/plugins/superpowers/skills/linear-superpowers/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/superpowers/references/provenance-map.json`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `repo-index/repo-index.json`

- [x] **Step 1: Add the projected skill**

Mirror the House Skills `SKILL.md` content into the Superpowers skill root so the marketplace skill list includes `linear-superpowers` under the Superpowers bundle.

- [x] **Step 2: Record provenance and source custody**

Update the Superpowers bundle manifest and provenance map so the new entry points back to `codex-marketplace/plugins/house-skills/skills/linear-superpowers/SKILL.md` as the canonical editable source.

- [x] **Step 3: Update the human-facing bundle docs**

Refresh `SOURCE.md` and `PROJECTION.md` so they explain that Superpowers now carries one source-backed first-party projection in addition to the retained upstream Superpowers roots.

- [x] **Step 4: Keep the repo index aligned**

Update `repo-index/repo-index.json` so the superpowers zone records the additional House Skills source ledger path if needed for discoverability.

### Task 3: Teach validation about the mixed-source projection

**Files:**
- Modify: `tools/validate_marketplace.py`

- [x] **Step 1: Allow the special first-party projected entry**

Extend `validate_superpowers_bundle_manifest()` so a first-party `linear-superpowers` entry is accepted when it points at the House Skills canonical source and the projected skill directory matches the source tree.

- [x] **Step 2: Keep the rest of the projection strict**

Preserve the existing checks for the upstream third-party Superpowers projection, the support-surface exclusions, and the top-level install surface shape.

### Task 4: Regenerate and validate everything

**Files:**
- Regenerated: `generated/skill-zips/superpowers/linear-superpowers/skill.zip`
- Regenerated: `generated/skill-zips/registry.json`

- [x] **Step 1: Regenerate the targeted skill artifact**

Run: `py -3 tools/update_skill_artifacts.py --skill superpowers/linear-superpowers`

- [x] **Step 2: Run the repo validation ladder**

Run:

```bash
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_generated_drift.py --base origin/main
py -3 tools/validate_skill_zips.py
```

- [x] **Step 3: Check the diff**

Run: `git diff --check`

- [x] **Step 4: Commit and publish**

Commit the Superpowers projection, the validator update, and the regenerated zip/registry together, then push the branch and open a PR against `main`.
