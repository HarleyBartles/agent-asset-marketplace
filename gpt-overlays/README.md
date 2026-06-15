# GPT Skill Overlays

This tree holds source-owned GPT export overlays for generated `skill.zip`
artifacts.

Overlays are not canonical source. They exist so GPT exports can stay safe and
platform-neutral without weakening the Codex plugin source tree.

Convention:

- `gpt-overlays/manifest.json` classifies each generated skill as `direct`,
  `overlay`, or `excluded`.
- Overlay sources mirror the target skill path under
  `gpt-overlays/<pack>/<skill>/...`.
- Generated archives are assembled from marketplace source custody plus the
  overlay tree when an overlay is declared.
- Excluded entries are omitted from raw GPT exports rather than being forced
  through without a safe adaptation path.

The generated surface remains `generated/skill-zips/`.

