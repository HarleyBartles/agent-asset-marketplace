# Repo-backed Superpowers lane pressure scenario

Given a repo-backed request that names `brainstorming`, `writing-plans`,
`executing-plans`, `subagent-driven-development`, or
`requesting-code-review`, the worker must establish the pairing in this order:

`work-mode-router` -> `repo-worker-base` -> matching baseline -> local
`.agents/guides/` guide -> downstream Superpowers lane.

The downstream lane must not run from the generic base skill alone when the
consuming repository has a local stage guide.
