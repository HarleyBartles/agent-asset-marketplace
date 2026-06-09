# MARK-71 OpenAI Developer Pack Provenance

Issue: `MARK-71`

## Outcome

Created a repo-owned clean-room OpenAI developer pack at `codex-marketplace/plugins/openai-developer-pack`.

## Blocked advisory root

- Upstream root: `openai/plugins/plugins/openai-developers`
- Usage posture: advisory only
- License posture: proprietary
- Copied payload: none

## Permitted source families reviewed

- OpenAI API docs and developer docs pages
- `openai/openai-agents-python` under MIT
- `openai/openai-agents-js` under MIT
- `openai/openai-cookbook` under MIT

## Repo-held evidence

- Pack README: `codex-marketplace/plugins/openai-developer-pack/README.md`
- Pack source note: `codex-marketplace/plugins/openai-developer-pack/SOURCE.md`
- Pack source map: `codex-marketplace/plugins/openai-developer-pack/references/source-map.md`
- Pack license notice: `codex-marketplace/plugins/openai-developer-pack/LICENSE`

## Notes

- The pack text was authored from first principles.
- The pack does not reproduce the proprietary OpenAI Platform connector or API-key creation flow.
- If the live OpenAI docs change, the pack should be refreshed from the official docs rather than from the blocked root.

