---
name: adventures-image-qa
description: Review Adventures generated candidates and compiled assets against source constraints and acceptance criteria, while keeping QA separate from image generation or editing authority.
version: v1.1
source_id: adventures-image-qa-v1.1
source_path: gpt-skills/house-skills/adventures-image-qa/SKILL.md
provenance_name: "MARK-9 chunk ledger \xC3\xA2\xE2\u201A\xAC\xE2\u20AC\x9D Adventures"
---
# Adventures Image Qa

Use this skill when Adventures work needs visual QA of generated candidates, reference art, or compiled sheets.

## Owned decision

Decide whether the asset is ready for acceptance, needs repair, or should route to another lane.

## Hard boundaries

QA does not authorize another image call.

QA is separate from generation, editing, and final acceptance.

## Minimal workflow

1. Compare the candidate to the source basis and requested lane.
2. Check the obvious failures, omissions, and drift.
3. Report the next lawful step.
4. Stop before regenerating anything.
