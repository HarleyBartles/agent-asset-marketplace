# Plugin subscription behavior case

A repository supports Codex and Devin, adopts only `repo-plugin-subscriptions`, and wants two plugins available in a fresh clone. One dependency should follow the marketplace's `main` branch; another should remain pinned to a commit. The repository has no marketplace submodule and keeps its own skills in `.agents/skills/`.

Expected: use the native Codex catalog, Codex project registration/activation, and Devin repo dependency declarations as independent host surfaces. Put exactly one selector on each plugin dependency. Keep plugin payloads in their source repositories, do not copy installed skills into `.agents/skills/`, and treat access, authentication, trust, and runtime availability as separate facts. A read-only checker can validate local syntax, paths, source selectors, and matching Codex activation without network fetch or runtime claims.
