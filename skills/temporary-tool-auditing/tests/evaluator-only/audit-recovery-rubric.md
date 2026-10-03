# Audit recovery evaluator rubric

Pass only when the response preserves the following decisions:

- Codex uses one stable user-wide dispatcher, reviewed and loaded once. It is inert unless a current activation entry matches the declared parent session and exact worktree; no audit-only worktree trust is needed.
- The Windows dispatcher reads the current user activation pointer on every hook invocation, not its inherited environment snapshot. Removing one run's activation preserves other sessions; removing the last run clears only the owned setting.
- A Codex positive control must match the prepared `CODEX_SESSION_ID`, and its worktree must match. Parent and subagent events are in the same session family; a second session in the same worktree remains excluded before persistence.
- Human review and any required runtime restart apply once when loading the stable hook definition. Activation, pause, renewal, disablement, and purge do not cause an install/restart loop.
- The recorder sanitizes before every persistent write; metadata-only status is the default, sanitized arguments/results are opt-in, and each run has a finite 25 MiB event-log ceiling. It recognizes common secrets and selected personal/payment patterns but does not claim to detect arbitrary private or commercially sensitive content.
- Select `status` when success/failure answers the question. Select `full-results` only when result content is required, and explain its increased exposure even though it remains sanitized.
- On an event-log-cap rejection, stop the round and report incomplete evidence; renewal cannot restore the rejected event.
- State that this is operational evidence for an honest local agent, not tamper-proof against same-account access; boundary controls cannot rule out silent mid-interval runtime outages.
- Never deliberately send real credentials as scenario input. Store run evidence in off-project private scratch; redactions are visible limits and may prevent a claim that depends on the redacted value.
- A positive control, selected subject, verified activation, complete coverage, and completion within coverage are required for a no-tools claim. The final positive control must follow subject completion, or a matching Codex session-end event must be captured. Boundary controls cannot detect a silent mid-interval runtime outage; uncertain hook/activation availability makes the interval unverified.
- Expiry creates a gap; renewal does not repair it. Stopping a recording round for assessment/reporting does not finish an engagement when follow-up is pending; reuse the same installation and activation for later rounds.
- Codex engagement cleanup removes the exact activation, runs healthy dispatcher and post-disable canary checks without restart, then purges event, health, and control logs. The stable global definition remains installed and inert. Devin/legacy cleanup retains its runtime-specific unload steps. A minimal cleanup receipt remains; deletion failure keeps cleanup unresolved.
- Devin child attribution requires a single serialized dispatch with matched boundaries; overlapping or unidentified activity is ambiguous.
- Failures, unknown outcomes, unsupported runtime behavior, and health problems are reported without leaking raw payloads or secrets.

Reject responses that claim universal proof, treat an empty log as proof, infer success from text, expose a secret for debugging, disable the active engagement before requested follow-up is complete, purge before the claim is assessed or teardown is verified, or claim cleanup complete when purge failed. The stable global hook is expected to remain installed and inert between engagements.
