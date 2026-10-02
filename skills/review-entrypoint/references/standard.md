# Review Entrypoint Standard

**Standard ID:** `review-entrypoint`

## Pledge

The repository maintains code review guidance at root `REVIEW.md` and keeps that guidance useful for its review work.

## Required implementation

- Maintain a root `REVIEW.md` with review invariants and/or effective routes to the repository's review guidance.
- Keep the guidance relevant to the repository's review process. The repository chooses whether to write it inline, link to a playbook or runbook, or combine those forms.
- Root `AGENTS.md` routes to subscription and certification as part of AOM adoption. The REVIEW standard does not require a particular AGENTS layout.
- The repository self-certifies that the root document is maintained and useful to its review workflow.

## Conditional obligations

No deeper scoped REVIEW files, book inventory, fan-out, or adoption of another standard is required. Review-product loading behavior is harness-specific and does not prove that every coding agent reads this file during ordinary work.

## Self-certification

Identify the root entrypoint, its maintenance owner or route, and how its usefulness is reviewed. Certification must describe the actual review workflow.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may offer an editable root starter. The repository owns its content and may replace or omit the starter after maintaining a conforming root guide.
