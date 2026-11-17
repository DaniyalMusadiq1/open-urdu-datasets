# Wikimedia Urdu web sample

Three whole-page documents, 14,777 whitespace-delimited tokens. Collected on 2026-11-17 from Urdu Wikisource and Urdu Wikipedia. This is a small grammar/literature sample, not a representative corpus or a count of independent sentences. All documents are `review_status: unreviewed`.

## Source and rights

CC BY-SA 4.0. Original literary authors and Wikimedia contributors retain attribution. Each record includes the page URL, revision ID, revision URL and contributor history. See SOURCES.md, the licensing notice on each source page, the Wikimedia terms, and the included license. Preserve attribution and share-alike terms for adaptations. The project code license does not replace the data license.

This collection is independent of the uploaded PDF editions. Its rights/provenance do not authorize redistribution of those scans. The supplied Qawaed Unicode transcription is tracked separately in catalog/upload-intake.json; no uploaded book bytes are republished here.

## Collection and transformations

The fixed three-page allowlist is in scripts/crawl_wikimedia.py. No recursion, search-result harvesting, paywall access or login. robots.txt was checked for each canonical /wiki/ path and its response is preserved. A descriptive User-Agent, gzip requests, sequential access, response-size limits and a two-second minimum delay limit load. HTTP errors stop collection. Revisions are read from the returned HTML, not fetched using oldid URLs.

HTML markup, navigation, scripts, styles and edit controls were removed. Nonempty text lines were trimmed and joined with newlines. Text is not translated, corrected, normalized to NFC or generated. Some in-article layout, template artifacts and footnote numbering may remain; verse boundaries and tables may lose formatting. This is not a checked OCR or critical edition.

## Limitations

No local human language review, sentence segmentation, grammar-label annotation, toxicity audit or full rights audit of every quotation is claimed. Wikipedia content can overlap the existing Dakshina corpus. Exact document hashes detect duplicate pages within this sample only; do not sum it with other corpora as unique text. Old grammatical prescriptions may differ from current usage. Sensitive names/topics and errors may occur in public text.

## Load and verify

```python
import gzip, json
with gzip.open('datasets/corpora/wikimedia-urdu-web-sample/data/documents.jsonl.gz', 'rt', encoding='utf-8') as stream:
    documents = [json.loads(line) for line in stream]
```

Run `python scripts/validate_web.py`. To make a new snapshot, install `.[web]` and run `python scripts/crawl_wikimedia.py NEW_OUTPUT`; the output directory must not exist. New snapshots require rights and content checks before publication.
