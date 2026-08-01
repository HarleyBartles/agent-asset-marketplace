# Remove the projection layer — Phase 1: Demolition

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the `sources/` custody tree, the custody-pack registry, and the tooling that exists only to project from custody into plugins. After this phase, `codex-marketplace/plugins/<plugin>/skills/<name>/` is the only canonical home for a skill.

**Architecture:** This phase removes `sources/first_party/`, `sources/third_party/`, `codex-marketplace/custody-pack-registry.json`, and the projection-only `tools/` scripts. The plugin manifests in `codex-marketplace/plugin-roots.json` and `codex-marketplace/plugins/<plugin>/.codex-plugin/plugin.json` remain as the marketplace source of truth. Existing plugin skill trees are already the vendored copies, so the repo keeps working once the registry is gone.

**Tech Stack:** Python 3.12, the existing `tools/run.py` / `tools/validate_marketplace.py` tooling, and `git`.

## Global Constraints

- CI must remain green after each task; run `py -3 tools/run.py ci --check` before every commit.
- No hand-editing of generated `codex-marketplace/plugins/<plugin>/skills/` trees; those are now the canonical source.
- Delete a file rather than adapt it if its only purpose was to service the removed custody/projection pipeline.
- Update `AGENTS.md` and runbook references in the same phase so doctrine does not drift.

---

### Task 1: Remove the `sources/` tree

**Files:**
- Delete: `sources/first_party/` (entire tree)
- Delete: `sources/third_party/` (entire tree)
- Delete: `sources/INDEX.md`
- Delete: `sources/README.md`

**Interfaces:**
- Consumes: none
- Produces: a repo with no `sources/` directory

- [ ] **Step 1: Delete the `sources/` tree**

```bash
rm -r sources
rm sources/INDEX.md
rm sources/README.md
```

- [ ] **Step 2: Stage the deletion**

```bash
git add -A
git status
```

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove sources/ custody tree

Remove sources/first_party/ and sources/third_party/.
Skills now live directly in the vendored plugin trees."
```

---

### Task 2: Remove the custody-pack registry and generated provenance/source maps

**Files:**
- Delete: `codex-marketplace/custody-pack-registry.json`
- Delete: `codex-marketplace/plugins/*/references/provenance-map.json` (all)
- Delete: `codex-marketplace/plugins/*/references/source-map.md` (all)
- Delete: `provenance/first-party-skills.md`
- Delete: `provenance/unslop.md`
- Delete: `provenance/superpowers-plus.md`
- Modify: `provenance/INDEX.md` to remove entries for deleted provenance notes

**Interfaces:**
- Consumes: none
- Produces: a repo without custody-pack registry; plugin `references/` may be recreated later from plugin manifests

- [ ] **Step 1: Remove the registry and generated references**

```bash
rm codex-marketplace/custody-pack-registry.json
rm codex-marketplace/plugins/*/references/provenance-map.json
rm codex-marketplace/plugins/*/references/source-map.md
rm provenance/first-party-skills.md
rm provenance/unslop.md
rm provenance/superpowers-plus.md
```

- [ ] **Step 2: Edit `provenance/INDEX.md` to remove deleted provenance links**

Open `provenance/INDEX.md` and delete the list items that pointed to the removed files.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove custody-pack registry and generated provenance/source maps

The custody-pack-registry.json and the generated provenance/source maps
only made sense when skills were projected from a separate custody layer.
They are no longer needed."
```

---

### Task 3: Delete projection-only tools

**Files to inspect and delete if they only service the removed pipeline:**
- `tools/generate_first_party_skill_catalog.py`
- `tools/normalize_first_party_skill_sources.py`
- `tools/skill_projection_helpers.py`
- `tools/update_skill_artifacts.py`
- `tools/update_superpowers_source.py`
- `tools/generate_provenance_maps.py`
- `tools/generate_source_maps.py`

**Files to modify:**
- `tools/INDEX.md` — remove deleted tool links
- `tools/run.py` — remove tool invocation targets that no longer exist

**Interfaces:**
- Consumes: plugin manifests from `codex-marketplace/plugin-roots.json`
- Produces: a smaller `tools/` tree whose remaining tools read directly from `codex-marketplace/plugins/`

- [ ] **Step 1: Inspect each tool and delete if projection-only**

For each of the scripts above, read the first 30 lines. If the docstring or imports reference `sources/first_party`, `sources/third_party`, `custody-pack-registry`, or `projection`, delete the file.

```bash
git rm tools/generate_first_party_skill_catalog.py
git rm tools/normalize_first_party_skill_sources.py
# ... repeat for each identified projection-only script
```

- [ ] **Step 2: Remove `tools/INDEX.md` links for deleted scripts**

Open `tools/INDEX.md` and delete the bullet items that point at removed files.

- [ ] **Step 3: Remove dead tool targets from `tools/run.py`**

Open `tools/run.py` and delete the `click` / `subprocess` invocations that call the removed scripts. If a `tools/run` target no longer has a backing script, delete the target.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove projection-only tools

Delete scripts that generated or validated the custody-to-plugin
projection pipeline."
```

---

### Task 4: Simplify `tools/validate_marketplace.py`

**Files:**
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: `codex-marketplace/plugin-roots.json` and plugin `.codex-plugin/plugin.json` manifests
- Produces: a validator that checks plugin shape and skill metadata but does not enforce `sources/first_party` or `custody-pack-registry.json`

- [ ] **Step 1: Read the current validator and identify custody/projection assertions**

Look for:
- references to `sources/first_party/`
- references to `sources/third_party/`
- `custody-pack-registry.json`
- `first_party`/`third_party` source-category validation
- orphan detection

- [ ] **Step 2: Remove or simplify those assertions**

Change the validator to only check:
- each plugin has a valid `.codex-plugin/plugin.json`
- each declared plugin root in `codex-marketplace/plugin-roots.json` exists
- each `skills/<name>/SKILL.md` has valid YAML front matter
- `source_category` and `content_mode` are allowed values

Remove the `detect_first_party_orphans` and source-custody checks.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: simplify marketplace validator

Remove source-custody and projection checks from validate_marketplace.py.
Validation is now plugin-root and plugin-manifest shape only."
```

---

### Task 5: Simplify `tools/validate_repo_index.py`

**Files:**
- Modify: `tools/validate_repo_index.py`

**Interfaces:**
- Consumes: repo-index entries
- Produces: a validator that no longer requires `sources/third_party` AGENTS or custody rules

- [ ] **Step 1: Remove `sources/third_party` AGENTS check**

Open `tools/validate_repo_index.py` and delete the block that validates the `sources/third_party` scoped AGENTS.md guidance.

- [ ] **Step 2: Commit**

```bash
git add -A
git commit -m "chore: remove sources/third_party AGENTS check from repo-index validator"
```

---

### Task 6: Remove or rewrite the custody and projection doctrine

**Files:**
- Delete: `docs/custody-and-projection-doctrine.md`
- Modify: `AGENTS.md` — remove source-custody language
- Modify: `.agents/docs/AGENTS.md` — remove `sources/first_party` and `sources/third_party` review guidance
- Modify: `.agents/runbooks/AGENTS.md` — remove `completing-plans`? (no, keep; unrelated)

**Interfaces:**
- Consumes: the repo's new shape
- Produces: documentation that matches the new no-projection, no-custody model

- [ ] **Step 1: Delete `docs/custody-and-projection-doctrine.md`**

```bash
git rm docs/custody-and-projection-doctrine.md
```

- [ ] **Step 2: Update `AGENTS.md`**

Open `AGENTS.md` and replace custody/projection language with the simpler statement that the repo's source of truth is `codex-marketplace/plugins/`.

- [ ] **Step 3: Update `.agents/docs/AGENTS.md`**

Open `.agents/docs/AGENTS.md` and remove the bullet that says "Treat `sources/first_party/**` as mutable source custody" and "Treat `sources/third_party/**` as immutable custody."

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove custody-and-projection doctrine

Delete the doctrine doc and update AGENTS files to reflect that
vendored plugin trees are the canonical source."
```

---

### Task 7: Regenerate the marketplace and repo index from plugin roots only

**Files:**
- Modify: `tools/run.py` — keep only `marketplace`, `repo-index`, `mesh`, `catalog`, `lint`, `repo-standards`
- Modify: `tools/marketplace_utils.py` — remove `first_party`/`third_party` and custody references
- Run: `py -3 tools/run.py marketplace --apply`
- Run: `py -3 tools/run.py ci --check`

**Interfaces:**
- Consumes: `codex-marketplace/plugin-roots.json` and plugin manifests
- Produces: regenerated `.agents/plugins/marketplace.json`, `codex-marketplace/manifest.json`, `repo-index/repo-index.json`, and mesh indexes

- [ ] **Step 1: Update `tools/marketplace_utils.py` to not reference `sources/`**

Open `tools/marketplace_utils.py` and remove any constants, helpers, or validation that reference `sources/first_party` or `sources/third_party`.

- [ ] **Step 2: Regenerate**

```bash
py -3 tools/run.py marketplace --apply
```

- [ ] **Step 3: Validate**

```bash
py -3 tools/run.py ci --check
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: regenerate marketplace from plugin roots only

Remove custody references from marketplace_utils.py and regenerate
all derived surfaces."
```

---

## SDD Confidence / Plan-Readiness Rating

**Rating: 7/10**

The demolition tasks are concrete, but the exact set of `tools/` scripts that can be deleted without breaking `tools/run.py` or `ci --check` can only be confirmed by reading each one in the implementation session. Task 4 and Task 5 may need small adjustments once the remaining validator behavior is tested. This plan is safe to start, but the implementer must run `py -3 tools/run.py ci --check` after every task and adjust if an unexpected dependency surfaces.
