---
language:
- ur
pretty_name: Open Urdu Datasets
configs:
- config_name: urdu-wikipedia
  data_files:
  - split: train
    path: "corpora/urwiki-articles/data/*.jsonl.gz"
- config_name: sangraha-verified-urdu
  default: true
  data_files:
  - split: train
    path:
    - "corpora/sangraha-verified-urdu/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-1/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-2/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-3/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-4/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-5/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-6/data/*.jsonl.gz"
    - "corpora/sangraha-verified-urdu-data-7/data/*.jsonl.gz"
- config_name: dakshina-urdu-native-text
  data_files:
  - split: train
    path: "corpora/dakshina-urdu-bulk/data/*.jsonl.gz"
- config_name: roman-urdu-sentiment
  data_files:
  - split: train
    path: "classification/uci-roman-urdu-sentiment/data/*.jsonl.gz"
- config_name: urwikisource-pd-old
  data_files:
  - split: train
    path: "corpora/urwikisource-pd-old/data/*.jsonl.gz"
---

# Open Urdu Datasets

## Start with one dataset

The default collection is **Sangraha Urdu**: 1,491,487 records in one consistent format. To load it, you do not need to choose a configuration:

```bash
python -m pip install "datasets>=3,<5"
```

```python
from datasets import load_dataset

rows = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

for row in rows.take(3):
    print(row["text"])
```

The source declares **CC BY 4.0**. The release has source details, manifests, record counts, and checksums. **The text has not been reviewed by native Urdu speakers**; records are marked `unreviewed`. Automated checks do not certify linguistic correctness or safety. See the [quick-start and export guide](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/QUICKSTART.md).

## Optional datasets

Other collections serve different tasks and have their own formats and licenses. Use them only when needed. This Hub repository is mixed-license; each collection's license is stated below and in its `LICENSE` and `SOURCES.md` files.

| Configuration | Records | Whitespace tokens | License | Dataset card |
| --- | ---: | ---: | --- | --- |
| `urdu-wikipedia` | 543,011 | 96,417,163 | CC BY-SA 4.0 | [card](corpora/urwiki-articles/DATASET_CARD.md) |
| `sangraha-verified-urdu` | 1,491,487 | 905,720,516 | CC BY 4.0 declared upstream | [card](corpora/sangraha-verified-urdu/DATASET_CARD.md) and shard cards |
| `dakshina-urdu-native-text` | 150,000 | 2,935,498 | CC BY-SA 4.0 | [card](corpora/dakshina-urdu-bulk/DATASET_CARD.md) |
| `roman-urdu-sentiment` | 27,106 | 528,943 | CC BY 4.0 | [card](classification/uci-roman-urdu-sentiment/DATASET_CARD.md) |
| `urwikisource-pd-old` | 6,366 | 1,300,675 | CC BY-SA 4.0 compilation | [card](corpora/urwikisource-pd-old/DATASET_CARD.md) |

Counts describe published files. Project-wide totals count records across collections and are not unique text totals. Native-speaker verified records: **0**.

## Source and license

Keep attribution and follow the license for the collection you use. The Sangraha upstream card declares CC BY 4.0. The word “verified” in its source name does not mean this project has completed local human review.

Exact duplicate checks use NFC-normalized text after whitespace collapse; they do not remove semantic, quotation, or near-duplicate overlap. Contact-pattern checks are triage and do not establish that data contains no personal information. See each dataset card, `manifest.json`, and `checksums.sha256` before redistribution. For repeatable work, record the dataset revision and source information.
