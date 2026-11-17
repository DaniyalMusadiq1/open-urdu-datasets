---
language:
- ur
license: cc-by-sa-4.0
task_categories:
- text-generation
- translation
pretty_name: Dakshina Urdu native text and word romanizations, deduplicated
---

# Dakshina Urdu native text and word romanizations

**150,000 published native training records**, containing **2,935,498 whitespace-delimited tokens**, in three compressed files (17,762,005 bytes). All are locally unreviewed.

Only the first three training files of a previous 16-file build were uploaded. The other 13 files, including all bulk romanization and validation records, are absent. `manifest.json` counts the published subset; `full-build-manifest.json` preserves the earlier build metadata and must not be treated as available data.

| Record type | Split | Published records |
|---|---|---:|
| native_sentence | train | 150,000 |

## Fields and provenance

`id`, `record_type`, `split`, `text`, `roman`, `attestations`, nested `source`, `license`, `review_status`, `duplicate_source_occurrences`. `text` is the original publisher string. `roman` and `attestations` are null for native-text units; they are source-provided for word pairs. Every native unit has source page/revision URLs and source member/line; every row retains archive/member SHA-256. No English gloss, POS or example was invented.

## Quality and limitations

The published subset retains the earlier importer's exact deduplication and contact-pattern filtering. Whole-build source counts and exclusion totals are historical metadata; they are not subset counts. All three published files match their recorded SHA-256 digests.

The corpus is Wikipedia-domain text, not representative conversation or colloquial Urdu. Arabic-script filtering is not a guarantee of Urdu identity. Units may include headings/fragments, non-Urdu quotations, offensive or sensitive topics, historical/public names and errors. Contact-pattern screening cannot prove PII absence; no human toxicity/copyright/linguistic audit is claimed. No private records are intentionally included. All records remain `review_status: unreviewed`; source human attestations are not local native review.

This corpus overlaps the 25-record vocabulary sample and older Wikipedia resources; do not sum them as unique independent examples. No synthetic text, model training or source scraping was performed. Downloading the publisher archive is not scraping Wikipedia. The full archive was hashed, but only named Urdu native-text and lexical components were structurally audited; do not infer all other languages/components are verified.

## Rights

CC BY-SA 4.0; each record retains that license. Preserve original contributors, source article/revision links, publisher attribution and modification notices. Share adaptations under the applicable share-alike terms. See LICENSE and SOURCES.md. MIT applies only to project code/documentation.

## Loading and validation

```python
import gzip, json
from pathlib import Path
root = Path('datasets/corpora/dakshina-urdu-bulk')
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
for shard in manifest['shards']:
    with gzip.open(root / shard['path'], 'rt', encoding='utf-8') as stream:
        first = json.loads(next(stream))
        assert first['review_status'] == 'unreviewed'
```

Run `python scripts/validate_bulk.py` to stream every record through its schema, exact identity, duplicate, filtering, checksum and count checks. Rebuild with `python scripts/import_dakshina_bulk.py /path/to/dakshina_dataset_v1.0.tar NEW_OUTPUT NEW_WORK.sqlite`; outputs must not already exist. No original text is silently normalized.
