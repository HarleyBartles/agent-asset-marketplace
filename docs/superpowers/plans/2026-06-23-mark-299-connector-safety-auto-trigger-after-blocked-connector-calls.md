# Connector Safety Auto-Trigger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `connector-safety` automatically obvious after blocked or rejected connector calls, and make Linear-facing skills route blocked Linear writes back into `connector-safety` recovery without extra prompting.

**Architecture:** Keep the canonical wording in `sources/first_party/skills/` and regenerate all projections and skill zips from that source. Treat generated marketplace files, manifests, and zips as derived outputs only. Keep the change narrow: improve blocked-call discoverability and recovery guidance, then refresh only the affected skill projections and validation surfaces.

**Tech Stack:** Markdown skill sources, YAML skill metadata, `py -3 tools/update_skill_artifacts.py`, `py -3 tools/generate_marketplace.py`, `py -3 tools/generate_repo_index.py`, `py -3 tools/materialize_projection.py`, `py -3 tools/validate_marketplace.py`, `py -3 tools/validate_repo_index.py`, `py -3 tools/validate_skill_zips.py`, `git diff --check`.

## Global Constraints

- First-party only: do not broaden this into a generic connector handbook.
- Preserve the discovery-before-mutation ladder already used by `connector-safety`.
- Do not imply a blocked call succeeded or that a memory-based retry is acceptable.
- Do not hand-edit generated zips, generated manifests, or registry files.
- Keep the Linear-facing edits limited to the smallest cross-references needed for blocked-write recovery.
- Use the current `main` branch baseline and keep the work to one branch and one PR.

---

### Task 1: Tighten the canonical `connector-safety` blocked-call contract

**Files:**
- Modify: `sources/first_party/skills/connector-safety/SKILL.md`

**Interfaces:**
- Consumes: the current description/frontmatter, the existing core rule, the discovery-before-mutation ladder, and the existing blocked-write recovery ladder.
- Produces: explicit blocked-call trigger wording, a top-level automatic-trigger section, a no-memory-paraphrase retry rule, a recovery shape that steps back to bounded parent discovery, and a concrete Linear blocked-write example.

- [ ] **Step 1: Expand the trigger wording in the skill metadata and opening prose**

Update the frontmatter `description` and the opening paragraphs so `connector-safety` clearly applies when a connector/tool call is blocked, rejected, safety-filtered, permission-rejected, schema-rejected, or validation-rejected.

- [ ] **Step 2: Add a top-level automatic-trigger section**

Insert a new section near the top of the skill body, immediately after the intro, with language that says blocked connector calls should route into `connector-safety` recovery automatically.

- [ ] **Step 3: Add the no-memory-retry rule**

State plainly that after a block, the agent must not retry by paraphrasing the failed payload or by rebuilding the request from memory.

- [ ] **Step 4: Strengthen the recovery shape**

Revise the blocked-write recovery ladder so it explicitly says:

1. acknowledge the mutation did not happen;
2. step back to bounded parent discovery;
3. read the exact target;
4. read connector-owned vocabulary if relevant;
5. retry once with one narrower safer mutation;
6. read back the target before claiming success.

- [ ] **Step 5: Add the Linear blocked-write example**

Add a concrete example that follows this shape: team/project discovery -> exact issue/project read -> label/status vocabulary if needed -> one narrow mutation -> readback.

- [ ] **Step 6: Re-check scope**

Verify the final wording still reads as a safety/recovery skill, not a general-purpose connector manual.

### Task 2: Add Linear-facing cross-references for blocked-write recovery

**Files:**
- Modify: `sources/first_party/skills/linear-superpowers/SKILL.md`
- Modify: `sources/first_party/skills/worker-dispatch-linear/SKILL.md`
- Modify: `sources/first_party/skills/worker-dispatch-linear/agents/openai.yaml`

**Interfaces:**
- Consumes: the current Linear shaping guidance, the current worker-dispatch control-plane wording, and the existing `connector-safety` reference.
- Produces: an explicit blocked-Linear-write route back into `connector-safety` in the visible Linear-facing skill text, plus the prompt-facing overlay for `worker-dispatch-linear`.

- [ ] **Step 1: Make blocked Linear writes route immediately to `connector-safety`**

Add or tighten the `linear-superpowers` wording so blocked Linear writes are treated as a direct trigger for `connector-safety` recovery, not as something to retry from the same surface.

- [ ] **Step 2: Mirror the cross-reference in `worker-dispatch-linear`**

Add matching language in `worker-dispatch-linear` so issue/comment/document shaping in Linear points to `connector-safety` when a write is blocked or rejected.

- [ ] **Step 3: Update the worker-dispatch prompt overlay**

Carry the same cross-reference into `sources/first_party/skills/worker-dispatch-linear/agents/openai.yaml` so the visible prompt guidance matches the skill body.

- [ ] **Step 4: Check for overreach**

Keep both Linear-facing skills focused on issue shaping and blocked-write recovery only; do not turn them into connector-safety manuals.

### Task 3: Regenerate derived artifacts and validate the refreshed surfaces

**Files:**
- Regenerate: `codex-marketplace/plugins/house-skills/skills/connector-safety/*`
- Regenerate: `codex-marketplace/plugins/adventures-pack/skills/connector-safety/*`
- Regenerate: `codex-marketplace/plugins/repo-worker-base/skills/connector-safety/*`
- Regenerate: `codex-marketplace/plugins/superpowers-plus/skills/linear-superpowers/*`
- Regenerate: `codex-marketplace/plugins/house-skills/skills/linear-superpowers/*`
- Regenerate: `codex-marketplace/plugins/house-skills/skills/worker-dispatch-linear/*`
- Regenerate: `codex-marketplace/plugins/adventures-pack/skills/worker-dispatch-linear/*`
- Regenerate: `generated/skill-zips/**`
- Regenerate: `codex-marketplace/manifest.json`
- Regenerate: `.agents/plugins/marketplace.json`
- Regenerate: `repo-index/repo-index.json`
- Regenerate: any affected projection/source-map/provenance files under the relevant plugin trees

**Interfaces:**
- Consumes: the edited first-party source files from Tasks 1 and 2.
- Produces: regenerated marketplace projections, skill zips, manifests, and index data that reflect the new trigger wording and cross-references.

- [ ] **Step 1: Refresh the affected skill artifacts with the targeted updater**

Run the targeted update commands for the affected installable skills, then confirm the generator writes the expected projected trees and zips rather than any manual edits.

Suggested commands:

```text
py -3 tools/update_skill_artifacts.py --skill house-skills/connector-safety
py -3 tools/update_skill_artifacts.py --skill adventures-pack/connector-safety
py -3 tools/update_skill_artifacts.py --skill repo-worker-base/connector-safety
py -3 tools/update_skill_artifacts.py --skill superpowers-plus/linear-superpowers
py -3 tools/update_skill_artifacts.py --skill house-skills/linear-superpowers
py -3 tools/update_skill_artifacts.py --skill house-skills/worker-dispatch-linear
py -3 tools/update_skill_artifacts.py --skill adventures-pack/worker-dispatch-linear
```

- [ ] **Step 2: Regenerate the repo-level derived surfaces**

Run the marketplace and repo-index generators so the manifest surfaces stay in sync with the updated projections.

Suggested commands:

```text
py -3 tools/generate_marketplace.py
py -3 tools/generate_repo_index.py
```

- [ ] **Step 3: Run the validation ladder**

Run the repo validations and the generated-artifact checks:

```text
py -3 tools/validate_marketplace.py
py -3 tools/validate_repo_index.py
py -3 tools/materialize_projection.py --check
py -3 tools/validate_skill_zips.py
git diff --check
```

- [ ] **Step 4: Inspect the diff for scope discipline**

Confirm the diff is limited to the intended source wording, the expected projections, and the derived metadata/zips. If the regeneration touches unrelated surfaces, stop and correct the source or the tool inputs before proceeding.

- [ ] **Step 5: Publish only after validation passes**

After the validation ladder passes, open the branch/PR with the actual regenerated outputs and report the publication proof separately from the plan.
