# Design: Pre-emptive Review Robustness

Date: 2026-08-04
Worktree: `Z:/_agent-worktrees/agent-asset-marketplace/feat/review-robustness`

## Problem

The recent `spec/using-playwright` PR needed multiple Devin auto-review and local `iterative-review` cycles before it was green. Several of the flagged issues were deterministic pattern classes (scaffolder behavior, `review_preflight` false positives, `tools/run.py` task semantics) that could have been caught before any subagent review was dispatched. The `iterative-review` loop is reactive: it re-discovers findings that already exist in Devin's known finding classes and in the repo's own `reviewer-known-findings.md`.

The result is wasted review rounds: the lens reviewers and `reviewer-strong` spend tokens reproducing what a fast local preflight could have said in seconds, and Devin auto-review then finds the same issues again because the local cycle did not close the gap.

## Goal

Reduce the number of Devin auto-review and `iterative-review` cycles by moving the deterministic, pattern-based finding classes into fast local preflights, tightening the lens profiles so they focus on what only an agent can judge, and documenting the new order of operations in a pre-submission runbook.

## Scope

1. **Fast-preflight tooling** — extend `tools/review_preflight.py` and `tools/run.py` to catch the pattern classes listed below before the diff reaches `iterative-review`.
2. **Lens re-jig** — split the mixed `reviewer-references` profile into a portable `reviewer-skills` lens and a repo-local `reviewer-marketplace` lens that absorbs the this-repo path/tooling checks.
3. **`reviewer-known-findings.md` overhaul** — tag each finding with the lens or preflight that owns it and whether it is portable to consumer repos.
4. **Pre-submission runbook** — create `.agents/runbooks/review-robustness.md` that defines the order: fast preflight first, then `iterative-review`, then flip to ready after CI passes.

## Non-goals

- Replace Devin auto-review or the `iterative-review` skill; this work augments and shortens the local loop.
- Add new MCPs, new skills, or new marketplace packs.
- Refactor `iterative-review` orchestration or the `subagent-workspace` scripts beyond procedure-level changes.
- Generalize the new preflights to consumer repos that do not install `repo-worker-pack`; any tool changes remain `agent-asset-marketplace` tooling.

## Design

### 1. Fast-preflight tooling

`tools/review_preflight.py` is the existing read-only scanner. It will gain checks for the bug classes that `reviewer-known-findings.md` already lists but that are currently only caught by subagents or Devin:

- **Snowflake / real-identifier context:** the existing 17–20 digit scanner already requires `guild|server|channel|user|tenant|discord` context. This spec validates the heuristic against a set of known-good and known-bad reference fixtures and documents the expected behavior.
- **`new_plugin.py` contract checks:**
  - (preflight, deterministic) `--sync` and `--apply` both honor `shared_checkout.approve_mutation` (exit-code check).
  - (lens-only, `reviewer-marketplace`) `--sync` preserves existing top-level bundle-manifest fields while still adding newly discovered skills.
  - (preflight, deterministic) The scaffolder does not write a literal `enabled: True` default that is immediately overwritten (default `enabled: True` enablement check).
  - (lens-only, `reviewer-marketplace`) No unused parameters in `new_plugin.py` helper functions.
- **`tools/run.py` task contract:**
  - `review-preflight` is an existing, read-only `tools/run.py` task already registered in `_TASKS`.
  - Read-only tasks do not advertise `--apply` fix hints.
  - `ci` includes `review-preflight` as a hard dependency so preflight findings block `ci --check`.
- **SKILL.md frontmatter `metadata` block:** guard against malformed `metadata` values (`metadata: `, `metadata: null`, `metadata: ~`, and `metadata: {}`) so the parser does not crash and the error message points at the file. A missing `metadata:` key is allowed; it is not flagged.
- **Canonical `py -3` invocation:** the preflight regex `r"(?:\bpython(?:3)? -m |\bpy -m )"` flags `python -m`, `python3 -m`, and `py -m` where `py -3 -m` is canonical.
- **Cross-skill script paths in `SKILL.md` and reference files:** verify that every backtick path starting with `subagent-workspace/scripts/` or `.agents/skills/` resolves to an existing installed or source skill file.

These checks run under the existing `tools/run.py review-preflight --check` task and, once `_TASKS["ci"].deps` is updated to include `"review-preflight"` (Task 2, Step 5), inside `tools/run.py ci --check`. They should fail fast with a concrete file/line message, not a subagent summary.

### 2. Lens re-jig

The current `reviewer-references` mixes portable skill-reference concerns with this-repo-local path/tooling drift. Re-shape the taxonomy:

- **`reviewer-skills`** (portable, derived from `reviewer-references`):
  - `SKILL.md` frontmatter schema and `metadata` block hygiene.
  - Markdown table row sanity.
  - Reference-file hygiene (no real IDs, no `python -m` examples where `py -3` is canonical, no secrets).
  - Prompt robustness (read-only prompts not asking subagents to mutate or recreate missing diffs).
  - In consumer repos this lens applies to skills installed from this marketplace and local skills; it also checks that the agent does not hand-edit installed skills (those are generated outputs).
- **`reviewer-marketplace`** (repo-local, already exists, expanded):
  - Scaffolder and generator behavior (`new_plugin.py`, `tools/run.py`, `plugin-roots.json`, bundle manifests, `repo-index.json`).
  - This-repo canonical path drift (`subagent-workspace/scripts/...` vs stale `subagent-driven-development/scripts/...`) and `repo-local-marketplace-policy.json` `install_defaults`.
  - `--check` vs `--apply` semantics and shared-checkout gating.
- **`reviewer-references`** is deprecated; its generated `.agents/agents/reviewer-references.md` copy and its source `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-references.md` are removed after `selecting-a-subagent` and `iterative-review` dispatch logic is updated. Its portable content moves to `reviewer-skills` (new source in `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-skills.md`) while its repo-local content moves to `reviewer-marketplace`. Update `selecting-a-subagent` and `iterative-review` dispatch logic to route `SKILL.md`/reference work to `reviewer-skills` and marketplace/tooling work to `reviewer-marketplace`.

`reviewer-known-findings.md` is updated to list each class with:

- finding title and severity
- the fast-preflight check, if any, that should catch it
- the owning lens (`reviewer-skills`, `reviewer-marketplace`, `reviewer-security`, `reviewer-strong`) that catches whatever the preflight cannot
- a note on whether the finding is portable to consumer repos

### 3. Pre-submission runbook

Create `.agents/runbooks/review-robustness.md` with the orchestrator-facing procedure:

1. Before any subagent review, run the consumer's fast preflight (`py -3 tools/run.py ci --check` for this repo).
2. If `review-preflight` reports findings, fix them and re-run preflight. Do not dispatch `iterative-review` while preflight is red.
3. Once preflight is green, run `iterative-review` with the updated lens profiles.
4. For each `iterative-review` finding, use `receiving-code-review` before applying; re-run preflight after each fix.
5. Only flip the PR to ready after a final green `ci --check` and a clean `reviewer-strong` pass.

This runbook is the process artifact that prevents short-circuiting the new fast checks.

## Validation

- `py -3 tools/run.py ci --check` passes after the preflight changes.
- `py -3 tools/run.py marketplace --apply` installs the updated lens profiles and runbook.
- A synthetic bad diff (e.g., `metadata: ` in a `SKILL.md`, stale `subagent-driven-development/scripts` path) is caught by `review-preflight` before `iterative-review` is invoked.

## Source and custody

- Tooling changes live in `tools/review_preflight.py` and `tools/run.py`.
- Portable lens profile sources live in `codex-marketplace/plugins/repo-worker-pack/assets/profiles/` (canonical product source per `.agents/AGENTS.md`); `.agents/agents/` is the installed/override surface. Create `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-skills.md` there; remove `codex-marketplace/plugins/repo-worker-pack/assets/profiles/reviewer-references.md` after dispatch is updated. Run `py -3 tools/run.py marketplace --apply` to install `reviewer-skills.md` into `.agents/agents/reviewer-skills.md`; `reviewer-marketplace.md` remains the tracked repo-local override in `.agents/agents/`.
- `reviewer-known-findings.md` source lives in `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-known-findings.md`; the installed copy is `.agents/skills/selecting-a-subagent/assets/reviewer-known-findings.md`.
- The new runbook lives in `.agents/runbooks/review-robustness.md`.
- Generated `.agents/agents/`, `.agents/skills/`, and index surfaces are downstream outputs; regenerate with `py -3 tools/run.py marketplace --apply`.

## Handoff confidence

8/10 — the design is bounded (tooling + profiles + runbook), the `iterative-review` skill is already in place, and the known finding classes are documented. The remaining uncertainty is exactly which new `review_preflight` checks are stable enough to run in `ci` without false positives; this will be resolved by fixture tests and one pilot PR.

## Trade-offs and deferred decisions

- **False-positive risk:** overly tight preflight checks can cost more time than they save. New checks must include at least one positive and negative fixture before being added to `ci`.
- **Consumer portability:** `reviewer-skills` is designed to be portable, but this work does not ship a generic consumer-grade profile yet; it only re-shapes this repo's lens files.
- **Review cycle reduction target:** the goal is fewer *rounds*, not zero findings; some contextual issues will still require `reviewer-strong`.
