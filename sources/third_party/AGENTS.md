# AGENTS.md

Scope: `sources/third_party/`

This scope covers third-party source custody, upstream snapshots, and the
retained third-party evidence tree.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Manifest guidance

Where a retained third-party snapshot feeds a marketplace projection, the
matching bundle manifest must declare `content_mode` for imported entries.

- `verbatim` means the retained snapshot and the projected plugin copy must
  remain byte/hash equivalent.
- `adapted` means equality is not expected, but the entry must carry an
  explicit adaptation note and a provenance trail.
- Projection roots under `codex-marketplace/plugins/` are distribution
  surfaces, not canonical source custody. Keep them aligned with the retained
  source/provenance contract recorded in the manifest.

## Review guidelines

- Treat nested upstream `AGENTS.md` files inside third-party snapshots as vendored
  package instructions, not repository doctrine.
- Flag third-party files that change without an explicit adaptation reason, source
  note, or license/notice update.
- Flag false "copied verbatim" claims after any adaptation, repackaging, or
  normalization.
- Flag license, notice, or source-map drift that breaks custody evidence.
- Flag source-root claims that do not match the pinned upstream snapshot or the
  actual third-party path recorded in provenance.
