# Output lanes

Choose the lane that matches the user's ask. If unsure, use `summary` unless the result will feed sheet creation,
dispatch, canon review, or major character decisions.

## Full detail lane

Use this for deep character, participant, room, event, reputation, or community-impact work. It is the normal precursor
for `rooms-sheet-creator-v1` when the subject is important, existing, sensitive, or harm-bearing.

Recommended sections:

1. Target and scope.
2. Source partition.
3. Confirmed identity/profile/account facts, including ledger state if available.
4. World character model or subject model: role, traits, contradictions, principles, and story function,
   source-labelled.
5. Public voice and timeline behaviour, if relevant.
6. Room voice, private/DM register, or event/reputation context.
7. Rooms and room lineage: confirmed, candidate, Harley-named, and unresolved.
8. Transcript evidence and transcript candidates, with identity confirmation state.
9. Key relationships, orbits, witnesses, and affected people.
10. Exchange/epistolary/public-thread surfaces.
11. Insight surfaces and developed interpretations.
12. Pit/archive/evidence surfaces and limits.
13. Manuscript/support surfaces and provenance limits.
14. Harley narrative and hypotheses.
15. Open ambiguities and missing surfaces.
16. Character or subject risks: overread, flattening, canon leakage, source gaps, participant sensitivity.
17. Sheet handoff implications for `prompt`, `peek`, or `recall`, if relevant.

Use compact subsections when the source set is light. Do not invent detail to fill the template.

## Summary lane

Use for normal character or subject summaries.

Recommended shape:

- one paragraph on who or what the subject is and the current source basis;
- one to three paragraphs on role, voice, relationships, rooms, impact, and open questions;
- a brief source-boundary note if material is mixed or uncertain.

Do not include a long audit trail unless Harley asks. Do include enough caveat language to avoid treating conversation,
reports, or participant accounts as canon.

## Sheet precursor lane

Use when Harley asks for a prompt, peek, or recall sheet and the job is to prepare the investigation packet.

Return a concise but sufficient packet for `rooms-sheet-creator-v1`:

- `sheet_lane`: `prompt`, `peek`, or `recall`.
- `respondent`: who the sheet is for.
- `subject`: who or what the sheet is about; for prompt and peek this may be the respondent.
- `source_partition`: inspected sources by basis label.
- `unavailable_or_not_checked`: relevant missing surfaces.
- `memory_anchors`: names, rooms, events, relationships, or motifs that can safely prompt memory.
- `hidden_or_sensitive_material`: source claims or interpretations that should stay behind the scenes.
- `candidate_material`: plausible material that must not be stated as fact.
- `recommended_shape`: suggested emphasis for the sheet creator.
- `risks`: overleading, flattening, defence capture, archive-case-file tone, or participant pressure.

## Prompt handoff guidance

For a `prompt` sheet, hand off memory veins about the respondent's own participation. Translate source findings into
open prompts, not conclusions. Keep characterisation and structural interpretation behind the scenes unless Harley
explicitly approves.

## Peek handoff guidance

For a `peek` sheet, hand off participant-safe character-read statements and correction risks. Do not hand off full room,
DM, exchange, conflict, or event prompt material. A peek lets the participant sanity-check the current read of them; it
does not ask them to reconstruct the era.

## Recall handoff guidance

For a `recall` sheet, hand off what the respondent might remember about another person, room, event, drama, reputation
pattern, reveal, fallout, or community impact.

Preserve these boundaries:

- direct experience;
- heard at the time;
- rumour;
- later reconstruction;
- current interpretation;
- unavailable or not checked.

For harm-bearing or antagonistic subjects, use the need-grounded frame: need is not excuse. Need explains function, not
innocence. Do not ask the respondent to relitigate whether well-evidenced actions happened. Ask what the behaviour did
for the subject, what need it fulfilled, what room/social mechanism made it possible, who noticed earlier, what was
minimised, and what changed after fallout.
