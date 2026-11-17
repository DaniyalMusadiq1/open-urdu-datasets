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

**622,805 real, technically validated, locally unreviewed records** from explicitly licensed publisher files. This is not millions of records. Native text contains **8,948,752 whitespace-delimited tokens** (not model tokens, unique words or native-reviewed words).

| Record type | Split | Retained records |
|---|---|---:|
| native_sentence | train | 470,397 |
| native_sentence | validation | 25,207 |
| romanization_pair | dev | 10,424 |
| romanization_pair | test | 10,517 |
| romanization_pair | train | 106,260 |

## Fields and provenance

`id`, `record_type`, `split`, `text`, `roman`, `attestations`, nested `source`, `license`, `review_status`, `duplicate_source_occurrences`. `text` is the original publisher string. `roman` and `attestations` are null for native-text units; they are source-provided for word pairs. Every native unit has source page/revision URLs and source member/line; every row retains archive/member SHA-256. No English gloss, POS or example was invented.

## Quality and limitations

Source candidates: 533,027 publisher-included native text rows and 127,201 romanization pairs. Removed 37,422 exact duplicate native rows, including 10,975 duplicates across train/validation; one email-like row was excluded. Retained native text: 495,604 units. Shards: 16; compressed total 63,998,560 bytes; largest 6,037,940 bytes. Every shard is below 20 MB and GitHub's 100 MB file limit. No Git LFS.

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
