---
name: rooms-image-sidecars
description: Use when preparing GPT-native semantic starter sidecars for Rooms image
  evidence batches before Pit/archive ingestion.
metadata:
  source-id: rooms-image-sidecars
  source-path: sources/first_party/skills/rooms-image-sidecars/SKILL.md
  provenance-name: Rooms Image Sidecars first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when preparing GPT-native semantic starter sidecars for Rooms image evidence
    batches before Pit/archive ingestion.
  use_when:
  - Use when preparing GPT-native semantic starter sidecars for Rooms image evidence
    batches before Pit/archive ingestion.
  do_not_use_when:
  - Do not use when the task is character investigation rather than image sidecar
    preparation — use rooms-character-investigation instead.
  - Do not use when the task is canon resolution — use rooms-canon-buster instead.
license: MIT
---
# Rooms Image Sidecars

Use this Skill to create a GPT-side starter packet for image evidence before Pit/archive ingestion. It does not ingest into Pit, mutate repositories, update DBs, or canonize World facts. It helps GPT inspect images, preserve order, identify visible room/entity/message clues, and produce source-partitioned, provisional sidecar guidance for the archive lane.

## Core rule

Treat the sidecar as `starter_guidance`, not truth. Every observation must remain verifiable by the archive lane before becoming custody evidence, reconstructed fact, or canon.## Required outputs

For a supplied image batch, produce an archive-ready packet:

- `raw/` with images in stable sequence order when available.
- `batch.intake.json` with operational intake metadata.
- `semantic_sidecar.json` and `semantic_sidecar.md` at the packet root (see `references/semantic_sidecar_schema.md`).
- optionally `image_observation_table.csv` for quick scanning.
- when downstream work includes Pit/ProjectDB promotion, `db_promotion_companion/` CSVs (see `references/db_mutation_proposal_csvs.md`).
- `README_FOR_ARCHIVE.md` explaining source partition, sidecar status, and verification requirements.

If files are not available, produce the sidecar text/JSON and tell the user what files must be placed alongside it.

## Workflow

1. Count and order the images; preserve supplied order and note gaps or duplicates.
2. Inspect each image visually (OCR is helper only). Record visual class, visible room titles, participants/handles, messages, dates, semantic labels, confidence, known-entity hints, and DB/Pit/World query suggestions.
3. Cluster images into conversation candidates with title variants, known/probable/unresolved members, and next checks.
4. Add entity-resolution hints, room-lineage hints, and `do_not_resolve` warnings for ambiguous or uncertain material.
5. If your human partner finished an identification pass and DB promotion is next, generate DB mutation proposal CSV companions.
6. Generate the packet using the helper script when image files are available.

See `references/workflow.md` for the full procedure and `references/semantic_sidecar_schema.md` for the schema.

## Source partition and confidence labels

Use source partition labels (`image-visible`, `conversation-derived`, `repo-grounded`, `worker-report`, `synthesis`, `missing-or-unchecked`) and starter confidence labels (`starter-high`, `starter-medium`, `starter-low`). Never use `confirmed`, `canon`, or `true` for sidecar claims. See `references/semantic_sidecar_schema.md` for full definitions.

## DB-promotion companion rules

When an image pack will feed Pit/ProjectDB promotion, produce a `db_promotion_companion/` folder with CSVs proposing where extracted data should land. Required after your human partner finishes identifying accounts or room relationships. Do not generate raw SQL as authority or treat CSVs as evidence. See `references/db_mutation_proposal_csvs.md` for required files, columns, provenance layers, and quality rules.## Rooms-specific rules

- Convert room-title screenshots into candidate group DM/room records with title variants, member lists, and next DB queries.
- Preserve exact visible strings including jokes, misspellings, and truncated text.
- Known-character hints point the archive lane toward likely matches; the archive lane owns DB/entity resolution.
- Capture identity-assimilation/name-bit observations as system/insight leads, not aliases.
- If your human partner asks to regenerate a pack after identifying people/rooms, regenerate sidecars and DB companion CSVs before any on-disk DB promotion worker is unpaused.

## Helper script

Use `scripts/build_sidecar_packet.py` when image files are available locally. It packages raw images, computes hashes, writes a starter manifest, copies optional sidecar/CSV files, and creates a zip packet. It does not perform semantic analysis or DB schema verification.
