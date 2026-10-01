# Adoption and certification

## Subscription

A repository adopts a standard by recording an explicit subscription in `.agents/contracts/operating-standards.json`. Each v2 subscription identifies the standard ID, source repository, full immutable Git commit, definition path, and repository-owned certification reference. The default certification location is `.agents/contracts/standards-certification.md`. The record identifies authority and routing; it does not prove compliance.

The repository owns its implementation. It may take, edit, or replace optional starter assets. A standard may have no deployable assets. Adoption does not require a particular checker unless the standard definition says so. AOM does not install assets automatically.

Any explicit AOM standard adoption opts the repository into having a root `AGENTS.md` entrypoint. Create it if absent. Keep it as an orientation and progressive-discovery router; the selected standards determine its substantive obligations.

## Self-certification

The certification is a human-readable, agent-facing statement of the adopted standards, how the repository satisfies each required invariant, and the measures that detect or prevent drift. Put it in a location agents can discover, normally the default certification path above. Where the repository adopts agent-doctrine-and-contracts, the certification itself is agent doctrine that records invariants to preserve.

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
