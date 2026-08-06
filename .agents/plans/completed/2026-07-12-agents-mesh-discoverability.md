# Agents Mesh Discoverability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the repo-wide agents mesh so documents are discoverable by agents at the right time. The implementation must keep `AGENTS.md` files slim routing surfaces, move durable guidance into the repo doctrine area, and add scoped `AGENTS.md` nodes where they materially improve routing.

**Source design:** Agents Mesh Discoverability Design Receipt

**Scope boundary:** this work changes mesh policy, scoped routing nodes, and generated navigation only. It does not change marketplace content, skill behavior, or generated marketplace artifacts.

## Global Constraints

- Do not begin implementation until this plan is approved.
- Keep the work to one branch and one PR.
- Use the existing repo doctrine and docs surfaces. Do not invent a second mesh policy.
- Keep `AGENTS.md` files short. The target is routing guidance, not long-form doctrine.
- Put durable guidance in `.agents/docs/` or `docs/`, not in every injected `AGENTS.md`.
- Add new scoped `AGENTS.md` nodes only where they create real routing value.
- Do not hand-edit generated `INDEX.md` files. Regenerate them through `py -3 tools/generate_index_mesh.py`.
- No marketplace rebuild is expected for this change unless the implementation discovers a hidden dependency on marketplace or skill surfaces.
- If the implementation discovers that a scope does not need a new `AGENTS.md` node, document the decision and keep the plan honest rather than forcing the file.

## Preflight Evidence

Current live repo inspection shows:

- root `AGENTS.md` is still carrying a lot of marketplace and publication detail
- `.agents/doctrine/mesh-policy.md` already exists but is short and not yet as explicit as the Wild Bunch mesh policy
- `.agents/docs/guides/AGENTS.md` does not exist
- `.agents/docs/contracts/AGENTS.md` does not exist
- `docs/AGENTS.md`, `tools/AGENTS.md`, `codex-marketplace/AGENTS.md`, `codex-marketplace/plugins/AGENTS.md`, `adapters/AGENTS.md`, `sources/AGENTS.md`, and `provenance/AGENTS.md` already exist and are slim enough to keep, but they do not yet route agents by work stage

The generated navigation surfaces that will change are:

- `.agents/superpowers/plans/INDEX.md`
- `.agents/docs/INDEX.md`
- `.agents/docs/guides/INDEX.md`
- `docs/INDEX.md`
- `.agents/docs/contracts/INDEX.md`

## Plan

- [x] Step 0: Verify the live routing seams before writing files
- [x] Step 1: Rewrite the canonical mesh policy and trim the root routing nodes
- [x] Step 2: Add scoped routing nodes for guides and contracts, and tighten the existing subtree nodes
- [x] Step 3: Regenerate the index mesh and validate the generated navigation

---

## Step 0: Verify the live routing seams before writing files

Before editing anything, re-open the live files that define the current mesh shape and confirm the target seam list:

- `AGENTS.md`
- `.agents/AGENTS.md`
- `.agents/docs/AGENTS.md`
- `.agents/doctrine/mesh-policy.md`
- `docs/AGENTS.md`
- `.agents/docs/contracts/INDEX.md`
- `.agents/docs/contracts/skill-frontmatter.md`
- `.agents/docs/contracts/openai-agent-yaml.md`
- `tools/AGENTS.md`
- `codex-marketplace/AGENTS.md`
- `codex-marketplace/plugins/AGENTS.md`
- `adapters/AGENTS.md`
- `sources/AGENTS.md`
- `provenance/AGENTS.md`
- `.agents/docs/guides/INDEX.md`

Confirm that `.agents/docs/contracts/` is a meaningful routing boundary because it contains only the two contract docs and the generated index. Confirm that the guides subtree is the right place for stage-based routing because it already contains design, planning, implementing, review, marketplace-generation, and skill-authoring guidance.

**Expected result**

- the file list for the mesh update is final
- the implementation does not invent a new seam after work starts

**Commit message**

- `docs: plan mesh discoverability refresh`

---

## Step 1: Rewrite the canonical mesh policy and trim the root routing nodes

**Files:**

- Modify: `.agents/doctrine/mesh-policy.md`
- Modify: `AGENTS.md`
- Modify: `.agents/AGENTS.md`
- Modify: `.agents/docs/AGENTS.md`
- Modify: `docs/AGENTS.md`

**Implementation shape**

Update `.agents/doctrine/mesh-policy.md` so it becomes the repo's canonical statement about documentation routing. It should explicitly define each surface separately:

- `AGENTS.md` files are routing law and scoped agent instruction, not doctrine storage
- `INDEX.md` files are generated navigation and coverage only
- `README.md` files are human-facing explanation only
- `docs/` files are docs-owned guidance and doctrine surfaces, but they are not the same thing as generated navigation
- the self-healing rule for stale mesh content
- the slim-node heuristic: `AGENTS.md` files should stay short and should mostly tell agents what to read and when to read it

Trim the root `AGENTS.md` so it keeps only these sections:

- repo purpose
- source-of-truth split
- publication proof
- a short pointer set to the scope-specific `AGENTS.md` files and the mesh policy

The root file should retain a short pointer block that names the next routing surfaces explicitly:

- `.agents/AGENTS.md` for tracked agent doctrine
- `.agents/doctrine/mesh-policy.md` for mesh-specific law
- `docs/AGENTS.md` for docs-owned guidance
- `tools/AGENTS.md` for generators and validators
- `codex-marketplace/AGENTS.md` for marketplace source/projection law
- `sources/AGENTS.md` for source custody
- `adapters/AGENTS.md` for adapter and overlay work
- `provenance/AGENTS.md` for provenance and trust evidence

The root file must stop carrying the following long-form guidance. That material belongs in the scoped nodes listed below or in the docs referenced by those nodes:

- deterministic pack rule and projection pipeline detail
- `house-skills` / project-pack exposure policy
- upstream drain rule
- no-dodge execution rule
- before-changing-files guidance
- versioned House Skills update notes
- shared local worker checkout start gate
- worktree location note
- PR mergeability, review-thread closure, validation, closeout, and maintenance instructions that belong in narrower docs

Move marketplace/tooling detail out of the root node and into the scope-specific nodes listed below. The root file should not carry long marketplace regeneration guidance once the subtree nodes are in place.

Update `.agents/AGENTS.md` so it becomes the tracked agent-doctrine entrypoint for `.agents/` and points agents at `.agents/doctrine/mesh-policy.md`, `.agents/docs/INDEX.md`, and the docs/guides and docs/contracts routing nodes instead of repeating doctrine.

Update `.agents/docs/AGENTS.md` so it points agents at the mesh policy, the docs index, `.agents/docs/guides/AGENTS.md`, and `.agents/docs/contracts/AGENTS.md`.

Update `docs/AGENTS.md` so it routes agents into the docs-owned guidance surfaces, including `.agents/docs/contracts/AGENTS.md`, `docs/INDEX.md`, and `.agents/docs/unslop/profile.md`, instead of leaving the docs tree as a single broad bucket.

**Expected result**

- the repo has one clear mesh policy
- the root `AGENTS.md` is slimmer and mostly routing/pointer content
- `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, and `docs/AGENTS.md` are routing surfaces rather than mini-doctrine dumps

**Commit message**

- `docs: tighten mesh policy and root routing`

---

## Step 2: Add scoped routing nodes for guides and contracts, and tighten the existing subtree nodes

**Files:**

- Create: `.agents/docs/guides/AGENTS.md`
- Create: `.agents/docs/contracts/AGENTS.md`
- Modify: `tools/AGENTS.md`
- Modify: `codex-marketplace/AGENTS.md`
- Modify: `codex-marketplace/plugins/AGENTS.md`
- Modify: `adapters/AGENTS.md`
- Modify: `sources/AGENTS.md`
- Modify: `provenance/AGENTS.md`

**Implementation shape**

Create `.agents/docs/guides/AGENTS.md` as the stage-routing entrypoint for the guides subtree. It should be short and should route agents by work stage:

- design or shaping work -> `design-guide.md`
- planning work -> `planning-guide.md`
- implementation work -> `implementing-guide.md`
- code review work -> `code-review-guide.md`
- marketplace generation or projection work -> `marketplace-generation-guide.md`
- skill or document authoring work -> `skill-authoring-guide.md`

The file should point to `.agents/docs/guides/INDEX.md` as the generated file list, but the AGENTS node is what teaches agents when to look there.

Create `.agents/docs/contracts/AGENTS.md` as the local routing node for the contract docs subtree. It is required because `.agents/docs/contracts/` contains a distinct contract-doc boundary with only two authored docs. It should tell agents to read:

- `skill-frontmatter.md` when editing skill frontmatter contracts or projection metadata contracts
- `openai-agent-yaml.md` when editing OpenAI agent YAML contract surfaces
- `docs/AGENTS.md` when they need the broader docs-routing context

Tighten the existing subtree nodes so they point into the new mesh instead of carrying generic guidance:

- `tools/AGENTS.md` must include explicit "read when" pointers to:
  - `.agents/doctrine/mesh-policy.md` before changing generator or validator behavior
  - `.agents/docs/guides/planning-guide.md` before planning tool changes
  - `.agents/docs/guides/implementing-guide.md` before implementing tool changes
  - `.agents/docs/guides/marketplace-generation-guide.md` before changing marketplace regeneration behavior
  - `.agents/docs/guides/code-review-guide.md` before reviewing tooling changes
- `codex-marketplace/AGENTS.md` must include explicit "read when" pointers to:
  - `docs/custody-and-projection-doctrine.md` before marketplace source/projection changes
  - `.agents/doctrine/mesh-policy.md` before changing marketplace routing or mesh references
  - `tools/AGENTS.md` before changing generators, validators, or regeneration assumptions
  - `codex-marketplace/plugins/AGENTS.md` before plugin-root changes
- `codex-marketplace/plugins/AGENTS.md` must include explicit "read when" pointers to:
  - `codex-marketplace/AGENTS.md` before plugin-root or bundle-manifest changes
  - `tools/AGENTS.md` before changing projection or validation behavior
  - `docs/custody-and-projection-doctrine.md` before any projection or provenance claim changes
- `adapters/AGENTS.md` must include explicit "read when" pointers to:
  - `docs/custody-and-projection-doctrine.md` before adapter or overlay work
  - `.agents/doctrine/mesh-policy.md` before changing adapter routing or generated navigation assumptions
- `sources/AGENTS.md` must include explicit "read when" pointers to:
  - `docs/custody-and-projection-doctrine.md` before source-custody edits
  - `.agents/doctrine/mesh-policy.md` before changing how source custody is surfaced to agents
- `provenance/AGENTS.md` must include explicit "read when" pointers to:
  - `docs/custody-and-projection-doctrine.md` before provenance or trust-record edits
  - `.agents/doctrine/mesh-policy.md` before changing how evidence surfaces are routed
  - `docs/AGENTS.md` before docs-owned evidence surfaces are changed

Keep each scoped file short. If a file grows into substantive doctrine, move that doctrine into `.agents/docs/` or `docs/` and leave the AGENTS node as a pointer.

**Expected result**

- guides become a stage-aware discovery surface instead of a flat list of files
- the contracts subtree gets a local entrypoint instead of relying on the broader docs node
- top-level subtree nodes start telling agents when to read the next doc, not just what the directory contains

**Commit message**

- `docs: add scoped mesh routing nodes`

---

## Step 3: Regenerate the index mesh and validate the generated navigation

**Files:**

- Modify: `.agents/superpowers/plans/INDEX.md`
- Modify: `.agents/docs/INDEX.md`
- Modify: `.agents/docs/guides/INDEX.md`
- Modify: `docs/INDEX.md`
- Modify: `.agents/docs/contracts/INDEX.md`

**Commands:**

```powershell
py -3 tools/generate_index_mesh.py
py -3 tools/generate_index_mesh.py --check
git diff --check
```

**Implementation shape**

Run the index generator after the authored mesh edits are complete so the new `AGENTS.md` files are reflected in the generated navigation. Then run the check mode to prove the mesh is current and finish with `git diff --check` to catch whitespace or patch-format issues.

Spot-check the generated indexes to confirm:

- `.agents/superpowers/plans/INDEX.md` lists this plan file
- `.agents/docs/guides/INDEX.md` includes the new `AGENTS.md`
- `.agents/docs/contracts/INDEX.md` includes the new `AGENTS.md`
- the generated indexes still remain generated files, not hand-edited docs

**Expected result**

- all affected `INDEX.md` files are current
- no hand-edited navigation remains
- the mesh can be discovered from the generated indexes as well as the routing nodes

**Commit message**

- `docs: regenerate mesh indexes`

---

## Verification Checklist

- [x] `.agents/doctrine/mesh-policy.md` defines AGENTS vs INDEX vs docs/README roles clearly
- [x] Root `AGENTS.md` retains only the explicit pointer block and the minimal repo-purpose/source-truth/publication sections
- [x] `.agents/AGENTS.md`, `.agents/docs/AGENTS.md`, and `docs/AGENTS.md` route to the exact target docs named in this plan and do not repeat long doctrine
- [x] `.agents/docs/guides/AGENTS.md` exists and routes by work stage
- [x] `.agents/docs/contracts/AGENTS.md` exists and routes contract-doc work to the right files
- [x] `tools/AGENTS.md`, `codex-marketplace/AGENTS.md`, `codex-marketplace/plugins/AGENTS.md`, `adapters/AGENTS.md`, `sources/AGENTS.md`, and `provenance/AGENTS.md` all point agents at the right doctrine before work starts
- [x] The generated `INDEX.md` files reflect the new routing nodes
- [x] `py -3 tools/generate_index_mesh.py --check` passes
- [x] `git diff --check` passes

## Self-Review

### Scope check

The plan stays on the mesh-discovery slice. It does not introduce marketplace, skill, or projection changes.

### Ambiguity check

The only intentional implementation discretion is whether a scoped node needs one extra read-when pointer to keep the file short and useful. The file-level seams are otherwise fixed. `AGENTS.md`, `README.md`, and `INDEX.md` must remain separate concerns throughout the implementation, and the plan now names the exact target docs each area must point at.

### Confidence

8/10. The current tree and the desired seams are both clear enough to hand off to an implementer without forcing them to invent new structure.
