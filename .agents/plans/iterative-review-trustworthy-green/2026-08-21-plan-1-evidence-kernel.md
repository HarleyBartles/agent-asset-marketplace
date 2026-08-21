# Iterative Review Evidence Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a version-2 fail-closed review state kernel whose green predicate cannot pass without current, complete, machine-validated evidence, while preserving version-1 data only as non-authoritative history.

**Architecture:** Create a small `review_core` package with a JSON model, atomic store, evidence registry, and pure transition policy. Add a thin mixed-mode `reviewctl.py` CLI as the only version-2 mutation surface. Keep the existing scripts operational during this plan, but route version-2 state through the new kernel and add regression tests that prove every known version-1 false-green path is rejected.

**Tech Stack:** Python 3 standard library, `argparse`, `dataclasses`, `hashlib`, `json`, `os.replace`, `pathlib`, `tempfile`, `unittest`/`pytest`, JSON Schema documentation.

**Execution Strategy:** `executing-plans` - the tasks are intentionally sequential because the policy and CLI consume the model and store defined earlier. Do not parallelize edits to the shared kernel files.

## Global Constraints

- Edit only canonical first-party source under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate the installed skill tree through the marketplace tooling, including `.agents/skills/iterative-review/SKILL.md`.
- Do not make version-1 reports, JSONL logs, metrics, or resolved-ledger Markdown authoritative inputs to version 2.
- Initial construction writes one validated empty intake state. Every subsequent version-2 mutation must validate the complete state, bind evidence to the current snapshot epoch, append one history record, and write atomically. No epoch-zero record is valid.
- Unknown fields, invalid enum values, malformed evidence, stale epochs, stale snapshot fingerprints, and missing referenced files fail closed with exit code `1`; CLI usage errors use exit code `2`.
- `reviewed-green` is a transient derived decision for an exact presented SHA. Stored state may reach only `green-candidate`; no command may persist green.
- All severities, including `minor`, must have a closed disposition before green.
- `accepted-risk` is not a green disposition. It produces `reviewed-with-exceptions` and an exception report.
- The [Version-2 state contract](../../specs/2026-08-21-trustworthy-iterative-review-design.md#version-2-state-contract) is normative; do not invent alternate keys or looser record shapes.
- Do not regenerate marketplace surfaces or run canonical CI until the task's source and tests are staged as directed.
- The complete version-2 workflow remains behind the new `reviewctl.py` entrypoint until the cutover plan; this plan does not claim that the existing skill is trustworthy green.
- Tasks 1-5 intentionally leave a local in-progress tree while TDD moves from RED to GREEN. Do not commit or publish that intermediate state, do not run canonical CI on it, and do not bypass hooks. Task 6 regenerates the overlay, stages the complete intended tree, runs canonical CI, and creates the first implementation commit.

---

### Task 1: Characterize every false-green and dead-route defect with failing tests

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/review_v2_helpers.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py`

**Interfaces:**
- Produces: `make_v2_state(tmp_path, **overrides) -> dict`, `make_complete_candidate(tmp_path) -> dict`, `make_remote_observation(state) -> tuple[dict, datetime]`, `remove_predicate(state, remote_observation, name) -> None`, `write_v2_state(tmp_path, state) -> Path`, and the invariant test catalog consumed by Tasks 2-5.
- Consumes: current version-1 `next_node.py`, `compile_metrics.py`, and `resolved_ledger.py` behavior as the RED baseline.

- [ ] **Step 1: Add reusable version-2 test state builders**

Create `review_v2_helpers.py` with these public helpers and exact default shape:

```python
from __future__ import annotations

import copy
import json
from pathlib import Path


def make_v2_state(tmp_path: Path, **overrides: object) -> dict:
    state = {
        "schema_version": 2,
        "review_id": "review-test",
        "status": "active",
        "stage": "intake",
        "scratch_dir": str(tmp_path),
        "snapshot": None,
        "evidence": {},
        "authorities": {},
        "obligations": {},
        "dispatches": {},
        "reviews": {},
        "findings": {},
        "checks": {},
        "blockers": {},
        "green_seal": None,
        "history": [],
    }
    state.update(copy.deepcopy(overrides))
    return state


def write_v2_state(tmp_path: Path, state: dict) -> Path:
    path = tmp_path / "review-state.json"
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return path
```

`make_complete_candidate()` must materialize non-empty evidence files under `tmp_path`, compute their real sizes and SHA-256 values, and return the smallest state satisfying every design-spec record shape and stored candidate predicate: one loaded authority; fast-, focused-, and strong-eligible covered obligations including one high-risk cross-surface obligation; matching current dispatches plus clean fast/focused/strong/final/closure reviews; strict route-selection evidence; one fixed finding with resolution proof; successful required preflight and remote-CI checks; and matching reviewed/CI head SHAs. Final and closure dispatches use the trusted `reviewer-strong` profile at the `final-strong` capability/reasoning floor, with a baked route that is not compared with or overridden by the parent. `make_remote_observation()` returns the matching transient observation plus the fixed UTC `now` used by `evaluate_green()`. The observation contains the PR head, authority metadata digest, required-check set, conclusions, and observation timestamp. `remove_predicate()` must remove only the named record or proof field and must not repair any dependent record. Keep these helpers in the test tree; production code must not import them.

- [ ] **Step 2: Add RED tests for the proven version-1 defects**

Extend `test_next_node.py` with legacy-fixture tests that prove version-1 state cannot be promoted to a version-2 green seal for:

```text
test_v1_final_strong_without_report_cannot_produce_v2_green
test_v1_circular_resolution_state_cannot_produce_v2_green
test_v1_cumulative_preflight_state_cannot_produce_v2_green
test_v1_lost_normalization_origin_cannot_produce_v2_green
test_v1_blocked_state_cannot_produce_v2_green
test_v1_round_state_cannot_produce_v2_green
test_v1_unrepresentable_blocker_cannot_produce_v2_green
```

Each test must exercise a public CLI rather than private helper functions. Preserve the existing `test_lens_triage_resolution_skips_fix` expectation and make its minimal version-1 routing correction in Task 5 so the focused suite returns to green; do not spend this plan rehabilitating the legacy graph.

- [ ] **Step 3: Add version-2 green-predicate negative tests**

In `test_review_invariants_v2.py`, define one parameterized test that starts from a valid green-candidate fixture and removes exactly one predicate per case:

```python
@pytest.mark.parametrize(
    "missing",
    [
        "snapshot",
        "authority",
        "coverage",
        "preflight",
        "fast-review",
        "focused-review",
        "strong-review",
        "finding-resolution",
        "blind-final-review",
        "closure-audit",
        "remote-ci",
        "remote-head-identity",
        "presentation-recheck",
        "reasoning-floor",
    ],
)
def test_green_rejects_each_missing_predicate(tmp_path, missing):
    state = make_complete_candidate(tmp_path)
    observation, now = make_remote_observation(state)
    remove_predicate(state, observation, missing)
    decision = evaluate_green(state, observation, now=now)
    assert decision.allowed is False
    assert missing in decision.missing
```

Also add:

```text
test_green_rejects_stale_epoch_evidence
test_green_rejects_wrong_snapshot_fingerprint
test_green_rejects_unassessed_obligation
test_green_rejects_deferred_minor_finding
test_green_rejects_reviewer_uncertainty
test_green_rejects_malformed_report
test_green_rejects_ci_for_previous_head
test_green_rejects_remote_observation_older_than_60_seconds
test_green_rejects_remote_observation_more_than_5_seconds_in_future
test_green_rejects_accepted_risk_and_returns_reviewed_with_exceptions
test_green_rejects_fast_profile_used_for_strong_obligation
test_green_rejects_final_reviewer_below_final_strong
test_green_accepts_trusted_reviewer_strong_with_baked_route
test_green_accepts_opaque_harness_reviewer_strong_contract
test_green_does_not_require_parent_equality_for_trusted_profile
test_green_rejects_model_override_on_trusted_profile
test_green_rejects_unqualified_final_fallback
test_green_accepts_qualified_inherit_fallback
test_current_profile_qualification_is_reusable_for_matching_dispatches
test_profile_or_inventory_change_invalidates_qualification
test_any_snapshot_mutation_revokes_green_candidate
test_fix_rereview_may_narrow_but_requires_broader_reascent
test_scope_risk_consequence_matrix_derives_required_tier
test_repo_override_can_raise_but_not_lower_required_tier
```

The imports from `review_core` should fail during RED because Tasks 2-4 have not created them.

- [ ] **Step 4: Run RED and capture the expected failures**

Run:

```powershell
py -3 -m pytest -q codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py
```

Expected: version-2 imports and legacy-to-version-2 boundary assertions fail because `review_core` and `reviewctl.py` do not exist. The already-red lens-triage test remains a separately identified baseline failure. Record the exact failure summary in the task report.

- [ ] **Step 5: Preserve RED evidence without committing it**

Save the exact command, exit code, and failure names in the task's off-repo scratch report. Leave RED tests in the working tree and proceed directly to Task 2. Do not stage, commit, publish, or bypass hooks while the suite is intentionally red.

- [ ] **Step 6: Mark Task 1 complete in this plan**

Change every Task 1 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 2: Implement the version-2 state model and strict validator

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/__init__.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/model.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-v2.schema.json`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/review_v2_helpers.py`

**Interfaces:**
- Produces: `new_state(review_id: str, scratch_dir: Path) -> dict`, `validate_state(state: dict) -> None`, `validate_remote_observation(observation: dict) -> None`, `snapshot_fingerprint(snapshot: dict) -> str`, enums/constants, and `StateValidationError`.
- Consumes: the default state shape and negative cases from Task 1.

- [ ] **Step 1: Write focused model validation tests**

Add tests that assert `StateValidationError` for:

```text
unknown top-level field
schema_version other than 2
relative scratch_dir
unknown status, stage, severity, disposition, obligation status, review verdict, or check conclusion
unknown scope level, capability tier, or normalized reasoning floor
unknown dispatch route-selection mode
unknown dispatch context mode
unknown route qualification source
base/head/tree identifiers whose length does not match declared `git_object_format`
non-64-character SHA-256 values
mapping key different from the identifier inside its record
evidence record whose current file is missing, resized, or re-hashed
authority, obligation, dispatch, review, finding, check, or blocker referencing nonexistent evidence
review whose role, profile, assignment, snapshot, or observed model/context does not match its dispatch
dispatch below an obligation's capability or reasoning floor
blind-final or closure dispatch below final-strong capability/reasoning
blind-final or closure dispatch that has neither a qualified trusted profile/runtime-role map nor a qualified fallback
trusted-profile dispatch with a model or reasoning override
blind-final or closure dispatch whose context is not fresh
blind-final dispatch whose context includes prior review or finding evidence
finding resolution referencing a nonexistent finding, review, check, or human decision
obligation/dispatch/review/check epoch different from the current snapshot when used as current
finding resolution epoch earlier than discovery or inconsistent with its proof records
green_seal present before the green-candidate stage
persisted status green
accepted-risk finding while evaluating a green candidate
blocked status without an active blocker, or active status with an active blocker
reviewed-with-exceptions status without at least one proven accepted-risk finding or while another finding remains open
broken history sequence, previous hash, or record hash
remote observation with unknown fields, short head SHA, wrong authority digest, missing required check, or invalid timestamp
epoch-zero record of any kind
```

Add a round-trip test proving `new_state()` validates and serializes deterministically.

- [ ] **Step 2: Implement canonical enums and required keys**

In `model.py`, define these exact tuples:

```python
STATUSES = ("active", "blocked", "reviewed-with-exceptions")
STAGES = (
    "intake",
    "authority",
    "impact-mapping",
    "coverage",
    "coverage-challenge",
    "preflight",
    "fast-review",
    "focused-review",
    "strong-review",
    "resolution",
    "final-review",
    "closure-audit",
    "remote-ci",
    "green-candidate",
    "reviewed-with-exceptions",
    "blocked",
)
SEVERITIES = ("blocking", "important", "minor")
DISPOSITIONS = (
    "open",
    "fixed",
    "false-positive",
    "accepted-risk",
    "deferred",
    "contested",
    "unassessed",
)
OBLIGATION_STATUSES = ("pending", "covered", "not-applicable", "invalidated", "unassessed")
REVIEW_VERDICTS = ("clean", "findings", "incomplete", "blocked")
DISPATCH_STATUSES = ("pending", "reported", "incomplete", "invalidated")
ROUTE_SELECTION_MODES = ("trusted-profile", "runtime-role-map", "literal-inherit", "explicit-route")
ROUTE_QUALIFICATION_SOURCES = ("effective-profile", "runtime-adapter", "parent-inheritance", "explicit-route")
REQUIRED_TOOL_CLASSES = (
    "repo-read",
    "git-read",
    "github-read",
    "issue-read",
    "document-read",
    "command-exec",
    "browser-read",
    "domain-read",
)
CHECK_CONCLUSIONS = ("success", "failure", "cancelled", "skipped")
GIT_OBJECT_FORMATS = ("sha1", "sha256")
EVIDENCE_KINDS = (
    "snapshot",
    "authority",
    "impact-map",
    "scope-challenge",
    "route-selection",
    "check-output",
    "review-attestation",
    "finding-proof",
    "fix-proof",
    "human-decision",
    "remote-ci",
)
AUTHORITY_KINDS = ("repo-law", "pr-description", "issue", "document", "plan", "spec", "non-goal")
AUTHORITY_AVAILABILITY = ("loaded", "unavailable")
OBLIGATION_CATEGORIES = (
    "authority-scope",
    "behavioral-correctness",
    "test-adequacy",
    "security-privacy",
    "reliability-concurrency",
    "compatibility-migration",
    "performance-resources",
    "operability-configuration",
    "documentation-contract",
    "source-custody",
)
OBLIGATION_RISKS = ("high", "medium", "low")
SCOPE_LEVELS = ("hunk", "file", "surface", "cross-surface", "whole-pr")
CAPABILITY_TIERS = ("fast", "focused", "strong", "final-strong")
REASONING_FLOORS = ("low", "standard", "high", "final-strong")
CONTEXT_MODES = ("fresh", "forked")
REVIEW_ROLES = (
    "impact-mapper-semantic",
    "impact-mapper-contract",
    "scope-challenger",
    "obligation-reviewer",
    "finding-adjudicator",
    "fix-reviewer",
    "blind-final",
    "closure-auditor",
)
CHECK_KINDS = ("preflight", "targeted", "remote-ci")
BLOCKER_CLASSES = (
    "authority-missing",
    "coverage-gap",
    "incomplete-review",
    "malformed-evidence",
    "snapshot-drift",
    "tool-blocked",
    "contested",
    "state-invalid",
)
```

Use explicit allowlists for every mapping. Do not silently retain unknown keys.

Validate every `route-selection` evidence file as the strict design-spec object with exactly `schema_version`, `observed_at`, `inventory_evidence_sha256`, `budget_contract_sha256`, `required_capability_tier`, `profile`, `profile_sha256`, `selection_mode`, `selected_model`, `selected_reasoning`, `selected_context_mode`, nullable `parent_model`, nullable `parent_reasoning`, `qualification_source`, and `rationale`. The duplicated values must match their dispatch. `trusted-profile` requires the effective named profile, no model/reasoning override, and a readable profile hash or opaque harness adapter identity hash; its selected model/reasoning are observed values or the literal `profile-defined`, never override inputs. `runtime-role-map` requires a current adapter mapping hash. `literal-inherit` and `explicit-route` are legal fallbacks only when no profile mapping exists and the adapter qualifies them at the assignment floor. Final and closure require `fresh` context and `final-strong` qualification.

- [ ] **Step 3: Implement snapshot fingerprinting**

Use canonical JSON with sorted keys and compact separators:

```python
def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()
```

`snapshot_fingerprint()` hashes only `epoch`, `git_object_format`, `base_sha`, `head_sha`, `tree_sha`, `diff_sha256`, `pr_metadata_sha256`, and `authority_manifest_sha256`. Validation recomputes and compares `fingerprint`.

- [ ] **Step 4: Implement recursive state validation**

`validate_state()` must implement the exact top-level and record contracts in the source design and:

1. validate top-level keys and enums;
2. validate the snapshot or require `None` during intake;
3. validate authorities, obligations, dispatches, reviews, findings, checks, blockers, seal, and history by key allowlists;
4. ensure referenced evidence IDs exist;
5. ensure each review matches its dispatch, each dispatch meets its assignment's capability/reasoning floor, and each route-selection evidence file parses as the strict profile-or-route qualification schema;
6. require final/closure dispatches to use a qualified `final-strong` trusted profile, runtime role map, or fallback in that precedence order; reject overrides on trusted profiles, require fresh context, and exclude prior review/finding evidence from blind-final context;
7. ensure each evidence file still exists and matches its registered byte length and digest;
8. ensure current evidence matches the current epoch and fingerprint;
9. ensure `fixed` and `false-positive` findings contain their required proof fields;
10. ensure `accepted-risk` cannot satisfy a green candidate;
11. verify monotonic history sequence plus `previous_record_sha256` and `record_sha256` chain values;
12. require status/blocker and reviewed-with-exceptions/accepted-risk consistency;
13. allow `green_seal` only at `green-candidate` and reject any attempt to persist a green status.

Return `None` on success and raise `StateValidationError` with a stable path-prefixed message on failure, for example `findings.F-1.disposition: unknown value 'ignored'`.

- [ ] **Step 5: Document the same contract in JSON Schema**

Write `review-state-v2.schema.json` as Draft 7 with `additionalProperties: false` at every object level and enum values identical to `model.py`. The Python validator remains runtime authority; the schema is interoperability documentation and a test fixture. Add a standard-library test that walks the schema and asserts every documented object closes additional properties and every named enum equals its Python tuple, so the two representations cannot drift silently.

- [ ] **Step 6: Run model tests**

```powershell
py -3 -m pytest -q codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py
```

Expected: PASS.

- [ ] **Step 7: Checkpoint the model locally**

Inspect `git diff --check` and confirm only intended canonical source, tests, references, and plan tracking changed. Do not commit while later invariant tests remain RED.

- [ ] **Step 8: Mark Task 2 complete in this plan**

Change every Task 2 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 3: Add atomic state storage and content-addressed evidence

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/store.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_store_v2.py`

**Interfaces:**
- Consumes: `validate_state()`, `canonical_json()`, and `sha256_json()` from Task 2.
- Produces: `load_state(path: Path) -> dict`, `save_state(path: Path, state: dict) -> None`, `register_evidence(state: dict, path: Path, *, kind: str, epoch: int, snapshot_fingerprint: str, candidate_snapshot: dict | None = None) -> str`, `register_evidence_batch(state: dict, specs: dict[str, tuple[str, Path]], *, epoch: int, snapshot_fingerprint: str, candidate_snapshot: dict | None = None) -> dict[str, str]`, `resolve_evidence_aliases(data: object, aliases: dict[str, str]) -> object`, `verify_evidence_files(state: dict, evidence_ids: Iterable[str] | None = None) -> None`, and `append_history(state: dict, event: dict) -> None`.

- [ ] **Step 1: Write failing atomicity and evidence tests**

Add tests for:

```text
load rejects missing, malformed, BOM-drifted, and version-1 state with distinct errors
save validates before writing
save leaves the previous valid file intact when serialization or replace fails
save writes UTF-8 without BOM and a final newline
register_evidence rejects missing files, directories, empty files, stale epochs, and stale fingerprints
register_evidence stores an absolute path, byte length, kind, epoch, SHA-256, and snapshot fingerprint
register_evidence deduplicates identical content but rejects an evidence ID collision with different metadata
batch registration rejects duplicate aliases, unknown kinds, unresolved aliases, unused aliases, and non-evidence-field alias substitution
candidate-snapshot registration is accepted only for an empty intake state and a fingerprint-valid `freeze-review-input` candidate
verify_evidence_files detects disappearance or byte drift after registration
append_history assigns a monotonic sequence, chains record hashes, and never rewrites prior records
```

- [ ] **Step 2: Implement Windows-safe atomic writes**

Use `tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False)`; flush and `os.fsync()`, close the file, then call `os.replace(temp_path, path)`. Delete only the explicit temporary file on failure. Never delete or rewrite the parent directory.

- [ ] **Step 3: Implement content-addressed evidence registration**

Evidence IDs use `evidence:` followed by the file's lowercase 64-character SHA-256. Store records under the already-required `state["evidence"]` mapping. A representative record contains exactly:

```json
{
  "evidence_id": "evidence:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "kind": "review-attestation",
  "path": "C:/review/evidence/review-attestation.json",
  "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "bytes": 1234,
  "snapshot_epoch": 2,
  "snapshot_fingerprint": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
}
```

CLI data files refer to command-local evidence as `@alias` only in allowlisted `evidence_id`, `evidence_ids`, and `context_evidence_ids` fields. Repeated CLI arguments use `--evidence-file alias=kind=C:/absolute/path`. The in-memory transaction registers all bytes, resolves every alias to its content ID, rejects unused or unresolved aliases, validates the final state, and performs one atomic save. For `freeze-review-input`, `candidate_snapshot` permits registration against the proposed snapshot only while the persisted state is an empty intake state; the action atomically ingests both the snapshot and its hashed authority records, and no intermediate state is saved.

- [ ] **Step 4: Implement append-only history records**

Each accepted mutation appends:

```json
{
  "sequence": 7,
  "event": "finding-resolved",
  "snapshot_epoch": 2,
  "snapshot_fingerprint": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "data_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "previous_record_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "record_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
}
```

History is diagnostic. Current state remains decision authority.

- [ ] **Step 5: Run store and model tests**

```powershell
py -3 -m pytest -q codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_store_v2.py
```

Expected: PASS.

- [ ] **Step 6: Checkpoint the store locally**

Inspect `git diff --check` and confirm the store/model focused tests are green. Do not commit while policy and CLI invariant tests remain RED.

- [ ] **Step 7: Mark Task 3 complete in this plan**

Change every Task 3 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 4: Implement the pure fail-closed policy and green predicate

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/policy.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_policy_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py`

**Interfaces:**
- Consumes: validated state from Task 2 and evidence records from Task 3.
- Produces: `Decision`, `next_action(state: dict) -> Decision`, `register_dispatch(state: dict, action: str, dispatch: dict, evidence_ids: list[str]) -> dict`, `evaluate_green(state: dict, remote_observation: dict, *, now: datetime) -> Decision`, `complete_action(state: dict, action: str, evidence_ids: list[str], data: dict) -> dict`, `block_review(...) -> dict`, and `resume_review(...) -> dict`.

- [ ] **Step 1: Write the complete transition table as tests**

Parameterize `test_review_policy_v2.py` over this ordered action sequence:

```python
ACTION_ORDER = (
    "freeze-review-input",
    "map-impact-semantic",
    "map-impact-contract",
    "plan-coverage",
    "challenge-coverage",
    "run-preflight",
    "run-fast-review",
    "run-focused-review",
    "run-strong-review",
    "resolve-findings",
    "run-final-review",
    "run-closure-audit",
    "run-remote-ci",
    "seal-green",
)
```

Action payloads are allowlisted, never merged generically:

| Action | Exact accepted `data` keys |
|---|---|
| `freeze-review-input` | `snapshot`, `authorities` |
| `map-impact-semantic` | `attestation`, `findings` |
| `map-impact-contract` | `attestation`, `findings` |
| `plan-coverage` | `obligations` |
| `challenge-coverage` | `attestation`, `findings`, `revised_obligations` |
| `run-preflight` | `checks`, `findings` |
| `run-fast-review` | `attestations`, `findings` |
| `run-focused-review` | `attestations`, `findings` |
| `run-strong-review` | `attestations`, `findings` |
| `resolve-findings` | `resolved_findings`, `verification_checks`, `rereview_attestations` |
| `run-final-review` | `attestation`, `findings` |
| `run-closure-audit` | `attestation`, `findings` |
| `run-remote-ci` | `checks` |
| `seal-green` | no keys; policy derives every digest and the seal |

Reject missing or extra payload keys. The Task 5 engine copies state in memory, registers supplied evidence files on that copy, then `complete_action()` ingests payload records into their allowlisted mappings and validates the whole candidate for the current snapshot, role, action, dispatch, and evidence registry. Only one final atomic save may replace original state. Hash the canonical action plus payload and evidence IDs for idempotency; an identical replay is a no-op, while the same action key with different content is an error.

Before any subagent-backed action runs, `register_dispatch()` must persist its pending dispatch, strict route-selection evidence, and hashed context package. The route-selection record captures the live inventory, budget contract, required tier, effective profile/adapter identity, selected route representation, qualification source, and rationale. An unchanged current qualification may be reused across matching dispatches; a changed profile hash, adapter identity, inventory hash, budget hash, or required tier invalidates it. Completion is rejected if the pending dispatch did not predate the attestation, the action does not match, the report differs from the dispatch, the profile or route is below the assignment floor, a trusted profile was overridden, or a lower-precedence fallback was used while an effective qualifying profile existed. Deterministic actions (`freeze-review-input`, `plan-coverage`, `run-preflight`, `run-remote-ci`, and `seal-green`) do not require a reviewer dispatch.

For each action, test:

- it is the only returned next action when all prior predicates are complete;
- skipping it is rejected;
- evidence for another epoch is rejected;
- missing or malformed required evidence is rejected;
- completing it appends one history event and advances the derived stage;
- repeating the identical completion is idempotent;
- repeating it with different data is rejected.

Also test that a caller-forged stored `stage` cannot skip an action; `next_action()` derives the lawful stage from records and the engine overwrites the stored display value on every accepted mutation.

- [ ] **Step 2: Implement `Decision` and explicit missing predicates**

Use:

```python
@dataclass(frozen=True)
class ActionRecipe:
    action: str
    dispatch_required: bool
    required_role: str | None
    minimum_capability_tier: str | None
    minimum_reasoning_floor: str | None
    preferred_profile: str | None
    data_keys: tuple[str, ...]
    evidence_kinds: tuple[str, ...]
    record_command: str


@dataclass(frozen=True)
class Decision:
    allowed: bool
    action: str
    reason: str
    missing: tuple[str, ...] = ()
    recipe: ActionRecipe | None = None
```

`next_action()` must have no fallback route. If state is internally inconsistent, return `Decision(False, "blocked", "state validation failed", (...,))` or let `StateValidationError` reach the CLI. If status is blocked, the only lawful action is `resume-review` with blocker-resolution evidence.

For reviewer-backed actions, the recipe exposes the maximum capability and reasoning floor of the assignments currently eligible for that stage. Fast, focused, and strong actions are distinct ordered gates. A missing stage may be vacuously complete only when the coverage plan contains no current obligation eligible for that tier; it may not consume a lower-tier attestation as a substitute.

Before returning `seal-green`, the policy re-runs `verify_evidence_files()` for every evidence ID used by a green predicate. `seal-green` writes a candidate seal and advances to `green-candidate`. `evaluate_green(state, remote_observation, now=...)` rechecks those files plus transient remote head, authority, hosted-check identity, and the 60-second observation age and returns a decision without mutating state. Tests pass a fixed `now`; the CLI supplies the current UTC clock.

- [ ] **Step 3: Implement stage predicates**

Implement named pure predicates:

```text
has_current_snapshot
authorities_complete
impact_maps_complete
coverage_complete
scope_challenge_complete
preflight_current_and_green
fast_reviews_complete
focused_reviews_complete
strong_reviews_complete
all_findings_closed
blind_final_current_and_clean
closure_audit_current_and_clean
remote_ci_current_and_green
remote_identity_matches
presentation_observation_matches_candidate
```

Every predicate returns `(bool, tuple[str, ...])`. `evaluate_green()` concatenates missing reasons from all predicates instead of stopping at the first one.

`coverage_complete()` must require every affected surface to have every applicable universal category from the design contract, derive scope plus risk capability/reasoning floors, reject zero assignees, require two distinct assignees for high-risk obligations, and accept `not-applicable` only with current evidence. `impact_maps_complete()` requires both independent mapper roles. `scope_challenge_complete()` requires a current challenger attestation covering the union of both maps; findings from that challenge return to coverage planning. `fast_reviews_complete()`, `focused_reviews_complete()`, and `strong_reviews_complete()` each require every assignment scheduled at that exact policy tier to have an attestation at or above its floor; a stronger route may serve an assignment but does not permit skipping its ordered stage. A fast/focused attestation cannot satisfy a broader or higher-risk obligation. Whole-PR obligations are satisfied only by final and closure predicates backed by valid `final-strong` profile-or-route qualification evidence.

Implement the design-spec floor table as a pure function and test every scope/risk pair plus every strong consequence override. The result is the maximum applicable tier, with normalized reasoning `low`, `standard`, `high`, or `final-strong` respectively. Repository policy may raise the result but any attempted lowering is a validation error.

- [ ] **Step 4: Implement finding closure rules**

`all_findings_closed()` rejects every `open`, `deferred`, `contested`, `unassessed`, or `accepted-risk` finding regardless of severity. It validates disposition proof:

- `fixed`: fix SHA, verification evidence, and re-review evidence;
- `false-positive`: adjudication evidence;
- `accepted-risk`: durable human decision evidence, followed by `reviewed-with-exceptions`; it never satisfies the green predicate.

Regression relationships are ordinary findings with `regression_of`; resolving them closes them without deleting their history.

A fix may be verified initially by a focused fix reviewer. The resolution transition still invalidates every impacted obligation attestation at that tier or broader. `next_action()` must return the earliest newly incomplete tier and force the workflow to re-ascend fast, focused, strong, final, and closure gates as applicable; it cannot jump from a narrow fix review to final or preserve an invalidated broader attestation.

There is no round cap that permits green or discards work. A configured resource cap may return `blocked` with the remaining obligations/findings and required escalation evidence.

- [ ] **Step 5: Implement blocking and lawful resume**

`block_review()` records blocker class, reason, evidence IDs, epoch, and fingerprint. `resume_review()` requires a resolution evidence ID, closes the active blocker, restores `status: active`, and lets `next_action()` recompute from predicates. There is no hard-coded `blocked -> blocked` terminal transition.

- [ ] **Step 6: Run policy and invariant tests**

```powershell
py -3 -m pytest -q codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_policy_v2.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py
```

Expected: PASS, including every remove-one-predicate green test.

- [ ] **Step 7: Checkpoint the policy locally**

Inspect `git diff --check` and confirm policy/invariant tests are green. Do not commit while the public CLI and full focused suite remain incomplete.

- [ ] **Step 8: Mark Task 4 complete in this plan**

Change every Task 4 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 5: Add the single version-2 CLI and version-aware compatibility boundary

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/reviewctl.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/engine.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_reviewctl_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/next_node.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py`

**Interfaces:**
- Consumes: model, store, and policy APIs from Tasks 2-4.
- Produces transaction functions in `engine.py`: `init_review(...)`, `dispatch_transaction(...)`, `complete_transaction(...)`, `block_transaction(...)`, and `resume_transaction(...)`; each operates on an in-memory copy and calls `save_state()` exactly once after full validation.
- Produces: public CLI commands `init`, `status`, `next`, `dispatch`, `complete`, `block`, `resume`, `validate`, and `present`; an explicit legacy boundary that cannot treat version-1 state or metrics as version-2 evidence.

- [ ] **Step 1: Write CLI contract tests before implementation**

Test exact behavior:

```text
reviewctl.py --help exits 0 and labels version 2 experimental until cutover
reviewctl.py --check exits 0 without files
init defaults to check and requires --apply to create version-2 state
status, next, and present are read-only
dispatch, complete, block, and resume require --apply
usage errors exit 2
validation, stale evidence, and unlawful transitions exit 1
--json emits one JSON object and no prose
complete seal-green re-evaluates every candidate predicate and cannot accept a caller-supplied verdict
present accepts only a connector-produced remote-observation file, re-evaluates the candidate, emits the exact reviewed SHA, and never changes state
any failed dispatch/complete/block/resume transaction leaves review-state bytes unchanged
evidence aliases are resolved before record validation and never survive in persisted state
```

- [ ] **Step 2: Implement thin command handlers**

Every handler should parse paths/data, call one `review_core.engine` transaction or pure policy function, and render the result. Do not duplicate transaction order or policy in the CLI. Mutation commands accept `--data-file` and repeated `--evidence-file alias=kind=absolute-path`; they never accept shell-embedded JSON.

Normal next-action JSON is:

```json
{
  "allowed": true,
  "action": "plan-coverage",
  "reason": "current snapshot and authority manifest are complete",
  "missing": [],
  "recipe": {
    "dispatch_required": false,
    "required_role": null,
    "minimum_capability_tier": null,
    "minimum_reasoning_floor": null,
    "preferred_profile": null,
    "data_keys": ["obligations"],
    "evidence_kinds": ["impact-map"],
    "record_command": "py -3 scripts/reviewctl.py complete --action plan-coverage --state C:/review/review-state.json --data-file C:/review/plan-coverage.json --evidence-file impact=impact-map=C:/review/impact-map.json --apply"
  },
  "state": "C:/review/review-state.json"
}
```

For subagent-backed actions, `next` returns the dispatch command first. `dispatch` records the exact role, assignments, profile hash, model/context request, tool requirements, and context-package evidence before the agent is started. After a valid attestation exists, `next` returns the corresponding `complete` command. There is no completion path that creates its dispatch retroactively.

- [ ] **Step 3: Make legacy boundaries explicit**

Update `next_node.py` so it detects `schema_version`:

- version 2 exits `1` with `BLOCKED: version-2 state is controlled only by reviewctl.py` rather than becoming a second mutation or routing surface;
- absent/version 1 uses the existing router only for legacy review continuation;
- `ready` on version 1 prints `BLOCKED: version-1 review state cannot produce a trustworthy-green seal; start a version-2 review` and exits `1`;
- `--metrics` remains read-only diagnostics and cannot be combined with `--propose`.

Make only the minimal legacy route correction required by the existing `test_lens_triage_resolution_skips_fix` contract. Preserve all other version-1 defects as migration fixtures and document that the legacy graph is review assistance only.

- [ ] **Step 4: Prove there is only one version-2 authority**

Add cross-CLI tests proving `next_node.py`, `compile_metrics.py`, and `resolved_ledger.py` cannot mutate a version-2 state file or create a green seal. Version-2 metrics and Markdown rendering are deferred until cutover; Plan 1 does not add parallel report adapters.

- [ ] **Step 5: Run all focused tests**

```powershell
py -3 -m pytest -q codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests
```

Expected: PASS, including the previously failing `test_lens_triage_resolution_skips_fix` and every new false-green regression.

- [ ] **Step 6: Run all bundled-script CLI self-checks**

```powershell
$scripts = Get-ChildItem codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts -File -Filter '*.py'
foreach ($script in $scripts) { py -3 $script.FullName --help | Out-Null; if ($LASTEXITCODE -ne 0) { throw "$($script.Name) --help failed" }; py -3 $script.FullName --check | Out-Null; if ($LASTEXITCODE -ne 0) { throw "$($script.Name) --check failed" } }
```

Expected: every executable script exits `0` for both commands.

- [ ] **Step 7: Checkpoint the complete focused implementation locally**

Inspect `git diff --check`, confirm the complete focused suite and CLI self-checks are green, and proceed to Task 6 without committing. The generated installed copy is still stale until Task 6.

- [ ] **Step 8: Mark Task 5 complete in this plan**

Change every Task 5 checkbox to `[x]` in the working tree. Task 6 will stage it with regenerated surfaces and the full canonical CI gate.

---

### Task 6: Document the kernel boundary and publish Plan 1 safely

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/trustworthy-green-invariants.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-graph.md`
- Modify: `.agents/plans/iterative-review-trustworthy-green/2026-08-21-plan-1-evidence-kernel.md`
- Modify: `.agents/plans/iterative-review-trustworthy-green/roadmap.md`
- Regenerate: the installed iterative-review skill tree, including `.agents/skills/iterative-review/SKILL.md`, and marketplace/index surfaces

**Interfaces:**
- Consumes: the public `reviewctl.py` commands and green predicate from Tasks 2-5.
- Produces: agent-facing kernel guidance, generated installed copies, an implementation-review record, and publication evidence for the roadmap.

- [ ] **Step 1: Write the invariant reference**

`trustworthy-green-invariants.md` must define:

- the nine green predicates from the design spec;
- version-1 versus version-2 authority;
- current snapshot evidence rules;
- all-severity finding closure;
- blocked/resume semantics;
- derived-report non-authority;
- the statement that process completeness is enforceable while omniscience is not.

Keep implementation flags in `reviewctl.py --help`; do not duplicate the full CLI reference.

- [ ] **Step 2: Add an honest interim boundary to `SKILL.md`**

Do not cut users over to the incomplete version-2 workflow. Add a prominent interim boundary that says:

```text
The current version-1 workflow is review assistance, not proof of reviewed green.
Version-1 workspaces cannot produce a trustworthy-green seal.
The experimental version-2 kernel is not the user entrypoint until the trustworthy-green roadmap reaches cutover.
```

Remove claims that `next_node.py` alone makes invalid moves impossible. The under-500-word control-plane rewrite belongs to Plan 7 after every action adapter exists.

- [ ] **Step 3: Update the graph reference**

Label current node recipes `version 1 - legacy assistance`. Add the version-2 target graph and scope-to-reasoning ladder from the design spec. Mark snapshot, authority, impact maps, scope challenge, tiered reviewer attestations, trusted-profile-first final-strong final/closure, exact-SHA CI, and presentation recheck as required evidence gates. Do not delete version-1 recipes until the final cutover plan.

- [ ] **Step 4: Update implementation progress before regeneration**

Mark completed Plan 1 boxes `[x]`, but leave Task 6 publication boxes open. Do not mark the roadmap item done or invent publication identifiers before they exist. Do not mark Plans 2-7 ready.

- [ ] **Step 5: Check source and overlay health before regeneration**

```powershell
py -3 tools/run.py heal --check
```

Expected: PASS.

- [ ] **Step 6: Regenerate marketplace and mesh surfaces**

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py mesh --apply
```

Expected: installed skill and indexes update from canonical source without manual edits.

- [ ] **Step 7: Stage the full intended tree and run canonical CI**

```powershell
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review .agents/skills/iterative-review .agents/plans/iterative-review-trustworthy-green .agents/specs/2026-08-21-trustworthy-iterative-review-design.md .agents/INDEX.md .agents/plans/INDEX.md .agents/specs/INDEX.md .agents/specs/INDEX.json
py -3 tools/run.py ci --check
```

Expected: PASS on the staged tree. Do not bypass the pre-commit hook.

- [ ] **Step 8: Commit, push, and open a draft pull request**

```powershell
git commit -m "feat(iterative-review): add fail-closed evidence kernel"
git push -u origin codex/iterative-review-evidence-kernel
```

Then open the draft PR with this exact command:

```powershell
gh pr create --draft --base main --head codex/iterative-review-evidence-kernel --title "feat(iterative-review): add fail-closed evidence kernel" --body "Implements Plan 1 of the Trustworthy Iterative Review epic.`n`nAdds the version-2 evidence kernel and regression boundary. The version-2 workflow is not cut over; Plans 2-7 remain required before claiming trustworthy green.`n`nValidation: focused iterative-review tests and staged canonical CI."
```

- [ ] **Step 9: Record publication evidence and mark Task 6 complete**

Read the PR number and implementation commit SHA from GitHub/git. Keep roadmap Plan 1 at `executing`, record that implementation SHA and PR number, and record the plan-readiness rating. Mark every Task 6 checkbox, including this one, `[x]`; stage the plan and roadmap; run canonical CI; then commit and push the tracking update. Verify the final remote head SHA and keep the pull request draft.

Return the PR URL, branch, full final remote head SHA, implementation commit SHA, focused test result, staged CI result, and remaining roadmap gate. Report implementation as ready for review, not roadmap-done; move Plan 1 to `done` only after the PR lands and repository state proves it.

## Plan-readiness self-review

- Spec coverage: Plan 1 implements the state/evidence/policy foundation and regression suite required by roadmap item 1. Snapshot acquisition, impact/coverage discovery, reviewer schema execution, remote seal/presentation automation, and pressure benchmarking remain explicitly assigned to Plans 2-7.
- Dependency order: tests precede model; model precedes store; model/store precede policy; all precede CLI and documentation.
- Source custody: canonical source is edited first; installed skill and indexes are regenerated only in Task 6.
- Interim state: version-2 APIs exist behind `reviewctl.py`; the current skill is not cut over and cannot claim version-2 green during this plan.
- Validation: focused tests, CLI contracts, heal, marketplace regeneration, mesh regeneration, staged CI, and draft PR publication are explicit.
- Handoff-gates result: 9/10 plan-readiness. Dependencies are producer-before-consumer; every task has explicit inputs/outputs and tracking; the temporary RED interval is local and non-publishable; canonical source and generated overlay are staged together; focused checks, canonical CI, draft publication, and exact return evidence are named. The remaining implementation detail belongs to the bounded later roadmap plans rather than hidden Plan 1 improvisation.
