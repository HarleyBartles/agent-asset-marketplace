---
name: rooms-source-partitioning
description: Label Rooms, Mostly claims by source basis and evidence state. Use when answers, reports, closure notes, doctrine takeaways, cleanup claims, or repo/canon/archive/manuscript assertions could blur inspected evidence, inference, conversation, reports, or unavailable sources.
metadata:
  source-id: rooms-source-partitioning
  source-path: plugins/house-skills/skills/rooms-source-partitioning/SKILL.md
  provenance-name: "MARK-9 chunk ledger \xC3\xA2\xE2\u201A\xAC\xE2\u20AC\x9D Rooms"
license: "MIT"
---
# Rooms Source Partitioning

Use this Skill to label what kind of support a Rooms, Mostly claim has and to prevent evidence from being laundered into a stronger truth lane.

`SKILL.md` is the control plane. It defines source-basis labels and partitioning posture. Do not select source routes or inspect connectors from this file alone.

## Reference loading

Load `references/source-route-labels.md` only when route capability matters, such as when the response must distinguish exact source reads, indexed search discovery, uploaded-file evidence, local evidence, unavailable routes, route failures, or source-coverage limits.

## Source-basis labels

- `verbatim`: directly quoted or copied from source.
- `source_fact`: directly stated by an inspected source.
- `partial`: source is incomplete or only partly inspected.
- `inferred`: reasoning from inspected evidence; not directly stated.
- `report-derived`: from a report or receipt; report is not underlying truth.
- `canon-derived`: from canon/world surfaces.
- `manuscript-derived`: from manuscript/prose surfaces.
- `conversation-derived`: from chat context, not canon, archive, or publication proof.
- `known-empty`: inspected and known absent or empty in scope.
- `unavailable`: source could not be accessed.
- `search-only`: found or not found by search only; not repo-grounded unless the located source content was inspected.
- `not repo-grounded`: no relevant repo file was inspected.

## Rules

Do not let a label launder a claim. If a response mixes evidence and synthesis, partition them explicitly.

Historical reports may preserve old paths as evidence of history, not active authority.

Do not infer global repo unavailability from one source route failing. Distinguish unavailable indexed discovery, exact source-read failure, permission failure, source-scope mismatch, and runtime/tool failure when route capability matters. Load the source-route labels reference for those cases.

## No-Shit / custody partitioning

When cleanup, anti-bloat, cold-store, governed-trash, or deletion claims appear, partition the source basis before accepting the claim. Separate current repo evidence, worker-reported local state, reports, receipts, manifests, conversation claims, inference, and unavailable source routes.

A report that something was deleted is not current-tree absence proof. A governed-trash sentinel is custody inventory, not deletion authority. A cold-store move preserves retained custody and must not be collapsed into cleanup success without source basis.

If protected archive, canon/world, manuscript, ProjectDB, machine-truth, publication-proof, or ambiguity-bearing surfaces are implicated, mark the claim as protected or routed rather than treating it as ordinary residue.

## Retrospective and doctrine-capture partitioning

When extracting lessons, doctrine proposals, or workflow followups, partition the source basis before making the takeaway. Separate commit or diff evidence, issue comments, worker returns, reports, receipts, conversation-derived material, current repo state, inference, and unavailable routes.

A commit message can be intent evidence, but not proof that validation ran. A worker return can describe local output, but remains reported unless corroborated by a source route. An issue comment can record closure posture, but does not by itself prove source-controlled state.

Use one or two evidence-grounded takeaways at most. If the inspected change is trivial housekeeping, label it as such rather than inventing a lesson.
