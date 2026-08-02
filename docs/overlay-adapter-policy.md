# Overlay and Adapter Policy

This policy defines when and how to adapt third-party skills for the agent-asset-marketplace repo. It covers provenance modes, overlay adapter triggers, and the normalisation exception for third-party source.

Use this policy when adapting third-party skills, adding overlay adapters, or deciding whether a skill needs adaptation.

For first-party skill authoring standards, see `docs/skill-standards-policy.md`.

## External references

- `docs/custody-and-marketplace-doctrine.md` — custody and export doctrine
- `docs/contracts/skill-frontmatter.md` — frontmatter contract

## Default: do not edit third-party source

Third-party skills are retained as provenance records or reference snapshots. Do not edit third-party source to adapt skill behavior. Adaptation happens through overlay adapters at plugin build time.

## Provenance modes

Every marketplace entry carries one provenance mode:

- **`verbatim`** — byte-identical to source custody. No transformation.
- **`normalised`** — minimal compliance adaptation only: codex-safe shape, openai-spec compliance, rich metadata, repointing moved-file links. The skill body is unchanged beyond link repointing. Ownership stays with the upstream author.
- **`adapted`** — substantive skill body changes beyond compliance. The plugin distribution must record what changed and why.

## Normalisation exception (editing third-party source)

Default: never edit third-party source content. The only authorized exception is line-ending and whitespace normalization (CRLF to LF, trailing whitespace stripping) for cross-platform consistency. This is a one-time pass, not a precedent for content edits.

If a third-party skill needs a content change, the path is:
1. Add a Codex overlay adapter under `adapters/codex/<plugin>/<skill>/`.
2. Set `content_mode` to `normalised` or `adapted` in the bundle manifest.
3. Record the adaptation note in the manifest entry.
4. Regenerate the plugin distribution with `py -3 tools/run.py marketplace --apply`.

Do not edit the third-party source tree to fix a skill. Edit at the adapter layer.

## When to add a Codex overlay adapter

- A third-party skill references harness-specific features (Claude hooks, Cursor plugins, etc.) that need repointing for Codex compatibility.
- A third-party skill's frontmatter needs normalization to marketplace schema without changing the instruction body.
- A third-party skill's internal links point to moved files that need repointing.

This is the `normalised` mode. The skill body stays unchanged beyond link repointing.

## When NOT to add an overlay adapter

**Usually, do not add an overlay.** If a skill is not suitable as a raw GPT
package, it should not be distributed at all (set `import_status` or
`content_mode` to `skipped`/`blocked` in the bundle manifest).

## First-party is always verbatim in distribution

First-party skills are always `verbatim` in distribution. If a first-party skill needs to change, fix the canonical source under `codex-marketplace/plugins/<plugin>/skills/<name>/` and run `py -3 tools/run.py marketplace --apply`. Do not adapt first-party content at distribution time. See `docs/skill-standards-policy.md` for first-party authoring standards.
