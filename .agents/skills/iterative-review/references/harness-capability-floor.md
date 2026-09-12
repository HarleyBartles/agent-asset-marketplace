# Devin harness capability floor

The version-2 evidence kernel depends on a small set of harness capabilities.
`reviewctl doctor` currently detects the runtime only: it reports `pass` on
Devin Desktop and `inert` (exit 1) on any other runtime, and mutation commands
refuse off-Devin runtimes with `unsupported-runtime` rather than silently
degrading to assertion-based evidence. Re-checking each capability row below
at review intake is planned for a later plan; until then the rows record the
empirical floor the kernel was designed against, not a live gate.

This document records the empirical basis for each requirement. Two evidence
classes are cited:

- **live** - reproduced during Plan 1 Task 0 in the current session.
- **recorded** - verbatim artifacts retained from the capability spike under
  the review scratch root, hash-bound below.

Recorded artifacts (scratch, disposable):

```text
<scratch-root>/<repo>/<branch>/capability-floor/
  pretool.jsonl       sha256 f490927ba270151168464c45852052f96a180133c66e9738886378e7af028688
  posttool.jsonl      sha256 09355375713fb0b759ae4d1ea96e1b3ab35414f9a21aa66148cf01fb7a479197
  SPIKE-FINDINGS.md   sha256 4bc884f53776731ee4f08e33124eb572b4d9404f2af18d461ef3785717ddde27
```

## Capability matrix

| Capability | Status | Evidence |
| --- | --- | --- |
| Devin runtime detected; non-Devin stays inert | PASS | live: `doctor` precondition is `runtime == devin-desktop`; all other runtimes return `unsupported-runtime` and mutate nothing |
| PreToolUse/PostToolUse hook records emitted for orchestrator calls | PASS | recorded: 263 PreToolUse / 245 PostToolUse records, one session, every call captured (`pretool.jsonl`, `posttool.jsonl`) |
| Hook records carry `session_id`, `prompt_id`, `tool_name`, `tool_input`, `tool_use_id`, `hook_event_name` | PASS | recorded: field set verified verbatim on all records; a single `session_id` persisted throughout |
| Hook records emitted for subagent dispatches and inner subagent tool calls | PASS | recorded: 12 `run_subagent` launches + 12 completions; inner calls (`edit`, `exec`, `read`, `grep`, `write`) all carry the parent `session_id` |
| Subagent inner calls carry the correlation field needed for positional attribution | PASS-with-constraint | recorded: inner calls share `session_id` but no `agent_id` field exists in hook records; attribution is positional (records between launch and completion), so reviewer dispatches must serialize |
| `session_id` survives IDE restart; `prompt_id` rotates per prompt | PASS | recorded + live: the same `session_id` persisted across restart; 16 distinct `prompt_id` values |
| `allowed-tools` confines a subagent profile to read/search-only | PASS | live: `subagent_explore` reported exactly `code_search, find_file_by_name, get_output, grep, notebook_read, read, web_search`; no `exec`/`write`/`edit`/`webfetch`/`mcp_call_tool`/`run_subagent` |
| Permission deny rules block canary reads and writes, including inside `exec` command text | PASS | recorded: `Read(...CANARY-*)`, `Write(...)`, `Edit(...)` deny rules all refused; deny evaluation reaches `exec` command strings |
| Deny refusal terminates or blocks the call, not just logs | PASS | recorded: canary write through `exec` ended the turn; canary read through `read` soft-denied and the run continued |
| File tools reject out-of-workspace paths before deny evaluation | PASS | recorded: a second confinement layer exists; out-of-workspace `read`/`write` are refused by the tool layer itself |
| `ask_user_question` PostToolUse captures the literal user selection | PASS | recorded: response output contained `"selected": ["Alpha"]`, `skipped: false`; `human-decision` witnesses bind the real answer |
| `gh` authenticated; check-run/workflow-run remote observation on a pushed SHA | PASS | live: `gh auth status` active; a check-run record (app `github-actions`) carried `id`, `head_sha`, and `conclusion` fields; workflow-runs carry `id`, `run_attempt`, `run_number`, `head_sha`, `conclusion` |
| `gh pr ready` transitions draft to ready; idempotent; reversible via GraphQL `convertPullRequestToDraft` | PASS | recorded: a disposable PR exercised the full transition, repeat call exited 0 ("already ready"), re-fetch via `isDraft` reconciled, re-draft mutation verified |
| Required subagent profiles resolve from the user-global profile root | PASS | live: `subagent_explore` dispatched successfully |
| Profiles defined inside the reviewed head cannot qualify a dispatch | PASS | live: `.devin/agents/self-qualify-probe.md` created in the reviewed tree; `run_subagent profile="self-qualify-probe"` failed to start |
| Review scratch creatable under canonical off-repo root | PASS | live: `<scratch-root>/<repo>/<branch>/capability-floor/` created, artifacts written |
| Hash-chained witness log: intact chain verifies, tampered entry detected | PASS | live: two-entry chain built in `witness-store/`; byte-level edit of entry 0 failed verification |

## Findings that constrain the design

1. **No `agent_id` in hook records.** Dispatch attribution is positional only.
   The kernel requires serialized reviewer dispatches; concurrent background
   dispatches interleave in the transcript and cannot be attributed.
2. **Hooks are observe-and-block only.** A PreToolUse hook emitting
   `updatedInput` was ignored by the runtime; the tool ran on the original
   input. Hooks cannot rewrite tool calls.
3. **Hook config loads at session start.** Installing or removing hooks
   mid-session has no effect until restart. Live verification of hook
   emission therefore requires the hooks pack to have been installed before
   the session began; the per-row `doctor` recheck that will report
   `capability-floor-failed` with a remediation pointer is deferred to a
   later plan (today `doctor` reports runtime support only).
4. **Model identity is not self-declared.** `subagent_explore`'s prompt
   carried no model name; reviewer-model pinning must come from the profile
   frontmatter at the user-global root, verified by the planned doctor
   recheck, not from agent self-report.

## doctor verdict for this session

`PASS` on Devin Desktop with the recorded floor above. `INERT` on
Codex/OpenAI-compatible runtimes by contract.
