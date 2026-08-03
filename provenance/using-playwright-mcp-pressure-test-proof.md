# Pressure-test proof — `using-playwright-mcp`

## Scenario

A page shows a "Saving..." label. After a save action, the agent must wait until the label disappears before proceeding.

## Method

Two isolated agents were given the same task:

- **RED (baseline):** No access to the `using-playwright-mcp` skill; could only reason over the live `mcp_list_tools` output for `mcp-playwright`.
- **GREEN (with skill):** Could read `using-playwright-mcp` and its references.

Both agents wrote their own reports:

- [pressure-test-red.md](pressure-test-red.md)
- [pressure-test-green.md](pressure-test-green.md)

## Result

Both agents eventually chose `browser_wait_for` with `textGone: "Saving..."`.

- **RED path:** The tool list returned by `mcp_list_tools` was truncated, so the agent had to locate the saved overflow dump, search it for wait-related `browser_*` names, and read the `browser_wait_for` schema. It chose correctly but spent extra reasoning and context on tool discovery.
- **GREEN path:** The skill routed the intent to `references/tabs-and-lifecycle.md`, confirmed `browser_wait_for` in `references/surface-map.md`, and the exact scenario was already described in `assets/pressure-tests.md`. The choice was mechanical, accurate, and fast.

## Conclusion

The `using-playwright-mcp` skill turns a discovery-and-search problem (which can fail or waste tokens when the MCP tool list is truncated) into a direct routing decision. For this scenario it reduced the agent's surface search space from a large, truncated tool list to a single reference file and a single tool call.
