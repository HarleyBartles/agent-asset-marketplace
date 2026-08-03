# Pressure Test Red: Waiting for the "Saving..." label to disappear

## 1. Tool chosen

`browser_wait_for` from the `mcp-playwright` MCP server.

## 2. Exact inputs

```json
{
  "textGone": "Saving..."
}
```

Optionally, a timeout can be added if the save is expected to finish within a known bound, e.g.:

```json
{
  "textGone": "Saving...",
  "time": 30
}
```

## 3. Reasoning

The task is to wait until the "Saving..." label is gone before proceeding. The `browser_wait_for` tool is the only one whose description explicitly covers this: "Wait for text to appear or disappear or a specified time to pass". It exposes a `textGone` parameter whose description is "The text to wait for to disappear", which is the exact condition we need to observe.

The initial `mcp_list_tools` output was truncated, so I used the saved full tool-list overflow file and searched it for wait-related names. That search surfaced `browser_wait_for` (line 797 of the overflow dump). Once the exact schema was read, `textGone` was the obvious match.

Using `browser_wait_for` with `textGone: "Saving..."` means the Playwright MCP server will not return until the "Saving..." text is no longer present in the page (accessibility snapshot). This naturally blocks the next action, satisfying the requirement.

## 4. Risks and workarounds if the best tool is not visible

- **Truncated list hides `browser_wait_for`:** Even if the tool was not visible in the truncated output, the saved overflow can be grepped for `browser_` names to locate wait-related tools. As a last resort, `mcp_call_tool` can be invoked with `browser_wait_for` anyway; the tool may still exist server-side even if the client listing was truncated.
- **Missing/fallback tools:** If `browser_wait_for` is genuinely unavailable, the next best options are:
  - `browser_evaluate` with a function such as `() => !document.body.innerText.includes("Saving...")`, called repeatedly until it returns `true`.
  - `browser_find` with `text: "Saving..."` to check presence; if it is still present, wait a short fixed interval and search again.
- **Match precision:** `textGone` likely requires the exact text. If the label contains surrounding whitespace or mixed case, the exact string should be adjusted, or `browser_evaluate` should be used with a normalized string comparison instead.
- **Visual vs. snapshot gone:** If the label is merely hidden or `opacity: 0` but still in the DOM, `textGone` may count it as gone because the accessibility snapshot no longer exposes it. This is usually acceptable for a wait-for-disappear check, but if the semantic is "element no longer exists", an explicit DOM query via `browser_evaluate` is more precise.
