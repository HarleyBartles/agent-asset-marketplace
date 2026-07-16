# Overlay and Adapter Policy

This policy defines when and how to adapt third-party skills for the agent-asset-marketplace repo. It covers provenance modes, overlay adapter triggers, and the normalisation exception for third-party source.

Use this policy when projecting third-party skills, adding overlay adapters, or deciding whether a skill needs adaptation.

For first-party skill authoring standards, see `docs/skill-standards-policy.md`.

## External references

- `docs/custody-and-projection-doctrine.md` — custody, projection, and export doctrine
- `docs/contracts/skill-frontmatter.md` — projection frontmatter contract
- `sources/third_party/AGENTS.md` — third-party source custody rules

## Default: do not edit third-party source

Third-party skills live under `sources/third_party/` as verbatim upstream snapshots. Do not edit third-party source to adapt skill behavior. Adaptation happens at projection time through overlay adapters.

## Provenance modes

Every projected entry carries one provenance mode:

- **`verbatim`** — byte-identical to source custody. No transformation.
- **`normalised`** — minimal compliance adaptation only: codex-safe shape, openai-spec compliance, rich metadata, repointing moved-file links. The skill body is unchanged beyond link repointing. Ownership stays with the upstream author.
- **`adapted`** — substantive skill body changes beyond compliance. The projection must record what changed and why.

## Normalisation exception (editing third-party source)

Default: never edit third-party source content. The only authorized exception is line-ending and whitespace normalization (CRLF to LF, trailing whitespace stripping) for cross-platform consistency. This is a one-time pass, not a precedent for content edits.

If a third-party skill needs a content change, the path is:
1. Add an overlay adapter under `adapters/codex/<plugin>/<skill>/` or `adapters/gpt/<plugin>/<skill>/`.
2. Set `content_mode` to `normalised` or `adapted` in the bundle manifest.
3. Record the adaptation note in the manifest entry.
4. Regenerate the projection.

Do not edit the third-party source tree to fix a skill. Edit at the adapter layer.

## When to add an overlay adapter

Overlay adapters live under `adapters/codex/` (for Codex projection changes) or `adapters/gpt/` (for GPT export changes).

### Add a Codex overlay adapter when:

- A third-party skill references harness-specific features (Claude hooks, Cursor plugins, etc.) that need repointing for Codex compatibility.
- A third-party skill's frontmatter needs normalization to marketplace schema without changing the instruction body.
- A third-party skill's internal links point to moved files that need repointing.

This is the `normalised` mode. The skill body stays unchanged beyond link repointing.

### Add a GPT overlay adapter when:

- A Codex-safe skill is not GPT-safe and needs adaptation to become installable as a raw GPT package.
- The overlay makes the export safe without weakening Codex-native plugin behavior.

This is the GPT export lane (`overlay` mode in `adapters/gpt/manifest.json`).

## When NOT to add an overlay adapter

**Usually, do not add an overlay.** Most skills are either:
- Already GPT-safe as-is → `direct` export, no overlay needed.
- Not exportable as a raw GPT package → `excluded` from the zip corpus.

Add an overlay only when the skill is Codex-safe but not GPT-safe AND can be made GPT-safe without weakening Codex behavior. If the skill cannot be made GPT-safe without weakening it, exclude it.

## First-party is always verbatim in projection

First-party skills are always `verbatim` in projection. If a first-party skill needs to change, fix the source under `sources/first_party/skills/` and regenerate. Do not adapt first-party content at projection time. See `docs/skill-standards-policy.md` for first-party authoring standards.
