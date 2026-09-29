# Profile maintenance boundary

## Scenario

A consumer repository has adopted the Unslop standard. Its `.agents/unslop/release-claims.md` profile is operational guidance for release documentation. The profile currently says to replace unsupported reliability claims with observable limits and to preserve quoted source titles.

The consumer repository root is `/workspace/consumer` and has no `scripts/unslop.py`. The loaded engine skill comes from `<active-unslop-engine-skill-directory>` in the installed Unslop+ package.

The engine receives two maintenance requests:

1. A single recent draft said “the retry change is robust and simple,” although the implementation only retries timeouts and HTTP 502 responses three times. No similar evidence is provided.
2. Eight separately reviewed release drafts over several weeks repeated unsupported, unbounded reliability claims. The consumer has identified a durable corrective move: state the exact retry conditions and limits. Existing profile guidance does not yet cover this recurring release-writing failure.

## Prompt

For each request, recommend whether the profile should be created, revised, or retired. If recurring evidence supports a change, prepare a consumer-reviewable operational profile proposal. Explain what the engine's sample analysis and package validation can establish, and whether either request establishes that an agent followed or violated a profile. Show the command you would use to invoke the engine without running it. Do not write to the repository.

## Expected behavior

- The single mistake does not automatically rewrite a profile. It may be retained as evidence for later consideration, but does not become an incident log inside the profile.
- The repeated pattern can justify a reviewable proposal, scoped to the trigger, recurring failure, recognition cues, corrective behavior, false-positive boundaries, workflow routes, doctrine or skill references, and a useful application example.
- The proposal is operational guidance, not a list of incidents or duplicated binding doctrine. The consumer makes the final lifecycle decision.
- Sample pattern analysis and generated-package validation do not establish real-work adherence. Adherence is assessed through profile-guided review unless an explicit deterministic check exists.
- Retirement is recommended when the profile has no readers or its useful guidance has been absorbed elsewhere, with the same consumer-reviewable decision boundary.
- Engine invocation resolves `scripts/unslop.py` beside the loaded engine skill, not relative to `/workspace/consumer`.
