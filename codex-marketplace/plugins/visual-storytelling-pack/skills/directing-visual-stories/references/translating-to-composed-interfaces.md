# Translating to composed interfaces

Use this route when a page or screen should behave as a composed visual field,
not merely as a collection of components. The direction describes the audience's
story and spatial read; a downstream web, React, accessibility, or styling skill
decides implementation. A page may be one complete frame, or a sequence of fields
whose local frames compose a larger argument.

## Page-direction output

Record the following before implementation:

- **Page story:** the audience change, proposition, and closing condition.
- **Field form:** one frame, spread, scroll passage, tableau, montage, polyptych,
  or another named structure, with its viewing contract (`directed`, `guided`, or
  `exploratory`).
- **Entry and dominant field:** where attention arrives, the first read, the
  dominant image/colour/space, and the question or expectation it creates.
- **Subordinate frames and voices:** each inset, detail, caption, quote, data
  object, or control with its story job; state whether it advances, qualifies,
  contradicts, or releases the dominant field.
- **Text as space:** exact copy or content source, reading order, measure, scale,
  placement, and the visual authority or interruption it should have. Do not
  invent copy to fill a composition.
- **Rhythm and transitions:** density, silence, scroll or state thresholds,
  dwell, reveal, rupture, return, and what changes between fields.
- **Closing field:** the final read, changed expectation, next route, or deliberate
  unresolved edge.
- **Survival requirements:** hierarchy, landmark, textual order, meaningful crop,
  contrast, motion alternative, and recovery cues that must survive viewport,
  zoom, reduced motion, keyboard, and assistive-technology translation.

For each field, include the primary compositional family and at most two supporting
families. Explain why the selected relationship carries the story. A responsive
translation may reorder or resize units, but it must preserve the declared story
roles and reading order; literal desktop coordinates are not the invariant.

## Handoff boundary

Pass the direction to the relevant implementation skills with an explicit contract:
the creative direction owns audience change, hierarchy, field relationships,
rhythm, intentional constraints, and rejected alternatives. The implementation
skills own DOM/component structure, responsive rules, interaction mechanics,
accessibility procedure, typography loading, and asset custody. Ask them to return
evidence that the direction survived at the target breakpoints and interaction
states. Do not smuggle CSS prescriptions into this skill or let a framework choose
the dominant field by default.

## Full-page and one-frame discipline

If the page is one frame, still name entry, secondary discovery, quiet zone, and
implied next state. If it contains many frames, describe the super-composition,
gutter or interval meaning, crossing boundaries, and the next field. A polished
hero with unrelated cards underneath is not a story; every subordinate unit must
change understanding, tempo, or anticipation.

### Avoid

- “nice web design” as a sufficient creative brief;
- card grids that flatten primary, secondary, and tertiary reads;
- ornamental panels, filler copy, or interaction without a beat;
- using a framework's stacking or breakpoint order as narrative direction;
- claiming accessibility or responsive validation from visual intention alone.
