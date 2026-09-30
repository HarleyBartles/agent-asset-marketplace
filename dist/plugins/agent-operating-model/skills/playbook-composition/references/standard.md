# Playbook Composition Standard

**Standard ID:** `playbook-composition`

## Pledge

The repository's playbooks guide kinds of work or concerns that can arise across lifecycle stages. A playbook explains when its concern applies and how to handle it.

## Required implementation

- Every document treated as a playbook is concern guidance, not a lifecycle-stage guide or an empty placeholder.
- Playbooks provide enough guidance to perform the concern directly or within a stage. They have clear applicability, effective inbound routing at relevant work points, and usable references.
- A playbook may compose relevant capabilities, doctrine, contracts, commands, paths, evidence expectations, and related playbooks. Include only what exists and is useful.
- No fixed inventory, heading list, section set, or empty composition slot is required.
- The repository self-certifies category, usefulness, reachability, and upkeep using its own compliance chain.
- AOM adoption requires root `AGENTS.md` routing to the subscription and relevant certification. It does not impose a universal book format.

## Capability references

Distinguish capability source and availability:

- Repository-authored skills are named and linked to their repository-owned location.
- Skills from a plugin declared in the repository are referenced by plugin-qualified name. Repository plugin declarations make the dependency available to a fresh clone subject to its harness and access prerequisites.
- Ambient skills are referenced by capability description and identified as environment-provided. Do not imply that a personal ambient plugin is available to every clone.

## Conditional obligations

Playbooks stand alone without runbooks or an agent doctrine/contracts store. If authoritative operating knowledge exists, link it and explain how it applies. Otherwise the playbook can carry the necessary knowledge inline. A repository may adopt doctrine/contracts separately when it wants shared stores.

When both runbook and playbook standards are adopted, relevant stages route to applicable concern guides. Keep one clear owner for shared topical guidance; no all-to-all or mandatory reciprocal links are required.

## Self-certification

The repository identifies its concern guides, the routes that make them available when relevant, and how it checks category, useful composition, reference validity, and upkeep. A checker can support mechanical integrity but cannot establish semantic usefulness by headings alone.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may supply editable example playbooks and a checker. The repository can select, adapt, replace, or omit each. Optional assets do not establish adoption and do not set a mandatory inventory.
