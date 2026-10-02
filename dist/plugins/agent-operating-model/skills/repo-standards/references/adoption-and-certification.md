# Adoption and certification

## Subscription

A repository adopts a standard by recording an explicit subscription in `.agents/contracts/operating-standards.json`. Each v2 subscription identifies the standard ID, source repository, full immutable Git commit, definition path, and repository-owned certification reference. The default certification location is `.agents/contracts/standards-certification.md`. The record identifies authority and routing; it does not prove compliance.

The repository owns its implementation. It may take, edit, or replace optional starter assets. A standard may have no deployable assets. Adoption does not require a particular checker unless the standard definition says so. AOM does not install assets automatically.

Any explicit AOM standard adoption opts the repository into having a root `AGENTS.md` entrypoint. Create it if absent. Keep it as an orientation and progressive-discovery router; the selected standards determine its substantive obligations.

## Adoption workflow

1. Confirm which standard or standards the human asked to adopt. Use the current catalog to locate definitions; do not add adjacent standards because a template, tool, or shared directory exists.
2. Read each definition from its declared source and immutable commit. Verify that the source checkout matches the declared repository before using the pinned reader. If the repository has an existing pin, assess it on its own authority first.
3. Identify required invariants and optional assets for each requested standard. Select only useful optional assets. Treat every example as input for a repository edit, not a file to overwrite authored content with.
4. For a new adoption, create the v2 subscription with a published immutable definition pin and initialize certification as not yet certified. For an existing subscription upgrade, keep the current pin authoritative while implementing and assessing the new definition; update the pin and certification together only after the revised implementation and compliance chain are established. Keep repository-owned files and current gates intact. Do not install assets automatically or register them on a command bus without an explicit repository task.
5. If a root `AGENTS.md` is absent, create a brief orientation and route to the subscription and certification. If it already exists, preserve it and add only the missing route needed for those records.
6. Implement the required behavior in the repository. Select only useful optional assets and adapt them as repository-owned files. Do not treat template presence as implementation.
7. Run the repository's own compliance chain and assess the semantic requirements. Record accurate status, implementation locations, evidence, and drift controls in the readable certification. A structural checker can validate records and selected mechanical facts; its successful exit never certifies the standard.
8. If required behavior remains incomplete, report partial adoption plainly. Do not claim compliance. Keep certification marked as not yet certified or describe the actual state; complete the implementation before asserting the pledge is met.

If the repository has a v1 record, do not replace it as a side effect of a new adoption. Resolve the v1-to-v2 record transition as explicit migration work while preserving the existing pinned obligations. If a requested adoption changes an existing v2 pin, compare both definitions and reconcile the implementation and certification in the same explicit update task.

## Self-certification

The certification is a human-readable, agent-facing statement of the adopted standards, how the repository satisfies each required invariant, and the measures that detect or prevent drift. Put it in a location agents can discover, normally the default certification path above. Where the repository adopts `agent-doctrine-contracts`, the certification itself is agent doctrine that records invariants to preserve.

Certification is semantic and repository-owned. A structural checker can report facts it can observe, but it cannot record or establish certified success by itself. When observed repository state conflicts with a certification claim, report the mismatch. Preserve the pinned standard. Repair the implementation or revise the certification to describe the actual state; change a checker only when evidence shows the checker misrepresents the pinned requirement.

Every agent changing an adopted surface is responsible for preserving or updating its certification and drift controls. Adoption is continuing responsibility, not a one-time scaffold event.

## Selecting optional assets

Read the pinned definition and distinguish required invariants from optional starter assets. Deploy only the assets the repository chooses. A repository can take a starter unchanged, adapt it, implement an equivalent approach, or omit optional assets while still self-certifying the required behavior. Do not create empty files or sections merely to resemble a template.

For example, runbook-composition offers a starter set of lifecycle-stage guides and a checker as optional accelerators. A repository can select any subset or none. If it adopts both runbook and playbook composition, it wires the selected lifecycle guides to relevant concern guides. No standard implies a fixed inventory of books.

## Assessment and upgrades

1. Read the subscription record and its certification reference before assessing the repository.
2. For v1, inspect the deployed authority and its recorded historical source. Assess against that pinned version; do not execute today's scaffolder or silently migrate.
3. For v2, retrieve the definition from its exact source repository, full commit, and path. A removed catalog entry does not invalidate an existing pin.
4. Compare observed implementation and drift measures with the pinned invariants and the certification. Report gaps accurately.
5. Upgrade only when explicitly requested. Reconcile the selected new definition against the repository implementation and certification, then record the new pin as part of that task.

An absent record means the repository has not adopted these standards. If the user asks to adopt one, add only that selection, implement its required invariants, and add the routing and certification surfaces needed to make that implementation discoverable and maintainable. The record and root router alone do not establish compliance. Current catalog entries are choices, not a checklist.

The [subscription example](../assets/templates/operating-standards-v2.example.json), [root router example](../assets/templates/AGENTS.md.example), and [certification example](../assets/templates/standards-certification.md.example) illustrate these records and routes. The certification example begins in a not-certified state and must be replaced with repository evidence before anyone can honestly claim compliance.
