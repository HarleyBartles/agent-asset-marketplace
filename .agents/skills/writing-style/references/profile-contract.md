# Writing profile contract

Use this contract when authoring, reviewing, or consuming profile data below
`references/profiles/`. Profile data supports inspectable style judgments; it
does not classify authorship.

## Profile identity and lifecycle

Each profile has one stable lowercase hyphenated `profile_id`, a semantic
`version`, and dated review metadata. A fatigue pattern has its own stable ID,
`status` (`active`, `retired`, or `rejected`), `reviewed_at`, and
`review_after`. Evidence strength and lifecycle status are separate.

Only active patterns belong in ordinary runtime guidance. Retired and rejected
records may remain in the evidence package to preserve decisions. After
`review_after`, an observation may still be shown, but an automated
recommendation must become `candidate` or `abstain` until a human review renews
or changes the record.

## Pattern record

Each record declares:

- `id`, `family`, `version`, and `status`;
- `rationale`: the audience/context concern, not an authorship claim;
- `observable_signals`: inspectable lexical, structural, cadence, or density
  signals that gain meaning only as a cluster;
- `contextual_threshold`: unit, minimum count, minimum distinct signals, and a
  decision rule;
- `evidence_class` and `source_ids`;
- `scope` and `limitations`;
- `preserve_conditions` and `repair_guidance`;
- review dates and linked golden case IDs.

The allowed evidence classes are `well_supported_reader_fatigue`,
`plausible_emerging`, `author_specific_preference`, and
`weak_or_folk_heuristic`. They describe support for the operational concern,
not the probability that text was generated.

## Finding result

Return one or more bounded findings:

| Type | Meaning |
| --- | --- |
| `observed` | A declared deterministic signal or threshold is present. |
| `candidate` | Contextual review is required before changing prose. |
| `preserve` | A legitimate or authorised use should remain. |
| `repair` | Context and current evidence support a smallest change. |
| `abstain` | Evidence or context cannot support a decision. |

Each finding must identify the profile and pattern IDs, observed evidence,
audience/context scope, rationale, preserve condition, limitation, and smallest
repair. A phrase match can produce `observed`; by itself it cannot produce
`repair`.

## Golden coverage

Every active fatigue pattern has at least one `repair`, one `preserve`, and one
contextual `abstain` case. Goldens name expected finding types and pattern IDs,
test clusters rather than isolated tokens, preserve legitimate devices, and
protect clarity and authorised voice. Fixtures must be synthetic or explicitly
approved for repository publication.

## Prohibited semantics

Profiles must not contain exact-token bans, forbidden-word lists, detector or
evasion scores, authorship probabilities, identity claims, or instructions to
degrade prose. Voice cards must not retain source prose or a private corpus.
