# Agents Mesh Discoverability Design Receipt

**Goal:** Make repository documentation discoverable by agents at the right time by refreshing the agents mesh, tightening the mesh policy, and adding scoped `AGENTS.md` nodes where they materially improve routing.

**Approved boundary:** this work is about agent-facing routing, doctrine placement, and generated navigation. It does not change marketplace content, skill semantics, or validation behavior except where a doc-routing rule needs a matching validation/reference update.

## Context

The repo already has a mesh, but it is not yet as explicit as the Wild Bunch pattern. The current surfaces show the right ingredients:

- root `AGENTS.md` for global repo doctrine
- `.agents/docs/mesh-policy.md` for the current mesh statement
- `.agents/docs/AGENTS.md` and `docs/AGENTS.md` for scoped doc-facing guidance
- generated `INDEX.md` files for navigation
- multiple workflow guides under `.agents/docs/guides/`

What is missing is a stronger routing posture:

- `AGENTS.md` nodes should be slim and mostly tell agents what to read and when to read it.
- doctrine-length guidance should live in repo doctrine files, not in every injected node.
- scoped `AGENTS.md` files should exist where they create real routing value, especially around doc-heavy or workflow-heavy surfaces.
- the mesh policy should define that separation clearly enough that future agents can keep the mesh discoverable without bloating context.

## Design

The update will establish one repo-wide rule set and then apply it through a small set of scoped routing seams.

### 1. Canonical mesh policy

`.agents/docs/mesh-policy.md` becomes the canonical policy for:

- the roles of `AGENTS.md`, `INDEX.md`, `README`, and doctrine files
- the rule that `AGENTS.md` is routing surface, not doctrine container
- the rule that `INDEX.md` is generated navigation only
- the rule that doc-heavy guidance belongs in `.agents/docs/`
- the self-healing expectation for stale or misleading mesh content

This policy should explicitly say that the purpose of `AGENTS.md` is to tell agents:

- what to read
- when to read it
- where the next relevant surface is

It should also capture the practical size heuristic already used in this repo: keep `AGENTS.md` slim, with roughly 30 lines as the target and more only when a scoped node genuinely needs extra routing detail.

### 2. Routing seams

The planning phase should build out the following routing seams.

| Surface | Expected role |
| --- | --- |
| `AGENTS.md` | Root law and pointer to the core doctrine surfaces; no long-form guidance |
| `.agents/AGENTS.md` | `.agents/` routing node with pointers into `.agents/docs/` and generated indexes |
| `.agents/docs/AGENTS.md` | Docs doctrine node with pointers to mesh policy and doc-local guidance |
| `.agents/docs/guides/AGENTS.md` | New scoped routing node for the guides subtree |
| `docs/AGENTS.md` | Human/docs surface routing node that points agents at docs-owned doctrine |
| `docs/contracts/AGENTS.md` | New scoped routing node if the contracts subtree needs its own “read when” guidance |
| `tools/AGENTS.md` | Workflow routing node for generator and validation commands |
| `codex-marketplace/AGENTS.md` | Marketplace projection routing node |
| `codex-marketplace/plugins/AGENTS.md` | Plugin-root routing node |
| `adapters/AGENTS.md` | Adapter/projection routing node |
| `sources/AGENTS.md` | Source-custody routing node |
| `provenance/AGENTS.md` | Provenance/evidence routing node |

The planner should verify each seam against the live tree and only add new `AGENTS.md` files where the node carries distinct routing value. The important part is not maximizing node count; it is placing route guidance close enough to the work that agents encounter the right read set before they mutate the wrong surface.

### 3. Scoped guidance pattern

Every scoped `AGENTS.md` added or updated by this work should follow the same shape:

- identify the scope at the top
- describe what law that scope owns
- list “read when” pointers to the doctrine docs relevant to that scope
- avoid restating long doctrine blocks already carried elsewhere
- keep any local deltas short and specific to the subtree

If a node starts carrying substantive doctrine, that content belongs in `.agents/docs/<topic>.md` and the `AGENTS.md` file should collapse back to routing pointers.

### 4. Guide discoverability

The `.agents/docs/guides/` subtree should become a first-class discovery surface rather than a flat file list. The new scoped guide `AGENTS.md` should point agents to the right guide based on task stage:

- design / shaping work -> design and planning docs
- implementation work -> implementing guide
- review work -> code-review guide
- marketplace generation or projection work -> marketplace-generation guide
- skill/document authoring work -> skill-authoring guide

That node should be backed by the generated `INDEX.md` for the subtree, but the `AGENTS.md` file is what teaches agents when to look there.

### 5. Mesh self-healing and generated navigation

The generated `INDEX.md` mesh should stay authoritative for “what is here.” If this work adds or removes any documentation directories or new scoped nodes, regenerate the relevant indexes rather than hand-editing the generated files.

The validation story should keep the repo honest about mesh drift:

- if the authored mesh changes, update the affected `AGENTS.md` files in the same change
- if the navigation mesh changes, regenerate the whole index mesh
- if the generator or validation cannot express the intended routing cleanly, fix the tooling rather than hand-writing exceptions

## Options Considered

### Option A: Policy-only refresh

Update `.agents/docs/mesh-policy.md` and the existing root/scoped `AGENTS.md` files, but do not add new scoped nodes.

- Pros: smallest diff, least churn
- Cons: discoverability remains coarse in doc-heavy subtrees; the repo still relies on broad top-level pointers

### Option B: Policy plus targeted scoped nodes

Refresh the mesh policy and add new scoped `AGENTS.md` nodes only where they materially improve routing, especially under `.agents/docs/guides/` and any other doc-heavy subtree that lacks a local entrypoint.

- Pros: matches the Wild Bunch pattern, keeps `AGENTS.md` slim, improves “read when” timing
- Cons: slightly larger diff, requires a careful seam audit

### Recommendation

Choose **Option B**. The user-facing problem is not just policy wording; it is timely discoverability. That requires both a stronger policy and the actual scoped routing nodes that point agents to the right documents.

## Validation and Acceptance

The implementation plan should require:

- regenerated index mesh after any directory or file additions/removals that affect discovery
- a review pass confirming that scoped `AGENTS.md` files remain slim and routing-focused
- a check that the new or updated nodes point to doctrine files rather than duplicating long guidance
- a review pass confirming that the repo’s root and scoped AGENTS surfaces are enough to discover the relevant docs without searching the tree manually

Success means an agent entering the repo can tell, from the injected `AGENTS.md` surfaces alone, which doctrine files to read next for the current stage of work.
