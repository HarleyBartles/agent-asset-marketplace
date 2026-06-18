# threat-modeling-techniques Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Project Claude-Cortex `threat-modeling-techniques` into `security-pack` while preserving retained Codex Cortex custody, provenance, and publishable marketplace artifacts.

**Architecture:** Keep `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/` as the retained source snapshot, mirror that slice into `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/` as the custody projection, and adapt `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/` to stay focused on design-time threat modeling, attack surfaces, abuse cases, and security framing. Update bundle manifests, source maps, ledgers, and generated skill zips so the new slice is discoverable in both the custody surface and the installable pack.

**Tech Stack:** Markdown skill sources, JSON manifests, provenance ledgers, repo index metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `git diff --check`

---

### Task 1: Retain the upstream threat-modeling source under Codex Cortex custody

**Files:**
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/SKILL.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/attack-trees.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/data-flow-diagrams.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/dread-scoring.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/mitigation-strategies.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-spoofing.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-tampering.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-repudiation.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-disclosure.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-dos.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/stride-elevation.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/references/tools-and-process.md`
- Create: `sources/third_party/codex-cortex/upstream/skills/threat-modeling-techniques/validation/rubric.yaml`
- Modify: `sources/first_party/skills/codex-cortex/intake.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.json`
- Modify: `sources/first_party/skills/codex-cortex/decisions.md`
- Modify: `provenance/codex-cortex.md`

- [x] **Step 1: Copy the retained upstream skill into third-party custody**

Keep the upstream threat-modeling skill, references, and validation rubric under the retained Claude-Cortex custody path.

- [x] **Step 2: Record the import ledger entry**

Add the MARK-210 intake and decision entries for `threat-modeling-techniques` and the boundary note that it stays focused on design-time security framing.

### Task 2: Project the threat-modeling slice into the installable pack

**Files:**
- Modify: `codex-marketplace/plugins/codex-cortex/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/codex-cortex/README.md`
- Modify: `codex-marketplace/plugins/codex-cortex/SOURCE.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/source-map.md`
- Modify: `codex-marketplace/plugins/codex-cortex/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/SKILL.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/attack-trees.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/data-flow-diagrams.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/dread-scoring.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/mitigation-strategies.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-spoofing.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-tampering.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-repudiation.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-disclosure.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-dos.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/stride-elevation.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/references/tools-and-process.md`
- Create: `codex-marketplace/plugins/codex-cortex/skills/threat-modeling-techniques/validation/rubric.yaml`
- Create: `codex-marketplace/plugins/security-pack/.codex-plugin/plugin.json`
- Create: `codex-marketplace/plugins/security-pack/README.md`
- Create: `codex-marketplace/plugins/security-pack/SOURCE.md`
- Create: `codex-marketplace/plugins/security-pack/LICENSE`
- Create: `codex-marketplace/plugins/security-pack/assets/icon.svg`
- Create: `codex-marketplace/plugins/security-pack/references/bundle-manifest.json`
- Create: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/SKILL.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/attack-trees.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/data-flow-diagrams.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/dread-scoring.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/mitigation-strategies.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-spoofing.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-tampering.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-repudiation.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-disclosure.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-dos.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/stride-elevation.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/references/tools-and-process.md`
- Create: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/validation/rubric.yaml`

- [x] **Step 1: Mirror the custody surface**

Project the threat-modeling slice into `codex-cortex` so the custody plugin retains the imported source for downstream projection.

- [x] **Step 2: Build the installable pack projection**

Adapt the `security-pack` threat-modeling slice so it stays within the design-time security-framing boundary.

### Task 3: Update ledgers, docs, and discoverability surfaces

**Files:**
- Modify: `README.md`
- Modify: `codex-marketplace/README.md`
- Modify: `codex-marketplace/plugins/README.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `codex-marketplace/manifest.json`
- Modify: `codex-marketplace/plugin-roots.json`
- Modify: `sources/README.md`
- Modify: `sources/third_party/README.md`
- Modify: `repo-index/repo-index.json`

- [x] **Step 1: Refresh repo-facing docs**

Update the repo, marketplace, and source-custody guidance so they name the MARK-210 threat-modeling slice.

- [x] **Step 2: Refresh structured navigation metadata**

Keep the repo index aligned with the new source custody and projection notes.

### Task 4: Regenerate and validate artifacts

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `generated/skill-zips/codex-cortex/threat-modeling-techniques/skill.zip`
- Modify: `generated/skill-zips/security-pack/threat-modeling-techniques/skill.zip`

- [x] **Step 1: Regenerate the targeted skill zips**

Run: `py -3 tools/update_skill_artifacts.py --skill security-pack/threat-modeling-techniques`
Expected: new deterministic zips for the `security-pack` and `codex-cortex` threat-modeling slices plus the matching registry entries.

- [x] **Step 2: Validate the marketplace and repo index**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
git diff --check
```

Expected: all commands pass with no unexpected drift.

- [x] **Step 3: Capture publication evidence**

Record the branch name, final head SHA, changed files, generated zip paths, validation output, and the exact composition note showing that `threat-modeling-techniques` stays narrower than generic compliance or infra security material.
