# `authoring-skills` design

## Problem

The repository can now create first-party skills that are grounded in an
authoritative external source, but that authoring pattern is not yet encoded
as a durable skill-authoring contract.

Without a dedicated contract, future workers may:

- modify the third-party `superpowers-plus:writing-skills` skill to add
  repository-specific custody rules;
- copy a large source into ordinary `references/` and cause agents to consume
  it by default;
- omit the exact source revision, license, attribution, or source links;
- write decomposed references without recording which source sections they
  cover;
- fail to notice that an upstream standard, catalogue, or reference has
  changed; or
- publish `use_with` composition metadata that disappears during source
  normalization or projection.

The immediate example is an OWASP-derived skill: a skill reconciled against
today's threat catalogue must be easy to identify as stale when tomorrow's
catalogue is released. The same contract should support the planned DDD
skill, OpenAPI and event specifications, and other specialist skills with
authoritative source material.

## Scope

Add a first-party `authoring-skills` companion skill to `repo-worker-pack`.
The skill will define how to author, review, custody, decompose, and refresh a
first-party skill grounded in an authoritative source.

The canonical skill source will live at:

```text
sources/first_party/skills/authoring-skills/
```

The installable projection will live at:

```text
codex-marketplace/plugins/repo-worker-pack/skills/authoring-skills/
```

The projection is generated from the canonical source and the editable
`repo-worker-pack` entry in:

```text
codex-marketplace/custody-pack-registry.json
```

The design covers the authoring skill, its references and templates, required
metadata behavior, source-grounded skill conventions, and the validation and
generation seams needed to keep those surfaces aligned.

## Goals

1. Provide a stable first-party companion to
   `superpowers-plus:writing-skills` without modifying third-party Superpowers
   custody.
2. Make source-grounded skill authoring a named, discoverable authoring lane.
3. Keep ordinary skill use bounded: agents read the router and selected short
   references, not the entire authoritative source.
4. Preserve exact source links so maintainers can quickly check whether a
   source has a newer edition, release, tag, or commit.
5. Record the exact source revision against which the decomposition was
   reconciled.
6. Keep source assets under their original license and keep first-party
   synthesis explicitly distinguishable from verbatim or adapted content.
7. Make source-section coverage reviewable and refresh work deterministic.
8. Ensure `use_with` metadata survives normalization, projection, cataloging,
   packaging, and generated-surface rebuilds.
9. Make `authoring-skills` the owner of cross-repository skill-authoring
   practice while leaving repository-local documents responsible only for
   this marketplace's paths, commands, and policy deltas.

## Non-goals

- Modifying or overlaying `superpowers-plus:writing-skills`.
- Automatically loading every companion skill from metadata. `use_with` is a
  routing and composition signal; the skill body remains the behavioral
  contract.
- Establishing legal advice or declaring that a source is redistributable
  merely because it is available online.
- Automatically rewriting a skill when its upstream source changes.
- Replacing the repository's existing third-party source-custody and adapter
  rules.
- Converting every existing specialist skill in this change.
- Removing repository-local skill-authoring documents when they contain local
  policy that has no portable home.
- Making generated README, SOURCE, PROJECTION, manifest, or index surfaces
  authored sources of truth.

## Existing guidance inventory

The live repository has several related surfaces. They have different owners
and must not become competing skill-authoring authorities:

| Surface | Current responsibility | Disposition |
| --- | --- | --- |
| `superpowers-plus:writing-skills` | General skill-authoring technique, skill TDD, discovery, and forward testing | Retain as third-party source; compose with `authoring-skills`; do not overlay |
| `docs/skill-standards-policy.md` | First-party marketplace standards, local frontmatter, metadata, word limits, and installable-skill requirements | Retain as a thin repository-specific policy; move portable authoring rules to `authoring-skills` and link to it |
| `.agents/guides/skill-authoring-guide.md` | Local authoring entrypoint, source paths, commands, and testing handoff | Retain as a thin local guide; remove duplicated generic standards and point to `authoring-skills` plus the local policy |
| `sources/first_party/skills/repo-worker-base/SKILL.md` | Portable repo-work routing and Superpowers composition | Do not add skill-authoring doctrine; only add `authoring-skills` to composition where a repo-worker route genuinely needs it |
| `sources/first_party/skills/repo-worker-base/references/design-baseline.md` | Portable design-stage baseline | Retain; it owns design-stage evidence and handoff, not skill-authoring content |
| `.agents/guides/design-guide.md` | Repository-specific design-spec paths, required sections, and handoff confidence | Retain; `authoring-skills` must follow it when the new skill is authored here |
| `docs/overlay-adapter-policy.md` | Third-party adaptation and overlay rules | Retain; add only a cross-reference if needed, never duplicate first-party source-grounded rules |
| `docs/contracts/skill-frontmatter.md` | Installable projection frontmatter contract | Retain as the projection contract; `authoring-skills` references it rather than restating it |
| `.agents/skills/writing-skills/` | Installed third-party projection/cache | Do not edit; it is not a repository-local authoring authority |

The cleanup rule is simple: one rule has one authoritative home. The
`authoring-skills` skill owns portable method and source-grounded custody;
`docs/skill-standards-policy.md` owns this repository's stricter standards;
`.agents/guides/skill-authoring-guide.md` owns only local navigation and
commands; projection contracts and third-party adaptation policies retain
their existing owners.

## Design decisions

### 1. Two authoring lanes

The repository will recognize two first-party authoring lanes:

| Lane | Use when | Source treatment |
| --- | --- | --- |
| Original first-party | The skill is an independently authored technique, pattern, router, or project-specific guide | External sources may be cited, but no source bundle is required |
| Source-grounded first-party | The skill is derived from a specification, standard, creator-authored reference, official documentation set, or maintained catalogue | The exact source is custody-tracked separately, decomposed references are mapped to it, and freshness metadata is required |

`authoring-skills` governs the second lane and composes with
`superpowers-plus:writing-skills`, which continues to govern the general
skill-authoring workflow and TDD-style skill verification.

### 2. Portable versus repository-specific ownership

`authoring-skills` is portable doctrine packaged for this repository's workers.
It must not absorb rules that depend on this repository's paths, generator
commands, plugin inventory, license choice for first-party skills, or local
publication gates.

The local policy surfaces will link to the portable skill and retain only
their local delta. In particular:

- `docs/skill-standards-policy.md` keeps the marketplace's required metadata,
  canonical source paths, first-party MIT choice, projection frontmatter,
  local word limits, and local validation commands.
- `.agents/guides/skill-authoring-guide.md` keeps the local read order,
  marketplace rebuild commands, install test, and local handoff expectations.
- `authoring-skills` owns the general concepts of source-grounded custody,
  source maps, pinned/latest source URLs, decomposition, content modes, and
  refresh review.

The implementation must remove duplicated portable paragraphs from the two
local documents and replace them with links or short local routing statements.
It must also update inbound links so no document points at a retired section or
describes a rule that has moved.

### 3. `authoring-skills` is first-party and belongs in `repo-worker-pack`

The skill is repository-specific worker infrastructure, not part of the core
Superpowers contract. It will be projected into `repo-worker-pack` so workers
receive it with the repository baseline while the third-party Superpowers
source remains immutable.

The canonical frontmatter will include composition metadata in the following
shape:

```yaml
metadata:
  source_category: first_party
  use_with:
    - superpowers-plus:writing-skills
```

The skill body will also contain an explicit required-companion section. The
metadata supports discovery and validation; it does not replace an imperative
instruction to use the companion skill.

### 4. Exact source assets are cold references

An authoritative source that is legally eligible for custody will be stored
under the source-grounded skill's `assets/` tree:

```text
assets/reference-source/<authority>/<revision>/
```

The asset directory may contain the exact source file, license text, notices,
and a machine-readable source manifest. It is not part of the ordinary
short-reference routing surface.

The router must state a cold-source rule equivalent to:

> Do not inspect the bundled authoritative source during ordinary use. Read
> only the relevant source section when a selected short reference leaves an
> unresolved question about terminology, scope, exception, or provenance.

The source is reference and provenance authority. It is not automatically the
current operational guidance for every task.

### 5. Source links distinguish pinned custody from freshness checks

Every source-grounded skill must record both the exact source used and the
location to check for future updates:

```yaml
authority:
  title: OWASP Top 10
  canonical_url: https://owasp.org/www-project-top-ten/
  pinned_source_url: https://github.com/OWASP/Top10/tree/<commit-or-edition>
  latest_check_url: https://owasp.org/www-project-top-ten/
  revision: "2025"
  retrieved_at: "2026-07-20"
  content_sha256: "<sha256>"
  license: CC-BY-SA-4.0
  license_url: https://creativecommons.org/licenses/by-sa/4.0/
```

`pinned_source_url` proves what the skill used. `latest_check_url` tells a
maintainer where to look for a newer version. `revision` and
`reconciled_against` identify what the decomposition actually covers.

Freshness checking is a maintenance operation, not a normal task-time
requirement. A later implementation may add a non-mutating drift checker, but
the initial contract must make manual comparison trivial without requiring
that tool.

### 6. Short references are decomposed and source-mapped

The normal operational surface remains a small `SKILL.md` router plus
task-selected references. Each source-grounded reference must declare the
source sections or concepts it covers:

```yaml
decomposition:
  reconciled_against: "2025"
  references:
    - path: references/injection.md
      source_sections:
        - "A05:2025"
      content_mode: first_party_synthesis
      load_when:
        - injection
        - untrusted input
```

The source map must expose intentional gaps as well as covered sections. A
source-grounded skill must not imply complete authority coverage when it only
implements a selected subset.

### 7. Content modes remain explicit

Source-grounded authoring will use three content modes:

| Mode | Meaning | Default location |
| --- | --- | --- |
| `first_party_synthesis` | Independently authored explanation grounded in the source | `SKILL.md` or `references/` |
| `licensed_adaptation` | Permitted derivative or adapted source material | Separate reference file with original license and attribution |
| `verbatim_source` | Exact upstream material retained for cold reference | `assets/reference-source/` |

The default for first-party router and short-reference prose is
`first_party_synthesis`. Source licenses must not be inferred from the
repository's first-party MIT license, and first-party prose must not be
presented as an official source text.

These source-grounding modes belong in the source manifest and section map.
They are distinct from the marketplace projection manifest's existing
`content_mode` values (`verbatim`, `normalised`, and `adapted`). The
implementation must not overload one field with both meanings.

### 8. `use_with` is structured metadata with preservation requirements

`use_with` will be a list of skill identifiers, beginning with:

```yaml
use_with:
  - superpowers-plus:writing-skills
```

The first-party source format already permits nested metadata, but the
normalization and projection tools must explicitly preserve and validate the
field. Unknown metadata must not silently vanish during rebuild.

The implementation must update the first-party metadata whitelist and add
tests proving that `use_with` survives:

- canonical source parsing;
- first-party catalog generation;
- marketplace projection;
- bundle-manifest and source-map generation; and
- skill packaging.

## Proposed skill contents

```text
sources/first_party/skills/authoring-skills/
  SKILL.md
  references/
    source-grounded-authoring.md
  templates/
    source-manifest.yaml
    source-section-map.yaml
    source-grounded-skill.md
    decomposed-reference.md
```

`SKILL.md` remains a compact router. The heavy reference covers authority
classification, license verification, custody layout, decomposition,
freshness, and review. Templates encode required structure rather than
prescribing domain prose.

The templates must require, at minimum:

- canonical source URL;
- pinned source URL;
- latest-check URL;
- source revision or edition;
- retrieval date;
- content hash;
- license and license URL;
- attribution and notice paths;
- reconciliation revision;
- reference-to-source section mapping;
- content mode; and
- explicit cold-source read policy.

## Repository seams

### Canonical source

Add the new skill under `sources/first_party/skills/authoring-skills/` with
first-party metadata and the companion declaration.

The implementation must also repair the local authoring guidance split:

1. Update `docs/skill-standards-policy.md` to introduce
   `authoring-skills` as the portable companion and retain only marketplace
   standards and local deltas.
2. Update `.agents/guides/skill-authoring-guide.md` to become a thin local
   route through `authoring-skills`, the local skill standards, source custody,
   and marketplace generation commands.
3. Search all tracked skill-authoring references for stale section names,
   duplicated portable rules, and links that still imply the local guide owns
   the complete cross-repository authoring method.
4. Leave third-party `writing-skills` and its projections unchanged.

### Pack membership

Add one verbatim first-party entry to the `repo-worker-pack` node in
`codex-marketplace/custody-pack-registry.json`. The registry remains the
editable membership source of truth.

### Projection and generated surfaces

Run the canonical marketplace rebuild. Do not hand-edit the projected skill,
bundle manifest, source map, provenance map, README, SOURCE, PROJECTION, or
index surfaces.

### Metadata tooling

Extend the first-party normalization whitelist and any relevant metadata
validators to preserve and validate `use_with`. If the source manifest and
decomposition map are later added to generated inventory, wire them through
the existing manifest-driven generation path rather than introducing a
pack-specific writer.

## Validation strategy

Follow `superpowers-plus:writing-skills`'s skill-TDD discipline for the new
skill:

1. Run baseline pressure scenarios without `authoring-skills`.
2. Record whether agents omit source links, read the full source by default,
   conflate source and first-party prose, or skip freshness metadata.
3. Write the smallest companion skill that addresses those failures.
4. Re-run the same scenarios with both skills composed.
5. Add regression scenarios for upstream version changes and metadata loss.

Repository validation must include:

- first-party skill validation;
- `use_with` metadata preservation tests;
- source-manifest schema validation;
- decomposition coverage and reconciliation checks;
- authoring-guidance ownership checks proving that portable rules appear in
  `authoring-skills` and local documents retain only local deltas;
- stale-link and duplicate-rule searches across skill-authoring guides;
- full marketplace rebuild;
- `py -3 tools/check_marketplace.py`;
- `py -3 -m pytest tests/ -x`; and
- `git diff --check`.

The skill itself must be tested for retrieval shape, not only for prose
quality. A successful test must demonstrate that an agent selects a relevant
short reference and consults the cold source only when the scenario requires
it.

## Future refresh workflow

For each source-grounded skill:

1. Open `latest_check_url` during maintenance.
2. Compare the discovered source revision with `reconciled_against`.
3. If the revision differs, inspect the pinned source and source diff.
4. Update or split short references as needed.
5. Refresh the exact source asset, license/notice files, hash, and source map.
6. Re-run source-grounded pressure tests.
7. Rebuild and validate all marketplace surfaces.

The workflow should eventually be supported by a non-mutating checker that
reports “current,” “source revision changed,” or “latest version unresolved.”
That checker is future work, not a prerequisite for the authoring contract.

## Guidance migration and duplicate prevention

The first implementation must treat guidance placement as a source-custody
change, not as additive documentation work. Before adding new prose to
`authoring-skills`, classify each existing rule in
`docs/skill-standards-policy.md` and `.agents/guides/skill-authoring-guide.md`
as either portable or repository-specific.

Portable rules move or are summarized in `authoring-skills`; local rules stay
where the repository's generators, paths, and policy make them authoritative.
The local documents should use short routing statements rather than copied
explanations. A final search must prove that there is no second, conflicting
description of source-grounded authoring, source freshness, or decomposition.

This migration intentionally does not move the general TDD skill-authoring
method out of third-party `superpowers-plus:writing-skills`. The companion
relationship is the boundary: Superpowers owns general skill creation;
`authoring-skills` owns repository-worker source-grounded extensions.

## Human-authority decisions

The human partner must approve:

- whether a candidate source is authoritative enough for the skill's claimed
  scope;
- whether its exact material may be redistributed under the identified
  license;
- whether the first-party decomposition is sufficiently complete for its
  intended use; and
- whether a source revision change requires a refresh before the skill remains
  active.

The skill may document evidence and recommendations, but it must not silently
make those canon or licensing decisions on behalf of the repository owner.

## Handoff to implementation planning

After this design is approved, the implementation plan should be staged as:

1. Add and test the `authoring-skills` canonical skill, references, and
   templates.
2. Reconcile `docs/skill-standards-policy.md` and
   `.agents/guides/skill-authoring-guide.md` into the ownership split.
3. Extend metadata normalization and validation for `use_with`.
4. Add the skill to `repo-worker-pack` through the registry.
5. Rebuild and validate all generated marketplace surfaces.
6. Review the skill and local guidance with fresh eyes, then run
   source-grounded pressure scenarios.

No DDD, OWASP, or other specialist skill migration is part of this design's
implementation. Those migrations begin only after this authoring contract is
landed and validated.

## Handoff confidence

**8/10.** The source and projection seams, ownership split, metadata contract,
refresh behavior, and validation expectations are concrete enough for one
implementation plan. The remaining human authority is limited to approving
the final wording of the local-policy reduction and the exact pressure
scenarios used to verify composition with `superpowers-plus:writing-skills`.
