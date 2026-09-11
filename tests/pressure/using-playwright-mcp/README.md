# Pressure test — `using-playwright-mcp`

## Scenario

A page shows a "Saving..." label. After a save action, the agent must wait until the label disappears before proceeding.

## Method

Two isolated agents were given the same task:

- **RED (baseline):** No access to the `using-playwright-mcp` skill; could only reason over the live `mcp_list_tools` output for `mcp-playwright`.
- **GREEN (with skill):** Could read `using-playwright-mcp` and its references.

Judge whether the guided agent reaches `browser_wait_for` with
`textGone: "Saving..."` directly from the skill references, while the baseline
must discover the same capability from the available tool surface. Report the
comparison in the current handoff; do not commit either response or verdict.
