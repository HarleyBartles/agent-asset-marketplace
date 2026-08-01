# Superpowers Plus Consolidation — Phase 2: Routing, Baselines, and Consumer Surfaces

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `.agents/specs/2026-08-04-superpowers-plus-consolidation-design.md`

**Goal:** Fold the new routing and baseline cleanup work into the original Phase 2 roadmap, then deliver the four deferred consumer surfaces: `asking-clarifying-questions` as an anytime escape hatch, `repo-worker-base` stripped of stage baselines, `publishing-source`, `using-github-mcp`, cross-repo draft-PR policy, and vendor profile packaging.

**Architecture:** `using-superpowers-plus` becomes the sole Superpowers bootstrap and composition router. `repo-worker-base` owns only worktree, branch, scratch, validation, and publication boundaries. Stage skills own their own baselines. `asking-clarifying-questions` is reachable from every stage skill as a one-fact-per-turn escape hatch.

**Tech Stack:** Markdown skill docs, YAML agent wrappers, git, `tools/run` deterministic build pipeline.

## Global Constraints

- Do not delete or rename `using-superpowers-plus` itself; only its body and references change.
- Do not move historical spec/plan files; only canonical first-party skill references and generator paths are repointed.
- Edit source first, then regenerate; never hand-edit generated plugin trees, bundle manifests, or index files.
- Every `tools/run * --apply` step must be followed by a commit before the next `tools/run ci --check`.
- All source edits are committed before marketplace regeneration begins.
- Keep each commit focused on one task; the final task is the validation commit.

## Task ordering

Run the tasks in the order listed. The main ordering constraints are:

- **Task 1** has no dependencies.
- **Task 2** consumes the `writing-plans/SKILL.md` changes from Task 1; it runs after Task 1 so both edits to `writing-plans/SKILL.md` do not conflict.
- **Task 3** renames `using-github` to `using-github-mcp` and updates all first-party references. It runs after Task 2 because Task 2 edits `using-superpowers-plus/references/bootstrap-routing.md`, which Task 3 must then update for the renamed skill.
- **Task 4** has no dependencies on Tasks 1–3.
- **Task 5** consumes the `using-github-mcp` rename from Task 3 and the `repo-worker-base` cleanup from Task 2; it runs after both.
- **Task 6** has no dependencies on earlier tasks.
- **Final integration** runs after all six tasks are committed.

No parallel execution is expected; one subagent (or the orchestrator) runs each task to completion before starting the next.

---

### Task 1: Reframe `asking-clarifying-questions` as an anytime escape hatch

**Files:**
- Edit:
  - `sources/first_party/skills/asking-clarifying-questions/SKILL.md`
  - `sources/first_party/skills/brainstorming/SKILL.md`
  - `sources/first_party/skills/writing-plans/SKILL.md` (also hosts the missing-scope rule)
  - `sources/first_party/skills/executing-plans/SKILL.md`
  - `sources/first_party/skills/subagent-driven-development/SKILL.md`
  - `sources/first_party/skills/risk-gates/SKILL.md`

**Consumes:** none.

**Interfaces:**
- `asking-clarifying-questions` is invoked at the natural ambiguity point inside each stage skill.
- The skill explicitly supports multiple turns: one question per message, as many turns as needed.
- `writing-plans` gains a missing-scope decision table that tells agents when to ask, brainstorm, or write a high-level draft.

- [x] **Step 1: Update `asking-clarifying-questions/SKILL.md`.**

  Replace the "one question" framing with "one question per turn, as many turns as needed." Add the concrete trigger: "If a single missing fact blocks the next step of the current skill, invoke this skill, record the answer, and continue; repeat for the next missing fact." Keep the existing `do_not_use_when` for design and risk-gate escalation.

- [x] **Step 2: Add the missing-scope decision table to `writing-plans/SKILL.md`.**

  Under a new "When to stop and ask" section, add:

  | Situation | Use |
  |---|---|
  | Plan item has no acceptance criteria and the answer is not in durable source or the spec | `/asking-clarifying-questions` |
  | The whole shape of the solution is unknown | `/brainstorming` to update the spec first |
  | Plan item has acceptance criteria but is large | Write the plan as a high-level draft and iterate |
  | Scope is in the spec but not yet broken into tasks | Write the plan, then review |

- [x] **Step 3: Add `asking-clarifying-questions` triggers to each stage skill.**

  Add one sentence to each of `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, and `risk-gates` at the point where a single missing fact can block the next step. The sentence must name the skill: "If a single missing fact blocks the next step, invoke `/asking-clarifying-questions` before guessing."

- [x] **Step 4: Commit.**

  ```bash
  git add sources/first_party/skills/asking-clarifying-questions sources/first_party/skills/brainstorming sources/first_party/skills/writing-plans sources/first_party/skills/executing-plans sources/first_party/skills/subagent-driven-development sources/first_party/skills/risk-gates
  git diff --stat
  git commit -m "feat: reframe asking-clarifying-questions as one-fact-per-turn escape hatch"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 2: Strip the baseline and composition router out of `repo-worker-base`

**Files:**
- Move:
  - `sources/first_party/skills/repo-worker-base/references/superpowers-composition.md` → `sources/first_party/skills/using-superpowers-plus/references/superpowers-composition.md`
  - `sources/first_party/skills/repo-worker-base/references/design-baseline.md` → `sources/first_party/skills/brainstorming/references/design-baseline.md`
  - `sources/first_party/skills/repo-worker-base/references/planning-baseline.md` → `sources/first_party/skills/writing-plans/references/planning-baseline.md`
  - `sources/first_party/skills/repo-worker-base/references/implementation-baseline.md` → `sources/first_party/skills/executing-plans/references/implementation-baseline.md`
  - `sources/first_party/skills/repo-worker-base/references/code-review-baseline.md` → `sources/first_party/skills/requesting-code-review/references/code-review-baseline.md`
- Edit:
  - `sources/first_party/skills/repo-worker-base/SKILL.md`
  - `sources/first_party/skills/using-superpowers-plus/references/bootstrap-routing.md`
  - `sources/first_party/skills/using-superpowers-plus/SKILL.md` (if the composition table is linked)
  - `sources/first_party/skills/repo-standards/references/repository-guide-standard.md`
  - `sources/first_party/skills/brainstorming/SKILL.md`
  - `sources/first_party/skills/writing-plans/SKILL.md`
  - `sources/first_party/skills/executing-plans/SKILL.md`
  - `sources/first_party/skills/requesting-code-review/SKILL.md`

**Consumes:** Task 1 (edits `writing-plans/SKILL.md` before this task adds the baseline-loading step).

**Interfaces:**
- `repo-worker-base` stops owning stage baselines and the Superpowers composition table.
- `using-superpowers-plus` owns `superpowers-composition.md` and the bootstrap routing contract.
- Each stage skill owns its own baseline reference and reads it as part of its own first step.

- [x] **Step 1: Move the references.**

  Use `git mv` for each file. The source custody moves; the content is otherwise unchanged unless a relative path inside the file needs updating.

- [x] **Step 2: Update `repo-worker-base/SKILL.md`.**

  Remove the `superpowers-composition.md` and all four baseline rows from the `Read when` table. Remove the "Composition contract" section that references `repo-worker-base -> matching baseline -> local guide -> selected Superpowers lane` and point instead to `using-superpowers-plus/references/bootstrap-routing.md` for composition.

- [x] **Step 3: Update `using-superpowers-plus/references/bootstrap-routing.md`.**

  Make the repo-backed handoff:

  ```text
  using-superpowers-plus -> repo-worker-base (hygiene) -> stage skill (reads its baseline + local guide)
  ```

  Update the `superpowers-composition.md` link to point at `using-superpowers-plus/references/superpowers-composition.md`.

- [x] **Step 4: Update `repo-standards/references/repository-guide-standard.md`.**

  Change the relationship to: `repo-standards` owns guide layout, invocation, and workflow order; `repo-worker-base` owns worktree, branch, scratch, validation, and publication boundaries; each stage skill owns its own baseline.

- [x] **Step 5: Add baseline loading to each stage skill.**

  Add a first step to `brainstorming`, `writing-plans`, `executing-plans`, and `requesting-code-review` that says: "Read this skill's baseline (`references/<stage>-baseline.md`) and the repo's `.agents/guides/<stage>-guide.md` before executing the stage checklist."

- [x] **Step 6: Commit.**

  ```bash
  git add sources/first_party/skills/repo-worker-base sources/first_party/skills/using-superpowers-plus sources/first_party/skills/brainstorming sources/first_party/skills/writing-plans sources/first_party/skills/executing-plans sources/first_party/skills/requesting-code-review sources/first_party/skills/repo-standards
  git diff --stat
  git commit -m "refactor: move stage baselines out of repo-worker-base"
  ```

- [x] **Step 7: Mark this task `[x]` in this plan before reporting back.**

---

### Task 3: Rename `using-github` to `using-github-mcp` and keep it in `repo-worker-pack`

**Files:**
- Rename:
  - `sources/first_party/skills/using-github/` → `sources/first_party/skills/using-github-mcp/`
- Edit:
  - `sources/first_party/skills/using-github-mcp/SKILL.md`
  - `sources/first_party/skills/using-github-mcp/agents/openai.yaml`
  - `codex-marketplace/custody-pack-registry.json`
  - `codex-marketplace/plugins/repo-worker-pack/*` bundle-manifest and source/provenance maps (regenerated, not hand-edited)
  - All first-party skills and guides that reference `/using-github` (e.g. `using-superpowers-plus/references/bootstrap-routing.md`, `.agents/guides/pr-guide.md`, `.agents/guides/implementing-guide.md`)

**Consumes:** Task 2 (edits `using-superpowers-plus/references/bootstrap-routing.md` before this task updates it for the renamed skill).

**Interfaces:**
- The skill is named `using-github-mcp`, remains in `repo-worker-pack`, and teaches agents how to use the available GitHub MCP and `gh` tools.
- All existing `/using-github` invocations in skills and guides become `/using-github-mcp`.

- [x] **Step 1: Rename the source directory.**

  ```bash
  git mv sources/first_party/skills/using-github sources/first_party/skills/using-github-mcp
  ```

- [x] **Step 2: Update skill identity.**

  Update `name` and any `source-id`/`provenance-name` fields in `SKILL.md` and `agents/openai.yaml` to `using-github-mcp`. Update all prose that mentions the old name.

- [x] **Step 3: Update first-party references.**

  Use `grep` to find every `/using-github` and `using-github` reference in `sources/first_party/`, `.agents/guides/`, and `docs/`. Repoint to `using-github-mcp`.

- [x] **Step 4: Commit.**

  ```bash
  git add sources/first_party/skills/using-github-mcp .agents/guides docs codex-marketplace/custody-pack-registry.json
  git diff --stat
  git commit -m "refactor: rename using-github to using-github-mcp"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 4: Design and implement `publishing-source` in `superpowers-plus`

**Files:**
- Create:
  - `sources/first_party/skills/publishing-source/SKILL.md`
  - `sources/first_party/skills/publishing-source/agents/openai.yaml`
  - `sources/first_party/skills/publishing-source/references/publishing-decisions.md` (optional, if the skill body grows)
- Edit:
  - `codex-marketplace/custody-pack-registry.json` (add `publishing-source` to `superpowers-plus`)
  - `sources/first_party/skills/using-superpowers-plus/SKILL.md` and `references/bootstrap-routing.md` (route source-publication tasks)

**Consumes:** none.

**Interfaces:**
- `publishing-source` owns the source-publication decision tree: when to commit, tag, release, push source, or export a pack.
- It is installed with `superpowers-plus` and discoverable via `using-superpowers-plus`.

- [ ] **Step 1: Draft the skill.**

  Write `publishing-source/SKILL.md` with `use_when`, `do_not_use_when`, a decision checklist, and the canonical source-publication sequences. Keep the body under 500 words; move long route tables to `references/`.

- [ ] **Step 2: Create the agent wrapper.**

  Write `agents/openai.yaml` with the Codex-facing wrapper metadata and a default prompt aligned to the skill trigger.

- [ ] **Step 3: Wire it into the pack and bootstrap router.**

  Add `publishing-source` to `superpowers-plus` in `codex-marketplace/custody-pack-registry.json`. Add a `publishing_source` mode to `using-superpowers-plus/references/bootstrap-routing.md`.

- [ ] **Step 4: Test with a pressure prompt.**

  Write a short pressure prompt that throws a source-publication decision at an agent and verify the skill directs it to the right sequence.

- [ ] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/publishing-source codex-marketplace/custody-pack-registry.json sources/first_party/skills/using-superpowers-plus
  git diff --stat
  git commit -m "feat: add publishing-source skill"
  ```

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

### Task 5: Implement cross-repo draft-PR policy

**Files:**
- Edit:
  - `.agents/guides/pr-guide.md`
  - `sources/first_party/skills/using-github-mcp/SKILL.md` (if it has PR-lifecycle guidance)
  - `sources/first_party/skills/requesting-code-review/SKILL.md`
  - `sources/first_party/skills/finishing-a-development-branch/SKILL.md` (if it exists)

**Consumes:** Task 3 (renames `using-github` to `using-github-mcp` before the draft-PR policy and helper skills reference the new name).

**Interfaces:**
- The draft-PR policy is documented in `pr-guide.md` and referenced from review and closeout skills.
- The policy covers when to open as draft, when to mark ready, and any repo-specific exceptions for this repo and for consumers.

- [ ] **Step 1: Draft the policy.**

  Add a "Draft PR policy" section to `.agents/guides/pr-guide.md` with rules for this repo and a consumer-canonical variant. Cover: open as draft for WIP, mark ready when preflight passes, keep branch review/closeout skills aware of the policy.

- [ ] **Step 2: Add policy triggers to relevant skills.**

  Add one sentence to `using-github-mcp`, `requesting-code-review`, and `finishing-a-development-branch` that tells the agent to consult `pr-guide.md` before changing a PR's draft state.

- [ ] **Step 3: Commit.**

  ```bash
  git add .agents/guides/pr-guide.md sources/first_party/skills/using-github-mcp sources/first_party/skills/requesting-code-review sources/first_party/skills/finishing-a-development-branch
  git diff --stat
  git commit -m "docs: add cross-repo draft-PR policy"
  ```

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

### Task 6: Vendor profile installation and third-party profile packaging

**Files:**
- Edit:
  - `sources/first_party/skills/selecting-a-subagent/SKILL.md`
  - `sources/first_party/skills/selecting-a-subagent/references/codex-multi-agent-v1-profile.md`
  - `sources/first_party/skills/selecting-a-subagent/references/codex-multi-agent-v2-profile.md`
  - `sources/first_party/skills/selecting-a-subagent/references/devin-desktop-profile.md`
  - `sources/first_party/skills/refreshing-installed-skills/scripts/refresh_installed_skills.py`
  - `codex-marketplace/custody-pack-registry.json`
- Create (if needed):
  - `sources/first_party/skills/selecting-a-subagent/references/vendor-profile-packaging.md`

**Consumes:** none.

**Interfaces:**
- Marketplace packs can ship third-party subagent `.md` profile assets.
- `refreshing-installed-skills` copies vendor profiles into the Devin/Codex search paths in consumer repos.
- `selecting-a-subagent` documents how to choose between built-in, vendor, and custom profiles.

- [ ] **Step 1: Define the packaging surface.**

  Document the packaging surface in `sources/first_party/skills/selecting-a-subagent/references/vendor-profile-packaging.md`:

  - Vendor profiles live under `assets/profiles/` inside a pack, e.g. `codex-marketplace/plugins/<pack>/assets/profiles/<name>.md`.
  - `refreshing-installed-skills` copies `*.md` files from `assets/profiles/` to `.agents/agents/` (and, if applicable, `.devin/agents/` for repo-local overrides) and records them in `.agents/skills/.provenance.json` under a `vendorProfiles` array.
  - Consumer search path order stays: `.devin/agents/` → `.agents/agents/` → `~/.config/devin/agents/`.

- [ ] **Step 2: Update `selecting-a-subagent`.**

  Add a "Vendor and third-party profiles" section to each dispatch reference (`devin-desktop-profile.md`, `codex-multi-agent-v1-profile.md`, `codex-multi-agent-v2-profile.md`) and the main `SKILL.md` that describes how to discover and select a vendor profile.

- [ ] **Step 3: Update `refreshing-installed-skills`.**

  Extend the refresh script to copy `assets/profiles/*.md` from installed plugins into the correct consumer search path (`.agents/agents/`, `.devin/agents/`, or the platform equivalent) and record them in `.provenance.json` under a `vendorProfiles` array.

- [ ] **Step 4: Add a sample vendor profile.**

  Add one trivial third-party profile asset to an existing pack (or a test pack) and verify the refresh tooling installs it in a clean consumer worktree.

- [ ] **Step 5: Commit.**

  ```bash
  git add sources/first_party/skills/selecting-a-subagent sources/first_party/skills/refreshing-installed-skills codex-marketplace/custody-pack-registry.json
  git diff --stat
  git commit -m "feat: vendor profile installation and third-party profile packaging"
  ```

- [ ] **Step 6: Mark this task `[x]` in this plan before reporting back.**

---

## Final integration

- [ ] **Step 1: Regenerate the marketplace.**

  ```bash
  .\tools\run.ps1 marketplace --apply
  ```

- [ ] **Step 2: Run CI.**

  Stage all changes and let the pre-commit hook run `tools/run ci --check`.

  ```bash
  git add -A
  git commit -m "chore: regenerate marketplace for phase 2 plan"
  ```

- [ ] **Step 3: Push the branch.**

  ```bash
  git push
  ```

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**
