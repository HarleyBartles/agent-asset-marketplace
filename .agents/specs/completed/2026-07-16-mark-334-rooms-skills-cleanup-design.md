# MARK-334: Rooms-* skills full cleanup design

## Problem

The rooms-* skills carry retired named-agent bindings (Chris, Albert, Brian, Derek, Will, Harley) that encode routing, ownership, authority, and simulation rules. A broader audit also found version suffix inconsistencies, broken frontmatter descriptions, generic do_not_use_when triggers, and word count overages.

## Scope

10 rooms-* skills under `sources/first_party/skills/rooms-*/`, merging to 8:
- rooms-ambiguity-buster
- rooms-analogy-buster
- rooms-bootstrap → **merged into rooms-project-doctrine**
- rooms-canon-buster
- rooms-character-investigation
- rooms-image-sidecars
- rooms-project-doctrine (absorbs bootstrap + source-partitioning)
- rooms-sheet-creator
- rooms-source-partitioning → **merged into rooms-project-doctrine**
- rooms-zoom-outs-buster

Plus their `references/` files and the `.agents/doctrine/skill-standards-policy.md` update for the human-operator naming standard.

## Changes

### 1. Named-agent → domain concept replacements

| Current | Replacement | Rationale |
|---|---|---|
| Albert/Pit | Pit/archive | Archive evidence domain |
| Brian/World | World/canon | Canon/world state domain |
| Derek/Manuscript | Manuscript/prose | Prose drafting domain |
| Chris | project-local governance | Project-local scope |
| Will | workspace governance | Workspace-level scope |
| Harley | your human partner | Human operator (per skill-standards-policy) |

Simulation boundaries: "Do not simulate Chris, Albert, Brian, Derek, or Will" → "Do not simulate archive, canon, manuscript, project-local, or workspace governance lanes."

Applies to all SKILL.md files and all reference files under rooms-* skills.

### 2. Version suffix cleanup

Remove all version suffixes from cross-references:
- `rooms-bootstrap-v1.1` → `rooms-bootstrap`
- `rooms-project-doctrine-v1` → `rooms-project-doctrine`
- `rooms-source-partitioning-v1` → `rooms-source-partitioning`
- `rooms-canon-buster-v1` → `rooms-canon-buster`
- `rooms-ambiguity-buster-v1` → `rooms-ambiguity-buster`
- `rooms-analogy-buster-v1` → `rooms-analogy-buster`
- `rooms-zoom-outs-buster-v1` → `rooms-zoom-outs-buster`
- `rooms-character-investigation-v1` → `rooms-character-investigation`
- `rooms-sheet-creator-v1` → `rooms-sheet-creator`
- `rooms-image-sidecars-v0.1` → `rooms-image-sidecars`
- `base-doctrine-v1.1` → `base-doctrine`
- `linear-issue-shaping-v1` → `linear-issue-shaping`
- `tps-reporting-v1` → `tps-reporting`
- `tps-ingress-v1` → `tps-ingress`
- `work-mode-router-v1` → `work-mode-router`

Affects `rooms-project-doctrine/references/rooms-skill-routing.md` and composition sections across most skills.

### 3. External repo path references

Add a note at the top of `rooms-character-investigation/references/source-routing.md` and `rooms-sheet-creator/references/direct-landing.md` clarifying that `rooms-world/`, `rooms-pit/`, `rooms-manuscript/` are external repo paths in the Rooms-mostly ecosystem, not paths in this marketplace repo. Do not remove them — they're domain guidance for when the skills are used in the Rooms context.

### 4. Frontmatter description fixes

- `rooms-ambiguity-buster`: "Use when preserve..." → "Use when preserving rooms ambiguity for identity, motive, authorship, archive gaps, narration, and disappearance."
- `rooms-analogy-buster`: Fix to "Use when validating rooms-specific interpretive analogies against the black box theatre analogy before binding them to world canon."
- `rooms-bootstrap`: Shorten to focus on triggering conditions.
- `rooms-image-sidecars`: Shorten to focus on triggering conditions.

### 5. Specific do_not_use_when triggers

Replace generic "Do not use when another more specific skill owns this task." with specific exclusions per skill. Examples:
- rooms-ambiguity-buster: "Do not use when the task is canon resolution rather than ambiguity detection — use rooms-canon-buster instead."
- rooms-analogy-buster: "Do not use when the task is canon validation rather than analogy validation — use rooms-canon-buster instead."
- rooms-sheet-creator: "Do not use when the task is character investigation rather than sheet creation — use rooms-character-investigation instead."

### 6. Word count trimming

Only 3 skills exceed 500 words (body excluding frontmatter):
- `rooms-canon-buster` (561 → <500): Move detailed canon-check steps to a new `references/canon-check-steps.md` file.
- `rooms-character-investigation` (523 → <500): Move source-routing details to existing `references/source-routing.md` file.
- `rooms-image-sidecars` (501 → <500): Trim verbose description and move DB companion details to existing `references/db_mutation_proposal_csvs.md`.

### What stays unchanged

- Skill names, directory names, frontmatter `name` fields
- `owner: Harley Bartles` in frontmatter metadata (identity field, not agent binding)
- `version-history.md` files (historical provenance records, not current cross-references)
- Plugin membership, bundle manifests
- The actual domain guidance content — only the agent-name wrapping changes

### 7. Skill-standards-policy update

Add "Referring to the human operator" section to `.agents/doctrine/skill-standards-policy.md`:
- Use "your human partner" when referring to the person the agent is working with.
- Do not use "user", "Harley", or other named individuals.
- Keeps skills portable across operators.

Add ordering and composition trigger fields to the metadata standard:
- `use_before` — ordering: this skill should fire before the listed skills (produces an artifact they consume).
- `use_after` — ordering: this skill should fire after the listed skills (consumes an artifact they produce).
- `use_with` — composition: these skills should run alongside this skill in the same turn.
- `use_instead` — routing: prefer the listed skills for specific sub-tasks where they are better suited. Pair with `do_not_use_when` entries explaining the specific cases.

### 8. Trigger field updates on rooms-* skills

Apply the new trigger vocabulary to rooms-* skills:

- `rooms-character-investigation`: add `use_before: [rooms-sheet-creator]`
- `rooms-sheet-creator`: add `use_after: [rooms-character-investigation]`
- `rooms-canon-buster`: add `use_with: [rooms-project-doctrine]` (after merge, source-partitioning is a reference doc within project-doctrine)
- `rooms-ambiguity-buster`: add `use_instead: [rooms-canon-buster]` for canon resolution tasks
- `rooms-analogy-buster`: add `use_instead: [rooms-canon-buster]` for canon validation tasks
- Other skills: add `use_with` / `use_instead` where the audit found "compose with" or routing relationships in the body text.

### 9. Skill merge: bootstrap + project-doctrine + source-partitioning → rooms-project-doctrine

Merge three orientation skills into one `rooms-project-doctrine` skill:

**Rationale:**
- Project-doctrine at 162 words is almost entirely a router to references.
- Bootstrap already routes to project-doctrine, which routes to source-partitioning — a chain of "load this next" that can be one entry point.
- Source-partitioning is referenced as a composition partner by other skills, but always as "use source-partitioning when evidence classes mix," which works equally well as a reference doc.

**Structure:**
- Skill body: compact router (under 500 words) covering first-turn arrival, doctrine lookup, and source-basis labeling.
- `references/bootstrap-posture.md`: first-turn arrival and request classification (from rooms-bootstrap body).
- `references/source-partitioning.md`: source-basis labeling rules (from rooms-source-partitioning body).
- Existing references from rooms-project-doctrine and rooms-bootstrap remain.

**Retired skills:**
- `rooms-bootstrap` — content absorbed into merged skill and `references/bootstrap-posture.md`.
- `rooms-source-partitioning` — content absorbed into `references/source-partitioning.md`.
- Their `version-history.md` files move to the merged skill's references as historical provenance.

**Cross-reference updates:**
- All skills that reference `rooms-bootstrap` → `rooms-project-doctrine`.
- All skills that reference `rooms-source-partitioning` → `rooms-project-doctrine` (or `references/source-partitioning.md` for direct source-basis guidance).
- `rooms-project-doctrine/references/rooms-skill-routing.md` updated to remove the two merged entries.

## What stays unchanged

- Skill names, directory names, frontmatter `name` fields
- Metadata identity fields (source-id, source-path, etc.)
- Plugin membership, bundle manifests
- The actual domain guidance content — only the agent-name wrapping changes

## Validation

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 -m pytest tests/ -x`
- Case-sensitive search proving no retired named-agent bindings remain in rooms-* source/projection set
