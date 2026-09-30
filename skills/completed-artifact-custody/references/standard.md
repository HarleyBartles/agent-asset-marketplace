# Completed Artifact Custody Standard

**Standard ID:** `completed-artifact-custody`

## Pledge

Agents follow next-slice retirement for plans, specifications, roadmaps, checkpoints, and similar execution artifacts. Completed artifacts remain through their completing PR, then are retired in the first commit of the next substantive slice.

## Required implementation

- Treat a completed artifact as no longer current authority even while it remains tracked through its completing PR.
- At the next substantive slice, identify semantically completed artifacts and retire eligible ones in that slice's first commit.
- Determine completion from the whole artifact scope and repository evidence. Checked boxes and evidence that the governed work is implemented are useful cues even without a special keyword.
- Preserve future plans and other still-live work. A completed item inside a roadmap does not make the entire roadmap complete.
- Before removal, promote enduring knowledge to its durable home and remove stale links and indexes.
- Treat abandonment as an explicit decision that preserves durable knowledge. Inactivity, scratch rejection, or deletion do not establish abandonment.
- If no later substantive slice occurs, a completed artifact may remain tracked without regaining authority.
- Maintain the repository's measure for agents to perform this classification and retirement. A marker may record state but cannot be the sole discovery path or prerequisite.
- AOM adoption requires root `AGENTS.md` routing to subscription and certification.

## Conditional obligations

Where runbooks or playbooks exist, route this lifecycle at the relevant completion and new-slice work points. Their adoption is not required by this standard.

## Self-certification

Describe the next-slice practice, the route by which agents inspect artifacts, how completion and future work are distinguished, and where durable content is promoted. Evidence should show the process is maintained, not just a marker convention.

## Subscription and continuing certification

Record this standard's ID, source repository, immutable commit, definition path, and certification reference in `.agents/contracts/operating-standards.json`. The readable certification defaults to `.agents/contracts/standards-certification.md` and states where the implementation lives, what agents must preserve, how drift is prevented, and what evidence is mechanical or judgment-based. Every agent changing an affected surface maintains the certification. Using these paths does not adopt the separate agent doctrine/contracts standard. AOM adoption also requires root `AGENTS.md` routing to these records.

## Optional AOM assets

AOM can provide guidance and implementation support for semantic discovery. Any starter becomes repository-owned and may be adapted. Ambient capability availability alone does not adopt this standard.
