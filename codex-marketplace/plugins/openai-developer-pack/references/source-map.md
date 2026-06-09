# OpenAI Developer Pack Source Map

This pack is clean-room work. The sources below informed the workflows and terminology, but no file from the proprietary `openai/plugins/plugins/openai-developers` root was copied.

## Advisory-only blocked root

- `openai/plugins/plugins/openai-developers`
  - License posture recorded by upstream: proprietary
  - Role here: capability-gap evidence only
  - Copied payload: none

## Repo-owned skill files

- `skills/openai-api-app-development/SKILL.md`
  - References official OpenAI API docs for app development, build paths, model selection, and responses-first guidance.
- `skills/openai-agents-python/SKILL.md`
  - References the MIT-licensed `openai/openai-agents-python` repo and its official docs for agents, tools, MCP, tracing, and examples.
- `skills/openai-agents-typescript/SKILL.md`
  - References the MIT-licensed `openai/openai-agents-js` repo and its official docs for JavaScript and TypeScript agents workflows.
- `skills/chatgpt-apps-sdk/SKILL.md`
  - References the OpenAI Apps SDK docs for metadata, UI, auth, submission, and the MCP Apps bridge.
- `skills/openai-mcp-integration/SKILL.md`
  - References the OpenAI Agents SDK MCP docs and Apps SDK auth guidance for server and app integration.
- `skills/openai-evals-troubleshooting/SKILL.md`
  - References the current OpenAI evaluation guidance, traces, datasets, and agent-eval docs.
- `skills/openai-env-safe-setup/SKILL.md`
  - References official OpenAI setup guidance for local API-key handling and environment variables.

## Permissive source families consulted

- `https://developers.openai.com/api/docs`
- `https://developers.openai.com/api/docs/guides/agents`
- `https://developers.openai.com/api/docs/guides/evals`
- `https://developers.openai.com/api/docs/guides/agent-evals`
- `https://developers.openai.com/apps-sdk`
- `https://developers.openai.com/apps-sdk/reference`
- `https://developers.openai.com/apps-sdk/build/auth`
- `https://developers.openai.com/apps-sdk/build/chatgpt-ui`
- `https://openai.github.io/openai-agents-python/`
- `https://openai.github.io/openai-agents-python/tools/`
- `https://openai.github.io/openai-agents-python/mcp/`
- `https://openai.github.io/openai-agents-python/tracing/`
- `https://openai.github.io/openai-agents-js/`
- `https://github.com/openai/openai-agents-python` (MIT)
- `https://github.com/openai/openai-agents-js` (MIT)
- `https://github.com/openai/openai-cookbook` (MIT)

## Notes

- The pack uses repo-authored prose, not lightly rewritten upstream skill text.
- If a workflow detail changes in the live docs, the pack should be updated from the docs source rather than from memorized behavior.

