# Consumer profile discovery and evidence-based application

## Scenario

The repository explicitly adopts the optional `unslop` standard. Its `.agents/contracts/unslop.json` declares `.agents/unslop` as a profile root. That directory contains a `release-claims` profile whose trigger is reviewing release and migration documentation. It identifies unsupported reliability claims as the recurring failure pattern, asks the agent to replace them with observable limits, and says quoted titles or defined measurements are false positives. The repository has no Writing Pack installation. The generic technical-writing profile is available in Unslop+.

The draft release note says: “The retry change is robust and simple.” The implementation retries timeouts and HTTP 502 responses up to three times, and returns authorization errors immediately. A linked standards document is titled “Robust Repository Recovery”.

## Prompt

Review this release note for accuracy and clarity. Return a suggested replacement and explain the evidence for each correction. Do not change files.

## Expected behavior

- Check the explicit standard adoption and declared profile roots, then read the matching consumer profile before applying its guidance.
- Read and apply the generic technical-writing profile too if its trigger fits; preserve the separate scope and authority of each profile.
- Ground the recommendation in the release note and retry behavior. Replace unsupported “simple” and make “robust” specific to the retry limits rather than mechanically deleting it.
- Preserve “Robust Repository Recovery” as a source title. Do not claim the missing Writing Pack blocked the review.
