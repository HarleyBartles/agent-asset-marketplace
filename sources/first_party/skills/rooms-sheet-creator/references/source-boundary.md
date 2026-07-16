# Source boundary

`rooms-sheet-creator` should normally consume a `rooms-character-investigation` packet instead of doing broad repo
lookup itself.

If broad discovery is missing, route back to `rooms-character-investigation`.

## Required file_search binding gate

For broad repo discovery feeding prompt, peek, or recall sheets, bound `file_search` GitHub is first-class. If it is
unavailable, unbound, or missing the relevant repo selection, stop and ask your human partner to bind/select the needed GitHub repos
before broad investigation. Normally request `rooms-world`, `rooms-pit`, `rooms-manuscript`, and `rooms-mostly`; include
`will-workspace` only when wrapper/workspace governance is relevant.

Only continue without `file_search` after your human partner explicitly confirms to proceed anyway. In fallback mode, use live
GitHub API exact searches/reads through the relevant connector and label the source set as narrower API-based discovery
that may miss indirect insight, transcript, manuscript-support, or adjacent room surfaces.

## Small exact reads

This Skill may perform small exact reads when the investigation packet names a template, style guide, lane index, or
specific existing sheet. Do not turn that into broad rediscovery.
