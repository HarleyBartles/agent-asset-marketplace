---
name: temporary-tool-auditing
description: Use when a scenario test needs bounded evidence of an agent's tool attempts, outcomes, or absence of tool use from Codex or Devin hooks.
metadata:
  source-id: temporary-tool-auditing
  source-path: skills/temporary-tool-auditing/SKILL.md
  provenance-name: Temporary Tool Auditing first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Temporary project-local hooks for sanitized, bounded tool-use evidence and verified teardown.
  use_when:
    - a scenario needs evidence that a selected agent did or did not attempt tools during a bounded run.
    - hook setup, restart, expiry, or cleanup must be tracked as part of the evidence.
  do_not_use_when:
    - general telemetry, permanent logging, policy enforcement, or tool authorization is needed.
    - the scenario requires proof about hosted tools that the runtime hooks do not observe.
license: MIT
---

# Temporary Tool Auditing

Use this skill when a scenario needs tool-use evidence. Hooks observe every agent in the runtime session, so select the subject by a captured session, agent, or Devin dispatch identifier. Evidence supports a bounded claim for verified coverage, not universal proof.

## Workflow

1. Identify the active runtime, its version, the project root, and the exact subject selector. Use the current isolated worktree when available; otherwise use the project checkout. Put run data in declared off-repository scratch or private user temporary storage, never inside the project. Choose `status` detail by default; choose `full-results` only when sanitized result content is needed to answer the scenario.
2. Resolve this skill's installed directory and use its `scripts/auditctl.py`. Run `--help`, then `prepare --check` with a unique run directory, `--runtime`, `--project`, the scenario question, `--subject session:<id>`, `agent:<id>`, or Devin `child:<dispatch-call-id>`, and the chosen `--detail`. Review the preview, then repeat with `--apply`. The default lease is 30 minutes. Set a longer or shorter positive duration only when needed.
3. Run `install --apply`. Inspect the exact project-local handler definition and the command paths. Do not write global hooks, overwrite unrelated configuration, or bypass runtime hook trust. Have your human partner review and trust the new definitions in the runtime. Restart the runtime, then run `verify --apply` to begin a two-minute activation probe. Make one harmless tool call and run `verify --apply --control-call-id <captured-call-id>`. Do not begin the scenario until activation is verified.
4. Run `start --apply`, conduct the scenario, and run `stop --apply` immediately when the selected subject completes. Stop records the operator's completion boundary; for Devin child subjects, the matching dispatch post is the completion boundary. During that dispatch, the orchestrator and other agents must make no tool calls. An explicit `renew --duration-minutes N --apply` extends the lease. If the lease expired, renewal starts a new interval only after activation is checked again; the uncovered time remains a gap. Stop does not remove the hooks or satisfy cleanup.
5. Run `assess --subject <selector>` and inspect the limitations and redaction paths. For Devin child attribution, only if the orchestrator and other agents remained idle during the serialized dispatch, run `assess --subject child:<dispatch-call-id> --confirm-parent-idle --apply`; this persists the orchestrator's positional-attribution self-attestation. Missing controls, incomplete coverage, unmatched calls, health failures, redactions, unconfirmed orchestrator idleness, or ambiguous subject attribution prevent a no-tools claim. State counts and outcome statuses as observed, with `observed-unknown` when the runtime does not establish a result.
6. Run `remove --apply`, restart the runtime, and run `verify-teardown --apply --phase begin`. Make a harmless runtime canary call, then run `verify-teardown --apply --phase finish --restart-confirmed --canary-performed`. If the cached hook records the canary, cleanup is not verified. Resolve conflicts and repeat removal, restart, and canary verification. Keep the sanitized evidence and inert recorder; do not delete run data as a shortcut.

Do not leave temporary instrumentation installed for later work. If interrupted, check the manifest first, disarm if needed, preserve the evidence, and resume removal and teardown verification. Expiry never completes cleanup. A failure, conflict, missing runtime, or uncertain restart means report cleanup as pending.

## Runtime details

- Read [Codex hook behavior](references/codex.md) before using Codex hooks.
- Read [Devin hook behavior](references/devin.md) before using Devin hooks.
- Use [evidence limits](references/evidence.md) when interpreting or reporting results.

The recorder sanitizes every persisted payload. Sanitization is a defensive filter, not a guarantee that arbitrary secrets can be recognized. Never deliberately send credentials through a test tool call. Keep full results off unless they are necessary.
