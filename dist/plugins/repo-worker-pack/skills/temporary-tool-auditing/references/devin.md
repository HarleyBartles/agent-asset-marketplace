# Devin hooks

The supported Devin shape here is grounded in the recorded Marketplace capability probe at [the harness capability floor](../../iterative-review/references/harness-capability-floor.md). That probe observed project-installed `.devin/hooks.v1.json` handlers and `PreToolUse` / `PostToolUse` payloads with `session_id`, `prompt_id`, `tool_name`, `tool_input`, `tool_use_id`, and `hook_event_name`. The evidence is historical; verify the active Devin runtime before relying on it.

The recorded probe found hooks are loaded when the session starts. Install the rendered project-local file, review it, and start or restart the Devin session before measuring capture. Remove the project-local entries and repeat the runtime canary check after restart. Do not adapt Codex's configuration shape by assumption; the adapters keep runtime handlers separate.

The probe found no child `agent_id` in hook records. Its only supported child attribution was positional: capture one `run_subagent` dispatch at a time, with a matched start and completion, and attribute inner hook events between those boundaries. Concurrent dispatches or unidentified activity make child attribution ambiguous. Use the dispatch call ID as the `child:<dispatch-call-id>` selector. If the current runtime payload no longer matches these observed fields, stop and report unsupported runtime capability rather than guessing.

The public [Devin documentation](https://docs.devin.ai/) does not currently define this local hook contract. This reference therefore labels the runtime semantics as recorded evidence, not as a vendor guarantee. Recheck the linked repository evidence and run a fresh live control when using a materially different Devin version.
