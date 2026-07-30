# Scope Notes Convention and Writing-With-Clarity Source-Reference Cleanup

## Goal

Make first-party skill boundaries actionable and document the pattern, while converting the `writing-with-clarity` historical source from an HTML context killer into agent-consumable chapter Markdown.

## Scope

1. `handoff-gates`
2. `working-with-epics`
3. `docs/skill-standards-policy.md`
4. `writing-with-clarity`

## Non-goals

- No implementation code.
- No skill-zip or `generated/skill-zips/` work.
- No broad audit of other `assets/authority/reference-source/` files.
- No changes to `skill-frontmatter.md` schema.

## Contract

### `handoff-gates`

Edit `sources/first_party/skills/handoff-gates/SKILL.md`:
- Add **Dependency-order coherence** as the first item in the `Plan-Readiness Checklist`.
- Reframe the existing **Task ordering** item as the repo-specific application of that rule.
- Add a `## Boundary cases` section at the bottom that loads `references/scope-notes.md` for thin specs, external blockers, or verification/review overlap.

Edit `sources/first_party/skills/handoff-gates/references/scope-notes.md`:
- Replace the stub with a real reference covering the three boundary cases.

Edit `sources/first_party/skills/handoff-gates/assets/authority/source-map.yaml`:
- Add `references/scope-notes.md` with `load_when` for the three boundary cases.

Edit the `do_not_use_when` frontmatter in `SKILL.md`:
- Add a scope-notes pointer to the "not clearly at a stage boundary" item.

### `working-with-epics`

Edit `sources/first_party/skills/working-with-epics/SKILL.md`:
- Add a `## Boundary cases` section that loads `references/scope-notes.md` for epic splitting, multi-plan scope changes, and human-vs-risk-gates escalation.

Edit `sources/first_party/skills/working-with-epics/references/scope-notes.md`:
- Replace the stub with real guidance on the three cases.

Edit `sources/first_party/skills/working-with-epics/assets/authority/source-map.yaml`:
- Add `references/scope-notes.md` with matching `load_when` conditions.

Edit the `do_not_use_when` frontmatter in `SKILL.md`:
- Add a scope-notes pointer to any item that benefits from expansion.

### `docs/skill-standards-policy.md`

Add a **Scope notes convention** section:
- When a first-party skill has real but non-primary boundary cases, create `references/scope-notes.md`.
- Do not create empty stubs.
- Wire it through `do_not_use_when` frontmatter, a `## Boundary cases` or `## When this skill isn't what you need` body call-out, and `assets/authority/source-map.yaml` if the skill has one.

### `writing-with-clarity`

Source a public-domain `Elements of Style` text (Project Gutenberg or equivalent).

Remove `sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918.html`.

Create `sources/first_party/skills/writing-with-clarity/assets/authority/reference-source/elements-of-style-1918/<chapter>.md`, one file per chapter, using the chapter titles as file names.

Update `sources/first_party/skills/writing-with-clarity/assets/authority/source-map.yaml`:
- Map each topical rule to the relevant chapter file/heading.

Update `sources/first_party/skills/writing-with-clarity/assets/authority/CITATIONS.md`:
- Record the new source and its public-domain status.

Update `sources/first_party/skills/writing-with-clarity/SKILL.md`:
- Replace the "do not read the HTML" instruction with a pointer to the chapter files and the source-map.

## Design

### Scope notes pattern

The main `SKILL.md` body keeps the primary lane. Boundary cases move to `references/scope-notes.md`. The body calls the reference explicitly so an agent only loads it when a boundary case matches. `do_not_use_when` frontmatter items can end with a parenthetical pointer to the same reference.

`assets/authority/source-map.yaml` lists `references/scope-notes.md` with `load_when` conditions that mirror the body call-out, keeping the authority record and the skill body in sync.

### Source-backed reference conversion

`writing-with-clarity` already treats the `Elements of Style` as a historical source, not the active style authority. The change is only the file format and granularity. One chapter per file keeps each bounded load small. `source-map.yaml` maps a topical reference to the right chapter file and heading.

## Validation

- `tools/run marketplace --apply`
- `tools/run ci --check`

## Deferred

- Audit and convert other `assets/authority/reference-source/` files.
- Backfill scope notes for additional first-party skills beyond `handoff-gates` and `working-with-epics`.
