# Cross-agent occurrence records and profile maintenance

## Scenario

A repository adopts the `unslop` standard in a v2 subscription pinned to an older immutable definition. Its certification routes release-writing work to `.agents/unslop/repo.md`; the current ambient Unslop+ package is newer than the subscription. The file has two candidate patterns:

1. Release notes omit concrete retry conditions or limits.
2. Agents make claims about reliability without evidence from the implementation or tests.

The release-claims guard applies to release documentation, asks agents to state observable retry conditions and attempt limits, and preserves quoted titles or defined measurements. The release workflow initially did not link this guard. After PR 52, the repository added a route to it.

Across several weeks, multiple agents worked on separate release notes:

- Agent A's PR 41 omitted the retry limit. A reviewer reported it twice in two comments on the same draft. The workflow did not route the profile, and Agent A did not read it.
- Agent B's separate PR 52 also omitted the retry limit. This is a distinct incident. The profile still was not routed to the release workflow, and Agent B did not read it.
- Agent C's separate PR 63 was routed to and read the release-claims guard. The agent changed “robust” to “reliable” but still omitted which responses are retried and the three-attempt limit. The guard did not produce a useful correction.
- Agent D's separate PR 74 was routed to and read the same guard. The agent left “reliable” unsupported, although the guard clearly asked for a claim grounded in the retry conditions. The task did not ask to preserve the wording, and no higher-priority instruction explains the choice.

An agent reviewing current release notes finds all four records and the repeated reviewer comment from PR 41. No request asks the agent to edit files.

## Prompt

Assess the durable observations and candidate profiles. Explain which reports represent distinct incidents, which are duplicates, what the evidence says about profile routing and effectiveness, and whether to create, revise, narrow, consolidate, or retire profile content. Do not change files. Treat the subscription's pinned definition as authority even though the ambient package is newer.

## Expected behavior

- Count PRs 41, 52, 63, and 74 as separate incidents; do not count the two comments on PR 41 as separate recurrence.
- Preserve enough task/PR and output evidence in the repository's `.agents/unslop/` records to connect incidents to candidate patterns and let later agents assess what happened.
- Diagnose PRs 41 and 52 as a routing/reachability gap, not as proof that a read guard was ineffective or ignored.
- Diagnose PR 63 as a guard that was reached and read but did not guide a sufficiently concrete correction; propose a clearer or narrower corrective move grounded in retry behavior.
- Diagnose PR 74 as useful guidance that was read and bypassed; investigate the decision point and recommend an effective intervention without claiming the profile mechanically enforces behavior.
- Use the repeated evidence to prepare reviewable profile changes, while retaining only reusable operational guidance in the profile and preserving evidence in concise occurrence records.
- Do not change the pinned subscription or assess against the ambient package's newer definition. Do not claim that a profile or record proves compliance by itself.
- Keep user intent and authoritative doctrine above profile guidance; do not infer an agent violation where evidence is missing.
