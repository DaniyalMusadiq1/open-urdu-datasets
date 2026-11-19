# Contribute original content to Klam

Klam's core release is built from material created for Klam, contributor submissions with explicit permission, CC0-dedicated source texts, and public-domain works whose status is verified for the exact work and edition. Preassembled third-party NLP datasets are not Klam source material.

## Before adding text

1. Add the source to `datasets/klam/sources.json`.
2. Include its source URL or local source description, exact version, rights basis, evidence link, license, and attribution.
3. Ask a maintainer to review the rights evidence and set `rights_status` to `approved`.
4. Only then add records to `datasets/klam/records/`.

For original and contributor-submitted text, Klam requires explicit permission to redistribute under CC BY 4.0. Keep consent evidence outside the public repository; record that the maintainer checked it. For CC0 source text, retain the exact pinned source version and a link that explicitly dedicates the text under CC0. For public-domain text, document the author, work, edition, publication history, and evidence for the exact edition. A downloadable book page or a public-domain label by itself is not enough.

A source registry entry follows [the source schema](../schemas/klam-source.schema.json). For original or contributor-permissioned text, it needs fields such as `rights_basis`, `rights_status`, `license`, `rights_evidence_url`, `attribution`, and `permission_evidence_recorded: true`. Use real evidence; never fill unknown fields with guesses. Do not put contributor names, emails, signatures, or private consent files in the public registry. Keep consent evidence securely with the maintainer.

## Record format

Add one record per UTF-8 JSONL line with these fields:

- `text`: original text, unchanged
- `source_id`, `source_record_id`, `source_locator`: traceable source and location
- `script`: `Arabic`, `Latin`, or `Mixed`
- `task`: a plain task name, such as `text` or `sentiment_classification`
- `label`, `split`: use empty strings if not applicable
- `review_status`: `unreviewed` until a person reviews the record

The build fills the stable Klam ID, source version, rights, license, and attribution from the approved source registry. All records share one simple output schema.

## Quality rules

- Do not submit synthetic or AI-generated text as source data.
- Do not use scraped text, OCR drafts, books, news, or translations until redistribution rights are clear.
- Do not change source text silently. Record any extraction or cleanup method.
- Mark text `human_reviewed` only with a reviewer ID, review date, and review scope.
- Keep personal data out. Contact-pattern scans are only triage.
- The release builder rejects unapproved sources and exact duplicate text.

Klam currently includes a CC0-dedicated digital transcription of Ghalib's poetry. Its 307 records are marked unreviewed. New sources still require rights review and record validation before release.
