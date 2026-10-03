# Temporary Tool Auditing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship an Agent Capability Pack skill that establishes bounded tool-use evidence in Codex and Devin and verifies removal of its temporary instrumentation.

**Architecture:** One Python recorder and evidence model, with focused Codex and Devin configuration/payload adapters. A durable run manifest separates registration, activation, recording, expiry, and verified cleanup. Every persisted surface passes through mandatory sanitisation.

**Tech Stack:** Python standard library, pytest, JSON/JSONL, runtime command hooks, existing marketplace builder and tracked Git hook. Support Windows and Linux; no new third-party runtime dependency.

**Spec:** [Approved design](../specs/2026-10-02-temporary-tool-auditing-design.md).

**Execution Strategy:** `executing-plans`. Sanitisation, recorder health, lifecycle transitions, ownership recovery, and assessment share state and require continuity through restarts. The nearest alternative is `subagent-driven-development`, which adds fresh per-task implementation/review contexts at the cost of repeated reconstruction of that state. Use inline sequential implementation with a fresh whole-branch review at completion.

## Global Constraints

- Implement MARK-377 only. No general hook framework, authorisation gate, secret-backed evidence fingerprints, or malicious-agent immutability claim.
- Codex and Devin are supported with explicit runtime differences. Capture all covered agents; select the subject when assessing evidence.
- Prefer worktree-local registration; record and explain checkout fallback. Never install global hooks or bypass human hook trust as normal skill behaviour.
- Record sanitized arguments, identifiers, and observed outcome status by default; full sanitized results are optional and chosen by the agent before observation.
- Default lease is 30 minutes, adjustable with explicit renewal. Expiry never clears cleanup and renewal never fills a capture gap.
- No raw payload spool, secret-bearing config backup, exception dump, or unsanitized diagnostic. Failure or ambiguity prevents a no-tools claim.
- Preserve existing hooks and unrelated configuration changes; remove only unchanged owned entries. Keep evidence and inert recorder after teardown.
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
| `assessment.py` | `assess(run: Path, subject: dict) -> dict`; counts and prerequisite/coverage/attribution limits. |
| `auditctl.py` | User CLI, durable transitions, controls, expiry renewal and restart handoffs. |

Tests live under `skills/temporary-tool-auditing/tests/scripts/`; use a local `conftest.py` that adds the scripts directory to test imports. Shared fixtures construct temporary runs/configurations and inject time; they do not invoke paid models. Behaviour cases live under `tests/behavior/` and `tests/pressure/`, with evaluator-only expectations under `tests/evaluator-only/`. Run outputs stay off-repo.

Manifest version 1 contains `run_id`, `runtime`, `runtime_version`, `project_root`, `registration_root`, `subject`, `detail`, `expires_at`, `armed`, `cleanup_required`, `registration_state`, `activation_verified`, `intervals`, `controls`, `health`, and `owned_entries`. Store UTC timestamps and positive finite lease durations. `detail` is `status` or `full-results`. An interval records start/end, detail and expiry boundaries. Controls reference actual captured call IDs and are excluded from scenario counts, never deleted.

Normalized records contain `run_id`, `received_at`, `event`, `session_id`, optional `agent_id`, `turn_id`, `call_id`, `tool_name`, sanitized `arguments`, `outcome_status`, optional sanitized `result`, and `redactions`. Missing IDs are null and invalidate dependent attribution/pairing rather than being manufactured. Outcome status is `observed-unknown`, `success`, `failure`, or `rejected`; use the latter three only when the runtime payload independently establishes them.

CLI: `auditctl.py <operation> --run-dir <absolute-path>`, with `--check` default and `--apply` for mutations. `prepare` additionally requires `--runtime codex|devin-desktop --project <root> --question <text> --subject <session-or-agent-selector> --detail status|full-results`, and accepts `--duration-minutes` default 30 and `--runtime-version`. Devin CLI remains unsupported until its config and correlation contract are verified separately. Provide `--help` at root and operation level. Missing required capabilities return nonzero and safe structured errors. Never put the raw question or exception text into output before sanitisation.

## Review Focus

- Credential patterns in free text, URLs, CLI flags, serialized JSON and common header forms are sanitized before persistence; pattern detection remains best-effort: Task 1 and Task 2.
- Interrupted config writes leave discoverable ownership; concurrent installers cannot stack runs. Registration locks live in private user temp storage, not in the project hook directory: Task 3.
- Late outcomes, lease gaps and missing call IDs cannot produce complete no-tools evidence: Task 4.
- Devin interleaving cannot be guessed into child attribution: Task 4.
- Cached hooks and a broken recorder cannot make silent teardown appear verified: Task 5 and Task 6.

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

### Task 3: Owned project-local registration and recovery

**Files:** Create `scripts/registration.py`, `tests/scripts/test_registration.py`; extend `store.py` transaction support only if required.

**Interfaces:** Consumes `render_handlers` and locked store; produces `install`/`remove` results containing ownership state and safe conflicts. Existing inline Codex hooks may coexist; use local hooks.json and preserve both source types rather than rewriting unrelated TOML.

- [x] Test preservation of existing handlers and top-level fields, non-ASCII paths/spaces, worktree root selection, concurrent installer rejection, same-run idempotence, and ownership conflict on removal. Build an interrupted-install fixture with an intent journal but incomplete registration.

```python
def test_remove_preserves_new_unrelated_handler(installed_run, config_path):
    add_unrelated_handler(config_path, 'unrelated-command')
    remove(installed_run)
    assert handler_commands(config_path) == ['unrelated-command']
    assert load_manifest(installed_run)['cleanup_required'] is True
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_registration.py -q` to RED.
- [x] Persist cleanup obligation and intended owned entries before config mutation. Use a registration-root lock and ownership marker containing only run location/ID, reject a second active run, and copy recorder dependencies into the run. Fingerprint owned handler entries without copying raw config. Recover by comparing intent against current entries after a crash. Remove unchanged owned entries only, never restore a whole-file backup. Detect malformed configs and changed owned entries as conflicts. Remove helper-created empty files/directories only; retain inert run assets.
- [x] Re-run tests to GREEN; include crash points before config replace and before manifest finalisation, plus successful repeated cleanup.
- [x] Commit `feat: manage temporary audit registration custody`.

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

**Interfaces:** Consumes Tasks 1-4 functions. Produces the CLI contract above and operations `prepare`, `install`, `status`, `verify`, `start`, `stop`, `renew`, `assess`, `disarm`, `remove`, `verify-teardown`.

- [x] Test no mutation under `--check`, default 30 minutes, positive finite durations, explicit renewal, expiry gaps, illegal transitions, interrupted install resume, capture-detail changes only between intervals, and cleanup remaining true after stop/expiry/removal.

```python
def test_expiry_does_not_complete_cleanup(expired_run):
    state = cli_status(expired_run)
    assert state['recording_state'] == 'expired'
    assert state['cleanup_required'] is True
```

- [x] Run `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts/test_lifecycle.py skills/temporary-tool-auditing/tests/scripts/test_cli.py -q` to RED.
- [x] Implement durable transitions, safe structured CLI output, root/operation help and explicit preview/apply. `verify` binds a marked actual captured call to the requested coverage. `start` refuses absent verified activation; `stop` closes interval without discarding evidence. `renew` after expiry closes the old interval at expiry and requires a new start. `verify-teardown` is two-phase: direct recorder health control, short armed baseline and runtime canary after removal/restart, then compare log and disarm. Cleanup clears only when both configuration absence and the healthy canary support unload. Always disarm on verification failure; unavailable runtime keeps cleanup pending.
- [x] Test a cached hook still firing after removal, a failed direct recorder control, silent health failure, and success after simulated unload. Re-run to GREEN. Tests inject a clock and runtime control fixtures; they do not declare simulated behaviour live.
- [x] Commit `feat: complete renewable audit lifecycle and teardown verification`.

### Task 6: Skill instructions, runtime controls and evidence limits

**Files:** Complete `SKILL.md`, `agents/openai.yaml`, `references/codex.md`, `references/devin.md`; add `tests/behavior/evidence-and-cleanup.md`, `tests/pressure/audit-recovery.md`, `tests/evaluator-only/audit-recovery-rubric.md`.

**Interfaces:** Consumes the working CLI. Produces an agent-readable workflow with executable commands resolved from the installed skill path, all mutation/restart obligations, evidence detail choice, mandatory sanitisation, runtime trust review and preserved capability limits.

- [x] Write reusable behavioural prompts for interrupted/expired audits, untrusted hooks, missing coverage, ambiguous Devin child activity, tempting empty-log claims, result-detail selection and secret-bearing inputs. Evaluate decisions against the contract, not prose matches. Keep expected answers in evaluator-only material. Fresh contexts selected status when sufficient, rejected real credentials, declined to fill expired coverage retroactively, and rejected the ambiguous Devin child claim; concise decision summaries are retained in scratch without transcripts or model metadata.
- [x] Exercise the complete helper against disposable project configurations using `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts -q`; fix failures through owning tasks rather than adding test-only overrides.
- [ ] Run fresh Codex live controls in the canonical worktree with run data under `Z:/_agent-scratch/agent-asset-marketplace/codex-mark-377-temporary-tool-auditing/implementation-validation/`. Capture parent shell success/nonzero failure, paired child call, completed no-tools child, nested tool execution and an available MCP call, selected detail levels, short expiry and explicit renewal. Human reviews actual hook definitions; use restart handoffs where observed necessary. Do not expose credentials or print raw responses to verification artifacts.
- [ ] Remove development registrations, disarm, restart if required and execute healthy armed unload canary before declaring teardown. Stop dependent completion if cleanup remains unresolved. Retain sanitized runtime evidence and result/coverage summaries in scratch, not source.
- [x] Compare Devin Desktop fixtures/references against the recorded `skills/iterative-review/references/harness-capability-floor.md` and current official Devin CLI documentation. Keep Devin CLI unsupported because its standalone hook config format differs and its documented event shape does not establish the per-call correlation ID. Run fresh Devin Desktop controls only if that runtime is available; otherwise state new code is tested by fixture/helper behaviour and historical runtime evidence, not live revalidated.
- [ ] Commit `docs: guide tool auditing and runtime recovery` after focused checks and behavioural evaluation. Run-specific model results are never committed into the skill.

### Task 7: Package, review and publish the capability

**Files:** Modify `src/plugin-definitions/repo-worker-pack/contents.json` to add the canonical skill, and `files/README.md`/`files/SOURCE.md` where their current authored inventory requires it. Update this plan and the approved spec status on completion. Regenerate builder-owned output rather than editing it.

**Interfaces:** Consumes the complete skill and verified teardown evidence. Produces a self-contained generated plugin, clean hooked commit, fresh whole-branch review and verified Draft PR.

- [x] Add the skill with first-party verbatim provenance matching neighbouring entries. Read existing repository build/shipping assertions and extend only a genuine packaging gap; do not add filename or exact-copy change-detector tests.
- [x] Run `py -3 tools/run.py marketplace --apply`, `py -3 tools/build_marketplace.py --check`, and `py -3 -m pytest skills/temporary-tool-auditing/tests/scripts -q`. Inspect generated diff and confirm installed relative helper/template paths work from the built package independently of the source tree.
- [ ] Promote enduring runtime and evidence rules into skill references; mark this plan/spec `completed-awaiting-retirement` when all agent-owned items are complete. Preserve them through the completing PR. Do not retire unrelated active artifacts. No predecessor cleanup was identified as eligible in the initial spec-only slice; reassess any subsequently landed completed artifacts against repository custody before adding removals.
- [ ] Commit through the tracked hook, which owns complete apply/check gates. Do not redundantly run complete CI immediately before/after that successful commit or bypass the hook.
- [ ] Obtain fresh whole-branch review through the installed requesting-code-review workflow. Correct actionable findings, re-run affected checks and obtain fresh review after correction; CI alone is insufficient review evidence.
- [ ] When execution is authorised through publication, push the task branch and create a Draft PR with exact-file body text. Attach it to this chat; verify the remote head and hosted checks. Report remaining human Ready/merge actions as subsequent actions, not unchecked implementation steps. If publication is not authorised at execution time, retain completed local work and request that final concrete publication decision.
- [ ] Return validation output, final head, changed source/generated boundaries, runtime coverage and residuals, all development-probe cleanup proof, and the PR URL when created. Update MARK-377 with evidence without declaring merged or Done unless those states are actually proved and authorised.

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
- [ ] Run the owning suite and full repository gates, regenerate the package, commit, and obtain fresh whole-branch plus matching topical reviews.

## Execution entry and current baseline

Use the existing canonical worktree `Z:/_agent-worktrees/agent-asset-marketplace/codex/mark-377-temporary-tool-auditing`, branch `codex/mark-377-temporary-tool-auditing`. The implementation and generated package are in place and under review; follow-up hardening changes address independent review findings. The previous disposable spike is fully torn down; its scratch evidence is context, not production code.

Read `.agents/runbooks/implementing.md`, the approved spec, this plan, source custody doctrine, skill tests contract and tracked command contract before execution. Refresh upstream and inspect drift without overwriting the current approved artifacts. Do not recreate a worktree or discard pre-existing dirty state. Every task's commit uses the repository hook and all helper tests named above; execution updates checkboxes from witnessed evidence.
