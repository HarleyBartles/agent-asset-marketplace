# Capability routing

Select an image capability by the behaviour the operation needs. A provider name,
model name, or convenient interface is not evidence that the required behaviour
exists. If no authorised capability satisfies the requirement, stop with
`blocked by missing capability` and record what is missing.

## Discover in this order

1. Read the requested operation and output contract. Separate hard requirements
   (for example, an edit must preserve a face) from preferences (for example,
   preferred speed).
2. Inspect the environment's declared media capabilities and any provider or
   harness adapters available to the agent. Use their own documentation only
   after the portable requirement is known.
3. Build a short capability card for each candidate. Do not infer support from a
   marketing label or from a previous run.
4. Select the smallest authorised capability that satisfies all hard requirements.
   If several qualify, prefer the one with the clearest output custody and the
   least irreversible transformation.
5. Record the selected capability and its constraints in the handoff record.

If the environment exposes no declared capability registry, use the adapter's
documented discovery surface or run a bounded capability probe before selecting
it. A generic provider label is not a capability card. If discovery cannot prove
the required operation, use the blocked terminal state.

## Capability card

```text
Capability: <local identifier or provider adapter>
Operation: generate | edit | variation | inpaint | outpaint | composite | cutout | convert
Input roles accepted: <reference, target, mask, identity, composition, style, palette>
Reference count/limits: <known limit or unknown>
Mask support: yes | no | unknown
Transparency: native | preserved on input | no | unknown
Output delivery: <actual local path, returned media, or provider result>
Composition control: <what can be locked or is likely to drift>
Known constraints: <format, size, text, identity, rate, or policy limits>
Authorisation/custody: <why this route is allowed and where results belong>
Evidence checked: <adapter documentation, capability listing, or run result>
```

Unknown is not yes. A capability that has not demonstrated masks, transparency,
reference roles, or output delivery cannot be selected when those are hard
requirements.

## Behaviour matrix

| Requirement | Evidence needed before selection | If absent |
| --- | --- | --- |
| New raster image | A generation operation returning media | Route to another generator or block |
| Controlled edit | Target input plus an edit operation | Do not phrase an edit as a new generation |
| Multiple reference images | Explicit multi-reference support and role mapping | Use one reference only if it preserves the brief, otherwise block |
| Masked local change | Mask input and documented mask semantics | Do not promise local-only editing |
| Transparent cutout | Native alpha or verified alpha-preserving output | Keep background or block; do not fake transparency with a checkerboard |
| Project-bound output | Stable retrieval and a writable destination | Preview-only result cannot satisfy handoff |
| Identity or exact composition | Suitable reference fidelity and invariant control | Escalate unresolved risk to the brief or block |
| Iteration | Comparable rerun with the same prompt and inputs | Do not compare unlike variants |

## Adapter boundary

An adapter may translate this contract to a concrete provider, runtime, or
application. Keep adapter details outside this skill's core. An adapter must state
which capability-card fields it implements, its authentication and output rules,
and its own source/licence provenance. Never hide provider-specific defaults in a
generic prompt or claim that a missing adapter was used.

## Terminal routing

- `not generated because the brief is incomplete`: crop, subject, operation, or
  other story-critical direction is unresolved; route back to
  `directing-visual-stories`.
- `blocked by missing capability`: the required behaviour or authorised output
  custody is unavailable; name the exact missing field.
- `generated but unresolved`: a capability returned media, but inspection found
  a material defect or an unverified invariant.
- `selected and handed off`: the selected result and all custody evidence are
  available at the declared destination.
