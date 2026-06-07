---
name: marketplace-family-doctrine-v1
description: First-party doctrine for classifying large upstream Claude Code skill families into repo-owned marketplace guidance without relabeling upstream source or activating broad packs by default.
---

# Marketplace Family Doctrine v1

Use this skill when a large upstream Claude Code surface needs to be turned into
first-party marketplace doctrine instead of being mirrored wholesale.

## Owned decision

Classify each family into one of four durable outcomes:

- first-party concept adaptation;
- mirror/vendor custody;
- pass with reason;
- intentional final park with evidence.

For MARK-46 and MARK-59 work, prefer first-party concept adaptation when the
upstream family is broad, repetitive, or better expressed as repo-owned
operating doctrine than as a literal copy of the upstream tree.

## Hard boundaries

- Do not relabel upstream source as Harley-owned.
- Do not treat a permissive license as a reason to mirror everything by default.
- Do not use analysis, inventory, or candidate lists as the final answer.
- Do not invent follow-up issues to avoid classifying usable surfaces.
- Do not assume raw upstream skill text is a durable marketplace asset when a
  compact first-party doctrine captures the same reusable consequence.

## Progressive references

- Read `references/source-basis.md` for the upstream commit, inspected source
  paths, and local repo conventions used to ground this doctrine.
- Read `references/family-outcomes.md` for the family-by-family outcome matrix.

## Minimal workflow

1. Confirm the upstream family set and the pinned source basis.
2. Decide whether the useful consequence is a mirror, a first-party doctrine
   adaptation, a pass, or a final park.
3. Record the reason in the family matrix.
4. Preserve the consequence in repo-owned source, not just in a note.
5. Stop once the outcome is durable and reviewable in-repo.

## Result shape

This skill is intentionally small. It exists to route mixed upstream families
into a single first-party doctrine surface that future workers can reuse without
re-reading the upstream pack catalog.
