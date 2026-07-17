# Asset sheet compiler manifest

The compiler is driven by a JSON manifest. The manifest is the durable source of intent for a
deterministic asset-sheet compile.

## Required fields

```json
{
  "lane": "character-v4",
  "output_dir": "/mnt/data/example_asset_sheet_package",
  "images": [
    {"slot": "hero", "path": "/mnt/data/hero.png", "copy_name": "source_hero.png"}
  ]
}
```

`lane` must be one of:

- `character-v4`: one main hero image, six alternate images, metadata, guidance, optional alt captions.
- `three-hero-six-alt-v4`: three equal hero columns with two alternate images beneath each hero.
- `four-column-four-hero-eight-alt-v2`: four equal vertical hero columns with two alternate images beneath each hero.

`images` can be a list of `{slot, path}` objects or an object mapping slot id to path.

## Common optional fields

```json
{
  "metadata": {
    "title": "BIT & BOT",
    "type": "PATCH MISSION CONTROL SUPPORT BOTS",
    "status": "PROVISIONAL / QA-ACCEPTED SOURCE SET",
    "version": "v1",
    "source_qa": "partner-approved source images"
  },
  "guidance": ["Short bullet one", "Short bullet two"],
  "trim": true,
  "slot_pad": 18,
  "output_png": "asset_sheet__character__example_v1.png",
  "output_zip": "example_asset_sheet_package.zip"
}
```

`trim: true` removes transparent or near-white margins from pasted images during placement only.
It does not edit or overwrite the approved source files.

## Slot names

### `character-v4`

- `hero`
- `alt_1` through `alt_6`

Each alt can include a caption:

```json
{"slot": "alt_1", "path": "/mnt/data/side.png", "caption": "SIDE VIEW"}
```

### `three-hero-six-alt-v4`

- `hero_1`, `hero_2`, `hero_3`
- `hero_1_alt_A`, `hero_1_alt_B`
- `hero_2_alt_A`, `hero_2_alt_B`
- `hero_3_alt_A`, `hero_3_alt_B`

### `four-column-four-hero-eight-alt-v2`

- `hero_1`, `hero_2`, `hero_3`, `hero_4`
- `hero_1_alt_A`, `hero_1_alt_B`
- `hero_2_alt_A`, `hero_2_alt_B`
- `hero_3_alt_A`, `hero_3_alt_B`
- `hero_4_alt_A`, `hero_4_alt_B`

## Output package

The script creates:

- the rendered PNG
- `sources/` with copied approved source images
- `asset_sheet_manifest.json`
- `asset_sheet_compile_spec.json`
- a zip package containing all of the above
