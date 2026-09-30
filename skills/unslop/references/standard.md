# Unslop Standard

**Standard ID:** `unslop`

## Pledge

The repository maintains effective unslop profiles and the feedback loop needed to improve them from recurring agent mistakes. Agent slop is a repeated or recurring mistake in repository work, including coding, tests, architecture, writing, or another relevant concern.

## Required implementation

- Use `.agents/unslop/` as the canonical profile and observation location.
- Record occurrences durably across agents and sessions. Keep enough evidence to connect distinct incidents, distinguish recurrence from duplicate reports, and assess whether a guard was reached and effective.
- Maintain actionable guards for encountered patterns. A guard describes recognition cues, corrective behavior, applicability, and false-positive boundaries clearly enough to use.
- Make profiles effectively reachable where relevant work happens. If runbooks or playbooks exist, route profiles from relevant stages and concerns. Otherwise provide another effective route.
- Review whether the guard was discoverable, followed, and effective. Distinguish absent routing, ineffective correction, and ignored useful guidance.
- Create, revise, narrow, consolidate, or retire profile content in response to observed evidence. Speculative static files or an unread inventory do not satisfy this pledge.
- Agents maintain the feedback loop as part of repository work. AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

Profiles may live in `.agents/unslop/repo.md` in a small repository or grow into files grouped by slop class. Occurrence records may be alongside a guard or linked to it. No separate database, file-per-pattern rule, fixed heading schema, telemetry service, or particular book standard is required.

## Self-certification

Describe where profiles and observations live, how agents record and connect occurrences, the route to applicable guards, and how the repository acts on evidence of failure or success. Certification should show that profile maintenance is current and used.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM provides a standalone profile management guide. Templates, observation formats, and structural checkers are optional support and cannot prove an effective feedback loop. Ambient Unslop+ or another profile authoring capability can assist; it is not required.
