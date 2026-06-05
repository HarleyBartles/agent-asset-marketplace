# House Skills Source Root

Issue: MARK-13

This directory is the canonical source-root marker for House Skills: Harley's
first-party GPT-native custom skill set after the MARK-9 sanity rollup.

This slice intentionally does **not** import full skill source text. Later
House Skills import slices should add reviewed, versioned GPT-native skill
sources here before projecting them into one or more Codex plugin bundles.

## Current Scope

- Establish first-party source custody for the `house-skills` asset family.
- Keep accepted, provisional, retired, folded, and reference-only decisions in
  provenance/source metadata instead of pretending every historical skill is
  active or installable.
- Preserve the distinction between canonical skill source identity and Codex
  plugin projection.

## Non-Goals In This Slice

- No ChatGPT skill ZIP packaging.
- No full House Skills text import.
- No revival of `skill-market`.
- No standalone GitHub operations or GitHub issue-management skills.
- No deck, PPTX, or receipt surfaces.
