# Rooms source and repo posture

Load this reference only when the classified task needs Rooms or workspace governance repository evidence, source-route availability, repo-scope claims, issue or publication evidence, broad discovery, or diagnosis of source access.

## Capability-based route selection

Choose routes by capability and evidence need, not by fixed tool names.

Use an available live repository-state capability for exact known targets: issue threads, comments, file-by-path reads, commit or ref comparisons, pull request inspection, and authorized issue operations.

Use an available indexed repository-search capability only for broad discovery: semantic search, stale-reference inventory, corpus-style reads, unknown-file discovery, or repo-wide duplicate checks. Use it only when the active runtime explicitly exposes the relevant Rooms or workspace governance repositories as searchable source content.

Do not assume the model-facing name of any route. Do not treat uploaded-file or file-library retrieval as repository discovery unless the active source list explicitly exposes the target repository. Do not let the mere presence of a connector trigger source-route work for ordinary conversation.

If exact known-target reads can satisfy the task, proceed through an exact route and mark broad indexed discovery as not used. If broad indexed discovery would materially reduce false-green risk but no suitable route is available, ask for the appropriate repository-search capability or state the limitation before making broad claims.

Treat route failures and search misses as evidence about route coverage only, not proof of repo absence.

## Rooms repo scope reminders

Relevant repos are normally:

- `will-workspace` for workspace-level governance, GPT-wide skill surface, and cross-project policy.
- `rooms-mostly` for the Rooms wrapper, project-local governance, and submodule coordination.
- `rooms-pit` for Pit, archive evidence, provenance, ProjectDB-adjacent material, and archive custody.
- `rooms-world` for World, canon/world state, characters, systems, and ambiguity-preserving canon support.
- `rooms-manuscript` for Manuscript, prose/manuscript surfaces, sidecars, and draft support.

Treat `rooms-mostly` as wrapper visibility, not full-stack proof. Respect submodule pointers. Do not assume a child repo latest branch equals the wrapper-pinned state.

## Source partitioning

Track the source basis used for any claim:

- exact repository evidence;
- indexed repository discovery;
- uploaded source package or zip mirror;
- worker report;
- conversation-derived material;
- unavailable or uninspected source.

Do not infer repo structure from memory, session summaries, reports, zips, or old worker returns.
