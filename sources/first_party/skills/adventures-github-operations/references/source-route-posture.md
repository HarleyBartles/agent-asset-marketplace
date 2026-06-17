# Source route posture

Load this reference only when verification depends on repository/source evidence, route coverage, connector availability, exact source reads, broad discovery, local evidence, or a route failure.

## Capability-based route choice

Choose by evidence need and active runtime capability, not by fixed tool name.

Use an available live repository-state capability for exact current-state checks such as issue state, comments, pull requests, commits, files by known path, refs, branches, labels, closure state, remote heads, comparisons, and authorized GitHub mutations.

Use an available indexed repository-search capability only for broad discovery such as stale-reference sweeps, duplicate hunts, multi-file inventories, unknown-file discovery, codebase-wide checks, and cited corpus-style reads, and only when the active runtime explicitly exposes the target repository as searchable content.

Use local or disk evidence only when a lawful local route is actually available. In chat-only verification, treat clean worktree and local path claims as worker-reported unless independently observable.

Do not assume the model-facing name of any connector. Do not assume that a file-search or uploaded-file route is repository search unless the active source list explicitly exposes the target repository. Connector, file, source, or tool presence is not itself a task signal.

## Route failure posture

Do not treat one route failure as source absence. State which layer failed or was unavailable:

- exact live repository-state capability;
- indexed repository-search capability;
- connector scope or binding;
- authorization;
- local/disk access;
- runtime/tool error.

If exact source reads are sufficient, proceed from exact routes even when indexed discovery is unavailable, and mark broad-search coverage as limited.

If broad indexed discovery is required for a closure or GREEN judgment and no suitable capability is available, mark the judgment AMBER or BLOCKED and name the missing capability instead of pretending spot checks were a broad audit.

## Reporting route coverage

When route coverage matters, report the capability class used rather than a hard-coded tool name. Examples:

- `exact_repository_state`: issue thread, known file, commit, PR, ref, or compare inspected.
- `indexed_repository_search`: broad discovery across searchable repo content inspected.
- `local_source`: lawful local file or working tree inspected.
- `reported_only`: worker or conversation claim only; not independently verified.
- `unavailable`: required route capability was absent, failed, or not authorized.
