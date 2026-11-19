# Urdu Wikipedia articles

This release contains **543,011 records and 96,417,163 whitespace-delimited
tokens** from the pinned 2026-11-01 dump. Whitespace units are not model tokens.
The CI release job rebuilds this corpus from the complete pinned dump, validates
every generated shard, and publishes the resulting manifest and checksums with
the data. The original source pages and revisions remain linked at record level.

Urdu Wikipedia text is available under CC BY-SA 4.0. Every record retains its
page, exact revision, and history links for attribution. This extraction strips
MediaWiki markup, applies a mechanical Arabic-script ratio filter, and removes
pages carrying common explicit copyright-exception templates. The filter is
not a complete rights review; pages can contain content with separate terms.
Check the source page and history before reuse, attribute Urdu Wikipedia, and
share adaptations under CC BY-SA 4.0.

Only main-namespace, non-redirect pages with substantial Arabic-script text
were retained. Exact duplicates were removed after NFC normalization and
whitespace collapse against repository text and within this source. This does
not detect paraphrases or alternate editions. The text was not corrected or
translated. Email-pattern matching is only triage, not a privacy guarantee.
All records remain `review_status: unreviewed`; native Urdu review is pending.

## Reproduce

Install the `ingest` extra, download the official dump whose SHA-256 is in
`manifest.json`, then run:

```sh
python scripts/import_urwiki_articles.py DUMP.xml.bz2 OUTPUT_DIR
python scripts/validate_urwiki_articles.py OUTPUT_DIR
```
