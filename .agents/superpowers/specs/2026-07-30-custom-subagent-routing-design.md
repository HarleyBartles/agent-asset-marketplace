# Custom Subagent Routing — Devin Desktop Design

> Spec for making the `subagent-model-routing` skill and the `subagent-driven-development` superpowers overlay accurate for Devin Desktop custom subagent profiles, and for shipping a `review-branch-diff` repo-worker-pack skill.

## Problem

Devin Desktop now supports custom subagent profiles under `~/.config/devin/agents/` (or `%APPDATA%\devin\agents\` on Windows). We have proven in spike that:

- `run_subagent profile: <name>` works after a restart.
- `model:` on a custom subagent profile is honoured.
- `allowed-tools:` is filtered by the runtime to `read`, `grep`/`find_file_by_name`, `edit`, and `exec` (`write` and `skill` are not granted).
- A skill can dispatch to a subagent via the `agent:` frontmatter field.

The repo currently treats `subagent_explore` and `subagent_general` as the only Devin Desktop dispatch options. The `subagent-model-routing` skill is stale, and the `subagent-driven-development` overlay still speaks in generic "Subagent (general-purpose)" terms. We also need a shareable, no-argument branch-diff review skill that the SDD final gate can call.

## Goals

1. Standardize and keep the global `~/.config/devin/agents/` profiles: `reviewer`, `implementer`, `branch-reviewer`.
2. Update `subagent-model-routing/references/devin-desktop-profile.md` to document custom profiles, `model:` ownership, and the `write` limitation.
3. Update the `subagent-driven-development` superpowers overlay so SDD dispatches `implementer` and `reviewer` custom profiles, and calls `/review-branch-diff` for the final whole-branch review.
4. Ship `review-branch-diff` as a first-party skill bundled in `repo-worker-pack`, with a static `branch-reviewer/AGENT.md` asset fallback.
5. Regenerate marketplace and installed-skill surfaces, then run `tools/run ci --check`.

## Constraints

- Custom subagent profiles must live globally in `~/.config/devin/agents/` for cross-repo availability.
- The `branch-reviewer` subagent needs `exec` only for `git diff`/`git rev-parse`; it must not edit files.
- `review-branch-diff` the skill must be no-argument and self-contained.
- `subagent-driven-development` is a third-party superpowers skill; changes go through `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`, not `sources/third_party/`.
- All first-party skill changes must have `SKILL.md` and `agents/openai.yaml` and pass `tools/run ci --check`.
- Generated surfaces under `codex-marketplace/plugins/` and `.agents/skills/` are downstream of `sources/` and `adapters/`.

## Proposed Approaches

### Option A: Update SDD overlay to reference `subagent-model-routing` for every dispatch

- At each SDD step, the controller invokes `/subagent-model-routing` to pick the profile.
- Pros: single source of truth for routing.
- Cons: one active skill at a time makes this clunky; SDD already knows the role and just needs the right profile string.

### Option B: Hardcode the custom profile names in the SDD overlay (recommended)

- Add `overlay.yaml` edits to `implementer-prompt.md` and `task-reviewer-prompt.md` so they say `run_subagent profile: implementer` and `run_subagent profile: reviewer`.
- Update the final whole-branch review step to invoke `/review-branch-diff`.
- Pros: keeps SDD self-contained and fast; `subagent-model-routing` remains a standalone skill for ad-hoc routing.
- Cons: profile names are duplicated between the overlay and the global profiles.

### Option C: Keep `review-branch-diff` as a user-local skill

- Leave `review-branch-diff` in `~/.config/devin/skills/` and do not vendor it.
- Pros: no repo work.
- Cons: not shared or versioned with the team; SDD cannot rely on it being installed.

**Recommendation:** Option B for SDD routing, and vendored `review-branch-diff` in `repo-worker-pack` instead of Option C.

## Design Details

### Global subagent profiles

```
~/.config/devin/agents/
├── reviewer/AGENT.md        (model: swe-1-7, read/search only)
├── implementer/AGENT.md     (model: glm-5-2, edit/exec)
└── branch-reviewer/AGENT.md (model: swe-1-7, read/search + git exec)
```

- `reviewer` and `implementer` are generic.
- `branch-reviewer` is the only read-only subagent allowed `exec`, restricted by its system prompt to `git diff`, `git rev-parse`, `git log`, `git show`, `git status`, `git branch`.

### `review-branch-diff` first-party skill

- Source: `sources/first_party/skills/review-branch-diff/`
  - `SKILL.md` with `agent: branch-reviewer`, no arguments.
  - `assets/branch-reviewer/AGENT.md` — a static fallback copy of the global `branch-reviewer` profile. It is not loaded by default; an agent can use it if the global profile is missing.
  - `agents/openai.yaml` per the marketplace contract.
- Bundled into `repo-worker-pack` by adding an entry to the `entries` array in `codex-marketplace/custody-pack-registry.json` and updating the `source_ledger` to include `sources/first_party/skills/review-branch-diff`. `tools/run marketplace --apply` then projects the skill into `codex-marketplace/plugins/repo-worker-pack/` and regenerates `references/bundle-manifest.json` and `references/source-map.md`.
- Installed to `.agents/skills/review-branch-diff/` via `tools/run installed-skills --apply`.
- Body: determine base ref (`main` or `origin/main`), run `git diff --no-color <base>...HEAD`, review for correctness, style, consistency, and risk. Cite files and line numbers.

### `subagent-model-routing` skill update

Update `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`:

- Add a "Custom subagent profiles" section covering `~/.config/devin/agents/`, `.devin/agents/`, and `.agents/agents/`.
- Routing table:
  - Review / architecture challenge → `reviewer`
  - Bounded implementation / bugfix → `implementer`
  - Branch diff review → `branch-reviewer` or `/review-branch-diff`
  - Broad read-only exploration → `subagent_explore`
  - Broad mixed work → `subagent_general`
- Document `model:`:
  - `subagent_explore` → default subagent model (SWE-1.6)
  - `subagent_general` → parent model
  - custom → `model:` in profile
- Document the `write` limitation: custom subagents do not get `write`; new files must be created via `exec`.
- Document the `skill`/`agent` dispatch pattern: a skill with `agent: <profile>` runs as that subagent.

### `subagent-driven-development` superpowers overlay

Add `edits` to `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`:

- `implementer-prompt.md`: replace the generic `Subagent (general-purpose)` dispatch block with `run_subagent profile: implementer`.
- `task-reviewer-prompt.md`: replace the generic reviewer dispatch with `run_subagent profile: reviewer`.
- `SKILL.md` final whole-branch review step: invoke `/review-branch-diff` instead of a generic final code reviewer.
- Keep `subagent-model-routing` mentioned only for ad-hoc or non-SDD dispatch.

## Files to Touch

- `sources/first_party/skills/subagent-model-routing/references/devin-desktop-profile.md`
- `adapters/codex/superpowers-plus/subagent-driven-development/overlay.yaml`
- `codex-marketplace/custody-pack-registry.json`
- `sources/first_party/skills/review-branch-diff/SKILL.md` (new)
- `sources/first_party/skills/review-branch-diff/agents/openai.yaml` (new)
- `sources/first_party/skills/review-branch-diff/assets/branch-reviewer/AGENT.md` (new)
- `codex-marketplace/plugins/repo-worker-pack/` generated bundle (via `tools/run marketplace --apply`)
- `.agents/skills/review-branch-diff/` installed copy (via `tools/run installed-skills --apply`)

## Verification

- `tools/run mesh --apply`
- `tools/run installed-skills --apply`
- `tools/run ci --check`
- Manually test on a feature branch:
  - `/review-branch-diff` runs as `branch-reviewer` and returns a review.
  - A sample SDD plan triggers `run_subagent profile: implementer` and `run_subagent profile: reviewer`.
