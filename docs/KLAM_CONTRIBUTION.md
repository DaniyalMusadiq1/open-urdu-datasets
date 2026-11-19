# Contribute to Klam

Klam is one simple Urdu dataset made from sources with documented redistribution rights. Existing approved input sources are combined into one normalized Klam release. To suggest another source, provide its publisher, exact version, license, rights evidence, attribution requirements, and checksum or revision.

## Rights

Only submit material with clear CC0, CC BY, CC BY-SA, or evidenced public-domain rights. Keep attribution and share-alike requirements. Do not include books, news, scraped pages, or OCR until exact rights are established. Publicly accessible does not mean redistributable.

## Record format

Add one UTF-8 JSON object per line. Required fields:

- `text`: original text
- `source_id`, `source_record_id`, `source_locator`: traceable provenance
- `script`: `Arabic`, `Latin`, or `Mixed`
- `task`, `label`, `split`: task details; empty strings when not applicable
- `review_status`: `unreviewed` until a person reviews the text

Klam generates the stable ID and fills source version, license, rights evidence, and attribution from the approved registry.

## Quality

Do not submit synthetic or AI-generated records. Keep source text unchanged except for documented extraction cleanup. Exact duplicates are removed; similar text may remain. Mark text `human_reviewed` only with a reviewer ID, review date, and review scope.

All newly imported records start as `unreviewed`. Automated language filters are not a substitute for native Urdu review.
