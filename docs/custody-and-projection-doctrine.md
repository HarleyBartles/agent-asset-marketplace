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

Two mega-packs carry broad bundles:

- **`house-skills`** is the first-party mega-pack. Every first-party skill goes
  in `house-skills` AND wherever else it is bundled. If a first-party skill is
  projected into a topical plugin, it must also appear in `house-skills`.
- **`superpowers-plus`** is the mega-pack for the obra/superpowers source
  family. Superpowers-family entries are bundled there in addition to any
  topical plugin they appear in.

Mega-packs are inclusion rules, not exclusion rules. A skill appearing in a
mega-pack may also appear in other plugins.

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

1. **Write source** — add or edit the skill under `sources/first_party/` or
   snapshot it under `sources/third_party/`.
2. **Add manifest entry** — declare the entry in the marketplace manifest with
   its provenance mode and target plugin(s).
3. **Add GPT decision** — record the GPT export lane decision (see below).
4. **Run one tool** — regenerate the projection with the designated tooling
   (e.g. `py -3 tools/update_skill_artifacts.py --skill <pack>/<skill>`).
5. **Validate** — run the repo validator and confirm the projection matches
   custody and manifest.

No Python edits for normal skill work. If the workflow requires editing Python
to land a skill, that is a tooling gap to raise, not a step to silently absorb.

## First-party orphan detection

A first-party skill that exists in source custody but is missing from
projection is an orphan. The tooling is expected to detect first-party
orphans: skills present under `sources/first_party/` with no corresponding
projection entry. Orphans should be surfaced by validation, not silently
ignored. The fix is to add the manifest entry and regenerate, not to delete
the source.

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
