# Implementing Runbook

Use this reference for repository-specific implementation commands,
marketplace custody, and completion checks in agent-asset-marketplace.

## Before You Begin: Read the Standards

Read these standards documents before writing any code:

- **[`.agents/doctrine/custody-and-marketplace-doctrine.md`](../../.agents/doctrine/custody-and-marketplace-doctrine.md)** — source custody rules, provenance modes, plugin curation rules
- **[`.devin/rules/tools.md`](../../.devin/rules/tools.md)** — marketplace generation and validation tooling

## Workflow routing

Invoke `using-superpowers-plus` once and follow its implementation handoff.
This runbook supplies only marketplace-specific constraints.

## Pre-Completion Verification

Before claiming work is done, verify:

- **Current-state validation passes:** use the repository's canonical gate for
  the exact tree/staged state being claimed. A normal commit uses the tracked
  pre-commit gate; run `tools/run ci --check` separately only for uncommitted
  verification, diagnosis, or explicit CI-parity evidence.
- **Marketplace regeneration succeeds:** `tools/run marketplace --apply` for local rebuild
- **Vendored output changed as intended:** If the task claims to update a vendored asset or marketplace bundle, verify the published vendored output itself changed on the PR head. An overlay, manifest edit, or generator tweak is not sufficient if the resulting vendored file still shows the stale behavior.
- **Build succeeds:** All Python scripts run without errors
- **Repeat only when justified:** rerun when the state changed, a check failed,
  nondeterminism is suspected, the environment drifted, or a different claim
  needs proof.
- **Workspace clean:** No phantom files, no stray debug artifacts, no uncommitted scratch files
- **INDEX.md regenerated:** If files were added or removed, run `tools/run mesh --apply`
- **No secrets committed:** Check your diff for credentials, API keys, or connection strings
- **Generated skills refreshed:** If canonical marketplace skills were modified,
  run `py -3 tools/run.py marketplace --apply`; never hand-edit downstream
  installed copies to bypass source review.
- **Runtime subagent profiles synced:** If `reviewer-*.md` profiles in the Devin Desktop agents search path or other subagent profiles were added or changed, run `py -3 tools/run.py runtime-agents --apply --allow-shared-checkout` to stage them in the main checkout. Restart the IDE before dispatching `run_subagent` with the new profiles.
- **Cross-repo consumer safety:** If the work changes a vendored skill, prompt, or marketplace bundle, confirm the change is safe for sister or consumer repos that install from this marketplace. Replace repo-specific commands and paths with consumer-canonical alternatives and avoid assumptions that do not hold in the consumer's environment.
- **Self-review against lens checklists:** Before handoff, read the relevant `reviewer-*.md` profiles in the Devin Desktop agents search path `## Checklist` profiles (at minimum `reviewer-skills`, `reviewer-marketplace`, and `reviewer-security` for the surfaces you touched). Run the checklist mechanically against your diff and fix anything you can. The goal is to make the reviewer loop a mechanical verification, not a bug-hunting exercise. This self-review is not a substitute for the `iterative-review` lens/strong dispatch; it only reduces the number of findings the reviewers must find.

## PR, Linear, and Plan Honesty

Implementation agents are responsible for keeping PR bodies, Linear issues, and plans honest about the work they contain. This is not optional — it is part of completing the work.

- **PR bodies must be honest.** The PR body must accurately describe what the PR contains — no more, no less. Do not claim work is done if it isn't. Do not omit scope changes, deferred work, or known issues. If the PR's scope diverged from the original plan, the PR body must say so and explain why. If work was deferred, the PR body must flag it and reference the Linear issue tracking the deferral.
- **Scope changes must stay honest without inventing Linear authority.** If implementation discovers that scope must expand, shrink, or shift, report the divergence in the plan/PR evidence. When durable issue tracking needs a Linear mutation, route it through the Linear-owning workflow and its authority contract; this runbook does not itself authorize creating or updating Linear issues.
- **Plans must be checked off before the PR can claim completion.** When execution completes, mark all plan checkboxes (`- [ ]`) as done (`- [x]`) — but only after verifying that the associated plan item was actually delivered in the final PR. Do not mark items complete based on intent or in-progress work. The plan file must be committed with the PR so reviewers can see what was planned vs. what was delivered. If the PR does not finish the whole plan, do not claim the plan is "implemented" or "complete" in the PR body; instead, describe what was delivered and what remains.
- **Completing the plan is the implementer's job, not the reviewer's.** Do not hand a PR off to review with an unchecked or partially checked plan and expect reviewers to catch the gaps. Review-stage handoff is valid only when the implementation, the plan checkboxes, and the PR body are already aligned.
- **Fix-while-here is bounded.** Repair a discovered defect inline only when it is low-risk, mechanically bounded, and on the touched surface. Do not turn the current task into a new product/architecture choice, migration, or validation campaign. Anything outside that boundary is reported as deferred work; if durable tracking is authorized, use the owning tracking workflow rather than creating external state from this runbook.

## When Dispatching Subagents

If you are a controller dispatching implementer subagents:
- Include the relevant standards doc paths in the subagent prompt — the subagent gets the AGENTS.md tree automatically, but calling out the specific docs that apply to the task ensures they read them
- Include the task brief path
- Specify the model explicitly per the SDD skill's Model Selection guidance
