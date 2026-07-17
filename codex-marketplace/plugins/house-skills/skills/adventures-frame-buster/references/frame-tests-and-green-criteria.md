# Frame Tests and Green Criteria

Read this reference when deciding whether a proposed Adventures frame is green, amber, or red; when
testing story progression, actor interactions, environments, or asset reuse; or when preparing a
frame-buster result.

## Contents

- Green criteria
- Adventure progression test
- Actor and interaction test
- Environment test
- Asset fit test

## Green criteria


A frame is green only when it satisfies all of these:

- It represents the issue's core principle without distorting it.
- It gives Patch an active role, not a decorative role.
- It creates a physical world with recognizable places, props, forces, and consequences.
- It defines Patch's counterparties: named stakeholder/team/agent roles, why Patch interacts with
  them, and what each role needs, blocks, verifies, grants, changes, or receives.
- It preserves Patch singularity: one Patch only, with any other agents defined as distinct
  non-Patch actors rather than Patch clones or Patch-shaped teams/audiences.
- It avoids random background people. If people appear, they should be a defined team, stakeholder
  group, operator, reviewer, requester, verifier, helper, blocker, or other purposeful role.
- It creates purposeful interactions. Patch should not merely stand near props; he should negotiate,
  request, present, receive, inspect, validate, hand off, be blocked, be briefed, be reviewed, or
  otherwise interact in ways that express the lesson.
- It defines environment progression: the concrete places Patch starts, gets blocked,
  learns/gathers, tests, and finishes; what each place represents; and why each belongs in this
  frame rather than being interchangeable scenery.
- It makes failure visible and success desirable.
- It defines conflict or cost: what goes wrong, becomes unsafe, becomes unverifiable, or wastes
  effort if Patch acts before the lesson is applied.
- It can generate most body-slide scenes without falling back to abstract diagrams.
- It has a short thesis sentence that the audience can remember.
- It maps the main teaching terms to concrete story objects, actions, locations, roles, or state changes.
- It identifies at least one boundary where the analogy stops helping.
- It suggests a visual grammar for images.
- It can support short in-world text where useful without requiring paragraphs on slides.
- It defines adventure state progression: what changes from beat to beat, what knowledge or
  capability the audience gains at each slide, and why the slide order matters.
- It identifies reusable asset candidates: characters, environments, props, interaction systems, or
  visual-state grammar that may become durable project assets if accepted.
- It states asset reuse posture: which existing assets naturally fit, which should not be reused,
  and which new provisional assets are likely needed.
## Adventure progression test


After selecting a candidate frame, test whether it supports a continuous journey.

Ask:

- What is Patch's starting state?
- Who gives, blocks, verifies, or receives Patch's work?
- What does Patch not know or not have at the start?
- What place or interaction exposes the initial failure?
- What new information, constraint, permission, evidence, or capability is gained at each body beat?
- What visible state changes on the mission card, dossier, map, route, permission, confidence, risk,
  or handoff object?
- What is the midpoint turn where Patch shifts from blocked/confused to executable/ready?
- What is the final threshold, test, or debrief that proves the lesson worked?
- Could any body slide move two positions earlier or later without changing the story semantics? If
  yes, the slide progression is probably too weak.

If the answer is mostly decorative, classify as `amber_progression_gap` or `red_bland_corporate` instead of green.
## Actor and interaction test


Patch needs meaningful counterparties unless your human partner explicitly defines a solitary adventure.

Ask:

- Who does Patch interact with in this adventure?
- If Patch presents something, who is the audience and what do they need from him?
- If Patch is delegated work, who is the requester and what do they misunderstand or omit?
- If other agents appear, why are they there, what are they responsible for, and why is Patch
  interacting with them rather than simply doing the work alone?
- Are other agents visually and narratively distinct from Patch rather than Patch-shaped duplicates,
  helper clones, or audience clones?
- Who blocks unsafe progress?
- Who supplies missing context, constraints, examples, or proof requirements?
- Who verifies success or receives the handoff?
- Which actors are durable enough to become reusable character assets or role archetypes?

If the answer is "random people," "generic team," or "other agents for flavour," classify as `amber_actor_gap`.
## Environment test


The frame needs places with semantic work to do.

Ask:

- What environments does Patch travel through or sojourn in?
- What does each place represent in the software/agent lesson?
- What does Patch do there that could not happen as clearly somewhere else?
- How does each place change Patch's state, the mission state, or the audience's understanding?
- What recurring environment grammar ties the places together?
- Could the environment be swapped for five similar-looking alternatives without changing the story?
  If yes, classify as `amber_environment_gap`.
## Asset fit test


Available assets are option space, not a mandate. Existing characters, environments, props, and
receipt-backed visual systems may be reused only when the frame makes them semantically honest. A
familiar asset should not appear merely because it exists or because reuse is cheaper.

When asset reuse may affect the hook, theme, story, or environment, inspect repo asset indexes first
and classify each relevant candidate:

- `reuse_candidate`: the asset naturally belongs in the frame and strengthens the lesson. Example: a
  client/stakeholder role in a mission-control deck if the world includes mission sponsors, command
  stakeholders, or briefing-room authorities.
- `maybe_adapt`: the asset could work only if your human partner explicitly chooses a frame that justifies the
  role or environment.
- `do_not_reuse`: the asset would be a cameo, cross-context noise, or misleading visual shorthand.
  Example: a Club DB bouncer in a non-club/non-gate deck unless the frame genuinely includes access
  control, thresholds, security, queueing, or a reason that bouncer role belongs.
- `new_asset_needed`: no existing asset is the right carrier; new deck-specific character,
  environment, prop, or visual grammar should be planned as provisional.

Ask:

- Does the asset's existing role match a role required by this frame?
- Does the asset's original environment/context belong here, or would it pull the deck into the wrong world?
- Would a new purpose-built asset teach the lesson more cleanly?
- Is reuse helping the audience understand the frame, or merely rewarding project familiarity?
- Should the asset stay out of this deck even though it is available?

If asset reuse remains material and unresolved, classify as `amber_asset_fit_unclear` and ask your human partner interactively.
