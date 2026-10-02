# Contribution Entrypoint Standard

**Standard ID:** `contribution-entrypoint`

## Pledge

The repository maintains root `CONTRIBUTING.md` with enough guidance to direct a contributor through the applicable contribution process.

## Required implementation

- Keep the root document sufficient to find and follow the repository's contribution process. Guidance can be inline, routed to existing material, or both.
- Keep references usable and the entrypoint maintained as the process changes.
- The repository self-certifies that contributors can use the document to discover the applicable process.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification, but this standard does not prescribe how CONTRIBUTING is linked from AGENTS.

## Conditional obligations

No heading scheme, document fan-out, runbooks, playbooks, or other standard is required. Git hosting products may recognize alternate CONTRIBUTING locations; this standard selects the repository root as its convention.

## Self-certification

Identify the root guide, its operative routes or inline process, and how its usefulness and references are maintained.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM may offer an editable starter. The repository owns and may change or replace it.
