---
name: selecting-a-subagent
description: Use when choosing a child subagent profile, model, reasoning level, or
  context mode for a task.
metadata:
  source-id: selecting-a-subagent
  source-path: codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md
  provenance-name: Selecting A Subagent first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when choosing a child subagent profile, model, reasoning level, or context
    mode, or when retrying failed work by changing profile, model, reasoning, or context.
  use_when:
  - Use before calling `spawn_agent` or an equivalent subagent tool.
  - Use when creating or selecting a named subagent configuration.
  - Use when recommending a child model, reasoning level, or context mode.
  - Use when retrying failed work by changing model, reasoning, or context.
  - Use when choosing a custom subagent profile such as `reviewer`, `reviewer-fast`,
    `reviewer-strong`, `reviewer-security`, `reviewer-marketplace`, `reviewer-references`,
    `implementer`, or `implementer-strong`.
  - Use when selecting an implementation, code-review, architecture-review, or adjudication
    agent.
  do_not_use_when:
  - Do not use to switch the current parent session when the runtime cannot change
    models mid-session.
  - Do not use when another more specific skill owns the task.
  related_skills:
  - dispatching-parallel-agents
  - risk-gates
  - repo-worker-base
  use_after:
  - inspecting-the-environment
license: MIT
---
# Selecting a Subagent

Use this skill before choosing a child subagent route. Detect the live dispatch
contract, load the shared policy and exactly one matching environment profile,
then choose the least escalated route the runtime actually exposes.

## Runtime contract

1. Detect the active child-dispatch contract.
2. Inventory the models, reasoning values, context controls, and capacity actually exposed.
3. Load `references/shared-policy.md` and exactly one matching profile.
4. Treat current runtime inventory as authoritative over stale profile metadata.
5. Choose the least escalated adequate exposed route; do not infer price or entitlement.
6. Record the profile, model or inheritance, reasoning or inheritance, context mode, rationale, and material limitation.
7. State explicitly when a desired route could not be enforced.

Routing chooses a route; it does not authorize delegation. Follow the current
task, environment, and repository rules before calling a child-dispatch tool.

## Profiles

| Live dispatch signature | Profile |
|---|---|
| `multi_agent_v1__spawn_agent` with Boolean `fork_context` | `references/codex-multi-agent-v1-profile.md` |
| `spawn_agent` with `fork_turns` | `references/codex-multi-agent-v2-profile.md` |
| Devin Desktop | `references/devin-desktop-profile.md` |
| Unknown or non-Codex runtime | `references/generic-free-first-profile.md` |

## Installing the custom profiles

The `.md` profile assets in `assets/` are Devin Desktop custom profiles. They are
not used by Codex; for Codex, use the `references/codex-multi-agent-v1-profile.md`
or `references/codex-multi-agent-v2-profile.md` mappings.

If you want to use the Devin Desktop custom profiles, install the corresponding
`.md` profile assets into a Devin Desktop profile search path:

- macOS/Linux: `~/.config/devin/agents/<profile>.md`
- Windows: `%APPDATA%\devin\agents\<profile>.md`

For example, copy `assets/implementer.md` to
`~/.config/devin/agents/implementer.md`, and do the same for `reviewer`,
`reviewer-fast`, `reviewer-strong`, `implementer`, and `implementer-strong`.

## Common custom subagent profile dispatch

| Task | Profile |
|---|---|
| Most review tasks, focused re-reviews, and architecture challenges | `reviewer` |
| Full branch/PR diff review where the whole branch is in scope | `reviewer-strong` |
| Security and PII lens in a full-branch/PR diff | `reviewer-security` |
| Marketplace, scaffolder, and generated-surface lens | `reviewer-marketplace` |
| SKILL.md, reference-file, markdown, and prompt-robustness lens | `reviewer-references` |
| Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fast` |
| Bounded implementation / bugfix | `implementer` |
| Implementation that needs more reasoning or broader context | `implementer-strong` |

The orchestrator must provide a `<diff_path>` and optional `<pr_description>` to any
reviewer profile. The reviewer subagent does not resolve the diff itself.

## Vendor and third-party profiles

Marketplace packs can ship third-party subagent `.md` profile assets under
`assets/profiles/`. The `refreshing-installed-skills` script copies those
profiles into the consumer's agent search path at `.agents/agents/` only
when a file of the same name does not already exist, and records them in
`.agents/skills/.provenance.json` under a `vendorProfiles` array.

When choosing a profile, apply this precedence:

1. Repo-local override (a hand-authored `.agents/agents/<name>.md` or a
   `.devin/agents/<name>.md` user-local override) wins.
2. Vendor profile installed from a marketplace pack (`.agents/agents/`).
3. Built-in custom profiles documented in
   `references/devin-desktop-profile.md` and the dispatch profiles above.
4. User-global profiles (`~/.config/devin/agents/` or
   `%APPDATA%\devin\agents\` on Windows).

No skill should create or pressure the consumer to create `.devin/agents/`.
`.agents/agents/` is the canonical surface for plugin-installed profiles.

Prefer a vendor profile when a pack ships one that matches the task role
(e.g. a pack-provided `reviewer.md`) and no repo-local override exists. Prefer
a repo-local override when the repo needs behavior the vendor profile does not
capture. See `references/vendor-profile-packaging.md` for the packaging
contract and the consumer search-path order.

## Common pressure

When the obvious choice is unclear or contested, read `references/pressure-scenarios.md` first.
