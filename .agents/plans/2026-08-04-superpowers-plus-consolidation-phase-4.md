# Superpowers Plus Consolidation — Phase 4: Doctrine Reconciliation, `review-branch-diff` Retirement, and Mesh Refresh

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `.agents/specs/2026-08-04-superpowers-plus-consolidation-design.md`

**Goal:** Close out the consolidation by (1) making `.agents/doctrine/` the canonical repo-local doctrine store and `.devin/rules/*.md` thin conditional rule triggers, (2) retiring the leftover `review-branch-diff` skill and recording provenance, and (3) running the full validation and mesh refresh so the regenerated marketplace, installed skills, indexes, and mesh all pass `tools/run ci --check`.

**Architecture:** This is the consolidation closeout. First, the repo's mesh law is made self-consistent: `.agents/doctrine/*.md` holds the canonical repo-local doctrine, `.devin/rules/*.md` and `AGENTS.md` files route to it, and `using-superpowers-plus` and `base-doctrine` load the doctrine delta. Then the `review-branch-diff` retirement is committed. Finally the full `tools/run` regeneration stack rebuilds the derived surfaces and the CI gate runs.

**Tech Stack:** Markdown skill docs, git, `tools/run` build pipeline, user-local Devin skill directories.

## Global Constraints

- Do not remove a skill name or surface until all references that point to it are repointed.
- Destructive user-local cleanup (outside the repo tree) requires explicit owner approval before deletion.
- Do not edit or rewrite historical `.agents/specs/` or `.agents/plans/` archives; only active skills, guides, and generated projections may change.
- Edit source first, then regenerate; never hand-edit generated plugin trees, bundle manifests, or index files.
- Every `tools/run * --apply` step must be followed by a commit before the next `tools/run ci --check`.
- All source edits are committed before the marketplace/mesh regeneration begins.
- Do not restate doctrine in `.devin/rules/*.md` or `AGENTS.md` files; those are routing/trigger surfaces. Put the doctrine in `.agents/doctrine/*.md` and use pointers.
- Keep each commit focused on one task; the final task is the validation commit.

## Task ordering

Run the tasks in the order listed. The main ordering constraints are:

- **Task 1** has no dependencies and produces the audit list.
- **Task 2** creates the `.agents/doctrine/` surface and updates the mesh policy.
- **Task 3** moves doctrine from `.devin/rules/*.md` to `.agents/doctrine/*.md` and rewrites the rule files as triggers.
- **Task 4** updates `using-superpowers-plus` and `base-doctrine` to load the `.agents/doctrine/` delta.
- **Task 5** is the `review-branch-diff` retirement and commits before regeneration.
- **Task 6** regenerates all derived surfaces and commits the generated output.
- **Task 7** runs the post-commit CI gate and opens the PR.

No parallel execution is expected.

---

### Task 1: Audit the current doctrine and `review-branch-diff` surfaces

**Files:**
- Read:
  - `.agents/docs/mesh-policy.md` — current mesh law for `.devin/rules/`, `.agents/`, `AGENTS.md`
  - `sources/first_party/skills/using-superpowers-plus/SKILL.md`
  - `sources/first_party/skills/using-superpowers-plus/references/repo-doctrine.md`
  - `sources/first_party/skills/base-doctrine/references/durable-doctrine-routing.md`
  - all `.devin/rules/*.md` (list them and note which contain substantive doctrine)
  - `C:\Users\%USERNAME%\AppData\Roaming\devin\skills\review-branch-diff\SKILL.md` (Windows user-local copy)
  - `~/.config/devin/skills/review-branch-diff/SKILL.md` (macOS/Linux user-local copy)
  - `.agents/skills/.provenance.json`
  - `codex-marketplace/custody-pack-registry.json`
- Check for existence:
  - `sources/first_party/skills/review-branch-diff/`
  - `.agents/skills/review-branch-diff/`
  - `codex-marketplace/plugins/*/skills/review-branch-diff/`
- Scan:
  - `sources/first_party/skills/` for `review-branch-diff`, `/review-branch-diff`, or `branch-reviewer`
  - `.agents/skills/` for `review-branch-diff` or `branch-reviewer`
  - `.agents/guides/` for `review-branch-diff`
  - `.agents/docs/` for `review-branch-diff`
- Create:
  - `Z:\_agent-scratch\consolidate-superpowers-plus-phase-4\2026-08-04-phase-4-audit.md` (off-repo scratch, not committed)

**Consumes:** none.

**Interfaces:**
- A list of every `.devin/rules/*.md` file that currently holds doctrine that belongs in `.agents/doctrine/`.
- A list of every remaining `review-branch-diff` surface.

**Audit commands:**

```powershell
# List all .devin/rules files and note which have more than scope/pointers.
Get-ChildItem .devin\rules\*.md | ForEach-Object {
  $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
  "{0}: {1} lines" -f $_.Name, $lines
}

# Review-branch-diff surface scan.
Get-ChildItem -Path "$env:APPDATA\devin\skills" -Filter "review-branch-diff" -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Path "sources\first_party\skills" -Filter "review-branch-diff" -Recurse
Get-ChildItem -Path ".agents\skills" -Filter "review-branch-diff" -Recurse
Get-ChildItem -Path "codex-marketplace\plugins" -Filter "review-branch-diff" -Recurse
Select-String -Path "codex-marketplace\custody-pack-registry.json" -Pattern "review-branch-diff"
Select-String -Path ".agents\skills\.provenance.json" -Pattern "review-branch-diff"
Select-String -Path "sources\first_party\skills" -Pattern "review-branch-diff" -Recurse
Select-String -Path ".agents\skills" -Pattern "review-branch-diff" -Recurse
Select-String -Path ".agents\guides" -Pattern "review-branch-diff" -Recurse
Select-String -Path ".agents\docs" -Pattern "review-branch-diff" -Recurse
```

- [x] **Step 1: Record the doctrine split findings.**

  For each `.devin/rules/*.md`, record whether it currently contains substantive doctrine, a `Scope`/`Purpose`/`Maintenance` sections, etc. The target state is that all such content moves to `.agents/doctrine/<same-name>.md` and the rule file becomes a thin trigger with a `MUST READ` pointer.

- [x] **Step 2: Record the `review-branch-diff` findings.**

  Read the user-local `SKILL.md` and note the `agent: branch-reviewer` frontmatter. Record any repo-owned, projected, or installed copies and any active references.

- [x] **Step 3: Save the off-repo audit report.**

  Write the findings to `Z:\_agent-scratch\consolidate-superpowers-plus-phase-4\2026-08-04-phase-4-audit.md`. Do not commit this file.

- [x] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

### Task 2: Add `.agents/doctrine/` to the mesh policy and create the directory

**Files:**
- Edit:
  - `.agents/docs/mesh-policy.md`
- Create:
  - `.agents/doctrine/AGENTS.md`
  - `.agents/doctrine/INDEX.md` (generated later; initial hand-authored entry point is `AGENTS.md`)

**Consumes:** Task 1 (audit of current doctrine surfaces).

**Interfaces:**
- The mesh policy explicitly names `.agents/doctrine/*.md` as the canonical repo-local doctrine content surface.
- `.agents/doctrine/AGENTS.md` defines the scope and the routing pointers.

- [x] **Step 1: Add the `.agents/doctrine/` section to mesh-policy.md.**

  Append the following section after the existing last numbered section (`## 6. Mesh self-healing`) in `.agents/docs/mesh-policy.md`. Do not renumber the earlier sections.

  ```markdown
  ## 7. `.agents/doctrine/` doctrine content

  `.agents/doctrine/*.md` is the canonical repo-local doctrine content surface.
  It holds operative repository law that is too large, too scoped, or too dynamic
  for `AGENTS.md` or `.devin/rules/*.md` triggers.

  `.devin/rules/*.md` and `AGENTS.md` are routing/trigger surfaces; they must not
  restate the doctrine. They may carry a short `Scope` and a `MUST READ` pointer
  to the relevant `.agents/doctrine/<topic>.md` file.

  `using-superpowers-plus` and `base-doctrine` load the `.agents/doctrine/`
  delta after the cross-runtime `base-doctrine` invariants.

  Keep each doctrine file focused on one topic. Use `INDEX.md` (generated) for
  navigation; do not hand-maintain a parallel table of contents.
  ```

- [x] **Step 2: Create `.agents/doctrine/AGENTS.md`.**

  ```markdown
  # AGENTS.md

  Scope: `.agents/doctrine/`

  This scope covers the repo's canonical repo-local doctrine content surface.

  Defer to the repository root `AGENTS.md` for global repo doctrine, to
  `.agents/docs/mesh-policy.md` for the canonical mesh statement, and to
  `.devin/rules/*.md` for the conditional rule triggers that route here.

  ## Routing pointers

  - For the mesh law that governs this surface, read `.agents/docs/mesh-policy.md`.
  - For the skill that loads this doctrine, read `sources/first_party/skills/using-superpowers-plus/SKILL.md`.
  - For the list of doctrine topics, read `INDEX.md` (generated by `tools/run mesh --apply`).
  - For the cross-runtime invariants, invoke `/base-doctrine`.
  ```

- [x] **Step 3: Update the repository root `AGENTS.md` routing pointers.**

  Edit the `## Routing pointers` section in `AGENTS.md` (repo root). Replace the bullet:

  ```markdown
  - Scoped law lives in `.devin/rules/*.md`
  ```

  with:

  ```markdown
  - Scoped rule triggers live in `.devin/rules/*.md`; canonical repo-local doctrine lives in `.agents/doctrine/*.md`
  ```

  Do not restate the doctrine in `AGENTS.md`; keep this a thin pointer.

- [x] **Step 4: Commit the mesh policy, scoped AGENTS.md, and root AGENTS.md.**

  ```bash
  git add .agents/docs/mesh-policy.md .agents/doctrine/AGENTS.md AGENTS.md
  git diff --stat
  git commit -m "mesh: establish .agents/doctrine/ as the repo-local doctrine surface

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 3: Migrate doctrine from `.devin/rules/*.md` to `.agents/doctrine/*.md` and thin the rule files

**Files:**
- Create:
  - `.agents/doctrine/<topic>.md` for every `.devin/rules/<topic>.md` that currently contains substantive doctrine
- Edit:
  - `.devin/rules/<topic>.md` for every rule file, replacing the body with a thin `MUST READ` pointer
- Exclude:
  - `.devin/rules/INDEX.md` (generated navigation; do not move)

**Consumes:** Task 2 (`.agents/doctrine/` and mesh policy established).

**Interfaces:**
- `.agents/doctrine/*.md` holds the full doctrine body.
- `.devin/rules/*.md` keeps its frontmatter and becomes a thin trigger that points at `.agents/doctrine/<topic>.md`.

- [x] **Step 1: Run the migration script from the repo root.**

  The migration script is a one-time, off-repo scratch tool. Do not commit it.

  Windows:
  ```powershell
  py -3 Z:\_agent-scratch\consolidate-superpowers-plus-phase-4\migrate_rules_to_doctrine.py
  ```

  macOS/Linux:
  ```bash
  python3 ../_agent-scratch/consolidate-superpowers-plus-phase-4/migrate_rules_to_doctrine.py
  ```

  If the script does not exist, create it with the following content and run it once:

  ```python
  #!/usr/bin/env python3
  # migrate_rules_to_doctrine.py
  # One-time migration: move doctrine body from .devin/rules/*.md to .agents/doctrine/*.md
  # and rewrite the rule file as a thin trigger with a MUST READ pointer.
  # Run from the repository root (not from this scratch path).
  from pathlib import Path
  import re

  rules_dir = Path('.devin/rules')
  doctrine_dir = Path('.agents/doctrine')

  doctrine_dir.mkdir(exist_ok=True)
  frontmatter_re = re.compile(r'^---\r?\n(.*?)\r?\n---\r?\n', re.DOTALL)

  for rule_file in sorted(rules_dir.glob('*.md')):
      if rule_file.name == 'INDEX.md':
          continue
      text = rule_file.read_text(encoding='utf-8')
      match = frontmatter_re.match(text)
      if not match:
          raise ValueError(f'No frontmatter in {rule_file}')
      front = match.group(0)
      body = text[match.end():]

      # Write the doctrine content (no rule frontmatter) to .agents/doctrine/
      doctrine_path = doctrine_dir / rule_file.name
      doctrine_path.write_text(body, encoding='utf-8', newline='\n')

      # Rewrite the rule file as a thin trigger
      thin = (
          "## Scope\n\n"
          f"For the canonical doctrine behind this rule, read `.agents/doctrine/{rule_file.name}`.\n\n"
          "This file is a conditional rule trigger. It does not contain the doctrine; "
          "it only tells the runtime when to load the doctrine from `.agents/doctrine/`. "
          "Do not restate the doctrine here.\n"
      )
      rule_file.write_text(front + thin, encoding='utf-8', newline='\n')

  print('Migration complete. Review the diff before committing.')
  ```

- [x] **Step 2: Inspect the generated files.**

  ```bash
  git diff --stat
  ```

  Verify that:
  - `.agents/doctrine/*.md` contains the former `.devin/rules/*.md` body without `---` frontmatter.
  - `.devin/rules/*.md` keeps its `---` frontmatter and the thin pointer body.
  - No `INDEX.md` was duplicated or deleted.
  - Line endings are LF: `python -c "from pathlib import Path; [print(p, 'has CRLF:', b'\r\n' in p.read_bytes()) for p in Path('.agents/doctrine').glob('*.md')]"`.

- [x] **Step 3: Commit the migration.**

  ```bash
  git add .devin/rules .agents/doctrine
  git diff --stat
  git commit -m "refactor: move doctrine from .devin/rules to .agents/doctrine

.devin/rules/*.md are now thin conditional triggers that route to
.agents/doctrine/*.md for the canonical doctrine.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

- [x] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

### Task 4: Update `using-superpowers-plus` and `base-doctrine` to load the `.agents/doctrine/` delta

**Files:**
- Edit:
  - `sources/first_party/skills/using-superpowers-plus/SKILL.md`
  - `sources/first_party/skills/using-superpowers-plus/references/repo-doctrine.md`
  - `sources/first_party/skills/base-doctrine/references/durable-doctrine-routing.md`

**Consumes:** Task 3 (doctrine migrated to `.agents/doctrine/`).

**Interfaces:**
- `using-superpowers-plus` loads `base-doctrine` then the `.agents/doctrine/` repo-local delta before classifying the request.
- `base-doctrine` includes `.agents/doctrine/` in the source-truth hierarchy.
- `repo-doctrine.md` correctly describes the priority of user instructions, `AGENTS.md`, mesh policy, `.agents/doctrine/`, `.devin/rules/`, and the active skill.

- [x] **Step 1: Update `using-superpowers-plus/SKILL.md` bootstrap step 3.**

  Replace the current step 3:

  ```markdown
  3. **Load doctrine.** Invoke `/base-doctrine` for cross-runtime invariants.
     For how local doctrine and user instructions shape routing, see
     [`references/repo-doctrine.md`](references/repo-doctrine.md).
  ```

  with:

  ```markdown
  3. **Load doctrine.** Invoke `/base-doctrine` for cross-runtime invariants,
     then load the repo-local doctrine from `.agents/doctrine/` by reading
     `.agents/doctrine/AGENTS.md` for scope and the relevant topic files.
     For how local doctrine and user instructions shape routing, see
     [`references/repo-doctrine.md`](references/repo-doctrine.md).
  ```

- [x] **Step 2: Rewrite `using-superpowers-plus/references/repo-doctrine.md`.**

  Replace the file content with:

  ```markdown
  # Repo doctrine and user instructions

  User instructions (explicit requests), repo-local doctrine, and the active skill
  all shape routing. The canonical repo-local doctrine surfaces are:

  - Root `AGENTS.md` for global repo doctrine and publication rules.
  - `.agents/docs/mesh-policy.md` for the canonical mesh statement.
  - `.agents/doctrine/*.md` for repository-local operative doctrine.
  - `.devin/rules/*.md` for conditional rule triggers; they do not contain the doctrine.

  If they explicitly conflict, follow this priority:

  1. Explicit human instruction.
  2. Root `AGENTS.md` and `.agents/docs/mesh-policy.md`.
  3. Repo-local doctrine in `.agents/doctrine/`.
  4. Conditional rule triggers (`.devin/rules/*.md`) and the active skill.
  5. Default behavior.

  Only skip a skill workflow when your human partner has explicitly told you to.
  ```

- [x] **Step 3: Update `base-doctrine/references/durable-doctrine-routing.md`.**

  In the source-truth hierarchy, find the line:

  ```markdown
  - Specific GPT-native skill: detailed workflow, output contract, checklist, or tool procedure.
  ```

  and insert the following bullet immediately after it:

  ```markdown
  - `.agents/doctrine/*.md`: repo-local operative doctrine that is too large or
    too dynamic for `AGENTS.md`/`.devin/rules` triggers; loaded by `using-superpowers-plus`.
  ```

  The hierarchy should then read, in order:

  ```markdown
  - System prompt: tiny boot/routing invariants needed before skills load.
  - cross-runtime doctrine skill: cross-project rules and contracts not owned elsewhere.
  - Specific GPT-native skill: detailed workflow, output contract, checklist, or tool procedure.
  - `.agents/doctrine/*.md`: repo-local operative doctrine...
  - Canonical agent asset repo: versioned source truth for GPT-native skill sources...
  ```

- [x] **Step 4: Commit the skill updates.**

  ```bash
  git add sources/first_party/skills/using-superpowers-plus sources/first_party/skills/base-doctrine
  git diff --stat
  git commit -m "docs: load .agents/doctrine/ as the repo-local doctrine delta

Update using-superpowers-plus, repo-doctrine.md, and base-doctrine
so the bootstrap loads base-doctrine then .agents/doctrine/.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

- [x] **Step 5: Mark this task `[x]` in this plan before reporting back.**

---

### Task 5: Retire the `review-branch-diff` skill

**Files:**
- Delete (if they exist):
  - `sources/first_party/skills/review-branch-diff/`
  - `.agents/skills/review-branch-diff/`
  - `codex-marketplace/plugins/*/skills/review-branch-diff/`
  - `C:\Users\%USERNAME%\AppData\Roaming\devin\skills\review-branch-diff\` (Windows)
  - `~/.config/devin/skills/review-branch-diff/` (macOS/Linux)
- Edit (if needed):
  - `.agents/skills/.provenance.json` to remove any `review-branch-diff` or `branch-reviewer` entries
  - `codex-marketplace/custody-pack-registry.json` to remove any `review-branch-diff` pack entries
- Create:
  - `provenance/2026-08-04-review-branch-diff-retired.md`

**Consumes:** Task 1 (audit findings).

**Interfaces:**
- No `review-branch-diff` file, directory, or registry entry remains in repo source or projected surfaces.
- The user-local skill is removed after explicit approval, or the blocker is recorded.

- [x] **Step 1: Remove any repo-owned copies.**

  If the audit found `review-branch-diff` under `sources/first_party/skills/`, `.agents/skills/`, or `codex-marketplace/plugins/`, delete them with git tracking:

  ```powershell
  git rm -r sources/first_party/skills/review-branch-diff 2>$null
  git rm -r ".agents/skills/review-branch-diff" 2>$null
  Remove-Item -Recurse -Force codex-marketplace\plugins\*\skills\review-branch-diff -ErrorAction SilentlyContinue
  ```

- [x] **Step 2: Remove the user-local skill after approval.**

  If the repo owner approves the destructive user-local cleanup, run:

  Windows:
  ```powershell
  Remove-Item -Recurse -Force "$env:APPDATA\devin\skills\review-branch-diff"
  if (Test-Path "$env:APPDATA\devin\skills\review-branch-diff") { throw 'user-local review-branch-diff still exists' }
  ```

  macOS/Linux:
  ```bash
  rm -rf ~/.config/devin/skills/review-branch-diff
  [ -d ~/.config/devin/skills/review-branch-diff ] && exit 1
  ```

  If approval is withheld, record the blocker in the provenance note and proceed.

- [x] **Step 3: Clean any stale registry or provenance entries.**

  If the audit found `review-branch-diff` in `codex-marketplace/custody-pack-registry.json` or `.agents/skills/.provenance.json`, edit the files to remove the entries. Then run `py -3 tools/run.py installed-skills --apply` to resync the installed skill surface.

- [x] **Step 4: Verify the repo tree is clean of `review-branch-diff` files.**

  ```powershell
  Select-String -Path "codex-marketplace\custody-pack-registry.json" -Pattern "review-branch-diff"
  Select-String -Path ".agents\skills\.provenance.json" -Pattern "review-branch-diff"
  if (Test-Path "sources\first_party\skills\review-branch-diff") { throw 'repo source still exists' }
  ```

- [x] **Step 5: Write the provenance note.**

  Create `provenance/2026-08-04-review-branch-diff-retired.md` with the following content:

  ```markdown
  # review-branch-diff retired

  ## Provenance

  - **Retired:** 2026-08-04
  - **Original source:** `~/.config/devin/skills/review-branch-diff/` (macOS/Linux) or `%APPDATA%\devin\skills\review-branch-diff\` (Windows)
  - **New home:** Whole-branch diff review is performed by a `subagent_explore`-based reviewer or by invoking `/requesting-code-review` with the branch/PR diff review lane.
  - **Reason:** The `review-branch-diff` skill was a local helper that ran entirely as the `branch-reviewer` subagent and could not gather an explicit branch and worktree on the main agent. The canonical branch diff review flow now uses the main agent to prepare the diff and dispatch a reviewer subagent.

  ## What changed

  | Old path | New state |
  | --- | --- |
  | `~/.config/devin/skills/review-branch-diff/SKILL.md` (or `%APPDATA%\devin\skills\review-branch-diff\SKILL.md`) | deleted, or deletion blocked by repo-owner policy (recorded here) |
  | `sources/first_party/skills/review-branch-diff/` | not in repo custody; confirmed absent |
  | `codex-marketplace/plugins/*/skills/review-branch-diff/` | not projected; confirmed absent |
  | `.agents/skills/review-branch-diff/` | not installed; confirmed absent |

  ## Routing updates

  - Branch diff review is no longer a dedicated skill invocation.
  - `/requesting-code-review` owns the branch/PR diff review lane.
  - `subagent-driven-development` final whole-branch review uses `subagent_explore` or `/requesting-code-review`, not `/review-branch-diff`.
  - `selecting-a-subagent` uses `reviewer-strong` for full branch/PR diff reviews.

  ## User-local deletion

  - **Status:** <deleted / blocked / not present>
  - **Blocker (if any):** <none or owner withheld destructive user-local cleanup>

  ## Source of truth

  Branch diff review behavior is now owned by `sources/first_party/skills/requesting-code-review/` and `sources/first_party/skills/subagent-driven-development/`.
  ```

- [x] **Step 6: Commit the retirement and provenance.**

  ```bash
  git add -A
  git diff --stat
  git commit -m "chore: retire review-branch-diff skill

Remove any repo-owned or projected copies, record provenance, and
remove the user-local copy with owner approval.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

- [x] **Step 7: Mark this task `[x]` in this plan before reporting back.**

---

### Task 6: Regenerate marketplace, installed skills, repo index, and mesh

**Files:**
- Generated (do not hand-edit):
  - `codex-marketplace/` plugin projections
  - `.agents/skills/` installed copies
  - `repo-index/`
  - `.agents/INDEX.md`
  - `.agents/plans/INDEX.md`
  - `.agents/specs/INDEX.md`
  - `.agents/guides/INDEX.md`
  - `.agents/skills/INDEX.md`
  - `.agents/agents/INDEX.md`
  - `.agents/doctrine/INDEX.md`
  - `codex-marketplace/INDEX.md`
  - all `codex-marketplace/plugins/*/*/INDEX.md` files generated by the mesh target

**Consumes:** Tasks 2–5 (all source edits committed).

**Interfaces:**
- Derived surfaces reflect the current source and the new `.agents/doctrine/` surface.
- No stale `review-branch-diff`, `branch-reviewer`, or `.devin/rules` doctrine references remain.

- [ ] **Step 1: Run the full regeneration stack.**

  ```powershell
  py -3 tools/run.py marketplace installed-skills repo-index mesh --apply
  ```

- [ ] **Step 2: Inspect the generated diff for stale references and drift.**

  ```bash
  git diff --stat
  ```

  Look for:
  - Any reintroduction of `review-branch-diff` or `branch-reviewer`.
  - Any `.devin/rules/*.md` that still has more than frontmatter + thin pointer.
  - Any `INDEX.md` that does not list the new `.agents/doctrine/` topic files.

  If any appear, do not hand-edit the generated files; fix the source and re-run this task.

- [ ] **Step 3: Commit the regenerated surfaces.**

  ```bash
  git add -A
  git diff --stat
  git commit -m "chore: regenerate marketplace, installed skills, indexes, and mesh

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>"
  ```

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

### Task 7: Run the final CI gate and open the PR

**Files:**
- None (validation and publication only).

**Consumes:** Task 6 (regenerated surfaces committed).

**Interfaces:**
- A green `tools/run ci --check` result and a draft PR on `origin/main`.

- [ ] **Step 1: Run the CI preflight on the committed tree.**

  ```powershell
  py -3 tools/run.py ci --check
  ```

  If this fails, fix the failures in the appropriate source and restart from the relevant earlier task.

- [ ] **Step 2: Push the branch.**

  ```bash
  git push origin consolidate-superpowers-plus-phase-4
  ```

- [ ] **Step 3: Open a draft PR.**

  Write the PR body to an off-repo scratch file and use `--body-file`:

  Windows:
  ```powershell
  $body = "Z:\_agent-scratch\consolidate-superpowers-plus-phase-4\pr-body.md"
  "## Summary`n- Establishes `.agents/doctrine/` as the canonical repo-local doctrine store and thins `.devin/rules/*.md` to conditional rule triggers.`n- Updates `using-superpowers-plus` and `base-doctrine` to load the `.agents/doctrine/` delta.`n- Retires the local `review-branch-diff` skill and records provenance.`n- Regenerates marketplace, installed skills, repo indexes, and agent mesh.`n- Passes `tools/run ci --check`.`n`n## Test plan`n- [ ] `tools/run marketplace installed-skills repo-index mesh --apply` passed`n- [ ] `tools/run ci --check` passed" | Set-Content -Path $body -Encoding UTF8 -NoNewline
  gh pr create --title "chore: phase 4 consolidation — doctrine reconciliation, review-branch-diff retirement, and mesh refresh" --body-file $body --base main --draft
  ```

  macOS/Linux:
  ```bash
  body="../_agent-scratch/consolidate-superpowers-plus-phase-4/pr-body.md"
  cat > "$body" <<'EOF'
  ## Summary
  - Establishes `.agents/doctrine/` as the canonical repo-local doctrine store and thins `.devin/rules/*.md` to conditional rule triggers.
  - Updates `using-superpowers-plus` and `base-doctrine` to load the `.agents/doctrine/` delta.
  - Retires the local `review-branch-diff` skill and records provenance.
  - Regenerates marketplace, installed skills, repo indexes, and agent mesh.
  - Passes `tools/run ci --check`.

  ## Test plan
  - [ ] `tools/run marketplace installed-skills repo-index mesh --apply` passed
  - [ ] `tools/run ci --check` passed
  EOF
  gh pr create --title "chore: phase 4 consolidation — doctrine reconciliation, review-branch-diff retirement, and mesh refresh" --body-file "$body" --base main --draft
  ```

- [ ] **Step 4: Mark this task `[x]` in this plan before reporting back.**

---

## SDD confidence rating

**8/10.** The scope is now broader and the `.devin/rules` to `.agents/doctrine/` migration is the largest unknown. The migration script and exact rewrites are specified, but the implementer must verify that the thin rule files still trigger correctly and that no `INDEX.md` or generated surface is accidentally corrupted. A careful first pass should raise this to 9/10 before execution.
