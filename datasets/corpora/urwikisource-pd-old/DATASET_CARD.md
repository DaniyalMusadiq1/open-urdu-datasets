# Urdu Wikisource — explicitly tagged PD-old pages

This release contains **6,366 page-level transcriptions / 1,300,675 whitespace-delimited tokens** extracted from the official Urdu Wikisource XML export dated 2026-11-01. Only main-namespace pages carrying the explicit `{{PD-old}}` template were considered. The source dump had 11,980 main-namespace pages.

The Wikisource policy defines `PD-old` for works whose authors died more than 100 years ago and describes the tag as public domain worldwide. This is a conservative source-level filter, not a substitute for reviewing a specific page's history or rights status. Pages with conflicting license markers, non-Urdu-script-heavy text, contact-pattern matches, or too little extracted text were excluded. Five exact duplicates inside this source and any exact matches against repository JSONL text fields were removed.

## Files and fields

- `data/pages-*.jsonl.gz`: deterministic gzip-compressed JSONL shards.
- `manifest.json`: source snapshot, extraction method, counts, exclusions, and shard hashes.
- `checksums.sha256`: SHA-256 for every data shard.
- `SOURCES.md`: source, rights-policy and attribution details.
- `LICENSE`: license for the compilation and transcription contribution. Underlying public-domain works remain public domain.

Each record preserves the extracted Urdu text, page title, source page, revision ID and timestamp, fixed revision URL, page history URL, rights tag, collection license, review status, and whitespace token count. Extraction removes MediaWiki markup and does not correct, modernize, translate or otherwise edit the text.

## Quality and review

All records are `review_status: unreviewed`; `human_verified_records` is zero. Automated checks cover explicit rights-tag presence, extraction length, script ratio, exact deduplication, likely contact-pattern triage, and file hashes. They do not establish linguistic correctness, OCR fidelity, privacy, completeness, or native-speaker review. No AI-generated text was added.

Deduplication removes exact text matches after NFC normalization and whitespace collapse. It does not detect alternate editions, paraphrases, quoted passages, or semantic overlap. The Urdu Wikisource export is a snapshot and may change in later monthly exports.

## Reproduction

Install the `wikimedia` extra and download the pinned dump listed in `manifest.json`, then run:

```sh
python scripts/import_urwikisource_pd_old.py DUMP.xml.bz2 OUTPUT_DIR
python scripts/validate_urwikisource_pd_old.py OUTPUT_DIR
```

The importer refuses a dump whose SHA-256 differs from the pinned source hash and refuses to overwrite an existing output directory.
