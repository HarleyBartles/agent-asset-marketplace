# Consumer profile discovery and pinned authority

## Scenario

The repository explicitly adopts `unslop`. Its subscription record and certification give the current route to consumer profiles. The repository has no Writing Pack installation. The generic technical-writing profile is available in Unslop+.

Two consumer subscription shapes exist in separate test fixtures:

- **v1 fixture:** `.agents/contracts/unslop.json` declares `.agents/unslop` as a profile root, matching the historical deployed definition. The `release-claims` profile applies to release and migration documents. It guards unsupported reliability claims, asks for observable limits, and identifies quoted titles and defined measurements as false positives.
- **v2 fixture:** `.agents/contracts/operating-standards.json` pins an older immutable `unslop` definition at `skills/unslop/references/standard.md`; the certification routes agents to `.agents/unslop/repo.md`. There is no `.agents/contracts/unslop.json`. The repo.md content has the same scoped release-claims guard, while the currently installed ambient definition is newer.

In either fixture, the draft release note says: “The retry change is robust and simple.” The implementation retries timeouts and HTTP 502 responses up to three times, and returns authorization errors immediately. A linked standards document is titled “Robust Repository Recovery”.

## Prompt

Review the release note in each fixture for accuracy and clarity. Return a suggested replacement and explain the evidence for each correction. State which authority and consumer profile route you use. Do not change files.

## Expected behavior

- In v1, follow the pinned historical definition and its deployed `.agents/contracts/unslop.json` resource; do not replace it with today's contract or current standard.
- In v2, read the exact immutable definition and its named certification through `repo-standards`, then follow the repository's route to `.agents/unslop/repo.md`; do not require or infer `.agents/contracts/unslop.json`.
- In each fixture, read the matching consumer profile before applying it and read/apply the generic technical-writing profile too if its trigger fits; preserve the separate scope and authority of each profile.
- Ground the recommendation in the release note and retry behavior. Replace unsupported “simple” and make “robust” specific to retry limits rather than mechanically deleting it.
- Preserve “Robust Repository Recovery” as a source title. Do not claim the missing Writing Pack blocks the review.
- Do not update the subscription or use the currently installed definition to redefine either fixture's authority.
