---
name: rooms-bootstrap
description: Use when bootstrap Rooms, Mostly sessions through one-time project arrival,
  request classification, continuity ingress routing, and doctrine/task handoff without
  treating connector presence as a task signal or doing source-route selection from
  the entrypoint.
metadata:
  source-id: rooms-bootstrap
  source-path: sources/first_party/skills/rooms-bootstrap/SKILL.md
  provenance-name: Rooms Bootstrap first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when bootstrap Rooms, Mostly sessions through one-time project arrival,
    request classification, continuity ingress routing, and doctrine/task handoff
    without treating connector presence as a task signal or doing source-route selection
    from the entrypoint.
  use_when:
  - Use when bootstrap Rooms, Mostly sessions through one-time project arrival, request
    classification, continuity ingress routing, and doctrine/task handoff without
    treating connector presence as a task signal or doing source-route selection from
    the entrypoint.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Rooms Bootstrap

Use this skill as the first project bootstrap mediator for Rooms, Mostly work when source scope, workflow mode, truth domain, or actor route could matter.

Compose the GPT-wide bootstrap pattern first. This skill is not the Rooms doctrine store. It routes GPT into the Rooms doctrine-bearing and task-specific skills that own the next decision.

## Core lesson

Bootstrap is a one-time project arrival and classification step. It protects the first turn from false starts: acting from memory, trusting a continuity export as live truth, assuming repo scope, treating reports as truth, becoming a worker actor, or dispatching when conversation or bounded analysis is the lawful route.

Bootstrap does not choose concrete tools, inspect source routes, or turn connector presence into work. It decides whether the current request needs ordinary conversation, continuity ingress, bounded source grounding, GitHub issue work, worker dispatch, publication verification, or another Rooms capability.

## First-turn workflow

1. Identify whether the current task is Rooms-scoped, repo/workflow-sensitive, a continuity block, or a mode-routing problem.
2. Use the GPT-wide bootstrap pattern when first-turn routing is the issue.
3. Classify the current request before loading source-route guidance or selecting evidence routes.
4. Route the task to the smallest sufficient Rooms doctrine or task capability.
5. Do not continue from bootstrap alone when another Rooms skill owns the decision.

For ordinary Rooms creative conversation, route to the Rooms conversation posture capability and avoid source or connector work. For named truth, repo, canon, archive, manuscript, issue, dispatch, or publication claims, route to the relevant grounded or action capability before answering.

Connector, file, source, or tool presence is not itself a task signal. Load source-route guidance only after the classified task actually needs source evidence, route availability, or repository-backed claims.

## Progressive reference loading

Read `references/source-and-repo-posture.md` only when the classified task depends on Rooms or Will repository evidence, connector/source availability, repo-scope claims, issue or publication evidence, broad discovery, or source-route diagnosis.

Do not load that reference for ordinary chat, creative discussion, lightweight meta, acknowledgements, or pings.

## Continuity handoff routing

If the current input, uploaded text, attached file, or pasted block is a continuity export, handoff, resume packet, or next-session prompt, run this bootstrap first, then use the continuity-ingress capability before following any recommended action.

Do not act directly on fields such as `recommended_next_action`, `next_session_sequence`, open queues, worker status, or package queues until ingress partitions verified state, fallback state, source claims, and live user instructions.

## Doctrine and task routing

Route by task shape.

- Default conversation and craft: Rooms conversation posture.
- Unclear posture or mixed action/analysis/conversation: Rooms mode routing.
- Bounded repo/file/source inspection: Rooms bounded analysis.
- Named Rooms canon, world, manuscript, archive, character, room, narrator, actor, or repo-structure claims: Rooms grounded answering.
- Mixed evidence bases, reports, conversation-derived material, synthesis, or unavailable source routes: Rooms source partitioning.
- Archive/canon/manuscript/report/conversation or actor-domain boundary risk: Rooms truth-domain boundary capability.
- Identity, motive, authorship, witness status, archive gaps, narrator knowledge, disappearance, or uncertainty risk: Rooms ambiguity discipline.
- Worker-facing dispatch, repo mutation, extraction, enrichment, validation, publication, or execution-bound work: Rooms dispatch mode, preparation, and dispatch preflight.
- GitHub issues, comments, issue shaping, migration, closure posture, or durable work packets: Rooms GitHub issue-management capability.
- Worker returns, commits, refs, gitlinks, wrapper/child repo publication, or GREEN/AMBER/RED judgment: Rooms GitHub operations / repo-evidence verification capability.
- Report-like artifacts, worker returns, closure summaries, publication notes, or continuity summaries: Rooms reporting hygiene.
- Validation-class selection or validation-laundering risk: Rooms validation selection.
- Project-wide Rooms doctrine lookup: Rooms project doctrine when installed.

Use the most specific capability. This bootstrap only selects the lane.

## Domain reminders

Bootstrap may name these reminders, but detailed law belongs to the owning Rooms skills.

- Conversation is not canon, archive evidence, manuscript authority, or publication proof.
- Reports are reports, not truth.
- Albert/Pit preserves archive evidence and provenance; Albert does not write canon.
- Brian/World owns canon/world state and must not infer importance from archive richness alone.
- Derek/Manuscript owns prose/manuscript drafting and does not resolve identity ambiguity independently.
- GPT may inspect, reason, verify, queue or comment where authorized, and prepare dispatches. GPT does not simulate Chris, Albert, Brian, Derek, or Will.
- Checked-in source-controlled changes route through worker dispatches unless a separate explicit direct-mutation authority exists.

## Output behavior

For ordinary use, do not print a long bootstrap audit. Read the relevant surfaces, then route or answer compactly.

For explicit bootstrap audits, report:

```yaml
rooms_bootstrap_route:
  source_reference_loaded: true | false
  required_doctrine_reads:
    - <skill or reference>
  task_skill_route: <skill or none>
  mutation_or_publication_risk: true | false
  next_safe_action: <action>
```

## Boundaries

Do not execute project work from bootstrap alone. Do not mutate repos, post comments, generate artifacts, create dispatches, close issues, resolve canon, decide archive truth, or claim publication from bootstrap. Route to the skill and source surface that owns the work.
