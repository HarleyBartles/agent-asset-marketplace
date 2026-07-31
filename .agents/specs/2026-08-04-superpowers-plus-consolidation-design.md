# Superpowers Plus Residuals Consolidation

## Overview

Now that the `obra/superpowers` v6.2.0 skills have been brought in as first-party
(`superpowers-plus`), we are carrying several surfaces that belong to the old
overlay/adapter architecture rather than to a first-party pack. This design
describes a consolidation that removes the residuals and gives each remaining
surface a single, well-homed owner.

## Goals

1. Remove the visual-companion runtime from `brainstorming`.
2. Move durable work products out of `.agents/superpowers/` to
   `.agents/specs/`, `.agents/plans/`, and `.agents/plans/<epic>/`.
3. Move transient SDD scratch out of the repo tree to `../_agents-scratch/`.
4. Make `using-superpowers-plus` the single bootstrap router.
5. Retire `work-mode-router` and `bootstrap-router` by folding their good content
   into `using-superpowers-plus`.
6. Merge `requesting-branch-review` into `requesting-code-review` and remove the
   `branch-reviewer` subagent profile.
7. Move `report-hygiene` from `base-doctrine` to `writing-with-clarity`.
8. Thin repo guides by moving generic review and skill-standards content into the
   relevant workflow skills.
9. Fold `mark-skill-authoring` into `writing-skills` and the marketplace skill
   standards policy.

## Constraints

- The `superpowers-plus` plugin must remain installable in every repo.
- No skill name or public identity is removed until the references that point to it
  are repointed.
- All marketplace and index regeneration must pass `tools/run ci --check`.
- The new layout must not be locked in this spec until the move is actually done;
  this design lives in the current `.agents/specs/` path because that is
  still the canonical location.

## New architecture

### Durable work products

```
.agents/specs/YYYY-MM-DD-<topic>-design.md                  # approved design
.agents/plans/YYYY-MM-DD-<feature>.md                       # single approved plan
.agents/plans/<epic-name>/
  roadmap.md                                                # epic sequence table
  plan-1.md
  plan-2.md
```

`working-with-epics` creates the `<epic-name>/` directory and writes `roadmap.md`;
`writing-plans` writes each plan into that directory.

### Transient scratch

```
../_agents-scratch/<branch-name>/<plan-basename>/
  ledger.md
  briefs/
  review-packages/
```

`subagent-driven-development/scripts/sdd-workspace` resolves to this path.

### Spin-up stack

```
using-superpowers-plus
  -> inspect environment
  -> load base-doctrine + .agents/doctrine/ delta
  -> classify request
  -> hand off to the owning skill
```

`using-superpowers-plus` becomes the only session bootstrap skill. It pulls in
`base-doctrine` for cross-runtime invariants and the repo's `.agents/doctrine/`
directory for repo-specific doctrine, then routes to `repo-worker-base`,
`writing-skills`, `using-github`, `using-linear`, etc.

`repo-worker-base` remains the repo-backed work baseline. It supplies portable
worktree, branch, scratch, validation, and publication boundaries, then hands off
to the right stage guide and skill.

### Review and subagent profiles

- `selecting-a-subagent` owns four subagent profiles: `implementer`,
  `implementer-strong`, `reviewer`, `reviewer-strong`.
- The `branch-reviewer.md` profile is deleted.
- `requesting-code-review` owns both per-task and whole-branch review lanes,
  dispatching `reviewer` or `reviewer-strong` with the appropriate diff range.
- `base-doctrine` owns the base code-review contract; repo `.agents/guides/code-review-guide.md`
  is a thin delta.

### Skill standards and authoring

- `writing-skills` owns the universal skill-authorship method (TDD for skills,
  SDO, frontmatter, directory shape).
- `writing-skills/references/source-grounded-authoring.md` holds the generic
  authority/citation/decomposition rules.
- `docs/skill-standards-policy.md` becomes the thin marketplace delta for
  `agents/openai.yaml`, canonical metadata, and accepted lanes.
- `mark-skill-authoring` is retired; its scaffolder becomes
  `tools/new_skill.py` or `writing-skills/scripts/new-skill.py`.

## Epic sequence

| Phase | Focus | Key outcomes |
|---|---|---|
| 1 | Layout and router cleanup | Remove visual companion, move `specs`/`plans`, off-repo SDD scratch, make `using-superpowers-plus` the sole bootstrap, retire `work-mode-router` and `bootstrap-router` |
| 2 | Review and subagent cleanup | Merge `requesting-branch-review` into `requesting-code-review`, consolidate `selecting-a-subagent` profiles, move base code-review contract into `base-doctrine` |
| 3 | Doctrine and guide thinning | Move `report-hygiene` to `writing-with-clarity`, thin `code-review-guide.md`, fold `mark-skill-authoring`, thin `skill-standards-policy.md` |
| 4 | Validation and mesh refresh | Regenerate marketplace, refresh installed skills, update `INDEX.md`, run `tools/run ci --check` |

## Phase 1 scope

Phase 1 is the first implementation plan. It unlocks the rest by removing the
`superpowers/` working surface and giving `using-superpowers-plus` a clean spin-up
contract.

In scope for Phase 1:

- Delete the visual-companion machinery under `sources/first_party/skills/brainstorming/scripts/`
  and the companion mention in `brainstorming/SKILL.md`.
- Move `.agents/superpowers/specs/` to `.agents/specs/` and `.agents/superpowers/plans/`
  to `.agents/plans/`, repointing every skill reference and `tools/generate_repo_index.py`.
- Repoint `sdd-workspace` to `../_agents-scratch/<branch>/<plan-basename>/` and delete
  the `sdd` directory from the repo tree.
- Rewrite `using-superpowers-plus/SKILL.md` as a generic bootstrap router: skill
  invocation contract, environment inspection, doctrine load, request classification,
  and routing. Remove the `Asset Marketplace Routing` section.
- Absorb `work-mode-router` and `bootstrap-router` references into
  `using-superpowers-plus/references/` and retire both skills.
- Update `repo-worker-base` to be the downstream repo-hygiene handoff, removing
  its own routing-classification language.
- Regenerate marketplace and run `tools/run ci --check`.

## Phase 1 file touch points

The planning agent can start from this map. Exact command sequences and `edit`
targets belong in the Plan 1 task list.

- `sources/first_party/skills/brainstorming/SKILL.md` — remove visual-companion step.
- `sources/first_party/skills/brainstorming/scripts/server.cjs` — delete.
- `sources/first_party/skills/brainstorming/scripts/helper.js` — delete.
- `sources/first_party/skills/brainstorming/scripts/frame-template.html` — delete.
- `sources/first_party/skills/brainstorming/scripts/start-server.*` — delete.
- `sources/first_party/skills/brainstorming/scripts/stop-server.*` — delete.
- `sources/first_party/skills/brainstorming/visual-companion.md` — delete.
- `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace` — repoint output directory.
- `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace.ps1` — repoint output directory.
- `sources/first_party/skills/subagent-driven-development/SKILL.md` — update workspace path references.
- `sources/first_party/skills/using-superpowers-plus/SKILL.md` — rewrite as generic bootstrap router.
- `sources/first_party/skills/using-superpowers-plus/references/bootstrap-routing.md` — new, absorbs `work-mode-router` and `bootstrap-router` route tables.
- `sources/first_party/skills/work-mode-router/` — retire after content is absorbed.
- `sources/first_party/skills/bootstrap-router/` — retire after content is absorbed.
- `sources/first_party/skills/repo-worker-base/SKILL.md` — remove routing-classification language; keep baseline handoff.
- `tools/generate_repo_index.py` — repoint `.agents/superpowers/plans` and `.agents/superpowers/specs`.
- `docs/skill-standards-policy.md` — repoint `.agents/superpowers/plans` and `.agents/superpowers/specs`.
- `.agents/superpowers/specs/` → `.agents/specs/`.
- `.agents/superpowers/plans/` → `.agents/plans/`.
- `codex-marketplace/plugins/superpowers-plus/references/bundle-manifest.json` — regenerate after retirements.
- `provenance/first-party-skills.md` — regenerate after retirements.

Out of scope for Phase 1:

- Merging `requesting-branch-review` (Phase 2).
- Moving `report-hygiene` (Phase 3).
- Folding `mark-skill-authoring` (Phase 3).
- Renaming `using-superpowers-plus` (the name stays; the body changes).

## Risks and mitigations

- **Risk:** `using-superpowers-plus` is the always-on entrypoint; a bad rewrite
  could break all repos that depend on it.
  - **Mitigation:** Keep the `SKILL.md` body under the 500-word limit, move the
    full route tables and platform references out to `references/`, and regenerate
    the marketplace after each skill change.
- **Risk:** Moving `specs/` and `plans/` breaks historical plan/spec links in
  comments, provenance, and `INDEX.md`.
  - **Mitigation:** Leave the historical files where they are; move only the
    canonical surface going forward. Update `tools/generate_repo_index.py` and
    generated indexes, not hand-edited paths.
- **Risk:** `work-mode-router` and `bootstrap-router` are installed in other repos.
  - **Mitigation:** This change is a source-custody change in the marketplace; the
    retirement will be picked up on the next plugin release, not a silent deletion.

## Success criteria

- `tools/run ci --check` passes.
- `using-superpowers-plus` is the only bootstrap skill an agent needs at session start.
- No first-party skill references `.agents/superpowers/` paths.
- No `mark-skill-authoring` or `work-mode-router` or `bootstrap-router` remains in
  `sources/first_party/skills/` or `codex-marketplace/plugins/superpowers-plus/`.
