# Runbook Composition Standard

**Standard ID:** `runbook-composition`

## Pledge

The repository's runbooks are lifecycle-stage guides for work that happens in the repository. Each maintained runbook explains when the stage applies, how work proceeds, and what completion means for that stage.

## Required implementation

- Every document treated as a runbook is a stage lifecycle guide, not a topical playbook or an empty placeholder.
- Maintained runbooks are useful for their stated stage, have clear applicability, and can be reached through effective inbound routing at the relevant work point.
- References used by a runbook resolve and retain clear ownership. The repository self-certifies that its runbooks match this category and support its actual workflow.
- The repository chooses its document layout, headings, inventory, and compliance chain. Do not create empty sections to imitate a template.
- AOM adoption requires root `AGENTS.md` routing to the subscription and relevant certification; it does not require this standard's documents to follow one universal AGENTS or book format.

## Conditional obligations

When the repository also adopts playbook composition, route each lifecycle stage to relevant concern guides with clear conditions. Keep lifecycle procedure in runbooks and reusable cross-stage concern guidance in playbooks. This routing does not create a minimum inventory for either kind of book.

Runbooks can stand alone when playbooks are absent. They can carry the operating knowledge needed for the stage directly or point to repository-owned capabilities and guidance that are actually available.

## Self-certification

The repository explains which stage lifecycle guides implement the pledge, how agents discover them at the stage, how references stay valid, and how category and usefulness are reviewed. Structural checks may support this assessment; file existence or a heading list alone cannot certify it.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM offers five optional starter runbooks for design, planning, implementation, code review, and PR work, plus an optional checker. Select any subset, adapt them, supply repository-authored guides, or use none of the starters. The standard requires useful stage guidance, not these five documents or their original text.
