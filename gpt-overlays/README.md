# GPT Skill Overlays

This tree holds source-owned GPT export overlays for generated `skill.zip`
artifacts.

Codex plugin first; generated GPT-safe skill zips second.

Convention:

- `gpt-overlays/manifest.json` classifies each generated skill as `direct`,
  `overlay`, or `excluded`.
- Overlay sources mirror the target skill path under
  `gpt-overlays/<pack>/<skill>/...`.
- Generated archives are assembled from marketplace source custody plus the
  overlay tree when an overlay is declared.

The generated surface remains `generated/skill-zips/`.

Overlays exist to make the generated GPT export safe and installable without
changing the behavior or custody of the Codex plugin roots.

