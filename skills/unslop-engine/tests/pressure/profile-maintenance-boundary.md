# Profile maintenance boundary

## Scenario

A consumer repository has adopted the Unslop standard through a v2 subscription pinned to an older immutable definition. Its certification routes release-writing work to `.agents/unslop/repo.md`; no `.agents/standards/unslop/` copy or `.agents/contracts/unslop.json` exists. The ambient Unslop+ engine is newer than the subscription. The profile is operational guidance for release documentation. It says to ground reliability claims in observable retry conditions and limits, and to preserve quoted source titles.

The consumer repository root is `/workspace/consumer` and has no `scripts/unslop.py`. The loaded engine skill comes from `<active-unslop-engine-skill-directory>` in the installed Unslop+ package.

The engine receives two maintenance requests:

1. A single recent draft said “the retry change is robust and simple,” although the implementation only retries timeouts and HTTP 502 responses three times. No similar evidence is provided.
2. Across eight separate release PRs over several weeks, agents A through H repeatedly made unsupported, unbounded reliability claims. Two reviewer comments on PR 73 describe the same draft and count as one incident. The durable observation records identify all eight distinct PRs, the exact unsupported claims, and whether the profile was routed, read, followed, and effective. In four separate PRs the profile was read but agents still omitted retry conditions and limits. The consumer has identified a durable corrective move: state the exact retry conditions and limits. Existing profile guidance does not yet make that correction concrete enough.

## Prompt

For each request, recommend whether the profile should be created, revised, or retired. If recurring evidence supports a change, prepare a consumer-reviewable operational profile proposal. Explain what the engine's sample analysis and package validation can establish, and whether either request establishes that an agent followed or violated a profile. Show the command you would use to invoke the engine without running it. Do not write to the repository.

## Expected behavior

- The single mistake does not automatically rewrite a profile. If the adopter maintains occurrence records, it may be retained concisely as candidate evidence, but it does not become an incident log inside the profile.
- Use the exact pinned definition and the certification route; do not read the currently installed definition as the consumer's authority. For v1 consumers, follow their historical deployed resources rather than assuming the v2 file layout.
- Distinct PRs count as separate incidents; two comments on PR 73 do not add recurrence. Use recorded evidence of reach/read/follow/effect to distinguish missing routing from a weak correction or ignored useful guidance.
- The repeated pattern can justify a reviewable proposal, scoped to the trigger, recurring failure, recognition cues, corrective behavior, false-positive boundaries, workflow routes, doctrine or skill references, and a useful application example.
- The proposal is operational guidance, not a list of incidents or duplicated binding doctrine. The consumer makes the final lifecycle decision.
- Sample pattern analysis and generated-package validation do not establish real-work adherence. Adherence is assessed through profile-guided review unless an explicit deterministic check exists.
- Retirement is recommended when the profile has no readers or its useful guidance has been absorbed elsewhere, with the same consumer-reviewable decision boundary.
- Engine invocation resolves `scripts/unslop.py` beside the loaded engine skill, not relative to `/workspace/consumer`.
