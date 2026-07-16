# MARK-334: Rooms-* skills full cleanup design

## Problem

The rooms-* skills carry retired named-agent bindings (Chris, Albert, Brian, Derek, Will, Harley) that encode routing, ownership, authority, and simulation rules. A broader audit also found version suffix inconsistencies, broken frontmatter descriptions, generic do_not_use_when triggers, and word count overages.

## Scope

All 10 rooms-* skills under `sources/first_party/skills/rooms-*/`:
- rooms-ambiguity-buster
- rooms-analogy-buster
- rooms-bootstrap
- rooms-canon-buster
- rooms-character-investigation
- rooms-image-sidecars
- rooms-project-doctrine
- rooms-sheet-creator
- rooms-source-partitioning
- rooms-zoom-outs-buster

Plus their `references/` files and the `docs/skill-standards-policy.md` update for the human-operator naming standard.

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

Trim to under 500 words (body excluding frontmatter):
- `rooms-bootstrap` (~550 → <500): Move domain reminder details to a new `references/domain-reminders.md` file.
- `rooms-canon-buster` (~600 → <500): Move detailed canon-check steps to a new `references/canon-check-steps.md` file.
- `rooms-character-investigation` (~550 → <500): Move source-routing details to existing `references/source-routing.md` file.
- `rooms-zoom-outs-buster` (~550 → <500): Move failure mode details to existing `references/zoom-out-failure-modes.md` file.

### 7. Skill-standards-policy update

Add "Referring to the human operator" section to `docs/skill-standards-policy.md`:
- Use "your human partner" when referring to the person the agent is working with.
- Do not use "user", "Harley", or other named individuals.
- Keeps skills portable across operators.

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
