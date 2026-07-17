> Paths like `rooms-world/`, `rooms-pit/`, `rooms-manuscript/` refer to external repos in the Rooms-mostly ecosystem, not paths in this marketplace repo.

# Source routing

Use the narrowest relevant source first. Search is discovery; fetched or inspected files are grounding.

## Required file_search binding gate

For character investigations and sheet precursor packets, use bound `file_search` GitHub as the default first pass for
broad discovery. It should search across the relevant Rooms repos before relying on exact API reads.

If `file_search` is unavailable, unbound, or missing the relevant repo selection, stop and ask your human partner to bind/select the
needed GitHub repos. Name `rooms-world`, `rooms-pit`, `rooms-manuscript`, and `rooms-mostly` when broad character or
subject investigation is needed; include `will-workspace` only when wrapper/workspace governance is part of the task.

Only continue without `file_search` after your human partner explicitly confirms to proceed anyway. In that fallback mode, use live
GitHub API exact searches/reads and label the source set as narrower API-based discovery that may miss indirect insight,
transcript, manuscript-support, or adjacent room surfaces.

## First-pass character/world surfaces

For a named target, inspect:

- `rooms-world/Characters/INDEX.md`.
- the target character folder, sketch, and sibling files.
- sibling files such as `Voice.md`, `Sample Tweets.md`, alternate sketches, notes, relationship files, or target-local
  research files.
- related character sketches named by the target surface.

Do not rely only on keyword search. Once a character folder is found, expand the local surface family.

## Rooms, events, reputation patterns, and systems

Inspect room/system surfaces when the character file, your human partner, transcript search, or exchange material names rooms,
events, drama, reputation patterns, or room mechanics.

Common surfaces:

- `rooms-world/Rooms/**` for room sketches and room-local material.
- `rooms-world/Systems/**` for room mechanics, cross-room behaviour, exchange dynamics, externalised room games,
  timeline/room mechanics, and related systems.
- room aliases and predecessor/successor names supplied by your human partner.

For recall-sheet precursor work, search the subject by name, handle, persona, room names, event labels, reveal terms,
fallout terms, and the names of likely witnesses or affected
people.

## Transcripts

Treat rendered transcripts as first-class inspection surfaces for character investigation and recall-sheet precursors.
They can support room membership, room presence, relationship texture, DM texture, witnessed events, and who was present
for what.

Search bounded transcript areas by:

- handle, display name, persona name, and real name where appropriate;
- partner-named rooms and known room aliases;
- world-named rooms and predecessor/successor room names;
- exchange terms, reveal terms, fallout terms, and repeated public-thread terms.

Prioritize transcript headers, participant lists, room labels, date ranges, archive provenance, and surrounding room
context before message content when establishing membership or presence.

If headers expose unresolved numeric ids, do not reject the transcript solely because the handle is absent. Classify it
as candidate-only until identity can be confirmed by handle, participant list, room context, message content, or a
governed resolved account/entity ledger.

Do not run new extraction, parse raw archives, or mutate Pit under this Skill. Inspect existing rendered transcript
surfaces only.

## Insights

Inspect World/canon insight surfaces when searches find them or the target is linked to insight-heavy material.

Possible surfaces include:

- `rooms-world/Research/Insights/**`.
- World/canon insight ledgers and provenance maps.
- entity-room insight linkage registries.
- room insight registries or indexes.

Treat insight surfaces as rich character/relationship leads and developed interpretations. Do not silently convert them
into canon unless the surface explicitly has that authority.

## Exchange, epistolary, and manuscript-support

Search for participant-specific repeated correspondence or public back-and-forth artifacts with terms such as:

- `Dear <name>`.
- `Dear <handle/persona>`.
- display-name/persona labels.
- known exchange titles.
- named public games, reply chains, or correspondence forms.

When a target is linked to public letters, correspondence, externalised room games, or repeated
back-and-forth artifacts, inspect:

- `rooms-world/Research/Epistolary And Exchange Style Guide.md` or current style-guide equivalent.
- `rooms-world/Systems/Exchange Dynamics.md`.
- bounded `rooms-world/World/ManuscriptSupport/**` bridge/index surfaces.
- `rooms-manuscript` synopses when available and appropriate.
- loose structure, story-beat placement, and prose tension/manuscript-support surfaces when exchange or prose-bearing
  material is involved.

Use exchange material to understand sequence, reciprocity, public/private movement, recognition, address, recurring
jokes, and the character's role in the exchange. Preserve manuscript/provenance boundaries.

## Pit/archive/evidence

Use only bounded searches/surfaces relevant to the participant, handle, room, event, exchange, reveal, fallout, or
reputation pattern. Do not run new extraction or parse raw archive data.

Pit evidence remains provenance-bound archive/evidence. It does not write canon, decide narrative significance, or
resolve character meaning by density.

## Participant accounts and existing sheets

Inspect existing participant accounts, prompt sheets, sneak peeks, or recall sheets only when relevant to the target,
adjacent participants, or the requested downstream use.

Classify them as `participant-account-derived`. They are subjective, partial, emotionally useful, and
provenance-sensitive, not canon by default.

## Resolved account/entity ledger

Once a governed repo-resident resolved account/entity ledger exists, inspect it for stable ids, handles, display names,
persona names, platform ids, bio/profile text, links, follow/follow-back posture, high-level counts, resident
conversations, transcript ids, provenance, and freshness markers.

If the ledger is missing or incomplete, mark this as `unavailable` or `not checked`, not as absence of evidence.

## Partner narrative

Use your human partner's current framing as `partner-narrative`. It can identify rooms, names, relationships, sensitivities, and
hypotheses to investigate or preserve, but it is not repo truth by itself.

## Minimum source sets by output lane

Summary mode may use the smallest sufficient inspected source set, but must not make affirmative named Rooms claims
without bounded grounding when repo access exists.

Full-detail and sheet-precursor modes should inspect all materially relevant available families above.

For recall sheets, inspect both the subject and the likely respondent context when known.

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
