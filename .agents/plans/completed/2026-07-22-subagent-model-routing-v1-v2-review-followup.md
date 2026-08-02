# Subagent Model Routing V1/V2 Review Follow-up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the PR review findings by making the routing skill’s discovery metadata match its live Codex contract, making pressure-scenario references unambiguous, and recording the V1/V2 change in a current durable plan.

**Architecture:** Edit only the first-party skill source and its contract tests. The marketplace rebuild projects canonical source verbatim to plugin, installed-skill, and ZIP surfaces; no generated projection is hand-edited. The existing Devin runtime profile is explicitly out of scope.

**Tech Stack:** Markdown, YAML, Python `pytest`, and the marketplace rebuild/validation tools.

## Global Constraints

- Canonical source is `sources/first_party/skills/subagent-model-routing/`; generated surfaces are downstream only.
- Do not modify `references/devin-desktop-profile.md`.
- Discovery metadata may describe selectable model, reasoning, and context mode, but must not promise paid-route or context-tier selection.
- Pressure-scenario IDs must be globally unique and sequential so cross-profile references are unambiguous.
- Run `py -3 tools/rebuild_marketplace.py`, `py -3 tools/check_marketplace.py`, and the full Python test suite before publication.

## Validation Baseline

On 2026-07-22, `py -3 -m pytest tests/test_repo_worker_base_contract.py -q`
failed on unchanged `main` with the same six `work-mode-router` contract failures
observed while validating this PR. Treat those failures as an external baseline,
not as a routing-skill regression; all routing-skill contract tests must pass.

---

### Task 1: Lock the review findings into source-contract tests

**Files:**
- Modify: `tests/test_subagent_model_routing_contract.py`

- [x] Add a test that reads canonical `SKILL.md` and `agents/openai.yaml` and asserts neither contains `paid route` or `context tier`.
- [x] Add a test that parses numbered pressure scenarios and requires the exact sequence `1` through `32`.
- [x] Run `py -3 -m pytest tests/test_subagent_model_routing_contract.py -v` and confirm both new tests fail against the reviewed source.

### Task 2: Make the canonical routing skill truthful and unambiguous

**Files:**
- Modify: `sources/first_party/skills/subagent-model-routing/SKILL.md`
- Modify: `sources/first_party/skills/subagent-model-routing/agents/openai.yaml`
- Modify: `sources/first_party/skills/subagent-model-routing/references/pressure-scenarios.md`

- [x] Replace `context tier` with `context mode` and remove `paid route` from discovery description, metadata scope/use triggers, and Codex wrapper metadata.
- [x] Renumber the Devin scenarios from `20` through `32`, leaving their text and Devin profile unchanged.
- [x] Run `py -3 -m pytest tests/test_subagent_model_routing_contract.py -v` and confirm the added contract tests pass.

### Task 3: Regenerate, validate, and publish the review follow-up

**Files:**
- Create: `.agents/superpowers/plans/2026-07-22-subagent-model-routing-v1-v2-review-followup.md`
- Generated: `.agents/skills/subagent-model-routing/**`, `codex-marketplace/plugins/**/skills/subagent-model-routing/**`, and `generated/skill-zips/subagent-model-routing.zip`
- Generated: `.agents/superpowers/plans/INDEX.md`

- [x] Run `py -3 tools/rebuild_marketplace.py` to regenerate all derived skill and index surfaces.
- [x] Run `py -3 -m pytest` and `py -3 tools/check_marketplace.py`; inspect the diff for source-to-projection consistency and unintended files. The full suite has the six pre-existing `repo-worker-base` baseline failures documented above; the routing-skill contract suite passes 6/6.
- [x] Mark this plan complete only after the evidence above is green, commit the canonical source, tests, plan, and generated outputs, then push the existing PR branch.
- [x] Request a fresh-context review of the published PR head and address every actionable finding before asking to merge. The review found no actionable findings on `e7ad3cd80e666404f153044d24db4df5708c459c`.
