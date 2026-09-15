# Asset handoff and custody

An image is not project-ready because a provider displayed it. A selected asset
needs a durable destination, a traceable operation, and enough provenance for the
next agent to understand what may be changed.

## Handoff record

```text
Asset: <human-readable name and stable version>
Status: selected and handed off | generated but unresolved
Destination: <actual workspace path, repository URL, or durable authorised provider result>
Intended consumer: <route, article, game screen, or preview>
Operation: <generate/edit/variation/inpaint/outpaint/composite/cutout/convert>
Capability: <selected capability identifier and adapter, if any>
Inputs: <each source/result and its role>
Direction/brief: <path or durable reference and version>
Prompt/operation trace: <final translated prompt or provider request reference>
Invariants checked: <summary and inspection record>
Unresolved defects: <none or explicit list>
Provenance/licence: <source assets, generated-result policy, and notices>
Validation: <dimensions, format, alpha, visual checks, and command/report>
Next owner: <implementation skill or human reviewer>
```

Use the actual returned location. If a provider result is remote or temporary,
copy it to the authorised project destination before calling it project-bound, or
leave the status as preview-only/generated but unresolved. A provider result is
project-bound only when it is durable, retrievable, and authorised for that
consumer. Never invent a stable path from a UI label.

Blocked or incomplete work has no asset handoff record. Record the terminal state
and missing evidence in the brief or run log instead of fabricating a selected
asset.

## Source and licence boundaries

Record every input that materially influences the result and its licence or
permission status. Distinguish:

- repository-owned source assets;
- user-supplied material with explicit permission;
- provider-generated output and the provider's current terms;
- third-party references used only for analysis or style direction;
- temporary previews that must not enter the repository.

Do not add a reference image to a distributable asset package without checking its
rights and intended use. The `generating-images` skill's Apache-2.0 derivative
notice concerns these instructions, not the licence of any generated image or
input artwork.

## File and destination discipline

- Preserve source files; create a new version unless replacement is explicitly
  authorised.
- Use the repository's asset-custody rules for naming, optimisation, attribution,
  and placement when a project asset is being added.
- Keep discarded variants and temporary provider files out of the project unless
  the brief asks for them or they are evidence needed for a decision.
- Verify format, dimensions, colour profile, alpha, and file readability after any
  copy or conversion.
- Update the consuming reference only after the selected asset is present at its
  declared destination.

## Handoff to downstream work

Pass the record to the consuming implementation skill with the selected file and
its creative invariants. Web, React, game, accessibility, and asset-custody
skills decide how the file is integrated. They must not infer permission to crop,
recolour, redraw, or substitute the asset from its filename alone; those changes
need a new direction or an explicit allowed-change entry.
