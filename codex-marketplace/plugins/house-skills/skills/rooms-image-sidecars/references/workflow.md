# Workflow and output pattern

## 1. Intake and ordering

Count images and preserve their supplied order. When images are uploaded in batches, record batch boundaries if known. Use stable sequence labels (`001`, `002`, etc.) in packet filenames and observations.

## 2. Image observation pass

For each image, record only what can be seen or what is clearly stated by the user. Separate direct visual observations from memory or repo-derived hints.

Use these visibility statuses:

- `exact`: legible and unambiguous.
- `likely`: strongly legible or strongly matched but still needs verification.
- `partial`: visible fragment only.
- `cropped`: truncated by screenshot/UI boundary.
- `uncertain`: multiple readings possible.
- `unreadable`: cannot be read.

## 3. Candidate conversation clustering

Convert repeated room-title sightings into thin group DM conversation candidates. A candidate should include:

- room/title string exactly as visible;
- title variants from memory or obvious spelling/stylization;
- image sequence references;
- known members from images only;
- candidate members from chat memory separately;
- likely existing World/Pit surface only if checked;
- next DB queries and unresolved checks.

Do not promote a candidate conversation to known room status unless repo/DB evidence was checked and supports it.

## 4. Entity hints

Entity hints are query accelerators. They are not resolutions. Use them to point Albert toward likely matches, possible aliases, and search terms.

Example:

```json
{
  "observed_string": "haikave octypus",
  "likely_entity": "Ku / @HaikuPlatypus",
  "resolution_status": "likely_known_character",
  "basis": "synthesis",
  "must_verify": true
}
```

## 5. Rooms-specific insight leads

Capture patterns such as identity assimilation, transplanted membership, room lineage, women/ladies-room leads, drop-room mechanics, or theme-room ecology as `semantic_clusters` and `world_handoff_candidates`. Keep these review-only.


## 6. DB promotion companion pass

Run this pass when Harley has finished identifying people, rooms, handles, current profiles, or relationship fragments and the packet will feed Pit/ProjectDB promotion.

Create a `db_promotion_companion/` folder using `references/db_mutation_proposal_csvs.md`. The companion CSVs should translate observations into DB-routing proposals: conversations, memberships, message fragments, observed entities, handles, alias/name forms, and relationship fragments.

Keep direct image evidence separate from Harley-context or profile screenshots. For example, a screenshot-visible display name can become an observed entity proposal, while Harley's later browser/profile identification becomes a separate resolution proposal.

The worker must still verify live schema and duplicate state before using the ProjectDB command/unit-of-work layer.

## 7. Packet generation

When image files are available locally, use:

```bash
python scripts/build_sidecar_packet.py \
  --input-dir /path/to/images \
  --sidecar semantic_sidecar.json \
  --sidecar-md semantic_sidecar.md \
  --readme README_FOR_ALBERT.md \
  --output /path/to/output.zip
```

The helper copies images into `raw/` with sequence prefixes, computes hashes, writes `starter_manifest.json`, and includes the supplied packet-root sidecar files plus any `db_promotion_companion/` folder before writing the zip.

The helper does not analyze images. GPT performs the visual analysis before invoking it.
