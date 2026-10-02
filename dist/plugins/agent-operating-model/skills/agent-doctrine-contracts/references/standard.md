# Agent Doctrine and Contracts Standard

**Standard ID:** `agent-doctrine-contracts`

## Pledge

The repository keeps agent-facing doctrine and contracts discoverable, clear, and fit to govern agent behavior. Doctrine describes what must remain true. Contracts govern the obligations through which agents make it true.

This standard covers agent operating behavior and repository work. A product data schema, public API contract, or model schema is outside scope merely because it uses the words doctrine or contract.

## Required implementation

- Store agent doctrine under `.agents/doctrine/` and agent contracts under `.agents/contracts/`.
- Give each document understandable scope and force. Use direct language for binding doctrine, with an explicit applicability hierarchy wherever obligations could conflict.
- Avoid weak, confusing, or contradictory guidance that leaves an agent to guess which obligation governs.
- Ensure each document is effectively reachable from an entrypoint agents encounter at the relevant work point. Applicability statements corroborate scope; they do not provide discovery by themselves.
- Classify mixed documents by their governing purpose. Split documents when separate obligations need separate ownership or discovery, not merely because one explanatory paragraph discusses procedure.
- Provide and maintain a repository-owned checker for placement, structured validity where applicable, broken references, and reachability within the limits of the repository's discovery mechanisms.
- If CI exists, run the checker in CI. If the repository also adopts the tracked hook/CI standard, its hook has equivalent coverage.
- Review clarity, scope, conflict hierarchy, and usefulness semantically. Mechanical checks must describe their limits, including routes provided by harnesses or non-Markdown references.
- AOM adoption also requires root `AGENTS.md` routing to subscription and certification; that shared requirement does not adopt the full AGENTS routing standard.

## Conditional obligations

When other standards supply contracts, preserve their schema and meaning and record the repository's values and commitments. This standard does not impose a universal wrapper or heading set.

CI and hook integration apply only when those facilities or standards are present; these conditions do not add a subscription.

## Self-certification

Certification names the stores, checker, effective routes, semantic review measure, and the controls that keep them current. A successful placement check does not certify clear doctrine or useful discovery.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. These shared records do not impose a universal schema on other contracts or cover product schemas. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may offer a checker starter and examples. The repository may adapt, replace, or omit them while maintaining the required checker and semantic review itself.
