# Retire Local Standard Deployment Copies

**Status:** ready

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove AOM's old deployed standard copies from this repository now that v2 subscription and repository-owned compliance are authoritative, while preserving the still-live Markdown formatter dependency for its separately planned migration.

**Architecture:** The v2 subscription points to immutable standard definitions in Marketplace history. `.agents/standards/` is no longer an implementation or compliance authority here. The active gate checks repository-owned records and implementation surfaces through `tools/check_agent_standards.py`. Retain only `.agents/standards/markdown-formatting/` until Plan 10 moves or retires the two live formatter consumers in `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`. Do not remove Marketplace source assets or historical v1 support during this local-copy retirement.

**Tech Stack:** Python 3, Git tracked-tree validation, existing `tools/run.py` command registry.

**Spec:** [Approved AOM design](../../specs/2026-09-30-aom-standard-adoption-and-shipping.md), especially sections 2, 3, 6, 7, and 8.

**Roadmap:** [Marketplace migration roadmap](2026-10-01-plan-7-marketplace-migration-roadmap.md), Plan 9. Baseline: Plan 8 closeout commit `a8bf8d4b6`.

**Execution Strategy:** `executing-plans` - establish the exact retained/deleted tree and prove the active checker/gate has no dependency on deleted copies before removing them.

## Global Constraints

- Do not change the primary checkout or other repositories.
- Preserve all eight v2 subscription IDs, exact pins, certification references, and repository-owned implementations.
- Preserve the active tracked hook, hosted workflow, `.agents/contracts/repo-standards-commands.json`, `tools/check_agent_standards.py`, and `tools/run.py` target order.
- Preserve the Markdown formatter copy only because its two current repository consumers still resolve that path. Plan 10 owns that dependency and subsequent formatter disposition.
- Do not change `dist/` or generated Marketplace/plugin artifacts by hand.
- Keep Marketplace source definitions and historical Git-pinned v1 authority readable; this plan retires local deployed copies only.
- Do not remove unrelated `.agents/contracts` files or collapse the certification into JSON.

## Review Focus

- Confirm the new subscription checker, full gate, and certification do not read `.agents/standards/` or `provenance.json`.
- Retain the formatter subtree until both discovered consumers are handled by Plan 10.
- Do not mistake historical test fixtures or old pinned-source documentation for live runtime dependencies.
- Do not silently delete generated outputs or repository-authored doctrine, contracts, or books.

## Retained and retired boundary

| Surface                                                                                | Plan 9 disposition | Reason                                                                                                                           |
| -------------------------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `.agents/standards/provenance.json`, `_runtime/`, and non-formatting standard subtrees | Delete             | The v2 subscription and active gate no longer consume copied resources or byte provenance.                                       |
| `.agents/standards/markdown-formatting/`                                               | Retain temporarily | `tools/new_plugin.py` and `tools/sync_skill_shared_references.py` still use the bundled formatter; Plan 10 owns their migration. |
| `skills/repo-shape/` historical source and v1 compatibility guidance                   | Retain             | The current Marketplace source can still serve an explicit historical pin; it is not a local deployed copy.                      |
| `.agents/contracts/operating-standards.json`, certification, and command binding       | Retain             | These are current repository-owned adoption and hook records.                                                                    |
| Marketplace `dist/` and other generated projections                                    | No change          | Not involved in deleting consumer-side deployed copies.                                                                          |

______________________________________________________________________

### Task 1: Demonstrate active compliance no longer depends on deployed copies

**Files:**

- Read: `tools/check_agent_standards.py`
- Read: `tools/run.py`
- Read: `.agents/contracts/operating-standards.json`
- Read: `.agents/contracts/standards-certification.md`
- Read: `.agents/standards/provenance.json` and all files under `.agents/standards/`
- Read: `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`
- Test: `tests/repository/test_agent_standards.py`

**Consumes:** Plan 8 v2 authority migration and exact live-reference inventory.

**Produces:** A verified keep/delete manifest for the local projection, preserving the formatter path and all authored v2 surfaces.

- [x] Confirm checker and active `repo-standards` target contain no reads of the deployment manifest, byte provenance, or deployed runtime.
- [x] Confirm the only direct runtime dependency in the local `.agents/standards/` tree is the Markdown formatter path used by `tools/new_plugin.py` and `tools/sync_skill_shared_references.py`.
- [x] Inspect the complete tracked tree under `.agents/standards/` and map each selected-standard copy to its current authoritative source or to the formatter exception.
- [x] Preserve historical compatibility tests/fixtures that model an old consumer; distinguish them from current repository runtime dependencies.

### Task 2: Remove obsolete local deployed resources

**Files:**

- Delete: `.agents/standards/provenance.json`
- Delete: `.agents/standards/_runtime/`
- Delete: all `.agents/standards/` subtrees except `markdown-formatting/`
- Keep unchanged: current v2 contracts, runbooks, playbooks, doctrine, certification, and generated Marketplace outputs

**Consumes:** Task 1 keep/delete manifest.

**Produces:** No local byte-vendored AOM standard implementations remain; only the explicitly temporary formatter copy remains.

- [x] Delete only the paths in the verified retirement boundary; keep `.agents/standards/markdown-formatting/` intact for Plan 10.
- [x] Check the v2 checker from a minimal consumer fixture that has no `.agents/standards/` tree; use existing behavioral cases if they already prove the claim rather than adding a tautological presence test.
- [x] Verify repository subscriptions, certification, the runbooks, and command declaration still point to owned live files.
- [x] Search current production routes for stale claims that the deployed runtime or provenance governs this checkout; leave explicitly historical fixtures and pin-specific source guidance intact.
- [ ] Run the focused checker suite, Markdown link validation, command-line validation, and the full Windows pre-commit hook on the atomic removal commit.

### Task 3: Review and close the local-copy retirement slice

**Files:**

- Modify: this plan, marking completed tasks
- Modify: `roadmap.md`, recording Plan 9's commit and the retained formatter dependency
- Review: complete change from Plan 8 closeout

**Consumes:** Tasks 1-2 and the complete Windows hook evidence.

**Produces:** A committed, reviewable repository without copied standard deployment machinery, with the Plan 10 dependency explicit.

- [ ] Inspect the full diff to verify only the identified local projection was removed.
- [ ] Verify no active AOM standard or compliance path still depends on removed copies.
- [ ] Obtain a fresh whole-slice review and resolve all material findings.
- [ ] Update the roadmap, commit the closeout, and identify the formatter subtree as Plan 10 carry-forward.
