# Codex hooks

Codex loads hooks from active user and project configuration layers. Project hook configuration belongs in `<project>/.codex/hooks.json`; Codex merges matching hooks from active sources rather than replacing lower-level sources. It skips project hooks unless the project `.codex/` layer is trusted. A changed, non-managed hook definition requires human review and trust before it runs.

The runtime reads hook definitions at session start. After installation, have your human partner inspect and trust the exact generated handlers, then restart Codex before testing activation. After removal, restart again and test a harmless tool canary before declaring teardown complete. The user's approval of an earlier hook definition does not automatically trust a changed definition.

The recorder listens to `PreToolUse`, `PostToolUse`, `SubagentStart`, `SubagentStop`, `SessionStart`, and `SessionEnd`. Hook payloads include `session_id`, `hook_event_name`, `tool_name`, and `tool_input`; tool events carry `tool_use_id`. Subagent events can carry `agent_id`. Missing IDs remain missing. Main-thread tool events may not have an agent ID, so a session selector and an agent selector mean different scopes.

The handler command includes an absolute interpreter and recorder path, with a Windows-specific command for Windows Codex. The recorder exits successfully with no stdout so it does not return a decision or alter a tool call. Hosted tools are outside this local command-hook evidence boundary. The Codex documentation also cautions that specialized paths can opt out of the normal hook path, so describe coverage honestly.

Codex hook configuration, event contracts, trust, and tool coverage are described in the [official Hooks reference](https://learn.chatgpt.com/docs/hooks). Check it again when runtime behavior changes.
