# Wild Bunch Worker Verification Deprecation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deprecate `wild-bunch-worker-verification` from the Wild Bunch project pack, keep the house-skills projection current, and normalize the surviving skill wording to the new human/agents/worker/GPT standard without broadening the broader workflow-skill campaign.

**Architecture:** Treat `sources/first_party/skills/wild-bunch-worker-verification/` as the only source-of-truth edit point for the skill wording. Remove the project-pack bridge exposure from `codex-marketplace/plugins/wild-bunch-project-pack/` and update the marketplace validator so the remaining projection inventory is explicit and boring. Regenerate the projected house-skills copy and the derived catalog/zip surfaces so the remaining house-skills exposure stays aligned with source custody.

**Tech Stack:** Markdown skill source, marketplace bundle manifests, deterministic projection/zip regeneration, Python validation scripts, Linear route state, GitHub draft PRs.

## Global Constraints

- Keep this slice narrow: only `wild-bunch-worker-verification` and the Wild Bunch project-pack exposure for that skill are in scope.
- Leave `crew` alone; it is a later deprecation target and does not need an edit in this slice.
- Do not widen into `work-mode-router`, `linear-issue-shaping`, `repo-worker-base`, or `linear` unless the deprecation changes reveal a hard dependency.
- Keep the Wild Bunch skill in `house-skills`; remove it from the project-pack plugin and its generated export surfaces.
- Add durable repo guidance that teaches future agents how to discover source custody, bundle manifests, validation rules, and generated projections before editing a generated plugin surface.
- Do not hand-edit generated skill trees, source maps, provenance maps, or zip artifacts.
- Keep the wording cleanup sane and direct; do not invent a new generic worker-verification taxonomy for this slice.
- Preserve project-specific Wild Bunch setup/entropy falsification where it still matters.

### Task 1: Clean up the Wild Bunch verification source wording

**Files:**
- Modify: `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`

**Interfaces:**
- Consumes: the current Wild Bunch verification wording and its existing falsification rule.
- Produces: a cleaner skill body that keeps the Wild Bunch-specific verification value while using the new human/agents/worker/GPT wording consistently.

- [ ] Tighten the frontmatter description and body wording so it reads naturally with the new terminology standard.
- [ ] Keep the falsification rule for Wild Bunch setup/entropy/seeded behavior intact where it is still relevant.
- [ ] Avoid adding new generic control-plane doctrine or a new generic verification skill in this slice.

### Task 2: Remove the project-pack exposure and update the validator

**Files:**
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: the current Wild Bunch project-pack source-of-truth list and dependency-topology checks.
- Produces: a project-pack manifest and validator that no longer advertise `wild-bunch-worker-verification` as part of the project-pack inventory.

- [ ] Remove `wild-bunch-worker-verification` from the project-pack `source_of_truth` list.
- [ ] Remove the `repo-worker-pack` bridge entry that exists only to pull that skill into the project-pack.
- [ ] Update the hardcoded validation expectations so the project-pack shape matches the reduced inventory.
- [ ] Keep the pack description honest about the remaining bridge/native skill set without overexplaining the deprecation.

### Task 3: Regenerate the retained house-skills and derived marketplace surfaces

**Files:**
- Regenerated: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/wild-bunch-worker-verification/**`
- Regenerated: `generated/skill-zips/house-skills/wild-bunch-worker-verification/**`
- Regenerated: `sources/first_party/skills/INDEX.md`
- Regenerated: `provenance/first-party-skills.md`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`
- Regenerated: `generated/skill-zips/wild-bunch-project-pack/**`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the updated source skill and the revised project-pack manifest.
- Produces: aligned house-skills and project-pack projections, plus the catalog and registry surfaces that describe where the skill now lives.

- [ ] Regenerate the house-skills projection so the retained copy matches the cleaned-up source wording.
- [ ] Regenerate the project-pack projection so the removed skill disappears from the project-pack tree and zip.
- [ ] Refresh the first-party catalog and generated registry so `wild-bunch-worker-verification` shows only the retained house-skills projection.
- [ ] Confirm no other plugin projections picked up the skill by accident.

### Task 4: Add durable repo guidance for manifest/projection discovery

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/custody-and-projection-doctrine.md`

**Interfaces:**
- Consumes: the learning from the Wild Bunch projection removal and the existing custody/projection doctrine.
- Produces: durable repo guidance that tells future agents where to look before changing a generated plugin projection and what the update sequence is.

- [ ] Add a concise note that generated plugin projections are downstream outputs, not the discovery starting point.
- [ ] Spell out that projection changes begin with source custody or the source-of-truth manifest, then regenerate the derived surfaces.
- [ ] Capture the exact surfaces future agents should inspect first: source skill, bundle manifest, validator, generated projection tree, generated zips, and catalog/registry evidence.
- [ ] Keep the guidance short enough that future agents can actually use it as a shortcut.

### Task 5: Validate the deprecation slice and write the Linear route update

**Files:**
- Validate: `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`
- Validate: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Validate: `tools/validate_marketplace.py`
- Validate: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the edited source skill, the reduced project-pack manifest, and the regenerated projection surfaces.
- Produces: proof that the skill is only retained in house-skills and that the project-pack no longer advertises it.

- [ ] Search for stale terminology in the touched Wild Bunch verification surfaces and classify any remaining hits as intentional compatibility or project-specific wording.
- [ ] Run the marketplace validator and the relevant skill-artifact regeneration checks.
- [ ] Update Linear route state with the plan path, plan PR, status, discovered scope shift, and the explicit split condition that keeps the broader router/crew cleanup out of this slice.
- [ ] Stop at the plan-only boundary until approval arrives.

## Validation

- `rg -n "wild-bunch-worker-verification|Harley|user|worker ready|worker-send-ready|Codex|Linear/Codex|Devin campaign" sources/first_party/skills/wild-bunch-worker-verification codex-marketplace/plugins/wild-bunch-project-pack tools`
- `py -3 tools/update_skill_artifacts.py --skill house-skills/wild-bunch-worker-verification`
- `py -3 tools/update_skill_artifacts.py --pack wild-bunch-project-pack`
- `py -3 tools/validate_marketplace.py`
- `git diff --check`

## Return Contract

When this plan is executed, return:

- the exact files changed;
- the wording changes made to `wild-bunch-worker-verification`;
- the exact project-pack membership removed;
- the validation output;
- the Linear route-state update;
- any remaining deprecation follow-up that was intentionally deferred.
