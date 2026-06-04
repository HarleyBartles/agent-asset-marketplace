# MARK-2 Marketplace Audit

Status: created for validation by `python3 tools/validate_marketplace.py`.

## Checkout Identity

- Working tree path: `/workspace/agent-asset-marketplace`
- Expected origin: `https://github.com/HarleyBartles/agent-asset-marketplace.git`
- Git network operations intentionally not used for publication or verification per MARK environment instruction.

## Marketplace Summary

- Marketplace file: `.agents/plugins/marketplace.json`
- Installable projection: `superpowers-workflow-pack`
- Reference-only projection: `superpowers-upstream-reference`
- Asset identity catalog: `sources/obra-superpowers/assets.json`
- Upstream intake record: `sources/obra-superpowers/intake.json`
- License/provenance record: `provenance/obra-superpowers.md`

## Superpowers Intake Summary

- Upstream: `obra/superpowers`
- Observed manifest version: `5.1.0`
- Observed upstream license: MIT
- Observed upstream skill identities: 14 reference-only skill assets
- Mirrored upstream content in MARK-2 installable projection: none

## Blocked Or Metadata-Only Sources/Assets

- `superpowers-upstream-reference` is metadata-only and not installable.
- Upstream skill identities are listed as reference-only until future review intentionally selects and mirrors content with notices.

## Validation

Run:

```sh
python3 tools/validate_marketplace.py
```

The script validates marketplace JSON, plugin source paths, plugin manifests, declared skills paths, provenance/license metadata, absence of mirrored third-party content without clearance, quality metadata, localization metadata, and this audit artifact.
