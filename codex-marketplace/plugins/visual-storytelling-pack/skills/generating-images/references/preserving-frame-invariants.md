# Preserving frame invariants

An invariant is a creative decision that must survive generation, editing,
conversion, and handoff. Record it before an operation so “close enough” does not
silently rewrite the authored frame.

## Invariant ledger

```text
Target/result: <asset and intended placement>
Operation: <operation>
Lock strength: hard | strong | soft
Must preserve: <specific decisions>
May change: <explicitly allowed properties or region>
Reference evidence: <input index, direction section, or approved frame>
Failure test: <observable reason to reject the result>
Notes after inspection: <drift found or confirmed>
```

Use `hard` for project requirements and story-critical decisions, `strong` for
approved visual language that may receive small technical variation, and `soft`
for exploratory cues. Do not downgrade a lock merely because the capability is
weak; report the capability limitation instead.

## What to lock

| Decision | Make it observable |
| --- | --- |
| Crop and aspect | Exact edge relationships, headroom, footroom, and required empty field |
| Scale and placement | Subject bounds and relationship to frame edges or other objects |
| Viewpoint and perspective | Camera height, angle, lens feel, horizon, vanishing direction |
| Pose and silhouette | Gesture, facing, key contour, hand/eye/action position |
| Depth and focus | Fore/mid/background order, focal plane, blur or sharpness relationship |
| Lighting | Key direction, shadow side, contrast level, colour temperature, practical sources |
| Palette | Role-based colour relationships, not merely a list of swatches |
| Attention path | Primary read, secondary cue, and quiet areas |
| Text and marks | Verbatim copy, placement, legibility, logos, watermarks, or none |
| Negative space | Region reserved for copy, interface, breathing room, or suspense |

Describe relationships rather than vague adjectives. “Warm key from upper left;
cooler unlit background; face is the only high-contrast focal area” is testable;
“cinematic and nice” is not.

## Operation risk

- `convert` should preserve every frame invariant unless the output contract says
  dimensions or colour profile may change.
- `edit` and `inpaint` may drift at the changed boundary and in adjacent light,
  reflections, texture, or text; inspect a generous halo around the edit.
- `outpaint` changes crop, negative space, perspective, and often attention; treat
  the new frame as a new direction, not a routine repair.
- `composite` must preserve the target's camera and light logic while integrating
  the insert; layer mismatch is a composition failure even if the insert is crisp.
- `variation` may change only the named experiment variable; all other hard and
  strong locks remain in force.

## Drift triage

When a result fails, classify the first material drift:

1. frame drift — crop, aspect, scale, placement, or perspective;
2. subject drift — identity, pose, silhouette, action, or object count;
3. attention drift — focus, contrast, hierarchy, or negative space;
4. light/palette drift — source direction, value structure, temperature, or role;
5. surface drift — material, texture, medium, or rendering language;
6. delivery drift — alpha, dimensions, text, format, or destination.

Fix one category at a time. If the failure shows that the direction itself has
changed, stop iterating and request a revised direction rather than stacking
contradictory prompts.
