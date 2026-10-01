# Managing Unslop Profiles

An unslop profile protects a repository from repeated agent mistakes with durable, actionable guidance. Treat it as a working feedback loop, not a one-time prediction exercise.

## Record and connect occurrences

When a concrete failure or near miss may reveal a recurring agent mistake, inspect the existing observations and add a concise record under `.agents/unslop/` when it adds distinct evidence. Include enough task or work-surface context and a durable evidence reference to distinguish the incident, then connect it to a candidate pattern or existing guard. For example: “Release PR 52 omitted the three-attempt limit from the retry description; this is a separate draft from PR 41. The release workflow did not link the retry-claims guard, and there is no evidence the author read it.”

Record whether the guard could be found, was available at the work point, was read or followed, and changed the result when those facts can be established. Say when the evidence is unknown. Keep the record concise and use the repository's chosen organization; there is no required field list, per-pattern file, or separate database. Do not add every review comment as another occurrence: check whether reports refer to the same underlying work before treating them as independent incidents.

## Improve only from evidence

Agents working in later sessions compare the durable observations before treating a behavior as a pattern. Separate incidents across tasks or work sessions can show recurrence; duplicate comments or reports about one draft cannot. Write or revise a guard when the distinct evidence supports a reusable correction or a near miss reveals a concrete opportunity to prevent the mistake. State the recognition cue, corrective action, applicable scope, and boundaries that prevent false positives. Keep candidate observations when the evidence does not yet support a durable guard.

## Review the result

After later work, assess whether the guard reached the agent and changed the behavior. If it was not routed or available at the work point, improve the route. If it was read but did not help, clarify or narrow the corrective move using the observed failure. If useful guidance was read and ignored, inspect the decision point and address why it was bypassed; do not assume adding more wording will help. A duplicate observation does not count as independent recurrence, and an unknown reach or effect must remain unknown rather than being guessed.

## Scale with the repository

A small repository can keep profiles and observations in `.agents/unslop/repo.md`. Split by concern when that improves discovery and ownership. Route the relevant profile from the point where the agent needs it, such as a playbook or runbook when the repository has those. Otherwise use another route agents encounter. Ambient profile-authoring skills may help, but the method remains usable without them.

Retire a guard when evidence shows it no longer applies or has been replaced. Preserve the observations needed to understand why the change was made.
