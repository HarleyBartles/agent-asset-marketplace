# Temporary Tool Auditing

Status: Approved by the human on 2026-10-03; implementation is in progress on `codex/mark-377-temporary-tool-auditing`. Design date: 2026-10-02. Issue: MARK-377. Source baseline: `b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa`.

## Purpose and boundary

Provide an Agent Capability Pack skill for an agent that needs to prove tool use during a bounded task. The capability installs temporary project-local instrumentation, verifies capture, records attempted calls and observed outcomes across covered agents, assesses an identified subject, and removes the instrumentation with verified runtime teardown.

The first release supports Codex and the demonstrated Devin Desktop hook contract. Devin CLI remains unsupported until its separate configuration and per-call correlation requirements are verified. It offers tool auditing, not a general hook framework, an authorisation gate, or an immutable evidence system. MARK-378 owns the separate authorisation experiment. Evidence supports cooperative auditing within demonstrated runtime coverage; it does not establish protection against an agent deliberately modifying its recorder or evidence.

Canonical source belongs under `skills/temporary-tool-auditing/`. Agent Capability Pack composition currently lives under `src/plugin-definitions/repo-worker-pack/`. Generated plugin outputs are rebuilt from those sources. Installation of the pack makes the skill available; it does not activate hooks in consumer repositories.

## Agent journey

Before installing, the agent states the evidence question, subject, runtime, capture detail, project scope, and observation duration. The skill provides executable helpers and hook templates, rather than expecting the agent to invent a logger or edit runtime configuration from memory.

The agent prefers hook registration in its isolated worktree. It uses the repo checkout when runtime discovery requires that location, recording the actual registration root and affected scope. Capture covers every agent reached by that registration. Selecting a subject for assessment does not suppress other agents' records.

The normal journey is prepare, preview, inspect existing project-local Codex configuration, install, temporarily trust the exact Codex worktree path when needed, obtain human review of hook definitions, restart or resume as required, verify a positive control, start observation, perform the task, end observation, assess evidence, disarm, remove registrations and only the trust entry created by this run, restart or resume as required, verify teardown, and purge the logs. The agent completes this journey on cancellation and failure as well as success. It never trusts a parent or wildcard path and does not override an explicit untrusted entry. A restart handoff includes the durable run location, next operation, and cleanup instructions.

## Components and interfaces

The skill owns instructions, runtime references, recorder templates, and a small Python helper with explicit operations for prepare, install, status, verify, start, stop, renew, assess, disarm, remove, verify-teardown, and purge. These are logical operations, not a generic extensibility API; exact CLI grouping is a planning choice. Mutation requires explicit apply semantics consistent with the repository's script conventions.

The installer identifies the runtime's local configuration, renders an absolute command to a run-local recorder, and adds owned handler entries without replacing unrelated hooks. The recorder reads the runtime event from stdin, applies the run's recording and sanitisation rules, and appends an event. It produces only runtime-valid neutral output and does not approve, block, or rewrite tools. The assessor reads recorded evidence and returns a bounded finding with coverage, attribution, completeness, and redaction limitations. The lifecycle helper maintains ownership and the cleanup obligation.

Run files live in the consuming repository's declared off-repo scratch location when available, otherwise a private user-owned temporary directory. The run directory remains available across restart. While active, it contains a versioned manifest and sanitized event, health, and control logs; assessment results are returned to the agent and are not persisted as a separate report. It contains no raw credential-bearing configuration backup or raw input spool. Assets needed by an installed hook are copied into the run so changing an installed skill package cannot break a pending cleanup. After verified teardown and purge, only a minimal cleanup receipt remains. This capability is intended for local use on the operator's machine; it does not send run data to a remote service.

## Run state and lifecycle

The manifest records run ID, runtime and observed version, project and registration roots, selected subject, capture detail, owned config entries and their fingerprints, recording policy, expiry, observation intervals, verification controls, health, and recovery commands. Write no secret values into the manifest. `cleanup_required` becomes true before the first configuration mutation and stays true through errors, expiry, cancellation, removal, teardown verification, and log purging. It clears only after the hook is verified unloaded and all run logs are purged.

Separate registration, runtime activation, and recording state. A definition on disk is not proof that a runtime executes it. Removal on disk is not proof that an existing session unloaded it. Status distinguishes prepared, installed-awaiting-activation, verified-active, recording, stopped/disarmed, expired, removed-awaiting-runtime-verification, and cleaned. Health and incomplete evidence are separate from these lifecycle states.

Only one managed audit installation may be active at a given registration root in v1. A second installation reports the existing run and its cleanup obligation rather than stacking another recorder. Multiple covered agents may write to that run; writes must preserve complete records under concurrency.

The default lease is 30 minutes. The agent can choose a different positive duration and explicitly renew it. Renewal records its time and new expiry. Expiry immediately stops recording when the next invocation checks the lease. It does not remove registration or clear cleanup. Renewal after expiry creates a new observation interval; it cannot retrospectively cover the gap. Restart or trust delays consume the lease unless it is renewed explicitly.

Disarm stops writes even when hooks remain cached. Removal locates and removes only this run's unchanged owned entries. It preserves unrelated edits and removes a file or directory only when the helper created it and it is now empty. If an owned entry was changed, report the conflict and retain the cleanup obligation instead of restoring a stale whole-file backup or deleting someone else's configuration.

Verify-teardown requires registrations absent and a runtime control after any required restart. Briefly arm the retained recorder with a short lease for this control, establish a log baseline, execute a harmless covered call, and confirm no invocation is recorded. Disarm again in all cases. A failed recorder cannot prove unload through silence: teardown verification also requires a working direct recorder control and current health. Once assessment has established the bounded claim, the agent must stop capture, remove registrations, verify unload, and run `purge --apply`. Purge removes `events.jsonl`, `health.jsonl`, `controls.jsonl`, and the known run-local recorder helper copies, strips subject and question data from the manifest, and keeps only a minimal cleanup receipt. It preflights the run directory, preserves unknown files, and rejects symlink or junction helper directories before deleting logs or helper copies. Unknown files and unsafe paths keep cleanup pending rather than being deleted. Cleanup clears only after deletion and the receipt update are verified. Purging is logical file removal on the local machine, not a promise of physical media erasure.

## Events, detail, and findings

Every event has run ID, UTC receipt time, runtime event name, available session/agent/turn/call identifiers, and source attribution. Attempt events retain sanitized tool name and full sanitized arguments. Outcome events retain observed completion and any independently available success, failure, rejection, or error status. Full sanitized result bodies are an agent-selected option. The chosen detail level is recorded before capture; changing it requires a stopped observation and a new declared interval.

Pair attempts and outcomes by the runtime call identifier, namespaced by run and subject. Preserve unmatched attempts and outcomes as incomplete records. Do not invent a success status from the presence of a post-tool event or infer failure solely from missing post-tool evidence.

An assessment reports attempted count, paired outcome count, unresolved count, subject, observation intervals, capture detail, known tool coverage, health failures, attribution method, and redactions. It can report no observed attempted calls for a completed, verified interval; it must not turn an empty file, unsupported tool path, expired period, recorder failure, or ambiguous subject into proof of no tools. A no-tool claim requires a positive control through relevant runtime paths, bounded observation, and demonstrated subject completion. Controls are tagged and excluded from scenario counts without deleting their evidence.

The helper establishes evidence prerequisites and counts. The calling agent remains responsible for framing the bounded claim and stating limitations; the helper does not award an automated scenario score.

## Runtime differences

Codex uses `.codex/hooks.json` with a `hooks` wrapper, or compatible inline project configuration. It requires project trust and review of non-managed hook definitions. Setup previews and adds only the exact worktree path to the active user `config.toml`; it preserves existing trust, refuses an explicit untrusted setting, and removes only the temporary entry it owns during teardown. This makes the local `.codex/` layer eligible for loading but does not approve hook definitions. Review any existing project-local Codex config and rules that become eligible when the path is trusted. Record attempts/outcomes plus supported session and subagent lifecycle events. Our observed build pairs calls by `tool_use_id`; child tool records have `agent_id`, while `session_id` remains the parent's. Main-agent attribution uses the session and absence of a child identity only within verified coverage. Do not infer that every runtime version supplies these fields.

The Codex desktop spike established live discovery, human trust review, activation after restart, cached execution after file removal, and unload after a second restart. Worktree-local capture succeeded in a trusted fresh CLI session. The skill describes the required trust/restart handoff and always verifies actual activation and teardown rather than universalising the spike's restart behaviour. Hosted and specialised paths outside demonstrated hook coverage remain explicit limitations.

The `devin-desktop` adapter is grounded in the recorded Devin Desktop capability probe and uses its observed `.devin/hooks.v1.json` wrapper and event payload. Devin CLI is a distinct contract: its current [hook documentation](https://docs.devin.ai/cli/extensibility/hooks/overview) requires a root event map and documents session/turn IDs without establishing the per-call correlation ID needed by this assessor. Keep Devin CLI unsupported until its schema and correlation behavior are separately verified. Do not present the Desktop spike as evidence for CLI behavior.

The recorded Devin Desktop spike proves pre/post capture for parent and child calls and `tool_use_id` pairing, but child calls share the parent session and lack `agent_id`. Session-wide auditing is supported. Individual child attribution requires serialized dispatch, verified launch/completion boundaries, and no overlapping unidentified tool producers. The orchestrator and other agents must remain idle for the dispatch window; the orchestrator records this positional-attribution assumption explicitly. Otherwise report unattributed events and decline the individual-child no-tool claim. Installation guidance carries the recorded session-start loading/restart constraint and verifies it live. Official CLI documentation does not silently replace recorded Desktop evidence.

Keep one recorder and evidence model, with small runtime-specific configuration and payload interpretation. Preserve unknown fields only through the selected sanitised detail rules. Missing required correlation, unsupported runtime behaviour, or failed activation produces an explicit capability limit rather than guessed evidence.

## Mandatory sanitisation

Sanitise before every persistent write, at every detail level. Apply the same protection to arguments, outputs, errors, lifecycle messages, manifests, assessments, health records, and helper diagnostics. Never write raw payloads to a spool or dump them on parse failure. Configuration fingerprints may support ownership checks; configuration values must not become an unsanitized backup.

Recursively redact credential-bearing fields and recognized secret patterns across tool arguments, results, errors, lifecycle messages, URLs, command arguments, headers, cookies, and nested serialized JSON. URL query keys use the same sensitive-name classifier as structured fields after decoding and normalizing common camelCase, dotted, and bracketed nested-key forms, supplemented by explicit provider-signature patterns; preserve unrelated query parameters. Cover passwords; provider and generic API keys; access, refresh, bearer, and session credentials; private keys; database credentials; and common payment and personal identifier fields. Detect high-confidence free-text forms such as email addresses, US Social Security numbers, JWTs, and Luhn-valid payment card numbers. Sensitive-data review also considers health and government identifiers, bank/payment data, source code, file paths, internal network names, and commercially sensitive content; these broader contextual classes may require selecting less detail because pattern detection cannot recognize them all. Runtime attribution is an explicit schema exception: preserve the normalized event's top-level `session_id` and the manifest's known subject/control attribution paths, while redacting a same-named field inside tool arguments or results. Use explicit redaction markers, never secret-derived stable identifiers, and avoid copying surrounding credential text into diagnostics.

If sanitisation or parsing fails, drop the unsafe content, write only a safe health marker where possible, and mark evidence incomplete. Full-results mode cannot disable sanitisation. Redactions remain visible in assessments because they can prevent proving an argument or result. Pattern-based detection cannot establish that every arbitrary secret, person, source-code fragment, or commercially sensitive passage is recognized. The skill states this limit, guides agents to avoid secret-bearing probe commands and unnecessary result capture, and requires purge after the evidence has proved its bounded claim.

## Failure and recovery

Hook invocation failures must not be interpreted as no activity. Recorder health includes sanitized parse, sanitisation, write, and concurrency failures where reportable. The helper verifies a writable log and recorder before observation and checks runtime error evidence and health before assessment. Failures that leave no trustworthy health channel make coverage unknown. Auditing observes tool use; it does not change runtime fail-open/fail-closed policy for tools.

Resume inspects the durable manifest, actual registration, lease, and runtime control rather than trusting a prior agent's statement. An interrupted install can be removed using its ownership records. A stopped or expired run retains the exact removal path. If a runtime, command interpreter, trust mechanism, or cleanup operation is unavailable, report the missing capability and outstanding obligation without claiming clean completion.

## Acceptance and validation boundary

Meaningful helper tests belong under `skills/temporary-tool-auditing/tests/`. They verify sanitized on-disk bytes for representative credentials and personal/payment data, nested session credential redaction with safe attribution preserved, intact concurrent records, attempt/outcome pairing and incompleteness, lease expiry and renewal gaps, crash/recovery states, preservation of unrelated hooks, ownership conflicts, idempotent removal, and purge only after verified teardown. Instruction behavior checks verify honest attribution/coverage claims and persistent cleanup obligations. No exact-prose or inventory-only tests substitute for these behaviours.

Live runtime controls verify activation, parent and child capture, a completed no-tools child, tool failure and unmatched outcomes, agent-selected result detail, expiry/renewal, and post-removal unload. Use existing Devin Desktop spike evidence for demonstrated capabilities, fresh runtime controls where that runtime is available, and explicit unverified limits where it cannot be repeated. Never declare a new live Devin check passed from documentation alone.

Rebuild marketplace projections from canonical sources and run the owning skill tests plus required repository and shipping gates. Return code and validation proof, runtime evidence, residual limits, and verified teardown for every installed development probe. Probe transcripts and run-specific findings remain scratch; durable runtime rules belong in the skill references.

## Evidence sources

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), and [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), for log minimization and sensitive data categories.
- [NIST SP 800-122](https://csrc.nist.gov/pubs/sp/800/122/final), for context-based PII protection.
- [PCI SSC guidance](https://www.pcisecuritystandards.org/faqs/1533/), for sensitive authentication data that must not be retained after authorization.
- [GitHub supported secret-scanning patterns](https://docs.github.com/en/code-security/reference/secret-security/supported-secret-scanning-patterns), as a practical taxonomy of generic and provider-specific secret formats.
- [OpenTelemetry URL semantic conventions](https://opentelemetry.io/docs/specs/semconv/url/), for scrubbing sensitive URL query values while retaining unrelated parameters.
- [RFC 9110 section 17.9](https://datatracker.ietf.org/doc/html/rfc9110#section-17.9), for privacy risks from sensitive or user-provided URI data.
- [Python `Path.is_junction`](https://docs.python.org/3.13/library/pathlib.html#pathlib.Path.is_junction) and [Microsoft reparse-point guidance](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points), for detecting Windows directory aliases before purge.
- [Microsoft `ReplaceFileW`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew), for preserving the existing Windows Codex config file's ACLs and attributes during atomic update.
- [CWE-59](https://cwe.mitre.org/data/definitions/59), for link-following/path-resolution risks.
- [Official Codex hooks](https://learn.chatgpt.com/docs/hooks).
- [Official Devin CLI hook configuration](https://docs.devin.ai/cli/extensibility/hooks/overview), used to define the unsupported CLI boundary.
- [Official Devin CLI lifecycle payloads](https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks), used to distinguish documented correlation fields from the Desktop spike.
- [Recorded Devin Desktop capability findings](../../skills/iterative-review/references/harness-capability-floor.md).

The completed Codex scratch spike is supporting experiment evidence, not a repository authority. Its durable consequences are stated above. Existing evidence does not remove the positive-control requirements for a future consumer run.
