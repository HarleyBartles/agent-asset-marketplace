# Repo and connector posture

`HarleyBartles/adventures-of-patch` is canonical project truth.

For known paths, issues, comments, commits, and writes, prefer the live GitHub API connector. Do not expect
search/index connector binding during bootstrap. A search/index miss, repository-selection error, or binding failure
is not evidence that GitHub is unavailable.

Before claiming repo access is blocked, try a live API known-path or known-issue read and record the exact result.

Use repo indexes before repo-content claims:

1. `INDEX.md`
2. `AGENTS.md`
3. `docs/project/INDEX.md` when relevant
4. relevant directory `INDEX.md` files
5. named issue/comment/artifact

Search/index can help discovery after direct access is established, but it is not the source of availability truth.
