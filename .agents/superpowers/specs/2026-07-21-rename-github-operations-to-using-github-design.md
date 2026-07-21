# Rename github-operations to using-github and restructure as a tool-router skill

## Goal

Rename the first-party skill `github-operations` to `using-github` and restructure it to mirror `using-linear`: a top-level `SKILL.md` router that maps task intents to focused reference docs, plus a complete `references/surface-map.md` catalog of every callable GitHub surface (MCP server, `gh` CLI, GitHub REST API, GitHub GraphQL API) with per-intent guidance.

## Scope

- Source custody under `sources/first_party/skills/github-operations/` moves to `sources/first_party/skills/using-github/`.
- The skill body is rewritten as a router: frontmatter, `SKILL.md` intent table, `agents/openai.yaml`, `intake.json`, `decisions.json`, `decisions.md`, and reference docs.
- Reference docs follow the `using-linear` pattern:
  - `references/read-discover.md`
  - `references/pull-requests.md`
  - `references/reviews.md`
  - `references/issues-comments.md`
  - `references/commits-branches.md`
  - `references/mutations.md`
  - `references/graphql.md`
  - `references/gh-cli.md`
  - `references/mcp-surface.md`
  - `references/surface-map.md`
- `sources/first_party/skills/github-operations/` is removed.
- Non-generated source references to `github-operations` are updated to `using-github`.
- Generated/projection surfaces are refreshed through `py -3 tools/rebuild_marketplace.py`.

## Non-goals

- No change to the underlying GitHub tool capabilities; only guidance and routing.
- No new first-party skill beyond the rename/restructure.
- No edits to historical plans/specs or generated market artifacts by hand.

## Contract

- `name` in `SKILL.md` frontmatter becomes `using-github`.
- `metadata.source-id`, `metadata.source-path`, and `metadata.provenance-name` derive from the new name and path.
- `codex-marketplace/custody-pack-registry.json` entries and `source_ledger` list `using-github` with `canonical_source_path` `sources/first_party/skills/using-github` and `local_path` `skills/using-github`.
- Source files referencing `github-operations` by skill name are updated (`repo-worker-base`, `house-skills`, `bootstrap-router`, `inspecting-the-environment`, `risk-gates`, `base-doctrine`, `wild-bunch-project-doctrine`, `pr-guide.md`, provenance notes).
- Generated surfaces (`codex-marketplace/plugins/*`, `.agents/skills/`, `generated/skill-zips/`, indexes, registry) are produced by the rebuild pipeline, not hand-edited.

## Validation

- `py -3 tools/rebuild_marketplace.py` passes.
- `py -3 tools/check_marketplace.py` passes.
- `py -3 tools/install_agent_skills.py --check` passes (or install is current after rebuild).
- `git diff --check` passes.
- No `github-operations` references remain in editable source paths after rebuild.

## Tradeoffs

- The skill name change is breaking for any prompt or rule that invokes `/github-operations`; the new `/using-github` name aligns with the `using-linear` naming convention and makes the intent clearer. The `openai.yaml` default prompt and `agents` metadata surface the new name.
- Historical intake/decision records are updated to the new canonical path so provenance stays aligned with current source; the original `MARK-226` issue is preserved as provenance.
