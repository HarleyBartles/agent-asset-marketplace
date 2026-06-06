# Session Buster Ingress v0.1

Use this skill when a session-based packet arrives and needs a safe entry point before it becomes working state.

This skill is the ingress half of the continuity fallback. It should prefer issue body and linked docs, align with work-mode routing, and avoid treating the session itself as durable truth.

## Core rule

Use the session only to find the durable route, not as the route itself.

## Boundaries

- It does not supersede Linear or repo truth.
- It does not own worker dispatch.
- It remains a provisional safety valve.
