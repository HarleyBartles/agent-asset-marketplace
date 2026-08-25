# MARK-371 writing pack and prose-fatigue design

**Status:** Approved design
**Control plane:** Linear issue MARK-371
**Date:** 2026-08-25

## Problem

The marketplace has useful writing capabilities, but their package boundaries
do not match their product responsibilities.

- `writing-with-clarity` is a general human-writing skill stranded in
  `repo-worker-pack`, despite not being repo-worker-specific.
- `unslop-profiles` exists under both `unslop-plus` and `repo-worker-pack`.
  The profile contents currently agree, but both plugin manifests claim their
  own source tree as canonical. That is duplicate source custody, not a
  generated install mirror.
- The current writing profile is a short phrase-oriented anti-slop checklist.
  It does not preserve the research, evidence strength, counterarguments,
  drift metadata, or preserve-versus-repair cases required by MARK-371.
- The existing `unslop-engine` discovers repeated patterns and generates a
  draft Markdown profile. It does not load and evaluate prose against an
  existing profile. Its text analysis also begins from a hard-coded phrase
  list, so it cannot be treated as the writing system required by MARK-371.
- Avoiding familiar AI prose patterns is not sufficient writing guidance.
  Anti-fatigue repair can make prose less clear, less accurate, or less like
  its author unless clarity and factual preservation remain explicit gates.

The marketplace needs a first-class writing product whose package boundary,
skill composition, evidence, and executable checks all support clear authored
prose. It also needs to preserve `unslop-plus` as the generic home for the
cross-domain engine and profiles that do not belong to the writing product.

## Goals

1. Create a `writing-pack` Codex plugin for general human-facing writing.
2. Make `writing-with-clarity` a first-class writing skill rather than a
   repo-worker-owned helper.
3. Add a compositional writing entrypoint that keeps clarity, author voice,
   and anti-fatigue review in a defined order.
4. Add a writing-style skill that separates stable positive voice guidance
   from time-sensitive reader-fatigue guidance.
5. Preserve the MARK-371 research as source-backed, inspectable profile
   material without loading the full evidence corpus during ordinary use.
6. Give the writing pack a purpose-built profile engine whose scope is the
   writing profiles and references shipped in the same plugin.
7. Keep `unslop-plus` as the coherent generic home for `unslop-engine` and
   `unslop-profiles`.
8. Remove duplicate custody from `repo-worker-pack` while preserving the
   capabilities this repository installs for its own workers.

## Non-goals

- Do not turn the writing pack into an AI detector or detector-evasion tool.
- Do not deliberately inject errors, randomness, choppiness, or other defects
  to make prose appear human.
- Do not ban em dashes, rhetorical questions, groups of three, contrast,
  `real`, or another device merely because models also use it.
- Do not move the generic `unslop-profiles` library into `writing-pack`.
- Do not make the writing pack responsible for the current generic text and
  visual `unslop-engine`.
- Do not require one marketplace-wide unslop engine or one canonical profile
  location across unrelated domains.
- Do not ship a private author corpus or a Harley-specific voice profile.
- Do not turn the design spec into a permanent research dump. Durable research
  belongs with the writing-style profile that interprets it.
- Do not preserve duplicate plugin source trees as a compatibility mechanism.

## Product boundaries

### `unslop-plus`

`unslop-plus` remains an installable generic anti-slop toolkit containing:

- `unslop-engine`: generic pattern discovery and draft profile generation,
  including its existing cross-domain and visual scope.
- `unslop-profiles`: generic profiles that can apply broadly across software
  work, including architecture, testing, debugging, security review, UI,
  cleanup custody, and other non-writing domains.

This plugin pays rent because its engine and profile router share a generic,
cross-domain purpose. MARK-371 may repair proven internal documentation drift
encountered during migration, but it must not redesign the generic engine to
serve writing-pack requirements.

### `writing-pack`

`writing-pack` is the first-class marketplace home for composed human-facing
writing capability. Generic profiles elsewhere may still apply to writing,
but they do not own this product's composition or source custody. Its initial
skills are:

1. `writing`
2. `writing-with-clarity`
3. `writing-style`
4. `writing-profile-engine`

The plugin name is `writing-pack`, not `language-pack`; the marketplace already
uses `language-patterns-pack` for Python and TypeScript guidance.

### `repo-worker-pack`

`repo-worker-pack` returns to repo-worker workflow, hygiene, source-custody,
validation, and publication responsibilities. A repo worker may consume
writing and generic anti-slop capabilities, but that does not make their source
trees repo-worker assets.

`repo-worker-pack` therefore stops bundling source copies of:

- `writing-with-clarity`
- `unslop-profiles`

## Writing-pack skill architecture

### `writing`

`writing` is the normal compositional entrypoint for drafting, revising, or
reviewing prose intended for human readers. It does not duplicate detailed
craft or style guidance. It routes work through the specialist skills in this
order:

1. Establish the requested artifact, audience, intent, verified facts,
   constraints, and applicable project or editorial style.
2. Draft or revise through `writing-with-clarity`.
3. Apply an authorised positive author-voice profile when one is available.
4. Apply the relevant anti-fatigue profile as an adversarial review.
5. Return through the `writing-with-clarity` final-edit gate to verify that the
   repair preserved meaning, qualification, tone, and readability.

The entrypoint must use bounded reference loading. It should not load the full
research ledger, every writing reference, or every profile for an ordinary
draft.

### `writing-with-clarity`

`writing-with-clarity` moves from `repo-worker-pack` to `writing-pack` with its
existing authority assets and reference structure preserved. It remains
authoritative for:

- meaning and factual fidelity;
- document and paragraph flow;
- directness, specificity, and concision;
- sentence mechanics and word choice;
- necessary uncertainty and qualification;
- accessibility and human-readable formatting;
- the final readability review.

The move should use `git mv` so history and custody remain inspectable. Content
changes in the migration commit must be limited to the composition contract,
source paths, and references made inaccurate by the new plugin boundary.

### `writing-style`

`writing-style` owns two explicitly separate profile families:

- **Voice profiles** are positive and relatively stable. They describe an
  authorised author's argument shape, qualification, humour, vocabulary,
  contractions, rhythm, directness, examples, and tolerated roughness.
- **Fatigue profiles** are dated and evidence-backed. They identify
  overexposed model habits, density, predictability, low-information emphasis,
  reader disengagement, false positives, and repair principles.

Voice profiles say what to preserve or pursue. Fatigue profiles say what to
challenge. The skill must not collapse either family into a list of forbidden
tokens.

The first fatigue profile is `ai-prose-fatigue`. It covers at least the pattern
families required by MARK-371:

1. low-information affirmation and significance boosters;
2. synthetic profundity through repeated contrast;
3. manufactured conversationality;
4. editorial throat-clearing;
5. predictable cadence and structural regularity;
6. synthetic affect and positivity;
7. semantic emptiness under polished prose;
8. genericity that overrides an identified author's voice.

### `writing-profile-engine`

`writing-profile-engine` is a writing-specific maintenance and evaluation
tool. It is not a fork that must remain compatible with the generic
`unslop-engine`, and it does not establish a marketplace-wide engine standard.

Its bounded responsibilities are:

- discover candidate lexical, structural, cadence, and density patterns in a
  prose sample corpus;
- evaluate prose or a corpus against a selected writing profile;
- validate profile structure, evidence links, review dates, false-positive
  guidance, and golden coverage;
- scaffold a reviewed candidate into the writing profile contract;
- distinguish deterministic observations from contextual judgements;
- produce typed, inspectable findings rather than an authorship score.

It does not analyse visual design, generate arbitrary software-engineering
profiles, own the profiles it consumes, decide whether text was written by a
human, or rewrite prose without the clarity and factual-preservation gates.

## Authority and conflict handling

The writing workflow uses this authority order:

1. Verified facts, explicit user intent, legal and safety requirements, and
   accessibility needs
2. Explicit project or editorial style
3. An authorised author-voice profile
4. General clarity defaults
5. Reader-fatigue heuristics

`writing-with-clarity` also runs as the final gate. This does not require a
uniform style: a fragment, unusual rhythm, technical term, or rhetorical
device may survive when it is intentional, accurate, comprehensible, and
appropriate. A fatigue finding cannot silently remove a qualification,
strengthen a claim, flatten an author's voice, or make the prose harder to
understand.

When two instructions cannot be reconciled, the workflow must preserve the
higher-authority requirement and report the unresolved lower-authority style
finding rather than forcing a rewrite.

## Lawful skill layout

Supporting material under a skill must be rooted in the canonical
`references/`, `assets/`, or `scripts/` directories. A top-level `profiles/`
folder under a skill is not permitted.

The writing-style source shape is:

```text
codex-marketplace/plugins/writing-pack/skills/writing-style/
  SKILL.md
  agents/
    openai.yaml
  references/
    profile-contract.md
    profiles/
      fatigue/
        ai-prose-fatigue/
          profile.md
          patterns.json
          goldens.json
          sources.md
      voice/
        author-voice-template.md
        custody-and-derivation.md
```

The nesting pays rent by keeping the stable voice and changing fatigue
families separate, while keeping each fatigue profile's operational guidance,
structured patterns, golden cases, and research together.

The engine source shape is:

```text
codex-marketplace/plugins/writing-pack/skills/writing-profile-engine/
  SKILL.md
  agents/
    openai.yaml
  references/
    evaluation-contract.md
  assets/
    schemas/
      writing-profile.schema.json
  scripts/
    discover_profiles.py
    evaluate_profile.py
    validate_profiles.py
```

The engine owns its executable schema and tooling. `writing-style` owns the
profiles. Engine scripts may consume structured profile files under
`writing-style/references/profiles/` without relocating or claiming custody
over them.

## Profile and evidence contract

Each fatigue profile package contains four complementary artifacts:

- `profile.md`: terse agent-facing operational guidance;
- `patterns.json`: machine-readable pattern records;
- `goldens.json`: preserve, repair, and abstention cases;
- `sources.md`: readable research, citations, methodology, limitations, and
  counterarguments.

The operational profile must remain useful when loaded alone. It links to the
deeper evidence package but does not inline the entire research record.

Each retained pattern record includes:

- a stable pattern ID and family;
- a description of the defect rather than only a token;
- observable signals and density considerations;
- evidence state;
- source IDs;
- first-observed and last-reviewed dates;
- model, platform, community, or genre scope when supported;
- false positives and legitimate uses;
- a repair principle;
- linked preserve, repair, and boundary cases.

Allowed evidence states are:

- `well_supported_reader_fatigue`
- `plausible_emerging`
- `author_specific_preference`
- `weak_or_folk_heuristic`

Evidence strength is separate from lifecycle status. Pattern status is one of
`active`, `retired`, or `rejected`. Only active patterns appear in the ordinary
runtime profile. Retired and rejected records remain in the evidence package
so future maintainers can see what was considered and why it is inactive.

`real` is modelled as a possible signal within the
`low_information_affirmation` family. It is not a prohibited token. A precise
distinction between real and simulated, hypothetical, apparent, or bogus
states is a preserve case.

## Golden cases and evaluation results

Every active fatigue pattern requires:

- at least one `repair` case;
- at least one `preserve` case;
- at least one `abstain` or boundary case when context materially affects the
  decision.

Golden cases include the input, expected classification, applicable pattern
IDs, rationale, and an expected repair principle where relevant. They test the
decision boundary, not only whether a phrase appears.

Engine evaluation returns typed results:

- `observed`: a deterministic signal was found;
- `candidate`: contextual review is required;
- `preserve`: a legitimate use matched or was confirmed;
- `repair`: the profile supports changing the prose;
- `abstain`: the available evidence does not support a decision.

Schema errors, broken source links, stale required review metadata, and missing
golden coverage may fail validation. A phrase match alone cannot fail prose or
justify a repair.

## Author-voice custody

The marketplace plugin ships a profile contract, safe template, synthetic
examples, and derivation guidance. It does not ship a real person's private
source corpus.

Voice-profile derivation must record:

- who authorised the source material;
- the permitted storage and distribution boundary;
- whether source excerpts may be retained;
- the genres and audiences represented;
- the limits of the inferred profile;
- the date and sample set used for review.

A private profile may be consumed from an explicitly supplied external path.
The writing engine must not copy the source corpus into generated output,
logs, fixtures, or the repository. Public availability alone does not grant
permission to create a marketplace-distributed author imitation profile.

## Research and drift strategy

Implementation begins by verifying and deepening the issue's existing source
base. It must include:

- direct reader and editorial evidence;
- original scholarly or peer-reviewed work where available;
- counterarguments showing that alleged AI tells are often legitimate human
  rhetoric;
- source and population limitations;
- model, platform, genre, and date scope;
- primary WikiProject or editorial guidance rather than only summaries;
- evidence about higher-order form, originality, cadence, stance, and
  specificity rather than only vocabulary.

Primary sources and original discussions take precedence over SEO listicles.
Community evidence is labelled as community evidence. Correlation, reader
reaction, model prevalence, and proof of authorship are not treated as the
same claim.

Every active fatigue pattern has a review date. Review may retain, amend,
downgrade, or retire it. A pattern that becomes ordinary, model-specific,
unsupported, or counterproductive must not remain permanent cargo cult. The
source record preserves why it changed without forcing retired material into
normal runtime context.

## Marketplace and installed-skill migration

The migration is one coherent source-custody change:

| Current source | Target |
| --- | --- |
| `repo-worker-pack/skills/writing-with-clarity` | Move with history to `writing-pack/skills/writing-with-clarity` |
| `repo-worker-pack/skills/unslop-profiles` | Remove duplicate source; retain `unslop-plus/skills/unslop-profiles` |
| `unslop-plus/skills/unslop-engine` | Remains in `unslop-plus` |
| `unslop-plus/skills/unslop-profiles` | Remains in `unslop-plus`; move its library from top-level `profiles/` to lawful `references/profiles/` |
| No writing composition skill | Add `writing-pack/skills/writing` |
| No writing style skill | Add `writing-pack/skills/writing-style` |
| No writing-specific engine | Add `writing-pack/skills/writing-profile-engine` |

The implementation must:

1. Scaffold `writing-pack` with the normal plugin manifest, license, icon,
   source record, bundle manifest, and marketplace metadata.
2. Add `writing-pack` and `unslop-plus` to this repository's
   `INSTALLED_BY_DEFAULT` set before regenerating installed skills.
3. Remove the two duplicate source entries from `repo-worker-pack` in the same
   coherent change.
4. Update root `AGENTS.md`, marketplace README material, source records, plugin
   descriptions, indexes, and other surfaces that state the installed or
   bundled skill inventory.
5. Audit cross-skill references for physical sibling-path assumptions. Replace
   those assumptions with stable skill-name or canonical source references.
6. Regenerate bundle manifests, marketplace manifests, installed skills,
   indexes, and provenance through the repository commands. Do not hand-edit
   generated `.agents/skills/` copies.
7. Move the retained generic profile library under
   `unslop-profiles/references/profiles/`; no skill may keep a top-level
   `profiles/` directory.

The migration must leave exactly one canonical marketplace source for each
skill name. Installed `.agents/skills/` copies remain generated deployment
outputs and are not counted as duplicate source custody.

## Testing and validation

### Focused tests

- Schema tests for all required pattern, evidence, date, source, and golden
  fields.
- Engine unit tests for discovery, typed evaluation, preserve/repair/abstain
  handling, and deterministic output.
- Negative tests proving a phrase match does not become an automatic repair.
- Golden tests covering every active pattern and legitimate counterexample.
- Privacy tests proving external author corpora are not copied into output.
- Plugin-boundary tests proving `repo-worker-pack` no longer bundles either
  moved skill and that the repository still installs both capabilities from
  their canonical plugins.
- Reference tests for stale physical paths and missing evidence/source IDs.

### Skill behaviour tests

Use the repository's skill pressure-testing route to verify that:

- `writing` composes the stages in the declared order;
- anti-fatigue repair cannot override verified facts or required uncertainty;
- an authorised voice profile survives the final clarity pass;
- legitimate rhetorical devices are preserved;
- unsupported detector-evasion requests are rejected;
- the skills remain useful when only the bounded runtime references are
  loaded.

### Repository validation

Run the relevant focused tests, then:

```text
py -3 tools/run.py marketplace --apply
py -3 tools/run.py installed-skills --apply
py -3 tools/run.py ci --check
```

The implementation plan must confirm the exact current command contract before
execution. A green local check proves repository consistency, not exhaustive
research quality or universal reader preference.

## Publication and completion

Implementation work is complete only when:

- the research, profile assets, skills, engine, tests, and migration are
  present in canonical source;
- generated marketplace and installed-skill surfaces are current;
- focused validation and canonical CI pass;
- self-review and the repository's review workflow close all blocking findings;
- the branch is published in a draft PR with its full head SHA;
- hosted checks for that exact SHA pass before the PR is presented as ready;
- the Linear issue links the published evidence and records any deliberately
  deferred work.

Local files, a local commit, or a worker summary are not publication proof.

## Acceptance criteria

- `writing-pack` exists as the first-class marketplace writing product.
- Its initial bundle contains exactly the four named skills.
- `writing-with-clarity` remains the clarity and final-edit authority.
- `writing-style` separates voice and fatigue profiles under lawful
  `references/` paths.
- The first fatigue profile addresses every MARK-371 pattern family with
  provenance, counterarguments, false positives, repair principles, and drift
  metadata.
- `real` and similar language are treated contextually, not banned.
- The writing-specific engine validates and evaluates the pack-local contract
  without claiming authorship detection.
- `unslop-plus` remains the generic home for its engine and profiles.
- `repo-worker-pack` no longer owns duplicate writing or unslop profile source.
- The repository continues to install the moved capabilities from their
  canonical plugin homes.
- No private author corpus is committed or distributed.
- Marketplace generation, installed-skill refresh, focused tests, and
  canonical CI pass.

## Planning handoff

This design is narrow enough for one implementation plan, but the plan should
sequence the work so source custody never becomes ambiguous:

1. Research verification and contract tests
2. Writing-pack scaffold and source moves
3. Writing composition, style, profile evidence, and writing-engine TDD
4. Consumer/reference migration and generated surfaces
5. Full validation, review, publication, and Linear closeout evidence

The planner must use exact file paths, commands, and test targets discovered
from the live branch. It must not invent a compatibility layer, broaden the
generic engine redesign, or move generic profiles into writing-pack.
