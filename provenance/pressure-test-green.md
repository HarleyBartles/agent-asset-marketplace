# Pressure test — waiting for "Saving..." to disappear

## 1. Tool chosen

`mcp_call_tool` with `server_name: "mcp-playwright"`, `tool_name: "browser_wait_for"`.

## 2. Exact inputs

```json
{
  "server_name": "mcp-playwright",
  "tool_name": "browser_wait_for",
  "arguments": {
    "textGone": "Saving...",
    "time": 30
  }
}
```

## 3. Reasoning

The task is a classic "wait for an element/text to disappear after an action" scenario.

- `SKILL.md` (line 23-31) routes "manage tabs, resize, wait, or close the browser" to [`references/tabs-and-lifecycle.md`](references/tabs-and-lifecycle.md).
- `references/tabs-and-lifecycle.md` (line 9) identifies `browser_wait_for` as the correct MCP tool and recommends using a concrete selector or condition whenever possible.
- `references/surface-map.md` (line 25) confirms `browser_wait_for` exists under "Wait for an event or timeout".
- Live `mcp_list_tools` for `mcp-playwright` returned the exact schema for `browser_wait_for`, showing the supported properties:
  - `text` — wait for text to appear
  - `textGone` — wait for text to disappear
  - `time` — wait time in seconds
- `assets/pressure-tests.md` (line 20-25) explicitly shows the GREEN path for this scenario: call `browser_wait_for` with `textGone: "Saving..."` and a `time` value.

Using `textGone: "Saving..."` makes the tool wait until the label is no longer present in the page snapshot, instead of polling with `browser_find` or writing JavaScript loops.

## 4. Risks and caveats

- **Text must be in the accessibility snapshot.** If the "Saving..." label is rendered in a way that Playwright's snapshot does not see (e.g., `aria-hidden`, a background image, or canvas), `textGone` may not be satisfied and the call will time out.
- **Race with the save action.** The `browser_wait_for` call must be issued *after* the save interaction has been triggered (e.g., after `browser_click`). If the label has not appeared yet because the request is still starting, the waiter may see the label already gone and return immediately.
- **Timeout selection.** The `time` value is a maximum. If 30 seconds is too short for the save operation on slow networks, increase it. If the label gets stuck, the call will fail cleanly with a timeout instead of blocking forever.
- **Truncated tool lists.** `mcp_list_tools` for `mcp-playwright` can be large and truncate; the skill files provide the reliable map that pointed directly to `browser_wait_for`.
- **Multiple matching elements.** If several elements contain "Saving...", `textGone` will be satisfied when all of them disappear. If you only care about one, a `selector` or `target`-based wait may be more precise, but the MCP `browser_wait_for` schema is limited to text and time properties.
