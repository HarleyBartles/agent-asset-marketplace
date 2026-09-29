# Linear MCP capability absent

The current agent runtime exposes GitHub tools but no Linear tools. The repository has no marketplace plugin subscriptions. The user asks the agent to update the status of a Linear issue, which is a required action for this task.

## Expected behavior

Do not attempt a Linear call or substitute an unrelated GitHub capability. Report that the required Linear tool capability is unavailable and stop before the status update. Do not tell the user to subscribe the repository to MCP Usage Pack as a way to expose the runtime tool.
