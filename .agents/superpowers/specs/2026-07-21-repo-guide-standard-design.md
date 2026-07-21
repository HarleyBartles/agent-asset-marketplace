# Design: repo-guide-standard skill and agent-asset-marketplace exemplar

**Date:** 2026-07-21
**Status:** Design (pending review)
**Author:** Devin

## 1. Problem

Every repo in this workspace needs a consistent, discoverable set of agent-facing guidance surfaces:

- Root `AGENTS.md` with standard headings that agents and tools look for.
- Root `REVIEW.md` and `CONTRIBUTING.md` as thin pointer files.
- `.agents/guides/` with a canonical set of stage and topical guides.

That guidance is currently split across `base-doctrine`, `repo-worker-base`, local `.agents/guides/*.md`, and ad-hoc root `AGENTS.md` edits. There is no single portable baseline that says "this is how a repo's guides should be laid out, how agents should invoke them, and what the handoff order is". Local guides therefore repeat cross-repo rules and repo-specific overlays get mixed with universal ones.

## 2. Goal

Create a portable first-party skill, `repo-guide-standard`, that becomes the canonical home for cross-repo guide concerns. The skill is invoked whenever an agent reads, creates, or updates repo guides. It supplies the universal standard; each repo supplies a thin `.agents/docs/repo-guide-policy.md` overlay with local mappings.

Then make `agent-asset-marketplace` the first fully-aligned exemplar by creating the missing guide docs and wiring the root surfaces to the skill.

## 3. Scope

### 3.1 Portable skill

- **Source location:** `sources/first_party/skills/repo-guide-standard/`
- **Pack assignment:** `repo-worker-pack` in `codex-marketplace/custody-pack-registry.json`
- **Files:**
  - `SKILL.md` — invocation surface and routing rules.
  - `references/repository-guide-standard.md` — the canonical cross-repo standard text.

### 3.2 Local overlay

- `.agents/docs/repo-guide-policy.md` in `agent-asset-marketplace` — the repo's local mapping and exceptions.

### 3.3 Root discoverable surfaces

- `AGENTS.md` — canonical headings first, then `## Routing pointers` pointing at the local policy, mesh policy, and scoped `AGENTS.md` files.
- `REVIEW.md` — pointer to `.agents/guides/code-review-guide.md`.
- `CONTRIBUTING.md` — pointer to `.agents/guides/contributing-guide.md`.

### 3.4 Guide set

Core stage guides already exist:

- `.agents/guides/design-guide.md`
- `.agents/guides/planning-guide.md`
- `.agents/guides/implementing-guide.md`
- `.agents/guides/code-review-guide.md`
- `.agents/guides/marketplace-generation-guide.md`
- `.agents/guides/skill-authoring-guide.md`

Additional guides to create:

- `.agents/guides/security-guide.md`
- `.agents/guides/testing-guide.md`
- `.agents/guides/contributing-guide.md`
- `.agents/guides/pr-guide.md`
- `.agents/guides/code-style-guide.md`

### 3.5 Routing surfaces

- `.agents/guides/AGENTS.md` — update to list all guides.
- `.agents/guides/INDEX.md` — regenerate.
- Root `INDEX.md` — regenerate.
- `docs/AGENTS.md` — add pointer to `.agents/docs/repo-guide-policy.md`.
- `.agents/docs/AGENTS.md` — add pointer to `repo-guide-policy.md`.

### 3.6 Marketplace projection

- Add `repo-guide-standard` to `repo-worker-pack` source ledger and entries.
- Run `tools/rebuild_marketplace.py` to project the skill into `codex-marketplace/plugins/repo-worker-pack/skills/repo-guide-standard/`.

## 4. Out of scope

- Sister repo alignment in this PR.
- Human-facing prose beyond the required AGENTS/REVIEW/CONTRIBUTING/guides/policy surfaces.
- Removing or duplicating `repo-worker-base` stage baselines. `repo-guide-standard` is invoked *alongside* `repo-worker-base` for guide work; `repo-worker-base` remains the authority for repo hygiene, worktree, branch, and publication boundaries.

## 5. Design

### 5.1 `repo-guide-standard` skill

`SKILL.md`:

- **use_when:** Reading, creating, updating, or aligning any repo guide; when deciding workflow order for design/plan/implement/review; when a repo's guide set is missing or misaligned with the standard.
- **do_not_use_when:** Generic repo hygiene (worktree, branch, source custody, publication) — defer to `repo-worker-base` for that.
- **Instructions:**
  1. Read `references/repository-guide-standard.md`.
  2. Locate the repo's `.agents/docs/repo-guide-policy.md` (or create it if missing and the task is to align the repo).
  3. Invoke `/repo-worker-base` for worktree, branch, validation, and publication boundaries.
  4. Read the repo's specific local guide.
  5. Route to the correct Superpowers skill for the stage:
     - design -> `/brainstorming`
     - planning -> `/writing-plans`
     - implementation -> `/executing-plans` or `/subagent-driven-development`
     - review -> `/requesting-code-review`

### 5.2 `references/repository-guide-standard.md`

The canonical cross-repo standard. Contains:

1. **Required root surfaces**
   - `AGENTS.md` with standard headings:
     - `## Build and test commands`
     - `## Testing instructions`
     - `## Code style guidelines`
     - `## Review guidelines`
     - `## PR instructions`
     - `## Contributing`
     - `## Security considerations`
   - `REVIEW.md` -> `.agents/guides/code-review-guide.md`
   - `CONTRIBUTING.md` -> `.agents/guides/contributing-guide.md`

2. **`.agents/guides/` core set**
   - `design-guide.md`
   - `planning-guide.md`
   - `implementing-guide.md`
   - `code-review-guide.md`

3. **Allowed additional guides**
   - Named `<topic>-guide.md`.
   - Must live in `.agents/guides/`.
   - Must be repo-specific overlays, not repeats of portable doctrine.
   - Examples: `security-guide.md`, `testing-guide.md`, `contributing-guide.md`, `pr-guide.md`, `code-style-guide.md`, `marketplace-generation-guide.md`, `skill-authoring-guide.md`.

4. **Workflow order**
   - `design -> planning -> implementing -> review`
   - Each stage handoff requires the portable baseline (`repo-guide-standard` for guide composition, `repo-worker-base` for repo hygiene), then the local guide, then the Superpowers lane.

5. **Local overlay policy**
   - Each repo keeps `.agents/docs/repo-guide-policy.md`.
   - It names the repo's existing guide files and any standard exceptions.

### 5.3 `.agents/docs/repo-guide-policy.md`

`agent-asset-marketplace` exemplar:

- States that the repo follows `repo-guide-standard`.
- Maps the standard guide names to local paths.
- Lists which additional guides exist and which are planned.
- Notes any repo-specific exceptions (e.g., `marketplace-generation-guide.md` and `skill-authoring-guide.md` exist because this repo is an asset marketplace).

### 5.4 Root `AGENTS.md` structure

Order:

1. `## Repository purpose`
2. `## Source-of-truth split`
3. `## Publication proof for repo work`
4. Canonical guide headings (`Build and test commands` through `Security considerations`)
5. `## Routing pointers` — scoped `AGENTS.md`, doctrine, and local policy.
6. `## Maintenance responsibility`

Each canonical heading is a thin pointer to the relevant guide or doc.

### 5.5 New guide docs

Each new guide is a thin overlay:

- **security-guide.md** — repo-specific security posture, references `security-review` profile and security-pack skills.
- **testing-guide.md** — repo test commands, TDD workflow, `pytest` conventions.
- **contributing-guide.md** — contributor lifecycle: `/work-mode-router` -> design -> planning -> implementation -> review; points to `design-guide.md`, `planning-guide.md`, `implementing-guide.md`, `code-review-guide.md`.
- **pr-guide.md** — PR workflow, publication proof, commit/branch conventions.
- **code-style-guide.md** — Python/markdown conventions, skill frontmatter, naming rules.

### 5.6 Guide-to-skill routing

Local guides route to installed skills:

- `contributing-guide.md` -> `/work-mode-router`
- `design-guide.md` -> `/brainstorming`
- `planning-guide.md` -> `/writing-plans`
- `implementing-guide.md` -> `/executing-plans` or `/subagent-driven-development`
- `code-review-guide.md` -> `/requesting-code-review` and `/risk-gates`

## 6. Detailed artifact outlines

### 6.1 `repo-guide-standard` skill source

`sources/first_party/skills/repo-guide-standard/SKILL.md`:

- Frontmatter:
  - `name: repo-guide-standard`
  - `description: Use when reading, creating, updating, or aligning repo guides; when determining guide workflow order and handoffs.`
  - `metadata.source-id`, `source-path`, `provenance-name`, `source-category: first_party`, `status: active`, `owner: Harley Bartles`
  - `metadata.scope`: Cross-repo guide layout, invocation, workflow order, and handoff requirements.
  - `metadata.use_when`: reading/creating/updating any repo guide; guide-set alignment; workflow order decisions.
  - `metadata.do_not_use_when`: generic repo hygiene (worktree, branch, source custody, publication).
  - `metadata.use_with`: `[repo-worker-base, work-mode-router, brainstorming, writing-plans, executing-plans, subagent-driven-development, requesting-code-review]`
  - `license: MIT`
- Body:
  - `# Repo Guide Standard`
  - `## Read when` table mapping needs to references.
  - `## Composition contract`: `repo-guide-standard -> repo-worker-base -> local guide -> Superpowers lane`.
  - `## Required root surfaces`
  - `## Core guide set`
  - `## Allowed additional guides`
  - `## Workflow order and Superpowers mapping`

`sources/first_party/skills/repo-guide-standard/agents/openai.yaml`:

- `interface.display_name: Repo Guide Standard`
- `interface.short_description: Use when reading, creating, updating, or aligning repo guides and their workflow order.`
- `interface.default_prompt`: Read `references/repository-guide-standard.md`, then the repo's `.agents/docs/repo-guide-policy.md`, then the specific local guide, then route to the matching Superpowers skill and `repo-worker-base` for hygiene.
- `policy.allow_implicit_invocation: true`

`sources/first_party/skills/repo-guide-standard/references/repository-guide-standard.md`:

- `# Repository Guide Standard`
- `## Required root surfaces`: `AGENTS.md` canonical headings, `REVIEW.md`, `CONTRIBUTING.md`.
- `## Core guide set`: `design-guide.md`, `planning-guide.md`, `implementing-guide.md`, `code-review-guide.md`.
- `## Allowed additional guides`: `<topic>-guide.md` in `.agents/guides/`; examples list.
- `## Workflow order`: design -> planning -> implementing -> review; handoff requirements.
- `## Local overlay policy`: each repo keeps `.agents/docs/repo-guide-policy.md`.
- `## Relationship to repo-worker-base`: `repo-guide-standard` owns guide composition; `repo-worker-base` owns repo hygiene and stage baselines.

### 6.2 Local overlay

`.agents/docs/repo-guide-policy.md`:

- `# Repo Guide Policy`
- States the repo follows `repo-guide-standard` and invokes `/repo-guide-standard` before guide work.
- `## Standard-to-local mapping`: table mapping standard guide names to local paths and status (exists / to create / N/A).
- `## Additional guides`: list of repo-specific additional guides with rationale.
- `## Exceptions`: any naming or location exceptions and why.

### 6.3 New guide docs

Each guide follows the same thin-overlay shape: `# <Topic> Guide`, `## When to use`, `## Before you begin`, `## Repo-specific guidance`, `## Routing to skills`.

- `.agents/guides/security-guide.md`:
  - No secrets in repo; validate inputs; use `security-review` profile; use security-pack skills for deep review.
- `.agents/guides/testing-guide.md`:
  - `pytest` entrypoint; TDD workflow; contract tests; running specific test files.
- `.agents/guides/contributing-guide.md`:
  - Invoke `/work-mode-router`; design -> planning -> implementing -> review; point to root `REVIEW.md`/`CONTRIBUTING.md`.
- `.agents/guides/pr-guide.md`:
  - Branch/PR workflow; publication proof per root `AGENTS.md`; commit/branch conventions; `github-operations` for evidence.
- `.agents/guides/code-style-guide.md`:
  - Python style; markdown conventions; skill frontmatter; naming; line endings (`newline="\n"`); `docs/skill-standards-policy.md` for skill shapes.

### 6.4 Root surface updates

`AGENTS.md` canonical headings become thin pointers:

- `## Build and test commands` -> `tools/AGENTS.md` and `implementing-guide.md`
- `## Testing instructions` -> `testing-guide.md`
- `## Code style guidelines` -> `code-style-guide.md` and `docs/skill-standards-policy.md`
- `## Review guidelines` -> `REVIEW.md` and `code-review-guide.md`
- `## PR instructions` -> `pr-guide.md`
- `## Contributing` -> `CONTRIBUTING.md` and `contributing-guide.md`
- `## Security considerations` -> `security-guide.md`

`REVIEW.md` and `CONTRIBUTING.md` stay thin pointers to `code-review-guide.md` and `contributing-guide.md`.

`## Routing pointers` moves below the canonical headings and adds:

- `.agents/docs/repo-guide-policy.md` for repo-specific guide mappings.

### 6.5 Marketplace and routing surfaces

- `codex-marketplace/custody-pack-registry.json`:
  - Add `sources/first_party/skills/repo-guide-standard` to `repo-worker-pack.source_ledger`.
  - Add an entry object for `repo-guide-standard` under `repo-worker-pack.entries` with `content_mode: verbatim`, `source_category: first_party`, `canonical_source_path: sources/first_party/skills/repo-guide-standard`, `local_path: skills/repo-guide-standard`.
- `codex-marketplace/plugin-roots.json`: no change.
- `.agents/plugins/marketplace.json`: no change; `repo-worker-pack` is already `INSTALLED_BY_DEFAULT`.
- `.agents/guides/AGENTS.md`: update routing pointers to list all guides, including the five new ones.
- `.agents/guides/INDEX.md`: regenerate.
- Root `INDEX.md`: regenerate.
- `docs/AGENTS.md` and `.agents/docs/AGENTS.md`: add pointer to `.agents/docs/repo-guide-policy.md`.

## 7. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Duplicating existing `repo-worker-base` stage contract | `repo-guide-standard` is invoked alongside `repo-worker-base`; `repo-worker-base` keeps its stage baselines. The skill only owns guide-specific layout, invocation, and workflow order. |
| `repo-worker-pack` grows | The skill is small and text-only; it replaces scattered guide base material. |
| Sister repos not aligned | Out of scope for this PR; the skill is the portable deliverable they can adopt later. |
| Marketplace regeneration surfaces pre-existing drift | Run `check_marketplace.py` and review diff carefully; only commit intended changes. |

## 8. Validation

- `py -3 tools/rebuild_marketplace.py`
- `py -3 tools/check_marketplace.py`
- `py -3 tools/generate_index_mesh.py --check`
- Manual review of `AGENTS.md`, `REVIEW.md`, `CONTRIBUTING.md`, `.agents/guides/INDEX.md`, and `.agents/docs/repo-guide-policy.md`.
- `git status` and `git diff` review for unintended changes.

## 9. Handoff to planning

The implementation plan should include tasks for:

1. Creating `sources/first_party/skills/repo-guide-standard/`.
2. Updating `codex-marketplace/custody-pack-registry.json`.
3. Creating `.agents/docs/repo-guide-policy.md`.
4. Updating root `AGENTS.md` (reorder headings and routing pointers).
5. Creating the five new `.agents/guides/*.md` files.
6. Updating `.agents/guides/AGENTS.md`.
7. Regenerating `INDEX.md` mesh and marketplace projections.
8. Validating and committing.

---

**Spec self-review:**

- [x] No `TBD` or `TODO` placeholders.
- [x] Goals, scope, and non-goals are consistent.
- [x] File targets and paths are concrete.
- [x] Validation steps are explicit.
- [x] Handoff to planning is clear.
