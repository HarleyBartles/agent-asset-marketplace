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
- `plugins/codex-security`: proprietary upstream license is not re-vendorable into the marketplace; final action `clean_room_followup` via MARK-72
- `plugins/convex`: declared upstream remains `UNLICENSED`; final action `blocked`
- `plugins/figma`: OpenAI-hosted root is blocked; alternate MIT source `GLips/Figma-Context-MCP` was checked separately; final action `alternate_source_available`
- `plugins/life-science-research`: OpenAI-hosted root is blocked; alternate MIT source `GPTomics/bioSkills` was checked separately; final action `alternate_source_available`
- `plugins/magicpath`: OpenAI-hosted copy was removed from vendor custody; legal MIT upstream `MagicPathAI/agent-skills` was re-vendored separately; final action `alternate_source_available`
- `plugins/openai-developers`: proprietary upstream license is not re-vendorable into the marketplace; final action `clean_room_followup` via MARK-71


## Notes

- The upstream source snapshot was copied into vendor custody under the pinned commit, then the six blocked roots were removed from `sources/vendor/openai/plugins/c33199897758cab145bb7fdab1ca8fb1cbd9de50/plugins/` so they remain provenance-only.
- MagicPath was then drained separately from `MagicPathAI/agent-skills` under its own MIT license, so the OpenAI-hosted copy stays out of vendor custody while the marketplace still gets a legal marketplace asset.
- Marketplace-facing copies were normalized only where required for registry compatibility.
- The machine-readable inventory is stored in `provenance/MARK-69-openai-plugins-inventory.json`.
- Validation enforces that the blocked roots do not remain in vendor custody.
