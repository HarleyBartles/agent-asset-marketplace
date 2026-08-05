# Reviewer lens expansion — design spec

> Scope: first phase. Add `reviewer-plans`, `reviewer-mesh`, and `reviewer-scripts` as portable subagent profiles, narrow `reviewer-marketplace` to this repo, and make `iterative-review` dispatch only the lenses that apply to a given PR.
> Date: 2026-08-05

## Problem

The `iterative-review` skill now routes through a state graph. It still describes a hard-coded set of lenses for the `agent-asset-marketplace` repository. That causes two concrete problems:

1. **Plan and spec review is not a runtime lens.** Plans and specs are reviewed by one-off prompt templates in `writing-plans` and `brainstorming`, and branch/PR scope drift is caught by an orchestrator-driven `scope-honesty` node. There is no dedicated subagent that can review a plan in isolation and then compare a submitted PR against that plan.
2. **Local and portable lenses are not separated cleanly.** `reviewer-marketplace` is described as a default lens, but it is actually repo-local to `agent-asset-marketplace` and is not relevant to `rooms-mostly`. Consumer repos need a generic scaffolder/mesh lens instead.

`reviewer-known-findings.md` was removed in the 2026-08-04 review-robustness work; each lens profile now owns its own `## Checklist`. New lenses must follow that pattern.

## Goals

1. Add `reviewer-plans`: a portable subagent profile that reviews a spec/plan in isolation and reviews a PR for compliance with its declared plan/spec/roadmap.
2. Add `reviewer-mesh`: a portable subagent profile that reviews generated mesh, scaffolder output, `INDEX.md` files, and the `repo-standards` / `generating-agent-mesh` surfaces common to `agent-asset-marketplace` and `rooms-mostly`.
3. Narrow `reviewer-marketplace` to its actual repo-local concern: `codex-marketplace` pack generation, `tools/new_plugin.py`, `tools/run.py`, and this repo's marketplace-specific generated files.
4. Make `iterative-review` discover and dispatch only the lenses whose applicability rules match the current PR. No lens is mandatory unless the diff and inputs say it applies.
5. Wire `selecting-a-subagent` to know about the new profiles and the `## Applies to` contract that lives inside each lens profile.
6. Add `reviewer-scripts`: a portable subagent profile that reviews new or changed scripts for CLI flag hygiene, dry-run semantics, shebang/invocation conventions, exit-code correctness, path safety, and cross-skill references.

## Non-goals (out of scope for this phase)

- New repo-local lenses for `adventures-of-patch`, `portfolio`, or `wild-bunch` (PPTX, frontend, .NET, game, assets).
- Adding new repo-local or portable lens profiles beyond `reviewer-plans`, `reviewer-mesh`, `reviewer-scripts`, and the explicit model-tier pinning listed below.
- A fully machine-parseable YAML schema for `applies_to`. The first version is a documented `## Applies to` section in each profile that `iterative-review` reads and matches with `grep` / `glob`.
- Reintroducing `reviewer-known-findings.md` or any other shared findings ledger.

## Contract and file targets

### New portable profile: `.agents/agents/reviewer-plans.md`

**Inputs**

- `<plan_path>` (optional)
- `<spec_path>` (optional)
- `<roadmap_path>` (optional)
- `<diff_path>` (when reviewing a branch)
- `<pr_description>` (optional)
- `<scan_findings>` (optional)

**Modes**

1. **In-isolation review:** Read `<plan_path>` / `<spec_path>` only. Validate completeness, consistency, clarity, scope, YAGNI, buildability.
2. **PR compliance review:** Read the diff plus the governing plan/spec/roadmap. Flag scope drift, missing / added / renamed / dropped surfaces, roadmap-order violations, and traceability gaps.

**Checklist** (used by `orchestrator-self-review` and as the core of the diff review):

- No TODOs, TBD, placeholders, or incomplete sections.
- No internal contradictions.
- Requirements are concrete enough that an implementer would not build the wrong thing.
- Scope fits in one plan; no YAGNI or speculative features.
- Tasks are actionable and verifiable.
- Implemented scope in the diff matches the declared plan/spec.
- New packs, renamed surfaces, or dropped features that are not in the plan are flagged as out of scope.
- Roadmap-order violations are flagged when a later-phase item is implemented before its prerequisites.

**Output:** `review-log-plans.md` with `file:line`, severity, description, and remediation. End with `reviewer-plans: N issue(s)` or `reviewer-plans: clean`.

### New portable profile: `.agents/agents/reviewer-mesh.md`

**Inputs**

- `<diff_path>`
- `<pr_description>` (optional)
- `<scan_findings>` (optional)

**Checklist**

- Generated `INDEX.md`, mesh, and scaffolder output (e.g. `scripts/scaffold_*`, `generating-agent-mesh` output) are not hand-edited.
- Scaffolder and mesh generators preserve existing top-level fields and do not lose provenance / author / license data.
- `--check` / `--apply` / `--sync` semantics for the `INDEX.md` / mesh / `repo-standards` generators are respected; dry-run exit codes are correct.
- No generated file is modified directly in `.agents/skills/` (installed copies) or in generated `INDEX.md` trees.

**Output:** `review-log-mesh.md` with the same `file:line`, severity, description, and remediation format.

### New portable profile: `.agents/agents/reviewer-scripts.md`

**Inputs**

- `<diff_path>`
- `<pr_description>` (optional)
- `<scan_findings>` (optional)

**Checklist**

- `--help` is documented and returns `0`; `--check` / `--apply` / `--sync` are classified as read-only, mutating, or mixed and have correct exit codes.
- Scripts use portable shebangs and the consumer's canonical interpreter (e.g. `py -3` on Windows, `python3` elsewhere).
- Scripts resolve output paths to absolute values before `Push-Location` / `cd` and restore the original directory.
- Read-only subagent prompts do not force the script to recreate missing packages or mutate repo state.
- Cross-skill script paths in `SKILL.md` and references point to existing installed or source files.

**Output:** `review-log-scripts.md` with the same `file:line`, severity, description, and remediation format.

### Updated repo-local profile: `.agents/agents/reviewer-marketplace.md`

Narrow to this repo's `codex-marketplace` and marketplace tooling:

- `tools/new_plugin.py` exit codes and default enablement.
- `tools/run.py` target wiring and `ci` dependency correctness.
- `plugin-roots.json`, `bundle-manifest.json`, `repo-index.json`, `codex-marketplace/manifest.json`, `.agents/plugins/marketplace.json`.
- Scaffolder or generator that overwrites existing top-level metadata.

Remove generic scaffolder / mesh checks that now belong to `reviewer-mesh`.

### `## Applies to` contract in every lens profile

Each lens profile must declare an `## Applies to` section containing:

- `globs`: a list of glob patterns evaluated against changed files in the diff.
- `keywords`: a list of path/keyword strings; presence in the diff or PR description indicates relevance.
- `inputs`: named inputs whose presence forces dispatch (e.g. `reviewer-plans` dispatches if `<plan_path>` is provided even when the diff alone does not match the globs).

### Reviewer model tier pinning

To make model selection explicit and remove the `inherit` model, every custom reviewer profile is pinned to a single three-tier model value:

- `reviewer-fast`: `swe-1-6`
- `reviewer`: `glm-5-2`
- `reviewer-strong`: `swe-1-7`
- `reviewer-security`, `reviewer-marketplace`, `reviewer-skills`, `reviewer-plans`, `reviewer-mesh`, `reviewer-scripts`: `glm-5-2`

### Runtime staging tool

`tools/sync_runtime_agents.py` copies the current worktree's `.agents/agents/*.md` profiles to the main checkout so the Devin Desktop runtime can resolve new or changed profiles while the feature branch is in progress.

**Semantics:**

- Default mode is `--check` (read-only drift detection).
- `--apply` is only permitted when `--allow-shared-checkout` is also passed.
- The main worktree is selected by exact `refs/heads/main` branch match, with a fallback to the worktree whose git directory matches the common git directory.
- Dirty-state preview is reported from the target main checkout, not the current worktree.
- No directory is created in `--check` mode; the main checkout is only mutated when `--apply` is approved.
- `tools/run.py runtime-agents` maps `ctx.allow_shared` to the script's `--allow-shared-checkout` and `--yes` flags.



### Reviewer stop condition / loop breaker

Every `reviewer-*.md` profile must end with a `## Stop condition and loop breaker` section that:

- Instructs the subagent not to count tool calls.
- Makes the final step `write` of the off-repo `review-log-<lens>.md` report.
- Requires the final response to be exactly one line: `<profile>: N issue(s)` or `<profile>: clean`.
- Breaks the review if the same `read`/`grep`/`find_file_by_name` call is about to be repeated without a new question it can answer.
- Breaks the review if the last two tool calls produced no new findings.
- Uses a hard backstop of no more than 50 total tool calls after loading inputs.

### `reviewer-mesh` absorbs `reviewer-scaffolders`

`reviewer-mesh` is the canonical portable lens for all generated mesh, scaffolder output, `INDEX.md`, and `repo-standards` surfaces. The separate `reviewer-scaffolders` profile is removed; any scaffolder review responsibilities it held now belong to `reviewer-mesh`. Consumer repos should dispatch `reviewer-mesh` for `**/*scaffold*` and `**/*mesh*` patterns.

### `selecting-a-subagent/SKILL.md` (source in `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/SKILL.md`)

Add to the dispatch table:

- `reviewer-plans` — plan/spec review and PR compliance.
- `reviewer-mesh` — scaffolder / mesh / `repo-standards` / `INDEX.md` lens.
- `reviewer-scripts` — script / CLI safety and compliance lens.

Document that each profile's `## Checklist` and `## Applies to` sections are the source of truth for `orchestrator-self-review` and `lens-dispatch`. Do not point to `reviewer-known-findings.md`; it no longer exists.

### `iterative-review/SKILL.md` (source in `codex-marketplace/plugins/superpowers-plus/skills/iterative-review/SKILL.md`)

Update the `lens-dispatch` node:

1. Discover all `.agents/agents/reviewer-*.md` files in the consumer repo. This set includes the portable profiles shipped by the repo-worker pack plus any repo-local overrides.
2. For each profile, read its `## Applies to` section and its `## Checklist`.
3. Match the diff, `pr_description`, and any provided plan / spec / roadmap paths against the `globs`, `keywords`, and `inputs` rules.
4. Dispatch the matching lenses in parallel. `reviewer-strong` remains mandatory and always runs with the collected logs.
5. If no lenses match, still run `reviewer-strong` on the diff; a pure refactor with no special lens still needs a whole-branch pass.

`orchestrator-self-review` already reads each lens's `## Checklist`; ensure it also reads the `## Applies to` section for lens selection.

Remove the current hard-coded "In this repo, the canonical lenses are..." list. Replace it with the dynamic selection rules.

### Marketplace pack (if applicable)

The portable runtime profiles live in `.agents/agents/` after installation. Their canonical product source is now the `selecting-a-subagent` skill: `codex-marketplace/plugins/superpowers-plus/skills/selecting-a-subagent/assets/` ships the `.md` profile assets. Add `reviewer-plans.md`, `reviewer-mesh.md`, and `reviewer-scripts.md` there (and remove the now-deprecated `reviewer-scaffolders` profile), then regenerate with `py -3 tools/run.py marketplace --apply` before publishing.

To make the shipped `.md` files discoverable in consumer repos, add `scripts/install_profiles.py` to the `selecting-a-subagent` skill. The helper installs the shipped profiles into the consumer repo's `.agents/agents/` directory, overwriting only changed shipped profiles and leaving any locally managed `.agents/agents/reviewer-*.md` files untouched. Update `selecting-a-subagent/SKILL.md` to document the helper and keep the manual global Devin Desktop profile path as an alternative.

## Cross-repo consumer considerations

- `rooms-mostly` consumes the portable `reviewer`, `reviewer-fast`, `reviewer-strong`, `reviewer-security`, `reviewer-skills`, and now `reviewer-plans` and `reviewer-mesh`. Its repo-local set is currently empty; it may add `reviewer-obsidian` later.
- `reviewer-mesh` must not hard-code `agent-asset-marketplace` paths. Its `globs` / `keywords` must use generic patterns (`**/*scaffold*`, `**/*mesh*`, `**/INDEX.md`, `**/repo-standards/**`) that also match `rooms-mostly`.
- `reviewer-plans` must not hard-code the `agent-asset-marketplace` plan directory. It accepts arbitrary plan / spec / roadmap paths.



## Validation

- This spec is the first deliverable.
- The implementation plan is the second deliverable.
- Implementation will be validated by:
  - `py -3 tools/run.py ci --check` passing.
  - `py -3 tools/run.py marketplace --apply` if any `codex-marketplace` source or pack asset changed.
  - A sample `iterative-review` dry-run that correctly selects `reviewer-plans` when a PR touches a plan, `reviewer-mesh` when a PR touches `INDEX.md`, and skips `reviewer-marketplace` in `rooms-mostly`.

## Risks and tradeoffs

- `reviewer-mesh` may overlap with `reviewer-skills` on markdown hygiene. The split is: `reviewer-skills` owns `SKILL.md` and prompt/reference hygiene; `reviewer-mesh` owns generated and scaffolder outputs. Each lens's `## Checklist` makes the split explicit.
- The `## Applies to` section is human-readable in the first version. If the orchestrator cannot parse it reliably, the first implementation may use a simpler heuristic (read the lens and ask it to self-report applicability) rather than strict parsing. This can be tightened later.
- Dynamic dispatch means `iterative-review` needs to `read` every `reviewer-*.md` before dispatch. This is a small cost but must be documented in the plan.

## Deferred

- `reviewer-frontend`, `reviewer-dotnet`, `reviewer-a11y`, `reviewer-assets` for `portfolio` and `wild-bunch`.
- Repo-local `reviewer-obsidian`, `reviewer-pptx`, `reviewer-game`, etc.
- Machine-parseable `applies_to` YAML frontmatter.
