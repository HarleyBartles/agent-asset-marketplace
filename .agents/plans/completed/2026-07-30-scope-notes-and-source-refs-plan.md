# Scope Notes and Source-Reference Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Implement the approved design: add the dependency-order gate to `handoff-gates`, fill `scope-notes.md` for `handoff-gates` and `working-with-epics`, document the convention, and convert `writing-with-clarity` source reference from HTML to chapter Markdown.

**Architecture:** Edit first-party skill source in place, update `assets/authority/source-map.yaml` where present, source a public-domain `Elements of Style` text, split it into chapter files, then regenerate the marketplace and run CI.

**Tech Stack:** Markdown, YAML, `tools/run marketplace --apply`, `tools/run ci --check`, `gh` for PR.

## Global Constraints

- Keep `SKILL.md` bodies under 500 words where possible.
- Do not modify `skill-frontmatter.md` schema.
- Do not hand-edit `generated/skill-zips/`; they will update automatically as a side effect of marketplace regeneration.
- Record provenance for any new source text in `assets/authority/CITATIONS.md` and `authority.yaml`.
- Do not use double quotes in frontmatter strings to keep `normalize_first_party_skill_sources.py` safe.

---

### Task 1: Update `.agents/doctrine/skill-standards-policy.md`

**Files:**
- Modify: `.agents/doctrine/skill-standards-policy.md`

Add a `### Scope notes` subsection under the skill body / reference guidance section with the following text:

```markdown
### Scope notes

When a first-party skill has real but non-primary boundary cases, move the expanded guidance to `references/scope-notes.md` and keep `SKILL.md` focused on the primary lanes.

- Do not create an empty `references/scope-notes.md` just because the convention exists.
- Wire the reference through three surfaces:
  1. The `do_not_use_when` frontmatter item, ending with `(see references/scope-notes.md for <case>)`.
  2. A short `## Boundary cases` or `## When this skill is not what you need` call-out near the bottom of `SKILL.md`.
  3. `assets/authority/source-map.yaml`, if the skill has one, with `load_when` conditions that match the body call-out.
- Keep `references/scope-notes.md` short. If it exceeds one screen, split it into topical files under `references/` instead of one long catch-all.
```

- [x] Insert the section in the right place.
- [x] Run `python tools/normalize_first_party_skill_sources.py --check`? No, this is a docs file. Just verify the file renders with `python -m markdown` or a quick read.
- [x] Mark completed.

---

### Task 2: Update `handoff-gates/SKILL.md`

**Files:**
- Modify: `sources/first_party/skills/handoff-gates/SKILL.md`

Add the dependency-order bullet as the first item in the `Plan-Readiness Checklist`:

```markdown
- [x] **Dependency-order coherence.** For each task, the `Consumes` block names only outputs from tasks that appear earlier in the plan. No task may consume an output from a task scheduled later. If a later task's output is needed earlier, either move the producer earlier, split an intermediate step, or add an explicit bridge/proxy.
```

Reframe the existing `Task ordering` bullet to:

```markdown
- [x] **Task ordering.** The general rule is that producers come before consumers. In this repo, that means all source and adapter/overlay edits are scheduled before any `tools/run * --apply` regeneration step.
```

Add a `## Boundary cases` section at the bottom:

```markdown
## Boundary cases

If the artifact is intentionally thin, depends on an external blocker, or the handoff touches `verification-before-completion` or `requesting-code-review`, load `references/scope-notes.md` and follow its guidance. Only proceed when the reference gives a green path.
```

Update the `do_not_use_when` frontmatter from:
- `Do not use when the artifact is not clearly at a stage boundary.`

to:
- `Do not use when the artifact is not clearly at a stage boundary. (see references/scope-notes.md for boundary cases)`

- [x] Apply the `SKILL.md` edits.
- [x] Mark completed.

---

### Task 3: Update `handoff-gates/references/scope-notes.md` and `source-map.yaml`

**Files:**
- Write: `sources/first_party/skills/handoff-gates/references/scope-notes.md`
- Modify: `sources/first_party/skills/handoff-gates/assets/authority/source-map.yaml`

Write `references/scope-notes.md` with the following content:

```markdown
# Scope Notes

Use when the main `handoff-gates` lanes do not cleanly fit the artifact or the boundary is unclear.

## Thin or co-designed specs

A spec may be intentionally thin because the user wants to co-design. Do not reject it for missing details. Instead:

- Rate the spec on whether the next planning stage can proceed without inventing scope.
- If the user explicitly kept decisions open, name and bound each open question and assign it to a specific stage or owner.
- If the open questions are bounded, hand off to `writing-plans` with the rating and the list of user-owned decisions.
- If the open questions are not bounded enough to plan, do not hand off. Return to `brainstorming`.

## Plans with external blockers

A plan may depend on a third-party API, a pending user decision, an upstream release, or another external event.

- Separate the plan into **contained** tasks the agent can do now and **blocked** tasks that require the external thing.
- If the contained tasks form a meaningful, testable slice, rate the slice and hand it off. Leave the blocked tasks in the roadmap, not in this plan.
- If there is no meaningful contained slice, the plan is not at a stage boundary. Classify as `blocked`, do not hand off, and return to `writing-plans` or `working-with-epics`.

## Overlap with verification and review

`handoff-gates` is a stage-boundary readiness check, not a final verification or a review request.

- Use `handoff-gates completion-readiness` before `verification-before-completion` or `requesting-code-review`.
- Use `verification-before-completion` when you are about to claim the work is green and a fresh command can prove it.
- Use `requesting-code-review` to dispatch a subagent reviewer.
- Use `receiving-code-review` when the subagent reviewer returns feedback.
- If `completion-readiness` finds a likely defect, do not skip straight to `requesting-code-review`. Return to `finishing-a-development-branch` or `executing-plans` first.

## Return posture

When a boundary case applies, return:

- the final rating if it is still ≥ 8;
- the lane;
- the specific boundary exception that led to this reference;
- the next skill or stage the artifact should move to.
```

Update `assets/authority/source-map.yaml` to:

```yaml
schema_version: 1
reconciled_against: 82a1c050fdf69df1473f44ca07074e9af07b8890e6acd4b7e7992b0308e98b9a
references:
  - path: references/scope-notes.md
    source_sections:
      - Thin or co-designed specs
      - Plans with external blockers
      - Overlap with verification and review
    load_when:
      - Use when the artifact is intentionally thin.
      - Use when the plan depends on an external blocker.
      - Use when the handoff overlaps with verification-before-completion or requesting-code-review.
    content_mode: first_party_synthesis
```

- [x] Write `scope-notes.md`.
- [x] Update `source-map.yaml`.
- [x] Mark completed.

---

### Task 4: Update `working-with-epics/SKILL.md`

**Files:**
- Modify: `sources/first_party/skills/working-with-epics/SKILL.md`

Add a `## Boundary cases` section at the bottom:

```markdown
## Boundary cases

If a roadmap item should split into a new epic, a scope change invalidates multiple pending plans, or you are choosing between asking the human and escalating through `risk-gates`, load `references/scope-notes.md` and follow its guidance.
```

Update the `do_not_use_when` frontmatter from:
- `Do not use when the goal fits a single tight writing-plans plan.`

to:
- `Do not use when the goal fits a single tight writing-plans plan. (see references/scope-notes.md when the boundary between one plan and a new epic is unclear)`

- [x] Apply the `SKILL.md` edits.
- [x] Mark completed.

---

### Task 5: Update `working-with-epics/references/scope-notes.md` and `source-map.yaml`

**Files:**
- Write: `sources/first_party/skills/working-with-epics/references/scope-notes.md`
- Modify: `sources/first_party/skills/working-with-epics/assets/authority/source-map.yaml`

Write `references/scope-notes.md` with the following content:

```markdown
# Scope Notes

Use when the main `working-with-epics` guidance does not cleanly cover the case in front of you.

## When a roadmap item should become a new epic

A single plan may grow until it contains multiple independent subsystems. If the current plan is already too large for `writing-plans`, do not force it. Instead:

- Extract the oversized or independent subsystem into a new epic.
- Add it to the roadmap as a pending future plan.
- Leave the current epic focused on the original goal.
- Hand off the new epic to `brainstorming` or `writing-plans` when it becomes the active plan.

## How to handle scope changes that invalidate multiple pending plans

When a decision changes the path for several roadmap items:

- Do not edit every pending plan at once.
- Update the roadmap table with the new path and mark the affected plans as `blocked` or `replan`.
- Re-write the next plan only; leave the others as placeholders.
- Document the change in `Handoff Notes` so the next agent understands why the roadmap shifted.

## When to ask the human a focused question versus escalating through risk-gates

If the next step depends on an unresolved assumption or a value judgement:

- Ask the human one focused question when the answer is a preference, business call, or missing fact.
- Use `risk-gates` when the proposed action could violate scope, authority, canon, or safety.
- Do not ask the human a question that is really a safety/authority decision in disguise. Route those to `risk-gates`.
```

Update `assets/authority/source-map.yaml` to:

```yaml
schema_version: 1
reconciled_against: 5d0b17d0ced31c5f7e5fa196e088c525c816ea74dce35f0688075e81e789e14e
references:
  - path: references/scope-notes.md
    source_sections:
      - When a roadmap item should become a new epic
      - How to handle scope changes that invalidate multiple pending plans
      - When to ask the human a focused question versus escalating through risk-gates
    load_when:
      - Use when a roadmap item should be split into a new epic.
      - Use when a scope change invalidates multiple pending plans.
      - Use when deciding between asking the human and escalating through risk-gates.
    content_mode: first_party_synthesis
```

- [x] Write `scope-notes.md`.
- [x] Update `source-map.yaml`.
- [x] Mark completed.

---

### Task 6: Source and convert `Elements of Style`

**Files:**
- Delete: `sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918.html`
- Create: `sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918/<chapter>.md`

**Consume:** The approved design and the public-domain text from a source such as Project Gutenberg.
**Produce:** One Markdown file per chapter in `assets/authority/reference-source/elements-of-style-1918/`.

Expected chapter files (adjust slugs to match the source if it uses different headings):
- `introductory.md`
- `elementary-rules-of-usage.md`
- `elementary-principles-of-composition.md`
- `a-few-matters-of-form.md`
- `words-and-expressions-commonly-misused.md`
- `spelling.md`

Steps:

- [x] Download the public-domain text and record the source URL.
- [x] Strip markup, navigation, and any non-book content.
- [x] Delete the old `elements-of-style-1918.html`.
- [x] Split the cleaned text into one file per chapter, preserving `##` headings.
- [x] Mark completed.

---

### Task 7: Update `writing-with-clarity` source map and skill body

**Files:**
- Modify: `sources/first_party/skills/writing-with-clarity/SKILL.md`
- Modify: `sources/first_party/skills/writing-with-clarity/assets/authority/source-map.yaml`
- Modify: `sources/first_party/skills/writing-with-clarity/assets/authority/CITATIONS.md`
- Modify: `sources/first_party/skills/writing-with-clarity/assets/authority/authority.yaml`

Update `SKILL.md` lines 41–45 to:

```markdown
Do not read `assets/authority/reference-source/elements-of-style-1918/*.md` during ordinary use.
Read only the relevant chapter file when a shorter reference leaves an unresolved
question about an exception, rationale, or original example. Use
`assets/authority/source-map.yaml` to locate the chapter file and heading. Each
`source_sections` entry is formatted as `<chapter-file>: <heading>`. The historical
source is context and provenance, not current style authority.
```

Update `assets/authority/source-map.yaml` so the first-party reference files map to the new chapter files and headings. The existing reference list and `load_when` values stay the same. Update `source_sections` to entries like:

```yaml
  - path: references/sentence-mechanics.md
    source_sections:
      - elementary-rules-of-usage.md: II. Elementary Rules Of Usage
    content_mode: licensed_adaptation
    load_when:
      - Use when correcting sentence-level mechanics.
```

Map all existing references to the correct chapter file and heading. If the exact heading in the source differs, match the source heading verbatim.

Update `CITATIONS.md` to record the new source format, the public-domain URL, and the chapter file list.

Recompute the SHA-256 of the upstream `.txt` source and use it for the `content_sha256` in `authority.yaml` and the `reconciled_against` values in `authority.yaml` and `source-map.yaml`. Use:

```powershell
# PowerShell
Get-FileHash -Path sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918/elements-of-style-1918.txt -Algorithm SHA256
```

or:

```bash
sha256sum sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918/elements-of-style-1918.txt
```

- [x] Update `SKILL.md`.
- [x] Update `source-map.yaml`.
- [x] Update `CITATIONS.md` and recompute hashes.
- [x] Mark completed.

---

### Task 8: Regenerate marketplace

**Files:**
- Generated: all `codex-marketplace/plugins/...` and `.agents/plugins/...` surfaces

- [x] Run `tools/run marketplace --apply`.
- [x] Inspect `git status` to confirm the regenerated surfaces include the new `scope-notes.md`, chapter files, and `SKILL.md` projections.
- [x] Mark completed.

---

### Task 9: Commit and run CI

- [x] Stage all source and generated changes.
- [x] Commit. Allow the pre-commit hook to run `tools/run ci --check` on the staged tree. If the hook is not present, commit with `--no-verify` and then run `tools/run ci --check`.
- [x] If `ci --check` fails, fix the root cause and re-run.
- [x] Mark completed.

---

### Task 10: Push and open a PR

- [x] Push the branch `feature/handoff-gates-dependency-order` to origin.
- [x] Open a PR using `gh pr create` with the repo's PR template.
- [x] Mark completed.

---

## Amendments and out-of-scope work

The review pass added the following work that was not in the original plan:

- `refreshing-installed-skills` and `repo-standards`: clarified that `localSkills` come from `repo.local_skill_prefixes`, kept `mark-*` as the repo-default local-skill prefix, and fixed `scaffold_marketplace_json.py` to treat an explicit empty `local_skill_prefixes` as valid.
- `subagent-driven-development` overlay: genericized the implementer commit/validate step, re-dispatched stuck implementers to `implementer-strong`, and removed leftover `[MODEL]` placeholders from review prompts.
- Canonical guides: added cross-repo consumer checks to the design, planning, implementation, and code-review guides so future agents consider sister repos that install vendored skills.
- Generated `skill.zip` files and plugin projections updated as a side effect of `tools/run marketplace --apply`; no hand-editing occurred.
