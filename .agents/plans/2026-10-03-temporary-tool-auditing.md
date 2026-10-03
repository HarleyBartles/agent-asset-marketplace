# Temporary Tool Auditing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an Agent Capability Pack skill that establishes bounded tool-use evidence in Codex and Devin, with a stable user-wide Codex hook and temporary, renewable recording engagements.

**Architecture:** One Python recorder and evidence model, with focused Codex and Devin adapters. Codex installs one stable user-wide hook definition and dispatcher, approved once, which reads current activation state on every invocation and stays inert outside an active worktree engagement. A durable run manifest separates installation from engagement activation, recording rounds, expiry, and verified disablement/purge; every persisted surface passes through mandatory sanitisation.

**Tech Stack:** Python standard library, pytest, JSON/JSONL, runtime command hooks, existing marketplace builder and tracked Git hook. Support Windows and Linux; no new third-party runtime dependency.

**Spec:** [Approved design](../specs/2026-10-02-temporary-tool-auditing-design.md).

**Execution Strategy:** `executing-plans`. Sanitisation, recorder health, lifecycle transitions, ownership recovery, and assessment share state and require continuity through restarts. The nearest alternative is `subagent-driven-development`, which adds fresh per-task implementation/review contexts at the cost of repeated reconstruction of that state. Use inline sequential implementation with a fresh whole-branch review at completion.

## Global Constraints

- Implement MARK-377 only. No general hook framework, authorisation gate, secret-backed evidence fingerprints, or malicious-agent immutability claim.
- Codex and Devin are supported with explicit runtime differences. Capture all covered agents; select the subject when assessing evidence.
- Codex uses stable user-wide registration in `$CODEX_HOME/hooks.json` (normally `C:/Users/hbart/.codex/hooks.json`) and a dispatcher at a stable user-owned path. Preserve unrelated hooks and require human hook-definition approval. Global hooks do not require project trust: do not add or remove worktree trust solely for auditing. Keep Devin Desktop registration runtime-specific until its global semantics are independently established.
- Record sanitized arguments, identifiers, and observed outcome status by default; full sanitized results are optional and chosen by the agent before observation.
- Default lease is 30 minutes, adjustable with explicit renewal. Expiry never clears cleanup and renewal never fills a capture gap.
- No raw payload spool, secret-bearing config backup, exception dump, or unsanitized diagnostic. Failure or ambiguity prevents a no-tools claim.
- Preserve existing hooks and unrelated configuration changes. Keep the stable Codex dispatcher installed and inert between engagements. At engagement completion disable activation, verify subsequent runtime calls create no records, and purge run logs and run-local recorder copies; retain only a minimal sanitized receipt. Explicit uninstall removes only unchanged owned global entries.
- Scope of the completing slice ends at a fully reviewable Draft PR with verified development-probe teardown. Ready and merge are human-owned subsequent actions.

## Source map and shared contracts

Create `skills/temporary-tool-auditing/SKILL.md`, `agents/openai.yaml`, `references/codex.md`, `references/devin.md`, `references/evidence.md`, and `assets/hooks/{codex,devin-desktop}.json`. Use canonical metadata conventions from neighbouring first-party skills; do not copy generated provenance.

Create these focused modules under `skills/temporary-tool-auditing/scripts/`:

| File | Responsibility and exported interface |
| --- | --- |
| `sanitize.py` | `sanitize(value: object) -> tuple[object, list[str]]`; recursively remove known secret forms and report safe redaction paths. |
| `store.py` | `load_manifest(run: Path) -> dict`, `save_manifest(run: Path, value: dict) -> None`, `create_manifest(...)`, atomic `update_manifest(...)`, `append_record(...)`; locked reads/writes and safe diagnostics. |
| `runtime.py` | `normalize_event(runtime: str, payload: dict, detail: str) -> dict`, `render_handlers(runtime: str, recorder: Path) -> dict`; runtime field/status conversion and absolute interpreter command. |
| `record.py` | `record_event(run: Path, payload: dict, now: float) -> bool`; lease/arming check, sanitisation, normalization, append and health handling; command entry reads stdin. |
| `registration.py` | `install(run: Path, project: Path, runtime: str) -> dict`, `remove(run: Path) -> dict`; owned JSON handler mutation and guarded recovery. |
| `codex_trust.py` | Retire the audit-only Codex project trust path after migrating the global dispatcher; preserve pre-existing user trust and unrelated configuration. |
| `activation.py` | Freshly read activation state per invocation, resolve the exact worktree/run and lease, and atomically enable/disable an engagement without changing hook definitions. |
| `global_registration.py` | Idempotently install the stable user-wide hook and dispatcher, preserve unrelated handlers, and verify owned helper hashes. |
| `assessment.py` | `assess(run: Path, subject: dict) -> dict`; counts and prerequisite/coverage/attribution limits. |
| `auditctl.py` | User CLI, durable transitions, controls, expiry renewal and restart handoffs. |

Tests live under `skills/temporary-tool-auditing/tests/scripts/`; use a local `conftest.py` that adds the scripts directory to test imports. Shared fixtures construct temporary runs/configurations and inject time; they do not invoke paid models. Behaviour cases live under `tests/behavior/` and `tests/pressure/`, with evaluator-only expectations under `tests/evaluator-only/`. Run outputs stay off-repo.

Manifest version 1 contains `run_id`, `runtime`, `runtime_version`, `project_root`, `registration_root`, `subject`, `detail`, `expires_at`, `armed`, `cleanup_required`, `registration_state`, `activation_verified`, `intervals`, `controls`, `health`, and `owned_entries`. Store UTC timestamps and positive finite lease durations. `detail` is `status` or `full-results`. An interval records start/end, detail and expiry boundaries. Controls reference actual captured call IDs and are excluded from scenario counts, never deleted.

Normalized records contain `run_id`, `received_at`, `event`, `session_id`, optional `agent_id`, `turn_id`, `call_id`, `tool_name`, sanitized `arguments`, `outcome_status`, optional sanitized `result`, and `redactions`. Missing IDs are null and invalidate dependent attribution/pairing rather than being manufactured. Outcome status is `observed-unknown`, `success`, `failure`, or `rejected`; use the latter three only when the runtime payload independently establishes them.

CLI: `auditctl.py <operation> --run-dir <absolute-path>`, with `--check` default and `--apply` for mutations. `prepare` additionally requires `--runtime codex|devin-desktop --project <root> --question <text> --subject <session-or-agent-selector> --detail status|full-results`, and accepts `--duration-minutes` default 30 and `--runtime-version`. Devin CLI remains unsupported until its config and correlation contract are verified separately. Provide `--help` at root and operation level. Missing required capabilities return nonzero and safe structured errors. Never put the raw question or exception text into output before sanitisation.

## Review Focus

- Credential patterns in free text, URLs, CLI flags, serialized JSON and common header forms are sanitized before persistence; pattern detection remains best-effort: Task 1 and Task 2.
- Global hook installation preserves unrelated handlers, stays idempotent, and needs no worktree trust; fresh activation reads affect only the selected worktree, expire inert, and cannot redirect writes to an unrelated run: Task 3.
- Interrupted config writes leave discoverable ownership; concurrent installers cannot stack runs. Registration locks live in private user temp storage, not in the project hook directory: Task 3.
- Late outcomes, lease gaps and missing call IDs cannot produce complete no-tools evidence: Task 4.
- Devin interleaving cannot be guessed into child attribution: Task 4.
- Missing activation, lease expiry, disablement, and failed dispatcher health checks cannot make silent recording or cleanup appear verified: Task 5 and Task 6.

### Task 1: Sanitised storage with portable concurrency

**Files:** Create `scripts/sanitize.py`, `scripts/store.py`, `tests/scripts/conftest.py`, `test_sanitize.py`, `test_store.py` within the new skill.

**Interfaces:** Consumes Python standard library only. Produces the `sanitize` and store functions above; safe errors expose codes, never raw payloads.

- [x] Write parametrized tests for API keys, nested password/token/cookie fields, Authorization headers, Basic/Bearer text, private-key blocks, URL userinfo, connection strings, CLI assignments and flags. Inspect persisted bytes and captured diagnostics, not only return dictionaries. Include harmless data preservation and redaction-path reporting.

```python
def test_secret_does_not_reach_persisted_record(tmp_path):
    secret = 'example-password-must-not-persist'
    append_record(tmp_path, 'events', {'arguments': {'password': secret}})
    assert secret.encode() not in (tmp_path / 'events.jsonl').read_bytes()
    assert '[REDACTED]' in (tmp_path / 'events.jsonl').read_text()
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_sanitize.py skills/temporary-tool-auditing/tests/scripts/test_store.py -q`; witness failure before implementation.
- [x] Implement recursive redaction plus bounded text patterns. Centralise sanitisation at persistent-write boundaries. Use OS-specific standard-library file locks (`msvcrt` on Windows, `fcntl` on POSIX), atomic manifest replacement, restrictive creation where supported, bounded lock acquisition, and generic error codes. Lock read/modify/write transactions, not just individual writes. Add subprocess-writer tests proving complete unique records; test lock failure and interrupted atomic replacement preserve readable state.
- [x] Re-run the two suites. Include redaction failures that produce no unsafe partial file. Inspect all written files for fixture secrets.
- [x] Commit `feat: add sanitised audit storage` through the tracked hook. Do not create empty skill scaffolding solely to satisfy an inventory test; add the minimal valid skill metadata required by repository validators with this deliverable.

### Task 2: Runtime adapters and paired event recording

**Files:** Create `scripts/runtime.py`, `scripts/record.py`, `assets/hooks/codex.json`, `assets/hooks/devin-desktop.json`, `tests/scripts/test_record.py`, `test_runtime.py`.

**Interfaces:** Consumes Task 1 storage. Produces `normalize_event`, `render_handlers`, and `record_event`; stdin command accepts `--run-dir`, emits neutral runtime-valid JSON, and never changes tool decisions.

- [x] Add Codex and Devin payload fixtures from observed field shapes using invented non-secret data. Cover Codex child identity, main identity absence, Devin prompt IDs, structured Devin success/failure/error, text-only Codex outcome, and missing correlation fields.

```python
def test_post_event_does_not_imply_success():
    result = normalize_event('codex', {
        'hook_event_name': 'PostToolUse', 'tool_name': 'Bash',
        'tool_use_id': 'call-1', 'tool_response': 'some output'
    }, 'status')
    assert result['outcome_status'] == 'observed-unknown'
    assert 'result' not in result
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_record.py skills/temporary-tool-auditing/tests/scripts/test_runtime.py -q` and witness RED.
- [x] Implement arming and expiry checks before persistence; collect raw fields only in memory, sanitize then normalize/store. Parse failures and write failures emit generic health codes without payload echoes. Supply Codex pre/post/session/subagent events and Devin pre/post/session events. Use absolute recorder/interpreter paths with platform-correct quoting; resolve active interpreter without assuming a shell's `python` alias. Probe unsupported interpreter capabilities before registration.
- [x] Test expiry boundary, disarm, full-results sanitisation, secret-containing malformed stdin, absent outcome status and concurrent invocation. Re-run the suites to GREEN.
- [x] Commit `feat: record runtime audit attempts and outcomes`.

### Task 3: Stable Codex global dispatcher and activation spike

**Files:** Modify `scripts/record.py`, `scripts/runtime.py`, `scripts/auditctl.py`, `tests/scripts/test_record.py`, `test_lifecycle.py`, and `references/codex.md`; create `scripts/activation.py`, `scripts/global_registration.py`, and their tests. Retire Codex audit-only trust mutations in `scripts/codex_trust.py` and their tests when no longer used. All paths are within `skills/temporary-tool-auditing/`.

**Interfaces:** Global installation is idempotent and independent of a run. The dispatcher receives runtime stdin, reads current activation state, matches the runtime `session_id` and exact configured worktree, and invokes only the hash-verified user-global recorder for an active, unexpired run belonging to that session family. Run-local evidence directories are data-only and never supply executable code. Each activation entry contains the parent session ID, worktree path, run ID/directory, detail level, and expiry. Codex documents that subagent hooks carry the parent session ID; preserve available child identifiers for attribution within that family. Reject missing or mismatched selectors before persisting event, health, or control records. The stable global hook may execute across projects, but inactive and unrelated sessions create no audit records. Enable/disable changes activation state without modifying approved hook definitions. Concurrent session families, including two sessions in the same worktree, retain separate activation entries and run identity. Session-family selection happens at capture time; choosing a particular child or parent within that family remains an assessment concern.

- [x] Inspect the current Codex user hook/config state read-only. Confirmed no existing `hooks.json`, no active environment pointer, and reconciled all scratch manifests. One earlier removed project-local probe remains pending its post-restart canary; clear it during the single initial global-hook restart.
- [x] Write behavior tests proving missing activation creates no audit files, unrelated projects and sessions remain unrecorded, two sessions in one worktree stay isolated, matching parent and child events are captured, missing session IDs create no records, expiry disables writes, independent session families can activate without clobbering each other, and repeated install preserves unrelated handlers and creates no duplicates. Reuse interrupted-write/ownership coverage from the existing registration implementation.
- [x] Implement one stable global definition and dispatcher, using an absolute interpreter/script command and generic safe failures. Persist ownership intent before changes; no raw configuration backup. Hash-check stable scripts, refuse unexpected drift, and refresh helpers only when existing owned files still match their recorded hashes and hook definitions are unchanged. Keep logs and run-local assets in the selected run directory, not in a global payload spool. Dispatch executes only the verified CODEX_HOME recorder; run-local paths are data-only.
- [ ] Live-spike the Windows user environment setting: retrieve its current persisted value on each hook invocation, not inherited `os.environ`. The implementation uses an activation registry keyed by parent session and exact worktree, with run ID/directory, detail, and lease. Live proof must demonstrate inactive behavior, activation, positive parent/child controls, isolation, disablement, and no later writes in this Codex process. Never put secrets into the switch or registry.
- [ ] If the fresh Windows registry lookup fails live, use the stable activation-registry fallback and record the observed reason. Other platforms use the stable file directly. Do not add parallel switch frameworks.
- [ ] The global definition is installed once. Obtain human hook review and perform one initial restart if required. After activation succeeds, reuse this installation for every live control and follow-up round. No restart is expected for activation, pause, resume, renewal, or engagement cleanup; prove this.
- [ ] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts -q`, inspect persisted test files and safe diagnostics, and commit through the tracked hook after the selected mechanism is proven. Explicit uninstall remains a separate user-requested operation and is not ordinary engagement cleanup.

### Task 4: Evidence assessment and subject attribution

**Files:** Create `scripts/assessment.py`, `tests/scripts/test_assessment.py`, `references/evidence.md`.

**Interfaces:** Consumes sanitized records and manifest. Produces structured counts, `claim_supported`, and `limitations`; never hides unresolved events. Match by run, subject and call ID; detect duplicates and malformed/truncated records as health limits.

- [x] Test paired attempts/outcomes, unmatched pre/post, controls excluded by captured IDs, no positive control, missing completion, redactions, missing IDs, expiry gaps, child session sharing, and late outcomes. Include Devin serialized boundary attribution versus overlapping dispatches or unidentified parent activity.

```python
def test_missing_control_cannot_prove_no_tools(empty_completed_run):
    result = assess(empty_completed_run, {'session_id': 'session-1'})
    assert result['claim_supported'] is False
    assert 'missing-positive-control' in result['limitations']
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_assessment.py -q` to RED.
- [x] Implement Codex agent-ID attribution and bounded main/session scopes. Devin child scope requires serialized captured dispatch boundaries, no overlapping unidentified producers, and a persisted orchestrator-idle self-attestation; reject ambiguous attribution. Retain late outcomes linked to in-window attempts even if delivered after stop, but do not repair an unobserved gap. Treat controls, runtime coverage and subject completion as prerequisites with evidence references, not free-form claims that silently override captured contradictions.
- [x] Re-run to GREEN. Document statuses and the distinction between no observed attempts within verified coverage and universal no-tool proof.
- [x] Commit `feat: assess bounded tool-use evidence`.

### Task 5: CLI lifecycle, renewable leases and restart recovery

**Files:** Create `scripts/auditctl.py`, `tests/scripts/test_lifecycle.py`, `test_cli.py`; extend manifest fixture support.

**Interfaces:** Consumes Tasks 1-4 functions. Produces the CLI contract above and operations `prepare`, `install`, `status`, `verify`, `start`, `stop`, `renew`, `assess`, `disarm`, `remove`, `verify-teardown`, `purge`.

- [x] Test no mutation under `--check`, default 30 minutes, positive finite durations, explicit renewal, expiry gaps, illegal transitions, interrupted install resume, capture-detail changes only between intervals, and cleanup remaining true after stop/expiry/removal.

```python
def test_expiry_does_not_complete_cleanup(expired_run):
    state = cli_status(expired_run)
    assert state['recording_state'] == 'expired'
    assert state['cleanup_required'] is True
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_lifecycle.py skills/temporary-tool-auditing/tests/scripts/test_cli.py -q` to RED.
- [ ] Revise durable transitions for stable global installation. `verify` binds a captured runtime control to the exact active run; `start` requires verified coverage; `stop` closes a recording round while retaining the engagement for assessment and follow-up. `renew` preserves the default 30-minute adjustable lease and never repairs gaps. Final engagement cleanup disables its activation entry, performs a healthy dispatcher control plus a runtime canary proving no records were appended, then purges event/health/control logs and run-local assets. Keep cleanup pending on failed disablement, unavailable runtime, or failed purge. Do not require global hook absence or unload for engagement cleanup; retain separate uninstall verification for explicit removal.
- [x] Test a cached hook still firing after removal, a failed direct recorder control, silent health failure, and success after simulated unload. Re-run to GREEN. Tests inject a clock and runtime control fixtures; they do not declare simulated behaviour live.
- [x] Commit `feat: complete renewable audit lifecycle and teardown verification`.

### Task 6: Skill instructions, runtime controls and evidence limits

**Files:** Complete `SKILL.md`, `agents/openai.yaml`, `references/codex.md`, `references/devin.md`; add `tests/behavior/evidence-and-cleanup.md`, `tests/pressure/audit-recovery.md`, `tests/evaluator-only/audit-recovery-rubric.md`.

**Interfaces:** Consumes the working CLI. Produces an agent-readable workflow with executable commands resolved from the installed skill path, all mutation/restart obligations, evidence detail choice, mandatory sanitisation, runtime trust review and preserved capability limits.

- [x] Write reusable behavioural prompts for interrupted/expired audits, untrusted hooks, missing coverage, ambiguous Devin child activity, tempting empty-log claims, result-detail selection, secret-bearing inputs, and post-assessment purge. Evaluate decisions against the contract, not prose matches. Keep expected answers in evaluator-only material. Fresh contexts selected status when sufficient, rejected real credentials, declined to fill expired coverage retroactively, rejected the ambiguous Devin child claim, and required purge after verified teardown; concise decision summaries are retained in scratch without transcripts or model metadata.
- [x] Exercise the complete helper against disposable project configurations using `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts -q`; fix failures through owning tasks rather than adding test-only overrides.
- [ ] Using the same installed global dispatcher and selected live activation mechanism, run fresh Codex live controls in the canonical worktree with run data under `Z:/_agent-scratch/agent-asset-marketplace/codex-mark-377-temporary-tool-auditing/implementation-validation/`. Capture parent shell success/nonzero failure, paired child call, completed no-tools child, nested tool execution and an available MCP call, selected detail levels, short expiry and explicit renewal. Human reviews the stable global definition once. Complete the initial activation spike first; all remaining controls reuse it without reinstalling or requesting further restarts. Record any unsupported event coverage as a limit rather than repeating setup. Do not expose credentials or print raw responses to verification artifacts.
- [ ] At the end of the full development engagement, disable recording, verify a healthy dispatcher and no writes from a subsequent runtime canary without restarting, then purge event, health, and control logs plus known run-local recorder copies. Verify only a minimal sanitized cleanup receipt remains. Keep the global dispatcher installed and inert. Assessment/reporting between rounds does not trigger cleanup while follow-up work is pending. Stop dependent completion if disablement or purge remains unresolved.
- [x] Compare Devin Desktop fixtures/references against the recorded `skills/iterative-review/references/harness-capability-floor.md` and current official Devin CLI documentation. Keep Devin CLI unsupported because its standalone hook config format differs and its documented event shape does not establish the per-call correlation ID. Run fresh Devin Desktop controls only if that runtime is available; otherwise state new code is tested by fixture/helper behaviour and historical runtime evidence, not live revalidated.
- [x] Update the skill, references, and pressure prompts to distinguish installation, engagement, and recording round. A stopped round may be assessed/reported and resumed for human-requested follow-up; cleanup is only due when the engagement is finished or abandoned. Focused helper validation and fresh-context retest pass; resumed engagements retain their activation, while another session in the same worktree is excluded. Metadata-only status, the 25 MiB event ceiling, stop-on-cap behavior, same-account trust boundary, and silent mid-interval outage limit are explicit. Run-specific model results are never committed into the skill.

### Task 7: Package, review and publish the capability

**Files:** Modify `src/plugin-definitions/repo-worker-pack/contents.json` to add the canonical skill, and `files/README.md`/`files/SOURCE.md` where their current authored inventory requires it. Update this plan and the approved spec status on completion. Regenerate builder-owned output rather than editing it.

**Interfaces:** Consumes the complete skill and verified teardown evidence. Produces a self-contained generated plugin, clean hooked commit, fresh whole-branch review and verified Draft PR.

- [x] Add the skill with first-party verbatim provenance matching neighbouring entries. Read existing repository build/shipping assertions and extend only a genuine packaging gap; do not add filename or exact-copy change-detector tests.
- [x] Run `py -3 tools/run.py marketplace --apply`, `py -3 tools/build_marketplace.py --check`, and `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts -q`. Inspect generated diff and confirm installed relative helper/template paths work from the built package independently of the source tree.
- [ ] Promote enduring runtime and evidence rules into skill references; mark this plan/spec `completed-awaiting-retirement` when all agent-owned items are complete. Preserve them through the completing PR. Do not retire unrelated active artifacts. The metadata-only default omits arguments/results, full-results is opt-in, and event logs have a 25 MiB ceiling. No predecessor cleanup was identified as eligible in the initial spec-only slice; reassess any subsequently landed completed artifacts against repository custody before adding removals.
- [ ] Commit through the tracked hook, which owns complete apply/check gates. Do not redundantly run complete CI immediately before/after that successful commit or bypass the hook.
- [ ] Obtain fresh whole-branch review through the installed requesting-code-review workflow. Correct actionable findings, re-run affected checks and obtain fresh review after correction; CI alone is insufficient review evidence.
- [ ] When execution is authorised through publication, push the task branch and create a Draft PR with exact-file body text. Attach it to this chat; verify the remote head and hosted checks. Report remaining human Ready/merge actions as subsequent actions, not unchecked implementation steps. If publication is not authorised at execution time, retain completed local work and request that final concrete publication decision.
- [ ] Return validation output, final head, changed source/generated boundaries, runtime coverage and residuals, all development-probe cleanup proof, and the PR URL when created. Update MARK-377 with evidence without declaring merged or Done unless those states are actually proved and authorised.

## Historical implementation evidence before the global-hook revision

Checked items below record witnessed work on the earlier project-local design. They do not establish acceptance of the revised global lifecycle. Task 3 and the reopened Task 5/6 items govern the remaining work. Update the approved spec to the settled global lifecycle before implementation; retain sanitisation and evidence constraints.

## Review hardening follow-up

The fresh whole-branch review at `5938683cf4d3b9e3c9ca183de7dc67413d67f2b9` found several evidence-integrity and cleanup gaps. The corrections below are implemented test-first; they need a fresh review at the new head before live runtime verification resumes.

- [x] Redact full quoted credential values, including escaped quote forms, in CLI flags and assignments; verify sanitized on-disk records.
- [x] Bind lifecycle controls to the exact installed helper path and run directory; namespace control identities by call, session, and agent so unrelated subject attempts remain visible.
- [x] Recover intent-only interrupted registration when no owned hook config exists, while preserving ambiguous-owner conflicts and pre-existing empty config files.
- [x] Persist and use the hook interpreter for direct teardown health checks; keep cleanup pending if that interpreter is unavailable.
- [x] Disable late outcome writes after explicit disarm, removal, and verified teardown while retaining matched late outcomes after ordinary stop/expiry.
- [x] Return subject, detail, intervals, unresolved count, coverage, health, and redaction data in assessment output.
- [x] Restrict lifecycle-control recognition to standalone invocations in known command tools and command fields; preserve mixed commands and nested payloads as subject attempts.
- [x] Detect all intersecting Devin dispatch intervals, including dispatches already active before the selected child starts; reject ambiguous child attribution.
- [x] Redact `Pwd=` connection-string values, including quoted and braced forms, and verify persisted event records.
- [x] Verify teardown health through the normalized event-recording path and exact event log; a writable controls log alone cannot satisfy cleanup.
- [x] Replace the Devin capability-floor relative link with an immutable repository source link so the reference remains available in the shipped package.
- [x] Attribute Codex session selectors to parent calls without a child agent ID; require an agent selector for Codex child calls.
- [x] Exclude only explicitly registered control call identities; exact lifecycle command text alone cannot hide a selected subject's tool attempt.
- [x] Redact plain `key=` URL query credentials while preserving unrelated query parameters.
- [x] Redact cloud signed-URL signature and credential query parameters before persistence.
- [x] Redact common JWT, ID token, and OAuth authorization-code URL parameters before persistence.
- [x] Redact common `auth_token` query and sensitive URL fragment values before persistence.
- [x] Redact common session-cookie identifier query parameters before persistence.
- [x] Redact legacy CFID/CFTOKEN URL session tracking credentials before persistence.
- [x] Preserve only explicitly supplied schema-defined audit attribution session-ID paths; redact same-named values in nested tool arguments and results.
- [x] Cover structured personal, health, payment, and common secret identifiers, plus selected high-confidence free-text email, US SSN, JWT, and Luhn-valid payment-card patterns. Document that arbitrary private or commercial content cannot be detected comprehensively.
- [x] Add post-assessment purge of event, health, and control logs plus known run-local recorder copies as a mandatory cleanup stage, gated on verified hook unload; preserve unknown files and keep cleanup pending until deletion is confirmed.
- [x] Preflight the whole run directory before purging; leave root-level unknown files intact and cleanup pending without deleting logs.
- [x] Reject symlink/junction helper directories and any resolved helper path outside the run before deleting logs or helper copies; verify with a Windows junction sentinel test.
- [x] Classify URL query keys through the structured sensitive-field rules after decoding and normalizing camelCase, bracket, and dotted nesting; verify persisted sentinels are removed while unrelated query parameters remain.
- [x] Run the owning suite and full repository gates, regenerate the package, commit, and obtain fresh whole-branch plus matching topical reviews. Fresh web-backed whole-branch and security reviews at `c7283d3f` found no actionable gaps; reviewers checked OWASP, OpenTelemetry, RFC 9110, Python junction handling, Microsoft reparse points, and CWE-59.

## Execution entry and current baseline

Use the existing canonical worktree `Z:/_agent-worktrees/agent-asset-marketplace/codex/mark-377-temporary-tool-auditing`, branch `codex/mark-377-temporary-tool-auditing`. The implementation and generated package are in place and under review; follow-up hardening changes address independent review findings. The previous disposable spike is fully torn down; its scratch evidence is context, not production code.

Read `.agents/runbooks/implementing.md`, the approved spec, this plan, source custody doctrine, skill tests contract and tracked command contract before execution. Refresh upstream and inspect drift without overwriting the current approved artifacts. Do not recreate a worktree or discard pre-existing dirty state. Every task's commit uses the repository hook and all helper tests named above; execution updates checkboxes from witnessed evidence.

## Updated acceptance and implementation handoff

- [x] Update the approved design spec to match the approved global/session-scoped lifecycle. MARK-377 remains In Progress and has no linked Linear documents.
- [ ] Prove capture-time session-family isolation: activate one parent session, capture its parent and subagent controls, and exercise a separate session in the same worktree plus a session in another project. Inspect the selected run to prove neither unrelated session was persisted; no post-recording filtering may satisfy this criterion. Establish the actual runtime session-ID source before activation and report unsupported or missing child identifiers as attribution limits.
- [ ] Prove one-time global load/approval followed by enable, positive control, pause/assessment, resume, renewal, disable, inert canary, and purge in one continuing Codex process. Keep recording rounds in one engagement and retain controls as evidence until final purge.
- [x] Fresh code and security reviews inspected the selected activation mechanism, per-worktree isolation, sanitisation, bounded storage, default-inert/expired behavior, and cleanup. The security reviewer web-spiked current official Codex hook semantics and OWASP logging guidance; findings were fixed or explicitly bounded to honest local-agent use.
- [x] Regenerate the shipped package and pass script tests, Ruff, marketplace generation/check, and diff whitespace checks. Do not treat earlier fixture or teardown evidence as proof of the new live mechanism.

The human approved this revision and the stable hook definition. Live runtime proof still awaits the one Codex restart and approval to refresh the changed, already-owned helper files. The refresh leaves the approved hook definitions unchanged, and the installer refuses helper drift unless the explicit review-gated flag is used. The selected execution lane remains `executing-plans` because dispatcher activation, lifecycle migration, and live evidence share state; a separate implementation agent per task would add handoff overhead without separating those concerns.
