# Translating to interactive worlds

Use this route when participants move through, inspect, or alter a designed world.
The world is a complete field with many possible frames. The direction must make
agency part of the composition: the audience's choice, viewpoint, and return can
change what the space means.

## World-direction output

Record:

- **Participant story:** what the participant should discover, decide, feel, or
  cause; distinguish authored beats from player-authored outcomes.
- **Agency contract:** directed, guided, or exploratory; what can be looked at,
  approached, changed, skipped, revisited, or misunderstood, and how recovery works.
- **Scales:** object/detail, frame/viewport, scene/complete field, and world/route;
  name which scale carries each beat and how the containing field supports it.
- **Observation points:** arrival, approach, threshold, dwell/interaction, return,
  and departure. For each, name viewpoint, crop, landmark, and likely alternate
  views rather than designing only one ideal screenshot.
- **Spatial evidence:** foreground/middle/background relationships, route shape,
  occlusion, environmental traces, social grouping, sound/light implication when
  relevant, and the causal inference each clue enables.
- **State change:** the action that changes the field, visible consequence, changed
  route or relation, and the evidence that makes the return leg meaningful.
- **Attention and atmosphere:** landmark relay, light and palette roles, depth,
  motion budget, quiet intervals, compression/release, and intentional off-frame
  space.
- **Interface relationship:** what belongs to the world, what is an overlay, what
  the participant must read as a control, and how interface attention supports rather
  than replaces environmental storytelling.
- **Survival invariant:** what remains legible across camera movement, viewport
  changes, player pace, state changes, reduced motion, and route choice.

For a tile-based world, describe tile grammar, exceptions, palette regions,
silhouette hierarchy, parallax or colour-cycle roles, landmark relays, and the
intended rhythm of quiet streets, social nodes, vistas, and event spaces. Keep the
creative rule here; downstream game skills own tile maps, rendering, collision,
state machines, and input implementation.

## Handoff boundary

Hand the direction to game/world implementation with explicit beats and evidence,
not a list of mechanics. The direction owns story, spatial relationship, attention,
atmosphere, agency intent, and invariants. The receiving skill owns engine or React
mechanics, data structures, accessibility, input, performance, and asset custody.
Request a playable or navigable proof of arrival, threshold, dwell, consequence,
and return. If the proof cannot preserve the intended read, revise the composition
or agency contract rather than decorating the world.

### Avoid

- designing for one screenshot when participants can move elsewhere;
- lore piles and prop clutter with no observable causal relation;
- arrows, quest markers, or HUD panels doing all the work of spatial composition;
- inventing project canon, outcomes, or backstory to make the world feel full;
- treating tile, anime, or cinematic language as a surface filter.
