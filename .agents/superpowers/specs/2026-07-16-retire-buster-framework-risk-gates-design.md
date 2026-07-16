# Retire Buster Framework, Consolidate Gates into risk-gates

**Date:** 2026-07-16
**Status:** Draft
**Branch:** `harleydbartles/retire-buster-framework-risk-gates`

## Problem

The buster framework has proliferated into 12+ thin first-party skills that are
either gates (pre-action risk checks), planning lenses, or artifact generators.
The thin-skill-per-concern model creates routing overhead, skill-count bloat,
and invites agents to invoke busters when they should be using other workflows.

Three distinct shapes were conflated under the "buster" name:

1. **Pre-action risk gates** — fire before a mutation, dispatch, canon claim,
   or resolution; return green/amber/red/blocked.
2. **Planning/reasoning lenses** — apply a thinking frame to a plan or route.
3. **Artifact generators** — produce a structured handoff export.

## Decision

Retire the buster framework and reorganize:

- **Retire outright:** `crew`, `crew-buster`, `boring-buster`, `boring-loop`,
  `session-buster`, `session-buster-ingress`. These are planning lenses,
  work-loop coordinators, or artifact generators whose function is either no
  longer needed or already better-homed in other skills:
  - `boring-buster` readiness judging → `verification-before-completion`
  - `boring-loop` work-loop coordination, false-green prevention, queue
    grooming → `verification-before-completion` (evidence-before-assertions,
    false-green checks) and `repo-worker-base` (worker coordination surface)
  - `crew`/`crew-buster` Crew thinking roles → retired; no skill absorbs this
  - `session-buster`/`session-buster-ingress` continuity exports → retired;
    agents handle handoffs on request; Linear/GitHub are durable surfaces
- **Consolidate gates into a new `risk-gates` skill:** `buster-framework`,
  `ambiguity-buster`, `canon-buster`, `invariant-buster`, `analogy-buster`,
  and the Rooms-specific gate overlays (`rooms-ambiguity-buster`,
  `rooms-analogy-buster`, `rooms-canon-buster`, `rooms-zoom-outs-buster`)
  become references under one skill with a tight router SKILL.md.

## Design

### New skill: `risk-gates`

**Location:** `sources/first_party/skills/risk-gates/`

**Purpose:** A single pre-action gate skill that routes to the relevant gate
reference docs based on what action is about to happen and what project context
is active. The SKILL.md is a decision router — it tells the agent which gates
to read and when, so the agent never reads or applies irrelevant gates.

#### SKILL.md structure

The SKILL.md carries:

1. **Frontmatter** — name, description, metadata per first-party skill format.
2. **Purpose and owned decision** — the green/amber/red/blocked contract,
   inherited from buster-framework. This is the gate mechanics: modes
   (internal, interactive, blocked), queue contract, output-surface boundary.
3. **Gate routing table** — the core router. Each gate has an inline entry with:
   - **Gate name**
   - **Use when** — the specific action/context that triggers this gate
   - **Do not use when** — when this gate is irrelevant, so the agent skips it
   - **Reference path** — `references/gates/<gate>.md` or
     `references/rooms/<gate>.md`
4. **Project overlay routing** — how to determine whether project-specific gates
   apply (currently only Rooms).
5. **Workflow** — name the action, identify material gates from the routing
   table, read only those reference docs, apply, return verdict.
6. **Boundaries** — do not use gates as broad planning; do not create permission
   the user/source/policy has not granted; do not import project-specific law
   into generic gate references.

#### Gate routing table (inline in SKILL.md)

Each entry is concise enough that the agent can decide whether to read the
reference without opening it:

**Generic gates** (apply in any project):

| Gate | Use when | Do not use when | Reference |
|------|----------|-----------------|-----------|
| ambiguity-gate | An action or answer depends on interpreting an ambiguous term, scope, target, source, authority, output shape, time reference, or vocabulary item, and guessing wrong would cause the wrong scope, target, route, artifact, or answer. | The ambiguity is harmless, already resolved by durable source, or does not affect the immediate safe next step. | `references/gates/ambiguity-gate.md` |
| canon-gate | About to make, change, summarize, publish, dispatch, or rely on a durable canon/truth claim — project doctrine, world state, character facts, source-of-truth records, schemas, accepted decisions, or policy. | The claim is not canon-facing (ordinary conversation, non-durable working notes, or a claim with no truth-surface consequences). | `references/gates/canon-gate.md` |
| invariant-gate | About to take an action, answer, plan, dispatch, or durable mutation where binding constraints (authority, scope, source hierarchy, workflow law, data/schema, provenance/license, canon/doctrine, safety/privacy) may be violated. | No binding invariants are implicated — the action is ordinary, unconstrained, and has no protected surfaces or required workflow steps. | `references/gates/invariant-gate.md` |
| analogy-gate | About to rely on an analogy, metaphor, comparison, role model, frame, or project-specific shorthand to answer, plan, dispatch, or make a durable decision. | No analogy is doing evidentiary or decision work — the reasoning is source-grounded without metaphorical scaffolding. | `references/gates/analogy-gate.md` |

**Rooms project gates** (apply only when working in Rooms, Mostly):

| Gate | Use when | Do not use when | Reference |
|------|----------|-----------------|-----------|
| rooms-ambiguity-gate | Working in Rooms and the action risks resolving identity, motive, authorship, witness status, narrator knowledge, archive gaps, disappearance, or manuscript uncertainty without evidence. | Not working in Rooms, or the ambiguity is generic (use the generic ambiguity-gate instead). | `references/rooms/ambiguity-gate.md` |
| rooms-canon-gate | Working in Rooms and testing canon pressure — whether an item fits, conflicts with, exposes a gap in, or belongs to another layer than established Rooms canon. | Not working in Rooms, or the canon question is generic (use the generic canon-gate instead). | `references/rooms/canon-gate.md` |
| rooms-analogy-gate | Working in Rooms and relying on the black box theatre analogy for a canon, world, manuscript, dispatch, or persistence decision. | Not working in Rooms, or no analogy is in play, or the analogy question is generic (use the generic analogy-gate instead). | `references/rooms/analogy-gate.md` |
| rooms-zoom-outs-gate | Working in Rooms and compressing a character, room, event, or system into a behavioural/emotional/structural model that will be used for canon, persistence, or dispatch decisions. | Not working in Rooms, or no zoom-out/compression model is being constructed or relied upon. | `references/rooms/zoom-outs-gate.md` |

#### Reference file layout

```
risk-gates/
  SKILL.md
  agents/
    openai.yaml
  references/
    gates/
      ambiguity-gate.md       (from ambiguity-buster/SKILL.md body)
      canon-gate.md           (from canon-buster/SKILL.md body)
      invariant-gate.md       (from invariant-buster/SKILL.md body)
      analogy-gate.md         (from analogy-buster/SKILL.md body)
    rooms/
      ambiguity-gate.md       (from rooms-ambiguity-buster/SKILL.md body + refs)
      canon-gate.md           (from rooms-canon-buster/SKILL.md body + refs)
      analogy-gate.md         (from rooms-analogy-buster/SKILL.md body + refs)
      zoom-outs-gate.md       (from rooms-zoom-outs-buster/SKILL.md body + refs)
```

#### Content migration

Each retired skill's SKILL.md body becomes a gate reference doc. The
buster-framework mechanics (green/amber/red/blocked, modes, queue contract,
output-surface boundary) move into the risk-gates SKILL.md itself, since they
are the shared gate contract all references inherit.

For skills with existing reference files (rooms-canon-buster had
canon-buster-queue.md, canon-green-paths.md, canon-pressure-types.md;
rooms-zoom-outs-buster had artifact-verification-gate.md,
compression-validity-test.md, queue-patterns.md, zoom-out-failure-modes.md;
rooms-analogy-buster had rooms-analogy-binding.md), fold those references
into the single gate reference doc. The rooms zoom-outs gate is the one case
where sub-references may be warranted (it has four substantial reference
files); keep those as `references/rooms/zoom-outs-*.md` sub-references and
link them from the main `references/rooms/zoom-outs-gate.md`. All other
rooms gates fold their sub-references inline.

The generic gate references drain project-specific content per the existing
extraction rule: no Rooms actor names, paths, source hierarchy, or
workflow assumptions in generic gates.

### Retired skills

The following skill directories are removed from
`sources/first_party/skills/`:

| Skill | Reason |
|-------|--------|
| `buster-framework` | Mechanics absorbed into risk-gates SKILL.md |
| `ambiguity-buster` | Becomes `references/gates/ambiguity-gate.md` |
| `canon-buster` | Becomes `references/gates/canon-gate.md` |
| `invariant-buster` | Becomes `references/gates/invariant-gate.md` |
| `analogy-buster` | Becomes `references/gates/analogy-gate.md` |
| `rooms-ambiguity-buster` | Becomes `references/rooms/ambiguity-gate.md` |
| `rooms-analogy-buster` | Becomes `references/rooms/analogy-gate.md` |
| `rooms-canon-buster` | Becomes `references/rooms/canon-gate.md` |
| `rooms-zoom-outs-buster` | Becomes `references/rooms/zoom-outs-gate.md` |
| `crew` | Retired — planning lens no longer needed |
| `crew-buster` | Retired — planning lens no longer needed |
| `boring-buster` | Retired — readiness judging better homed in `verification-before-completion` |
| `boring-loop` | Retired — work-loop coordination, false-green prevention, and queue grooming better homed in `verification-before-completion` and `repo-worker-base` |
| `session-buster` | Retired — agents handle handoffs on request; durable surfaces (Linear/GitHub) are the continuity |
| `session-buster-ingress` | Retired — depends on session-buster |

### Cross-references to update

Other skills and surfaces that reference the retired buster names need updates.
The 187-file match surface breaks into categories:

**Skills with buster/boring-loop references in their SKILL.md or references:**
- `repo-worker-base/SKILL.md` and `agents/openai.yaml` — lists `boring-loop`
  as a dependency and references it in the routing list; remove the dependency
  and update the routing line. Queue discipline and next-smallest-move
  guidance that `repo-worker-base` wants to keep should be absorbed inline
  or routed to `verification-before-completion`.
- `work-mode-router/SKILL.md` — references buster-framework; update routing.
- `tps-reporting/SKILL.md` — references buster; update.
- `rooms-sheet-creator/SKILL.md` — references rooms-canon-buster; update to
  risk-gates.
- `rooms-project-doctrine/references/rooms-skill-routing.md` — references
  rooms-ambiguity-buster, rooms-analogy-buster, rooms-canon-buster,
  rooms-zoom-outs-buster; update to risk-gates rooms overlays.
- `rooms-project-doctrine/references/ambiguity-and-narration.md` — references
  rooms-ambiguity-buster; update.
- `linear-issue-shaping/SKILL.md` — references boring-buster in its routing
  examples and specialist-boundary list; update to risk-gates or
  verification-before-completion.
- `base-doctrine/references/output-artifact-shape.md` — references
  boring-buster; update.
- `house-skills/SKILL.md` — references boring-loop; update.

**Generated/projection surfaces (regenerate, do not hand-edit):**
- `generated/skill-zips/registry.json`
- `sources/first_party/skills/INDEX.md`
- `codex-marketplace/plugins/house-skills/skills/INDEX.md`
- `codex-marketplace/plugins/rooms-project-pack/skills/INDEX.md`
- `codex-marketplace/plugins/house-skills/references/source-map.md`
- `codex-marketplace/plugins/rooms-project-pack/references/source-map.md`
- `codex-marketplace/plugins/house-skills/references/provenance-map.json`
- `codex-marketplace/plugins/rooms-project-pack/references/provenance-map.json`
- `codex-marketplace/plugins/house-skills/references/bundle-manifest.json`
- `codex-marketplace/plugins/rooms-project-pack/references/bundle-manifest.json`
- `codex-marketplace/plugins/house-skills/README.md`

**House-skills metadata (update to reflect retirement):**
- `sources/first_party/skills/house-skills/intake.json`
- `sources/first_party/skills/house-skills/decisions.json`
- `sources/first_party/skills/house-skills/decisions.md`

**Provenance (update to record retirement):**
- `provenance/first-party-skills.md`
- `provenance/house-skills.md`

**Marketplace plugin copies (regenerate from source):**
- All `codex-marketplace/plugins/house-skills/skills/<retired-skill>/`
  directories.
- All `codex-marketplace/plugins/rooms-project-pack/skills/<retired-skill>/`
  directories.
- New `codex-marketplace/plugins/*/skills/risk-gates/` projections.

### Regeneration

After source changes, run marketplace rebuild and skill installation:

```bash
py -3 tools/rebuild_marketplace.py
py -3 tools/install_agent_skills.py
```

This regenerates INDEX.md files, provenance maps, bundle manifests, registry,
and installed skills in `.agents/skills/`.

### Provenance

Record the retirement in `provenance/first-party-skills.md`:
- Mark retired skills as `status: retired` with retirement date and reason.
- Add `risk-gates` as a new active skill with provenance noting it consolidates
  the gate busters.

## Scope boundaries

**In scope:**
- Create `risk-gates` skill with router SKILL.md and gate reference docs.
- Remove 15 retired skill directories from `sources/first_party/skills/`.
- Update cross-references in other source skills (including `repo-worker-base`
  dependency removal and `linear-issue-shaping` routing updates).
- Update provenance records.
- Regenerate marketplace projections and installed skills.

**Out of scope:**
- Redesigning `work-mode-router`, `verification-before-completion`, or other
  skills beyond updating their buster/boring-loop references and absorbing
  explicitly mapped content (false-green prevention →
  verification-before-completion, queue discipline → repo-worker-base).
- Changing the `brainstorming` skill (it was not modified; the original
  proposal to make busters into brainstorming profiles was superseded by the
  gate-skill approach).
- Retiring any skills other than the 15 listed.
- Changing the first-party skill source format or metadata schema.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Agents that learned to invoke specific buster names (e.g. `ambiguity-buster`) will find them gone. | The `risk-gates` description and routing table cover the same trigger surface. Provenance records the rename so agents can discover the migration. |
| Rooms-specific gate content in the same skill as generic gates violates the old "do not import project law" doctrine. | File-level namespacing (`references/gates/` vs `references/rooms/`) keeps the separation. The SKILL.md router explicitly gates Rooms references behind "working in Rooms" condition. |
| 187-file reference surface means high blast radius. | Generated surfaces are regenerated, not hand-edited. Source-level cross-references are updated skill-by-skill. Provenance records the retirement for traceability. |
| `crew` doctrine is referenced by `crew-buster` and possibly other surfaces. | Verify no other skill depends on `crew` doctrine before removing. The crew-lenses.md reference is already a compatibility pointer, suggesting the dependency surface is small. |
| `boring-loop` is wired into `repo-worker-base` as a dependency and into the `repo-worker-pack` plugin. Retiring it breaks that wiring. | Update `repo-worker-base` SKILL.md and openai.yaml to remove the dependency. Absorb minimal queue-discipline guidance inline or route to `verification-before-completion`. Regenerate `repo-worker-pack` plugin projection. |
| `boring-loop` is also referenced in tooling (`validate_export_skill_zips.py`, `generate_repo_index.py`) and `custody-pack-registry.json`. | Update tooling references during regeneration. The custody-pack-registry is regenerated by the marketplace rebuild. |
