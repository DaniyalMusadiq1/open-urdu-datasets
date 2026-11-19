---
language:
- ur
pretty_name: Klam (کلام)
configs:
- config_name: klam
  default: true
  data_files:
  - split: train
    path: "klam-original/data/train/*.jsonl.gz"
  - split: validation
    path: "klam-original/data/validation/*.jsonl.gz"
  - split: test
    path: "klam-original/data/test/*.jsonl.gz"
---

# Klam (کلام)

Klam is one easy-to-use Urdu dataset in a single normalized JSONL.GZ format. It brings together the project's approved, pinned sources and removes duplicate records with the same normalized text, task, and label. Every row includes its source, source version, license, attribution, and review status.

The release includes rights-cleared Urdu text from Dakshina, Urdu Wikisource works tagged PD-old, Urdu Wikipedia, UCI Roman Urdu sentiment datasets, AI4Bharat Sangraha verified Urdu, and a CC0 Ghalib transcription. Klam preserves the applicable source terms: licenses can differ by row. See `klam-original/DATASET_CARD.md` and `klam-original/SOURCES.md` for actual release counts, source details, and license summaries.

No automated filter counts as native-speaker review. Records without reviewer evidence are marked `unreviewed`.

## Load Klam

```bash
python -m pip install "datasets>=3,<5"
```

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)
for row in data.take(3):
    print(row["text"], row["license"], row["source_id"])
```

Users can load this one dataset without selecting upstream datasets or managing their revisions. Per-record provenance and license fields carry those details inside Klam.

See the [quick start](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/QUICKSTART.md) and [license policy](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/LICENSE_POLICY.md).

