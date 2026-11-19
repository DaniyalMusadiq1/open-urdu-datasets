# Klam data architecture

Klam is one dataset for users. The build combines approved, version-pinned Urdu sources into one normalized release. It removes duplicate records with the same normalized text, task, and label, while carrying record-level provenance, license, and review metadata.

## Where things live

| Location | Purpose |
| --- | --- |
| `datasets/klam/sources.json` | Approved sources, versions, rights evidence, licenses, and attribution |
| `datasets/klam/records/` | Klam-originated records |
| `schemas/klam-record.schema.json` | Normalized record format |
| `scripts/build_klam_release.py` | Builds the unified Klam release |
| Hugging Face `klam-original/` | Loadable Klam records, source list, license notes, and checksums |
| Other corpus folders | Reproducible input collections used to build Klam; users can ignore them |

GitHub holds the source registry and reproducible build. Hugging Face exposes one default Klam config, so users can load Klam without selecting the input datasets.

## What each row contains

Text, title where available, language and script, task and label where available, source ID and exact source record ID, locator, source version, license and rights evidence, attribution, and review status. Transliteration pairs keep the Urdu side in `text` and the Roman side in `paired_text`, with a script tag for each side. Duplicate records are detected after Unicode NFC normalization and whitespace collapse, with task, label, and both pair sides included so alternate Roman spellings remain distinct. Similar text may remain.

A Klam release has one manifest with record totals, source and license counts, file checksums, and source versions. The same source and license details needed for reuse stay with every row.

## Loading

```python
from datasets import load_dataset

data = load_dataset("Daniyal643/open-urdu-datasets", split="train", streaming=True)
for row in data.take(3):
    print(row["text"], row["license"], row["source_id"])
```

See the [quick start](QUICKSTART.md), [license policy](LICENSE_POLICY.md), and [record schema](../schemas/klam-record.schema.json).

