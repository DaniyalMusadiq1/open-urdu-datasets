---
language:
- ur
pretty_name: Klam (کلام)
configs:
- config_name: klam
  default: true
  data_files:
  - split: train
    path: "klam/data/*.jsonl.gz"
---

# Klam (کلام)

Klam is one easy-to-use collection for Urdu and Roman Urdu data. It combines the project's currently published collections in one consistent record format. The current release contains about **2.2 million records**.

## Load the dataset

Install Hugging Face Datasets:

```bash
python -m pip install "datasets>=3,<5"
```

Then load Klam:

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

for row in data.take(3):
    print(row["text"])
```

You can use `text` and ignore the other fields for basic text work. The common fields are:

| Field | Meaning |
| --- | --- |
| `id` | Stable Klam record ID |
| `text` | Original text; not rewritten |
| `language`, `script` | Language and writing system |
| `task` | `text`, `sentiment_classification`, or `romanization` |
| `label`, `roman`, `split` | Task fields; blank when not used |
| `source`, `source_version` | Source and pinned source-release manifest |
| `license`, `license_url`, `attribution` | Reuse information for this record |
| `review_status` | Whether people have reviewed the record |
| `word_count` | Whitespace-delimited word count |
| `metadata_json` | Original source metadata for traceability |

## Reuse terms

Klam brings multiple openly licensed collections into one dataset, but the content does not have one universal license. Every row carries its own license and attribution, and `sources.json` records the full source manifests used in this Klam release. You can use one Klam release and cite its Hugging Face revision; Klam keeps the source details alongside it. Follow the terms attached to the records you use.

## Quality and review

**Native-speaker verified records: 0.** The records remain marked `unreviewed`. Automated filtering and file checks do not confirm linguistic correctness, privacy, or safety. Review records for your intended use.

The JSONL.GZ files under `klam/data/` are the single normalized dataset. Source-specific files and manifests remain available in their folders for audit and reproducibility, but users can load Klam without selecting among them.
