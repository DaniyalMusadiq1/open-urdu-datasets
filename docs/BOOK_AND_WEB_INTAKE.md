# Book and web intake

Inspected 2026-11-17. The original uploaded archives are unchanged. See `catalog/upload-intake.json` for archive/member SHA-256 digests and machine-counted sizes. This inventory is not human verification of the text.

| Supplied archive | Findings | Public use decision |
|---|---|---|
| DeewanEGhalibNuskhaHamidAliKhan.zip | 226-page image-only PDF; zero extractable text characters | OCR and edition-specific rights review needed; raw scan not hosted |
| qawaed-tazkeer-o-tanees.zip | PDF, DOCX and existing UTF-8 TXT; TXT has 112 nonempty lines and 2,005 whitespace tokens | Archive metadata asserts Public Domain Mark 1.0; hold supplied edition/transcription pending review. The independently licensed Wikisource page is hosted with its own provenance |
| urdu-grammar.zip | 172-page scan; sampled text layer contains CamScanner/library watermarks | OCR and permission/edition review needed; raw scan not hosted |

Internet Archive identifiers and creator fields are retained as source assertions, not independently established authorship or rights. Public Domain Mark describes asserted public-domain status; it is not CC0 or an affirmative license grant. The Ghalib work's age does not resolve the rights of a particular edition's commentary or editorial additions. Public availability alone is not a redistribution permission.

## Web collection performed

The fixed three-page crawl is scoped to Urdu Wikisource and Urdu Wikipedia. See the [dataset card](../datasets/corpora/wikimedia-urdu-web-sample/DATASET_CARD.md) and `catalog/web-corpora.json`. Wikimedia page notices and terms provide the CC BY-SA reuse basis. Preserve original author/contributor attribution and revision/history URLs and share-alike terms.

The crawler checked each site's robots.txt for canonical `/wiki/` URLs. It does not recursively follow links or fetch restricted `/w/` API paths. Requests are sequential, identify the project and pause at least two seconds between pages. It stops on errors rather than attempting access workarounds. Robots permission and content license are checked separately.

The collection contains three page-level records and 14,777 whitespace-delimited tokens. They are not 14,777 unique words or independent examples. Qawaed overlaps the uploaded transcription's work; Wikipedia can overlap Dakshina. All text remains `unreviewed`. This addition does not satisfy the million-record goal or replace native review.

For a substantially larger collection, prefer publisher dumps after source-specific rights review instead of crawling millions of live pages. New sites require their own terms, license, robots and privacy checks before enabling collection.

## Checks

`python scripts/validate_web.py` checks source evidence, per-document identities, duplicates, token counts, data/metadata checksums and held-book publication flags. `python -m pytest tests/test_web.py` checks the URL allowlist, UTF-8 extraction, revision capture, script removal and missing-licensing rejection using synthetic markup fixtures.
