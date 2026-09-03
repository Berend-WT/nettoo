# Netto photo catalog — question-linked pilot

This folder is a standalone media catalog. It does not change the website frontend or the existing puzzle data.

## Contents

- `question_media_pilot.xlsx` — review workbook with five sheets and embedded thumbnails.
- `assets/` — optimized JPEG thumbnails downloaded from Wikimedia Commons.
- `maak_fotocatalogus.py` — reproducible generator for this pilot.

## Lookup model

```text
puzzle_id + question_slot → question_id → media_id → asset/source/licence
```

Question IDs are SHA-256-derived from normalized canonical question text. They are stable across puzzle placements, so a repeated question can reuse the same image relationship.

## Review requirements

Every media row records the original Commons file page, direct file URL, creator, licence, licence URL, attribution text, alt text, and answer-reveal risk. The status is intentionally `review needed`; an editor should approve or replace each image before production use.

The pilot attaches one contextual image to each of the first 25 library puzzles. The other question slots remain mapped with an empty `media_id`, so the catalog does not force irrelevant images onto abstract questions.

Generated catalog: 25 media records, 75 unique question IDs, 75 puzzle-question mappings.

## License note

Images were selected directly through the Wikimedia Commons API from files whose metadata reports a reusable CC BY, CC BY-SA, CC0, or Public Domain Mark licence. The workbook records the original Commons file page, creator, licence, attribution text, and direct asset URL. Always retain the recorded attribution and re-check the source page before publishing; file metadata can change.
