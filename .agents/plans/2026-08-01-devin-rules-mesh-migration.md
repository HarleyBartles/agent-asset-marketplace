# Devin Rules Mesh Migration

> **For agentic workers:** REQUIRED SUB-SKILL: Use `/subagent-driven-development` (recommended) or `/executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stop the `AGENTS.md` rule overload in Devin Local by migrating scoped rules to `.devin/rules/*.md`, thinning the root `AGENTS.md`, and updating the mesh policy to match the runtime's actual behavior.

**Architecture:** Devin Local / Devin CLI loads every discovered `AGENTS.md` as an always-on rule. Scoped, conditional, or directory-specific law therefore cannot live in sub-directory `AGENTS.md`. The migration moves that scoped law to `.devin/rules/*.md` with explicit `trigger:` frontmatter. Long reference content moves to `.agents/guides/` or `README.md`. Root `AGENTS.md` is reduced to a small set of genuinely always-on rules and routing pointers.

**Tech Stack:** Markdown, Devin Rules frontmatter, existing `tools/run` marketplace/mesh pipeline, git, GitHub.

## Global Constraints

- Do not create `.agents/rules/`; Devin Local does not read it and the repo should not invent a projection for it.
- Keep each `.devin/rules/*.md` under 12,000 characters.
- Keep root `AGENTS.md` under 50 lines and sub-directory `AGENTS.md` under 20 lines if they must survive.
- Generated `AGENTS.md` surfaces (under `codex-marketplace/**`, `sources/first_party/**` projections, etc.) must be removed by editing their source or generator, not by hand.
- All changes must pass `tools/run ci --check` before a PR is called green.
- Publication proof must be a GitHub PR into `main` per root `AGENTS.md`.

---

### Task 1: Audit all `AGENTS.md` files and classify them

**Files:**
- Read-only scan: `find_file_by_name "**/AGENTS.md"` in the repo root
- Output: a table saved to `provenance/2026-08-01-agents-md-migration-audit.md`

**Interfaces:**
- Consumes: the current list of `AGENTS.md` files (discovered by the audit)
- Produces: a classification table mapping each `AGENTS.md` to one of:
  - `keep-thin` (genuinely always-on, keep as `AGENTS.md` but shorten)
  - `devin-rule` (scoped/conditional law, rewrite as `.devin/rules/*.md` with `trigger: glob`)
  - `guide` (reference/procedure, rewrite as a `.agents/guides/` doc named after the source scope)
  - `readme` (human discovery, rewrite as `README.md`)
  - `delete` (no longer useful)
  - `regenerate-source` (generated `AGENTS.md`, remove by fixing source or generator)

- [ ] **Step 1: List every `AGENTS.md` file**

  Run: `find_file_by_name "**/AGENTS.md"` or `git ls-files "**/AGENTS.md"`.

- [ ] **Step 2: Classify each file**

  For each file, decide its fate based on the four-question test:
  1. Is it generated from a marketplace/source projection? -> `regenerate-source`
  2. Does it contain law that must be always-on for the whole repo? -> `keep-thin`
  3. Does it contain law that should only apply in a specific directory or file pattern? -> `devin-rule`
  4. Is it guidance, procedure, or reference? -> `guide` or `readme`

- [ ] **Step 3: Record the classification table**

  Save the table to `provenance/2026-08-01-agents-md-migration-audit.md`. Include the full path and the chosen disposition for every file.

- [ ] **Step 4: Get review on the classification**

  Before moving files, have a human review the classification. Misclassified generated `AGENTS.md` files will reappear on the next `tools/run marketplace --apply`.

---

### Task 2: Update `.agents/docs/mesh-policy.md`

**Files:**
- Modify: `.agents/docs/mesh-policy.md` (draft already exists in this worktree)

**Interfaces:**
- Consumes: the current `mesh-policy.md` and Devin documentation
- Produces: canonical mesh policy that no longer claims sub-directory `AGENTS.md` scoping

- [ ] **Step 1: Confirm the updated `AGENTS.md` mesh section**

  The section must state:
  - `AGENTS.md` is always-on in Devin Local once discovered.
  - Sub-directory `AGENTS.md` does not scope by working directory.
  - Root `AGENTS.md` is for genuinely always-on law only.
  - Law that is not always-on belongs in `.devin/rules/*.md`.

- [ ] **Step 2: Confirm the new `.devin/rules/` section**

  The section must describe:
  - `.devin/rules/*.md` as the canonical surface for scoped rules.
  - The `trigger` values: `always_on`, `glob`, `model_decision`, `manual`.
  - The 12,000 character limit per rule file.
  - An example with `trigger: glob` and `globs:`.

- [ ] **Step 3: Run `tools/run ci --check` for the policy change alone**

  This ensures the mesh policy update does not break repo-shape or index-mesh validation before the rest of the migration is attempted.

---

### Task 3: Thin the root `AGENTS.md`

**Files:**
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: current root `AGENTS.md`, updated `mesh-policy.md`
- Produces: a root `AGENTS.md` that fits in ~30-50 lines and is safe to always load

- [ ] **Step 1: Remove detailed content that is not always-on**

  Delete or move the following to `.agents/guides/`:
  - Long command lists (e.g., the full `tools/run` matrix from `tools/AGENTS.md`)
  - Per-directory review guidelines that should be scoped
  - Source/projection details that are already in guides

- [ ] **Step 2: Add pointer to `.devin/rules/` and guides**

  Add a short routing section:
  - `For directory-scoped rules, see .devin/rules/*.md`
  - `For procedures, see .agents/guides/` and `docs/AGENTS.md`

- [ ] **Step 3: Verify root `AGENTS.md` is under 50 lines**

  Count lines. If still over, keep cutting until only always-on law remains.

---

### Task 4: Create `.devin/rules/*.md` for the first batch of scoped rules

**Files (example set based on the current AGENTS.md surface):**
- Create: `.devin/rules/tools.md` from `tools/AGENTS.md`
- Create: `.devin/rules/docs.md` from `docs/AGENTS.md`
- Create: `.devin/rules/agents.md` from `.agents/AGENTS.md`
- Create: `.devin/rules/agents-docs.md` from `.agents/docs/AGENTS.md`
- Create: `.devin/rules/sources.md` from `sources/AGENTS.md`
- Create: `.devin/rules/provenance.md` from `provenance/AGENTS.md`
- Create: `.devin/rules/adapters.md` from `adapters/AGENTS.md`
- Create: `.devin/rules/codex-marketplace.md` from `codex-marketplace/AGENTS.md`

**Interfaces:**
- Consumes: the content of the `AGENTS.md` files being migrated
- Produces: scoped, trigger-activated rule files

- [ ] **Step 1: Write each rule with frontmatter**

  Pattern:

  ```markdown
  ---
  description: "tools and marketplace generation"
  trigger: glob
  globs: "tools/**"
  ---

  - Run `tools/run ci --check` for the CI gate.
  - For full procedures, see `.agents/guides/marketplace-tooling-guide.md`.
  ```

- [ ] **Step 2: Move heavy procedure content to guides**

  For each rule, if the content is over 100 lines or is mostly reference, create a `.agents/guides/` doc named after the source scope and make the rule a short pointer.

- [ ] **Step 3: Validate character limits**

  Ensure every `.devin/rules/*.md` is under 12,000 characters. If it is over, split into multiple rules or move content to a guide.

---

### Task 5: Delete or convert the sub-directory `AGENTS.md` files

**Files (example set based on the current AGENTS.md surface):**
- Delete: `tools/AGENTS.md`, `docs/AGENTS.md`, `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, `sources/AGENTS.md`, `provenance/AGENTS.md`, `adapters/AGENTS.md`, `codex-marketplace/AGENTS.md`, `codex-marketplace/plugins/AGENTS.md`, and other authored sub-`AGENTS.md` files.
- Modify source/generator for: `sources/first_party/skills/**/AGENTS.md`, `sources/third_party/**/AGENTS.md`, `codex-marketplace/plugins/**/AGENTS.md` (projected/generated copies)

**Interfaces:**
- Consumes: the classification from Task 1
- Produces: a repo with a minimal `AGENTS.md` surface

- [ ] **Step 1: Delete authored sub-`AGENTS.md` files that have been converted**

  Run `git rm` on each. Do not delete by hand in a way that leaves untracked orphans.

- [ ] **Step 2: Convert `delete` files to `README.md` or guides if they had useful content**

  If the content is still useful for humans but not as a rule, move it to `README.md` or `.agents/guides/` and delete the `AGENTS.md`.

- [ ] **Step 3: Fix generated `AGENTS.md` at the source**

  For `AGENTS.md` files under `codex-marketplace/`, `sources/first_party/` (projected), etc.:
  - Find the source template or generator that emits them.
  - Remove `AGENTS.md` from the generated outputs.
  - Run `tools/run marketplace --apply` and `tools/run ci --check`.

- [ ] **Step 4: Update any hard-coded references to the deleted `AGENTS.md` files**

  Grep for the deleted paths and update them to the new surface (`README.md`, `.devin/rules/*.md`, or `.agents/guides/`).

---

### Task 6: Update repo guides and routing

**Files:**
- Modify: `.agents/docs/repo-guide-policy.md`
- Modify or create: the `.agents/guides/` files named in the audit (for example, `.agents/guides/marketplace-tooling-guide.md`)

**Interfaces:**
- Consumes: the new rule surface and the deleted `AGENTS.md` files
- Produces: authoritative guides that the rules and root `AGENTS.md` route to

- [ ] **Step 1: Document `.devin/rules/` in the repo guide policy**

  Add a row or section explaining that `.devin/rules/*.md` is the canonical scoped rule surface for Devin Local and that new scoped rules belong there.

- [ ] **Step 2: Move long procedural content from `tools/AGENTS.md` to a guide**

  Create `.agents/guides/marketplace-tooling-guide.md` containing the full `tools/run` matrix, command details, and workflow notes.

- [ ] **Step 3: Move skill/worktree guidance from `.agents/skills/AGENTS.md` and `docs/AGENTS.md` to guides if needed**

  Ensure no unique information is lost when `AGENTS.md` files are deleted.

---

### Task 7: Add a CI gate to prevent regression

**Files:**
- Create: `tools/validate_agents_md.py`
- Modify: `tools/run.py` and `tools/run.ps1` to run the new validator in the `mesh` target

**Interfaces:**
- Consumes: the new mesh policy and the list of allowed `AGENTS.md` files
- Produces: a CI check that fails if the mesh policy is violated

- [ ] **Step 1: Define the allow-list of `AGENTS.md` files**

  After migration, the allowed tracked `AGENTS.md` files are:
  - root `AGENTS.md`
  - `.agents/AGENTS.md` if the audit confirms it is genuinely always-on
  - `AGENTS.local.md` (gitignored, not tracked)

  Any tracked `AGENTS.md` found outside this list causes the validator to fail and `tools/run ci --check` to return non-zero.

- [ ] **Step 2: Implement `tools/validate_agents_md.py`**

  The script must:
  - Find every tracked `AGENTS.md` file (exclude `AGENTS.local.md` and untracked files).
  - Compare it to the allow-list.
  - Report the exact unexpected paths.
  - Check every `.devin/rules/*.md` for a `trigger` and `description` in its frontmatter and fail if the file is over 12,000 characters.

- [ ] **Step 3: Wire the validator into `tools/run`**

  Add `validate_agents_md.py --check` to the `mesh` target in `tools/run.py` (and `tools/run.ps1`) so it runs during `tools/run ci --check`.

---

### Task 8: Regenerate indexes and verify the repo mesh

**Files:**
- Generated: `INDEX.md` files across the repo

**Interfaces:**
- Consumes: the deleted/renamed files and new `.devin/rules/` surface
- Produces: a valid, regenerated mesh

- [ ] **Step 1: Run `tools/run marketplace --apply`**

  This regenerates the marketplace projections and installed skills.

- [ ] **Step 2: Run `tools/run mesh --apply`**

  This regenerates the `INDEX.md` mesh.

- [ ] **Step 3: Run `tools/run ci --check`**

  This validates the full repo surface.

- [ ] **Step 4: Inspect the diff**

  Ensure the diff contains only the intended deletions, the new `.devin/rules/` files, the thinned `AGENTS.md`, and regenerated `INDEX.md` files. No new `AGENTS.md` should appear.

---

### Task 9: Commit and publish

**Files:**
- All changed files in the worktree

**Interfaces:**
- Consumes: the green `tools/run ci --check` result
- Produces: a GitHub PR with branch name and head SHA

- [ ] **Step 1: Stage all changes**

  `git add -A` or explicit `git add` of the changed files.

- [ ] **Step 2: Commit with a clear message**

  Commit message:

  ```text
  docs(mesh): migrate scoped law from AGENTS.md to .devin/rules

  - Update .agents/docs/mesh-policy.md to reflect Devin Local's always-on
    AGENTS.md loading and the correct use of .devin/rules/*.md for scoped rules.
  - Thin root AGENTS.md to always-on law only.
  - Add .devin/rules/*.md for scoped directory rules.
  - Delete or convert sub-directory AGENTS.md to guides/README/devin-rules.
  - Update validators and regenerate indexes.
  ```

- [ ] **Step 3: Push the branch and open a PR**

  `git push -u origin plan-rule-mesh-migration`

  Use `gh pr create` with a summary and verification evidence.

- [ ] **Step 4: Provide publication proof**

  Return the PR URL, branch name, and full head SHA.
