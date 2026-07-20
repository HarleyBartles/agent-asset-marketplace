# Source-grounded authoring

Use `superpowers-plus:writing-skills` when creating, reviewing, or refreshing a
skill. Select the lane before drafting: `first_party` is original operational
guidance with no authority assets; `skills-with-source` records approved
redistributable source; and `skills-with-citation` is a clean-room synthesis
from citable sources only.

For either source-backed lane, decompose the authority into operational files
under `references/`. Every `authority.yaml` and `source-map.yaml` reference
records its `path`, `source_sections` mapping, `load_when` trigger, and content mode.
Keep the two records reconciled: the source map is the operational projection
of `authority.yaml`'s decomposition, not a second authority manifest.

`skills-with-source` requires legal redistribution approval before a source is
copied. Put approved cold material in `assets/authority/reference-source/` and
write operational prose from the recorded decomposition. `skills-with-citation`
must use `first_party_synthesis` for every reference, keep no vendored source,
and maintain scholarly evidence in `assets/authority/CITATIONS.md`.

No inline citations belong in operational prose. Put authority metadata,
citations, derivation boundaries, reconciliation, and review evidence in
`assets/authority/`. Freshness is manual: a human performs a manual freshness
review, records retrieval details, and approves any refresh before the skill
changes.
