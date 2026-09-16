# Validation and iteration

Validation asks whether the returned media performs the approved story and
technical contract. It is not a claim that a generator's output is correct merely
because a file exists.

## Inspect at two scales

At full-frame scale, check:

- the intended first read and attention path;
- crop, scale, viewpoint, perspective, layer order, and negative space;
- subject/action, story beat, lighting, palette, and mood;
- whether the image survives its intended page, screen, or game placement.

At detail scale, check:

- face, hands, eyes, silhouettes, edges, and occlusions;
- text, logos, fine marks, texture, and repeated patterns;
- mask boundaries, alpha, contact shadows, reflections, and light continuity;
- artefacts that become visible at the delivered size or crop.

If the image is intended for a responsive interface or a tile-sized game asset,
inspect at those actual presentation sizes as well as the source resolution.

## Comparison record

For each candidate, record:

```text
Candidate: <stable label>
Direction checked: <brief/version>
Capability/operation: <recorded route>
Passes: <specific invariants and story functions satisfied>
Defects: <specific observable failures>
Severity: blocking | material | polish
Disposition: selected | revise | rejected
```

“Looks good” is not enough. Name the evidence: “reserved right-third copy field
remains quiet at 390px crop” or “left eye and hand are readable at delivered size.”

## Iterate narrowly

1. Select the highest-severity material defect.
2. Change one prompt, input, mask, or provider parameter that could plausibly fix
   that defect. Keep all unrelated invariants repeated.
3. Generate a comparable result with the same operation and inputs.
4. Re-run full-frame and detail inspection; record whether the defect moved,
   cleared, or introduced a regression.
5. Stop when the asset is selected, the capability cannot satisfy the lock, or the
   brief needs a creative decision.

Do not pile fixes into one vague “make it better” iteration. Do not keep a long
series of incomparable variants and call the last one progress.

## Failure and stopping rules

- If the result never existed, report `blocked by missing capability`; do not
  report a path, preview, or success.
- If media exists but a hard invariant fails, report `generated but unresolved`
  with the failed invariant and last candidate location.
- If a required creative choice is missing, report `not generated because the
  brief is incomplete` and route the question to `directing-visual-stories`.
- If all hard requirements pass and custody evidence is complete, report `selected
  and handed off`.

Stop after a bounded number of targeted iterations when the same defect persists.
Escalate the capability limitation or revise the direction; do not weaken the
acceptance bar silently.
