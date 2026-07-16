# DB mutation proposal CSV companions

Use this reference when a Rooms image sidecar packet is intended to support Pit/ProjectDB promotion or DB-backed materialisation.

## Boundary

DB companion CSVs are routing proposals, not executable mutation commands and not evidence by themselves.

GPT may propose where observed facts should land. Albert must verify the live DB schema, run duplicate checks, and use the lawful ProjectDB command/unit-of-work route before any write. Do not generate raw SQL inserts as final authority.

Keep provenance layers separate:

- `image-visible`: directly visible in the supplied image batch.
- `harley-context`: supplied by Harley from memory or browsing/profile screenshots.
- `repo-grounded`: checked against repo files in the current session.
- `db-grounded`: checked against the live local machine-surface DB by a worker.
- `synthesis`: GPT reasoning that must be verified.

## Required companion CSVs for DB-promotion packs

When the downstream task includes DB promotion, include a `db_promotion_companion/` folder with these files.

### db_target_routing_companion.csv

Columns:

- `data_family`
- `target_db_surface_or_table_family`
- `promotion_rule`
- `worker_verification_note`

Purpose: map classes of extracted data to target DB table families or DB-backed surfaces.

### conversation_promotion_companion.csv

Columns:

- `conversation_key`
- `observed_title_or_titles`
- `canonical_label_suggestion`
- `source_image_seq`
- `image_proven_visible_members`
- `promotion_status`
- `resolution_or_context_notes`
- `target_db_surfaces`

Purpose: propose thin `dm_conversation` style rows and title/variant handling. Use image-proven members only in the member column; keep memory-only members out.

### membership_promotion_companion.csv

Columns:

- `conversation_key`
- `observed_member_string`
- `source_image_seq`
- `resolved_entity_label`
- `membership_basis`
- `membership_confidence`
- `target_db_surfaces`
- `worker_verification_note`

Purpose: make `dm_participant` style rows explicit. Every visible participant/member should appear here, including unresolved display-name-only entities.

### message_fragment_companion.csv

Columns:

- `image_seq`
- `conversation_key`
- `speaker_observed_string`
- `visible_text_fragment`
- `reading_status`
- `provenance_layer`
- `target_db_surfaces`
- `worker_verification_note`

Purpose: route visible text into `dm_event` / `image_visible_text` style surfaces. Preserve exact/partial/cropped status. Do not reconstruct missing chat.

### entity_resolution_companion.csv

Columns:

- `observed_string`
- `resolved_entity_label`
- `known_handle_or_current_profile`
- `resolution_status`
- `basis_or_caution`
- `target_db_surfaces`

Purpose: route observed display names, handles, labels, and Harley follow-up resolutions into account/entity/handle/identity-label surfaces. Preserve observed strings separately from resolved entities.

### alias_name_form_companion.csv

Columns:

- `observed_name_form`
- `resolved_entity_or_anchor`
- `name_form_role`
- `source_image_seq`
- `resolution_status`
- `promotion_note`
- `target_db_surfaces`

Purpose: preserve display-name mutations, joke names, and identity-assimilation forms as queryable observed forms, not just normalized identities.

### relationship_fragment_companion.csv

Columns:

- `relationship_key`
- `source_context`
- `subjects`
- `relationship_type`
- `strength`
- `not_proof_of`
- `target_db_surfaces`
- `worker_verification_note`

Purpose: route social-graph observations and relationship fragments, especially those supplied after the image batch, while preventing overclaims.

## Quality rules

- Every proposed DB row should include a source image sequence, provenance layer, or source-context note.
- Include unresolved entities as observed records rather than dropping them.
- Mark uncertain/current-profile continuity as `probable`, `resolved_with_handle_variant`, or `unresolved_observed`; do not flatten it.
- If a direct message or cropped room has no title, propose an unresolved conversation/event surface rather than inventing a title.
- For inbox/list screenshots, do not promote membership unless the DB/write policy allows room-list membership inference or a worker verifies it.
- If the user asks for a refreshed pack after an identification pass, regenerate all companion CSVs so the on-disk package reflects the latest Harley context before DB mutation.

## Recommended package layout

```text
batch.intake.json
semantic_sidecar.json
semantic_sidecar.md
starter_manifest.json
README_FOR_ALBERT.md
image_observation_table.csv
conversation_candidates.csv
db_promotion_companion/
  README.md
  db_target_routing_companion.csv
  conversation_promotion_companion.csv
  membership_promotion_companion.csv
  message_fragment_companion.csv
  entity_resolution_companion.csv
  alias_name_form_companion.csv
  relationship_fragment_companion.csv
```
