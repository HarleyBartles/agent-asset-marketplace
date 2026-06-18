# codex-receipts-superpowers Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** add a first-party projected `codex-receipts-superpowers` skill that composes `writing-plans`, `executing-plans`, `codex-repo-receipts`, `using-superpowers`, and `unslop-superpowers` so non-trivial repo-backed Codex work naturally plans and publishes the matching implementation record before closeout.

**Architecture:** keep canonical first-party custody in House Skills, project the new skill into the vendored `superpowers` plugin as a directory-level wrapper, and update the bundle source/projection docs so the new skill is part of the explicit compositional surface instead of a hidden one-off. Regenerate the marketplace skill export after the source edits so the Codex-facing install surface and generated archive stay aligned.

**Tech Stack:** Markdown skill specs, `agents/openai.yaml`, Codex marketplace plugin projection files, generated skill zips, repo validation scripts.

---

### Task 1: Map the current projection seam and register the new wrapper

**Files:**
- Modify: `codex-marketplace/plugins/superpowers/SOURCE.md`
- Modify: `codex-marketplace/plugins/superpowers/PROJECTION.md`
- Modify: `codex-marketplace/plugins/house-skills/README.md` if the active first-party inventory needs an explicit mention

- [x] **Step 1: Read the existing first-party projection pattern**

Use the current `linear-superpowers`, `github-superpowers`, and `unslop-superpowers` wrapper skills as the template for the new skill wording and metadata.

- [x] **Step 2: Add `codex-receipts-superpowers` to the bundle docs**

Extend the projection/source text so `codex-receipts-superpowers` is named as a first-party compositional wrapper that belongs in the active `superpowers` surface.

- [x] **Step 3: Keep the composition boundary narrow**

State that the wrapper composes workflow-selection, planning, execution, and receipt publication, but does not fork third-party `writing-plans` or `executing-plans` source.

### Task 2: Add the canonical House Skills source and projected bundle copy

**Files:**
- Create: `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers/agents/openai.yaml`
- Create: `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/SKILL.md`
- Create: `codex-marketplace/plugins/superpowers/skills/codex-receipts-superpowers/agents/openai.yaml`

- [x] **Step 1: Write the failing source shape first**

Author the House Skills skill as a first-party compositional wrapper with explicit triggers for repo-backed planning, durable receipt publication, and final-link requirements.

- [x] **Step 2: Compose the required workflows**

The skill must tell workers to start with `using-superpowers`, then use `writing-plans`, `executing-plans`, `codex-repo-receipts`, and `unslop-superpowers` in the narrowest applicable way.

- [x] **Step 3: Require artifact linkage**

The skill must require the PR body or final worker report to link both the durable plan and the implementation record.

- [x] **Step 4: Mirror the source into the projected plugin**

Copy the House Skills source into the vendored `superpowers` plugin surface without introducing a second editable source root.

### Task 3: Regenerate the bundle outputs and verify the new skill is exported

**Files:**
- Modify generated outputs under `generated/skill-zips/`
- Modify any generated registry or bundle manifest files touched by the packaging tool

- [x] **Step 1: Regenerate skill artifacts**

Run the repo’s skill artifact generator so the new skill appears in the generated export corpus.

- [x] **Step 2: Inspect the regenerated outputs**

Confirm the new wrapper is present in the generated `superpowers` archive and that the projected copy stayed consistent with the canonical House Skills source.

- [x] **Step 3: Note any GPT overlay/export decision**

If the repo convention does not require a separate GPT overlay for this wrapper, record the omission explicitly in the implementation record.

### Task 4: Validate and record closeout evidence

**Files:**
- Create: `docs/superpowers/records/2026-06-16-mark-162-codex-receipts-superpowers-planning-receipt-composition.md`

- [x] **Step 1: Run marketplace validation**

Use the repo’s marketplace and generated-drift validation commands plus `git diff --check`.

- [x] **Step 2: Capture the implementation record**

Record the issue, branch, start SHA, head SHA, changed files, generated artifacts, validation commands, skipped checks, and any follow-up needed.

- [x] **Step 3: Confirm publication state**

Prepare the branch for PR publication and capture the resulting PR URL and head SHA in the implementation record.

## Self-review checklist

- The plan covers the narrow first-party projection only.
- The plan does not edit upstream `writing-plans` or `executing-plans` source.
- The plan names the durable receipt linkage requirement.
- The plan keeps the GPT overlay/export decision explicit instead of implicit.
- The plan points to concrete files and commands, not placeholders.
