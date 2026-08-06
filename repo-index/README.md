# Repo Index

`repo-index/` is the boring navigation surface for this repository.

The index exists so agents can traverse the repo without depending on chat
memory, embeddings, or a separate discovery runtime. It records the main repo
zones, the nearest scoped `AGENTS.md` file where one exists, and the protected
marketplace plugin pack surfaces that matter for validation and review.

## How to use it

- Start with `repo-index/repo-index.json` when you need a compact map of the
  repo.
- Regenerate the index with `py -3 tools/generate_repo_index.py` before
  validating when marketplace roots change, and use
  `py -3 tools/generate_repo_index.py --check` to prove the checked-in file is
  current.
- Use the `zones` entries to find the nearest guidance file and the right
  validation or generation hook for a path.
- Use the `marketplace_plugins` entries to jump from a protected plugin name
  to the plugin manifest, license evidence, bundle manifest, skills path, and
  known provenance references.
- The canonical repo unslop profile lives at `.agents/docs/unslop/profile.md`.
- Treat the index as navigation metadata only. It helps you find repo truth;
  it does not replace manifests, ledgers, provenance files, or the files on
  disk themselves.

## Scoped AGENTS mesh

The repo relies on the closest applicable `AGENTS.md` file for review and
worker guidance. The scoped files added for this issue are meant to keep
reviewers focused on path-specific failures such as manifest drift, missing
support files, false source claims, and vendor-custody changes that need an
explicit reason.

## RAG readiness

This index is intentionally simple so it can later feed corpus preparation,
search, or retrieval pipelines. It is a source-map and traversal aid, not a
semantic database. Future RAG work should build from the same file paths and
provenance records that this index already records.

## Validation

Keep the index current with:

- `py -3 tools/generate_marketplace.py --check`
- `py -3 tools/generate_repo_index.py --check`
- `py -3 tools/validate_marketplace.py`
- `py -3 tools/generate_repo_index.py`
- `py -3 tools/validate_repo_index.py`
- `py -3 tools/update_skill_artifacts.py --all`
- `py -3 tools/project_skills.py --check`

If the repo index changes, the validator should fail on stale paths or missing
guidance files before the change can be treated as complete.
