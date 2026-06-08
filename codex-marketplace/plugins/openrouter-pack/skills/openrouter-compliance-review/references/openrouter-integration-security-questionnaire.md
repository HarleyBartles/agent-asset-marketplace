# OpenRouter Integration Security Questionnaire

## Purpose

Use this questionnaire to capture the minimum security and compliance questions
before an OpenRouter integration is promoted to production. It fills the gap left
by the missing upstream support file referenced by `SKILL.md`.

## Questions

- Which data classifications can be routed through OpenRouter?
- Are API keys stored in secrets management rather than source control?
- Are provider fallbacks disabled for regulated traffic?
- Is audit logging capturing generation IDs, model choice, and cost metadata?
- Are prompts redacted before logging or export?
- Are retention and deletion requirements documented?
- Are approved providers and models explicitly allowlisted?

## Evidence to Attach

- Architecture diagram showing app -> OpenRouter -> provider data flow
- Screenshot or export of API key limits and access controls
- Log samples showing redaction and request metadata
- Compliance sign-off for the selected data classification scope
