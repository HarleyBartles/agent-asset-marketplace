# Custody and projection doctrine

This document is required reading for agents working in this repo. It defines
where source lives, how it is projected into the marketplace, and how the
projection is exported as GPT-ready zips. It is authoritative, not a tutorial.

## Source custody

Source custody is the canonical home for asset content. Projection and export
surfaces are derived from custody, never the reverse.

- **Third-party pool** lives under `sources/third_party/`. These are verbatim
  upstream snapshots pinned to a commit. Preserve upstream source, package
  payload, license, notice, and source-map evidence there. Do not edit
  third-party custody to adapt skill behavior; adapt at projection time and
  record the adaptation honestly.
- **First-party authoring** lives under `sources/first_party/`. These are
  Harley-authored skills. Edit the skill body here when the skill needs to
  change.
- **MIT posture.** First-party source is MIT licensed. Third-party source
  retains its upstream license; projection must preserve attribution and
  license evidence.

## Provenance modes

Every projected entry carries one provenance mode. Provenance is per-entry,
not per-plugin (see Plugin curation below).

- **`verbatim`** — the projection is byte-identical to source custody. No
  transformation, no metadata enrichment beyond what source already carries.
  Example: a first-party skill projected straight into a plugin with no
  changes.
- **`normalised`** — minimal compliance adaptation only: codex-safe shape,
  openai-spec compliance, rich metadata, and repointing of moved-file links.
  The skill body is unchanged beyond link repointing. Ownership stays with the
  upstream author. Example: a third-party skill whose YAML front matter is
  normalized to marketplace schema but whose instructions body is untouched.
- **`adapted`** — substantive skill body changes beyond compliance. The
  projection must be honest about what changed and why. Example: a third-party
  skill whose instruction body was rewritten for marketplace voice or merged
  with first-party guidance.

### First-party is always verbatim in projection

First-party skills are always `verbatim` in projection. If a first-party skill
needs to change, fix the source under `sources/first_party/` and regenerate.
Do not adapt first-party content at projection time. This keeps source custody
as the single edit point for first-party work.

## Plugin curation

Plugins under `codex-marketplace/plugins/` are curated bundles, not upstream
package mirrors. Harley curates which entries appear in which plugin.

- **Provenance is per-entry, not per-plugin.** A single plugin may mix
  `verbatim`, `normalised`, and `adapted` entries. Each entry's manifest record
  declares its own mode.
- **Plugins are not source custody.** If an entry's content needs to change,
  change the source and regenerate the projection. Do not edit plugin files
  directly to change skill behavior.

## Mega-packs

Seven mega-packs carry broad bundles, one per custody root. The
custody→mega-pack mapping is declared in
`codex-marketplace/custody-mega-pack-registry.json` and drives automatic
mega-pack manifest generation:

- **`house-skills`** — first-party mega-pack. Every first-party skill goes
  in `house-skills` AND wherever else it is bundled.
- **`codex-cortex`** — claude-cortex source family mega-pack.
- **`everything-codex-code`** — ecc source family mega-pack.
- **`superpowers-plus`** — superpowers source family mega-pack. Also
  carries curated cross-family first-party projections.
- **`game-studio`** — game-studio source family mega-pack.
- **`dotnet-kit`** — dotnet-claude-kit source family mega-pack.
- **`unslop-plus`** — unslop source family mega-pack.

Mega-pack manifests are **generated**, not hand-edited. Run
`py -3 tools/generate_mega_packs.py` to regenerate them. First-party mega-packs
such as `house-skills` are rebuilt from active first-party source custody under
`sources/first_party/skills/`, while non-first-party mega-packs are rebuilt from
the union of selected plugin entries by custody root. The generator preserves
curated cross-family entries (e.g. first-party skills projected into
`superpowers-plus`).

Mega-packs are inclusion rules, not exclusion rules. A skill appearing in a
mega-pack may also appear in other plugins. Validation
(`validate_mega_pack_inclusion`) fails if a topical plugin entry is missing
from its mega-pack.

## Projection layer model

The flow is:

1. **Source custody** — `sources/third_party/` and `sources/first_party/`.
2. **Projection** — `codex-marketplace/plugins/` vendored bundles, generated
   from custody plus manifest entries.
3. **Install / export** — `codex-marketplace/plugins/` is the canonical install
   surface; `generated/skill-zips/` is the derived GPT export corpus.

Projection is generated, not hand-edited. The manifest is the edit surface that
drives projection.

## BAU workflow

The business-as-usual target for adding or updating a skill is:

1. **Write source** — add or edit the skill under `sources/first_party/skills/`
   or snapshot it under `sources/third_party/`.
2. **Add manifest entry** — declare the entry in the plugin's
   `references/bundle-manifest.json` with `canonical_name`,
   `source_category`, `content_mode`, `source_family`,
   `canonical_source_path` (directory-level), and `local_path`.
3. **Regenerate mega-packs** — run `py -3 tools/generate_mega_packs.py` so
   the entry appears in its custody root's mega-pack automatically. For
   first-party skill adds/removals, the first-party mega-pack is rebuilt from
   `sources/first_party/skills/`; curated non-first-party mega-packs still
   follow their selected-entry unions.
4. **Add GPT decision** — record the GPT export lane decision (see below).
5. **Run one tool** — regenerate the projection with the designated tooling
   (e.g. `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`).
6. **Regenerate proof surfaces** — run
   `py -3 tools/generate_provenance_maps.py` and
   `py -3 tools/generate_source_maps.py`.
7. **Validate** — run `py -3 tools/validate_marketplace.py` and
   `py -3 tools/materialize_projection.py --check` to confirm the projection
   matches custody and manifest.

No Python edits for normal skill work. If the workflow requires editing Python
to land a skill, that is a tooling gap to raise, not a step to silently absorb.

## First-party orphan detection

A first-party skill that exists in source custody but is missing from
projection is an orphan. The validator (`detect_first_party_orphans` in
`tools/validate_marketplace.py`) scans `sources/first_party/skills/` for
directories with `SKILL.md` and checks that each one appears as a
`first_party` entry in some plugin manifest. Orphans cause validation to
fail with a clear list of the missing skills. MARK-295 removed the stale
`ecc-superpowers` wrapper source along with its projection, so there is no
retired-source exception to carry forward. For active skills, the fix is
still to add the manifest entry and regenerate, not to delete the source.

## Manifest shape validation

All 20 plugin manifests must use the directory-level `entries[]` projection-lane
shape. The validator (`validate_no_legacy_manifest_shapes`) rejects manifests
with legacy shapes (`skills[]`, `components[]`, or file-level
`canonical_source_path` ending in a file suffix). This ensures the materializer
never silently skips a plugin.

## Proof surface generation

`provenance-map.json` and `source-map.md` are generated from bundle manifests,
not hand-maintained. Run `py -3 tools/generate_provenance_maps.py` and
`py -3 tools/generate_source_maps.py` to regenerate them. Both generators have
`--check` mode that fails on drift.

## Zip projection lanes

When projecting from marketplace source to GPT-ready zips under
`generated/skill-zips/`, each entry falls into one lane:

- **`direct`** — already GPT-safe. Verbatim passthrough from projection to
  zip. No overlay needed.
- **`overlay`** — codex-safe but not GPT-safe. Needs GPT adaptation declared
  under `adapters/gpt/` to become installable as a raw GPT package. The
  overlay makes the export safe without weakening Codex-native plugin
  behavior.
- **`excluded`** — not exportable as a raw GPT package. The entry is
  intentionally omitted from the zip corpus. Exclusion is explicit, not
  silent.

The lane is a per-entry decision recorded alongside the manifest entry. It
drives export behavior, not projection behavior.
