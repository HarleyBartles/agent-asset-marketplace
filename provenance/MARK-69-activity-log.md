# MARK-69 Activity Log

## Start Posture

- Date: 2026-06-09
- Branch: `mark-69-openai-plugins-drain`
- Upstream repo: `openai/plugins`
- Upstream URL: <https://github.com/openai/plugins.git>
- Upstream commit: `c33199897758cab145bb7fdab1ca8fb1cbd9de50`
- Marketplace route: `codex-marketplace/plugins/` plus `.agents/plugins/marketplace.json`
- Vendor custody route: `sources/vendor/openai/plugins/c33199897758cab145bb7fdab1ca8fb1cbd9de50/`

## Inventory Summary

- Candidate roots inventoried: `174`
- Imported into the marketplace: `168`
- Blocked from marketplace publication: `6`

## Blocked Roots
- `plugins/codex-security`: proprietary upstream license is not re-vendorable into the marketplace
- `plugins/convex`: upstream plugin has no redistributable license declaration
- `plugins/figma`: Figma developer terms are not a re-vendored marketplace license
- `plugins/life-science-research`: proprietary upstream license is not re-vendorable into the marketplace
- `plugins/magicpath`: upstream plugin has no redistributable license declaration
- `plugins/openai-developers`: proprietary upstream license is not re-vendorable into the marketplace


## Notes

- The upstream source snapshot was copied into vendor custody under the pinned commit, then the six blocked roots were removed from `sources/vendor/openai/plugins/c33199897758cab145bb7fdab1ca8fb1cbd9de50/plugins/` so they remain provenance-only.
- Marketplace-facing copies were normalized only where required for registry compatibility.
- The machine-readable inventory is stored in `provenance/MARK-69-openai-plugins-inventory.json`.
- Validation enforces that the blocked roots do not remain in vendor custody.
