# Temporary Tool Auditing

Status: Approved by the human on 2026-10-03; implementation is in progress on `codex/mark-377-temporary-tool-auditing`. Design date: 2026-10-02. Issue: MARK-377. Source baseline: `b481f98ae90aa45e5271d10fe1f7aaeb6c7047aa`.

## Purpose and boundary

Provide an Agent Capability Pack skill for an agent that needs to prove tool use during a bounded task. The capability installs temporary project-local instrumentation, verifies capture, records attempted calls and observed outcomes across covered agents, assesses an identified subject, and removes the instrumentation with verified runtime teardown.

The first release supports Codex and Devin. It offers tool auditing, not a general hook framework, an authorisation gate, or an immutable evidence system. MARK-378 owns the separate authorisation experiment. Evidence supports cooperative auditing within demonstrated runtime coverage; it does not establish protection against an agent deliberately modifying its recorder or evidence.

Canonical source belongs under `skills/temporary-tool-auditing/`. Agent Capability Pack composition currently lives under `src/plugin-definitions/repo-worker-pack/`. Generated plugin outputs are rebuilt from those sources. Installation of the pack makes the skill available; it does not activate hooks in consumer repositories.

## Agent journey

Before installing, the agent states the evidence question, subject, runtime, capture detail, project scope, and observation duration. The skill provides executable helpers and hook templates, rather than expecting the agent to invent a logger or edit runtime configuration from memory.

The agent prefers hook registration in its isolated worktree. It uses the repo checkout when runtime discovery requires that location, recording the actual registration root and affected scope. Capture covers every agent reached by that registration. Selecting a subject for assessment does not suppress other agents' records.

The normal journey is prepare, install, obtain any required human trust review, restart or resume as required, verify a positive control, start observation, perform the task, end observation, assess evidence, disarm, remove registrations, restart or resume as required, and verify teardown. The agent completes this journey on cancellation and failure as well as success. A restart handoff includes the durable run location, next operation, and cleanup instructions.

## Components and interfaces

The skill owns instructions, runtime references, recorder templates, and a small Python helper with explicit operations for prepare, install, status, verify, start, stop, renew, assess, disarm, remove, and verify-teardown. These are logical operations, not a generic extensibility API; exact CLI grouping is a planning choice. Mutation requires explicit apply semantics consistent with the repository's script conventions.

The installer identifies the runtime's local configuration, renders an absolute command to a run-local recorder, and adds owned handler entries without replacing unrelated hooks. The recorder reads the runtime event from stdin, applies the run's recording and sanitisation rules, and appends an event. It produces only runtime-valid neutral output and does not approve, block, or rewrite tools. The assessor reads recorded evidence and returns a bounded finding with coverage, attribution, completeness, and redaction limitations. The lifecycle helper maintains ownership and the cleanup obligation.

Run files live in the consuming repository's declared off-repo scratch location when available, otherwise a private user-owned temporary directory. The run directory remains available across restart. It contains a versioned manifest, sanitized event log, sanitized health records, and any assessment. It contains no raw credential-bearing configuration backup or raw input spool. Assets needed by an installed hook are copied into the run so changing an installed skill package cannot break a pending cleanup.

## Run state and lifecycle

The manifest records run ID, runtime and observed version, project and registration roots, selected subject, capture detail, owned config entries and their fingerprints, recording policy, expiry, observation intervals, verification controls, health, and recovery commands. Write no secret values into the manifest. `cleanup_required` becomes true before the first configuration mutation and stays true through errors, expiry, cancellation, and removal until teardown is verified.

Separate registration, runtime activation, and recording state. A definition on disk is not proof that a runtime executes it. Removal on disk is not proof that an existing session unloaded it. Status distinguishes prepared, installed-awaiting-activation, verified-active, recording, stopped/disarmed, expired, removed-awaiting-runtime-verification, and cleaned. Health and incomplete evidence are separate from these lifecycle states.

Only one managed audit installation may be active at a given registration root in v1. A second installation reports the existing run and its cleanup obligation rather than stacking another recorder. Multiple covered agents may write to that run; writes must preserve complete records under concurrency.

The default lease is 30 minutes. The agent can choose a different positive duration and explicitly renew it. Renewal records its time and new expiry. Expiry immediately stops recording when the next invocation checks the lease. It does not remove registration or clear cleanup. Renewal after expiry creates a new observation interval; it cannot retrospectively cover the gap. Restart or trust delays consume the lease unless it is renewed explicitly.

Disarm stops writes even when hooks remain cached. Removal locates and removes only this run's unchanged owned entries. It preserves unrelated edits and removes a file or directory only when the helper created it and it is now empty. If an owned entry was changed, report the conflict and retain the cleanup obligation instead of restoring a stale whole-file backup or deleting someone else's configuration.

Verify-teardown requires registrations absent and a runtime control after any required restart. Briefly arm the retained recorder with a short lease for this control, establish a log baseline, execute a harmless covered call, and confirm no invocation is recorded. Disarm again in all cases. A failed recorder cannot prove unload through silence: teardown verification also requires a working direct recorder control and current health. Retain the inert recorder and evidence so a mistakenly cached command does not reference a deleted executable. Evidence deletion is outside automatic teardown.

## Events, detail, and findings

Every event has run ID, UTC receipt time, runtime event name, available session/agent/turn/call identifiers, and source attribution. Attempt events retain sanitized tool name and full sanitized arguments. Outcome events retain observed completion and any independently available success, failure, rejection, or error status. Full sanitized result bodies are an agent-selected option. The chosen detail level is recorded before capture; changing it requires a stopped observation and a new declared interval.

Pair attempts and outcomes by the runtime call identifier, namespaced by run and subject. Preserve unmatched attempts and outcomes as incomplete records. Do not invent a success status from the presence of a post-tool event or infer failure solely from missing post-tool evidence.

An assessment reports attempted count, paired outcome count, unresolved count, subject, observation intervals, capture detail, known tool coverage, health failures, attribution method, and redactions. It can report no observed attempted calls for a completed, verified interval; it must not turn an empty file, unsupported tool path, expired period, recorder failure, or ambiguous subject into proof of no tools. A no-tool claim requires a positive control through relevant runtime paths, bounded observation, and demonstrated subject completion. Controls are tagged and excluded from scenario counts without deleting their evidence.

The helper establishes evidence prerequisites and counts. The calling agent remains responsible for framing the bounded claim and stating limitations; the helper does not award an automated scenario score.

## Runtime differences

Codex uses `.codex/hooks.json` with a `hooks` wrapper, or compatible inline project configuration. It requires project trust and review of non-managed hook definitions. Record attempts/outcomes plus supported session and subagent lifecycle events. Our observed build pairs calls by `tool_use_id`; child tool records have `agent_id`, while `session_id` remains the parent's. Main-agent attribution uses the session and absence of a child identity only within verified coverage. Do not infer that every runtime version supplies these fields.

The Codex desktop spike established live discovery, human trust review, activation after restart, cached execution after file removal, and unload after a second restart. Worktree-local capture succeeded in a trusted fresh CLI session. The skill describes the required trust/restart handoff and always verifies actual activation and teardown rather than universalising the spike's restart behaviour. Hosted and specialised paths outside demonstrated hook coverage remain explicit limitations.

Devin uses `.devin/hooks.v1.json`, whose root is the event map. Its documented events include PreToolUse, PostToolUse, SessionStart, and SessionEnd. Use its own supported event set rather than copying Codex subagent event registrations. Its turn identifier is `prompt_id`, shell tool name is `exec`, and documented post-tool response includes `success`, `output`, and `error`.

The recorded Devin Desktop spike proves pre/post capture for parent and child calls and `tool_use_id` pairing, but child calls share the parent session and lack `agent_id`. Session-wide auditing is supported. Individual child attribution requires serialized dispatch, verified launch/completion boundaries, and no overlapping unidentified tool producers. Otherwise report unattributed events and decline the individual-child no-tool claim. Installation guidance carries the recorded session-start loading/restart constraint and verifies it live. Official CLI documentation does not silently replace recorded Desktop evidence.

Keep one recorder and evidence model, with small runtime-specific configuration and payload interpretation. Preserve unknown fields only through the selected sanitised detail rules. Missing required correlation, unsupported runtime behaviour, or failed activation produces an explicit capability limit rather than guessed evidence.

## Mandatory sanitisation

Sanitise before every persistent write, at every detail level. Apply the same protection to arguments, outputs, errors, lifecycle messages, manifests, assessments, health records, and helper diagnostics. Never write raw payloads to a spool or dump them on parse failure. Configuration fingerprints may support ownership checks; configuration values must not become an unsanitized backup.

Recursively redact credential-bearing fields and recognized secret patterns, including API keys, bearer/basic authorization values, passwords, access/refresh tokens, cookies, private keys, connection-string credentials, and secrets embedded in URLs or command arguments. Replace values with explicit redaction markers rather than secret-derived stable identifiers. Avoid copying surrounding credential text into diagnostic messages.

If sanitisation or parsing fails, drop the unsafe content, write only a safe health marker where possible, and mark evidence incomplete. Full-results mode cannot disable sanitisation. Redactions remain visible in assessments because they can prevent proving an argument or result. Pattern-based detection cannot establish that every arbitrary secret is recognized; the skill states this limit and guides the agent to avoid secret-bearing probe commands and unnecessary result capture.

## Failure and recovery

Hook invocation failures must not be interpreted as no activity. Recorder health includes sanitized parse, sanitisation, write, and concurrency failures where reportable. The helper verifies a writable log and recorder before observation and checks runtime error evidence and health before assessment. Failures that leave no trustworthy health channel make coverage unknown. Auditing observes tool use; it does not change runtime fail-open/fail-closed policy for tools.

Resume inspects the durable manifest, actual registration, lease, and runtime control rather than trusting a prior agent's statement. An interrupted install can be removed using its ownership records. A stopped or expired run retains the exact removal path. If a runtime, command interpreter, trust mechanism, or cleanup operation is unavailable, report the missing capability and outstanding obligation without claiming clean completion.

## Acceptance and validation boundary

Meaningful helper tests belong under `skills/temporary-tool-auditing/tests/`. They verify sanitised on-disk bytes for representative credentials, intact concurrent records, attempt/outcome pairing and incompleteness, lease expiry and renewal gaps, crash/recovery states, preservation of unrelated hooks, ownership conflicts, and idempotent removal. Instruction behaviour checks verify honest attribution/coverage claims and persistent cleanup obligations. No exact-prose or inventory-only tests substitute for these behaviours.

Live runtime controls verify activation, parent and child capture, a completed no-tools child, tool failure and unmatched outcomes, agent-selected result detail, expiry/renewal, and post-removal unload. Use existing Devin spike evidence for demonstrated capabilities, fresh runtime controls where available, and explicit unverified limits where it cannot be repeated from Codex. Never declare a new live Devin check passed from documentation alone.

Rebuild marketplace projections from canonical sources and run the owning skill tests plus required repository and shipping gates. Return code and validation proof, runtime evidence, residual limits, and verified teardown for every installed development probe. Probe transcripts and run-specific findings remain scratch; durable runtime rules belong in the skill references.

## Evidence sources

- [Official Codex hooks](https://learn.chatgpt.com/docs/hooks).
- [Official Devin hook configuration](https://docs.devin.ai/cli/extensibility/hooks/overview).
- [Official Devin lifecycle payloads](https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks).
- [Recorded Devin Desktop capability findings](../../skills/iterative-review/references/harness-capability-floor.md).

The completed Codex scratch spike is supporting experiment evidence, not a repository authority. Its durable consequences are stated above. Existing evidence does not remove the positive-control requirements for a future consumer run.
