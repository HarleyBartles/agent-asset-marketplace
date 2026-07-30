# Implementing Guide

Use this reference when implementing work in the agent-asset-marketplace repo — whether as a direct implementer or as a controller dispatching implementer subagents. This guide covers the implementer workflow: what to read before starting, what skills to invoke, and what to verify before claiming done.

## Before You Begin: Read the Standards

Read these standards documents before writing any code:

- **[`docs/custody-and-projection-doctrine.md`](../../docs/custody-and-projection-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`tools/AGENTS.md`](../../tools/AGENTS.md)** — marketplace generation and validation tooling

## Skills to Invoke

- Invoke `/repo-worker-base` before any marketplace work that touches generation, validation, or tooling
- Invoke `/test-driven-development` before implementing any feature or bugfix
- Invoke `/systematic-debugging` before proposing fixes for any bug, test failure, or unexpected behavior
- Invoke `/writing-skills` when creating or editing skills

## TDD Discipline

When implementing a feature or bugfix:
1. Write a failing test first
2. Verify it fails for the right reason
3. Implement the minimum code to make it pass
4. Verify the test passes
5. Run the full suite to check for regressions

Record TDD evidence in your report: the RED command and failure output, then the GREEN command and passing output.

## Pre-Completion Verification

Before claiming work is done, verify:

- **All validation passes:** `tools/run ci --check` for CI validation
- **Marketplace regeneration succeeds:** `tools/run marketplace --apply` for local rebuild
- **Vendored output changed as intended:** If the task claims to update a vendored asset or projection, verify the published vendored output itself changed on the PR head. An overlay, manifest edit, or generator tweak is not sufficient if the resulting vendored file still shows the stale behavior.
- **Build succeeds:** All Python scripts run without errors
- **No flaky tests:** Run validation multiple times to ensure consistent results
- **Workspace clean:** No phantom files, no stray debug artifacts, no uncommitted scratch files
- **INDEX.md regenerated:** If files were added or removed, run `tools/run mesh --apply`
- **No secrets committed:** Check your diff for credentials, API keys, or connection strings
- **Skills refreshed:** If skills were modified, run `tools/run installed-skills --apply` to refresh installed skills
- **Cross-repo consumer safety:** If the work changes a vendored skill, prompt, or projection, confirm the change is safe for sister repos (e.g. under `Z:\`) that install from this marketplace. Replace repo-specific commands and paths with consumer-canonical alternatives and avoid assumptions that do not hold in the consumer's environment.

## PR, Linear, and Plan Honesty

Implementation agents are responsible for keeping PR bodies, Linear issues, and plans honest about the work they contain. This is not optional — it is part of completing the work.

- **PR bodies must be honest.** The PR body must accurately describe what the PR contains — no more, no less. Do not claim work is done if it isn't. Do not omit scope changes, deferred work, or known issues. If the PR's scope diverged from the original plan, the PR body must say so and explain why. If work was deferred, the PR body must flag it and reference the Linear issue tracking the deferral.
- **Linear issues must be updated when scope changes.** If the implementation discovers that the issue's scope needs to expand, shrink, or shift, update the Linear issue to reflect the actual work. Do not silently deliver something different from what the issue requested. If the work is complete but the scope changed, add a comment to the issue explaining the change.
- **Plans must be checked off and committed with the implementation PR.** When execution completes, mark all plan checkboxes (`- [ ]`) as done (`- [x]`) — but only after verifying that the associated plan item was actually delivered in the final PR. Do not mark items complete based on intent or in-progress work. The plan file must be committed with the PR so reviewers can see what was planned vs. what was delivered.
- **Deferred work must be tracked.** If the implementation encounters a problem that has a cheap fix (under 10 minutes), fix it — do not defer. If the fix is genuinely large, create a Linear issue to track it and reference the issue in the PR body and the task report. Silent deferral is not acceptable.

## When Dispatching Subagents

If you are a controller dispatching implementer subagents:
- Include the relevant standards doc paths in the subagent prompt — the subagent gets the AGENTS.md tree automatically, but calling out the specific docs that apply to the task ensures they read them
- Include the task brief path
- Specify the model explicitly per the SDD skill's Model Selection guidance
