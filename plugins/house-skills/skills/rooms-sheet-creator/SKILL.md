---
name: rooms-sheet-creator
description: create Rooms prompt, peek, and recall sheets from character-investigation packets.
metadata:
  source-id: rooms-sheet-creator
  source-path: plugins/house-skills/skills/rooms-sheet-creator/SKILL.md
  provenance-name: "MARK-9 chunk ledger \xC3\xA2\xE2\u201A\xAC\xE2\u20AC\x9D Rooms"
license: "MIT"
---
# Rooms Sheet Creator

Create participant-facing Rooms sheets from a `rooms-character-investigation-v1` packet and Harley's approved direction.

This Skill owns sheet creation. It does not own broad repo lookup, character investigation, canon decisions, archive
extraction, or manuscript drafting.

## Source route discipline

Use bound `file_search` GitHub for broad repository discovery, stale-pattern sweeps,
and indexed corpus reads when it is available and relevant. Use live GitHub API
routes such as `api_tool` for exact issue, comment, file, commit, compare, and
authorized mutation operations.

If `file_search` is not bound and broad repo discovery would materially reduce
risk, ask Harley to bind the relevant GitHub connector before continuing, or state
that the pass is operating from narrower live API spot checks. Do not treat an
unbound `file_search` route as repo absence when another live GitHub route works.

## Sheet lanes

Use these lane names:

- `prompt`: participant memory prompt sheet about the respondent's own participation.
- `peek`: participant-facing character-read preview about the respondent.
- `recall`: participant-facing memory sheet asking a respondent what they remember about another person, room, event,
  drama, reputation pattern, reveal, fallout, or community impact.

If Harley asks for a character investigation, summary, or source scan rather than sheet text, route to
`rooms-character-investigation-v1` first.

## Required composition

Compose with these Skills when available:

- `rooms-character-investigation-v1` for broad repo lookup and the required source-partitioned precursor packet.
- `rooms-source-partitioning-v1` when source basis or uncertainty must be restated in the creation step.
- the `domain-truth-boundaries` reference under `rooms-project-doctrine-v1` before using world, archive, transcript,
  manuscript, participant-account, report, or Harley-narrative material in participant-facing text.
- `rooms-ambiguity-buster-v1` when memory, motive, identity, witness status, harm, disappearance, or fallout could be
  overresolved.

## Core workflow

1. Identify the requested lane: `prompt`, `peek`, or `recall`.
2. Confirm there is a sufficient `rooms-character-investigation-v1` packet. If not, run or request that investigation
   first. Do not redo broad repo lookup inside this Skill.
3. If broad discovery is unexpectedly needed, enforce the `file_search` binding gate in `references/source-
boundary.md`.
4. Read the lane rules in `references/sheet-lanes.md`.
5. Draft participant-facing text from the investigation packet and Harley's instructions.
6. Keep source evidence behind the scenes unless Harley explicitly approves exposing it.
7. If Harley approves persistence, use only the governed direct-landing lanes in `references/direct-landing.md`.

## Investigation packet requirement

For important, existing, sensitive, or harm-bearing subjects, do not draft from memory alone. Use a packet from
`rooms-character-investigation-v1` containing:

- respondent and subject;
- intended sheet lane;
- source partition and unavailable surfaces;
- memory anchors safe to expose;
- hidden or sensitive material to keep behind the scenes;
- candidate material that must not be stated as fact;
- recommended sheet emphasis;
- risks and no-go phrasings.

If Harley explicitly asks to proceed without a fresh packet, state the limitation before drafting.

## Participant-facing rules

All lanes must be plain, permissive, and non-forensic. The sheet should make memory or correction easier, not
narrower.

Do not:

- claim canon, evidence, or testimony status;
- present repo, archive, transcript, or DB material as a case file;
- ask a participant to verify source evidence;
- expose hidden structural or thematic interpretation unless Harley approves;
- pressure the respondent to answer every section;
- launder rumours, participant accounts, Harley narrative, or inference into truth;
- simulate the respondent's voice.

## Direct-landing summary

Prompt and peek lanes already have governed GPT direct-landing exceptions in World research surfaces. Recall may be
created in chat, but do not persist recall sheets until a repo-resident recall lane or explicit Harley-approved write
surface exists.

Use `references/direct-landing.md` for exact path limits before any repo mutation.

## Output

For drafts, return only the sheet text plus a short source-boundary note when helpful. Do not include hidden source
analysis inside participant-facing text.

For persistence, report the created/updated path, commit, and navigation update. Stay inside the allowed lane.
