# MARK-319 Workflow Skill Normalization and Project-Pack Deprecations Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize the generic repo agent workflow skills to the new human/agents/worker/GPT standard, deprecate thin project-pack verification and crew exposures where appropriate, and keep the surviving house-skills and repo guidance current without broadening beyond the durable MARK-319 contract.

**Architecture:** Keep the changes centered on the first-party skill sources, their projected marketplace surfaces, and the repo guidance that teaches future agents how to navigate them. Update `work-mode-router` and `linear-issue-shaping` without turning them into doctrine dumps, add or promote a generic `worker-verification` surface, fold or deprecate thin project-pack verification wrappers, and keep `crew` only where it belongs, such as `house-skills`. Regenerate the derived projections and validation surfaces from the source and manifest changes.

**Tech Stack:** Markdown skill source, marketplace bundle manifests, deterministic projection/zip regeneration, Python validation scripts, Linear route state, GitHub draft PRs.

## Global Constraints

- Keep this slice aligned with the full MARK-319 contract: `work-mode-router`, `linear-issue-shaping`, generic `worker-verification`, durable repo guidance, provider-neutral terminology, and the deprecation or folding of thin project-pack verification/crew exposures where appropriate.
- Keep `wild-bunch-worker-verification` in `house-skills`; remove it from project-pack plugin exposure unless the manifest or docs justify a narrow retained bridge.
- Deprecate `crew` from project-pack plugin exposure except where `house-skills` or another explicitly approved project-specific surface retains it.
- Do not turn `work-mode-router` or `linear-issue-shaping` into doctrine dumps; keep them as routers/control surfaces that point at the right workflow and evidence boundaries.
- Keep the wording cleanup sane and direct; do not invent a sprawling new taxonomy, but do include boring generic worker-verification doctrine where the issue asks for it.
- Add durable repo guidance that teaches future agents how to discover source custody, bundle manifests, validation rules, generated projections, and the update sequence before editing generated surfaces.
- Do not hand-edit generated skill trees, source maps, provenance maps, or zip artifacts.
- Preserve project-specific Wild Bunch setup/entropy falsification where it still matters, but move generic verification law into the generic worker-verification surface.

### Task 1: Update the workflow routers without expanding them into doctrine dumps

**Files:**
- Modify: `sources/first_party/skills/work-mode-router/SKILL.md`
- Modify: `sources/first_party/skills/linear-issue-shaping/SKILL.md`

**Interfaces:**
- Consumes: the current router and Linear shaping wording plus the route-state rules already in repo truth.
- Produces: a small router/control-plane refresh that teaches campaign-shaped defaults, durable route-state handling, and provider-neutral terminology without becoming a doctrine dump.

- [x] Update `work-mode-router` so it classifies the durable state from Linear/repo evidence and hands off the discovered mode without provider-branded route identity.
- [x] Update `linear-issue-shaping` so it teaches campaign-shaped worker issue shaping by default while preserving compact bodies, docs, route-state blocks, and plan/execution PR separation.
- [x] Keep both skills short, router-shaped, and evidence-first.

### Task 2: Promote generic worker verification and deprecate thin project-pack wrappers

**Files:**
- Modify: `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`
- Modify: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Modify: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Modify: `tools/validate_marketplace.py`

**Interfaces:**
- Consumes: the current Wild Bunch verification wording and project-pack dependency topology.
- Produces: a generic `worker-verification` surface, a deprecation or folding path for thin project-pack verification/crew wrappers, and a project-pack manifest/validator that no longer advertises the removed exposures.

- [x] Update the Wild Bunch verification source so generic verification law is either promoted into generic `worker-verification` wording or clearly separated from Wild Bunch-only falsification law.
- [x] Deprecate `crew` from project-pack exposure while retaining it where approved, such as `house-skills`, without changing `sources/first_party/skills/crew/SKILL.md` unless the issue discoverably needs terminology cleanup there.
- [x] Remove `wild-bunch-worker-verification` from the project-pack `source_of_truth` list if it is no longer a real project-pack dependency.
- [x] Remove any project-pack bridge entry that exists only to pull thin verification or crew wrappers into the project pack.
- [x] Update the hardcoded validation expectations so the project-pack shape matches the reduced inventory.
- [x] Keep the pack description honest about the remaining bridge/native skill set without overexplaining the deprecation.

### Task 3: Regenerate the retained house-skills and derived marketplace surfaces

**Files:**
- Regenerated: `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/house-skills/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/crew/**`
- Regenerated: `codex-marketplace/plugins/house-skills/skills/wild-bunch-worker-verification/**`
- Regenerated: `generated/skill-zips/house-skills/crew/**`
- Regenerated: `generated/skill-zips/house-skills/wild-bunch-worker-verification/**`
- Regenerated: `sources/first_party/skills/INDEX.md`
- Regenerated: `provenance/first-party-skills.md`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/references/source-map.md`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/references/provenance-map.json`
- Regenerated: `codex-marketplace/plugins/wild-bunch-project-pack/skills/**`
- Regenerated: `generated/skill-zips/wild-bunch-project-pack/**`
- Regenerated: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the updated source skills and the revised project-pack manifest.
- Produces: aligned house-skills and project-pack projections, plus the catalog and registry surfaces that describe where the skills now live.

- [x] Regenerate the house-skills projection so the retained copies match the cleaned-up source wording.
- [x] Regenerate the project-pack projection so the removed skill and crew exposures disappear from the project-pack tree and zip where appropriate.
- [x] Refresh the first-party catalog and generated registry so the retained skills show only their approved surfaces.
- [x] Confirm no other plugin projections picked up the removed exposures by accident.

### Task 4: Add durable repo guidance for manifest/projection discovery

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/custody-and-projection-doctrine.md`

**Interfaces:**
- Consumes: the learning from the workflow normalization pass and the existing custody/projection doctrine.
- Produces: durable repo guidance that tells future agents where to look before changing a generated plugin projection and what the update sequence is.

- [x] Add a concise note that generated plugin projections are downstream outputs, not the discovery starting point.
- [x] Spell out that projection changes begin with source custody or the source-of-truth manifest, then regenerate the derived surfaces.
- [x] Capture the exact surfaces future agents should inspect first: source skill, bundle manifest, validator, generated projection tree, generated zips, catalog/registry evidence, and the repo guidance that points at them.
- [x] Include the project-pack exposure rules and the crew retention rule so future agents know what belongs only in `house-skills`.
- [x] Keep the guidance short enough that future agents can actually use it as a shortcut.

### Task 5: Validate the normalization slice and write the Linear route update

**Files:**
- Validate: `sources/first_party/skills/wild-bunch-worker-verification/SKILL.md`
- Validate: `codex-marketplace/plugins/wild-bunch-project-pack/references/bundle-manifest.json`
- Validate: `tools/validate_marketplace.py`
- Validate: `generated/skill-zips/registry.json`

**Interfaces:**
- Consumes: the edited source skills, the reduced project-pack manifest, and the regenerated projection surfaces.
- Produces: proof that the retained skills are projected where approved and that the project-pack no longer advertises the removed exposures.

- [x] Search for stale terminology in the touched workflow, verification, and project-pack surfaces and classify any remaining hits as intentional compatibility, provider-specific wording, project-specific wording, or approved house-skills retention.
- [x] Run the marketplace validator and the relevant skill-artifact regeneration checks.
- [x] Update Linear route state with the plan path, plan PR, status, repair status, and the explicit split condition only for any work genuinely outside the MARK-319 contract.
- [x] Stop at the plan-only boundary until approval arrives.

## Validation

- `rg -n "wild-bunch-worker-verification|crew|Harley|user|worker ready|worker-send-ready|Codex|Linear/Codex|Devin campaign" sources/first_party/skills codex-marketplace/plugins/wild-bunch-project-pack tools docs`
- `py -3 tools/update_skill_artifacts.py --skill house-skills/wild-bunch-worker-verification`
- `py -3 tools/update_skill_artifacts.py --skill house-skills/crew`
- `py -3 tools/update_skill_artifacts.py --pack wild-bunch-project-pack`
- `py -3 tools/validate_marketplace.py`
- `git diff --check`

## Return Contract

When this plan is executed, return:

- the exact files changed;
- the wording changes made to `wild-bunch-worker-verification`;
- the exact project-pack membership removed or retained with reason;
- the validation output;
- the Linear route-state update;
- any remaining deprecation follow-up that was intentionally deferred.
