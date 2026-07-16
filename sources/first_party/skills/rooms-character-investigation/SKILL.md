---
name: rooms-character-investigation
description: Use when rooms character and subject investigations with source partitioning
  for prompt, peek, and recall handoffs.
metadata:
  source-id: rooms-character-investigation
  source-path: sources/first_party/skills/rooms-character-investigation/SKILL.md
  provenance-name: Rooms Character Investigation first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when rooms character and subject investigations with source partitioning
    for prompt, peek, and recall handoffs.
  use_when:
  - Use when rooms character and subject investigations with source partitioning for
    prompt, peek, and recall handoffs.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Rooms Character Investigation

Investigate Rooms, Mostly people, handles, rooms, events, reputation patterns, and community-impact subjects from
repo/source surfaces, then return a source-partitioned investigation packet.

This Skill owns broad repo lookup and source partitioning. It does not create participant sheets. Use
`rooms-sheet-creator` to turn the investigation packet into a participant-facing prompt, peek, or recall sheet.

## Required composition

Compose with these Skills when available:

- `rooms-project-doctrine` (source-partitioning reference) for source-basis separation.
- `base-doctrine` and `rooms-project-doctrine` for named Rooms character, world, canon, archive, room,
  narrator, actor, or repo-structure claims and the related truth-boundary references.
- `risk-gates` (rooms ambiguity gate) when identity, motive, authorship, witness status, archive gaps, relationship meaning,
  disappearance, room history, or emotional cost could be overresolved.
- `rooms-sheet-creator` after the investigation packet when your human partner wants a participant-facing sheet.

## Core workflow

1. Identify the target person, handle(s), display/persona names, room/event/drama/reputation subject, and downstream
   sheet lane when known.
2. Enforce the GitHub `file_search` binding gate before broad discovery.
3. Inspect source surfaces using `references/source-routing.md`.
4. Partition claims using the source-basis labels below.
5. Produce the requested investigation lane using `references/output-lanes.md`.
6. Include a handoff section for `rooms-sheet-creator` when the next step is a prompt, peek, or recall sheet.
7. If source access is partial, state what is unavailable rather than filling gaps from memory.

## GitHub source-route discipline

For character investigations and sheet precursor packets, bound `file_search` GitHub is the first-class route for broad
repo discovery. Use it for unknown-path searches, cross-repo character surface discovery, transcript and insight recall,
stale-pattern sweeps, and corpus-style reads across World, Pit, Manuscript, and wrapper surfaces.

Use live GitHub API routes such as `api_tool` only for exact file-by-path reads, issue/comment/PR/commit/ref operations,
remote-head checks, and authorized mutations after discovery has identified the relevant surfaces.

If `file_search` GitHub is unavailable, unbound, or missing the relevant repo selection, stop before the broad
investigation and ask your human partner to bind/select the relevant GitHub repos. Name the needed repos when known, normally
`rooms-world`, `rooms-pit`, `rooms-manuscript`, and `rooms-mostly`, plus `will-workspace` when wrapper or workspace
governance is relevant.

Do not silently fall back to the live GitHub API for broad discovery. Fall back to the narrower live API route only
after your human partner explicitly confirms to proceed anyway. When proceeding by fallback, state that the result is based on
narrower API spot checks and may miss semantically adjacent or indirect repo surfaces.

Search results are discovery, not final truth. Inspect the relevant file, issue, commit, or source surface before
making affirmative repo-grounded claims.

## Investigation lanes

Use these modes:

- `full_detail`: default for deep character/person/room/event/reputation work and required precursor for major sheet
  creation. Produce a dense source-partitioned investigation packet.
- `summary`: default when your human partner asks for a character summary or "what do we know about X?" without asking for deep
  detail.
- `sheet_precursor`: focused packet for `rooms-sheet-creator` when your human partner already knows the sheet lane.

Sheet lanes are not produced here. Use `rooms-sheet-creator` for:

- `prompt`: participant memory prompt sheet about the respondent's own participation.
- `peek`: participant-facing character-read preview about the respondent.
- `recall`: participant-facing memory sheet asking a respondent what they remember about another person, room, event,
  drama, reputation pattern, reveal, fallout, or community impact.

If the user asks directly for a sheet and the investigation is already done in the conversation, hand off the packet
summary to `rooms-sheet-creator`. If the investigation is not done, do the investigation first.

## Source basis labels

Use these labels explicitly when source basis matters:

- `world-derived`: character, room, system, or non-insight research surfaces from `rooms-world`.
- `insight-derived`: World/canon insight surfaces, registries, room/entity insights, or explicit insight files.
- `transcript-derived`: rendered Pit transcript surfaces, including group DM, one-to-one DM, and future DB-backed
  tweet-chain/public-thread transcripts.
- `exchange-derived`: public correspondence, letter/exchange style guides, exchange dynamics, manuscript-support
  bridges, manuscript synopses, or derived exchange documents.
- `pit-derived`: bounded archive/evidence outputs from `rooms-pit`.
- `participant-account-derived`: existing prompt sheets, recall sheets, sneak peeks, or participant accounts.
- `manuscript-derived`: manuscript surfaces or synopses not already covered by exchange-derived material.
- `ledger-derived`: governed resolved account/entity ledger surfaces once available.
- `partner-narrative`: your human partner's current framing, relationship knowledge, sensitivity guidance, or outreach context.
- `inferred`: GPT synthesis from inspected material.
- `candidate`: plausible but not confirmed by the inspected source set.
- `not checked` or `unavailable`: relevant surfaces not inspected or inaccessible.

Never let a label launder a claim into truth. Counts, transcript density, archive richness, participant accounts,
reports, or partner narrative do not become canon by being included in a character investigation.

## Sheet handoff contract

When the investigation will feed sheet creation, end with a compact handoff packet for `rooms-sheet-creator`:

- target subject and respondent, if different;
- intended sheet lane: `prompt`, `peek`, or `recall`;
- source partition and unavailable surfaces;
- participant-safe facts and memory anchors;
- candidate or inferred material that must remain tentative;
- sensitivity risks and hidden material that should not be exposed;
- recommended sheet emphasis;
- specific no-go phrasings or overleading risks;
- green path or questions your human partner must answer before drafting.

For recall sheets, also include direct/second-hand/later-reconstruction boundaries and any harm-bearing/need-grounded
analysis that may shape the questions.

## Hard boundaries

- Do not simulate canon, archive, manuscript, project-local, or workspace governance lanes, or participant voices.
- Do not mutate repos from chat under this Skill.
- Do not draft or persist prompt, peek, or recall sheets under this Skill.
- Do not run new archive extraction or parse raw archives; inspect existing rendered/source-controlled surfaces only.
- Do not treat manuscript material as canon or participant testimony.
- Do not treat participant accounts as canon by default.
- Do not treat conversation or partner narrative as repo truth.
- Do not expose sensitive archive/transcript details in participant-facing handoff content unless your human partner explicitly
  approves.
