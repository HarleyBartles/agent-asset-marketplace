# MARK-262 Licensing Provenance Audit Findings

**Date:** 2026-06-19
**Auditor:** Automated marketplace audit
**Scope:** All 16 active marketplace plugins from `codex-marketplace/plugin-roots.json`

## Executive Summary

This audit examined licensing and provenance metadata across all active marketplace plugins to ensure compliance with MARK-244 standard:
- Plugins authored by Harley / Asset Marketplace as plugin projections
- Skills projected verbatim retain upstream author and upstream license
- Skills adapted state adapted authorship honestly
- Plugin-level license/rights metadata must not flatten or misattribute upstream skill authorship

**Overall Status:** PARTIALLY COMPLIANT - 3 critical gaps, 9 plugins with missing authorship fields

---

## Finding 1: Missing source-map.md Files (3 Plugins)

**Status:** CRITICAL - Violates MARK-244 attribution requirement

**Affected Plugins:**
1. `unslop` - No `codex-marketplace/plugins/unslop/references/source-map.md`
2. `game-studio` - No `codex-marketplace/plugins/game-studio/references/source-map.md`
3. `wild-bunch-project-pack` - No `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`

**Expected:** Each plugin should have a source-map.md that distinguishes verbatim vs adapted content and includes upstream author information.

**Evidence:**
- `unslop/SOURCE.md` (line 3): "This plugin adapts the upstream `mshumer/unslop` workflow"
- `unslop/references/bundle-manifest.json` (lines 17-18): Marks content as "adapted" but no source-map.md to document this
- `game-studio/SOURCE.md` (line 7): "Repo: `openai/plugins`" - third-party origin
- `game-studio/references/bundle-manifest.json` (lines 17-25): All entries marked "verbatim" but no source-map.md
- `wild-bunch-project-pack/SOURCE.md` (line 8): "mixed first-party and third-party custody"
- `wild-bunch-project-pack/references/bundle-manifest.json` (lines 78-84): Third-party entries present but no source-map.md

**Recommendation:** Create source-map.md files for these three plugins following the pattern in `adventures-pack/references/source-map.md` or `dotnet-kit/references/source-map.md`.

---

## Finding 2: Missing Upstream Authorship Fields in Bundle Manifests (9 Plugins)

**Status:** HIGH - Violates MARK-244 attribution requirement for verbatim/adapted content

**Affected Plugins and Missing Fields:**

### 2a. Codex Cortex-based plugins (missing `source_author`, `source_license`, `source_repo`)
- `architecture-pack` - All 22 entries missing upstream authorship
- `api-contracts-pack` - All 6 entries missing upstream authorship
- `frontend-pack` - All 5 entries missing upstream authorship
- `language-patterns-pack` - All 34 entries missing upstream authorship
- `codex-cortex` - All 71 entries missing upstream authorship

**Expected Fields for Codex Cortex entries:**
```json
{
  "source_author": "NickCrew",
  "source_license": "MIT",
  "source_repo": "https://github.com/NickCrew/Claude-Cortex",
  "source_path": "sources/third_party/codex-cortex/upstream/skills/<skill>/SKILL.md"
}
```

**Evidence:**
- `architecture-pack/references/bundle-manifest.json` (lines 14-19): Entry for `cqrs-event-sourcing` has `content_mode: "verbatim"` but no `source_author`, `source_license`, or `source_repo`
- `api-contracts-pack/references/bundle-manifest.json` (lines 14-18): Entry for `api-design-patterns` marked `content_mode: "adapted"` but missing upstream origin fields
- `frontend-pack/references/bundle-manifest.json` (lines 14-18): Entry for `react-performance-optimization` marked `content_mode: "verbatim"` but missing upstream authorship

### 2b. Dotnet Kit (missing `source_author`, `source_license`, `source_repo`)
- `dotnet-kit` - All 6 entries missing upstream authorship

**Expected Fields for Dotnet Kit entries:**
```json
{
  "source_author": "codewithmukesh",
  "source_license": "MIT",
  "source_repo": "https://github.com/codewithmukesh/dotnet-claude-kit",
  "source_path": "sources/third_party/dotnet-claude-kit/upstream/skills/<skill>/SKILL.md"
}
```

**Evidence:**
- `dotnet-kit/references/bundle-manifest.json` (lines 14-18): Entry for `modern-csharp` has `content_mode: "adapted"` but no upstream authorship fields

### 2c. Unslop (missing `adapted_author`)
- `unslop` - Entries marked "adapted" but missing `adapted_author` field

**Expected Field:**
```json
{
  "adapted_author": "Harley Bartles",
  "source_author": "mshumer",
  "source_license": "MIT",
  "source_repo": "https://github.com/mshumer/unslop"
}
```

**Evidence:**
- `unslop/references/bundle-manifest.json` (lines 17-18): Entry for `unslop/SKILL.md` marked `content_mode: "adapted"` but no `adapted_author` field

### 2d. Game Studio (missing upstream authorship)
- `game-studio` - All 9 entries marked "verbatim" but missing upstream authorship fields

**Expected Fields:**
```json
{
  "source_author": "OpenAI",
  "source_license": "MIT",
  "source_repo": "https://github.com/openai/plugins",
  "source_path": "sources/third_party/game-studio/upstream/skills/<skill>/SKILL.md"
}
```

**Evidence:**
- `game-studio/references/bundle-manifest.json` (lines 14-18): Entry for `game-playtest` marked `content_mode: "verbatim"` but no upstream authorship

### 2e. Wild Bunch Project Pack (missing upstream authorship for third-party entries)
- `wild-bunch-project-pack` - Third-party entries (5 skills from game-studio) missing upstream authorship

**Evidence:**
- `wild-bunch-project-pack/references/bundle-manifest.json` (lines 77-84): Entry for `web-game-foundations` marked `content_mode: "verbatim"` and `source_category: "third_party"` but no `source_author`, `source_license`, or `source_repo`

**Recommendation:** Add the missing fields to all bundle-manifest.json entries. Reference `superpowers-ecc/references/bundle-manifest.json` (lines 36-45) as the gold standard for complete authorship metadata.

---

## Finding 3: Missing Skill Frontmatter Metadata (14 Plugins)

**Status:** HIGH - Violates MARK-244 skill-level attribution requirement

**Affected Plugins:** All except `superpowers-ecc` and `house-skills`

**Current State:**
- Most skill SKILL.md files only have basic frontmatter:
  ```yaml
  ---
  name: <skill-name>
  description: <description>
  ---
  ```

**Expected State (from superpowers-ecc gold standard):**
```yaml
---
name: <skill-name>
description: <description>
metadata:
  origin: ECC  # or upstream source name
  source_author: Affaan Mustafa  # or upstream author
  source_license: MIT
  source_repo: https://github.com/affaan-m/ECC  # or upstream repo
  source_path: sources/third_party/ecc/upstream/skills/<skill>/SKILL.md
  content_mode: verbatim  # or adapted
---
```

**Evidence:**
- `unslop/skills/unslop/SKILL.md` (lines 1-4): Only has `name` and `description`, missing metadata block
- `game-studio/skills/game-studio/SKILL.md` (lines 1-4): Only has `name` and `description`, missing metadata block
- `superpowers-plus/skills/brainstorming/SKILL.md` (lines 1-4): Only has `name` and `description`, missing metadata block
- `architecture-pack/skills/cqrs-event-sourcing/SKILL.md`: Missing metadata block
- `frontend-pack/skills/react-performance-optimization/SKILL.md`: Missing metadata block
- `security-pack/skills/secure-coding-practices/SKILL.md`: Missing metadata block
- All other plugins: Skills missing metadata blocks

**Counterexample (Gold Standard):**
- `superpowers-ecc/skills/agent-harness-construction/SKILL.md` (lines 1-11): Complete metadata block with origin, source_author, source_license, source_repo, source_path, content_mode

**Recommendation:** Add metadata blocks to all skill SKILL.md files. For verbatim skills, include upstream authorship. For adapted skills, include adapted_author.

---

## Finding 4: Inconsistent Plugin-Level Authorship Statements (11 Plugins)

**Status:** MEDIUM - Violates MARK-244 clarity requirement

**Affected Plugins:**
- `house-skills`, `adventures-pack`, `unslop`, `game-studio`, `wild-bunch-project-pack`, `repo-worker-base`, `dotnet-kit`, `codex-cortex`, `api-contracts-pack`, `architecture-pack`, `language-patterns-pack`, `security-pack`, `frontend-pack`

**Current State:**
- Most SOURCE.md files don't explicitly state that the plugin shell is authored by Harley Bartles / Asset Marketplace
- Some SOURCE.md files state this clearly (superpowers-ecc, superpowers-plus)

**Expected State:**
Each SOURCE.md should include an explicit statement like:
"The plugin shell is authored by Harley Bartles. The projected skill roots retain their upstream source author, source license, and source path in the bundle manifest and source map so verbatim content stays attributable."

**Evidence:**
- `superpowers-ecc/SOURCE.md` (lines 6-8): ✅ Explicitly states plugin shell authorship
- `superpowers-plus/SOURCE.md` (lines 12-14): ✅ Clearly distinguishes first-party compositional skills
- `house-skills/SOURCE.md` (lines 1-3): ⚠️ States "reviewed first-party House Skills projection root" but doesn't explicitly state Harley as author
- `adventures-pack/SOURCE.md` (lines 1-4): ⚠️ Doesn't state plugin shell authorship
- `unslop/SOURCE.md` (lines 1-3): ⚠️ Doesn't state plugin shell authorship
- `game-studio/SOURCE.md` (lines 1-3): ⚠️ Doesn't state plugin shell authorship
- `wild-bunch-project-pack/SOURCE.md` (lines 1-3): ⚠️ Doesn't state plugin shell authorship
- `repo-worker-base/SOURCE.md` (lines 1-4): ⚠️ States "repo-canonical copy" but doesn't explicitly state Harley as author
- `dotnet-kit/SOURCE.md` (lines 1-4): ⚠️ Doesn't state plugin shell authorship
- `codex-cortex/SOURCE.md` (lines 1-8): ⚠️ Doesn't state plugin shell authorship
- `api-contracts-pack/SOURCE.md` (lines 1-5): ⚠️ Doesn't state plugin shell authorship
- `architecture-pack/SOURCE.md` (lines 1-6): ⚠️ Doesn't state plugin shell authorship
- `language-patterns-pack/SOURCE.md` (lines 1-3): ⚠️ Doesn't state plugin shell authorship
- `security-pack/SOURCE.md` (lines 1-4): ⚠️ Doesn't state plugin shell authorship
- `frontend-pack/SOURCE.md` (lines 1-6): ⚠️ Doesn't state plugin shell authorship

**Recommendation:** Add explicit authorship statements to all SOURCE.md files following the superpowers-ecc pattern.

---

## Finding 5: Verbatim vs Adapted Classification Accuracy

**Status:** GOOD - Most classifications are accurate

**Accurate Classifications:**
- ✅ `superpowers-plus`: Correctly marks upstream Superpowers skills as "verbatim" and adapted skills as "adapted"
- ✅ `superpowers-ecc`: Correctly marks all ECC skills as "verbatim"
- ✅ `wild-bunch-project-pack`: Correctly marks first-party skills as "verbatim" and third-party game skills as "verbatim"
- ✅ `architecture-pack`: Correctly marks Codex Cortex skills as "verbatim"
- ✅ `frontend-pack`: Correctly marks Codex Cortex skills as "verbatim"

**Potentially Inaccurate Classifications:**
- ⚠️ `security-pack`: Marks Codex Cortex and ECC skills as "adapted" when they should be "verbatim"
  - Evidence: `security-pack/references/bundle-manifest.json` (lines 31-32): "Adapted from the retained Codex Cortex source" but content is byte-identical
  - The adaptation note says "adapted" but the actual content is verbatim copies from upstream
  - Recommendation: Change `content_mode` to "verbatim" and add upstream authorship fields

- ⚠️ `dotnet-kit`: Marks all skills as "adapted" when some are verbatim
  - Evidence: `dotnet-kit/references/bundle-manifest.json` (lines 17-18): All entries marked "adapted"
  - SOURCE.md (lines 15-19) indicates these are "Reimplemented" and "Removed provider-specific" - so "adapted" is correct
  - This is accurate

- ⚠️ `codex-cortex`: Marks all skills as "adapted" when they should be "verbatim"
  - Evidence: `codex-cortex/references/bundle-manifest.json` (lines 17-18): All entries marked "adapted"
  - But these are the canonical custody copies, not projections
  - The "adapted" note says "Imported into the Codex Cortex custody plugin and retained as the canonical seed"
  - This is a custody plugin, not a projection, so "adapted" may be the wrong classification
  - Recommendation: Clarify whether codex-cortex is a custody plugin or projection plugin

- ⚠️ `language-patterns-pack`: Marks some skills as "adapted" when they're verbatim
  - Evidence: `language-patterns-pack/references/bundle-manifest.json` (lines 17-18): `typescript-advanced-patterns` marked "adapted"
  - But the adaptation note says "Adapted from the retained Claude-Cortex snapshot so the installable pack uses skill-root-relative reference paths"
  - This is a path adaptation, not content adaptation
  - Recommendation: Clarify whether path normalization counts as "adapted" or "verbatim"

---

## Finding 6: Positive Examples (Gold Standards)

**Status:** EXCELLENT - These plugins meet MARK-244 standard

### superpowers-ecc
- ✅ SOURCE.md explicitly states plugin shell authorship (line 6)
- ✅ bundle-manifest.json has complete authorship fields for all entries (lines 36-45)
- ✅ source-map.md distinguishes verbatim vs adapted (lines 35-46)
- ✅ All skill SKILL.md files have complete metadata blocks (e.g., agent-harness-construction lines 1-11)
- ✅ Upstream author attribution preserved throughout

### superpowers-plus
- ✅ SOURCE.md clearly distinguishes first-party compositional skills (lines 12-20)
- ✅ bundle-manifest.json has content_mode and authorship fields (lines 44-86)
- ✅ source-map.md distinguishes verbatim vs adapted (lines 35-46)
- ✅ Upstream author attribution preserved

### adventures-pack
- ✅ bundle-manifest.json has content_mode for all entries
- ✅ source-map.md has complete component summary table (lines 46-67)
- ✅ First-party authorship clear

---

## Summary Table: Audit Results by Plugin

| Plugin | Source-map.md | Bundle Authorship | Skill Metadata | Plugin Authorship | Overall |
|--------|---|---|---|---|---|
| house-skills | ✅ | ✅ | ⚠️ | ⚠️ | GOOD |
| adventures-pack | ✅ | ✅ | ❌ | ⚠️ | GOOD |
| unslop | ❌ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| game-studio | ❌ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| wild-bunch-project-pack | ❌ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| superpowers-plus | ✅ | ✅ | ⚠️ | ✅ | EXCELLENT |
| superpowers-ecc | ✅ | ✅ | ✅ | ✅ | EXCELLENT |
| everything-codex-code | ✅ | ✅ | ❌ | ⚠️ | GOOD |
| repo-worker-base | ✅ | ✅ | ❌ | ⚠️ | GOOD |
| dotnet-kit | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| codex-cortex | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| api-contracts-pack | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| architecture-pack | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| language-patterns-pack | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| security-pack | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |
| frontend-pack | ✅ | ⚠️ | ❌ | ⚠️ | NEEDS WORK |

**Legend:**
- ✅ = Compliant with MARK-244
- ⚠️ = Partially compliant or unclear
- ❌ = Non-compliant or missing

---

## Recommendations (Priority Order)

### CRITICAL (Blocks MARK-244 compliance)
1. **Create missing source-map.md files** for `unslop`, `game-studio`, `wild-bunch-project-pack`
   - Files: 3
   - Effort: Medium (reference existing source-map.md files)

2. **Add upstream authorship fields to bundle manifests** for 9 plugins
   - Files: 9 bundle-manifest.json files
   - Fields to add: `source_author`, `source_license`, `source_repo`, `source_path`
   - Effort: High (9 files × ~10-70 entries each)

### HIGH (Violates attribution requirement)
3. **Add metadata blocks to skill SKILL.md files** for 14 plugins
   - Files: ~200+ skill SKILL.md files
   - Effort: High (requires systematic update across all plugins)
   - Can be automated with a script

### MEDIUM (Violates clarity requirement)
4. **Add explicit plugin authorship statements** to SOURCE.md files for 11 plugins
   - Files: 11 SOURCE.md files
   - Effort: Low (copy-paste from superpowers-ecc pattern)

### LOW (Clarification needed)
5. **Clarify verbatim vs adapted classification** for security-pack, codex-cortex, language-patterns-pack
   - Effort: Low (update content_mode and notes)

---

## Conclusion

The marketplace has strong foundational metadata in bundle manifests (all have `content_mode` fields), but is missing critical upstream authorship attribution at the skill level and in several bundle manifests. The superpowers-ecc and superpowers-plus plugins serve as excellent gold standards for MARK-244 compliance.

**Compliance Status:** 2/16 plugins fully compliant (superpowers-ecc, superpowers-plus)
**Partial Compliance:** 4/16 plugins (house-skills, adventures-pack, everything-codex-code, repo-worker-base)
**Needs Work:** 10/16 plugins

**Next Steps:** Implement recommendations in priority order, starting with creating missing source-map.md files and adding upstream authorship fields to bundle manifests.