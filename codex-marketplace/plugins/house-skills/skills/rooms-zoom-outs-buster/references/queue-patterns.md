# Queue patterns

Use this reference for Rooms zoom-out buster item content. Inherit visible queue mechanics, item formatting, approval
handling, batch cadence, and one-path suppression from `buster-framework`.

## Output rule

Interactive buster items are conversational by default. Do not use YAML, JSON, code fences, or copyable schemas for
normal chat buster items unless Harley explicitly asks for structured output.

A visible zoom-out item should be compact and readable, normally including:

- the entity or pattern under discussion;
- the proposed compression or zoom-out;
- the artifact basis checked, or the artifact gap;
- the amber/red risk, such as flattening, overresolution, externalising, symbolic drift, artifact gap, or regeneration
  failure;
- the green condition;
- GPT's strong recommendation.

Example visible item:

Z1. Mel as a stable performance model. The compression is that Mel performs without self-loss. The artifact gap is
whether this survives her room behaviour, not just the sketch. The risk is flattening her into "healthy Cunty." Green
requires checking voice, room, and exchange surfaces. Recommendation: keep the compression as a prompt-shaping lens
unless artifacts support it directly.

## Domain-specific item content

Use these fields conceptually when thinking through an item, but do not print them as a schema:

- entity or pattern;
- proposed zoom-out;
- artifact basis checked;
- compression claim;
- regeneration test;
- risk type;
- green condition;
- GPT recommendation;
- decision needed, if Harley must choose.

## Domain suppression guidance

Do not queue a zoom-out item when the artifact path gives only one lawful move. Examples:

- If artifacts have not been checked, internally downgrade to `amber_artifact_needed` or `green_model_only` instead of
  asking Harley to accept artifact verification.
- If a compression overresolves motive or identity, repair or reject it rather than asking Harley to approve
  overresolution.
- If the model is only conversation-derived, label it that way and do not present it as artifact-verified.
