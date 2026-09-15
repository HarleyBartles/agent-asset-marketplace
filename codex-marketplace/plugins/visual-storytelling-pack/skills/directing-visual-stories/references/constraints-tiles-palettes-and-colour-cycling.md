# Constraints, tiles, palettes, and colour cycling

Use this route when a constrained visual system—especially a tile-based world,
retro display, or deliberately limited palette—must carry story. Constraints are
not nostalgia garnish. They make silhouette, repetition, exception, contrast,
and motion allocation do more narrative work.

## Make the constraint causal

State the limitation and the story advantage it creates: a small palette forces
role clarity; a tile set makes repeated architecture establish a norm; a fixed
viewport makes thresholds and landmarks precious; a limited sprite budget makes
one moving accent significant. If the constraint does not change attention,
readability, production logic, or world meaning, it is probably a surface filter.

## Tile fields and exceptions

Use tile families to establish the ordinary: road, wall, roof, ground, edge,
vegetation, shopfront, and prop. Then reserve controlled exceptions for status,
history, danger, prosperity, access, or destination. Authorship comes from the
relationship between norm and exception, not from disguising repetition at any
cost. Maintain readable roads, junctions, thresholds, footprints, and sightlines.

Compose at several scales:

- **tile/object:** material, wear, symbol, interaction, or evidence;
- **room/block:** social function, enclosure, density, and local landmark;
- **district/town:** route, skyline, palette region, and arrival/departure rhythm;
- **world/sequence:** changed state, seasonal or political contrast, and return.

Sprite and silhouette discipline keeps recognition legible under a small budget:
choose a readable scale, reserve a few pose or shape cues for identity and action,
and test the silhouette before internal detail. Repetition establishes a town's
ordinary grammar; one economical exception can carry its status or story beat.

Deterministic variation may prevent monotony, but it must preserve hierarchy,
seams, orientation, and meaningful exceptions. A tile town should have a clear
arrival read, a discoverable centre or landmark, legible interaction sites, and a
changed composition after consequential action.

## Palette as narrative infrastructure

Assign colours roles rather than adjectives: world base, subject separation,
affiliation, prosperity, damage, alert, weather, time, region, and interaction.
Reuse is valuable when it creates a visual relationship. A controlled palette swap
can show ownership, danger, or world-state change across many assets at once.
Contrast should support silhouette and route reading before decoration. Regional
rules can create distinct zones while keeping the whole world coherent.

## Cycling and layered display logic

Colour cycling is spatial animation: contiguous palette-indexed pixels change
register assignment to suggest water, fire, shimmer, machinery, magic, or ambient
flow without changing geometry. It is effective when the cycle has a story job and
the moving region is semantically isolated. If one range is shared by unrelated
objects, every occurrence moves and the palette loses authorship.

The Amiga-era bitplane and Copper lessons generalise to layered, region-specific
display rules: one frame can contain zones with different palette, timing, or
visibility behaviour. Translate the principle, not the hardware ornament. Parallax
similarly works when each layer has a spatial relation and a depth cue; decorative
sliding of unrelated layers is noise.

## Motion budget and translation

Choose which layer may animate: water, weather, a sign, a character accent, a
highlight, or a state cue. Hold the rest so the movement remains a discoverable
attention signal. Record the palette and tile invariants that must survive asset
generation, viewport change, or alternate rendering. Implementation may differ;
the causal role must not.

### Route output

Record: constraint and its advantage; tile norms and meaningful exceptions;
observation scales; palette roles and shared ranges; cycling/parallax layer and
story verb; regional rules; changed-state behaviour; seam/orientation invariant;
and the accessibility or alternate-view concern to pass downstream.

### Avoid

- pixel texture, dithering, or palette limits added solely for retro mood;
- random tile variation that destroys paths, landmarks, or social meaning;
- colour cycling reused across unrelated semantic regions;
- maximum motion in every layer;
- letting hardware or rendering mechanics dictate story decisions that should have
  been made in the brief.
