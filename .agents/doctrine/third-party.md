
## Scope

per-pack `SOURCE.md`

This scope covers third-party source custody, upstream evidence, and the provenance notes that record retained upstream material in each plugin pack.

Defer to the repository root `AGENTS.md` for global doctrine, publication rules, and upstream-drain policy.

Third-party custody is retained evidence, not repo doctrine. Keep any scoped guidance here limited to custody and evidence rules for the per-pack `SOURCE.md` provenance records.

Default custody shape: record the upstream repo, pinned commit, license, and adaptation path in `codex-marketplace/plugins/<plugin>/SOURCE.md`. If a vendor snapshot is retained in-tree, place it under `codex-marketplace/plugins/<plugin>/skills/<skill>/` and record it in the pack's `SOURCE.md`.

## Line-ending normalization exception

In a one-time authorized pass, CRLF line endings were normalized to LF and trailing whitespace was stripped across all retained custody files. This was an explicit exception to the default immutability rule for third-party source, authorized to eliminate cross-platform line-ending inconsistency that was causing `git diff --check` failures and generator output drift. The immutability rule still holds for content changes — only line endings and trailing whitespace were affected, not skill content. Future agents should not treat this as precedent for editing third-party source content.

## Manifest guidance

Where a third-party skill is vendored into a Codex plugin, the matching bundle manifest must declare `content_mode` for imported entries.

- `verbatim` means the retained snapshot and the plugin copy must remain byte/hash equivalent.
- `adapted` means equality is not expected, but the entry must carry an explicit adaptation note and a provenance trail.
- Plugin roots under `codex-marketplace/plugins/` are the canonical distribution and source custody surfaces. Keep them aligned with the retained source/provenance contract recorded in the bundle manifest.

## Review guidelines

- Treat nested upstream `AGENTS.md` files inside retained snapshots as vendored package instructions, not repository doctrine.
- Flag third-party files that change without an explicit adaptation reason, source note, or license/notice update.
- Flag false "copied verbatim" claims after any adaptation, repackaging, or normalization.
- Flag license, notice, or provenance drift that breaks custody evidence.
- Flag source-root claims that do not match the pinned upstream snapshot or the actual third-party path recorded in provenance.

## Maintenance responsibility

This file must stay aligned with the repo's third-party custody structure. When third-party source patterns change or new upstream snapshot conventions are added, review and update this file to reflect current expectations. Manifest guidance on `content_mode` must stay aligned with bundle-manifest practices—when those practices evolve, this file should be updated to prevent drift.
