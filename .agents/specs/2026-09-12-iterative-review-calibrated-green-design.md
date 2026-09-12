# Trustworthy Iterative Review - Calibrated-Green Design (v2)

Status: normative successor to `2026-08-21-trustworthy-iterative-review-design.md` for all epic work after the 2026-09-12 harness spike. The prior spec's state contract, coverage model, finding lifecycle, and remote/CI semantics carry over unless a section here explicitly narrows or replaces them. Its receipt-envelope, trusted-adapter, challenge, and confined-runner machinery is removed.

## Product claim and scope

`iterative-review` is a Devin Desktop workflow for converging a draft pull request to the point where the cloud frontier reviewer (run on ready-for-review flip, usage permitting) finds no new material issues. Local `green` is a **calibrated prediction** of the frontier verdict, not a security seal. When frontier review is unavailable, local green is the sole gate and its published miss rate is the honest confidence statement.

Target harness: Devin Desktop only. The skill is **inert on every other harness** (Codex, generic OpenAI-compatible runners): the entry gate detects the harness, reports "iterative-review requires Devin Desktop subagent/hook surfaces," and stops. No adapter or capability-abstraction layer exists.

## Threat model

Agents are assumed honest-but-fallible, not malicious. The failure modes defended against are accidents and blind spots:

1. **Recall failure** - a weaker reviewer reports clean without covering a risky surface.
2. **Bookkeeping rot** - ledger/metrics/graph state drifts from what actually happened.
3. **Hollow claims** - "ran checks," "reviewed file," "resolved" asserted without the work occurring.
4. **Contamination** - a blind or independent role consuming prior conclusions instead of forming its own.
5. **Staleness** - green asserted on a snapshot other than what ships.
6. **Audit-trail erosion** - evidence that quietly rewrites itself after the fact.

The defense is **witnessed evidence**: every load-bearing action must leave a record emitted by the harness outside the model's control (the lifecycle-hook transcript), plus genuinely external records where they exist (GitHub check-runs, workflow runs, PR lifecycle). Forgery is possible only by editing a hash-chained log whose head is anchored into the pushed commit; it is **tamper-evident, not tamper-proof**. The honest claim: "complete, witnessed, independently checkable."

## Witness model

The harness emits a per-tool-call transcript via lifecycle hooks. PreToolUse captures `tool_name`, full `tool_input`, `tool_use_id`, `session_id`, `prompt_id`; PostToolUse adds the full `tool_response`. Subagent calls fire the same hooks. A review session appends every relevant event to an append-only JSONL **witness log** under the review-owned scratch store; each entry carries `record_sha256 = sha256(previous_record_sha256 + canonical entry bytes)`, forming a hash chain. The green seal binds the chain head, and the seal lands in the pushed commit - the external anchor.

A **witness record** in review state is a typed reference into that log plus the digests that make it checkable: `witness_id`, `kind`, `tool_use_id` or `agent_id`, `subject_sha256`, `transcript_range`/`record_positions`, `chain_head_at_record`, `snapshot_epoch`, `snapshot_fingerprint`. The verifier confirms the referenced entries exist at those positions, hash-match, chain correctly, and carry harness-assigned (never caller-chosen) IDs.

The closed `kind` vocabulary: `authority-discovery`, `profile-resolution`, `review-launch`, `review-completion`, `command-execution`, `remote-transition`, `remote-observation`, `human-decision`. (Plan 1 implements this vocabulary; the earlier draft's `dispatch-launch`/`dispatch-completion` names are realized as `review-launch`/`review-completion`, `profile-resolution` was added for route-selection proof, and `tool-transcript` exists as an evidence kind rather than a witness kind.)

- `review-launch`/`review-completion`: the PreToolUse/PostToolUse pair for one `run_subagent` call. The launch record binds exact task bytes and profile; the completion record binds the verbatim returned output and `agent_id`.
- `profile-resolution`: the route-selection record binding required role, tier, and reasoning floor to the selected user-global profile.
- `tool-transcript` (evidence kind, not a witness kind): ordered digest over every tool call a dispatch made between its launch and completion records. Proves what a reviewer actually touched; Plan 1 ingests it as immutable evidence and relies on the attested `audit_result`, while independent transcript-derived contamination enforcement is deferred to a later plan.
- `command-execution`: an `exec` record plus exit code, output digest, working directory, and pre/post source digests. Engine-witnessed, not sandbox-attested.
- `remote-transition`/`remote-observation`: `gh` call records plus independently re-fetched GitHub state (check-run ids, workflow run/attempt, head_sha, draft flag).
- `authority-discovery`: the transcript digest of the enumeration session plus per-authority content digests.
- `human-decision`: the transcript record of a human question/answer. The workflow for deciding when and how to ask belongs to the `asking-clarifying-questions` skill - iterative-review defers to it rather than encoding its own question policy; the `ask_user_question` tool's recorded call and response are what the witness binds, since the response carries the user's actual selection which the agent cannot fabricate in-band.

`read_subagent(agent_id)` provides a second harness-held re-read of completion output for cross-checking the recorded bytes.

## Storage and custody

Two distinct artifacts, both scratch-disposable:

- **Raw transcript** - the hooks pack is installed once (project `.devin/hooks.v1.json` or user-level) and is deliberately dumb: it appends every Pre/PostToolUse record to a session-keyed file at `<scratch-root>/<repo>/<branch>/transcripts/<session_id>.jsonl`. It knows nothing about reviews. The `session_id` field in each record is the correlation key.
- **Review witness store** - under the review's `scratch_dir`, resolved to the canonical off-repo scratch root (`<scratch-root>/<repo>/<branch>/reviews/<review-id>/`). Contains `witness-store/` (the chained JSONL log the engine ingests transcript segments into) alongside `evidence-store/` and `review-state.json`. Witness records in state point into this store; each stored entry also records its source transcript file and positions so a segment can be re-ingested if needed.

Custody lifecycle: both artifacts are scratch and may be deleted at any time - during review they are the audit substrate, after green they are optional retention. The only durable artifact is the seal: `seal-green` binds the witness chain head into the seal record, which lands in the pushed commit. Deleting the transcript or witness store afterward does not invalidate the seal; it only narrows post-hoc audit to "the recorded chain head matched," which is the honest claim anyway. A review that needs its evidence re-inspected keeps the files; one that is done can shed them.

Consequence for `doctor` and verification: the chain head is the committed anchor, so a verifier re-checking an old seal needs only the seal digest - not the original log bytes - to confirm the sealed state is what was presented.

For the seal to actually be anchored, `seal-green` writes the seal record to a policy-owned repository path that must be committed inside the reviewed head - the pushed commit is what makes the chain head durable. The in-scratch witness store is the working copy; the committed seal artifact is the anchor.

## Capability floor (entry gate)

`reviewctl doctor` (the harness capability check, replacing the old capability gate) must pass before a review may start. It verifies live:

1. The review session's hooks pack (`.devin/hooks.v1.json` project-level or user-level) is installed and emitting records for orchestrator **and** subagent calls, and subagent records are discoverable for ingestion - either sharing the parent `session_id` or correlating through the dispatch's `agent_id`/`prompt_id`.
2. A smoke dispatch proves `allowed-tools` confinement: a probe profile must be denied a canary read by the policy hook and/or permission deny, and its tool list must match its frontmatter.
3. `gh` auth and remote-observation endpoints are reachable.
4. Required subagent profiles exist with pinned `model:` and correct `allowed-tools`.
5. The review-owned store and witness log can be created with private permissions.

`doctor` failing any check makes the skill inert for that session - it reports the missing capability and stops rather than degrading silently.

## Version-2 state contract

The top-level object retains the prior spec's shape with witness substitutions. Exactly these keys:

```json
{
  "schema_version": 2,
  "review_id": "review-uuid",
  "generation": 0,
  "status": "active",
  "stage": "intake",
  "scratch_dir": "<scratch-root>/<repo>/<branch>/reviews/<review-id>",
  "snapshot": null,
  "content_objects": {},
  "evidence": {},
  "authorities": {},
  "authority_manifest": null,
  "impact_maps": {},
  "coverage_inventory": null,
  "obligations": {},
  "hypothesis_assignments": {},
  "dispatches": {},
  "reviews": {},
  "route_selections": {},
  "witness_records": {},
  "findings": {},
  "review_repairs": {},
  "checks": {},
  "ready_transition": null,
  "ci_candidate": null,
  "calibration": null,
  "blockers": {},
  "green_seal": null,
  "history": []
}
```

`status` is `active`, `blocked`, or `reviewed-with-exceptions`. `stage` is derived, never asserted. `calibration` holds the rolling frontier-feedback state (below). All prior record requirements, projection allowlists, epoch/fingerprint binding rules, unique-ID rules, and the strict `additionalProperties: false` contract carry over unchanged except that every field formerly named `*_receipt_id`, `challenge_id`, `execution_id`, or `envelope_evidence_id` is replaced by the corresponding `*_witness_id` or `witness` fields defined per record below:

| Record | Changed fields (vs prior spec) |
|---|---|
| Authority manifest | `discovery_witness_id` replaces `discovery_receipt_id` |
| Dispatch | drops `launch_challenge_id`, `launch_receipt_id`; adds `launch_witness_id`, `completion_witness_id` (nullable until reported), `agent_id`, `tool_use_id`, `transcript_sha256` |
| Review | `completion_witness_id` replaces `completion_receipt_id`; adds `audit_result` (`clean`, `contaminated`, `incomplete`) |
| Witness record | new record type as defined above |
| Local check | `execution_witness_id` replaces `execution_receipt_id` |
| Hosted check | `remote_observation_witness_id` replaces `remote_observation_receipt_id` |
| Ready transition | `transition_witness_id` replaces `transition_receipt_id`; drops `challenge_id`/`execution_id` |
| Calibration | new: `frontier_runs` counter, `misses` by taxonomy class, `last_sample_sha`, `last_sample_at`, `sample_ids` |

No field may carry caller-minted identity where the harness assigns one (`tool_use_id`, `agent_id`, check-run ids): the verifier requires the harness-side value.

## Independence and confinement

Declared + audited, not enforced isolation:

- Reviewer profiles carry `allowed-tools` in frontmatter. Blind and independent roles get read/search tools only - never `exec`, `write`, `edit`, `webfetch`, MCP, or subagent tools. The harness strips unlisted tools at the function surface; unknown names grant nothing.
- Project/user permission `deny` rules and a policy PreToolUse hook forbid reads of review-internal paths (state, ledgers, prior reports, feedback artifacts) for review-internal path patterns. A deny that fires aborts the dispatch - treated as `incomplete`, never green.
- The blind role contract says exactly what it may see; the dispatch task must not smuggle prior findings (the launch record's task bytes are auditable for this).
- Post-completion audit reads the `tool-transcript` evidence: any touched path outside the role's allowlisted namespaces marks the review `contaminated`, which invalidates it (fail-closed) and opens a `review-process` finding against the environment, not the agent. Plan 1 records the audit result the completing attestation carries; deriving contamination independently from the transcript is deferred to a later plan.
- Fresh-context and role-contract-distinctness rules from the prior spec stand: exemption, blind-final, closure, and repair-verifier dispatches are resolved fresh per launch; a review-sourced finding's adjudicator differs in execution and realized role contract.

## Checks

- **Local checks** are engine-witnessed: `reviewctl` materializes the reviewed tree into a review-owned clean copy, records argv/cwd/environment digest, pre/post source digests, exit code, and output digest; the `command-execution` witness binds them. There is no sandbox claim on Windows; commands that need credential/network isolation do not run locally - hosted CI is their gate.
- **Hosted checks** use the prior spec's GitHub identity requirements unchanged: app/workflow-definition/trigger/input/check-run/run-attempt identity, authoritative attempt on the exact reviewed SHA, re-fetched remotely.
- A non-success required check deterministically creates a check-sourced finding in the same transaction.

## Finding lifecycle

Unchanged from the prior spec: `adjudicate-findings`, `close-false-positive`, `enter-fixing` (new epoch), `run-fix-verification`, `review-fix`, `close-fixed`, `enter-review-repair` (same-snapshot invalidation cut), `verify-review-repair`, `close-review-repaired`, `accept-risk`, `contested`. `accepted-risk` requires a `human-decision` witness and yields `reviewed-with-exceptions`, never green. All severities, including `minor`, must be closed before green.

## Final review, remote gate, presentation

- **Blind final** and **closure audit** run on the same final snapshot through separately witnessed dispatches with fresh resolution. The blind final is the local stand-in for the cloud frontier reviewer.
- `mark-ready-for-ci` keeps its three-phase shape minus challenge/execution machinery: persist strict intent (idempotency key still derived from canonical intent), witness the `gh pr ready` call, then verify via a `remote-observation` re-fetch that the PR actually left draft on the exact head SHA; a crash leaves a retryable intent reconciled by observation, and an already-ready remote produces a verified no-op.
- Hosted CI on the exact reviewed SHA completes the remote gate; the seal binds repository/PR/head/authority/feedback identity plus the witness chain head.
- `present` is read-only: it re-fetches remote state, re-locks, re-reads state generation and byte digest, re-verifies witness-chain integrity, and emits the proof only on exact match. `reviewed-green` is transient and tied to the presented SHA; stored state never persists green.

## Calibration

Calibration is the product's honest-confidence surface, not a gate on green:

- Each cloud-frontier run on a pushed PR is recorded as a `calibration` sample: provider, run identity, `head_sha`, findings raised, and the local epoch it reviewed.
- Every frontier finding not present in the local ledger is a **miss**, classified by taxonomy: `uncovered-surface`, `weak-lens`, `premature-closure`, `stale-epoch`, `frontier-false-positive`, `new-information`.
- `present` reports calibration health: sample count, miss rate, last sample age. A stale or thin calibration history is shown plainly; it never silently implies confidence.
- Miss records feed the review process itself: each miss is a finding against the loop, so recall improves from real failures.
- A repo or user policy MAY require a tightened local bar (e.g., no `accepted-risk` closures, extra strong pass) when frontier coverage is known-absent for a period.

## Green predicates (revised)

`green-candidate` requires all of the following for one snapshot epoch; each is a pure function over validated state plus the witness log:

1. `authorities_complete` - expected manifest loaded or required-unavailable-blocked.
2. `impact_maps_current` - both maps present for the current epoch.
3. `coverage_complete` - challenged inventory covers the map union; every obligation assigned.
4. `challenge_current` - scope challenge clean for the epoch.
5. `checks_current` - required local checks witnessed successful; hosted checks remotely verified on the SHA.
6. `reviews_current` - every required review has launch + completion witnesses, matching `agent_id`/scope, `audit_result: clean`, verdict known.
7. `findings_clear` - every finding in a closed disposition; none open/fixing/repairing/contested/deferred.
8. `final_current` - blind-final and closure witnesses clean on the epoch.
9. `remote_verified` - remote observation matches repository/PR/head/authority/feedback identity at seal time.

`accepted-risk` findings contribute to `reviewed-with-exceptions` only. `reviewed-green` remains transient-present-time only.

## Action vocabulary

Same lifecycle, simplified payloads: `start-review`, `freeze-review-input`, `run-impact-mapping`, `build-coverage`, `run-scope-challenge`, `run-preflight`, `run-fast-review`, `run-focused-review`, `run-strong-review`, `run-exemption-challenge`, `adjudicate-findings`, `close-false-positive`, `enter-fixing`, `run-fix-verification`, `review-fix`, `close-fixed`, `enter-review-repair`, `verify-review-repair`, `close-review-repaired`, `accept-risk`, `run-blind-final`, `run-closure-audit`, `mark-ready-for-ci`, `record-remote-observation`, `record-frontier-run`, `record-human-decision`, `seal-green-candidate`, `present`, `refresh-review-input`, `block`, `resume`. `reviewctl next` prints one action, required inputs, witness schema, and the completing command.

## Fail-closed graph

Identical topology to the prior spec's mermaid graph with these substitutions: "receipt-verified" becomes "witnessed"; `ready` keeps its three-phase intent/witness/observation shape; the presentation node adds witness-chain re-verification; a new terminal class `inert` covers harness-capability failure at entry.

## Honest limits (normative)

- A motivated orchestrator can forge the witness log before the seal anchors it; the design detects forgery on audit, it does not prevent it. The chain head lands in the pushed commit so post-hoc edits are detectable.
- Permission denies are command-text matched; an `exec`-capable subagent could evade a path deny by indirection - which is why review roles never get `exec`.
- The realized subagent model is self-reported; the `model:` pin is a declared contract, not an attested one.
- Local checks are witnessed, not isolated.
- Calibration measures the local loop against frontier output; if frontier review is weak or absent, green's confidence claim degrades accordingly - say so in presentation.
