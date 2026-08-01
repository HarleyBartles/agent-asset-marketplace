# 2026-07-25-02-repo-standards-alignment.md

**Goal:** Harden the `repo-standards` skill so it enforces a consistent, router-based `AGENTS.md` shape, canonical `.agents/guides/`, a standardized `marketplace.json` schema, and cross-platform `.sh`/`.ps1` entry points for all scaffold and preflight scripts.

**Architecture:** Treat `repo-standards` as the opinionated enforcement layer and `generating-agent-mesh` as the content validator. `repo_standards.py` checks that required surfaces exist *and* that scaffold scripts report no drift when run with `--check`. The root `AGENTS.md` becomes a thin router with five core sections and a routing table; detailed topic guidance lives in `.agents/guides/<topic>-guide.md` or scoped `AGENTS.md` files. The `marketplace.json` schema uses `repo.local_skill_prefixes` as the single source of truth for local skill retention.

**Tech Stack:** Python 3.13, bash, PowerShell, git, `py -3` launcher.

**Depends on:** [2026-07-25-01-generating-agent-mesh.md](2026-07-25-01-generating-agent-mesh.md) — the `generating-agent-mesh` rename and `validate-agent-mesh` command must land first because `repo-standards` preflight and `refreshing-installed-skills` depend on them.

**Working worktree:** `Z:\_agent-worktrees\agent-asset-marketplace\repo-standards-design`.

## Constraints and notes

- All text writes use LF (`newline="\n"`).
- Generated/projected surfaces must be produced by `py -3 tools/rebuild_marketplace.py` and proven by `py -3 tools/check_marketplace.py`.
- The shared pre-commit hook has been temporarily disabled (renamed to `pre-commit.disabled` in the main checkout `.git/hooks`). This plan must restore it as part of the final scaffold/apply step or in a follow-up PR.
- This is a draft plan. The exact list of canonical `AGENTS.md` topics and the precise routing targets should be assessed after Plan 1 implementation and before Plan 2 execution.

---

## Task 1: Update the repository shape standard and manifest

**Files:**
- Modify: `sources/first_party/skills/repo-standards/references/repository-shape-standard.md`
- Modify: `sources/first_party/skills/repo-standards/references/repository-shape-manifest.json`

### Step 1: Update `repository-shape-standard.md`

Rewrite the `## Required surfaces` section to match the router + mesh model:

- `.agents/plugins/marketplace-source` as a git submodule (or declared exception).
- `.agents/plugins/marketplace.json` with `repo.local_skill_prefixes` configured.
- `scripts/ci-preflight.sh` and `scripts/ci-preflight.ps1` for the default preflight bundle.
- `.git/hooks/pre-commit` wired to `scripts/ci-preflight.sh --check`.
- `.agents/docs/repo-runbook-policy.md` mapping the repo to the cross-repo guide standard.
- `REVIEW.md` at the repo root as the review entry point.
- `CONTRIBUTING.md` at the repo root as the substantive contributor entry point.
- `.gitignore` containing the `.agents/superpowers/sdd/**` and `!.agents/superpowers/sdd/.gitignore` rule.
- Root `AGENTS.md` as a router with five core sections and a routing table.
- `.agents/guides/<standard-guide>.md` for the core and declared guide set.

Add a new section `## Router AGENTS.md model`:

```markdown
## Router AGENTS.md model

Root `AGENTS.md` is a router, not an encyclopedia. It must contain exactly five core sections:

1. `## Repository purpose`
2. `## Source-of-truth split`
3. `## Build and test commands`
4. `## Routing pointers`
5. `## Maintenance responsibility`

The `## Routing pointers` section must list resolvable links to the scoped surfaces that own each canonical topic. Canonical topics include: Repository purpose, Source-of-truth split, Publication proof, Build and test commands, Testing instructions, Code style guidelines, Review guidelines, PR instructions, Contributing, Security considerations, Routing pointers, and Maintenance responsibility.

A `repo-standards --check` run validates that the five core sections exist, that every routing pointer resolves to a tracked file, and that the 12 canonical topics are covered by the union of root sections and routed targets.
```

### Step 2: Update `repository-shape-manifest.json`

Add a `root-agents-md` surface and a `guides-agents-md` surface, plus `scaffold` pointers where missing. The result should look like:

```json
{
  "version": 2,
  "surfaces": [
    {
      "id": "marketplace-source-submodule",
      "path": ".agents/plugins/marketplace-source",
      "kind": "submodule",
      "source": null,
      "optional": false
    },
    {
      "id": "marketplace-json",
      "path": ".agents/plugins/marketplace.json",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_marketplace_json.py",
      "optional": false
    },
    {
      "id": "ci-preflight-ps1",
      "path": "scripts/ci-preflight.ps1",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_ci_preflight.py",
      "optional": false
    },
    {
      "id": "ci-preflight-sh",
      "path": "scripts/ci-preflight.sh",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_ci_preflight.py",
      "optional": false
    },
    {
      "id": "pre-commit-hook",
      "path": ".git/hooks/pre-commit",
      "kind": "hook",
      "source": "templates/pre-commit",
      "optional": false
    },
    {
      "id": "repo-runbook-policy",
      "path": ".agents/docs/repo-runbook-policy.md",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_repo_guide_policy.py",
      "optional": false
    },
    {
      "id": "root-agents-md",
      "path": "AGENTS.md",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_agents_md.py",
      "optional": false
    },
    {
      "id": "guides-agents-md",
      "path": ".agents/guides/AGENTS.md",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_guides.py",
      "optional": true
    },
    {
      "id": "review-entry",
      "path": "REVIEW.md",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_review.py",
      "optional": false
    },
    {
      "id": "contributing-entry",
      "path": "CONTRIBUTING.md",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_contributing.py",
      "optional": false
    },
    {
      "id": "root-gitignore",
      "path": ".gitignore",
      "kind": "file",
      "source": null,
      "scaffold": "scaffold_gitignore.py",
      "optional": false
    }
  ]
}
```

Commit this task on its own so the shape contract is clear before changing the code that enforces it.

---

## Task 2: Add new scaffold scripts for `AGENTS.md` and `marketplace.json`

**Files:**
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_agents_md.py`
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_agents_md.sh`
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_agents_md.ps1`
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_marketplace_json.py`
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_marketplace_json.sh`
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold_marketplace_json.ps1`
- Modify: `sources/first_party/skills/repo-standards/scripts/scaffold-all.sh`
- Modify: `sources/first_party/skills/repo-standards/scripts/scaffold-all.ps1`

### Step 1: `scaffold_agents_md.py`

The script supports `--check` and `--force`. It operates on `AGENTS.md` at the repo root.

Behavior:

- If `AGENTS.md` does not exist and `--check` is passed, report `DRIFT: AGENTS.md missing` and exit 1.
- If `AGENTS.md` exists and `--check` is passed, validate:
  - The five core section headings exist (`^## Repository purpose$`, etc.).
  - A `## Routing pointers` section exists and contains at least one markdown link.
  - Every markdown link in the `## Routing pointers` section resolves to an existing file inside the repo.
  - The 12 canonical topics are covered. A topic is "covered" if it appears as a heading in `AGENTS.md` or as a heading in any routed target reachable from the routing pointers.
- If validation fails, print `DRIFT: <message>` for each failure and exit 1.
- If `--force` is passed or `AGENTS.md` is missing, write a scaffold template.
- The scaffold template should be stored at `sources/first_party/skills/repo-standards/templates/AGENTS.md`.

Create the template `sources/first_party/skills/repo-standards/templates/AGENTS.md`:

```markdown
# <repo-name>

## Repository purpose

<!-- One paragraph describing what this repo produces and who consumes it. -->

## Source-of-truth split

<!-- State the split between repo state and external control planes. -->

## Build and test commands

<!-- Canonical commands for validation, build, and test. -->

## Routing pointers

- Repository purpose: [AGENTS.md](AGENTS.md)
- Source-of-truth split: [AGENTS.md](AGENTS.md)
- Publication proof: [<topic-guide>](.agents/guides/<topic-guide>)
- Build and test commands: [AGENTS.md](AGENTS.md)
- Testing instructions: [.agents/guides/testing-guide.md](.agents/guides/testing-guide.md)
- Code style guidelines: [.agents/guides/code-style-guide.md](.agents/guides/code-style-guide.md)
- Review guidelines: [.agents/guides/code-review-guide.md](.agents/guides/code-review-guide.md)
- PR instructions: [.agents/guides/pr-guide.md](.agents/guides/pr-guide.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security considerations: [.agents/guides/security-guide.md](.agents/guides/security-guide.md)
- Routing pointers: [AGENTS.md](AGENTS.md)
- Maintenance responsibility: [AGENTS.md](AGENTS.md)

## Maintenance responsibility

<!-- Who keeps this file and the routed surfaces current. -->
```

### Step 2: `scaffold_marketplace_json.py`

The script supports `--check` and `--force`. It operates on `.agents/plugins/marketplace.json`.

Behavior:

- If the file is missing, write a minimal scaffold:

```json
{
  "repo": {
    "local_skill_prefixes": ["mark-"]
  },
  "plugins": []
}
```

- If the file exists, ensure it has a top-level `repo` object with a non-empty `local_skill_prefixes` list.
- Migrate legacy keys:
  - Top-level `local_skill_prefixes` -> move to `repo.local_skill_prefixes`.
  - Top-level `local_skills` -> transform names into prefixes and move to `repo.local_skill_prefixes`.
- Preserve the `plugins`, `name`, and `interface` blocks unchanged.
- In `--check` mode, report drift if the `repo.local_skill_prefixes` key is missing or empty.

### Step 3: Wrapper parity

Add `.sh` and `.ps1` wrappers for both new scripts. The `.sh` wrapper should follow the existing `scaffold-guides.sh` pattern. The `.ps1` wrapper can follow `validate-agent-mesh.ps1` from Plan 1.

### Step 4: Update `scaffold-all`

Add `scaffold-agents-md` and `scaffold-marketplace-json` to the `scaffold-all.sh` and `scaffold-all.ps1` sequences.

---

## Task 3: Harden `repo_standards.py` `--check` mode

**Files:**
- Modify: `sources/first_party/skills/repo-standards/scripts/repo_standards.py`

### Step 1: Invoke scaffold scripts with `--check`

In `_check_surface`, when a surface has a `scaffold` script, run `[sys.executable, scaffold, "--check"]` and surface any `DRIFT:` output as a finding. The existing `template`-based byte comparison can remain for surfaces that have `source` but no `scaffold`.

The check should:

1. Run the scaffold script with `--check`.
2. If it exits non-zero, add each line of stdout/stderr that starts with `DRIFT:` to `findings`.
3. If the scaffold passes, still verify the surface file exists at the declared `path`.

### Step 2: Add `AGENTS.md` validation

For the `root-agents-md` surface, in addition to scaffold check, run an inline validation:

- Parse `AGENTS.md` headings.
- Verify the five core sections.
- Extract links from `## Routing pointers` and resolve them relative to the repo root.
- Verify the 12 canonical topic coverage across root and routed files.

If any validation fails, emit `DRIFT:` findings and exit non-zero.

### Step 3: Update `repository-shape-manifest.json` version

Bump the manifest `version` to `2` and verify `repo_standards.py` reads it.

---

## Task 4: Add PowerShell wrappers for all scaffold scripts

**Files:**
- Create: `sources/first_party/skills/repo-standards/scripts/scaffold-*.ps1` for every scaffold that lacks one.
- Modify: `sources/first_party/skills/repo-standards/scripts/scaffold-all.ps1` to call the `.ps1` wrappers.

### Step 1: Audit existing wrappers

List every script in `sources/first_party/skills/repo-standards/scripts/` that has a `.sh` wrapper but no `.ps1` wrapper. Expected targets:

- `scaffold-ci-preflight.ps1`
- `scaffold-contributing.ps1`
- `scaffold-gitignore.ps1`
- `scaffold-guides.ps1`
- `scaffold-repo-guide-policy.ps1`
- `scaffold-review.ps1`
- `scaffold-agents-md.ps1`
- `scaffold-marketplace-json.ps1`

### Step 2: Write the `.ps1` wrappers

Each wrapper should:

- Accept `[switch]$Check` and `[switch]$Force`.
- Locate the adjacent `.py` script with `Split-Path -Parent $MyInvocation.MyCommand.Path`.
- Find a Python interpreter (`py`, `python`, `python3`) and call the `.py` script with `-Check` or `-Force` translated to `--check` and `--force`.
- Exit with the same code as the Python script.

### Step 3: Update `scaffold-all.ps1`

Replace the current implementation with a loop over the scaffold names, calling each `.ps1` wrapper with the same parameters.

---

## Task 5: Update `repo-standards` skill documentation

**Files:**
- Modify: `sources/first_party/skills/repo-standards/SKILL.md`
- Modify: `sources/first_party/skills/repo-standards/agents/openai.yaml` (if needed)

### Step 1: Update `SKILL.md`

- In `## Scaffold helpers`, add `scaffold-agents-md` and `scaffold-marketplace-json`.
- Add a `## Router AGENTS.md` section explaining the five core sections, routing table, and canonical-topic coverage.
- Add a `## Marketplace.json schema` section stating that `repo.local_skill_prefixes` is the canonical key and that the script migrates legacy top-level keys.
- Document that `ci-preflight` supports an optional `scripts/ci-preflight-extra.sh` / `scripts/ci-preflight-extra.ps1` hook with the same `--check` / `--changed-from` contract.

### Step 2: Update `agents/openai.yaml`

Update `interface.short_description` and `interface.default_prompt` to mention `AGENTS.md` router enforcement and `marketplace.json` schema migration.

---

## Tightening notes (post-Plan 1 review)

- **Pre-commit flag**: The `templates/pre-commit` already calls `scripts/ci-preflight.sh --check` (lowercase). Update `repository-shape-standard.md` to match; do not introduce `-Check`.
- **Plan 1 carry-over**: `ci-preflight` now supports `scripts/ci-preflight-extra.sh` / `.ps1` with `--check` and `--changed-from`. Document this in `repo-standards/SKILL.md`.
- **PowerShell wrappers**: Existing scaffolds already have `.ps1` wrappers, but they pass `@args` raw and use `python` instead of the `py` launcher. Task 4 should rewrite *all* `.ps1` wrappers to accept `[switch]$Check` / `[switch]$Force` and translate them to `--check` / `--force`, then call `py -3 <script>.py` (with fallback to `python`/`python3`).
- **New scaffold registration**: `scaffold-all.sh` and `scaffold-all.ps1` currently list `scaffold-repo-guide-policy scaffold-guides scaffold-review scaffold-contributing scaffold-ci-preflight scaffold-gitignore`. Add `scaffold-agents-md` and `scaffold-marketplace-json` to both sequences.
- **marketplace.json enforcement**: `repo_standards.py` already validates `repo.local_skill_prefixes` in `_check_marketplace_json`; `scaffold_marketplace_json.py` can focus on writing/migrating the file. Migration should move top-level `local_skill_prefixes` and `local_skills` into `repo.local_skill_prefixes` as described.
- **AGENTS.md validation**: The 12 canonical topic coverage check should be shared between `scaffold_agents_md.py` and `repo_standards.py` so `--check` from either surface reports consistent `DRIFT:` messages. Consider extracting the heading/link parser into a small module under `repo-standards/scripts/`.
- **Tests**: Add a new `tests/test_repo_standards.py` (or extend existing) covering:
  - `scaffold_agents_md.py --check` on a valid router `AGENTS.md`.
  - `scaffold_agents_md.py --check` detecting a missing core section.
  - `scaffold_marketplace_json.py` migrating legacy `local_skill_prefixes`.
  - `repo_standards.py --check` reporting `DRIFT:` for `root-agents-md` and `guides-agents-md` surfaces.
- **Regeneration order**: After code changes, run `py -3 tools/rebuild_marketplace.py` and `py -3 tools/check_marketplace.py` as the final green-path proof, then regenerate `scripts/ci-preflight.*` if templates changed.
- **Pre-commit restoration**: The pre-commit hook was disabled during Plan 1. Restore `.git/hooks/pre-commit` either as the final step of this plan or in a follow-up PR if the scope grows.

---

## Task 6: Align the source repo surfaces

**Files:**
- Modify: `AGENTS.md` (source repo root)
- Modify: `.agents/docs/repo-runbook-policy.md`
- Modify: `.agents/plugins/marketplace.json` (if migration needed)
- Modify: `REVIEW.md` and `CONTRIBUTING.md` (if drift from templates)

### Step 1: Rewrite root `AGENTS.md` as a router

Use the five core sections. Keep the existing routing targets where they are valid, and add any missing pointers. The current root `AGENTS.md` already has good content; this step mostly collapses the monolithic headings into the router form and moves detailed guidance to routed files.

Draft the new root `AGENTS.md`:

```markdown
# Agent Asset Marketplace

## Repository purpose

This repository is the source of truth for agent-facing assets. It is an agent asset marketplace, not just a research ledger. The primary durable output is market-consumable assets.

## Source-of-truth split

GitHub and the repository tree prove file state, landed assets, manifests, source snapshots, provenance notes, validation scripts, and playbooks. Linear remains the control plane for issue state, worker state, review posture, and closeout decisions.

## Build and test commands

Canonical validation and regeneration commands live in [`tools/AGENTS.md`](tools/AGENTS.md). Run `py -3 tools/rebuild_marketplace.py` for full regeneration and `py -3 tools/check_marketplace.py` for CI.

## Routing pointers

- Repository purpose: [AGENTS.md](AGENTS.md)
- Source-of-truth split: [AGENTS.md](AGENTS.md)
- Publication proof: [tools/AGENTS.md](tools/AGENTS.md)
- Build and test commands: [tools/AGENTS.md](tools/AGENTS.md)
- Testing instructions: [.agents/guides/testing-guide.md](.agents/guides/testing-guide.md)
- Code style guidelines: [.agents/guides/code-style-guide.md](.agents/guides/code-style-guide.md)
- Review guidelines: [REVIEW.md](REVIEW.md) and [.agents/guides/code-review-guide.md](.agents/guides/code-review-guide.md)
- PR instructions: [.agents/guides/pr-guide.md](.agents/guides/pr-guide.md)
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security considerations: [.agents/guides/security-guide.md](.agents/guides/security-guide.md)
- Maintenance responsibility: [AGENTS.md](AGENTS.md)

## Maintenance responsibility

This file is the repository's primary worker doctrine. When repo conventions, marketplace structure, or publication rules change, this file must be updated to reflect the new expectations.
```

### Step 2: Move detailed topic content to routed targets

For each topic that is no longer a root heading, ensure the routed target contains equivalent guidance. The routed targets are already present (`.agents/guides/*.md`, `REVIEW.md`, `CONTRIBUTING.md`). The main work is removing duplication from `AGENTS.md` and adding missing routing pointers.

### Step 3: Update `.agents/docs/repo-runbook-policy.md`

Add a note under `## Standard-to-local mapping` that root `AGENTS.md` is a router and that the canonical topics are covered by the union of root sections and the listed guides.

### Step 4: Ensure `marketplace.json` uses `repo.local_skill_prefixes`

Run the new `scaffold_marketplace_json.py --check`. If it reports drift, run it without `--check` to migrate. Verify the file still contains the `plugins` array and any other Codex-required fields.

---

## Task 7: Regenerate and validate

### Step 1: Run the scaffold check sequence

```bash
py -3 sources/first_party/skills/repo-standards/scripts/scaffold-all.sh --check
```

Expected: `OK` for every scaffold. If `AGENTS.md` or `marketplace.json` drift is reported, fix the source or run without `--check`.

### Step 2: Run `repo-standards --check`

```bash
py -3 sources/first_party/skills/repo-standards/scripts/repo_standards.py --check
```

Expected: `OK repo-standards: all surfaces present`.

### Step 3: Regenerate the marketplace

```bash
py -3 tools/rebuild_marketplace.py
```

Expected: completes without errors and writes the projected surfaces.

### Step 4: Run the marketplace check

```bash
py -3 tools/check_marketplace.py
```

Expected: exit code 0.

### Step 5: Restore the pre-commit hook (or decide to defer)

If the shared pre-commit hook should be restored now:

```bash
py -3 sources/first_party/skills/repo-standards/scripts/repo_standards.py --apply --yes
```

If the hook should stay disabled until the PR merges, add an explicit note to this plan and to the final commit message.

### Step 6: Commit

```bash
git add -A
git commit -m "feat: harden repo-standards for router AGENTS.md, canonical guides, and marketplace.json schema"
```

---

## Completion checklist

- [x] Task 1: Repository shape standard and manifest updated with router AGENTS.md model.
- [x] Task 2: `scaffold_agents_md.py` and `scaffold_marketplace_json.py` scripts, templates, and `.sh`/`.ps1` wrappers added.
- [x] Task 3: `repo_standards.py --check` hardened with scaffold checks and AGENTS.md validation.
- [x] Task 4: PowerShell wrappers for all scaffold scripts rewritten for `py` launcher and `-Check`/`-Force` support.
- [x] Task 5: `repo-standards/SKILL.md` and `agents/openai.yaml` updated.
- [x] Task 6: Source repo `AGENTS.md` rewritten as a router; `repo-runbook-policy.md` notes root router coverage; `marketplace.json` already uses `repo.local_skill_prefixes`.
- [x] Task 7: Full scaffold check, `repo-standards --check`, `rebuild_marketplace.py`, `check_marketplace.py`, and pre-commit hook restore completed.

## Execution Confidence Rating

**6/10 draft.**

The high-level shape, file list, and design intent are clear. The exact 12-topic coverage algorithm, the precise scaffold template content, and the PowerShell wrapper details need to be finalized after Plan 1 lands and we can assess the actual `AGENTS.md` and `marketplace.json` state. The plan is deliberately scoped to the source repo; cross-repo rollout is Plan 3-6.

## Known gaps to close before execution

1. Final canonical topic list and whether "Publication proof" is a separate topic or part of "Source-of-truth split".
2. Exact heading-matching regex (case-insensitive, optional trailing anchors, allowed whitespace).
3. Whether `guides-agents-md` (`.agents/guides/AGENTS.md`) is required or optional and what its content should be.
4. Whether `scaffold_marketplace_json.py` should also validate that `plugins` entries match `codex-marketplace/manifest.json`.
5. Whether `repo_standards.py` should call `validate-agent-mesh` directly in `--check` mode or leave that to `ci-preflight`.
6. How to handle the temporarily disabled pre-commit hook (restore now, add an exception, or restore after PR merge).
