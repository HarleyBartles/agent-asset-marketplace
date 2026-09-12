# Iterative Review Evidence Kernel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a version-2 fail-closed review state kernel whose green predicate cannot pass without current, complete, machine-validated witnessed evidence, while preserving version-1 data only as non-authoritative history. The kernel is Devin-only: outside a Devin Desktop session it reports unsupported and stays inert.

**Architecture:** Create a small `review_core` package with a strict JSON model, review-owned immutable content store plus epoch-bound evidence bindings, a witness-verifier protocol over the hash-chained hook transcript and `gh` remote state, exclusive locked compare-and-swap transactions, and pure fail-closed policy. Add a thin mixed-mode `reviewctl.py` CLI as the only version-2 mutation surface. Keep existing scripts operational during this plan, but route version-2 state through the new kernel and add regression tests proving known version-1 false-green paths plus caller-fabricated provenance are rejected.

**Tech Stack:** Python 3 standard library, `argparse`, `ctypes` for Windows handle checks, POSIX `dir_fd`/`O_NOFOLLOW`/`fstat` primitives, `dataclasses`, `hashlib`, `json`, `os.replace`, `pathlib`, `tempfile`, `unittest`/`pytest`, JSON Schema documentation.

**Spec:** [Trustworthy Iterative Review - Calibrated-Green Design (v2)](../../specs/2026-09-12-iterative-review-calibrated-green-design.md) - the plan argues from this spec; executors read both. The earlier [2026-08-21 design](../../specs/2026-08-21-trustworthy-iterative-review-design.md) is superseded historical context.

**Execution Strategy:** `executing-plans` - the tasks are intentionally sequential because the policy and CLI consume the model and store defined earlier. Do not parallelize edits to the shared kernel files.

## Global Constraints

- Edit only canonical first-party source under `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/`; regenerate the installed skill tree through the marketplace tooling, including `.agents/skills/iterative-review/SKILL.md`.
- The version-2 workflow is Devin-Desktop-only. Runtime detection checks for Devin surfaces (hook configuration, subagent profile loading); on any other harness every `reviewctl` mutation reports `unsupported-runtime` and exits without creating or mutating state.
- The review store (state, `evidence-store/`, `witness-store/`) lives under the canonical off-repo scratch root resolved by `subagent-workspace` (`<scratch-root>/<repo>/<branch>/reviews/<review-id>/`); raw hook transcripts land per-session under `<scratch-root>/<repo>/<branch>/transcripts/<session_id>.jsonl`. Both are disposable: `seal-green` binds the witness chain head into a seal record committed inside the reviewed head, so deleting scratch afterward narrows audit but cannot invalidate the seal.
- Do not make version-1 reports, JSONL logs, metrics, or resolved-ledger Markdown authoritative inputs to version 2.
- Initial construction writes one validated empty intake state at generation 0. Every subsequent version-2 mutation must hold an exclusive state lock from load through evidence ingestion and save, validate the complete state, bind evidence to the current snapshot epoch, append one history record, increment generation once, compare the exact prior generation and byte digest, and replace atomically. No epoch-zero record is valid.
- Unknown fields, invalid enum values, malformed evidence, stale epochs, stale snapshot fingerprints, and missing referenced files fail closed with exit code `1`; CLI usage errors use exit code `2`.
- `reviewed-green` is a transient derived decision for an exact presented SHA. Stored state may reach only `green-candidate`; no command may persist green.
- All severities, including `minor`, must have a closed disposition before green.
- `accepted-risk` is not a green disposition. It produces `reviewed-with-exceptions` and an exception report.
- The [v2 spec's Version-2 state contract](../../specs/2026-09-12-iterative-review-calibrated-green-design.md#version-2-state-contract) is normative (it carries the prior contract forward with witness substitutions); do not invent alternate keys or looser record shapes.
- Complete the task's canonical source and tests before regenerating marketplace surfaces. Regeneration must precede staging, and the complete canonical and generated tree is staged together before the commit whose pre-commit hook runs the canonical gate.
- The complete version-2 workflow remains behind the new `reviewctl.py` entrypoint until the cutover plan; this plan does not claim that the existing skill is trustworthy green.
- Preserve the legacy skill's explicit-human-opt-in, non-frontier-only entry gate until Plan 7 replaces it. Plan 1 must not re-enable implicit invocation, route `gpt-5.6-sol` or another harness-designated frontier orchestrator through version 1, or reinterpret version-1 `ready` as green.
- Local records and hashes prove consistency, not that work ran. Plan 1 defines a sealed witness-source policy/verifier interface over two sources - the hash-chained Devin hook transcript and `gh`-fetched GitHub state - and blocks witness-dependent transitions when a required witness cannot be verified; Plans 2, 4, and 6 wire live dispatch, command, and remote witness acquisition before a real PR can seal or present green. The verifier implementation is selected by the composition root, never by locator values in state or CLI input.
- Task 0 is a hard go/no-go capability check against this Devin harness, implemented as the `reviewctl doctor` contract. Do not write the kernel until the harness proves: hook-emitted Pre/PostToolUse transcripts covering orchestrator and subagent calls with `tool_use_id`/`agent_id`/`session_id`, `allowed-tools` list stripping, a denied-path refusal, `gh` remote custody, and witness-store creation. A failed check makes the skill inert for that session; it never relaxes the invariant and never produces a partial green.
- Plan 1 implements strict record validation and the full pure lifecycle/predicate semantics over synthetic witness records so later plans cannot invent weaker transitions. Plans 2-6 still own live acquisition, impact/coverage generation, reviewer/command execution, finding workflow integration, and presentation; the Plan 1 CLI must return a typed missing-witness-source block for those live actions.
- Plan 1 does not expose `reviewctl present`, accept caller-supplied remote observations through the CLI, or emit a reviewed-SHA proof. The pure presentation predicate exists only for fixture-driven kernel tests until Plan 6 adds the witnessed `gh` fetch path.
- The spec actions `record-remote-observation`, `record-frontier-run`, and `record-human-decision` enter state only through composition-root witness acquisition; Plan 1 validates their synthetic witness/record shapes but the CLI returns `missing-witness-source` for live calls. The plan's `seal-green` action is the spec's `seal-green-candidate` verb; the spec's `resume` is `resume-review` here.
- Tasks 1-5 intentionally leave a local in-progress tree while TDD moves from RED to GREEN. Do not commit or publish that intermediate state, do not run canonical CI on it, and do not bypass hooks. Task 6 regenerates the overlay, stages the complete intended tree, and creates the first implementation commit; the tracked pre-commit hook is the single complete local gate (it materializes the staged snapshot, runs `ci --apply`, stages the owned generated surfaces, and runs `ci --check --diagnostics`). Never run `py -3 tools/run.py ci --check` immediately before a normal commit or immediately after a successful hooked commit.
- All Plan 1 publication work happens on branch `codex/iterative-review-evidence-kernel`, created through `using-git-worktrees` isolation before Task 0 publishes. Task 0 opens the single draft PR; Task 6 reuses it.
- Before Task 0, use `subagent-workspace` to resolve an absolute off-repo scratch directory into `$irReviewScratch` (Task 0 already writes probe artifacts under `$irReviewScratch/capability-floor/`). Every task-boundary step must create a recoverable checkpoint, not merely call `git diff --check`: write the task's JUnit XML there; use `git diff --binary --output="$irReviewScratch/<task>-tracked.patch"`; `Compress-Archive -Force` the entire canonical iterative-review skill directory plus this plan into `$irReviewScratch/<task>-working-tree.zip` so untracked files are preserved; write `git status --porcelain=v2` to `<task>-status.txt`; and write SHA-256 hashes for the patch/zip/XML. Never place these recovery artifacts in the repository.

For each boundary, set `$irCheckpointName` to `task-1` through `task-5` and run this exact recipe after the task's JUnit-producing command:

```powershell
$irCheckpointPaths = @(
  'codex-marketplace/plugins/superpowers-plus/skills/iterative-review',
  '.agents/plans/iterative-review-trustworthy-green/2026-08-21-plan-1-evidence-kernel.md'
)
git diff --binary --output="$irReviewScratch/$irCheckpointName-tracked.patch"
Compress-Archive -Path $irCheckpointPaths -DestinationPath "$irReviewScratch/$irCheckpointName-working-tree.zip" -Force
git status --porcelain=v2 | Set-Content -Encoding utf8 "$irReviewScratch/$irCheckpointName-status.txt"
Get-FileHash -Algorithm SHA256 "$irReviewScratch/$irCheckpointName-tracked.patch", "$irReviewScratch/$irCheckpointName-working-tree.zip", "$irReviewScratch/$irCheckpointName-tests.xml" |
  ConvertTo-Json | Set-Content -Encoding utf8 "$irReviewScratch/$irCheckpointName-hashes.json"
```

For Task 1, rename `task-1-red.xml` to `task-1-tests.xml` after preserving the original exit code in the scratch report, so the recipe remains uniform.

---

### Task 0: Prove the Devin witness-capability floor

**Files:**
- Create after the probe, whether its decision is `PASS` or `INERT`: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/harness-capability-floor.md`
- Write raw probe artifacts only under `$irReviewScratch/capability-floor/`

**Interfaces:**
- Consumes the live Devin harness: its hooks pipeline, subagent profile loader, permission rules, `ask_user_question`, and `gh` connectivity.
- Produces an evidence-backed capability matrix before any `review_core` implementation exists; the matrix becomes the `reviewctl doctor` contract.

- [ ] **Step 1: Exercise every required live witness surface**

Using harmless disposable subjects outside the reviewed branch, prove on this Devin Desktop install that:

- the hooks pack emits a `PreToolUse` and `PostToolUse` record for an orchestrator tool call, each carrying verbatim `tool_input`, `tool_use_id`, `session_id`, `prompt_id`, and (for post) `tool_response`;
- the same record pair is emitted for a `run_subagent` call, and the child's own tool calls appear with `agent_id` correlating them to the dispatch;
- those child records are ingestible from the transcript: prove whether they share the parent `session_id` or must be located via `agent_id`/`prompt_id`, and record the correlation field the witness-store ingestion will use;
- a confined subagent profile's `allowed-tools` list strips every unlisted tool - dispatch a spike profile and capture the available-tool report verbatim;
- a `read`/`exec` deny rule on a canary path is refused and logged (record honestly that the refusal is run-fatal for that subagent run);
- `read_subagent` re-fetches a stored completion record after the dispatch ends;
- `ask_user_question` is withheld from subagent profiles but works for the orchestrator, with question and answer present in the transcript;
- `gh` is authenticated and can fetch a check-run and workflow-run record with `id`, `head_sha`, `conclusion`, `app_slug`, and run-attempt identity for a real pushed commit;
- the witness store creates with private permissions and accepts an append, and a `sha256` chain over two appended entries verifies and detects a tampered middle entry.

For each surface also record what it does **not** provide: no issuer outside the reviewed head for local records, no OS-level sandbox on Windows, no realized-model attestation, no caller-identity field in hook payloads. These are documented limitations, not failures.

- [ ] **Step 2: Record the capability matrix and decision**

`harness-capability-floor.md` records the harness/runtime identity, every probed surface, the verbatim evidence hash of each probe artifact, the confirmed witness classes (`witnessed-local` transcript, `externally-hosted` GitHub), the confirmed-absent guarantees, and one explicit decision:

- `PASS`: every floor item above is proven and the `reviewctl doctor` contract can name them all; or
- `INERT`: name every missing floor item. The skill's runtime detection treats this harness as unsupported: it reports the gaps and performs no review actions. This is a designed terminal output, not a fake-pass path.

- [ ] **Step 3: Verify the floor is outside candidate control**

Attempt self-qualification from a policy/profile definition in the reviewed head and require rejection. Re-read one earlier transcript segment and verify its chain digests recompute. Store the matrix and probe-artifact hashes in `$irReviewScratch/capability-floor/`; do not store secrets or provider credentials in the repository.

- [ ] **Step 4: Publish the floor decision and generated projection before kernel work**

Run `py -3 tools/run.py marketplace --apply` and `py -3 tools/run.py mesh --apply`, then stage the canonical capability reference together with every generated installed-skill/index projection those commands changed. Run `git diff --cached --check`, then commit on `codex/iterative-review-evidence-kernel`; the tracked pre-commit hook materializes the staged snapshot, runs `ci --apply`, stages the owned generated surfaces, and runs `ci --check --diagnostics` as the single complete local gate. Do not run `py -3 tools/run.py ci --check` before this commit. Push the branch and open its single draft PR (or update/reuse it if one already exists). Proceed to Task 1 only from that published `PASS` commit and record the draft PR URL/number for Task 6. An `INERT` decision is a publishable terminal output: publish its honest capability report through the same canonical/generated workflow and do not start kernel work until the harness floor changes.

---

### Task 1: Characterize every false-green and dead-route defect with failing tests

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/review_v2_helpers.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py`

**Interfaces:**
- Produces now: `make_empty_v2_state(tmp_path, **overrides) -> dict`, `write_v2_state(tmp_path, state) -> Path`, minimal malformed-state fixtures, and the invariant test catalog consumed by Tasks 2-5.
- Declares but does not hand-build: `make_complete_candidate`, `make_remote_observation`, `make_policy_bundle`, and `remove_predicate`; Task 4 implements them by composing the canonical constructors delivered by Tasks 2-3.
- Consumes: current version-1 `next_node.py`, `compile_metrics.py`, and `resolved_ledger.py` behavior as the RED baseline.

- [x] **Step 1: Add the minimal intake-state builder and invariant catalog**

Create `review_v2_helpers.py` with these public helpers and exact default shape:

```python
from __future__ import annotations

import copy
import json
from pathlib import Path


def make_empty_v2_state(tmp_path: Path, **overrides: object) -> dict:
    state = {
        "schema_version": 2,
        "review_id": "review-test",
        "generation": 0,
        "status": "active",
        "stage": "intake",
        "scratch_dir": str(tmp_path),
        "snapshot": None,
        "content_objects": {},
        "evidence": {},
        "authorities": {},
        "authority_manifest": None,
        "impact_maps": {},
        "coverage_inventory": None,
        "obligations": {},
        "hypothesis_assignments": {},
        "dispatches": {},
        "reviews": {},
        "route_selections": {},
        "witness_records": {},
        "findings": {},
        "review_repairs": {},
        "checks": {},
        "ready_transition": None,
        "ci_candidate": None,
        "calibration": None,
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

Add named invariant-case constants and minimal malformed dictionaries only. The complete green candidate is intentionally impossible to assemble correctly until canonical payload projection, snapshot, content/evidence, route, witness-record, and transition constructors exist. Define the four later helpers as stubs that raise `NotImplementedError("implemented in Task 4 from production constructors")`; do not copy future schemas or precompute mutually dependent hashes in Task 1.

- [x] **Step 2: Add RED tests for the proven version-1 defects**

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

Each test must exercise a public CLI rather than private helper functions. The `test_lens_triage_resolution_skips_fix` routing correction already landed on main and the focused suite is green at baseline; preserve that contract unchanged and do not spend this plan rehabilitating the legacy graph.

- [x] **Step 3: Add version-2 green-predicate negative tests**

In `test_review_invariants_v2.py`, define one parameterized test that starts from a valid green-candidate fixture and removes exactly one predicate per case:

```python
@pytest.mark.parametrize(
    "missing",
    [
        "snapshot",
        "authority-manifest",
        "authority",
        "impact-map",
        "coverage-inventory",
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
        "witnesses",
    ],
)
def test_green_rejects_each_missing_predicate(tmp_path, missing):
    state = make_complete_candidate(tmp_path)
    observation, now = make_remote_observation(state)
    policies = make_policy_bundle(state)
    remove_predicate(state, observation, missing)
    decision = evaluate_green(state, observation, policies=policies, now=now)
    assert decision.allowed is False
    assert missing in decision.missing
```

Also add:

```text
test_green_rejects_stale_epoch_evidence
test_green_rejects_wrong_snapshot_fingerprint
test_green_rejects_unassessed_obligation
test_green_rejects_incomplete_expected_authority_manifest
test_green_rejects_unverified_authority_discovery_witness
test_green_rejects_missing_impact_map_surface
test_green_rejects_coverage_inventory_that_omits_map_surface
test_green_rejects_coverage_inventory_that_omits_map_hazard
test_green_rejects_missing_inventory_surface_category_obligation
test_green_rejects_inventory_entry_without_all_universal_categories
test_green_rejects_not_applicable_without_qualified_attestation
test_green_rejects_high_risk_not_applicable_without_independent_overlap
test_green_rejects_deferred_minor_finding
test_green_rejects_reviewer_uncertainty
test_green_rejects_malformed_report
test_green_rejects_ci_for_previous_head
test_green_rejects_required_check_from_wrong_app_or_workflow
test_green_rejects_wrong_repository_or_pr_identity
test_green_rejects_unresolved_feedback_drift
test_green_rejects_stable_nonempty_unresolved_feedback_set
test_provider_resolved_feedback_remains_a_finding_until_lifecycle_closure
test_initially_resolved_feedback_materializes_finding
test_green_blocks_when_authority_discovery_witness_reports_incomplete
test_green_rejects_discovery_policy_qualified_by_reviewed_head
test_green_rejects_remote_observation_older_than_60_seconds
test_green_rejects_remote_observation_more_than_5_seconds_in_future
test_green_rejects_accepted_risk_and_returns_reviewed_with_exceptions
test_green_rejects_fast_profile_used_for_strong_obligation
test_green_rejects_mapper_below_strong_or_without_fresh_distinct_execution
test_green_rejects_scope_challenger_below_final_strong_or_reusing_mapper_contract
test_green_rejects_adjudicator_below_source_floor_or_self_adjudicating
test_green_rejects_final_reviewer_below_final_strong
test_green_accepts_role_qualified_profile_for_blind_final
test_green_accepts_role_qualified_profile_for_closure_auditor
test_current_vendored_reviewer_strong_profile_cannot_qualify_as_blind_final
test_green_does_not_require_parent_equality_for_qualified_profile
test_green_rejects_model_override_on_qualified_profile
test_green_rejects_profile_authority_from_reviewed_head
test_green_rejects_final_strong_profile_without_blind_final_role
test_green_rejects_closure_profile_without_closure_role
test_green_rejects_fabricated_launch_or_completion_witness
test_green_rejects_fabricated_command_success_without_execution_witness
test_green_rejects_dirty_checkout_or_mutable_source_command_witness
test_green_rejects_command_with_review_evidence_access_or_surviving_child
test_green_rejects_command_witness_with_wrong_toolchain_or_environment_digest
test_green_rejects_hosted_check_with_local_command_witness
test_green_rejects_local_check_with_remote_observation_witness
test_green_rejects_replayed_launch_witness_or_reused_agent_id
test_green_rejects_cross_review_replay_for_every_witness_kind
test_green_rejects_unverified_witness_source_or_locator
test_green_rejects_reduced_manifest_paired_with_genuine_discovery_witness
test_green_rejects_discovery_witness_for_different_snapshot_subject
test_green_rejects_dispatch_witness_with_broken_or_tampered_transcript_chain
test_green_rejects_contaminated_blind_final_transcript_audit
test_green_rejects_cloned_high_risk_not_applicable_attestations
test_green_rejects_high_risk_exemption_without_final_strong_exemption_challenger
test_green_rejects_whitespace_only_hazard_framing_as_independence
test_green_rejects_mapper_report_paired_with_substituted_map_subject
test_green_rejects_challenger_report_paired_with_substituted_inventory
test_green_rejects_copied_prior_conclusions_in_new_blind_context_evidence
test_blind_final_profile_has_no_exec_write_or_mcp_tools
test_blind_final_transcript_audit_detects_prior_review_or_feedback_reads
test_green_rejects_profile_mapping_change_between_resolution_and_launch
test_final_and_closure_re_resolve_profile_at_each_launch
test_green_blocks_dispatch_when_no_qualifying_profile_exists
test_green_rejects_profile_without_allowed_tools_or_model_pin
test_current_profile_qualification_is_reusable_only_for_matching_non_final_dispatches
test_profile_or_inventory_change_invalidates_qualification
test_any_snapshot_mutation_revokes_green_candidate
test_fix_enters_fixing_with_published_replacement_epoch_before_verification
test_fix_rereview_may_narrow_but_requires_broader_reascent_before_fixed
test_false_positive_resolution_does_not_require_replacement_snapshot
test_confirmed_closure_process_finding_repairs_same_snapshot_then_refinalizes
test_review_process_finding_rejects_enter_fixing_and_byte_identical_refresh
test_review_repair_cannot_close_without_independent_current_verification
test_close_fixed_does_not_advance_epoch_again
test_accepted_risk_does_not_require_replacement_snapshot
test_mapper_finding_is_valid_before_obligations_exist
test_failed_remote_ci_atomically_materializes_a_check_finding
test_green_blocks_when_remote_observation_witness_reports_untrusted_current_attempt
test_green_rejects_manual_or_unauthorized_ci_trigger
test_green_rejects_wrong_workflow_definition_or_policy_input_digest
test_adjudication_and_fix_review_proof_exist_before_resolution_consumes_them
test_adjudication_outcome_cannot_authorize_incompatible_resolution_branch
test_confirmed_adjudication_can_atomically_choose_accept_risk_with_human_proof
test_accept_risk_and_enter_fixing_are_mutually_exclusive
test_non_fix_drift_uses_refresh_review_input_and_reascends
test_scope_risk_consequence_matrix_derives_required_tier
test_consequence_union_drops_none_when_other_mapper_reports_security
test_repo_override_can_raise_but_not_lower_required_tier
test_final_and_closure_reject_not_applicable_outcome
test_hypothesis_assignments_are_canonical_dispatchable_and_seal_bound
test_preflight_rejects_omitted_or_substituted_local_check_policy_item
test_duplicate_json_keys_rejected_at_every_ingestion_boundary
test_every_canonical_projection_matches_independent_golden_bytes_and_hash
test_every_included_projection_field_changes_digest
test_mark_ready_for_ci_is_reserved_and_blocks_without_remote_witness
test_ready_transition_recovers_after_remote_success_before_local_commit
test_initially_ready_pr_uses_verified_idempotent_noop_transition
```

The imports from `review_core` should fail during RED because Tasks 2-4 have not created them.

- [x] **Step 4: Run RED and capture the expected failures**

Run:

```powershell
py -3 -m pytest -q --junitxml="$irReviewScratch/task-1-red.xml" codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_next_node.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py
```

Expected: version-2 imports and legacy-to-version-2 boundary assertions fail because `review_core` and `reviewctl.py` do not exist. The lens-triage contract is already green at baseline, so every other failure is a defect to investigate, not an expected baseline. Record the exact failure summary in the task report.

- [x] **Step 5: Preserve RED evidence without committing it**

Save the exact command, exit code, and failure names in the task's off-repo scratch report, rename the XML as directed, then execute the global recovery recipe with label `task-1`; verify the zip contains the new untracked tests/helpers. Leave RED tests in the working tree and proceed directly to Task 2. Do not stage, commit, publish, or bypass hooks while the suite is intentionally red.

- [x] **Step 6: Mark Task 1 complete in this plan**

Change every Task 1 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 2: Implement the version-2 state model and strict validator

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/__init__.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/model.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/references/review-state-v2.schema.json`
- Create by hand, never from production constructors: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/fixtures/review-v2-canonical-vectors.json`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/review_v2_helpers.py`

**Interfaces:**
- Produces the exact constructor/validator API below, discriminated strict witness/manifest/check schemas, enums/constants, and stable typed errors.
- Consumes: the default state shape and negative cases from Task 1.

```python
class StateValidationError(ValueError):
    code: str
    path: str


def new_state(review_id: str, scratch_dir: Path) -> dict: ...
def strict_json_loads(raw: bytes, *, source: str) -> object: ...
def validate_state(state: dict, *, verify_content: bool = True) -> None: ...
def validate_remote_observation(observation: dict) -> None: ...
def normalize_consequences(*groups: tuple[str, ...]) -> tuple[str, ...]: ...
def manifest_payload(
    *, repository_id: str, pr_number: int, pr_url: str,
    authority_discovery_policy_id: str, authority_discovery_policy_version: str,
    authority_discovery_policy_sha256: str, authorities: tuple[dict, ...],
    feedback_history_policy_id: str, feedback_history_policy_version: str,
    feedback_history_policy_sha256: str, feedback_history_sha256: str,
    local_check_policy_id: str, local_check_policy_version: str,
    local_check_policy_sha256: str, required_check_policy_sha256: str,
    review_assignment_policy_id: str, review_assignment_policy_version: str,
    review_assignment_policy_sha256: str,
    command_execution_policy_id: str, command_execution_policy_version: str,
    command_execution_policy_sha256: str,
    evidence_ingestion_policy_id: str, evidence_ingestion_policy_version: str,
    evidence_ingestion_policy_sha256: str,
    hypothesis_derivation_policy_id: str,
    hypothesis_derivation_policy_version: str,
    hypothesis_derivation_policy_sha256: str,
    unresolved_feedback_sha256: str,
) -> dict: ...
def authority_manifest_id(payload: dict) -> str: ...
def pr_metadata_subject(
    *, title: str, body: str, base_ref: str,
    scope_labels: tuple[str, ...], declared_links: tuple[str, ...],
) -> dict: ...
def snapshot_subject(
    *, epoch: int, repository_id: str, pr_number: int, pr_url: str,
    git_object_format: str, base_sha: str, head_sha: str, tree_sha: str,
    diff_sha256: str, pr_metadata_sha256: str, authority_manifest_sha256: str,
    authority_discovery_policy_id: str, authority_discovery_policy_version: str,
    authority_discovery_policy_sha256: str, witness_policy_sha256: str,
    feedback_history_policy_id: str, feedback_history_policy_version: str,
    feedback_history_policy_sha256: str, feedback_history_sha256: str,
    local_check_policy_id: str, local_check_policy_version: str,
    local_check_policy_sha256: str, required_check_policy_sha256: str,
    review_assignment_policy_id: str, review_assignment_policy_version: str,
    review_assignment_policy_sha256: str,
    command_execution_policy_id: str, command_execution_policy_version: str,
    command_execution_policy_sha256: str,
    evidence_ingestion_policy_id: str, evidence_ingestion_policy_version: str,
    evidence_ingestion_policy_sha256: str,
    hypothesis_derivation_policy_id: str,
    hypothesis_derivation_policy_version: str,
    hypothesis_derivation_policy_sha256: str,
    unresolved_feedback_sha256: str,
) -> dict: ...
def snapshot_fingerprint(snapshot: dict) -> str: ...
def content_id(raw: bytes) -> str: ...
def evidence_binding_subject(record: dict) -> dict: ...
def loaded_authority_subject(record: dict) -> dict: ...
def unavailable_authority_subject(record: dict) -> dict: ...
def impact_map_subject(record: dict) -> dict: ...
def coverage_inventory_subject(record: dict) -> dict: ...
def obligation_subject(record: dict) -> dict: ...
def hypothesis_assignment_subject(record: dict) -> dict: ...
def route_selection_subject(record: dict) -> dict: ...
def pending_dispatch_intent_subject(record: dict) -> dict: ...
def review_wrapper_subject(record: dict) -> dict: ...
def witness_record_subject(record: dict) -> dict: ...
def finding_identity_subject(record: dict) -> dict: ...
def review_repair_intent_subject(record: dict) -> dict: ...
def local_check_subject(record: dict) -> dict: ...
def hosted_check_subject(record: dict) -> dict: ...
def ready_intent_subject(record: dict) -> dict: ...
def ci_candidate_subject(record: dict) -> dict: ...
def blocker_identity_subject(record: dict) -> dict: ...
def green_seal_subject(record: dict) -> dict: ...
def history_record_subject(record: dict) -> dict: ...
def authority_discovery_subject(snapshot: dict, manifest_payload: dict) -> dict: ...
def profile_resolution_subject(route_selection: dict) -> dict: ...
def review_launch_subject(
    pending_dispatch: dict, context_manifest: dict,
    *, tool_use_id: str, task_bytes_sha256: str, profile_name: str,
) -> dict: ...
def review_completion_subject(
    raw_attestation_bytes: bytes, *, tool_transcript_sha256: str,
    agent_id: str,
) -> dict: ...
def command_execution_subject(command_intent: dict, result: dict) -> dict: ...
def remote_transition_subject(
    intent: dict, *, tool_use_id: str,
    prior_lifecycle_state: str, result_lifecycle_state: str,
) -> dict: ...
def remote_observation_subject(observation_without_witness: dict) -> dict: ...
```

The bodies represented by `...` are implementation work, but their allowlists are not: every constructor implements the exact projection row in the normative spec and rejects missing/extra keys before projection. Argument ownership and return types are fixed here; no constructor accepts caller-selected projection keys or performs generic "drop wrapper keys" subtraction. Each error sets a stable `code` and JSON-style `path`. `strict_json_loads()` is the only JSON decoder used by state, CLI, witness acquisition, reports, witness records, observations, evidence re-reads, or golden-vector input; it rejects BOMs, non-finite numbers, and duplicate object keys before canonicalization. Completion subjects bind the digest of the exact accepted raw bytes as well as the validated structured content, the harness-assigned `agent_id`, and the tool transcript.

- [x] **Step 1: Write focused model validation tests**

Add tests that assert `StateValidationError` for:

```text
unknown top-level field
duplicate object key at every state, CLI, witness-acquisition, report, witness-record, observation, and evidence JSON boundary
schema_version other than 2
relative scratch_dir
unknown status, stage, severity, disposition, obligation status, review verdict, or check conclusion
unknown scope level, capability tier, or normalized reasoning floor
unknown dispatch route-selection mode
unknown dispatch context mode
unknown route qualification source
base/head/tree identifiers whose length does not match declared `git_object_format`
snapshot or remote observation with mismatched repository ID, PR number, or canonical PR URL
PR metadata projection that includes draft/ready or omits a content-bearing title/body/base/scope label/link field
non-64-character SHA-256 values
mapping key different from the identifier inside its record
snapshot-derived record ID reused by a later epoch instead of a globally unique epoch namespace
evidence record whose current file is missing, resized, or re-hashed
content object whose path is outside the review-owned content store or not the canonical path for its digest
evidence binding whose content object is absent or whose binding digest is wrong
two epoch bindings for byte-identical content that incorrectly overwrite one another
authority manifest or authority-discovery witness missing, mismatched, or rooted in a policy authored by the reviewed head
authority manifest whose discovery-policy digest differs from the snapshot or sealed connector policy
authority manifest whose review-assignment or command-execution policy identity/version/digest differs from the snapshot/composition-root policy
authority-discovery policy whose identity/version/source is controlled by the reviewed head
feedback history that omits an actionable already-resolved thread or whose policy identity/version/digest is controlled by the reviewed head
loaded authority without source hash/evidence, or unavailable authority with fabricated source fields or missing failure evidence
authority-manifest payload containing local evidence, witness-record, epoch, or fingerprint fields
witness record containing a local evidence ID or wrapper fields
witness record whose transcript-segment or remote-fetch evidence is absent or mismatched
authority, impact map, coverage inventory, obligation, dispatch, review, witness record, finding, review repair, check, or blocker referencing nonexistent evidence
impact map with the wrong mapper role, duplicate surface, missing universal category, duplicate category, or duplicate/blank hazard
impact/coverage entry with missing/unknown consequence, `none` plus another consequence, or obligation consequence not propagated from inventory
conflicting valid map consequences `none` and a substantive value that do not normalize by dropping `none`
coverage inventory whose map or challenger reference is absent, stale, or role-mismatched
coverage inventory that omits a surface, category, or hazard from either current impact map
review whose agent-authored identity, assignment, snapshot, or observed model/context does not match its dispatch's canonical route selection
mapper/challenger report whose witness-bound structured-output digest differs from the stored map/inventory/obligations subjects
adjudication/fix/exemption result with a missing or role-incompatible outcome/evidence set
review without structurally matching launch and completion witness references bound to one transcript `agent_id`
dispatch below an obligation's capability or reasoning floor
impact mapper below strong/high, scope challenger below final-strong, any mapper/challenger in a non-fresh or reused execution, or mapper/challenger role contracts that violate the sealed independence policy
finding adjudicator below max(strong/high, source-dispatch floor, linked-assignment floors), in a non-fresh execution, or self-adjudicating a review-sourced finding through the source execution/role contract
review-repair verifier below its source/target floor, non-fresh, or sharing the source/repair-producing role contract or execution
blind-final or closure dispatch below final-strong capability/reasoning
exemption-challenger dispatch below final-strong capability/reasoning or sharing the primary review's profile contract
blind-final or closure dispatch without a role-qualified profile
role-qualified profile dispatch with a model or reasoning override
blind-final or closure dispatch whose context is not fresh
blind-final or closure dispatch whose profile role does not match its exact requested role
blind-final dispatch whose task text includes prior review or finding evidence
blind-final task text containing any non-allowlisted subject bytes, free-form context, or hazard framing
blind-final transcript audit showing prior-review/feedback/state reads, non-read/search tool use, or an unbound tool-transcript digest
launch witness whose profile name or task bytes differ from the registered dispatch intent
finding resolution referencing a nonexistent finding, review, check, or human decision
obligation/dispatch/review/check epoch different from the current snapshot when used as current
finding resolution epoch earlier than discovery or inconsistent with its proof records
green_seal present before the green-candidate stage
green_seal whose repairs_sha256 omits or mismatches any review-repair record
persisted status green
accepted-risk finding while evaluating a green candidate
blocked status without exactly one active blocker, more than one active blocker, active status with an active blocker, or closed blocker without current resolution evidence/epoch/fingerprint
reviewed-with-exceptions status without at least one proven accepted-risk finding or while another finding remains open
broken history sequence, previous hash, or record hash
remote observation or witness record with unknown/missing fields, short head SHA, wrong authority digest, missing required check, or invalid timestamp
remote check with a wrong app, workflow, run, policy digest, repository/PR identity, feedback digest, or head SHA
hosted check missing policy item, workflow ID/path/definition ref/SHA, event, trigger subject, policy input/configuration digest, check-run, workflow-run, or run-attempt identity; using an unauthorized trigger; or selecting a superseded attempt
local check with hosted fields or remote provenance, and hosted check with a command or local execution provenance
local check missing from the sealed complete policy set or with substituted command, working directory, requiredness, or policy item
local check missing/mismatching command-execution policy, clean-tree materialization/toolchain/environment identity, equal pre/post source digest, or complete process-tree termination
not-applicable obligation without a qualified current assignment attestation and concrete evidence, or high-risk exemption without independent overlap
final or closure result with `not-applicable`
hypothesis assignment with ad hoc/non-canonical ID, missing opposite polarity, wrong policy digest, unresolved dispatch ID, or absent seal binding
pending/in-progress ready transition without its strict intent/idempotency fields, completed transition without a witnessed `gh` call and reconciling observation, or ci_candidate/remote-ci-candidate stage without that completed transition
fixing finding without a replacement snapshot/publication proof, and fixed finding without current verification/re-review proof
review-repairing finding without a confirmed review-process adjudication and exact invalidation cut, or review-repaired finding without current replacement records and independent verification
confirmed candidate-change adjudication entering review repair, confirmed review-process adjudication entering fixing, or either branch being reused after acceptance
any literal canonical-vector input whose constructor bytes/digest/derived ID differ from the independent fixture, any included-field mutation that leaves a digest unchanged, or any excluded-field mutation that changes subject bytes
epoch-zero record of any kind
```

Add a round-trip test proving `new_state()` validates and serializes deterministically.
Add `test_construct_epoch_one_from_raw_witness_payloads_without_fixed_point`: starting only from raw authority/failure bytes, typed discovery outputs, and sealed discovery/witness-policy digests, use production constructors in the required order to compute the manifest payload digest, snapshot fingerprint, payload evidence, witness record, and final manifest wrapper. Assert no hashed projection contains its own digest or any later binding field and no partial wrapper validates.
Add one table-driven golden-vector test for every normative projection and witness target. The literal fixture contains strict input, expected canonical UTF-8 bytes, expected digest/derived ID, and expected witness subject digest where applicable; production code may read but never generate or update it. A per-field mutation test proves every included semantic/security field changes the subject digest and every explicitly excluded wrapper field leaves subject bytes unchanged while strict wrapper/state validation still protects it.

- [x] **Step 2: Implement canonical enums and required keys**

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
    "review-repair",
    "final-review",
    "closure-audit",
    "remote-ci-candidate",
    "remote-ci",
    "green-candidate",
    "reviewed-with-exceptions",
    "blocked",
)
SEVERITIES = ("blocking", "important", "minor")
DISPOSITIONS = (
    "open",
    "fixing",
    "fixed",
    "review-repairing",
    "review-repaired",
    "false-positive",
    "accepted-risk",
    "deferred",
    "contested",
    "unassessed",
)
OBLIGATION_STATUSES = ("pending", "covered", "not-applicable", "invalidated", "unassessed")
REVIEW_VERDICTS = ("clean", "findings", "incomplete", "blocked")
OBLIGATION_OUTCOMES = ("covered", "not-applicable", "findings", "incomplete")
BLIND_FINAL_OUTCOMES = ("covered", "findings", "incomplete")
CLOSURE_AUDIT_OUTCOMES = ("covered", "findings", "incomplete")
FINDING_ADJUDICATION_OUTCOMES = ("confirmed", "false-positive", "contested")
ADJUDICATION_REMEDIATION_CLASSES = ("candidate-change", "review-process")
FIX_REVIEW_OUTCOMES = ("verified", "findings", "incomplete")
REVIEW_REPAIR_OUTCOMES = ("verified", "findings", "incomplete")
EXEMPTION_CHALLENGE_OUTCOMES = ("not-applicable-confirmed", "applicable", "incomplete")
DISPATCH_STATUSES = ("pending", "reported", "incomplete", "invalidated")
READY_TRANSITION_STATUSES = ("pending", "authorized", "completed")
ROUTE_SELECTION_MODES = ("profile",)
ROUTE_QUALIFICATION_SOURCES = ("profile-file",)
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
    "authority-manifest-payload",
    "impact-map",
    "scope-challenge",
    "route-selection",
    "witness-record",
    "check-output",
    "review-attestation",
    "tool-transcript",
    "finding-proof",
    "fix-proof",
    "review-repair-proof",
    "human-decision",
    "remote-observation",
)
AUTHORITY_KINDS = ("repo-law", "pr-description", "issue", "document", "plan", "spec", "non-goal", "review-feedback")
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
CONSEQUENCES = (
    "none",
    "security",
    "authorization",
    "privacy",
    "secrets",
    "irreversible-data-loss",
    "concurrency-recovery",
    "migration-rollback",
    "public-compatibility",
    "source-custody",
)
HYPOTHESIS_POLARITIES = ("claim", "counterexample")
SCOPE_LEVELS = ("hunk", "file", "surface", "cross-surface", "whole-pr")
CAPABILITY_TIERS = ("fast", "focused", "strong", "final-strong")
REASONING_FLOORS = ("low", "standard", "high", "final-strong")
CONTEXT_MODES = ("fresh", "forked")
REVIEW_ROLES = (
    "impact-mapper-semantic",
    "impact-mapper-contract",
    "scope-challenger",
    "obligation-reviewer",
    "exemption-challenger",
    "finding-adjudicator",
    "fix-reviewer",
    "review-repair-verifier",
    "blind-final",
    "closure-auditor",
)
REVIEW_REPAIR_TARGET_KINDS = (
    "semantic-impact",
    "contract-impact",
    "coverage-plan",
    "coverage-challenge",
    "obligation-review",
    "exemption-review",
    "finding-adjudication",
    "fix-review",
    "blind-final",
    "closure-audit",
    "local-check",
    "hosted-check",
)
REVIEW_REPAIR_STATUSES = ("repairing", "verified", "closed")
CHECK_KINDS = ("preflight", "targeted", "remote-ci")
FINDING_SOURCE_KINDS = ("review", "check", "feedback")
WITNESS_KINDS = (
    "authority-discovery",
    "profile-resolution",
    "review-launch",
    "review-completion",
    "command-execution",
    "remote-transition",
    "remote-observation",
    "human-decision",
)
BLOCKER_CLASSES = (
    "authority-missing",
    "feedback-unresolved",
    "intake-incomplete",
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

Implement every named constructor in the API from the normative projection table - no anonymous fallback and no generic key subtraction. Validation reconstructs the exact allowlisted subject and ID derivation, then compares it with the independently authored golden bytes/digest. The test matrix covers every included field, every explicitly excluded wrapper field, derived versus externally assigned IDs, mutable finding/repair/blocker lifecycle fields, and every witness target. A constructor and validator that make the same omission must still fail the literal fixture or per-field mutation vectors.

Validate every first-class route-selection record as the strict design-spec object. `route_selection_subject()` includes its externally assigned globally unique epoch-namespaced ID and the resolved profile identity (profile name plus profile-file bytes hash) and excludes local evidence/epoch/fingerprint fields; evidence binds those subject bytes and the wrapper is attached afterward. The dispatch references that record and does not duplicate profile, tier, model, reasoning, context, parent, or selection fields; CLI output derives them from the route. A `profile` route requires the named profile file to exist in a harness profile root outside the reviewed head - the user-global agents directory; a profile file inside the reviewed tree is reviewed-head content and cannot qualify, carry a `model:` pin at or above the assignment floor and an `allowed-tools` list appropriate to the role, and be dispatched by name with no model/reasoning override; its declared model/reasoning are read from the profile and recorded, never injected. There is no fallback route: when no qualifying profile exists, the dispatch blocks. Launch verification compares the witnessed launch record's profile name and exact task bytes against the route selection and pending dispatch intent; drift between resolution and launch blocks. Mappers, scope challenger, adjudicator, and review-repair verifier require fresh, dispatch-distinct launches at their portable role floors and the exact role-contract separation defined by the spec. Exemption challenger, repair verifier, final, and closure require newly verified profile resolution for each launch; exemption/final/closure and any repair reaching whole-PR proof are role-specific `final-strong`. They never reuse cached qualification. Blind-final context uses the strict constructor-owned allowlist manifest and requires `hazard_framing_sha256: null`.

- [x] **Step 3: Implement snapshot fingerprinting**

Use canonical JSON with sorted keys and compact separators:

```python
def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()
```

Canonicalization is only for an already validated object. All raw JSON reaches it through `strict_json_loads()` using a duplicate-key-rejecting `object_pairs_hook`; the implementation must not call plain `json.load()`/`json.loads()` at any ingress boundary.

Implement and test the construction order rather than accepting a preassembled mutually dependent object:

1. `manifest_payload()` emits only typed discovery fields, externally rooted discovery-policy identity/version/digest, and the local-check, hosted-check, evidence-ingestion, hypothesis-policy, feedback, and authority digests; it contains no local IDs/bindings. `authority_manifest_id()` hashes that payload.
2. `snapshot_subject()` includes that manifest digest and every sealed policy identity/digest but excludes `fingerprint`; its canonical PR-metadata projection explicitly excludes draft/ready lifecycle state.
3. `snapshot_fingerprint()` hashes exactly that subject and validation compares it with `fingerprint`.
4. Epoch-bound content/evidence for manifest and authority/failure payloads are attached only after both hashes exist; the manifest wrapper does not yet exist.
5. The authority-discovery witness subject hashes the full snapshot subject plus fingerprint and typed manifest digest; store its record/evidence/wrapper, then construct the complete manifest wrapper last.

This order must be the only production constructor path. No digest projection contains its own digest, evidence ID, witness ID, epoch binding, or later wrapper.

- [x] **Step 4: Implement recursive state validation**

`validate_state()` must implement the exact top-level and record contracts in the source design and:

1. validate top-level keys, generation, and enums;
2. validate the snapshot or require `None` during intake;
3. validate content objects, epoch-bound evidence bindings, the nullable expected-authority manifest, authorities, impact maps, the nullable coverage inventory, obligations, canonical hypothesis assignments, route selections, dispatches, reviews, witness records, feedback/review/check findings, review-repair intents, discriminated checks, nullable ready-transition intent, CI candidate, and calibration record, blockers, seal, and history by key allowlists;
4. ensure referenced evidence/content IDs exist, `content_id == sha256(bytes)`, and `evidence_id == sha256(canonical binding projection)`; permit multiple epoch bindings to the same content object without mutation;
5. permit at most one current map per mapper role during ordered construction, reject duplicate or role-mismatched maps, validate strict impact/coverage entries, normalize cross-map consequences by vocabulary-ordered union of substantive values (or exactly `none` only when no substantive value exists), and, whenever a coverage inventory is present, prove it contains the full surface, category, normalized-consequence, and hazard union without trusting caller summaries;
6. require the coverage inventory to reference the two current maps, the current scope-challenger attestation, and evidence bytes encoding the exact inventory;
7. recompute the authority-manifest payload digest, require it to match snapshot repository/PR/discovery-policy/authority/complete-feedback-history/unresolved-subset/check-policy identity and every stored current loaded/unavailable authority exactly once, materialize provider/thread-keyed findings for all actionable feedback history regardless of provider resolution state, and require a structurally matching authority-discovery witness subject bound to the full snapshot and manifest digest;
8. ensure each review's role-specific results and structured-output digests match its dispatch, route selection, and derived records; final/closure cannot return `not-applicable`; each dispatch resolves canonical obligation/finding/hypothesis assignment IDs and meets its assignment floor; each local check references `command-execution`; each hosted check references the current authorized trigger, immutable workflow definition, policy inputs/configuration, and non-superseded policy-item/check-run/workflow-run/attempt `remote-observation`; and all witness-record full scope plus subject digests are structurally consistent without treating them as authentic;
9. require exemption/final/closure dispatches to use role-qualified `final-strong` profiles in precedence order; reject reviewed-head profile authority, wrong-role profiles, model/reasoning overrides, non-fresh/cached qualification, launch-record drift, and any blind-final task byte outside the constructor-owned raw-subject allowlist;
10. ensure each review-owned content-store file still exists and matches its registered byte length and digest;
11. ensure current evidence matches the current epoch and fingerprint;
12. derive and validate canonical first-class hypothesis assignments from the sealed policy; enforce structured `not-applicable` proof; high-risk exemptions require opposite-polarity assignments plus a separate final-strong `exemption-challenger`, a distinct profile contract, dispatch, witnessed execution, and fresh context - not raw hash inequality;
13. ensure `fixing`, `fixed`, and `false-positive` findings contain their required proof fields and legal epoch relationships;
14. ensure `accepted-risk` cannot satisfy a green candidate;
15. verify monotonic history sequence/generation, require the final history generation to equal top-level generation, and verify `previous_record_sha256` plus `record_sha256` chain values;
16. require at most one active blocker, persisted resolution evidence on every closed blocker, status/blocker consistency, and reviewed-with-exceptions/accepted-risk consistency;
17. allow `green_seal` only at `green-candidate` and reject any attempt to persist a green status.

`validate_state()` proves strict shape and internal cross-reference consistency only. It must not label witness records authentic. Policy/engine predicates call the composition-root `WitnessVerifier`, which selects a witness source from the sealed per-kind policy - the hook-transcript store for local kinds, `gh` remote state for remote kinds - verifies chain integrity or re-fetches the remote record, and compares its subject and harness-assigned identity. State fields cannot select a verifier or widen the witness policy.

Return `None` on success and raise `StateValidationError` with a stable path-prefixed message on failure, for example `findings.F-1.disposition: unknown value 'ignored'`.

- [x] **Step 5: Document the same contract in JSON Schema**

Write `review-state-v2.schema.json` as Draft 7 with `additionalProperties: false` at every object level and enum values identical to `model.py`. The Python validator remains runtime authority; the schema is interoperability documentation and a test fixture. Add a standard-library test that walks the schema and asserts every documented object closes additional properties and every named enum equals its Python tuple, so the two representations cannot drift silently.

- [x] **Step 6: Run model tests**

```powershell
py -3 -m pytest -q --junitxml="$irReviewScratch/task-2-tests.xml" codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py
```

Expected: PASS.

- [x] **Step 7: Verify and persist the Task 2 recovery checkpoint**

Run `git diff --check`, confirm only intended canonical source/tests/references/plan tracking changed, then execute the global task-boundary recovery recipe with label `task-2` and hash `task-2-tests.xml`. Verify the zip contains untracked model/schema/test files. Do not commit while later invariant tests remain RED.

- [x] **Step 8: Mark Task 2 complete in this plan**

Change every Task 2 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 3: Add locked state storage and content-addressed evidence

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/store.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_store_v2.py`

**Interfaces:**
- Consumes: `validate_state()`, `canonical_json()`, and `sha256_json()` from Task 2.
- Produces the exact API and ownership below. `StateTransaction` alone may commit an existing state; registration mutates only `tx.candidate`; the CLI never receives `allowed_sources` directly.

```python
class StoreError(RuntimeError):
    code: str
class ConcurrentStateError(StoreError): pass
class UnsafeEvidenceSourceError(StoreError): pass

@dataclass(frozen=True)
class EvidenceRegistration:
    content_id: str
    evidence_id: str
    bytes: int
    sha256: str

@dataclass(frozen=True)
class EvidenceRequest:
    alias: str
    kind: str
    source: Path
    snapshot_epoch: int
    snapshot_fingerprint: str

@dataclass(frozen=True)
class EvidenceIngestionPolicy:
    source_id: str
    source_version: str
    sha256: str
    per_kind_max_bytes: Mapping[str, int]
    transaction_max_bytes: int
    review_max_bytes: int
    windows_allowed_trustee_sids: tuple[str, ...]
    posix_directory_mode: int
    posix_file_mode: int

@dataclass(frozen=True)
class EvidenceIngestionContext:
    action: str
    candidate_snapshot: dict | None
    eligible_sources: tuple[Path, ...]

class StateTransaction(AbstractContextManager["StateTransaction"]):
    prior_generation: int
    prior_bytes_sha256: str
    candidate: dict
    def commit(self) -> dict: ...

def load_state(path: Path) -> dict: ...
def create_state(path: Path, state: dict) -> None: ...
def locked_state_transaction(path: Path) -> StateTransaction: ...
def register_evidence(
    tx: StateTransaction, source: Path, *, alias: str, kind: str,
    snapshot_epoch: int, snapshot_fingerprint: str,
    policy: EvidenceIngestionPolicy, context: EvidenceIngestionContext,
) -> EvidenceRegistration: ...
def register_evidence_batch(
    tx: StateTransaction, requests: tuple[EvidenceRequest, ...], *,
    policy: EvidenceIngestionPolicy, context: EvidenceIngestionContext,
) -> dict[str, EvidenceRegistration]: ...
def resolve_evidence_aliases(payload: dict, registrations: dict[str, EvidenceRegistration]) -> dict: ...
def verify_evidence_files(state: dict, evidence_ids: tuple[str, ...]) -> None: ...
def append_history(candidate: dict, *, event: str, data_sha256: str) -> dict: ...
```

`StateTransaction` captures prior generation and exact persisted-byte SHA-256, increments generation exactly once, rechecks both immediately before replacement, and rejects stale/lost updates. The composition root supplies the sealed ingestion policy whose digest must equal the candidate/current snapshot; every cap is positive, every evidence kind has an explicit cap, Windows trustees are exact SID strings, and POSIX modes may not grant group/other access. The engine alone derives the context's action, candidate snapshot, and exact file allowlist from trusted manifest paths and dedicated witness-source staging files; callers cannot broaden it to a root. Registration stores immutable content under `<scratch_dir>/evidence-store/sha256/<digest>` and a separate epoch-bound evidence binding, never a live source path. Errors have stable codes such as `state-concurrent`, `unsafe-source`, `content-drift`, `policy-mismatch`, `size-cap`, `acl-untrusted`, and `state-invalid`.

- [x] **Step 1: Write failing atomicity and evidence tests**

Add tests for:

```text
load rejects missing, malformed, BOM-drifted, and version-1 state with distinct errors
create/commit validates before writing
commit leaves the previous valid file intact when serialization or replace fails
commit writes UTF-8 without BOM and a final newline
two processes loading generation N cannot both commit; a concurrent finding cannot be lost to a stale green candidate
commit rejects a changed prior-byte digest even when generation was illicitly left unchanged
the exclusive lock covers load, evidence ingestion, validation, history append, generation increment, and replace
register_evidence rejects missing files, directories, empty files, stale epochs, and stale fingerprints
register_evidence rejects UNC/device paths, alternate data streams, reparse points/symlinks in any component, sources outside the exact per-action allowlist, VCS/administrative metadata, state/lock/temp self-reference, broad/unapproved Windows trustees, unsafe POSIX modes, and per-kind/transaction/review size-cap violations
register_evidence verifies final handle volume/path/file identity and stable size, denies write/delete sharing, reads that handle once, stores an immutable content object, and creates a separate epoch-bound evidence binding
register_evidence never reopens the source between validation and hashing and verification never reopens the source
register_evidence deduplicates identical content while preserving two distinct evidence bindings when the same bytes are used in successive epochs
scratch/store creation rejects substituted reparse roots, broad ACLs, and final-path escape
POSIX descriptor-relative traversal rejects component swaps/symlinks and unsupported safe primitives block without fallback
batch registration rejects duplicate aliases, unknown kinds, unresolved aliases, unused aliases, and non-evidence-field alias substitution
candidate-snapshot registration is accepted only when the ingestion context action is empty-intake `freeze-review-input`, confirmed-fix `enter-fixing`, or trusted-drift `refresh-review-input`; replacement transitions advance exactly one epoch
candidate-snapshot registration rejects every other action, byte-identical/non-advancing refresh, pre-publication/local-only fix, or mismatched replacement authority manifest
verify_evidence_files detects disappearance or byte drift after registration
append_history assigns a monotonic sequence, chains record hashes, and never rewrites prior records
```

- [x] **Step 2: Implement locked compare-and-swap state transactions**

Use a sibling lock file with an OS-level exclusive lock. Acquire it before reading the state and retain it until the replacement and directory flush are complete. `StateTransaction` captures the exact prior bytes, their SHA-256, and `generation`; immediately before commit it re-reads through the held lock and compares both, validates the candidate, requires `candidate["generation"] == prior + 1`, then writes a sibling temporary file with UTF-8/no BOM/final newline, flushes and `os.fsync()`s, closes it, and calls `os.replace`. Delete only the explicit temporary file on failure. Never delete or rewrite the parent directory. Add a deterministic two-process barrier test in which one transaction records a finding and the stale transaction attempts to seal; exactly one commits and the finding remains.

Create and verify the scratch/evidence-store root with private current-user permissions. On Windows, reject extended/device/UNC namespaces and alternate-data-stream syntax; open path components and final files using `CreateFileW` reparse-safe flags, reject any reparse tag, deny write/delete sharing for the source read, and verify `GetFinalPathNameByHandleW`, volume serial number, file ID, regular-file type, and stable size against the exact allowlisted path before streaming. This final-handle identity check is mandatory even after component checks, so a junction swap cannot redirect ingestion. Use the same root/final-path verification for store creation and later content verification.

On POSIX, start from verified directory descriptors and traverse each component with `openat`/`O_NOFOLLOW`; use `fstat` to reject symlinks/non-regular files, perform the bounded read from that same descriptor, create roots/files with private modes, and fsync both files and owning directories. Add Linux tests that swap a parent symlink between validation and open and assert rejection. If the platform lacks the required safe-open/locking primitives, initialization returns typed `unsupported-safe-store` and blocks; do not implement a `resolve()`-then-`open()` fallback.

- [x] **Step 3: Implement content-addressed evidence registration**

Content IDs use `sha256:` followed by the file's lowercase digest. Evidence IDs use `evidence:` followed by the SHA-256 of the canonical binding projection. A representative content object and binding are:

```json
{
  "content_objects": {
    "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": {
      "content_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "path": "C:/review/evidence-store/sha256/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "bytes": 1234
    }
  },
  "evidence": {
    "evidence:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc": {
      "evidence_id": "evidence:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "content_id": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "kind": "review-attestation",
      "snapshot_epoch": 2,
      "snapshot_fingerprint": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    }
  }
}
```

CLI data files refer to command-local evidence as `@alias` only in allowlisted evidence-reference fields. Repeated CLI arguments use `--evidence-file alias=kind=C:/absolute/path`. The current action recipe declares every alias/kind, and the engine resolves its exact eligible source: a trusted-manifest repo file or a dedicated per-transaction staging file materialized by a connector/harness action. It constructs `EvidenceIngestionContext` itself and passes the composition-root `EvidenceIngestionPolicy`; the user cannot select an action context, candidate snapshot, policy, trustee, cap, or allowed root. Registration streams bounded bytes from the one verified handle into the owned store, fsyncs, and constructs the content object followed by the epoch binding. The in-memory transaction resolves aliases to evidence IDs, rejects unused/unresolved aliases, validates final state, and commits once. `candidate_snapshot` is legal only for initial freeze, published `enter-fixing`, or trusted `refresh-review-input`; each atomically ingests the replacement snapshot, canonical manifest payload, authority/failure records, discovery witness record, and finally the complete manifest wrapper with no intermediate current state. Add an epoch-advance test where an unchanged authority document reuses its content object while retaining two distinct evidence bindings and historical wrappers, plus a test rejecting a manifest wrapper created before its discovery witness exists.

- [x] **Step 4: Implement append-only history records**

Each accepted mutation appends:

```json
{
  "sequence": 7,
  "generation": 7,
  "event": "finding-resolved",
  "snapshot_epoch": 2,
  "snapshot_fingerprint": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "data_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "previous_record_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "record_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
}
```

History is diagnostic. Current state remains decision authority. For non-empty state, the final history `generation` equals top-level `generation`; each accepted mutation increments both exactly once.

- [x] **Step 5: Run store and model tests**

```powershell
py -3 -m pytest -q --junitxml="$irReviewScratch/task-3-tests.xml" codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_model_v2.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_store_v2.py
```

Expected: PASS.

- [x] **Step 6: Verify and persist the Task 3 recovery checkpoint**

Run `git diff --check`, confirm store/model tests are green, then execute the global task-boundary recovery recipe with label `task-3` and hash `task-3-tests.xml`. Verify the zip contains the untracked store/tests. Do not commit while policy and CLI invariant tests remain RED.

- [x] **Step 7: Mark Task 3 complete in this plan**

Change every Task 3 checkbox to `[x]` in the working tree. Task 6 will stage the completed plan after the implementation is green.

---

### Task 4: Implement the pure fail-closed policy and green predicate

**Files:**
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts/review_core/policy.py`
- Create: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_policy_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py`
- Modify: `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/review_v2_helpers.py`

**Interfaces:**
- Consumes: validated state from Task 2 and evidence records from Task 3.
- Produces: sealed `WitnessPolicy`, `ReviewAssignmentPolicy`, `CommandExecutionPolicy`, `LocalCheckPolicy`, and `HypothesisDerivationPolicy` protocols; `Decision`, `next_action`, `register_dispatch`, `record_launch`, `evaluate_green`, `complete_action`, `block_review`, and `resume_review` with the exact signatures below. The composition-root verifier owns the sealed per-kind source registry (hook-transcript store or `gh` remote state), verifies transcript-chain integrity or re-fetches remote records, enforces harness-identity uniqueness, and returns verified witness identities; no generic local-file or caller-selected verifier exists.

- [x] **Step 1: Write the complete transition table as tests**

Parameterize `test_review_policy_v2.py` over this clean happy-path action sequence (no findings):

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
    "run-final-review",
    "run-closure-audit",
    "mark-ready-for-ci",
    "run-remote-ci",
    "seal-green",
)
```

Action payloads are allowlisted, never merged generically:

| Action | Exact accepted `data` keys |
|---|---|
| `freeze-review-input` | `snapshot`, `authority_manifest`, `authorities` |
| `refresh-review-input` | `snapshot`, `authority_manifest`, `authorities`, `drift_reasons` |
| `map-impact-semantic` | `impact_map`, `attestation`, `findings` |
| `map-impact-contract` | `impact_map`, `attestation`, `findings` |
| `plan-coverage` | `obligations` |
| `challenge-coverage` | `coverage_inventory`, `attestation`, `findings`, `revised_obligations` |
| `run-preflight` | `checks` |
| `run-fast-review` | `attestations`, `findings` |
| `run-focused-review` | `attestations`, `findings` |
| `run-strong-review` | `attestations`, `findings` |
| `run-exemption-challenge` | `attestations`, `findings` |
| `adjudicate-findings` | `attestations`, `findings` |
| `close-false-positive` | `resolutions` |
| `enter-fixing` | `resolutions`, `replacement_snapshot`, `replacement_authority_manifest`, `replacement_authorities` |
| `run-fix-verification` | `checks` |
| `review-fix` | `attestations`, `findings` |
| `close-fixed` | `resolutions` |
| `enter-review-repair` | `resolutions` |
| `verify-review-repair` | `attestations`, `findings` |
| `close-review-repaired` | `resolutions` |
| `accept-risk` | `resolutions` |
| `resume-review` | `blocker_id`, `resolution_evidence_ids` |
| `run-final-review` | `attestation`, `findings` |
| `run-closure-audit` | `attestation`, `findings` |
| `mark-ready-for-ci` | no caller keys; the witnessed `gh` transition derives `ci_candidate` and transition witness |
| `run-remote-ci` | `remote_observation`, `checks` |
| `seal-green` | no keys; policy derives every digest and the seal |

The table is the engine's normalized action contract, not a promise that every field is caller-supplied. Snapshot discovery, route selection, witness records, command results, ready transitions, and remote observations may enter it only from the corresponding composition-root witness acquisition. Plan 1 reserves and tests `mark-ready-for-ci` plus the `remote-ci-candidate` stage but returns a typed missing-witness-source block for live execution until Plan 6; the CLI cannot accept files for provenance-bearing fields.

If freeze/refresh discovers unavailable authority or non-empty feedback, the same transaction installs the representable snapshot/manifest records and deterministically opens one blocker: `authority-missing`, `feedback-unresolved`, or `intake-incomplete` when both classes occur. Its evidence/reason enumerates every cause; resume requires proof that all listed causes changed, normally followed by trusted refresh. There is no transient active state with incomplete authority and no caller-supplied blocker record.

Reject missing or extra payload keys. Resolution payloads are discriminated further: `close-false-positive` requires an existing adjudicator outcome of `false-positive` plus counter-evidence IDs and no replacement fields. A `confirmed` result has exactly one remediation class. `candidate-change` permits exactly `enter-fixing` or `accept-risk`; `review-process` permits exactly `enter-review-repair` or `accept-risk`. `enter-fixing` requires publication IDs and non-null replacement records. `enter-review-repair` forbids replacement records, preserves epoch/fingerprint, derives the exact invalidation cut from the closed target kind/IDs, creates a strict repair intent, and moves the finding to `review-repairing`. `verify-review-repair` records an independent current attestation only after the invalidated gates have replacement records; `close-review-repaired` consumes an existing `verified` result and exact replacements, then forces new blind-final/closure. `close-fixed` requires existing `verified` targeted-check/fix-review/current-obligation IDs and forbids replacement fields. `accept-risk` requires durable human-decision evidence, consumes the confirmed branch, forbids replacement fields, and atomically enters `reviewed-with-exceptions`. `refresh-review-input` requires a trusted discovery result that differs in at least one snapshot subject field, advances exactly one epoch, and has no finding-resolution semantics. `resume-review` names the sole active blocker and non-empty current resolution evidence. The Task 5 engine works inside one `locked_state_transaction`, registers supplied evidence on the in-memory copy, then `complete_action()` ingests allowlisted records and validates the whole candidate. Hash the canonical action, branch-specific payload, prior generation, and evidence IDs for idempotency; an identical replay against the already-produced generation is a no-op, while the same action key with different content is an error.

Implement the design spec's closed repair-target invalidation table literally and parameterize every row. The engine computes the exact transitive `invalidated_record_ids`; caller/adjudicator data may name only the typed target IDs and cannot add, omit, or retain dependent records. `finding-adjudication` reopens the finding whose invalidated resolution it authorized; `fix-review` returns its already-current-snapshot finding to `fixing`; authority/feedback/policy/snapshot omissions reject review repair and require trusted drift refresh. Tests prove the unchanged epoch/fingerprint, retained historical IDs, new globally unique replacement IDs, exact earliest next action, and mandatory fresh final/closure for every row.

Before any subagent-backed action runs, `register_dispatch()` must persist its pending dispatch, referenced canonical route selection and resolved profile identity, the declared-blindness/context manifest digests, and context-package/hazard-framing digests. It computes the maximum portable role floor, sealed `ReviewAssignmentPolicy` floor, source-dispatch floor, and linked assignment floors; every reviewer-backed `ActionRecipe` has non-null capability/reasoning floors. It also resolves the role's fresh-context, distinct-dispatch, distinct-profile-contract, and non-self-adjudication constraints against current witnessed provenance before route selection. The route selection captures live inventory, budget contract, resolved profile-file identity/hash, required tier/role, selected route representation, qualification source, and rationale. Qualification may be reused only where the assignment policy permits; mapper, challenger, adjudicator, repair-verifier, exemption, blind-final, and closure launches are fresh, and the last four plus any policy-designated role re-resolve immediately before launch. `record_launch()` then binds the witnessed `run_subagent` call: the hook transcript's `tool_use_id`, verbatim task bytes, and profile name must match the registered intent. Completion is rejected unless the sealed-policy verifier confirms matching launch and completion transcript records scoped to the exact review/dispatch/epoch/fingerprint, bound to one harness-assigned `agent_id`, plus the ordered `tool-transcript` digest covering every call the dispatch made. Completion binds the exact accepted raw attestation bytes plus that transcript digest. Caller-authored witness-shaped JSON is not provenance. Also reject action/report mismatch, a route below the computed role/assignment/source floor, any independence violation, a wrong-role/anchored final profile, model/reasoning override, or a profile absent at launch. Blind-final dispatch uses the constructor-owned context manifest, no free-form context/hazard framing, inert authority/repository data, and a read/search-only `allowed-tools` profile; post-completion transcript audit must show no reads of review state, prior reports/findings, or provider feedback/comments - contamination invalidates the review and opens a `review-process` finding. Deterministic actions (`freeze-review-input`, `plan-coverage`, `run-preflight`, `mark-ready-for-ci`, `run-remote-ci`, and `seal-green`) do not require a reviewer dispatch, but freeze, commands, ready transition, and remote CI still require their witnesses. Mapper completion atomically derives its impact-map record from the witness-bound digest. Challenge completion atomically derives the coverage inventory, canonical hypothesis assignments, and replacement obligations from witness-bound digests.

Witness subjects use explicit non-circular projections: profile resolution hashes the canonical route-selection content plus resolved profile-file identity; launch hashes the pending dispatch intent, context manifests, the transcript `tool_use_id`, and the exact task bytes; completion hashes the exact raw agent-authored attestation, harness `agent_id`, and ordered typed tool transcript before the state-only review wrapper exists. Mapper/challenger raw attestations contain the exact map/inventory/obligation/hypothesis subject digests, and the engine derives records only from matching bytes. A stored wrapper references canonical witness-record evidence that contains no local evidence ID. Add tests that changing any projected or scope field, substituting structured output, changing a named-profile mapping before launch, replaying across reviews/dispatches/actions or with a reused `agent_id`/`tool_use_id`, hashing a witness-enriched wrapper, injecting duplicate JSON keys, or referencing a transcript segment whose chain digest does not verify is rejected.

`mark-ready-for-ci` is a durable three-phase protocol rather than one `gh` call. Derive its idempotency key from canonical `{review_id, repository_id, pr_number, head_sha, snapshot_epoch, action: "mark-ready-for-ci"}` and its ID as `ready:<epoch>:<idempotency-key>`. Phase 1 persists that pending intent plus prior/expected lifecycle. Phase 2 performs the witnessed `gh pr ready` call; the `remote-transition` witness binds the transcript `tool_use_id` and verbatim command/response. Phase 3 re-fetches PR state through `gh`, confirms the transition (or a verified already-ready no-op tied to the same intent and exact head), marks the intent completed, and creates `ci_candidate` atomically. A crash after remote success therefore leaves an in-progress intent that retry can reconcile. Unassociated ready state is not completion. Plan 1 implements and tests pure state/subject semantics but its CLI blocks the live phases until Plan 6 supplies the witnessed `gh` path.

For each action, test:

- it is the only returned next action when all prior predicates are complete;
- skipping it is rejected;
- evidence for another epoch is rejected;
- missing or malformed required evidence is rejected;
- completing it appends one history event and advances the derived stage;
- repeating the identical completion is idempotent;
- repeating it with different data is rejected.

Also test that a caller-forged stored `stage` cannot skip an action; `next_action()` derives the lawful stage from records and the engine overwrites the stored display value on every accepted mutation.

Now extend `review_v2_helpers.py` using only production constructors from Tasks 2-3. Small builders create one canonical artifact at a time: raw loaded/unavailable authority/manifest payload, snapshot, content object/evidence binding, route/profile selection, strict declared-blindness context manifest, pending dispatch, transcript launch/completion segment, raw discriminated attestation and tool transcript, witness record, canonical hypothesis assignment, feedback finding, review-repair intent/proof, complete-policy engine-witnessed local check, hosted workflow-definition/trigger/input/attempt observation, CI candidate, blocker/resume proof, and finding resolution. `make_complete_candidate()` composes those builders in dependency order and materializes the smallest valid state satisfying every stored green-candidate predicate. It includes distinct role-qualified final/closure profiles with affirmative `covered` results, a fixed finding whose typed adjudication/check/fix-review proof predates closure, a same-snapshot review-repaired finding whose independent proof predates fresh final/closure, canonical empty unresolved feedback, and a local plus hosted check using their respective provenance unions. `make_remote_observation()` creates separate fresh presentation bytes; `make_policy_bundle()` supplies test-only sealed witness/local-check/review-assignment/command-execution/hypothesis policies after the live Task 0 floor check; `remove_predicate()` removes only named proof. Add a fixture reading the exact canonical `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/reviewer-strong.md` bytes and assert that its prior-log contract cannot qualify as `blind-final`.

Add conditional transition tests for every finding-producing gate (`map-impact-*`, `challenge-coverage`, feedback intake, preflight, fast, focused, strong, exemption challenge, fix review, repair verification, final, closure, and remote CI): any new finding interrupts immediately and makes `adjudicate-findings` the only action until a current witnessed typed outcome exists. Mapper findings use the snapshot assignment and nullable obligation; failed checks cause the engine to materialize typed check findings atomically rather than trusting a caller-supplied findings list. On both initial freeze and refresh, the sealed feedback-history source enumerates every actionable provider thread/change request, including already-resolved items, and the engine creates a durable finding keyed by provider/thread identity unless a lawful lifecycle closure already exists. Provider-side resolution changes the current feedback subset but cannot close that finding. A proposed high-risk N/A result makes `run-exemption-challenge` the next action before final; `applicable` rejects the exemption and returns to the earliest incomplete obligation predicate, while `not-applicable-confirmed` completes it. A `false-positive` adjudication outcome permits only `close-false-positive`. A `confirmed/candidate-change` outcome permits exactly `enter-fixing` or `accept-risk`; a `confirmed/review-process` outcome permits exactly `enter-review-repair` or `accept-risk`; `contested` blocks. No outcome can authorize a different or second branch. `enter-fixing` accepts published replacement snapshot/manifest/authorities in one atomic transition, advances exactly one epoch with `head_sha == fix_sha`, invalidates current derived evidence, and returns to semantic impact mapping. While a finding is `fixing`, policy permits impact/check/fast/focused/strong re-ascent but blocks final review. It then requires already-recorded `run-fix-verification` and witness-bound `review-fix: verified` proof before `close-fixed` may consume those IDs without advancing the epoch. `enter-review-repair` preserves the exact snapshot, marks the finding `review-repairing`, derives and atomically invalidates the target/downstream record cut, and returns the earliest missing gate. After replacement proof exists, `verify-review-repair` must run under the computed independent floor; only its already-recorded `verified` result allows `close-review-repaired`, after which blind final and closure run fresh. Add an end-to-end case where closure finds an omitted coverage/security review on unchanged bytes; no no-op commit, byte-identical refresh, false-positive, or self-closing repair may escape the lawful repair route. Separately, any trusted non-fix drift requires `refresh-review-input`, advances one epoch, invalidates the same derived evidence, and re-ascends. Test all resolution branches, refresh causes, and finding origins, including feedback, final, and closure.

- [x] **Step 2: Implement `Decision` and explicit missing predicates**

Use:

```python
class WitnessVerificationError(RuntimeError):
    code: str


@dataclass(frozen=True)
class WitnessSource:
    kind: str
    source: str  # "hook-transcript" | "github-remote"
    locator_prefix: str


@dataclass(frozen=True)
class VerifiedWitness:
    witness_id: str
    kind: str
    source: str
    locator: str
    review_id: str
    dispatch_id: str | None
    snapshot_epoch: int
    snapshot_fingerprint: str
    subject_sha256: str
    tool_use_id: str | None
    agent_id: str | None
    observed_at: datetime
    record_sha256: str


class WitnessPolicy(Protocol):
    @property
    def sha256(self) -> str: ...

    @property
    def sources(self) -> tuple[WitnessSource, ...]: ...

    def permits(self, *, kind: str, source: str, locator: str) -> bool: ...


class WitnessVerifier(Protocol):
    @property
    def policy(self) -> WitnessPolicy: ...

    def verify(
        self,
        *,
        stored_record_bytes: bytes,
        expected_kind: str,
        expected_review_id: str,
        expected_dispatch_id: str | None,
        expected_snapshot_epoch: int,
        expected_snapshot_fingerprint: str,
        expected_subject: bytes,
        expected_tool_use_id: str | None,
        expected_agent_id: str | None,
    ) -> VerifiedWitness: ...


@dataclass(frozen=True)
class LocalCheckItem:
    policy_item_id: str
    name: str
    command: tuple[str, ...]
    working_directory: str
    required: bool


class LocalCheckPolicy(Protocol):
    @property
    def source_id(self) -> str: ...

    @property
    def source_version(self) -> str: ...

    @property
    def sha256(self) -> str: ...

    @property
    def items(self) -> tuple[LocalCheckItem, ...]: ...


@dataclass(frozen=True)
class RoleRequirement:
    capability_tier: str
    reasoning_floor: str
    context_mode: str
    distinct_execution_from: tuple[str, ...]
    distinct_role_contract_from: tuple[str, ...]


class ReviewAssignmentPolicy(Protocol):
    @property
    def source_id(self) -> str: ...

    @property
    def source_version(self) -> str: ...

    @property
    def sha256(self) -> str: ...

    def requirement(
        self, *, state: dict, role: str, assignment_ids: tuple[str, ...],
    ) -> RoleRequirement: ...


class CommandExecutionPolicy(Protocol):
    @property
    def source_id(self) -> str: ...

    @property
    def source_version(self) -> str: ...

    @property
    def sha256(self) -> str: ...

    def command_intent(
        self, *, snapshot: dict, item: LocalCheckItem,
    ) -> dict: ...


class HypothesisDerivationPolicy(Protocol):
    @property
    def source_id(self) -> str: ...

    @property
    def source_version(self) -> str: ...

    @property
    def sha256(self) -> str: ...

    def derive(self, *, obligation: dict) -> tuple[dict, ...]: ...


@dataclass(frozen=True)
class PolicyBundle:
    witness_verifier: WitnessVerifier
    local_checks: LocalCheckPolicy
    review_assignments: ReviewAssignmentPolicy
    command_execution: CommandExecutionPolicy
    hypotheses: HypothesisDerivationPolicy


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


def next_action(state: dict, *, policies: PolicyBundle) -> Decision: ...
def register_dispatch(
    state: dict, *, route_selection: dict, dispatch: dict,
    policies: PolicyBundle,
) -> dict: ...
def record_launch(
    state: dict, *, dispatch_id: str, launch_witness_bytes: bytes,
    policies: PolicyBundle,
) -> dict: ...
def complete_action(
    state: dict, *, action: str, raw_data: bytes,
    policies: PolicyBundle,
) -> dict: ...
def evaluate_green(
    state: dict, remote_observation_bytes: bytes, *,
    policies: PolicyBundle, now: datetime,
) -> Decision: ...
def block_review(
    state: dict, *, blocker_id: str, blocker_class: str, reason: str,
    evidence_ids: tuple[str, ...],
) -> dict: ...
def resume_review(
    state: dict, *, blocker_id: str,
    resolution_evidence_ids: tuple[str, ...],
) -> dict: ...
```

These functions return a validated candidate copy and never write files. `review_core.engine` alone owns locked persistence and witness-source access. Raw byte arguments are decoded once with `strict_json_loads()`. Each policy digest must equal its snapshot-bound digest; state/CLI data cannot substitute a policy. `WitnessVerificationError.code` is one of `missing-source`, `policy-drift`, `source-untrusted`, `locator-untrusted`, `witness-mismatch`, `scope-mismatch`, `subject-mismatch`, `identity-replay`, `chain-broken`, or `transcript-contaminated`; policy converts it to a blocking decision and never downgrades to caller-authored JSON.

The verifier first checks that its sealed policy digest equals the snapshot's `witness_policy_sha256`, selects the witness source by expected kind from that policy - the hash-chained hook-transcript store for local kinds, `gh` remote state for remote kinds - rejects an unpermitted source or locator, recomputes the transcript chain digests or re-fetches the remote record, decodes it with the strict decoder, requires exact equality with the stored bytes (or transient presentation bytes), and compares every expected kind/review/dispatch/epoch/fingerprint/subject/`tool_use_id`/`agent_id` field with the returned `VerifiedWitness`. State validation/policy enforce that a witness record, `tool_use_id`, `agent_id`, or remote-run identity is bound to only one canonical review/dispatch/action; re-verifying that same binding during sealing is lawful, but reuse in another scope is replay. Witness-source registration is a composition-root capability, not a path, source, locator, command, or verifier supplied in review state or CLI data.

`next_action()` must have no fallback route. If state is internally inconsistent or any witness needed to treat a current action as complete cannot be verified against its source, return `Decision(False, "blocked", ...)` or let the typed validation/provenance error reach the CLI. If status is blocked, the only lawful action is `resume-review` with blocker-resolution evidence.

For reviewer-backed actions, the recipe exposes the non-null maximum of the portable role floor, sealed review-assignment-policy floor, source-dispatch floor, and assignments currently eligible for that stage, plus its required fresh/distinct provenance. Fast, focused, and strong actions are distinct ordered gates. A missing stage may be vacuously complete only when the coverage plan contains no current obligation eligible for that tier; it may not consume a lower-tier attestation as a substitute. Explicit tests reject fast/low or forked mappers, a challenger below final-strong, self-adjudication, and a repair verifier that shares prohibited source/repair provenance.

Before returning `seal-green`, policy re-runs `verify_evidence_files()` for every green evidence ID and re-verifies every authority-discovery, command-execution, profile-resolution, launch, completion, ready-transition, and stored remote-observation witness used by a predicate with its full review/dispatch/epoch/fingerprint scope, plus transcript-chain integrity end to end. It requires the exact complete sealed local-check policy item set and matching sealed command-execution policy. Each command witness binds the policy item, argv/command bytes, clean-tree working directory, snapshot head/tree, executable/interpreter/script/module/toolchain and allowlisted environment digest, equal pre/post source digests, complete process-tree termination, exit/timing identity, and output digest. A dirty or mutable checkout or a surviving descendant blocks. A hosted check binds the full repository/PR/snapshot/policy/empty-feedback identity and exact policy-item/app/workflow ID/path/definition ref/SHA/event/trigger subject/policy inputs/configuration/check-run/workflow-run/attempt/head identity through a remote-observation witness, never a command witness. Plan 1 proves generic structural/verifier failure only; Task 0 must first prove the hook-transcript and `gh` witness surfaces, Plan 2 owns live per-root/per-edge omission fixtures, Plan 4 owns hostile-command runner fixtures and live dispatch/command witnesses, and Plan 6 owns live multi-attempt/unauthorized-trigger selection fixtures. `seal-green` binds all verified witness-record digests and separate canonical coverage/findings/repairs/reviews/checks digests plus the witness-chain head; `repairs_sha256` covers every repair intent, invalidation cut, replacement set, status, and verifier attestation. It writes a candidate seal and advances to `green-candidate`. `evaluate_green(..., policies=..., now=...)` rechecks owned bytes and witnesses plus separately fresh strict remote-observation bytes and 60-second age without mutating state. Plan 1 tests use a fixed clock and test-only policy bundle only after Task 0 proves the witness floor; until live witness sources exist, the experimental CLI blocks witness-dependent completion/sealing rather than accepting local JSON.

- [x] **Step 3: Implement stage predicates**

Implement named pure predicates:

```text
has_current_snapshot
authority_manifest_complete
authorities_complete
impact_maps_complete
coverage_plan_covers_map_union
scope_challenge_complete
coverage_complete
preflight_current_and_green
fast_reviews_complete
focused_reviews_complete
strong_reviews_complete
all_findings_closed
review_repairs_current_and_verified
blind_final_current_and_clean
closure_audit_current_and_clean
remote_ci_candidate_current
remote_ci_current_and_green
remote_identity_matches
presentation_observation_matches_candidate
witnesses_verified
```

Every predicate returns `(bool, tuple[str, ...])`. `evaluate_green()` concatenates missing reasons from all predicates instead of stopping at the first one.

`authority_manifest_complete()` recomputes the canonical typed manifest-payload digest and requires a discovery witness whose subject binds that exact digest plus the complete canonical snapshot subject/fingerprint and externally rooted discovery, feedback-history, review-assignment, command-execution, local-check, evidence-ingestion, hypothesis, and witness-policy source identities, versions, and digests. The transcript-witnessed discovery session must traverse every authority root/typed edge and enumerate policy-complete actionable feedback history before verification succeeds. A policy edit in the reviewed head is data and cannot govern this run. `authorities_complete()` requires an exact discriminated match between manifest entries and current records, every expected record loaded, and the exact typed unresolved-feedback subset empty. Every actionable feedback-history item, including already-resolved items seen at initial freeze, also has a durable feedback finding; provider resolution alone does not close it. Neither predicate can be satisfied by a caller-authored smaller set, an unreadable authority with a fabricated source hash, a self-qualified policy, a genuine witness from another review/snapshot, or witness-shaped local evidence.

`impact_maps_complete()` requires exactly one current map for each independent mapper role. It validates structured entries and computes their surface/category/consequence/hazard union itself; `normalize_consequences()` discards `none` whenever any substantive consequence exists and otherwise returns exactly `none`, in closed-vocabulary order. Caller-provided counts or summaries are never authoritative. `coverage_plan_covers_map_union()` requires an obligation for every surface/category pair and propagation of normalized consequences before challenge dispatch. `scope_challenge_complete()` requires a current challenger attestation assigned both map evidence IDs and a current coverage inventory that references that attestation and contains every mapped surface, normalized consequence, and hazard. The challenger may add but cannot remove or weaken map entries; replacing `none` with a substantive consequence is explicitly strengthening. Any additions plus complete revised obligation and deterministically derived hypothesis sets are accepted in the same transition. Add a transition test where one mapper returns `none` and the other `security`; the lawful inventory contains only `security`.

`coverage_complete()` validates obligations against the final challenged coverage inventory, not against either mapper's potentially smaller set. It requires every inventory surface to have every universal category and typed consequence from the design contract, derives scope plus risk/consequence capability/reasoning floors, and rejects zero assignees. The snapshot-bound hypothesis policy deterministically derives first-class epoch-namespaced assignment records; every high-risk obligation has an opposite-polarity pair in one family and two strong reviews from distinct profile contracts, dispatches, and fresh contexts. Dispatch IDs must resolve those records and `coverage_sha256` binds their canonical subjects. `not-applicable` additionally requires concrete current counter-evidence and a lawful obligation result; for high risk, a separate distinct-contract final-strong `exemption-challenger` must return `not-applicable-confirmed`. Missing profiles block, and cloned runs or changed free-form hashes fail. An empty tier is vacuously complete only when no inventory-derived obligation is assigned there and no exemption was used to erase it. `fast_reviews_complete()`, `focused_reviews_complete()`, and `strong_reviews_complete()` each require every assignment scheduled at that exact policy tier to have a witnessed attestation at or above its floor; a stronger profile may serve an assignment but does not permit skipping its ordered stage. A fast/focused attestation cannot satisfy a broader or higher-risk obligation. Whole-PR obligations are satisfied only by final and closure `covered` results backed by newly resolved role-specific `final-strong` profiles and launch/completion witnesses; `not-applicable` is invalid for those roles.

Implement the design-spec floor table as a pure function over the obligation's closed `scope_level`, `risk`, and non-empty `consequences` tuple. Test every scope/risk pair plus every consequence vocabulary value; hazard prose is never parsed as policy. The result is the maximum applicable tier, with normalized reasoning `low`, `standard`, `high`, or `final-strong` respectively. Repository policy may raise the result but any attempted lowering is a validation error.

- [x] **Step 4: Implement finding closure rules**

`all_findings_closed()` rejects every `open`, `fixing`, `review-repairing`, `deferred`, `contested`, `unassessed`, or `accepted-risk` finding regardless of severity. It validates disposition proof:

- `fixing`: fix SHA, publication evidence, and an exact replacement snapshot/authority manifest installed atomically; still unresolved;
- `fixed`: the same publication/replacement identity plus current targeted-check evidence, witnessed fix-review evidence, and the current impacted obligation IDs they cover;
- `review-repaired`: confirmed review-process adjudication, same-snapshot repair intent/invalidation cut, current replacement record IDs, and witnessed independent repair-verifier evidence;
- `false-positive`: witnessed adjudication plus counter-evidence;
- `accepted-risk`: durable human decision evidence, followed by `reviewed-with-exceptions`; it never satisfies the green predicate.

Regression relationships are ordinary findings with `regression_of`; resolving them closes them without deleting their history.

An open finding first requires `adjudicate-findings`. A confirmed candidate change uses `enter-fixing` to atomically advance to the published replacement snapshot; it cannot claim `fixed` in the discovery epoch. That transition invalidates current maps, inventory, obligation attestations, checks, final/closure, CI, and seal. `next_action()` returns impact mapping, then forces every applicable fast, focused, and strong tier to re-ascend. Only after separate `run-fix-verification` and `review-fix` actions have stored current proof may `close-fixed` consume those IDs without changing the epoch. A confirmed review-process defect instead uses `enter-review-repair` with no snapshot change, invalidates the deterministic target/downstream cut, re-runs the earliest missing gates, then requires separate `verify-review-repair` proof before `close-review-repaired`. Both closure paths force final and closure afresh. `close-false-positive` and `accept-risk` are non-replacement branches with their own exact payloads. No close action may create its own adjudication, check, review, publication, replacement, or repair-verification proof.

There is no round cap that permits green or discards work. A configured resource cap may return `blocked` with the remaining obligations/findings and required escalation evidence.

- [x] **Step 5: Implement blocking and lawful resume**

`block_review()` rejects creation when another blocker is active and records the exact blocker ID, class, reason, evidence IDs, epoch, fingerprint, and opened sequence. `resume_review()` requires that exact sole active ID plus non-empty current `resolution_evidence_ids`; it atomically records those IDs, resolution epoch/fingerprint, and closed sequence before restoring `status: active`. Missing/wrong/stale evidence, toggling `active` directly, or multiple active blockers fails validation. `next_action()` then recomputes predicates; recovered authority/drift routes to `refresh-review-input`. Add exhaustive zero/one/two-blocker and wrong-ID resume tests. There is no hard-coded `blocked -> blocked` terminal transition.

- [x] **Step 6: Run policy and invariant tests**

```powershell
py -3 -m pytest -q --junitxml="$irReviewScratch/task-4-tests.xml" codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_policy_v2.py codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests/test_review_invariants_v2.py
```

Expected: PASS, including every remove-one-predicate green test.

- [x] **Step 7: Verify and persist the Task 4 recovery checkpoint**

Run `git diff --check`, confirm policy/invariant tests are green, then execute the global task-boundary recovery recipe with label `task-4` and hash `task-4-tests.xml`. Verify the zip contains the untracked policy/tests. Do not commit while the public CLI and full focused suite remain incomplete.

- [x] **Step 8: Mark Task 4 complete in this plan**

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
- Produces the exact composition/transaction API below. Each mutation uses one `locked_state_transaction`, operates on its candidate, and calls `commit()` exactly once after validation. Reviewer dispatch and ready-transition flows each persist intent, then the witnessed call, then the reconciled outcome in separate durable transactions so no external side effect can predate its recoverable intent.
- Produces: public CLI commands `init`, `status`, `next`, `dispatch`, `complete`, `block`, `resume`, and `validate`; an explicit legacy boundary that cannot treat version-1 state or metrics as version-2 evidence. `init` is this plan's name for the spec's `reviewctl start` verb; the state contract and lifecycle semantics remain normative, and the command creates the validated generation-0 intake state.
- Does not produce: `present`, a remote-observation CLI input, or any reviewed-SHA proof. Plan 6 owns the live connector fetch and presentation command.

```python
@dataclass(frozen=True)
class EvidenceSource:
    alias: str
    kind: str
    path: Path

@dataclass(frozen=True)
class TrustedActionPayload:
    raw_data: bytes
    evidence_sources: tuple[EvidenceSource, ...]

class AuthorityDiscoverySource(Protocol):
    def acquire(self, *, action: str, current_snapshot: dict | None) -> TrustedActionPayload: ...

class ReviewerDispatchSource(Protocol):
    def resolve_profile(self, *, action: str, recipe: ActionRecipe) -> TrustedActionPayload: ...
    def launch(self, *, dispatch: dict) -> TrustedActionPayload: ...
    def collect(self, *, dispatch: dict) -> TrustedActionPayload: ...

class CommandRunnerSource(Protocol):
    def run(self, *, action: str, command_intent: dict) -> TrustedActionPayload: ...

class RemoteTransitionSource(Protocol):
    def observe_lifecycle(self, *, intent: dict) -> TrustedActionPayload: ...
    def apply_or_confirm_ready(self, *, intent: dict) -> TrustedActionPayload: ...

class RemoteObserverSource(Protocol):
    def observe(self, *, action: str, snapshot: dict) -> TrustedActionPayload: ...

@dataclass(frozen=True)
class WitnessSources:
    policies: PolicyBundle
    evidence_ingestion_policy: EvidenceIngestionPolicy
    authority_discovery: AuthorityDiscoverySource | None
    reviewer_dispatch: ReviewerDispatchSource | None
    command_runner: CommandRunnerSource | None
    remote_transition: RemoteTransitionSource | None
    remote_observer: RemoteObserverSource | None

@dataclass(frozen=True)
class EngineResult:
    decision: Decision
    generation: int
    state_path: Path

def init_review(
    state_path: Path, *, review_id: str, scratch_dir: Path, apply: bool,
) -> EngineResult: ...
def register_dispatch_transaction(
    state_path: Path, *, action: str, sources: WitnessSources,
) -> EngineResult: ...
def launch_transaction(
    state_path: Path, *, dispatch_id: str, sources: WitnessSources,
) -> EngineResult: ...
def register_ready_transition_transaction(
    state_path: Path, *, sources: WitnessSources,
) -> EngineResult: ...
def finalize_ready_transition_transaction(
    state_path: Path, *, ready_transition_id: str, sources: WitnessSources,
) -> EngineResult: ...
def complete_transaction(
    state_path: Path, *, action: str, caller_data_bytes: bytes,
    caller_evidence: tuple[EvidenceSource, ...], sources: WitnessSources,
) -> EngineResult: ...
def block_transaction(
    state_path: Path, *, blocker_class: str, reason: str,
    evidence: tuple[EvidenceSource, ...], sources: WitnessSources,
) -> EngineResult: ...
def resume_transaction(
    state_path: Path, *, blocker_id: str,
    resolution_evidence: tuple[EvidenceSource, ...], sources: WitnessSources,
) -> EngineResult: ...
```

Each live witness-source method returns exact `raw_data` bytes plus evidence sources. The engine first uses `strict_json_loads()`, derives `EvidenceIngestionContext` and the exact source allowlist from that tuple, and never unions it with caller paths. The dispatch source's launch/collection payload must include the complete ordered tool-call transcript segment bound to the dispatch's `agent_id`; blind-review calls that read denied namespaces are caught by the post-completion transcript audit and invalidate the review before report acceptance. For provenance-bearing fields, `caller_data_bytes` must be the canonical empty object, caller evidence must be empty, and a missing source returns `Decision(False, "blocked", missing=("missing-witness-source:<kind>",))`. Engine errors use stable model/store/witness codes and leave persisted bytes unchanged.

The `dispatch` CLI handler sequences two durable phases: `register_dispatch_transaction` persists the pending dispatch and resolved profile identity; then the source launch plus `launch_transaction` verifies and stores the witnessed `run_subagent` call (transcript `tool_use_id`, verbatim task bytes, profile name). Completion later verifies the launch/completion transcript pair and ordered tool-call digest. The `complete --action mark-ready-for-ci` handler mirrors that pattern with `register_ready_transition_transaction` and `finalize_ready_transition_transaction`. It observes prior lifecycle before registering the exact intent, and finalization accepts either a witnessed performed transition or a verified already-ready no-op for the same idempotency key and head. A crash leaves a visible pending record at the last durable phase; retry is idempotent for the same intent and rejects an unrelated remote state or replay.

- [x] **Step 1: Write CLI contract tests before implementation**

Test exact behavior:

```text
reviewctl.py --help exits 0 and labels version 2 experimental until cutover
reviewctl.py --check exits 0 without files
init defaults to check and requires --apply to create version-2 state
status and next are read-only
dispatch, complete, block, and resume require --apply
usage errors exit 2
validation, stale evidence, and unlawful transitions exit 1
--json emits one JSON object and no prose
complete seal-green re-evaluates every candidate predicate and cannot accept a caller-supplied verdict
no present subcommand exists before Plan 6
no CLI command accepts a remote-observation file or emits a reviewed-SHA proof
arbitrary observation files can exercise only the pure evaluate_green fixture API and cannot produce presentation proof
no CLI option accepts a caller-supplied witness record, witness verifier, profile authority, or authority-discovery manifest as trusted provenance
reviewer completion and sealing block with a typed missing-witness-source result until Plans 2/4/6 wire live sources
mark-ready-for-ci is present in the version-2 vocabulary but blocks without Plan 6's witnessed remote-transition path
ready transition persists intent then the witnessed `gh` call before remote mutation settles, recovers after crash, and verifies initially-ready no-op against the same idempotency key/head
every JSON file and witness/report/observation payload rejects duplicate keys before canonicalization
any failed individual dispatch/ready/complete/block/resume transaction leaves review-state bytes unchanged; a multi-phase command retains only its earlier successfully committed phases
concurrent stale completion cannot erase a finding or overwrite a newer generation
evidence aliases are resolved before record validation and never survive in persisted state
```

- [x] **Step 2: Implement thin command handlers**

Every handler should read exact bytes/paths, pass JSON bytes through `strict_json_loads()`, call one `review_core.engine` transaction or pure policy function, and render the result. Do not duplicate transaction order or policy in the CLI. Mutation commands accept `--data-file` and repeated `--evidence-file alias=kind=absolute-path`; they never accept shell-embedded JSON. Evidence files are untrusted sources to ingest, not provenance. Plan 1 exposes no flag for local witness/manifest/policy trust; its witness sources are fail-closed until later plans inject the live hook-transcript and `gh` sources through the internal engine composition root.

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

For subagent-backed actions, `next` returns the dispatch command first. `dispatch` records the exact role, assignments, tool requirements, context-package/hazard-framing evidence, and canonical resolved profile identity before launch. It commits the pending dispatch first; only then may the witnessed `run_subagent` call launch the agent. Completion requires transcript-verified launch and completion witnesses bound to that prior dispatch, context, and exact raw output. There is no completion path that creates its dispatch or witnesses retroactively, and no local JSON fallback when the hook transcript cannot supply them.

- [x] **Step 3: Make legacy boundaries explicit**

Update `next_node.py` so it detects `schema_version`:

- version 2 exits `1` with `BLOCKED: version-2 state is controlled only by reviewctl.py` rather than becoming a second mutation or routing surface;
- absent/version 1 uses the existing router only for legacy review continuation;
- `ready` on version 1 prints `BLOCKED: version-1 review state cannot produce a trustworthy-green seal; start a version-2 review` and exits `1`;
- `--metrics` remains read-only diagnostics and cannot be combined with `--propose`.

The legacy `lens-triage` route correction already landed on main, so no version-1 routing change is needed; keep the existing `test_lens_triage_resolution_skips_fix` contract green. Preserve all other version-1 defects as migration fixtures and document that the legacy graph is review assistance only.

- [x] **Step 4: Prove there is only one version-2 authority**

Add cross-CLI tests proving `next_node.py`, `compile_metrics.py`, and `resolved_ledger.py` cannot mutate a version-2 state file or create a green seal. Version-2 metrics and Markdown rendering are deferred until cutover; Plan 1 does not add parallel report surfaces.

- [x] **Step 5: Run all focused tests**

```powershell
py -3 -m pytest -q --junitxml="$irReviewScratch/task-5-tests.xml" codex-marketplace/plugins/superpowers-plus/skills/iterative-review/tests
```

Expected: PASS, including the already-green `test_lens_triage_resolution_skips_fix` contract and every new false-green regression.

- [x] **Step 6: Run all bundled-script CLI self-checks**

```powershell
$scripts = Get-ChildItem codex-marketplace/plugins/superpowers-plus/skills/iterative-review/scripts -File -Filter '*.py'
foreach ($script in $scripts) { py -3 $script.FullName --help | Out-Null; if ($LASTEXITCODE -ne 0) { throw "$($script.Name) --help failed" }; py -3 $script.FullName --check | Out-Null; if ($LASTEXITCODE -ne 0) { throw "$($script.Name) --check failed" } }
```

Expected: every executable script exits `0` for both commands.

- [x] **Step 7: Verify and persist the complete focused implementation checkpoint**

Run `git diff --check`, confirm the complete focused suite and CLI self-checks are green, then execute the global task-boundary recovery recipe with label `task-5` and hash `task-5-tests.xml`. Verify the zip contains every untracked kernel/CLI/test file. Proceed to Task 6 without committing; the generated installed copy is still stale.

- [x] **Step 8: Mark Task 5 complete in this plan**

Change every Task 5 checkbox to `[x]` in the working tree. Task 6 will stage it with regenerated surfaces and pass it through the pre-commit hook's canonical gate.

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

Remove claims that `next_node.py` alone makes invalid moves impossible. The under-500-word control-plane rewrite belongs to Plan 7 after every witness source exists.

- [ ] **Step 3: Update the graph reference**

Label current node recipes `version 1 - legacy assistance`. Add the version-2 target graph and scope-to-reasoning ladder from the design spec. Mark snapshot, authority, impact maps, scope challenge, tiered reviewer attestations, role-profile final-strong final/closure, exact-SHA CI, and presentation recheck as required evidence gates. Do not delete version-1 recipes until the final cutover plan.

- [ ] **Step 4: Update implementation progress before regeneration**

Mark completed Plan 1 boxes `[x]`, but leave Task 6 publication boxes open. Do not mark the roadmap item done or invent publication identifiers before they exist. Do not mark Plans 2-7 ready.

- [ ] **Step 5: Check source and overlay health before regeneration**

```powershell
py -3 tools/run.py installed-skills --check
```

This resolves the `inventory`, `marketplace`, and `installed-skills` checks and proves the canonical source and generated installed overlay are not already drifted without rewriting them. Expected: PASS.

- [ ] **Step 6: Regenerate marketplace and mesh surfaces**

```powershell
py -3 tools/run.py marketplace --apply
py -3 tools/run.py mesh --apply
```

Expected: installed skill and indexes update from canonical source without manual edits.

- [ ] **Step 7: Stage the full intended tree**

```powershell
git add codex-marketplace/plugins/superpowers-plus/skills/iterative-review .agents/skills/iterative-review .agents/skills/INDEX.md .agents/plans/iterative-review-trustworthy-green .agents/specs/2026-08-21-trustworthy-iterative-review-design.md .agents/specs/2026-09-12-iterative-review-calibrated-green-design.md INDEX.md INDEX.json .agents/INDEX.md .agents/plans/INDEX.md .agents/plans/INDEX.json .agents/specs/INDEX.md .agents/specs/INDEX.json .agents/plugins/INDEX.md .agents/plugins/INDEX.json .agents/plugins/marketplace.json codex-marketplace/INDEX.md codex-marketplace/INDEX.json codex-marketplace/manifest.json codex-marketplace/plugins/INDEX.md codex-marketplace/plugins/INDEX.json codex-marketplace/plugins/superpowers-plus/INDEX.md codex-marketplace/plugins/superpowers-plus/skills/INDEX.md
git diff --cached --check
```

Expected: the staged tree contains every canonical, generated, and tracking change together. Do not run `py -3 tools/run.py ci --check` here; the commit in Step 8 invokes the tracked pre-commit hook, which materializes the staged snapshot, runs `ci --apply`, stages the owned generated surfaces, and runs `ci --check --diagnostics` as the single complete local gate. Never bypass the hook with `--no-verify`.

- [ ] **Step 8: Commit, push, and update the one draft pull request**

```powershell
git commit -m "feat(iterative-review): add fail-closed evidence kernel"
git push -u origin codex/iterative-review-evidence-kernel
```

Then update the draft PR created by Task 0. If no open PR exists for the exact head branch, create it once; if more than one exists, block instead of guessing:

```powershell
$irPlanPrs = @(gh pr list --state open --head codex/iterative-review-evidence-kernel --json number,url | ConvertFrom-Json)
if ($irPlanPrs.Count -gt 1) { throw 'multiple open Plan 1 PRs' }
$irPlanBody = "Implements Plan 1 of the Trustworthy Iterative Review epic.`n`nAdds the version-2 evidence kernel and regression boundary. The version-2 workflow is not cut over; Plans 2-7 remain required before claiming trustworthy green.`n`nValidation: focused iterative-review tests and the pre-commit hook's staged-snapshot canonical gate."
if ($irPlanPrs.Count -eq 0) {
  gh pr create --draft --base main --head codex/iterative-review-evidence-kernel --title "feat(iterative-review): add fail-closed evidence kernel" --body $irPlanBody
} else {
  gh pr edit $irPlanPrs[0].number --title "feat(iterative-review): add fail-closed evidence kernel" --body $irPlanBody
}
```

- [ ] **Step 9: Record publication evidence and mark Task 6 complete**

Keep roadmap Plan 1 at `executing`. Run the plan-readiness gate and report its rating in the current handoff without persisting it. Mark every Task 6 checkbox, including this one, `[x]`; stage the plan and roadmap; commit and push the tracking update, letting the pre-commit hook run the canonical gate on the staged snapshot. Verify publication from GitHub and keep the pull request draft.

Return the PR URL, branch, full final remote head SHA, implementation commit SHA, focused test result, pre-commit hook gate result, and remaining roadmap gate. Report implementation as ready for review, not roadmap-done; move Plan 1 to `done` only after the PR lands and repository state proves it.

## Plan-readiness self-review

- Spec coverage: Plan 1 first proves the Devin witness-capability floor is present, then implements strict validation and pure lifecycle/predicate semantics over synthetic witness records. Live snapshot/authority acquisition, provider-specific traversal, impact/coverage generation, dispatch/command witness capture, finding-workflow integration, remote attempt selection/presentation, and frontier-calibration benchmarking remain explicitly assigned to Plans 2-7; the Plan 1 CLI blocks those paths without their witness sources.
- Dependency order: Task 0 proves and publishes the live witness floor before synthetic work; Task 1 then declares RED catalogs and minimal malformed fixtures; model constructors precede store; model/store precede the compositional complete candidate and policy; all precede CLI and documentation. No worker must hand-assemble a complete candidate before canonical constructors exist.
- Source custody: canonical source is edited first; Task 0 publishes its capability reference with generated projections, and Task 6 regenerates/stages them again after the kernel and documentation changes. One draft PR is opened/reused throughout Plan 1.
- Interim state: version-2 APIs exist behind `reviewctl.py`; the current skill is not cut over and cannot claim version-2 green during this plan.
- Validation: focused tests, CLI contracts, the `installed-skills --check` source/overlay check, marketplace regeneration, mesh regeneration, the pre-commit hook's staged-snapshot `ci --apply` plus `ci --check --diagnostics` gate, and draft PR publication are explicit. No `ci --check` runs immediately before a normal commit.
- Handoff-gates: the plan-readiness rating is reported in the execution handoff, not persisted here. Re-gated 2026-09-12 after the witnessed-evidence pivot (hook-transcript and `gh` witnesses replace receipt envelopes, challenges, issuer namespaces, and sandbox confinement; Task 0 is a capability floor producing `PASS`/`INERT`, not a terminal `BLOCKED`; the skill is Devin-only and inert elsewhere). Dependencies are producer-before-consumer; the capability floor precedes synthetic proof; every task has explicit inputs/outputs and tracking; the temporary RED interval is local and non-publishable; canonical source and generated overlay are staged together at both publication boundaries; focused checks, the hook gate, one reused draft PR, and exact return evidence are named. Provider-specific traversal and attempt-selection proofs remain with their live-witness plans rather than being faked in the kernel.
