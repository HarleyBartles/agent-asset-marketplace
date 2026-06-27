---
name: rooms-image-sidecars
description: Use when prepare GPT-native semantic starter sidecars for Rooms image
  evidence batches before Albert/Pit ingestion. Use when a user supplies screenshots,
  image batches, or a zip/folder of images and wants GPT to inspect them visually,
  generate non-authoritative room/entity/message candidates, known-character hints,
  tags, DB query suggestions, and an Albert-ready sidecar packet without mutating
  repos or treating observations as canon.
metadata:
  source-id: rooms-image-sidecars
  source-path: sources/first_party/skills/rooms-image-sidecars/SKILL.md
  provenance-name: Rooms Image Sidecars first-party skill
  source-category: first_party
  status: active
  owner: Harley Bartles
  scope: Use when prepare GPT-native semantic starter sidecars for Rooms image evidence
    batches before Albert/Pit ingestion. Use when a user supplies screenshots, image
    batches, or a zip/folder of images and wants GPT to inspect them visually, generate
    non-authoritative room/entity/message candidates, known-character hints, tags,
    DB query suggestions, and an Albert-ready sidecar packet without mutating repos
    or treating observations as canon.
  use_when:
  - Use when prepare GPT-native semantic starter sidecars for Rooms image evidence
    batches before Albert/Pit ingestion. Use when a user supplies screenshots, image
    batches, or a zip/folder of images and wants GPT to inspect them visually, generate
    non-authoritative room/entity/message candidates, known-character hints, tags,
    DB query suggestions, and an Albert-ready sidecar packet without mutating repos
    or treating observations as canon.
  do_not_use_when:
  - Do not use when another more specific skill owns this task.
license: MIT
---
# Rooms Image Sidecars

Use this Skill to create a GPT-side starter packet for image evidence before Albert/Pit ingestion.

This Skill does not ingest into Pit, mutate repositories, update DBs, or canonize World facts. It helps GPT inspect images directly, preserve order, identify visible room/entity/message clues, and produce sidecar guidance that reduces rediscovery work for Albert while keeping all claims source-partitioned and provisional.

## Core rule

Treat the sidecar as `starter_guidance`, not truth. Every observation must remain verifiable by Albert from the image, DB, Pit evidence, or World surfaces before becoming custody evidence, reconstructed fact, or canon.

## Required outputs

For a supplied image batch, produce an Albert-ready packet containing:

- `raw/` with images in stable sequence order when available to package.
- `batch.intake.json` with operational intake metadata for Albert's image intake Skill.
- `semantic_sidecar.json` at the packet root using `references/semantic_sidecar_schema.md`.
- `semantic_sidecar.md` at the packet root as a readable summary of the same evidence.
- optionally `image_observation_table.csv` at the packet root for quick scanning.
- when downstream work includes Pit/ProjectDB promotion, `db_promotion_companion/` CSVs using `references/db_mutation_proposal_csvs.md`.
- `README_FOR_ALBERT.md` explaining source partition, sidecar status, and verification requirements.

If files are not available to package, produce the sidecar text/JSON and tell the user what files must be placed alongside it.

## Workflow

1. Count and order the images. Preserve supplied order. Note gaps, duplicates, or uncertainty.
2. Inspect each image visually. Do not use OCR as the primary source unless visual reading is impossible; OCR is helper evidence only.
3. For each image, record:
   - visual class: `room_inbox_list`, `room_chat_screenshot`, `tweet_screenshot`, `profile_screenshot`, `media_object`, or `unknown`;
   - visible room titles, including cropped or partial text;
   - visible participants/display names/handles;
   - visible messages or tweet text, with speaker if visible;
   - dates/times visible;
   - semantic labels and confidence;
   - known-entity hints and unresolved leads;
   - DB/Pit/World query suggestions.
4. Cluster images into thin conversation candidates. A conversation candidate is a possible group DM/room/entity surface with a display title, title variants, source images, known-from-image members, probable known members, unresolved member leads, and next verification checks.
5. Add entity-resolution hints only as hints. Use statuses like `likely_known_character`, `candidate_existing_entity`, `candidate_new_entity`, `unresolved_lead`, and `do_not_resolve`.
6. Add room-lineage hints when images imply room inheritance, name changes, or membership transfer.
7. Add `do_not_resolve` warnings for ambiguous names, cropped titles, identity uncertainty, and conversation-derived memory.
8. If Harley has finished an identification pass and the next step is DB promotion, generate DB mutation proposal CSV companions before the worker continues. Use `references/db_mutation_proposal_csvs.md`; treat them as routing guidance, not executable DB truth.
9. Generate the packet. If using the helper script, pass the source folder plus prepared sidecar JSON/Markdown files and any DB companion CSVs.

## Source partition labels

Use these labels consistently:

- `image-visible`: directly visible in one or more images.
- `conversation-derived`: supplied by Harley/user in chat, not durable evidence by itself.
- `repo-grounded`: checked against repo/file surfaces in the current session.
- `worker-report`: from a worker return or report, not independently revalidated unless inspected.
- `synthesis`: GPT reasoning from the above.
- `missing-or-unchecked`: relevant surface not inspected or not found.

## Confidence labels

Use starter confidence only:

- `starter-high`: directly visible and easy to read, but still needs Albert verification.
- `starter-medium`: visible or strongly inferred, but cropped, indirect, or requires cross-check.
- `starter-low`: weak lead, uncertain reading, or primarily conversation-derived.

Never use `confirmed`, `canon`, or `true` for sidecar claims.

## DB-promotion companion rules

When an image pack will feed Pit/ProjectDB mutation or promotion, produce a `db_promotion_companion/` folder with CSVs that say where the extracted data should land. This is required after Harley finishes identifying accounts or room relationships from memory/browser checks. The CSVs should propose target table families such as `account_entity`, `account_handle`, `identity_label`, `dm_conversation`, `dm_participant`, `dm_event`, and `social_graph_relationship_observation`, while leaving final schema verification and writes to Albert and the ProjectDB command/unit-of-work layer.

Do not generate raw SQL as authority. Do not treat these CSVs as evidence. Every row must keep provenance clear: image-visible, Harley-context, repo-grounded, DB-grounded, or synthesis. Preserve observed display strings separately from resolved entities and handles.

See `references/db_mutation_proposal_csvs.md` for required files and columns.

## Rooms-specific rules

- Convert room-title screenshots into candidate group DM/room records where useful.
- Preserve exact visible strings, including jokes, misspellings, stylized titles, and truncated text.
- Room candidates should have title variants, known-from-image member lists, likely existing room links, and next DB queries.
- Known-character hints can point Albert toward likely matches, but Albert owns DB/entity resolution.
- Identity-assimilation/name-bit observations should be captured as system/insight leads, not flattened into mere aliases.
- World handoff candidates are review prompts, not canon updates.
- If Harley asks to regenerate a pack after identifying people/rooms, regenerate the sidecars and DB companion CSVs before any on-disk DB promotion worker is unpaused.

## Helper script

Use `scripts/build_sidecar_packet.py` when image files are available locally and you already have or can write the sidecar files. The script packages raw images, computes hashes, writes a starter manifest, copies optional sidecar/CSV companion files, and creates a zip packet. It does not perform semantic analysis or DB schema verification.

See `references/workflow.md` and `references/semantic_sidecar_schema.md` for the full schema and output pattern.
