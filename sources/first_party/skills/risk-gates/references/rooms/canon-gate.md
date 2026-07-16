# Rooms Canon Gate

Use this gate to test canon pressure in Rooms, Mostly. The canon gate protects coherence, not tidiness: do not flatten useful ambiguity, narrator limitation, archive gaps, or layered truth merely because an item is uncomfortable.

## Scope

This gate is Rooms-only. It does not answer generic continuity questions for other projects.

Use `rooms-project-doctrine-v1` for Rooms truth boundaries, `rooms-source-partitioning-v1` to separate evidence classes, the rooms ambiguity gate when the right outcome is to preserve unresolved identity or motive, and `linear-issue-shaping-v1` when a canon-safe next step turns into Linear issue readiness, worker-shaped issue status handling, external handoff text when explicitly requested, or GitHub proof handoff after a PR/branch/commit exists.

Use the GPT-wide gate framework pattern. Run internally when there is one lawful path. Switch to interactive queue mode when Harley must decide a real creative/canon tradeoff.

## What the Canon Gate Tests

Given an item under discussion, test whether it:

- fits established Rooms canon;
- conflicts with established canon;
- exposes a gap in canon;
- belongs to another truth layer rather than canon;
- should cause the item, canon, or both to move;
- should remain unresolved because ambiguity is part of the book.

The canon gate may be used before dispatch planning, during conversation, before persistence, when reviewing manuscript/world claims, or when converting archive/conversation material into candidate world state.

## Source Ladder

Prefer current repo evidence over memory.

1. Machine truth when relevant and available, especially locked append-only truth surfaces.
2. Rooms project doctrine, source ledger, bundle/source map, and reviewed Rooms source surfaces.
3. Reviewed source surfaces accepted by Rooms as project basis.
4. Manuscript surfaces as manuscript state only, not world truth unless Rooms says so.
5. Pit/archive evidence as evidence only, not canon by itself.
6. Reports and receipts as reports, not truth.
7. Conversation-derived material as candidate pressure only, not canon.
8. Structured memory as fallback or retrieval aid when repo grounding is unavailable or explicitly not required.

If repo access is available, inspect the smallest sufficient Rooms surfaces before declaring a canon conflict. If unavailable, mark the pass not repo-grounded.

## GitHub source-route discipline

Before repo-dependent judgment, identify the available source route. Use repo-local and GitHub-backed discovery routes for broad repo search, exact issue threads, comments, file-by-path reads, commit and ref comparison, PR details, and authorized mutations.

Search results are discovery, not final truth. Inspect the relevant file, issue, commit, or source surface before making affirmative repo-grounded claims.

## Compose With Existing Rooms Skills

Use or defer to:

- `rooms-project-doctrine-v1` for source routing, truth boundaries, publication, and report hygiene;
- `rooms-source-partitioning-v1` to separate evidence, report, synthesis, inference, missing data, and conversation-derived material;
- the rooms ambiguity gate when identity, motive, authorship, witness status, narrator knowledge, reconstruction, or disappearance could be overresolved;
- the rooms analogy gate when analogy is doing too much work;
- the rooms zoom-outs gate when the full frame is getting lost;
- `rooms-character-investigation-v1` for broad source lookup and source-partitioned investigation packets;
- `rooms-sheet-creator-v1` for prompt, peek, and recall sheet creation from durable packets;
- `rooms-image-sidecars-v0.1` for image evidence starter packets before Albert/Pit ingestion;
- `linear-issue-shaping-v1` for Linear worker issue readiness, worker-shaped issue status handling, external handoff text when explicitly requested, and GitHub proof handoff after a PR/branch/commit exists.

## Canon pressure types

Use these pressure types to classify gate items.

- `direct_conflict`: the item contradicts established Rooms canon.
- `gap`: canon has no settled answer and the item may fill or expose that gap.
- `ambiguity`: the item touches an intentionally unresolved identity, motive, witness, authorship, disappearance, or narrator question.
- `layer_mismatch`: the item belongs to archive evidence, report, manuscript state, character belief, memory, inference, or conversation rather than canon.
- `terminology_mismatch`: the apparent conflict comes from using a term differently across surfaces.
- `no_conflict`: the item fits existing canon.

Do not classify by vibes alone. Inspect source surfaces when available.

## Green Outcomes

A green outcome is not always "no conflict." The canon gate can go green through more than one route. Valid green outcomes include:

- `green_no_conflict`: the item fits current canon.
- `green_item_modified`: modify the item to fit established canon. Use when established canon is stronger and the item can be adjusted without losing its purpose.
- `green_canon_update_recommended`: keep the item and route a Rooms canon update. Use when the item is stronger or newer Harley or Rooms intent should move the world state. This requires lawful Rooms routing before claiming canon changed.
- `green_both_update_recommended`: adjust both item and canon through lawful routing. Use when the item reveals a better shape but both the item and the existing canon surface need revision.
- `green_layer_partitioned`: the item is valid in another layer, not canon. Use when the item is valid in another layer: archive evidence, report, manuscript unreliability, character belief, narrator limitation, working theory, or conversation candidate.
- `green_ambiguity_preserved`: the apparent conflict is intentionally unresolved and should not be collapsed. Use when resolving the conflict would flatten intended uncertainty.

When relevant source surfaces are unavailable or the evidence chain is insufficient, defer pending evidence rather than forcing a green.

GPT may recommend canon modification, but GPT does not directly change canon in chat. Canon changes route through Rooms authority.

## Amber, Red, and Blocked

Use `amber_harley_decision_needed` when a real creative or canon choice remains.

Use `amber_repo_grounding_needed` when relevant Rooms surfaces must be inspected before judgment.

Use `red_domain_violation` when the item tries to canonize archive evidence, reports, conversation, manuscript state, or inference without lawful route.

Use `blocked_source_unavailable` when required canon sources are unavailable and the pass cannot be responsibly completed.

## Internal Mode

Resolve internally when only one lawful path exists.

Examples:

- If archive evidence is being treated as canon, partition it as evidence or candidate instead of asking Harley.
- If a contradiction is only a character belief or narrator limitation, preserve the layer rather than forcing world-canon repair.
- If a repo-backed Rooms move has one lawful route, take it directly rather than turning it into a queue.

Do not show a gate queue for one-path corrections unless Harley asks to see the reasoning.

## Interactive Queue Mode

Use interactive mode when Harley must choose among legitimate canon paths. Present up to five items at a time by default. Harley may blanket approve GPT recommendations with "go," "proceed," "accepted," "agreed," a thumbs-up, or similar positive affirmation.

Default to at most five visible items. For each item, show:

1. Item under discussion.
2. Canon pressure.
3. Source basis checked.
4. Risk if unresolved.
5. GPT recommendation.
6. Decision needed to go green.

Suppress items with only one lawful path. Internally repair those before output.

Accept blanket approval for all visible GPT recommendations when Harley says "go," "proceed," "accepted," "agreed," gives a thumbs-up, or uses similar affirmative language.

Queue item shape:

```yaml
item:
  id: "C1"
  item_under_discussion: ""
  established_canon_pressure: ""
  source_basis_checked: []
  conflict_type: "direct_conflict | gap | ambiguity | layer_mismatch | terminology_mismatch | no_conflict"
  green_paths:
    - "modify_item"
    - "modify_canon"
    - "modify_both"
    - "preserve_boundary"
    - "preserve_ambiguity"
    - "defer_pending_evidence"
  gpt_recommendation: ""
  decision_needed: ""
```

Keep queue items brief and actionable.

## Boundary Rules

Do not let the canon gate become a continuity cop. Rooms uses fragmented records, degraded memory, narrator limitation, hidden rooms, partial archive evidence, and unresolved identity or motive questions.

Do not modify established canon just because a new item is attractive. Do not reject a strong new item just because current canon can lawfully move.

Do not treat archive richness as character importance. Do not treat conversation as canon. Do not treat reports as truth. Do not let manuscript convenience decide world state.

When the right outcome is "we do not know," keep it unknown.
