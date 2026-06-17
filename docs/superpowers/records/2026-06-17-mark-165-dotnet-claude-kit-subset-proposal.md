# MARK-165 dotnet-claude-kit subset proposal Implementation Record

**Issue:** MARK-165
**Branch:** `codex/mark-165-dotnet-claude-kit-subset-proposal`
**Starting main SHA:** `cf36959fcf3ff4e502d2b27d103c23ffb8582fdd`
**Implementation commit SHA:** `3a680368fc051d2bb4d7b5479d1bff0718b9b0c1`
**Final head SHA:** `3a680368fc051d2bb4d7b5479d1bff0718b9b0c1`
**PR URL:** [https://github.com/HarleyBartles/agent-asset-marketplace/pull/102](https://github.com/HarleyBartles/agent-asset-marketplace/pull/102)

## Files changed

- `docs/superpowers/plans/2026-06-17-mark-165-dotnet-claude-kit-subset-proposal.md`
- `provenance/dotnet-claude-kit.md`

## Selected subset

- `modern-csharp`
- `vertical-slice`
- `clean-architecture`
- `ddd`
- `ef-core`
- `testing`

## Deferred skills

- `tdd`
- `verify`

Reason: both are workflow orchestrators with strong Claude command and validation-pipeline assumptions, so they were deferred from the first Codex-native technical slice.

## Validation

- `rg -n "original work|authored here|first-party origin" provenance/dotnet-claude-kit.md`
  - Result: passed; the only hit was the explicit anti-claim guardrail in the provenance note.
- `git diff --cached --check`
  - Result: passed; no whitespace or patch-format issues in the staged docs.
- `py -3 tools/validate_marketplace.py`
  - Result: failed on pre-existing stale generated-artifact drift for `house-skills/codex-receipts-superpowers`.

## Blocker

The repository validator reports unrelated generated-artifact drift:

- `generated/skill-zips/house-skills/codex-receipts-superpowers/skill.zip` is stale relative to `codex-marketplace/plugins/house-skills/skills/codex-receipts-superpowers`

This is outside the MARK-165 receipt work and does not affect the provenance note or subset proposal.

## No repackaging confirmation

No upstream `dotnet-claude-kit` skills were repackaged in this child. The work here is limited to intake, provenance, and subset selection for MARK-166.

## Follow-up

MARK-166 should use this plan and record pair as the receipt trail for the repack step and continue from the selected subset only.
