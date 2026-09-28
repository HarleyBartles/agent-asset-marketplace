# Choosing a Jev tool

Use the specific preset for a bounded question. Each result is advisory; the caller applies its own policy and performs any action.

| Decision boundary                                                 | Tool                    | Required fields                                  |
| ----------------------------------------------------------------- | ----------------------- | ------------------------------------------------ |
| Select among at least two eligible models                         | `jev_route_model`       | `task`, `candidates` with `id` and `description` |
| Choose a next task path from the preset options                   | `jev_route_task`        | `task`                                           |
| Assess a consequential tool call                                  | `jev_guard_tool_call`   | `tool`, `action`                                 |
| Judge whether supplied evidence supports a claim                  | `jev_check_research`    | `claim`                                          |
| Assess whether an objective appears complete                      | `jev_review_completion` | `objective`                                      |
| Ask a bounded Choice, Score, or Noul question when no preset fits | `jev_decide`            | `state`, `questions`                             |

Use only the tool whose decision is needed. `jev_check_research` does not retrieve evidence, `jev_review_completion` does not replace validation, and `jev_guard_tool_call` does not grant approval. If a tool's current schema differs from this reference, follow its live schema without weakening the owning workflow's constraints.

Calls consume the service's decision quota. Do not send an entire repository, private document, credential, or long conversation when a small state summary is sufficient. The plugin's `SOURCE.md` records the service documentation used for this reference.
