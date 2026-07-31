# Superpowers Plus Consolidation — Phase 1: Layout and Router Cleanup

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `.agents/specs/2026-08-04-superpowers-plus-consolidation-design.md`

**Goal:** Remove the `superpowers/` working-surface residuals, make `using-superpowers-plus` the generic bootstrap router, and retire `work-mode-router` and `bootstrap-router`.

**Architecture:** Move durable specs/plans to `.agents/specs/` and `.agents/plans/`, move SDD scratch to `../_agents-scratch/<branch>/<plan-basename>/`, delete the visual-companion runtime, rewrite `using-superpowers-plus` as a repo-agnostic spin-up router, and absorb the good parts of `work-mode-router` and `bootstrap-router` into `using-superpowers-plus/references/`. `repo-worker-base` becomes the downstream repo-hygiene and baseline handoff.

**Tech Stack:** Markdown skill docs, YAML agent wrappers, git, `tools/run` deterministic build pipeline.

## Global Constraints

- Do not delete or rename `using-superpowers-plus` itself; only its body changes.
- Do not move historical spec/plan files; only canonical first-party skill references and generator paths are repointed.
- Edit source first, then regenerate; never hand-edit generated plugin trees, bundle manifests, or index files.
- Every `tools/run * --apply` step must be followed by a commit before the next `tools/run ci --check`.
- All source edits are committed before marketplace regeneration begins.
- Keep each commit focused on one task; the final task is the validation commit.

---

### Task 1: Remove the visual brainstorming companion

**Files:**
- Delete:
  - `sources/first_party/skills/brainstorming/scripts/server.cjs`
  - `sources/first_party/skills/brainstorming/scripts/helper.js`
  - `sources/first_party/skills/brainstorming/scripts/frame-template.html`
  - `sources/first_party/skills/brainstorming/scripts/start-server`
  - `sources/first_party/skills/brainstorming/scripts/start-server.ps1`
  - `sources/first_party/skills/brainstorming/scripts/stop-server`
  - `sources/first_party/skills/brainstorming/scripts/stop-server.ps1`
  - `sources/first_party/skills/brainstorming/visual-companion.md`
- Edit:
  - `sources/first_party/skills/brainstorming/SKILL.md` — remove the "Offer the visual companion just-in-time" step.

**Interfaces:**
- Removes: the entire Brainstorm Companion HTTP/WebSocket runtime.
- Produces: a `brainstorming` skill that uses text and the design spec only.

- [ ] **Step 1: Delete the companion files and scripts.**

```bash
git rm sources/first_party/skills/brainstorming/scripts/server.cjs
# repeat for helper.js, frame-template.html, start-server, start-server.ps1, stop-server, stop-server.ps1
git rm sources/first_party/skills/brainstorming/visual-companion.md
```

- [ ] **Step 2: Remove the companion step from `brainstorming/SKILL.md`.**

Read the file, locate the visual-companion call-out, delete it, and re-verify the checklist order.

- [ ] **Step 3: Commit.**

```bash
git add sources/first_party/skills/brainstorming
# Review the diff: no remaining references to server.cjs, visual-companion.md, or browser companion
git commit -m "feat: remove visual brainstorming companion runtime"
```

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

### Task 2: Move the durable specs and plans working surfaces

**Files:**
- Move:
  - `.agents/superpowers/specs/` → `.agents/specs/`
  - `.agents/superpowers/plans/` → `.agents/plans/`
- Edit:
  - `tools/generate_repo_index.py` — repoint the protected spec/plan paths.
  - `docs/skill-standards-policy.md` — repoint references to spec/plan locations.
  - `sources/first_party/skills/writing-plans/SKILL.md` — repoint the plan save path.
  - `sources/first_party/skills/brainstorming/SKILL.md` — repoint the spec save path.
  - `sources/first_party/skills/working-with-epics/SKILL.md` — repoint the roadmap path.
  - `sources/first_party/skills/subagent-driven-development/SKILL.md` — repoint plan path references.
  - `sources/first_party/skills/work-mode-router/references/route-states.md` — repoint plan references.
  - `.agents/superpowers/plans/AGENTS.md` — move to `.agents/plans/AGENTS.md` and repoint scope.
  - `.agents/superpowers/specs/AGENTS.md` — move to `.agents/specs/AGENTS.md` and repoint scope.
- Delete the now-empty `.agents/superpowers/` directory.

**Interfaces:**
- Produces: `.agents/specs/`, `.agents/plans/`, and a removed `.agents/superpowers/` directory.
- Does not move: historical spec/plan files in the new locations; the move is a directory rename.

- [ ] **Step 1: Move the directories and their `AGENTS.md` files.**

```bash
git mv .agents/superpowers/specs .agents/specs
git mv .agents/superpowers/plans .agents/plans
# The spec and plan AGENTS.md files move with the directories; update their scope headers in place.
```

- [ ] **Step 2: Repoint all first-party skill references.**

For each file in the list above, replace `.agents/superpowers/specs/` with `.agents/specs/` and `.agents/superpowers/plans/` with `.agents/plans/`. Use `grep` to find missed references; no first-party skill or script should keep the old path.

- [ ] **Step 3: Update `tools/generate_repo_index.py`.**

The protected indexer references the spec/plan roots. Update the paths and run a quick `python -c` import check if a test exists.

- [ ] **Step 4: Delete the empty `.agents/superpowers/` tree.**

```bash
rmdir .agents/superpowers || true
# Check for any leftover files; if any, decide whether they belong in .agents/specs/ or .agents/plans/.
```

- [ ] **Step 5: Run `tools/run repo-index --check` or the repo's quick index validation.**

This catches any hardcoded path the indexer still expects.

- [ ] **Step 6: Commit.**

```bash
git add .agents/specs .agents/plans .agents/superpowers sources/first_party/skills tools/generate_repo_index.py docs/skill-standards-policy.md
git diff --stat
git commit -m "refactor: move specs and plans out of .agents/superpowers/"
```

- [ ] **Step 7: Mark this task `[x]` in this plan before reporting back.**

---

### Task 3: Move SDD workspace to off-repo scratch

**Files:**
- Edit:
  - `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace`
  - `sources/first_party/skills/subagent-driven-development/scripts/sdd-workspace.ps1`
  - `sources/first_party/skills/subagent-driven-development/SKILL.md`
- Delete the git-ignored `.agents/superpowers/sdd/` directory if it still exists.

**Interfaces:**
- `sdd-workspace` now prints `../_agents-scratch/<branch>/<plan-basename>/`.
- Subagent briefs, reports, and review packages write outside the repo tree.

- [ ] **Step 1: Determine branch and plan-stem in `sdd-workspace`.**

The script must resolve the git branch and the plan file basename. Base the workspace path on `git rev-parse --abbrev-ref HEAD` and the sanitized plan stem, not on the repo root.

- [ ] **Step 2: Update the Bash and PowerShell scripts.**

Replace the `.agents/superpowers/sdd/<plan-stem>/` path with `../_agents-scratch/<branch>/<plan-stem>/`. Ensure the parent directories are created. Remove the in-repo `.gitignore` write; the scratch is not inside git.

- [ ] **Step 3: Update `subagent-driven-development/SKILL.md` references.**

Repoint all mentions of the old `.agents/superpowers/sdd/` workspace to the new scratch path.

- [ ] **Step 4: Test the new `sdd-workspace` scripts.**

Run both scripts with a sample plan path and verify the output directory is under `../_agents-scratch/`, not in the repo.

- [ ] **Step 5: Commit.**

```bash
git add sources/first_party/skills/subagent-driven-development
# Review: no .agents/superpowers/sdd/ references remain
git commit -m "refactor: move SDD workspace to off-repo scratch"
```

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

### Task 4: Rewrite `using-superpowers-plus` as the generic bootstrap router

**Files:**
- Edit:
  - `sources/first_party/skills/using-superpowers-plus/SKILL.md`
  - `sources/first_party/skills/using-superpowers-plus/agents/openai.yaml`
- Create:
  - `sources/first_party/skills/using-superpowers-plus/references/bootstrap-routing.md`
  - `sources/first_party/skills/using-superpowers-plus/references/platform-adaptation.md` (if platform refs need to move out of `SKILL.md`)
- Delete:
  - `sources/first_party/skills/work-mode-router/`
  - `sources/first_party/skills/bootstrap-router/`
- Update:
  - `sources/first_party/skills/repo-worker-base/SKILL.md` and `references/` — remove routing-classification language, keep baseline handoff.

**Interfaces:**
- `using-superpowers-plus` now: invokes before any action, inspects environment, loads base doctrine, classifies request, routes to the owning skill.
- `repo-worker-base` becomes the downstream repo-hygiene handoff.

- [ ] **Step 1: Extract platform-adaptation content from `using-superpowers-plus/SKILL.md`.**

Move the Codex/Pi/Antigravity/Gemini platform notes to `references/platform-adaptation.md` to keep the body under 500 words. Update the `SKILL.md` links.

- [ ] **Step 2: Write the new `using-superpowers-plus/SKILL.md` body.**

Body must contain:
1. Skill invocation contract.
2. Bootstrap order (inspect environment, load doctrine, classify, route).
3. Minimal request-classification table.
4. Handoff to `repo-worker-base` for repo-backed work.
5. Link to `references/bootstrap-routing.md` for the full routing table and `references/platform-adaptation.md` for harness-specific instructions.

- [ ] **Step 3: Create `references/bootstrap-routing.md`.**

Absorb the good route tables from `work-mode-router/references/route-states.md` and `bootstrap-router/SKILL.md`, but keep them generic. Include the new `.agents/doctrine/` local-doctrine hook and the `base-doctrine` base hook.

- [ ] **Step 4: Update `repo-worker-base/SKILL.md`.**

Remove or repoint any routing-classification language. Keep the composition contract: `repo-worker-base -> matching baseline -> local guide -> stage skill`. Remove `work-mode-router` and `bootstrap-router` from `related_skills`.

- [ ] **Step 5: Retire `work-mode-router` and `bootstrap-router`.**

```bash
git rm -r sources/first_party/skills/work-mode-router
git rm -r sources/first_party/skills/bootstrap-router
```

Ensure no first-party skill or guide still references them; grep for `work-mode-router` and `bootstrap-router`.

- [ ] **Step 6: Update `agents/openai.yaml` if the default prompt or short description changed.**

- [ ] **Step 7: Run `tools/run marketplace --apply` and commit source first.**

```bash
git add sources/first_party/skills/using-superpowers-plus sources/first_party/skills/repo-worker-base
git commit -m "refactor: make using-superpowers-plus the generic bootstrap router"
```

- [ ] **Step 8: Mark this task `[x]` in this plan before reporting back.**

---

### Task 5: Regenerate marketplace, refresh skills, and run CI

**Files:**
- All generated surfaces under `codex-marketplace/`, `.agents/plugins/`, `.agents/skills/`, and `provenance/`.

**Interfaces:**
- Produces a passing `tools/run ci --check` and updated marketplace projections.

- [ ] **Step 1: Run the full deterministic marketplace regeneration.**

```bash
./tools/run marketplace --apply
```

- [ ] **Step 2: Review the generated diff.**

The diff should show:
- `work-mode-router` and `bootstrap-router` removed from projections.
- `using-superpowers-plus` updated.
- `specs/` and `plans/` no longer under `.agents/superpowers/` in generated indexes.

- [ ] **Step 3: Stage and commit the generated surfaces.**

```bash
git add codex-marketplace .agents/plugins .agents/skills provenance
# Do not commit if the diff contains unexpected manual edits.
git commit -m "chore: regenerate marketplace after superpowers-plus consolidation phase 1"
```

- [ ] **Step 4: Run `tools/run ci --check`.**

Wait for the result. If it fails, fix the source, regenerate, and re-commit before proceeding.

- [ ] **Step 5: Commit any CI fixes separately.**

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

## Verification

- `tools/run ci --check` passes on the final tree.
- `using-superpowers-plus` is the only first-party skill that a worker invokes at session boot.
- `git grep -E '\.agents/superpowers/(specs|plans|sdd)'` returns only historical or moved files, no first-party source or script references.
- `git grep -E 'work-mode-router|bootstrap-router'` returns only `provenance/` or `sources/third_party/`.

## Publication

- Push the `consolidate-superpowers-plus-residuals` branch to origin.
- Open a PR with title "refactor: consolidate superpowers-plus residuals (phase 1)".
- Attach the PR URL and head SHA as publication proof.
