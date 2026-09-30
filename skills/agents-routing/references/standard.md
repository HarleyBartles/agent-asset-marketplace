# AGENTS Routing Standard

**Standard ID:** `root-agent-router`

## Pledge

The repository maintains every `AGENTS.md` as a brief, safe router for progressive discovery. Agents working in the repository can find applicable authoritative guidance without receiving the whole doctrine corpus on every turn.

## Required implementation

- Keep root and domain routers concise. They orient the agent and point to authoritative material with conditions that say when to read it.
- Use rich routers at natural domain boundaries when a large repository needs delegation. Use thin scoped routers to state the affected tree and the guidance to read for work in that scope.
- Keep doctrine, contracts, long procedures, and detailed policies in their owning documents. `AGENTS.md` describes routes and scope; it does not duplicate that authority.
- Thin scoped routers state the affected tree and read condition in one sentence. Rich root and domain routers divide orientation at natural repository boundaries so the root stays a brief, always-on entrypoint.
- Set and document repository-owned budgets and placement policy that fit the repository. Prevent both per-file sprawl and a confusing router at every directory boundary.
- Provide a repository-owned checker that applies the chosen budgets and structure policy. Semantic review must still assess whether routers are brief, safe, scoped, and useful.
- If CI exists, run the checker in CI. If the repository also adopts the tracked hook/CI standard, the hook and hosted CI have equivalent coverage.
- Any AOM adoption creates or updates root `AGENTS.md` to route agents to the subscription and applicable certification. That shared adoption requirement does not adopt this full standard.

## Conditional obligations

CI integration applies when CI exists. Hook parity applies when the repository adopts the tracked hook/CI standard. These conditions do not adopt either standard.

## Self-certification

The repository identifies its router locations, policy, checker, CI route where applicable, and semantic review measure. Certification describes the actual policy and how agents maintain it. File counts or checker success alone do not establish useful routing.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may supply an editable checker starter. The investigated 55-line warning and 100-line error are starter defaults only. The repository chooses its own thresholds, locations, checks, and implementation, then owns them. No fixed maximum number of `AGENTS.md` files is imposed.
