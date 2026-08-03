# Tabs and lifecycle

Use these `mcp-playwright` tools to manage the browser session, tabs, and viewport.

| Tool | When to use it | Required inputs | Optional inputs |
| --- | --- | --- | --- |
| `browser_resize` | Set viewport size | `width`, `height` | — |
| `browser_tabs` | List or switch tabs | — | `action`, `tabId` |
| `browser_wait_for` | Wait for an event or timeout | `time` or `selector` | — |
| `browser_close` | Close the page | — | — |

## Fast rules

1. **Close at the end.** Run `browser_close` when the browser task is done.
2. **Avoid arbitrary waits.** Use `browser_wait_for` with a concrete `selector` whenever possible.
3. **Resize to a desktop/mobile size only when the task requires it.**
