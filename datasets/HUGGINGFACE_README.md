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

This Hub repository contains separate, source-aware configurations. Select one corpus at a time; each configuration preserves its own fields and source meaning. This is a mixed-license repository, so the license is stated per corpus below and in each folder's `LICENSE` and `SOURCES.md` files.

## Available configurations

| Configuration | Records | Whitespace tokens | License | Dataset card |
| --- | ---: | ---: | --- | --- |
| `urdu-wikipedia` | 543,011 | 96,417,163 | CC BY-SA 4.0 | [card](corpora/urwiki-articles/DATASET_CARD.md) |
| `sangraha-verified-urdu` | 1,491,487 | 905,720,516 | CC BY 4.0 declared upstream | [card](corpora/sangraha-verified-urdu/DATASET_CARD.md) and shard cards |
| `dakshina-urdu-native-text` | 150,000 | 2,935,498 | CC BY-SA 4.0 | [card](corpora/dakshina-urdu-bulk/DATASET_CARD.md) |
| `roman-urdu-sentiment` | 27,106 | 528,943 | CC BY 4.0 | [card](classification/uci-roman-urdu-sentiment/DATASET_CARD.md) |
| `urwikisource-pd-old` | 6,366 | 1,300,675 | CC BY-SA 4.0 compilation | [card](corpora/urwikisource-pd-old/DATASET_CARD.md) |

The counts above describe the currently published files. The project-wide corpus total is 2,217,970 records and 1,006,902,795 whitespace-delimited tokens. These are whitespace counts, not model-token counts. Native-speaker verified records: **0**. Text remains unreviewed unless a record says otherwise.

## Load and stream

Install `datasets`:

```bash
python -m pip install "datasets>=3,<5"
```

Then load a configuration by name:

```python
from datasets import load_dataset

rows = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "sangraha-verified-urdu",
    split="train",
    streaming=True,
)

for row in rows.take(3):
    print(row["text"], row["review_status"])
```

For repeatable work, pin the repository to a commit revision and record that revision in your own experiment metadata. The file-level source revisions and SHA-256 values are recorded in each release manifest.

## License and use

This repository does not have one universal content license. Retain the original attribution and comply with the license for the configuration you use. Sangraha's upstream card declares CC BY 4.0. The corpus “verified” label and automated language filters are not local human review.

Exact duplicate checks use NFC-normalized text after whitespace collapse; they do not remove semantic, quotation or near-duplicate overlap. Contact-pattern checks are triage and do not establish that data contains no personal information. See each dataset card, `manifest.json`, and `checksums.sha256` before redistribution.
