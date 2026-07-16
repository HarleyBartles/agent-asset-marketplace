# MARK-262 Licensing Provenance Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit and fix plugin-level and skill-level licensing/provenance across marketplace plugins to the MARK-244 standard.

**Architecture:** Systematic audit of all active marketplace plugins, fixing missing or incorrect authorship/license metadata in bundle manifests, source maps, and skill frontmatter. Focus on distinguishing verbatim vs adapted content and ensuring upstream attribution is preserved.

**Tech Stack:** Python validation scripts, JSON bundle manifests, Markdown source maps, YAML skill frontmatter

---

## Task 1: Audit current licensing/provenance state across all plugins

**Files:**
- Read: All `codex-marketplace/plugins/*/SOURCE.md`
- Read: All `codex-marketplace/plugins/*/references/bundle-manifest.json`
- Read: All `codex-marketplace/plugins/*/references/source-map.md`
- Read: Sample `codex-marketplace/plugins/*/skills/*/SKILL.md` frontmatter
- Create: `docs/superpowers/plans/2026-06-19-mark-262-audit-findings.md`

- [ ] **Step 1: Read all SOURCE.md files to understand plugin authorship claims**

For each plugin in `codex-marketplace/plugin-roots.json`:
```bash
cat codex-marketplace/plugins/<plugin>/SOURCE.md
```
Expected: Each SOURCE.md should clearly state plugin shell authorship and distinguish between verbatim and adapted skills.

- [ ] **Step 2: Read all bundle-manifest.json files to check content_mode and authorship fields**

For each plugin:
```bash
cat codex-marketplace/plugins/<plugin>/references/bundle-manifest.json
```
Expected: Each entry should have `content_mode` (verbatim/adapted), and verbatim entries should have `source_author`, `source_license`, `source_repo` fields.

- [ ] **Step 3: Read all source-map.md files to check attribution consistency**

For each plugin:
```bash
cat codex-marketplace/plugins/<plugin>/references/source-map.md
```
Expected: Source maps should distinguish verbatim vs adapted content and include upstream author information.

- [ ] **Step 4: Sample skill frontmatter to check metadata presence**

For each plugin, sample 2-3 skills:
```bash
head -20 codex-marketplace/plugins/<plugin>/skills/<skill>/SKILL.md
```
Expected: Skills should have frontmatter metadata including `source_author`, `source_license`, `source_repo`, `content_mode` for verbatim skills, and `adapted_author` for adapted skills.

- [ ] **Step 5: Document audit findings**

Create `docs/superpowers/plans/2026-06-19-mark-262-audit-findings.md` with:
- List of plugins with missing/incorrect plugin-level authorship
- List of plugins with missing bundle-manifest authorship fields
- List of plugins with missing source-map attribution
- List of plugins with missing skill frontmatter metadata
- Specific examples of verbatim vs adapted misclassification

---

## Task 2: Fix security-pack licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/security-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/security-pack/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/security-pack/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json content_mode and authorship fields**

For each entry in `security-pack/references/bundle-manifest.json`:
- Codex Cortex skills: Set `content_mode: "verbatim"`, add `source_author: "NickCrew"`, `source_license: "MIT"`, `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- ECC skills: Set `content_mode: "verbatim"`, add `source_author: "Affaan Mustafa"` (or "Community contributors" for community skills), `source_license: "MIT"`, `source_repo: "https://github.com/affaan-m/ECC"`
- Add `source_path` field pointing to retained upstream custody

- [ ] **Step 2: Update source-map.md to distinguish verbatim vs adapted**

Change table to include columns: `Content mode`, `Source origin`, `Upstream author`, `Upstream license`, `Source path`
- Mark Codex Cortex skills as `verbatim` with upstream authorship
- Mark ECC skills as `verbatim` with upstream authorship
- Remove "Adapted" language if content is actually verbatim

- [ ] **Step 3: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `security-pack/skills/`:
```yaml
---
metadata:
  origin: ECC # or Codex Cortex
  source_author: Affaan Mustafa # or NickCrew
  source_license: MIT
  source_repo: https://github.com/affaan-m/ECC # or https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/ecc/upstream/skills/<skill>/SKILL.md
  content_mode: verbatim
---
```

- [ ] **Step 4: Update SOURCE.md to clarify plugin shell authorship**

Add explicit statement:
"The plugin shell is authored by Harley Bartles. The projected skill roots retain their upstream source author, source license, and source path in the bundle manifest and source map so verbatim content stays attributable."

- [ ] **Step 5: Validate security-pack changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 3: Fix architecture-pack licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/architecture-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/architecture-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/architecture-pack/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/architecture-pack/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json to add missing authorship fields**

For each entry in `architecture-pack/references/bundle-manifest.json`:
- Add `source_author: "NickCrew"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- Add `source_path` field pointing to Codex Cortex custody

- [ ] **Step 2: Update source-map.md to include upstream authorship**

Add columns to table: `Upstream author`, `Upstream license`
- Fill in NickCrew and MIT for all entries

- [ ] **Step 3: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `architecture-pack/skills/`:
```yaml
---
metadata:
  origin: Codex Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/codex-cortex/upstream/skills/<skill>/SKILL.md
  content_mode: verbatim
---
```

- [ ] **Step 4: Update SOURCE.md to clarify plugin shell authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and verbatim skill attribution.

- [ ] **Step 5: Validate architecture-pack changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 4: Fix frontend-pack licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/frontend-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/frontend-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/frontend-pack/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/frontend-pack/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json to add missing authorship fields**

For each entry in `frontend-pack/references/bundle-manifest.json`:
- Add `source_author: "NickCrew"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- Add `source_path` field pointing to Claude-Cortex custody

- [ ] **Step 2: Update source-map.md to include upstream authorship**

Add columns to table: `Upstream author`, `Upstream license`
- Fill in NickCrew and MIT for all entries

- [ ] **Step 3: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `frontend-pack/skills/`:
```yaml
---
metadata:
  origin: Claude-Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/claude-cortex/upstream/skills/<skill>/SKILL.md
  content_mode: verbatim
---
```

- [ ] **Step 4: Update SOURCE.md to clarify plugin shell authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and verbatim skill attribution.

- [ ] **Step 5: Validate frontend-pack changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 5: Fix dotnet-kit licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/dotnet-kit/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/dotnet-kit/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/dotnet-kit/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json to add upstream authorship fields**

For each entry in `dotnet-kit/references/bundle-manifest.json`:
- Add `source_author: "codewithmukesh"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/codewithmukesh/dotnet-claude-kit"`
- Add `adapted_author: "Harley Bartles"` for adapted entries
- Add `source_path` field pointing to dotnet-claude-kit custody

- [ ] **Step 2: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `dotnet-kit/skills/`:
```yaml
---
metadata:
  origin: dotnet-claude-kit
  source_author: codewithmukesh
  source_license: MIT
  source_repo: https://github.com/codewithmukesh/dotnet-claude-kit
  source_path: sources/third_party/dotnet-claude-kit/upstream/skills/<skill>/SKILL.md
  content_mode: adapted
  adapted_author: Harley Bartles
---
```

- [ ] **Step 3: Update SOURCE.md to clarify plugin shell and adaptation authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and adapted skill attribution.

- [ ] **Step 4: Validate dotnet-kit changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 6: Fix language-patterns-pack licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/language-patterns-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/language-patterns-pack/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/language-patterns-pack/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json to add upstream authorship fields**

For each entry in `language-patterns-pack/references/bundle-manifest.json`:
- Add `source_author: "NickCrew"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- For adapted entries, add `adapted_author: "Harley Bartles"`
- Add `source_path` field pointing to Claude-Cortex custody

- [ ] **Step 2: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `language-patterns-pack/skills/`:
```yaml
---
metadata:
  origin: Claude-Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/codex-cortex/upstream/skills/<skill>/SKILL.md
  content_mode: adapted # or verbatim for reference files
  adapted_author: Harley Bartles # for adapted entries
---
```

- [ ] **Step 3: Update SOURCE.md to clarify plugin shell and adaptation authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and adapted skill attribution.

- [ ] **Step 4: Validate language-patterns-pack changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 7: Fix api-contracts-pack licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/api-contracts-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/api-contracts-pack/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/api-contracts-pack/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json to add upstream authorship fields**

For each entry in `api-contracts-pack/references/bundle-manifest.json`:
- Add `source_author: "NickCrew"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- For adapted entries, add `adapted_author: "Harley Bartles"`
- Add `source_path` field pointing to Claude-Cortex custody

- [ ] **Step 2: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `api-contracts-pack/skills/`:
```yaml
---
metadata:
  origin: Claude-Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/codex-cortex/upstream/skills/<skill>/SKILL.md
  content_mode: adapted
  adapted_author: Harley Bartles
---
```

- [ ] **Step 3: Update SOURCE.md to clarify plugin shell and adaptation authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and adapted skill attribution.

- [ ] **Step 4: Validate api-contracts-pack changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 8: Fix codex-cortex licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/codex-cortex/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/codex-cortex/SOURCE.md`

- [ ] **Step 1: Fix bundle-manifest.json content_mode and authorship fields**

For each entry in `codex-cortex/references/bundle-manifest.json`:
- Change `content_mode` from "adapted" to "verbatim" for verbatim projections
- Add `source_author: "NickCrew"`
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/NickCrew/Claude-Cortex"`
- Add `source_path` field pointing to Claude-Cortex custody

- [ ] **Step 2: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `codex-cortex/skills/`:
```yaml
---
metadata:
  origin: Claude-Cortex
  source_author: NickCrew
  source_license: MIT
  source_repo: https://github.com/NickCrew/Claude-Cortex
  source_path: sources/third_party/codex-cortex/upstream/skills/<skill>/SKILL.md
  content_mode: verbatim
---
```

- [ ] **Step 3: Update SOURCE.md to clarify plugin shell authorship**

Add explicit statement about plugin shell authorship by Harley Bartles and verbatim skill attribution.

- [ ] **Step 4: Validate codex-cortex changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 9: Fix repo-worker-base licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/repo-worker-base/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/repo-worker-base/skills/*/SKILL.md` (all skills)
- Modify: `codex-marketplace/plugins/repo-worker-base/SOURCE.md`

- [ ] **Step 1: Add repo_index metadata to bundle-manifest.json**

Add repo_index section with source_ledger and provenance_refs:
```json
"repo_index": {
  "source_ledger": [
    "sources/first_party/skills/repo-worker-base/SKILL.md",
    "sources/first_party/core/boring-loop/SKILL.md",
    "sources/first_party/core/connector-safety/SKILL.md",
    "sources/first_party/core/github-operations/SKILL.md"
  ],
  "provenance_refs": [
    "provenance/repo-worker-base.md",
    "codex-marketplace/plugins/repo-worker-base/references/source-map.md"
  ],
  "agents_md": null,
  "registry_alignment": {
    "status": "aligned",
    "note": null
  }
}
```

- [ ] **Step 2: Add frontmatter metadata to all skill SKILL.md files**

For each skill in `repo-worker-base/skills/`:
```yaml
---
metadata:
  origin: first_party
  source_author: Harley Bartles
  source_license: MIT
  source_repo: https://github.com/HarleyBartles/agent-asset-marketplace
  source_path: sources/first_party/skills/<skill>/SKILL.md
  content_mode: verbatim
---
```

- [ ] **Step 3: Update SOURCE.md to clarify first-party authorship**

Ensure SOURCE.md clearly states this is a first-party plugin authored by Harley Bartles.

- [ ] **Step 4: Validate repo-worker-base changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 10: Fix everything-codex-code licensing/provenance

**Files:**
- Modify: `codex-marketplace/plugins/everything-codex-code/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/everything-codex-code/skills/*/SKILL.md` (all skills)

- [ ] **Step 1: Add source authorship fields to bundle-manifest.json components**

For each component in `everything-codex-code/references/bundle-manifest.json`:
- Add `source_author: "Affaan Mustafa"` (or "Community contributors" for community skills)
- Add `source_license: "MIT"`
- Add `source_repo: "https://github.com/affaan-m/ECC"`
- Add `source_path` field pointing to superpowers-ecc skills

- [ ] **Step 2: Ensure skill frontmatter metadata is inherited from superpowers-ecc**

Verify that each skill in `everything-codex-code/skills/` has the same frontmatter metadata as the corresponding skill in `superpowers-ecc/skills/`.

- [ ] **Step 3: Validate everything-codex-code changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

---

## Task 11: Update validator to enforce licensing/provenance standards

**Files:**
- Modify: `tools/validate_marketplace.py`

- [ ] **Step 1: Add validation for bundle-manifest authorship fields**

In `_validate_projection_entry_provenance` function, add checks:
- For `content_mode: "verbatim"` entries, require `source_author`, `source_license`, `source_repo`, `source_path` fields
- For `content_mode: "adapted"` entries, require `adapted_author` field
- Ensure upstream author is not claimed as repo author for verbatim skills

- [ ] **Step 2: Add validation for skill frontmatter metadata**

Add function to check that SKILL.md files have required metadata fields based on content_mode:
- Verbatim skills: `source_author`, `source_license`, `source_repo`, `source_path`, `content_mode`
- Adapted skills: `source_author`, `source_license`, `source_repo`, `source_path`, `content_mode`, `adapted_author`

- [ ] **Step 3: Add validation for plugin-level vs skill-level authorship separation**

Add check to ensure plugin-level license/author metadata does not flatten skill-level attribution:
- Plugin `plugin_author` should be Harley Bartles for repo-authored plugin shells
- Plugin `plugin_license` should be MIT for repo-authored plugin shells
- Individual skills should retain their own upstream authorship in frontmatter and bundle manifest

- [ ] **Step 4: Test validator changes**

Run: `py -3 tools/validate_marketplace.py`
Expected: Validator should catch missing authorship fields and misattributed content

---

## Task 12: Run full validation and regenerate artifacts

**Files:**
- Run: `py -3 tools/update_skill_artifacts.py --all`
- Run: `py -3 tools/generate_marketplace.py`
- Run: `py -3 tools/generate_repo_index.py`
- Run: `py -3 tools/validate_marketplace.py`
- Run: `py -3 tools/validate_repo_index.py`
- Run: `py -3 tools/validate_skill_zips.py`
- Run: `git diff --check`

- [ ] **Step 1: Update all skill artifacts**

Run: `py -3 tools/update_skill_artifacts.py --all`
Expected: All skill artifacts regenerated with updated metadata

- [ ] **Step 2: Generate marketplace**

Run: `py -3 tools/generate_marketplace.py`
Expected: Marketplace generated successfully

- [ ] **Step 3: Generate repo index**

Run: `py -3 tools/generate_repo_index.py`
Expected: Repo index generated successfully

- [ ] **Step 4: Validate marketplace**

Run: `py -3 tools/validate_marketplace.py`
Expected: PASS

- [ ] **Step 5: Validate repo index**

Run: `py -3 tools/validate_repo_index.py`
Expected: PASS

- [ ] **Step 6: Validate skill zips**

Run: `py -3 tools/validate_skill_zips.py`
Expected: PASS

- [ ] **Step 7: Check for whitespace issues**

Run: `git diff --check`
Expected: No whitespace errors

---

## Task 13: Create PR with validation evidence

**Files:**
- Create: Branch and commit changes
- Create: PR with comprehensive description

- [ ] **Step 1: Create feature branch**

Run: `git checkout -b mark-262-licensing-provenance-audit`

- [ ] **Step 2: Commit changes with descriptive messages**

Run: `git add` and `git commit` for each plugin fix with messages like:
```
fix: add upstream authorship metadata to security-pack bundle manifest and skills

- Add source_author, source_license, source_repo fields to bundle-manifest.json entries
- Add frontmatter metadata to all skill SKILL.md files
- Update source-map.md to distinguish verbatim vs adapted content
- Clarify plugin shell authorship in SOURCE.md
```

- [ ] **Step 3: Push branch to GitHub**

Run: `git push -u origin mark-262-licensing-provenance-audit`

- [ ] **Step 4: Create PR with comprehensive description**

Create PR with:
- Summary of licensing/provenance fixes across all plugins
- Before/after examples for verbatim and adapted skills
- Validator coverage added
- Generated artifact explanation
- Validation output
- List of any remaining ambiguities needing follow-up

- [ ] **Step 5: Request review**

PR should be ready for Codex review and manual review.

---

## Self-Review

**1. Spec coverage:** 
- Audited all active marketplace plugins ✓
- Fixed bundle-manifest authorship fields ✓
- Fixed source-map attribution ✓
- Fixed skill frontmatter metadata ✓
- Updated validator to enforce standards ✓
- Ran full validation ladder ✓

**2. Placeholder scan:** 
- No TBD, TODO, or placeholder text found ✓
- All steps contain specific file paths and content ✓
- All validation commands are specified ✓

**3. Type consistency:** 
- Field names consistent across bundle manifests ✓
- Frontmatter metadata structure consistent ✓
- Validation function names consistent ✓