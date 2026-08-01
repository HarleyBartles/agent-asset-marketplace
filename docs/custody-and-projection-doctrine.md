# Custody and projection doctrine

This document is required reading for agents working in this repo. It defines
where source lives, how it is projected into the marketplace, and how the
projection is exported as GPT-ready zips. It is authoritative, not a tutorial.

## Source custody

Source custody is the canonical home for asset content. Projection and export
surfaces are derived from custody, never the reverse.

- **Third-party pool** lives under `provenance/`. These are verbatim
  upstream snapshots pinned to a commit. Preserve upstream source, package
  payload, license, notice, and source-map evidence there. Do not edit
  third-party custody to adapt skill behavior; adapt at projection time and
  record the adaptation honestly.
- **First-party authoring** lives under `codex-marketplace/plugins/<plugin>/`. These are
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
needs to change, fix the source under `codex-marketplace/plugins/<plugin>/` and regenerate.
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

## Mega-packs (retired)

The `house-skills` mega-pack, `is_mega_pack` registry field, and
`tools/generate_mega_packs.py` have been removed. First-party skills now
project into topical packs directly; `superpowers-plus` remains the only
mixed plugin bundle. This section is kept as a tombstone for
historical context.


## Projection layer model

The flow is:

1. **Source custody** — `provenance/` and `codex-marketplace/plugins/<plugin>/`.
2. **Projection** — `codex-marketplace/plugins/` vendored bundles, generated
   from custody plus manifest entries.
3. **Install / export** — `codex-marketplace/plugins/` is the canonical install
   surface.

Projection is generated, not hand-edited. The manifest is the edit surface that
drives projection.

Projection discovery shortcut: when a generated plugin projection needs to
change, start at the source skill, then the plugin manifest, then the relevant
validator, then the generated projection tree. If the source or manifest
changes, regenerate the derived outputs instead of hand-editing the generated tree.

When a change touches multiple generated surfaces, prefer regenerating the full
market surface set before chasing validator failures one artifact at a time.
The validator is a proof gate, not a replacement for regeneration.

## BAU workflow

The business-as-usual target for adding or updating a skill is:

1. **Write source** — add or edit the skill under `codex-marketplace/plugins/<plugin>/skills/`
   or snapshot it under `provenance/`.
2. **Add manifest entry** — declare the entry in the pack's
   `codex-marketplace/custody-pack-registry.json` bundle `entries` with
   `canonical_name`, `source_category`, `content_mode`, `source_family`,
   `canonical_source_path` (directory-level), and `local_path`.
3. **Regenerate projection** — run `tools/run marketplace --apply` to update
   bundle manifests, source maps, provenance maps, projected skill trees, and
   marketplace exports.
4. **Validate** — run `tools/run ci --check` to prove all surfaces are current.

If a first-party skill is removed from a project pack but remains in source
custody, keep the source and regenerate the projections so only the pack loses
the exposure. Retire a skill to provenance only when it is no longer supported.

No Python edits for normal skill work. If the workflow requires editing Python
to land a skill, that is a tooling gap to raise, not a step to silently absorb.

## Manifest shape validation

All 19 plugin manifests must use the directory-level `entries[]` plugin
shape. The validator (`validate_no_legacy_manifest_shapes`) rejects manifests
with legacy shapes (`skills[]`, `components[]`, or file-level
`canonical_source_path` ending in a file suffix). This ensures the materializer
never silently skips a plugin.

## Zip projection (retired)

Flat `skill.zip` exports under `generated/skill-zips/` and the `house-skills`
mega-pack have been removed. The Codex plugin tree under
`codex-marketplace/plugins/` is the canonical install surface.
