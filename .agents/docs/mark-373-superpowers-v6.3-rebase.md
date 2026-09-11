# Superpowers+ v6.3 Rebase Decisions

Canonical provenance, upstream commits, and source custody are recorded in
`codex-marketplace/plugins/superpowers-plus/SOURCE.md`. This record retains only
the decisions that cannot be reconstructed reliably from the resulting Git
diff.

## Manual merges

| upstream path | retained upstream change | first-party constraint | canonical destination |
|---|---|---|---|
| `skills/brainstorming/SKILL.md` | three-path classification and scaled ceremony | preserve marketplace metadata and authority rules | same path |
| `skills/finishing-a-development-branch/SKILL.md` | refusal-safe cleanup guidance | preserve marketplace custody and publication rules | same path |
| `skills/requesting-code-review/code-reviewer.md` | prohibit nested reviewer dispatch | preserve first-party prompt metadata | same path |
| `skills/subagent-driven-development/SKILL.md` | rulings, conflict scan, batching, and no-stall behavior | preserve the first-party execution-lane contract | same path |
| `skills/subagent-driven-development/implementer-prompt.md` | prohibit nested subagents and reviewers | preserve first-party prompt metadata | same path |
| `skills/subagent-driven-development/re-review-prompt.md` | prohibit nested reviewers | preserve first-party prompt metadata | same path |
| `skills/subagent-driven-development/task-reviewer-prompt.md` | evidence readability and batched-file checks | preserve first-party prompt metadata | same path |
| `skills/using-superpowers/references/codex-tools.md` | current Codex multi-agent and event guidance | retain the first-party Codex adapter | `skills/using-superpowers-plus/references/codex-tools.md` |
| `skills/writing-plans/SKILL.md` | plans carry their governing spec | preserve recipient-relative planning | same path |
| `skills/writing-skills/render-graphs.js` | ESM and direct executable invocation | preserve first-party skill tooling | same path |

## Deliberate exclusions

- Upstream Claude, Cursor, Devin, Gemini, Hermes, release, package, repository,
  and test-harness files were not imported because this bundle ships
  first-party Codex skills through marketplace-owned packaging and validation.
- `skills/using-superpowers/SKILL.md` was not imported as an entrypoint;
  `skills/using-superpowers-plus/SKILL.md` remains canonical.
- `skills/brainstorming/visual-companion.md` was not imported because the
  marketplace does not ship its runtime or guide.
- Upstream plans, specs, release notes, and README content were not copied into
  the active plugin tree.
