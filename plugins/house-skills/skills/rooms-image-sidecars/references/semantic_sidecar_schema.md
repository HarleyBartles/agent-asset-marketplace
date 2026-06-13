# Semantic sidecar schema

Use this schema for `semantic_sidecar.json`. Fields may be omitted only when not applicable. Preserve empty arrays when a section is intentionally checked and no candidates were found.

```json
{
  "sidecar_type": "gpt_semantic_image_starter",
  "schema_version": "1.0.0",
  "status": "non_authoritative_starter_guidance",
  "truth_boundary": "starter guidance only; not archive truth, DB truth, World canon, or worker verification",
  "source_batch": {
    "batch_id": "string",
    "source_family": "string",
    "source_owner": "string",
    "expected_image_count": 0,
    "observed_image_count": 0,
    "generated_by": "GPT",
    "generated_at": "ISO-8601 or unknown",
    "input_notes": ["string"]
  },
  "image_observations": [
    {
      "image_seq": 1,
      "filename": "string",
      "visual_class": "room_inbox_list | room_chat_screenshot | tweet_screenshot | profile_screenshot | media_object | unknown",
      "image_role_notes": ["string"],
      "visible_dates": [
        {"text": "string", "status": "exact | likely | partial | cropped | uncertain", "confidence": "starter-high | starter-medium | starter-low"}
      ],
      "visible_room_titles": [
        {
          "text": "string",
          "status": "exact | likely | partial | cropped | uncertain",
          "candidate_room_key": "slug",
          "known_or_new": "known_world_room | likely_existing_room | candidate_new_room | unresolved_lead",
          "confidence": "starter-high | starter-medium | starter-low",
          "notes": "string"
        }
      ],
      "visible_participants": [
        {
          "display_name": "string or null",
          "handle": "string or null",
          "status": "visible | cropped | partial | uncertain",
          "candidate_entity_key": "slug or null",
          "likely_known_character": true,
          "likely_known_character_hint": "string or null",
          "confidence": "starter-high | starter-medium | starter-low",
          "lead_notes": "string"
        }
      ],
      "visible_messages": [
        {
          "speaker": "visible speaker or unknown",
          "text": "string",
          "reading_status": "exact | likely | partial | cropped | uncertain",
          "confidence": "starter-high | starter-medium | starter-low",
          "notes": "string"
        }
      ],
      "semantic_labels": ["string"],
      "membership_evidence": [
        {
          "room_candidate": "string",
          "member_candidate": "string",
          "basis": "image-visible | conversation-derived | synthesis",
          "confidence": "starter-high | starter-medium | starter-low",
          "notes": "string"
        }
      ],
      "entity_resolution_hints": ["entity_resolution_hint_id"],
      "conversation_candidate_refs": ["candidate_conversation_key"],
      "db_queries_to_run": ["string"],
      "world_surfaces_to_check": ["path or glob"],
      "pit_surfaces_to_check": ["path or glob"],
      "uncertainties": ["string"]
    }
  ],
  "conversation_candidates": [
    {
      "candidate_conversation_key": "slug",
      "candidate_type": "group_dm_room | one_to_one_dm | tweet_thread | unknown",
      "display_title": "string",
      "title_variants": ["string"],
      "source_images": [1],
      "known_members_from_images": ["string"],
      "candidate_members_from_memory": ["string"],
      "likely_existing_world_surface": "path or null",
      "likely_existing_pit_surface": "path or null",
      "membership_confidence": "starter-high | starter-medium | starter-low",
      "room_status_hint": "known_world_room | likely_existing_room | candidate_new_room | unresolved_lead",
      "next_checks": ["string"],
      "notes": "string"
    }
  ],
  "entity_resolution_hints": [
    {
      "hint_id": "slug",
      "observed_string": "string",
      "likely_entity": "string or null",
      "resolution_status": "likely_known_character | candidate_existing_entity | candidate_new_entity | unresolved_lead | do_not_resolve",
      "basis": "image-visible | conversation-derived | repo-grounded | synthesis",
      "source_images": [1],
      "must_verify": true,
      "db_queries_to_run": ["string"],
      "world_surfaces_to_check": ["path or glob"],
      "notes": "string"
    }
  ],
  "room_lineage_hints": [
    {
      "lineage_key": "slug",
      "lineage": "string",
      "status": "image-visible | conversation-derived | repo-grounded | synthesis",
      "source_images": [1],
      "must_verify": true,
      "notes": "string",
      "next_checks": ["string"]
    }
  ],
  "semantic_clusters": [
    {
      "cluster_key": "slug",
      "label": "string",
      "source_images": [1],
      "description": "string",
      "candidate_surfaces": ["string"],
      "next_checks": ["string"]
    }
  ],
  "do_not_resolve": ["string"],
  "suggested_albert_queries": ["string"],
  "db_promotion_companion": {
    "status": "not_requested | included | omitted",
    "companion_folder": "db_promotion_companion or null",
    "truth_boundary": "routing proposal only; worker must verify live DB schema and use sanctioned command/UOW route",
    "files": [
      "db_target_routing_companion.csv",
      "conversation_promotion_companion.csv",
      "membership_promotion_companion.csv",
      "message_fragment_companion.csv",
      "entity_resolution_companion.csv",
      "alias_name_form_companion.csv",
      "relationship_fragment_companion.csv"
    ]
  },
  "world_handoff_candidates": [
    {
      "target_type": "character | room | relationship | insight | system | index",
      "target_hint": "string",
      "basis": "image-visible | conversation-derived | repo-grounded | synthesis",
      "source_images": [1],
      "status": "review_only",
      "notes": "string"
    }
  ]
}
```
