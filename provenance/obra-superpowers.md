# obra/superpowers Provenance And License Posture

Issue: MARK-2

## Upstream

- Repository: <https://github.com/obra/superpowers>
- Observed Codex plugin manifest: <https://raw.githubusercontent.com/obra/superpowers/main/.codex-plugin/plugin.json>
- Observed upstream manifest version: `5.1.0`
- Observed author: Jesse Vincent
- Observed upstream license: MIT
- License source: <https://raw.githubusercontent.com/obra/superpowers/main/LICENSE>

## MARK-2 Decision

`obra/superpowers` is used as the first upstream proof source and retained as an upstream aggregate. The marketplace does not blindly import Superpowers as one giant curated plugin.

MARK-2 creates two projections:

1. `superpowers-workflow-pack` — installable, locally authored adapter/projection that can answer "install this to do disciplined coding-agent workflow work." It does not mirror upstream skill text.
2. `superpowers-upstream-reference` — metadata-only/reference-only projection for the upstream aggregate. It is explicitly not installable.

## License Posture

- Licensing is first-class even though this marketplace is private.
- Available upstream does not mean safe to mirror.
- Safe to list does not mean safe to bundle.
- Upstream declares MIT, but MARK-2 still avoids copying upstream skill text, scripts, hooks, SVGs, or binary assets into the installable projection.
- If future projections copy upstream content, they must include the MIT notice and update copied-content provenance before becoming installable.

## Quality Posture

Retained and projected assets carry production-grade metadata in:

- `.agents/plugins/marketplace.json`
- `sources/obra-superpowers/intake.json`
- `sources/obra-superpowers/assets.json`
- plugin manifests under `plugins/*/.codex-plugin/plugin.json`

Current quality status:

- `superpowers-workflow-pack`: early private marketplace baseline, review required before external distribution.
- `superpowers-upstream-reference`: metadata-only, not installable.

## Localization Posture

The inspected source and local projections are English-source assets. No translation is needed for MARK-2 unless future content inspection proves otherwise.

## Blocked Or Metadata-Only Assets

The upstream aggregate and all listed upstream skill identities are retained as metadata-only/reference-only in MARK-2. They are not copied into the installable plugin projection.
