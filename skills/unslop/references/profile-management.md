# Managing Unslop Profiles

An unslop profile protects a repository from repeated agent mistakes with durable, actionable guidance. Treat it as a working feedback loop, not a one-time prediction exercise.

## Record and connect occurrences

When an agent recognizes a recurring mistake or a near miss, add a concise observation under `.agents/unslop/`. Include enough context to distinguish a new incident from a duplicate report and link it to a candidate pattern or existing guard. Record whether the relevant guard was available, read, followed, and effective when that can be established.

## Improve only from evidence

Compare distinct incidents before treating a behavior as a pattern. Write or revise a guard when evidence shows a repeated mistake or a useful near miss. State the recognition cue, corrective action, applicable scope, and boundaries that prevent false positives. Keep candidate observations when the evidence does not yet support a durable rule.

## Review the result

After later work, assess whether the guard reached the agent and changed the behavior. Missing routing calls for a better route. A guard that was read but did not help calls for a clearer or narrower correction. A useful guard that was ignored calls for addressing the decision point where it was bypassed. A duplicate observation does not count as independent recurrence.

## Scale with the repository

A small repository can keep profiles and observations in `.agents/unslop/repo.md`. Split by concern when that improves discovery and ownership. Route the relevant profile from the point where the agent needs it, such as a playbook or runbook when the repository has those. Otherwise use another route agents encounter. Ambient profile-authoring skills may help, but the method remains usable without them.

Retire a guard when evidence shows it no longer applies or has been replaced. Preserve the observations needed to understand why the change was made.
