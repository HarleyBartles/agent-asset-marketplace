---
name: selecting-a-subagent
description: Use when choosing a child subagent profile, model, reasoning level, or context mode for a task.
metadata:
  source-id: selecting-a-subagent
  source-path: skills/selecting-a-subagent/SKILL.md
  provenance-name: Selecting A Subagent first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  use_when:
    - a `spawn_agent` or equivalent subagent call is about to be made.
    - creating or selecting a named subagent configuration.
    - recommending a child model, reasoning level, or context mode.
    - retrying failed work by changing model, reasoning, or context.
    - choosing a custom subagent profile such as `reviewer`, `reviewer-fixes`, `reviewer-strong`, `reviewer-security`, `reviewer-skills`, `reviewer-plans`, `reviewer-scripts`, `implementer`, or `implementer-strong`.
    - selecting an implementation, code-review, architecture-review, or adjudication agent.
  do_not_use_when:
    - to switch the current parent session when the runtime cannot change models mid-session.
    - another more specific skill owns the task.
  related_skills:
    - dispatching-parallel-agents
    - risk-gates
    - repo-worker-base
    - inspecting-the-environment
    - conducting-code-review
license: MIT
---

# Selecting a Subagent

## Bundled helper paths

Resolve a bundled helper under its owning skill directory supplied by the active runtime. In examples, `<runtime-skill-path-for-selecting-a-subagent>` means this skill's runtime location; do not assume a consumer `.agents/skills/` projection.

Use this skill before choosing a child subagent route. Detect the live dispatch contract, load the shared policy and exactly one matching environment profile, then choose the least escalated route the runtime actually exposes.

## Runtime contract

1. Detect the active child-dispatch contract.
2. Inventory exposed models, reasoning, context and capacity. For review, also check actual repository, skill/catalog, authoritative retrieval, focused execution/scratch and report-writing access; model adequacy alone does not establish capability adequacy.
3. Load `references/shared-policy.md` and exactly one matching profile.
4. Treat current runtime inventory as authoritative over stale profile metadata.
5. Choose the least escalated adequate exposed route; do not infer price or entitlement.
6. Record profile, model or inheritance, reasoning or inheritance, context mode, rationale, actual review-resource access and material limitations separately.
7. State explicitly when a desired route could not be enforced.

Routing chooses a route; it does not authorize delegation. Follow the current task, environment, and repository rules before calling a child-dispatch tool.

The workflow or stage owner decides whether delegation is warranted at all. This selector is only the second decision: if delegation is warranted, choose the least-escalated adequate profile, model, reasoning, and context mode that the live runtime exposes. Do not delegate merely because a reviewer profile exists, and do not escalate to Astra when Sol or a less capable adequate route can satisfy the contract.

## Profiles

| Live dispatch signature                                   | Profile                                      |
| --------------------------------------------------------- | -------------------------------------------- |
| `multi_agent_v1__spawn_agent` with Boolean `fork_context` | `references/codex-multi-agent-v1-profile.md` |
| `spawn_agent` with `fork_turns`                           | `references/codex-multi-agent-v2-profile.md` |
| Devin Desktop                                             | `references/devin-desktop-profile.md`        |
| Unknown or non-Codex runtime                              | `references/generic-free-first-profile.md`   |

## Installing the custom profiles

The `.md` profile assets in `assets/` are Devin Desktop custom profiles. They are not used by Codex; for Codex, use the `references/codex-multi-agent-v1-profile.md` or `references/codex-multi-agent-v2-profile.md` mappings.

If you want to use the Devin Desktop custom profiles, run the helper to install the shipped `.md` assets into the user-global Devin Desktop agents directory:

```
py -3 <runtime-skill-path-for-selecting-a-subagent>/scripts/install_profiles.py --apply
```

The helper overwrites shipped profiles only when they have changed and leaves any other files in the target directory untouched. The default target is:

- macOS/Linux: `~/.config/devin/agents/`
- Windows: `%APPDATA%\devin\agents\`

Use `--target` to install to a different directory, such as a consumer repository's `.agents/agents/` directory.

Do not install repo-local `<lens>.md` profiles from the pack. The consumer repo authors its own `.agents/agents/reviewer-<lens>.md` files (or omits them) for its own domain-specific surfaces.

## Common custom subagent profile dispatch

| Task                                                                    | Profile             |
| ----------------------------------------------------------------------- | ------------------- |
| Most review tasks, focused re-reviews, and architecture challenges      | `reviewer`          |
| Full branch/PR diff review where the whole branch is in scope           | `reviewer-strong`   |
| Security and PII lens in a full-branch/PR diff                          | `reviewer-security` |
| `SKILL.md`/reference/prompt-robustness lens                             | `reviewer-skills`   |
| Plans, specs, or roadmap changes at the repository's declared locations | `reviewer-plans`    |

| Script safety, CLI compliance, shebangs, or `--check`/`--apply` classification | `reviewer-scripts` | | Small, tightly focused reviews or coherent single-responsibility re-review diffs | `reviewer-fixes` | | Repo-specific lens for surfaces not covered by the portable set | `.agents/agents/reviewer-<lens>.md` (see below) | | Bounded implementation / bugfix | `implementer` | | Implementation that needs more reasoning or broader context | `implementer-strong` |

The dispatcher supplies the prepared `<diff_path>` and scope/context, actual conducting-code-review skill entrypoint, usable resource/catalog entrypoints, reviewed checkout/revision, known capability limits, owned proof scratch and report destination. Supply a catalog if a fresh child does not receive one. A globally installed Devin profile cannot resolve a skill through an assumed relative path. The reviewer does not recreate missing packages; unavailable research or execution yields a truthful best-available review and explicit gaps. Use the [shared policy](references/shared-policy.md) for capability recovery.

## Lens dispatch from `## Applies to`

Every lens profile in `reviewer-*.md` profiles in the Devin Desktop agents search path (portable or repo-local) should include a `## Applies to` section with:

- `inputs:` — required and optional `run_subagent` placeholders.
- `globs:` — path globs that, if matched in the diff, make the lens relevant.
- `keywords:` — keyword triggers that make the lens relevant.

When selecting one or more lenses for a PR or a branch diff, read the relevant profile files and match them in this order:

1. Input match: if the orchestrator provides an input listed under `## Applies to` for that lens (e.g. `<plan_path>` for `reviewer-plans`), the lens applies.
2. Glob match: if any changed file matches a glob, the lens applies.
3. Keyword match: if the PR title/body or diff summary contains a keyword, the lens applies.
4. Assess relevant trust boundaries even without keyword matches; use reviewer-security for applicable authentication/authorization, untrusted input/output, process/filesystem, serialization, dependency or privacy changes. If no specialist applies, select the adequate whole-branch route.

Prefer the least escalated lens that covers the diff. For broad, multi-surface branches, include all matching lenses rather than a single generalist.

## Repo-specific lens profiles

A consumer repo can extend the portable lens set by authoring a hand-edited `.agents/agents/reviewer-<lens>.md` override. These are not installed by the marketplace; they are repo-local and take precedence over vendor profiles.

Use this when the repo has domain-specific surfaces that a generic lens cannot cover. For example, one consumer might add a `.agents/agents/reviewer-marketplace.md` lens for pack generation, another might add `reviewer-domains.md` for domain canon, or `reviewer-tests.md` for a test harness. These are not part of the portable pack.

When the owning review workflow authorizes lens dispatch, discover applicable reviewer profiles from the active runtime and repository routes, assess their Applies-to cues against the diff and its trust boundaries, and select only the warranted lenses. Use requesting-code-review for whole-branch review and conducting-code-review for the reviewer method; profile availability does not authorize additional dispatches.

## Vendor and third-party profiles

This skill ships first-party portable subagent `.md` profiles under `dist/plugins/superpowers-plus/skills/selecting-a-subagent/assets/`. Run `py -3 <runtime-skill-path-for-selecting-a-subagent>/scripts/install_profiles.py --apply` to copy them to the Devin Desktop user-global agents directory (`~/.config/devin/agents/` or `%APPDATA%\devin\agents\` on Windows). Use `--target <dir>` to install elsewhere; the default target is the canonical surface for shared, portable profiles.

When choosing a profile, apply the Devin Desktop agents search path; later directories in this list override earlier ones:

1. Built-in profiles documented in `references/devin-desktop-profile.md`.
2. User-global profiles (`~/.config/devin/agents/` or `%APPDATA%\devin\agents\` on Windows).
3. `.devin/agents/<name>.md` user- or repo-local hand-authored overrides.
4. `.agents/agents/<name>.md` plugin-local or vendor profiles.

No skill should create or pressure the consumer to create `.devin/agents/`. `.agents/agents/` remains available for plugin-local or vendor profiles staged by other marketplace tooling.

See `references/vendor-profile-packaging.md` for the packaging contract and the full consumer search-path order.

## Common pressure

When the obvious choice is unclear or contested, read `references/pressure-scenarios.md` first.
