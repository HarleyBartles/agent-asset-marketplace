# MARK-13 House Skills Marketplace Skeleton Audit

Status: created for validation evidence by `python3 tools/validate_marketplace.py`.

## Checkout Identity

- Working tree path: `/workspace/agent-asset-marketplace`
- Branch: `codex/mark-13-house-skills-skeleton`
- Starting HEAD: `9ad912c327669d7feed74eaacb78f3083c76d3e6`
- Issue: MARK-13

## Marketplace Summary

- Marketplace file: `.agents/plugins/marketplace.json`
- Installable skeleton projection: `house-skills`
- Plugin source projection: `plugins/house-skills/`
- Canonical GPT-native source marker: `gpt-skills/house-skills/README.md`
- Asset identity catalog: `sources/house-skills/assets.json`
- Intake/source posture record: `sources/house-skills/intake.json`
- License/provenance/trust record: `provenance/house-skills.md`

## House Skills Skeleton Summary

MARK-13 establishes House Skills as the repo-backed first-party bundle and
provenance group for Harley's custom GPT-native skills. The projection is
installable only as an early private skeleton so Codex can discover the bundle,
source identity, and validation metadata.

## Import Boundary

- Full House Skill source text imported: no.
- ChatGPT skill ZIPs packaged: no.
- `skill-market` revived: no.
- Standalone GitHub operations or issue-management skills created: no.
- Deck, PPTX, receipt, or generated package surfaces added: no.
- Retired/folded/reference-only historical skills made active installable entries: no.

## Schema Assumptions

- The existing `assetCatalog` string remains for backward compatibility with
  MARK-2/Superpowers.
- MARK-13 adds `assetCatalogs` as a narrow generalization so multiple source
  identity catalogs can be validated without merging unrelated asset families
  into one file.
- Plugin projection metadata must reference projection and asset IDs present in
  one of the declared asset catalogs.

## TODOs For Later House Skills Import Slices

- Add reviewed, versioned canonical skill sources under `gpt-skills/house-skills/`.
- Project selected skills into `plugins/house-skills/skills/` or other sensible
  bundles after source/provenance records are updated.
- Revisit per-skill license, localization, quality, and installability posture
  when actual content is imported.
