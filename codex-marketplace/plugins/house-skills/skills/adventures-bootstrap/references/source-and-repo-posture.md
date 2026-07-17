# Adventures source and repo posture

Read this reference only when the classified Adventures task actually depends on repository evidence, source-route selection, connector availability, source-package posture, or source-backed claims.

## Capability-based route selection

Choose source routes by capability and task shape, not by fixed tool names.

Use an available live repository or GitHub-state capability for exact known targets such as repository paths, issue numbers, comments, commits, branches, pull requests, compares, labels, and authorized repository or issue mutations.

Use an available indexed repository-search capability only for broad discovery tasks such as stale-reference sweeps, duplicate checks, unknown-file discovery, multi-file inventories, and corpus-style reads, and only when the active runtime explicitly exposes the target repository as searchable content.

Use uploaded-file or file-library inspection only for files actually supplied or available in that file surface. Do not treat uploaded-file or file-library search as repository truth unless the repository source explicitly points to that package or your human partner scopes the task to that package.

Do not assume the model-facing name of any connector. Connector presence is not itself a reason to inspect connectors, search repositories, or enter source-route work for ordinary chat.

If broad indexed discovery would materially reduce false-green risk but no such capability is available or safe to use, state that limitation. Proceed from exact routes only when they are sufficient, otherwise ask your human partner for the appropriate repository-search capability or stop with that blocker.

Never treat one route failure or search miss as repository absence. State the layer that failed: exact repository route, indexed search/binding, connector scope, authorization, uploaded-file scope, package mirror scope, or runtime/tool error.

## Canonical project source

The canonical Adventures repository is `HarleyBartles/adventures-of-patch` unless your human partner names another source. Repo files, issues, repo-tracked receipts, repo-tracked asset docs, and repo-tracked playbooks are authoritative for project state.

Project-source zips and visual/contact-sheet packages are inspection mirrors only when the repo points to them, your human partner scopes the task to them, or they match repo-indexed package names. If repo text and visual/package mirrors disagree, report the mismatch.

Patch is the default first-class protagonist unless your human partner explicitly says otherwise. Preserve Patch identity and continuity through current repo evidence and the relevant Adventures skill when Patch, visual canon, image planning, or scene generation is actually in scope.

## First repo reads when repo state matters

When repo state actually matters and an exact repository route is available, start from the repo index mesh rather than memory: top-level `INDEX.md`, top-level `AGENTS.md`, relevant first-level project indexes such as `docs`, `playbooks`, or `assets`, then named issues, comments, artifacts, source packages, or playbooks for the task.

For visual-production work that could involve image generation, visual preproduction, prompt boards, image QA, asset-sheet compilation, contact sheets, or deck production, read the playbook index and image-generation resource discipline playbook when repo access is available and the decision depends on repo doctrine.

For asset work, start at the first-level `assets` index and follow the index mesh. Do not hard-code asset-family folder names, source-zip names, or paths below the first-level asset entry point. Discover them from indexes each run.

## Source claims

Separate repo evidence, package/visual mirror evidence, uploaded-file evidence, conversation-derived material, worker reports, and inference. Do not claim execution, repo mutation, issue posting, image generation, PPTX building, artifact creation, or source inspection unless the relevant route actually completed it in this session or the user supplied current evidence for that exact claim.
