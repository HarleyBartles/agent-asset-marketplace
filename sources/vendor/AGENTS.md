# AGENTS.md

Scope: `sources/vendor/`

This scope covers third-party source custody, upstream snapshots, and the
vendor evidence tree.

Defer to the repository root `AGENTS.md` for global doctrine, publication
rules, and upstream-drain policy.

## Review guidelines

- Treat nested upstream `AGENTS.md` files inside vendor snapshots as vendored
  package instructions, not repository doctrine.
- Flag vendor files that change without an explicit adaptation reason, source
  note, or license/notice update.
- Flag false "copied verbatim" claims after any adaptation, repackaging, or
  normalization.
- Flag license, notice, or source-map drift that breaks custody evidence.
- Flag source-root claims that do not match the pinned upstream snapshot or the
  actual vendor path recorded in provenance.
