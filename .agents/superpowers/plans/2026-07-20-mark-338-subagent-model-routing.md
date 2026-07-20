# MARK-338: subagent-model-routing skill implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a first-party `subagent-model-routing` skill that chooses the cheapest adequate included model/reasoning/context route for child subagents across Codex, Devin Desktop, and unknown runtimes, then project it into `repo-worker-pack`.

**Architecture:** A compact `SKILL.md` detects the active runtime, loads one shared policy plus exactly one matching runtime profile, and returns a route hint. Detailed doctrine lives in `references/` and is projected verbatim into `repo-worker-pack` through the marketplace rebuild pipeline.

**Tech Stack:** Markdown skill docs, YAML frontmatter, Codex `agents/openai.yaml`, `codex-marketplace/custody-pack-registry.json`, `py -3 tools/rebuild_marketplace.py`.

## Global Constraints

- First-party source of truth: `sources/first_party/skills/subagent-model-routing/`.
- Active install target: `codex-marketplace/plugins/repo-worker-pack/skills/subagent-model-routing/`.
- Projection is `verbatim`; never hand-edit generated plugin copies.
- Skill body under 500 words excluding frontmatter; detailed guidance in `references/`.
- Codex (GPT-5.6) Max reasoning is forbidden; Devin Desktop SWE-1.7 may use Medium and Max with Max reserved for exceptional subagent tasks.
- Prefer free/included before metered; select by capability, not role label; report routes as hints when the runtime cannot enforce them.
- Any source/projection change requires `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py`.

---

## Task 1: Create first-party source skill

**Files:**
- Create: `sources/first_party/skills/subagent-model-routing/SKILL.md`
- Create: `sources/first_party/skills/subagent-model-routing/agents/openai.yaml`
- Create: `sources/first_party/skills/subagent-model-routing/references/shared-policy.md`
- Create: `sources/first_party/skills/subagent-model-routing/references/codex-profile.md`
- Create: `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`
- Create: `sources/first_party/skills/subagent-model-routing/references/generic-free-first-profile.md`
- Create: `sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md`

### Step 1.1: Write `SKILL.md` frontmatter and body

- [ ] **Create `sources/first_party/skills/subagent-model-routing/SKILL.md` with this exact content:**

```markdown
---
name: subagent-model-routing
description: Use when choosing a child subagent model, reasoning level, context tier, or paid route, or when retrying failed work by changing model/reasoning/context.
metadata:
  source-id: subagent-model-routing
  source-path: sources/first_party/skills/subagent-model-routing/SKILL.md
  provenance-name: Subagent Model Routing first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when choosing a child subagent model, reasoning level, context tier, or paid route, or when retrying failed work by changing model/reasoning/context.
  use_when:
  - Use before calling `spawn_agent` or an equivalent subagent tool.
  - Use when creating or selecting a named subagent configuration.
  - Use when recommending a child model, reasoning level, context tier, or paid route.
  - Use when retrying failed work by changing model/reasoning/context.
  - Use when selecting an implementation, code-review, architecture-review, or adjudication agent.
  do_not_use_when:
  - Do not use to switch the current parent session when the runtime cannot change models mid-session.
  - Do not use when another more specific skill owns the task.
  related_skills:
  - dispatching-parallel-agents
  - risk-gates
  - work-mode-router
  - repo-worker-base
license: MIT
---
# Subagent Model Routing

Use this skill before choosing a child subagent route. Detect the runtime, load the shared policy and exactly one matching environment profile, then return the cheapest adequate included or approved route.

## Runtime contract

1. Detect the active environment.
2. Inventory the models and controls actually available.
3. Load `references/shared-policy.md` and exactly one matching profile.
4. Treat current runtime inventory as authoritative over stale profile metadata.
5. Choose the cheapest adequate included route.
6. Record a concise rationale and fallback when material.
7. State explicitly when a desired route could not be enforced.

## Profiles

| Runtime | Profile |
|---|---|
| OpenAI Codex / ChatGPT | `references/codex-profile.md` |
| Devin Desktop | `references/devin-desktop-profile.md` |
| Unknown or non-Codex runtime | `references/generic-free-first-profile.md` |

## Common pressure

When the obvious choice is unclear or contested, read `references/pressure-scenarios.md` first.
```

- [ ] **Verify frontmatter** with `py -3 tools/normalize_first_party_skill_sources.py --check`.

### Step 1.2: Write `agents/openai.yaml`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/agents/openai.yaml` with this exact content:**

```yaml
interface:
  display_name: Subagent Model Routing
  short_description: Use when choosing a child subagent model, reasoning level, context tier, or paid route.
  default_prompt: Use /subagent-model-routing before choosing a child subagent model, reasoning level, context tier, or paid route. Detect the runtime, load the shared policy and exactly one matching profile, then return the cheapest adequate included route.
policy:
  allow_implicit_invocation: true
```

### Step 1.3: Write `references/shared-policy.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/shared-policy.md` by transcribing the `## Shared policy` section of MARK-338 and replacing the line "Max reasoning is forbidden globally" with "Max reasoning is forbidden for GPT-5.6 (Codex) routes; other runtimes define their own Max reasoning policy."**

### Step 1.4: Write `references/codex-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/codex-profile.md` by transcribing the `## Codex profile` section of MARK-338 verbatim.**

### Step 1.5: Write `references/devin-desktop-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md` by transcribing the `## Devin Desktop profile` section of MARK-338 and adding this constraint at the top of the profile body:**

```markdown
## Devin Desktop reasoning ceiling

SWE-1.7 exposes Medium and Max reasoning. Use Medium for the normal plan/chat agent. Reserve Max reasoning for exceptional subagent tasks that genuinely need the additional reasoning budget. Do not use Max for routine navigation, scans, or ordinary bounded implementation.
```

### Step 1.6: Write `references/generic-free-first-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/generic-free-first-profile.md` with the same structure as the Devin profile but scoped to unknown/non-Codex runtimes:**
  - Detect the runtime by looking for known markers (Codex `chatgpt`/`codex`, Devin `SWE-*`/`GLM-*`, etc.).
  - If the runtime cannot be identified, assume only free or included models are approved.
  - Disallow paid metered routes unless the user explicitly authorizes `metered_allowed` or `explicit_paid_override`.
  - Use Medium reasoning as the default; do not use Max unless the runtime exposes it and the task is exceptional.
  - Prefer the smallest adequate context; do not purchase context without evidence the task needs it.

### Step 1.7: Write `references/pressure-scenarios.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md` by collecting the anti-patterns and failure modes from the `## Problem` section of MARK-338 plus the escalation rules from `## Shared policy`.** Add concrete examples for:
  - retry loops that raise reasoning instead of diagnosing failure;
  - choosing a larger model because the task is underdefined;
  - confusing fresh-context review with model-diverse review;
  - spending premium models on mechanical edits.

- [ ] **Step 1.8: Commit source-only addition**

```bash
git add sources/first_party/skills/subagent-model-routing
git commit -m "feat: add subagent-model-routing first-party source (MARK-338)

Adds SKILL.md, openai.yaml wrapper, and reference docs for
shared policy, Codex profile, Devin Desktop profile,
generic free-first profile, and pressure scenarios."
```

## Task 2: Register the skill in `repo-worker-pack`

**Files:**
- Modify: `codex-marketplace/custody-pack-registry.json`

### Step 2.1: Add to `repo-worker-pack` source ledger and entries

- [ ] **Add `sources/first_party/skills/subagent-model-routing` to the `source_ledger` array of the `repo-worker-pack` pack.**
- [ ] **Add this entry to the `entries` array of the `repo-worker-pack` pack (keep alphabetical order by `canonical_name`):**

```json
{
  "canonical_name": "subagent-model-routing",
  "source_category": "first_party",
  "content_mode": "verbatim",
  "source_family": "first_party",
  "canonical_source_path": "sources/first_party/skills/subagent-model-routing",
  "local_path": "skills/subagent-model-routing",
  "provenance_note": "Projected verbatim from the first-party subagent-model-routing skill.",
  "copy_expectation": "byte_identical"
}
```

- [ ] **Step 2.2: Commit registry change**

```bash
git add codex-marketplace/custody-pack-registry.json
git commit -m "feat: register subagent-model-routing in repo-worker-pack (MARK-338)"
```

## Task 3: Regenerate marketplace projection

### Step 3.1: Run full rebuild

- [ ] **Run the canonical rebuild command:**

```bash
py -3 tools/rebuild_marketplace.py
```

Expected: projection trees, bundle manifests, source maps, provenance maps, skill zips, and marketplace manifests update without errors.

- [ ] **Step 3.2: Commit generated outputs**

```bash
git add codex-marketplace/ .agents/plugins/marketplace.json repo-index/
git commit -m "chore: regenerate marketplace projection for subagent-model-routing (MARK-338)"
```

## Task 4: Validate before publication

### Step 4.1: Run CI-gate validation

- [ ] **Run the non-mutating check command:**

```bash
py -3 tools/check_marketplace.py
```

Expected: exits 0 with no drift or missing generated surfaces.

- [ ] **Run first-party source normalization check:**

```bash
py -3 tools/normalize_first_party_skill_sources.py --check
```

Expected: "OK first-party skill sources: current"

## Task 5: Publish the implementation branch

### Step 5.1: Push branch and open PR

- [ ] **Push the current branch:**

```bash
git push -u origin mark-338-subagent-model-routing-plan
```

- [ ] **Open a PR into `main` with title** `feat: add subagent-model-routing skill to repo-worker-pack`.
- [ ] **PR body includes:**
  - Summary of new skill and runtime profiles.
  - Canonical source path and projection target.
  - Link to MARK-338.
  - Local validation results from `check_marketplace.py` and `normalize_first_party_skill_sources.py --check`.

## Task 6: Update Linear route state

- [ ] **After the PR is open, update MARK-338 with:**
  - `route_state: preflight_complete_pending_approval`
  - `plan_path: .agents/superpowers/plans/2026-07-20-mark-338-subagent-model-routing.md`
  - `pr_url: <PR URL>`
  - `head_sha: <full head SHA>`

## Execution Confidence Assessment

- SDD Confidence: **7/10**
- Reason: the mechanical files (frontmatter, openai.yaml, registry entry, rebuild commands) are exact and verified. The reference prose is sourced from MARK-338 and user clarifications, so a subagent implementer must transcribe rather than design; this is a controlled gap but not an ambiguity.

## Spec Coverage Check

- Cross-runtime shared doctrine: Task 1.3.
- Codex profile: Task 1.4.
- Devin Desktop profile (with Medium/Max clarification): Task 1.5.
- Generic free-first fallback: Task 1.6.
- Pressure scenarios / anti-patterns: Task 1.7.
- Canonical source + projection flow: Tasks 1-3.
- Validation: Task 4.
