# Rooms Bootstrap v1

Use this skill as the first read for Rooms work that needs a route decision.

This skill is the compact Rooms router. It cleans the route map, then hands off to project doctrine or a more specific Rooms capability.

## Core rule

Resolve the route first, then act.

## Boundaries

- It does not own repo mutation.
- It does not own source partitioning.
- It does not replace project doctrine.
