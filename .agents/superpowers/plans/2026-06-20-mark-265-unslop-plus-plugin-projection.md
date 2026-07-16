# MARK-265 unslop+ Plugin Projection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the first `unslop+` plugin projection as one composed skill in one plugin, bundling the third-party Unslop engine with thirteen first-party reviewed portable profiles.

**Architecture:** Create a new plugin root `codex-marketplace/plugins/unslop-plus/` that composes the third-party Unslop engine (copied from existing `unslop` plugin) with thirteen new first-party portable profiles derived from the Linear issue requirements. The plugin will follow the existing marketplace projection conventions with proper provenance tracking, bundle manifests, and registry integration.

**Tech Stack:** Python scripts (Unslop engine), Markdown profiles, JSON manifests, Codex plugin format

---

## Task 1: Create unslop-plus plugin root structure

**Files:**
- Create: `codex-marketplace/plugins/unslop-plus/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/unslop-plus/SOURCE.md`
- Create: `codex-marketplace/plugins/unslop-plus/LICENSE`
- Create: `codex-marketplace/plugins/unslop-plus/README.md`
- Create: `codex-marketplace/plugins/unslop-plus/assets/icon.svg`
- Create: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`

- [ ] **Step 1: Create plugin.json for unslop-plus**
- [ ] **Step 2: Create SOURCE.md documenting the composition**
- [ ] **Step 3: Create LICENSE file (MIT)**
- [ ] **Step 4: Create README.md**
- [ ] **Step 5: Copy icon.svg from existing unslop plugin**
- [ ] **Step 6: Create initial bundle-manifest.json**
- [ ] **Step 7: Commit plugin root structure**

## Task 2: Copy Unslop engine from existing plugin

**Files:**
- Modify: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/scripts/`
- Create: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/references/upstream-provenance.md`

- [ ] **Step 1: Copy Unslop scripts directory**
- [ ] **Step 2: Copy upstream provenance reference**
- [ ] **Step 3: Update bundle-manifest.json with engine entries**
- [ ] **Step 4: Commit engine copy**

## Task 3-15: Create thirteen portable profiles

For each of the thirteen profiles (writing, technical-writing, implementation-plans, code-review, worker-returns, debugging, frontend-react, frontend-ui, api-design, architecture, testing, security-review, cleanup-custody):

**Files:**
- Create: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/profiles/<profile-name>.md`
- Modify: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`

- [ ] **Step 1: Create profile from Linear requirements**
- [ ] **Step 2: Update bundle-manifest.json with profile entry**
- [ ] **Step 3: Commit profile**

Each profile must include:
- Purpose section
- Where to use section
- Slop patterns to avoid
- Required avoid rules
- Required prefer-instead rules
- False positives / do not overapply
- Before/after examples
- Acceptance checks

## Task 16: Create main skill SKILL.md and agent config

**Files:**
- Create: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/SKILL.md`
- Create: `codex-marketplace/plugins/unslop-plus/skills/unslop-plus/agents/openai.yaml`
- Modify: `codex-marketplace/plugins/unslop-plus/references/bundle-manifest.json`

- [ ] **Step 1: Create main SKILL.md**
- [ ] **Step 2: Create agent config**
- [ ] **Step 3: Update bundle-manifest.json with skill entries**
- [ ] **Step 4: Commit main skill and agent config**

## Task 17: Add unslop-plus to plugin-roots.json

**Files:**
- Modify: `codex-marketplace/plugin-roots.json`

- [ ] **Step 1: Add unslop-plus entry to plugin-roots.json**
- [ ] **Step 2: Commit plugin-roots.json update**

## Task 18: Update marketplace manifest

**Files:**
- Modify: `codex-marketplace/manifest.json`

- [ ] **Step 1: Add unslop-plus to marketplace manifest**
- [ ] **Step 2: Commit marketplace manifest update**

## Task 19: Run marketplace validation

**Files:**
- No file changes

- [ ] **Step 1: Run marketplace validation**
- [ ] **Step 2: Review validation output**
- [ ] **Step 3: Run git diff check**

## Task 20: Push branch and create PR

**Files:**
- No file changes

- [ ] **Step 1: Push branch to origin**
- [ ] **Step 2: Create draft PR**

---

## Profile Content Requirements

Each of the thirteen profiles must be derived from the Linear issue requirements and include:

1. **writing** - Generic AI prose patterns (from document ID: 53fe21b1-f7b5-4318-8ed1-8553f10c5609)
2. **technical-writing** - Documentation and technical content (from document ID: 71ed9669-3683-4fc9-991c-b9a68a80db46)
3. **implementation-plans** - Executable coding plans (from document ID: 8760a228-9dec-417e-b250-bf581447cfd4)
4. **code-review** - Evidence-based code review (from document ID: a6dd9b9a-57dc-4ab2-a30d-f3ae2fef9b8b)
5. **worker-returns** - Completion report validation (from document ID: 929af3ee-285c-4e52-a6eb-09415559cf25)
6. **debugging** - Systematic bug diagnosis (from document ID: c9b987d6-1357-4e1e-9965-592701df7c61)
7. **frontend-react** - React implementation defaults (from document ID: 67912abd-23b2-4e46-a718-e27c794aa623)
8. **frontend-ui** - Generic UI patterns (from document ID: c33e7ea6-a7ad-4ee0-be35-c8d3fcc193b2)
9. **api-design** - API contract design (from document ID: 8453a7c5-5931-474b-9541-bfd9580b128b)
10. **architecture** - Pattern-based architecture reasoning (from document ID: a22aab90-32f5-441c-8e92-174d3c1d3794)
11. **testing** - Behavior-focused testing (from document ID: a9aaa8ca-e9ad-40c3-ae37-f590893f5fd6)
12. **security-review** - Concrete security analysis (from document ID: 44d55677-a5e6-4ef9-96b8-4d63d01b38f4)
13. **cleanup-custody** - Repository hygiene decisions (from document ID: 74b27a98-a69d-42ef-9f09-ef3af4812099)

**Note:** There are two "writing" documents with identical content (IDs: 53fe21b1-f7b5-4318-8ed1-8553f10c5609 and 8639744c-e50d-48f2-9f31-6b7edc6e4383). This is a duplicate attachment - cover writing once in the final profile table.

## Key Implementation Requirements

1. **Exactly one plugin** - Create `unslop-plus` as a single plugin with one composed skill
2. **Portable profiles** - No Asset Marketplace-specific nouns, local issue IDs, or project-only assumptions
3. **Clear provenance** - Distinguish third-party engine custody from first-party profile authorship
4. **No temporary clutter** - Do not leave temporary generation output in the live source tree
5. **Bundle manifest** - Track all components with proper content_mode (verbatim for engine, adapted for profiles)
6. **Marketplace integration** - Update plugin-roots.json and marketplace manifest
7. **Validation** - Run marketplace validation before completion

## Definition of Done

- One `unslop+` plugin projection exists as one composed skill
- The projection includes the third-party Unslop engine/scripts plus all thirteen first-party reviewed portable profiles
- Provenance/source-map material clearly distinguishes third-party engine custody from first-party profile authorship and projection composition
- The profile library is portable across repos and does not encode Asset Marketplace-specific nouns or local issue IDs
- Generated candidates, if used, are reviewed and normalized before becoming shipped first-party profiles
- Temporary generation output is not left in the live source tree unless deliberately retained as provenance with a clear purpose
- Marketplace/plugin validators pass