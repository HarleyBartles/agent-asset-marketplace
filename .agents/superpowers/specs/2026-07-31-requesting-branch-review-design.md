# Requesting Branch Review — Main-Agent Dispatch Design

> Spec for replacing the subagent-locked `review-branch-diff` skill with a main-agent `requesting-branch-review` skill that explicitly dispatches the `branch-reviewer` subagent for a target branch and worktree.

## Problem

`review-branch-diff` is locked to the `branch-reviewer` subagent via the `agent: branch-reviewer` frontmatter. When it runs, the entire skill executes as the subagent, so the main agent cannot be told to gather a branch and worktree and then dispatch the review. We need an equivalent skill that the main agent can invoke, which then launches `branch-reviewer` with a prompt naming the branch and worktree to compare to `main`.

## Goals

1. Replace the first-party `review-branch-diff` source with `requesting-branch-review`.
2. `requesting-branch-review` must run on the main agent (no `agent:` frontmatter).
3. The skill instructs the main agent to:
   - collect a target branch and worktree,
   - verify both exist,
   - ensure the `branch-reviewer` subagent profile is installed (using the bundled `assets/branch-reviewer/AGENT.md` fallback if needed),
   - dispatch `run_subagent profile: branch-reviewer` with a task that specifies the branch and worktree,
   - return the subagent's findings.
4. Preserve the `branch-reviewer` subagent profile unchanged in `assets/branch-reviewer/AGENT.md`.
5. Update all marketplace wiring and skill references from `review-branch-diff` to `requesting-branch-review`.
6. Regenerate downstream surfaces with `tools/run marketplace --apply` and pass `tools/run ci --check`.

## Constraints

- `requesting-branch-review` must not carry `agent:`; it is a main-agent dispatch skill.
- The `branch-reviewer` subagent remains read-only, with `exec` restricted to git commands.
- The new skill must ship in the same packs as the old one to avoid breaking consumers.
- Generated surfaces under `codex-marketplace/plugins/`, `generated/skill-zips/`, and `.agents/skills/` are derived from source and registry; only edit `sources/`, `adapters/`, and `codex-marketplace/custody-pack-registry.json`.
- First-party skill source must contain `SKILL.md` and `agents/openai.yaml` and must pass the marketplace shape validators.

## Proposed Approaches

### Option A: Rename the source and rewrite the skill body (recommended)

- Rename `sources/first_party/skills/review-branch-diff/` to `sources/first_party/skills/requesting-branch-review/`.
- Rewrite `SKILL.md` to remove `agent:` and describe the main-agent dispatch procedure.
- Keep `assets/branch-reviewer/AGENT.md`.
- Update `custody-pack-registry.json`, the SDD overlay, and `selecting-a-subagent` references.
- Regenerate downstream surfaces.
- Pros: a clean replacement; the old name is retired; one source of truth.
- Cons: requires touching adapter overlays and registry entries.

### Option B: Add `requesting-branch-review` while keeping `review-branch-diff`

- Create a new first-party skill and leave the subagent-locked skill in place.
- Pros: no breakage of existing slash commands.
- Cons: two skills for the same job; the user explicitly asked to replace it.

### Option C: Make it a repo-local `mark-*` skill

- Put `requesting-branch-review` under `.agents/skills/mark-requesting-branch-review/` only.
- Pros: fastest local authoring.
- Cons: not versioned in the marketplace, not shipped in packs, and does not replace the old skill.

**Recommendation:** Option A.

## Design Details

### `requesting-branch-review` first-party skill

Source tree: `sources/first_party/skills/requesting-branch-review/`

- `SKILL.md`
  - `name: requesting-branch-review`
  - `description`: Use when an agent should dispatch a whole-branch diff review for a specific branch and worktree against main.
  - No `agent:` frontmatter.
  - `triggers: user, model`
  - `use_when`: a branch is complete; a whole-branch diff review is needed; the review must target a specific branch or worktree.
  - `do_not_use_when`: the current branch has no commits ahead of main; only a single file needs review.
  - `related_skills`: `selecting-a-subagent`, `subagent-driven-development`, `finishing-a-development-branch`, `requesting-code-review`.
  - Body:
    1. Determine the target branch and worktree (from the user, the current git state, or by asking).
    2. Verify the branch with `git rev-parse --verify <branch>` and the worktree with a path check.
    3. Determine the base ref (`main` or `origin/main`) in that worktree.
    4. If the global `branch-reviewer` profile is not installed, copy `assets/branch-reviewer/AGENT.md` to `~/.config/devin/agents/branch-reviewer/AGENT.md` (or `%APPDATA%\devin\agents\branch-reviewer\AGENT.md` on Windows).
    5. Dispatch the subagent:
       ```markdown
       run_subagent profile: branch-reviewer
         title: "Review <branch> vs main"
         task: "Review the diff of branch <branch> against <base> in the worktree at <worktree> for correctness, style, consistency, and risk. If the subagent is not already in that worktree, run `cd <worktree>` before running git commands. Use `git diff --no-color <base>...<branch>` to obtain the diff. Cite specific files and line numbers. Do not modify files."
       ```
    6. Report the subagent's findings.

- `assets/branch-reviewer/AGENT.md` — unchanged from the current `review-branch-diff` skill.
- `agents/openai.yaml` — updated with `skill_name: requesting-branch-review`, `display_name: Requesting Branch Review`, `short_description: Use when an agent should dispatch a whole-branch diff review for a specific branch and worktree against main.`, and `default_prompt: Use /requesting-branch-review when an agent should dispatch a whole-branch diff review for a specific branch and worktree against main.`

### Marketplace wiring

- `codex-marketplace/custody-pack-registry.json`: rename all `review-branch-diff` entries to `requesting-branch-review`, updating `canonical_name`, `canonical_source_path`, `local_path`, `source_path`, and the `source_ledger` references.
- `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`: replace references to `/review-branch-diff` with `/requesting-branch-review` in the final whole-branch review step.
- `sources/first_party/skills/selecting-a-subagent/SKILL.md` and `references/devin-desktop-profile.md`: update the branch diff review row from `invoke /review-branch-diff` to `invoke /requesting-branch-review` and the profile-shipped note from `review-branch-diff` to `requesting-branch-review`.

### Regeneration

- `tools/run marketplace --apply` will:
  - project the new skill into `codex-marketplace/plugins/repo-worker-pack/`, `codex-marketplace/plugins/superpowers-plus/`, and `codex-marketplace/plugins/house-skills/`,
  - regenerate bundle manifests, source maps, provenance maps, and skill zips,
  - refresh the installed skill copy under `.agents/skills/requesting-branch-review/`.

## Files to Touch

- `sources/first_party/skills/review-branch-diff/SKILL.md` → `sources/first_party/skills/requesting-branch-review/SKILL.md` (rename + rewrite)
- `sources/first_party/skills/review-branch-diff/agents/openai.yaml` → `sources/first_party/skills/requesting-branch-review/agents/openai.yaml` (rename + rewrite)
- `sources/first_party/skills/review-branch-diff/assets/branch-reviewer/AGENT.md` → `sources/first_party/skills/requesting-branch-review/assets/branch-reviewer/AGENT.md` (rename, unchanged content)
- `codex-marketplace/custody-pack-registry.json` (rename registry entries)
- `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml` (slash command update)
- `sources/first_party/skills/selecting-a-subagent/SKILL.md`
- `sources/first_party/skills/selecting-a-subagent/references/devin-desktop-profile.md`
- Derived surfaces under `codex-marketplace/plugins/**/`, `generated/skill-zips/`, and `.agents/skills/` (regenerated)

## Verification

- `tools/run marketplace --apply`
- `tools/run ci --check`
- Inspect the regenerated `codex-marketplace/plugins/repo-worker-pack/skills/requesting-branch-review/SKILL.md` to confirm no `agent:` frontmatter and a `run_subagent` dispatch with explicit branch and worktree.
- Inspect `.agents/skills/requesting-branch-review/SKILL.md` to confirm the installed copy matches the source.
