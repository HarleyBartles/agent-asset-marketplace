# MARK-248 ECC Security Skills into Security Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`[ ]`) syntax for tracking.

**Goal:** Replace the prior `security-pack` slice with the ECC security-related skills in the canonical `security-pack` while preserving ECC provenance, keeping compliance-only material out of scope, and regenerating the installable marketplace artifacts.

**Architecture:** Use the retained ECC custody tree under `sources/third_party/ecc/upstream/` as the source basis, replace the prior Codex Cortex-backed `security-pack` skill set with the ECC security-focused slice, and project only the security-pack-fit skills into `codex-marketplace/plugins/security-pack/` with matching source maps, bundle inventory, and generated zips. Treat `defi-amm-security`, `django-security`, `laravel-security`, `llm-trading-agent-security`, `network-config-validation`, `perl-security`, `prediction-market-risk-review`, `quarkus-security`, `safety-guard`, `security-bounty-hunter`, `security-review`, `security-scan`, and `springboot-security` as the include set; leave `evm-token-decimals`, `healthcare-phi-compliance`, and `hipaa-compliance` out because they are not a clear fit for this pack slice.

**Tech Stack:** Markdown skill sources, JSON bundle manifests, provenance notes, repo index metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, `git diff --check`

---

### Task 1: Lock the ECC source basis and record the projection boundary

**Files:**
- Read: `sources/third_party/ecc/upstream/manifest.json`
- Read: `sources/third_party/ecc/upstream/skills/defi-amm-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/django-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/laravel-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/llm-trading-agent-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/network-config-validation/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/perl-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/prediction-market-risk-review/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/quarkus-security/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/safety-guard/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/security-bounty-hunter/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/security-review/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/security-scan/SKILL.md`
- Read: `sources/third_party/ecc/upstream/skills/springboot-security/SKILL.md`

- [ ] **Step 1: Confirm the include and reject set**

Use the upstream manifest and skill headers to verify the include set above, then keep `evm-token-decimals`, `healthcare-phi-compliance`, and `hipaa-compliance` out of the security-pack projection.

- [ ] **Step 2: Capture ECC provenance**

Create a provenance note that records the ECC upstream repository, pinned commit, retained custody root, and the fact that this issue projects into `security-pack`, not into a new inventory surface.

### Task 2: Project the selected ECC skills into `security-pack`

**Files:**
- Create: `provenance/ecc.md`
- Modify: `codex-marketplace/plugins/security-pack/.codex-plugin/plugin.json`
- Modify: `codex-marketplace/plugins/security-pack/README.md`
- Modify: `codex-marketplace/plugins/security-pack/SOURCE.md`
- Modify: `codex-marketplace/plugins/security-pack/references/source-map.md`
- Modify: `codex-marketplace/plugins/security-pack/references/bundle-manifest.json`
- Remove: `codex-marketplace/plugins/security-pack/skills/secure-coding-practices/`
- Remove: `codex-marketplace/plugins/security-pack/skills/owasp-top-10/`
- Remove: `codex-marketplace/plugins/security-pack/skills/security-testing-patterns/`
- Remove: `codex-marketplace/plugins/security-pack/skills/threat-modeling-techniques/`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/defi-amm-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/django-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/laravel-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/llm-trading-agent-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/network-config-validation/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/perl-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/prediction-market-risk-review/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/quarkus-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/safety-guard/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/security-bounty-hunter/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/security-review/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/security-scan/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/springboot-security/SKILL.md`
- Modify or create: `codex-marketplace/plugins/security-pack/skills/*/references/*`
- Modify or create: `generated/skill-zips/security-pack/*/skill.zip`
- Modify: `generated/skill-zips/registry.json`
- Modify: `repo-index/repo-index.json`
- Modify only if needed: `gpt-overlays/manifest.json`

- [ ] **Step 1: Replace the old pack slices with the selected ECC security skills**

Remove the old Codex Cortex-backed `security-pack` skill roots and project the selected ECC security skills into the plugin shape, keeping the pack focused on security review, security testing, scanning, and adjacent safety guidance.

- [ ] **Step 2: Update the pack metadata and source map**

Refresh the README, `SOURCE.md`, bundle manifest, and source map so they describe the ECC basis, the projected skill list, and the out-of-scope compliance-only candidates.

- [ ] **Step 3: Regenerate installable skill zips**

Ensure the pack exports deterministic zips for each included skill and that the generated registry and repo index stay aligned with the new pack contents.

### Task 3: Regenerate and validate the repository surfaces

**Files:**
- Modify: `generated/skill-zips/registry.json`
- Modify: `repo-index/repo-index.json`
- Modify: `gpt-overlays/manifest.json` only if the selected skill set requires overlay or exclusion changes

- [ ] **Step 1: Regenerate the skill corpus**

Run:

```powershell
py -3 tools/update_skill_artifacts.py --all
```

Expected: the `security-pack` zips and registry entries refresh together, without touching unrelated surfaces beyond any required generator churn.

- [ ] **Step 2: Validate the workspace**

Run:

```powershell
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/validate_skill_zips.py
git diff --check
```

Expected: validation passes, and any blocker that remains is stated exactly in the issue return.

### Task 4: Publish the branch evidence

**Files:**
- None beyond the code changes above

- [ ] **Step 1: Review the diff and commit**

Use the issue branch only, inspect the final diff, and commit the security-pack projection with a message that names the ECC security skills work.

- [ ] **Step 2: Push the branch and open a draft PR**

Push `harleydbartles/mark-248-project-ecc-security-skills-into-security-pack` and open a draft PR against `main` so the publication surface has a durable GitHub receipt.

- [ ] **Step 3: Return the evidence set**

Report the PR URL, branch, changed files, generated-artifact explanation, validation output, and any remaining blocker or follow-up slice.
