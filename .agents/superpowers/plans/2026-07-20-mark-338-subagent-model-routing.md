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

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/shared-policy.md` with this exact content:** (No additional editing is required; the Max clarification is already applied below.)

```markdown
Apply these rules in every environment:

* Resolve ambiguity through brainstorming, specification, or planning before escalating model capability.
* Choose by judgment, consequence, reversibility, verification burden, context need, modality, and task type—not task size alone.
* Prefer free or included models before metered models.
* Treat paid usage as an explicit escalation, not a silent fallback.
* Treat model, reasoning effort, and context allocation as separate decisions.
* Use the lowest reasoning effort that is reliably adequate.
* Max reasoning is forbidden for GPT-5.6 (Codex) routes; other runtimes define their own Max ceiling in their profile.
* Preserve reviewer independence where it adds value, but distinguish:
  * fresh-context independence;
  * model-family diversity;
  * deterministic verification.
* Do not call two agents “independent models” merely because they have separate contexts.
* Escalate once deliberately by model, reasoning, context, or review type; do not loop retries on the same route.
* Investigate broadly enough to understand cause, but mutate only the smallest surface required by the approved goal. Report adjacent findings instead of silently expanding scope.
* Do not manufacture a role for every available model. Inferior or redundant models may remain fallbacks only.
* Do not use a stronger model to compensate for an underdefined task.

Budget posture should support at least:

* `free_only`;
* `included_usage`;
* `metered_allowed`;
* `explicit_paid_override`.

Default to the environment’s free/included posture.
```

### Step 1.4: Write `references/codex-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/codex-profile.md` with this exact content:** (No editing is required.)

```markdown
### Normal parent posture

The intended persistent on-disk parent is GPT-5.6 Terra at High reasoning, configured outside this skill. The skill may describe that posture but must not claim authority to switch the parent.

### Approved routes

* `gpt-5.4-mini`
* `gpt-5.5`
* `gpt-5.6-luna`
* `gpt-5.6-terra`
* `gpt-5.6-sol`

Treat exact runtime slugs—including a slug shown under a Custom picker entry—as the model actually used.

### Routing

**GPT-5.4 mini**

* Medium: mechanical edits, exact repetitive transformations, routine cleanup, straightforward tests, low-judgment migrations.
* High: default bounded implementation after strong Superpowers/SDD planning.
* Prefer it over Luna for ordinary well-specified coding when context is sufficient.
* Do not use it as the sole high-consequence architecture, security, migration, or concurrency reviewer.

Fallback when unavailable:

* Luna for tightly bounded work or where large context is the main need;
* Terra when implementation judgment matters.

**GPT-5.6 Luna**

* Low: exact lookups and fast discovery.
* Medium: repository inventories, broad scans, source summaries, large-context read-heavy work.
* High only when 5.6 behaviour or its larger context materially helps a bounded task.
* Do not make Luna the routine implementation default while GPT-5.4 mini remains adequate.

**GPT-5.6 Terra**

* Medium: normal multi-file implementation, established integration work, ordinary engineering judgment.
* High: difficult debugging, cross-boundary reasoning, planning, synthesis, or meaningful local design decisions.

**GPT-5.6 Sol**

* High: architecture, domain modelling, security, concurrency, transactional correctness, difficult migrations, consequential review, or conflicting-findings adjudication.
* Extra High: exceptional architecture/security/migration/debugging or unresolved high-consequence disagreement.
* Extra High is the absolute ceiling. Max is forbidden.
* Do not spend Sol on routine navigation, scans, mechanical edits, or ordinary bounded implementation.

**GPT-5.5**

Use only for:

* deliberate regression comparison against previously trusted 5.5 behaviour;
* intentionally diverse second opinion;
* continuation of a workflow calibrated on 5.5;
* checking whether a 5.6 route introduced behavioural regression.

Use High. Fall back to Sol High when unavailable. Do not present 5.5 as a cheaper Sol substitute.

### Codex review gradient

* GPT-5.4 mini implementation: Terra High parent review for ordinary work; independent Terra High or Sol High for consequential work.
* Terra Medium implementation: Terra High or Sol High review as risk requires.
* Terra High implementation: Sol High review when independent stronger verification matters.
* Sol High work: fresh-context Sol High review; Sol Extra High only for exceptional consequence or unresolved disagreement.
```

### Step 1.5: Write `references/devin-desktop-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md` with this exact content:** (The SWE-1.7 reasoning ceiling clarification is already applied below.)

```markdown
Use a SWE-first policy for repository software work. Do not preserve GLM merely to give every model a lane.

### Runtime-observed model inventory

Initial profile data:

* SWE-1.7 — free/included, approximately 262K context, multimodal in the observed runtime, reasoning available through Max.
* GLM-5.2 — free/included at approximately 200K context, High reasoning available, text-only in the observed runtime; optional 1M context costs approximately $0.60 per million input tokens.
* SWE-1.6 — free/included fallback.
* SWE-1.6 Fast — metered at approximately $0.30 per million input tokens and $1.50 per million output tokens.

These are environment observations and may change. Current runtime inventory overrides stale profile values. Public provider evidence and local evaluation should be used when deliberately revising the profile.

### SWE-1.7 reasoning ceiling

Max reasoning is in scope for SWE-1.7 but is reserved for exceptional subagent tasks that need the additional reasoning budget. The normal plan and chat agent uses Medium reasoning. Do not use Max for routine navigation, scans, or ordinary bounded implementation.

### SWE-1.7 — default repo parent, planner, engineer, and technical reviewer

Use SWE-1.7 High for:

* persistent repo-backed parent/orchestration;
* live-source exploration;
* source-grounded planning and SDD decomposition;
* normal and difficult implementation;
* difficult debugging;
* integration;
* technical code review;
* multimodal, screenshot, frontend, and visual engineering work.

Use SWE-1.7 Medium for:

* mechanical edits;
* exact repetitive transformations;
* low-judgment bounded implementation.

Do not treat SWE-1.7 as a code typist. It may identify root causes, hidden requirements, plan drift, and edge cases. It must report material plan drift or omitted constraints rather than blindly execute or silently broaden scope.

Its thoroughness can create scope pressure. Require broad enough investigation to understand the problem but bounded mutation. Adjacent improvements become findings unless required for correctness.

For technical code review, prefer a fresh-context SWE-1.7 High reviewer. Describe this as fresh-context independence, not model-family diversity.

### GLM-5.2 — optional distinct textual/architecture challenger

Do not assign GLM a routine code-review lane when SWE-1.7 High is better suited to live-repository technical review.

Use GLM-5.2 High only when its distinct lens is materially useful for:

* product or architecture reasoning not dominated by live code manipulation;
* challenging issue, specification, plan, or architectural assumptions;
* higher-level intent and plan-conformance review;
* cross-document semantic consistency;
* large text-only synthesis;
* deliberately model-diverse review of reasoning that may be shared within the SWE model family.

For ordinary technical correctness questions—root cause, tests, regressions, repository conventions, edge cases, and diff scope—use SWE-1.7 High.

Model diversity alone is not sufficient reason to choose GLM. Choose the review question first.

### GLM paid 1M context

Treat 1M context as a paid context escalation, not a default model upgrade.

Require explicit paid authorization and evidence that:

* the task is text-only;
* 200K plus indexes, search, source maps, plans, targeted reads, and decomposition is insufficient;
* narrowing would materially lose important cross-source relationships;
* the agent records why the larger context is necessary.

Do not buy 1M context merely because the repository is large.

### SWE-1.6 and SWE-1.6 Fast

Do not create default lanes merely because these models are available.

Use SWE-1.6 as a fallback for:

* SWE-1.7 outage or unavailability;
* quota/rate-limit differences observed in practice;
* regression reproduction;
* a measured local case where SWE-1.6’s behaviour is preferable.

Use SWE-1.6 Fast only when latency, quota, outage, or evaluation evidence justifies paying for it. Do not choose it merely because it is inexpensive while SWE-1.7 is free and adequate.

The skill must allow later evaluation evidence to promote or retire these fallback roles without changing shared doctrine.

### Devin review policy

Normal change:

1. SWE-1.7 High performs or coordinates the repo work.
2. Fresh-context SWE-1.7 High performs technical review when warranted.
3. Deterministic validation proves the result.

Consequential architecture/security/concurrency/migration change:

1. SWE-1.7 High performs live-repository technical analysis and implementation.
2. Fresh-context SWE-1.7 High performs technical review.
3. GLM-5.2 High may perform a non-overlapping architecture/intent/assumption challenge.
4. Deterministic checks remain the proof surface.

GLM is additive only when a distinct review question exists. It does not replace the SWE technical reviewer.
```

### Step 1.6: Write `references/generic-free-first-profile.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/generic-free-first-profile.md` with this exact content:** (No editing is required.)

```markdown
For an unknown or non-Codex runtime, do not guess equivalence from model names. Inventory available models and classify them by capability:

```text
planner_orchestrator:
  best included/free model for the task’s reasoning and source access

engineer:
  best included/free software-engineering model

multimodal:
  best included/free model capable of the required visual evidence

technical_reviewer:
  strongest included/free live-source reviewer, preferably fresh context

architecture_intent_challenger:
  optional alternate model only when it offers a genuinely different competent lens

premium_backstop:
  disabled unless explicitly authorized
```

For each available model, capture:

* exact runtime label/slug;
* cost class;
* selectable reasoning levels;
* reasoning ceiling;
* context size;
* text or multimodal capability;
* preferred roles;
* prohibited roles;
* fallback route;
* whether selection can be enforced.

Prefer lowering reasoning on the strongest included model over selecting an older model solely because the task is easy, unless quotas, latency, or evaluation evidence favour the older model.
```

### Step 1.7: Write `references/pressure-scenarios.md`

- [ ] **Create `sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md` with this exact content:** (No editing is required.)

```markdown
### Shared failures

1. An underdefined task asks for a stronger model -> return to brainstorming/specification/planning.
2. An agent claims every available model needs a lane -> reject; allow fallback-only models.
3. A failed High attempt requests Max -> reject and diagnose/reroute.
4. A runtime cannot enforce selection -> provide a desired-route hint without claiming enforcement.
5. Two same-family agents are called model-independent -> correct the independence description.
6. A large repository triggers paid context automatically -> require retrieval/decomposition and explicit authorization.
7. A strong model investigates adjacent issues -> preserve bounded mutation and report findings.

### Codex

 8. Well-specified SDD implementation -> GPT-5.4 mini High.
 9. Mechanical exact change -> GPT-5.4 mini Medium.
10. Large read/inventory -> Luna Medium.
11. Cross-boundary debugging -> Terra High.
12. Security-sensitive migration or concurrency review -> Sol High; Extra High only with explicit exceptional justification.
13. 5.5 is proposed as cheaper Sol -> reject; allow only deliberate diversity/regression use.
14. GPT-5.4 mini unavailable -> Luna or Terra fallback according to context versus judgment need.

### Devin Desktop

15. New repo feature needs live exploration and planning -> SWE-1.7 High, not GLM by inherited “planner” label.
16. Product-level textual design discussion without substantial repo work -> GLM-5.2 High may be selected.
17. Approved mechanical implementation -> SWE-1.7 Medium.
18. Hidden root-cause bug -> SWE-1.7 High with broad investigation but bounded mutation.
19. Screenshot-dependent frontend fault -> SWE-1.7 High.
20. Technical code review -> fresh-context SWE-1.7 High.
21. SWE-authored plan needs architecture/intent challenge -> GLM-5.2 High with a non-overlapping prompt.
22. “SWE implemented it, therefore GLM must review” -> reject automatic pairing and classify review type first.
23. “The task is easy, therefore use SWE-1.6” -> prefer SWE-1.7 Medium unless quota/evaluation evidence says otherwise.
24. “SWE-1.6 Fast is cheap, therefore use it” -> reject while free SWE-1.7 is adequate; allow only latency/quota/outage/evaluation justification.
25. SWE-1.7 is unavailable -> use explicit SWE-1.6 fallback.
26. Large diff/repo triggers GLM 1M -> reject automatic paid context.
27. Provider benchmark conflicts with repeated local evaluation -> preserve documented default until an evaluation-backed profile update is made; do not drift ad hoc.
```

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

- SDD Confidence: **8/10**
- Reason: the exact frontmatter, openai.yaml, registry entry, rebuild/validate commands, and reference-doc source content are provided inline or via the repo-resident design spec. A competent implementer can transcribe the files without designing; the only residual judgement is applying the user Max-reasoning clarification, which is already captured in the spec.

## Spec Coverage Check

- Cross-runtime shared doctrine: Task 1.3.
- Codex profile: Task 1.4.
- Devin Desktop profile (with Medium/Max clarification): Task 1.5.
- Generic free-first fallback: Task 1.6.
- Pressure scenarios / anti-patterns: Task 1.7.
- Canonical source + projection flow: Tasks 1-3.
- Validation: Task 4.
