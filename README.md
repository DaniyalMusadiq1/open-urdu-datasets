# Klam (کلام)

Klam is one easy-to-use Urdu dataset. It combines the project's approved, openly licensed Urdu sources into one JSONL.GZ format, removes duplicate records with the same normalized text, task, and label, and keeps the source, version, attribution, license, and review status with every record.

The release is built from pinned Dakshina, Urdu Wikisource PD-old, Urdu Wikipedia, UCI Roman Urdu sentiment, AI4Bharat Sangraha verified Urdu, and the CC0 Ghalib transcription. Source-specific terms remain attached to each row; Klam does not replace them. All unreviewed records stay marked `unreviewed`; automated language filters are not human review. See the generated dataset card for exact release counts.

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
    if row["task"] == "transliteration_pair":
        print(row["paired_text"])
```

Users can use this one dataset without installing or selecting its upstream datasets. The row fields and `sources.json` keep provenance available for attribution and audit.

- [Quick start](docs/QUICKSTART.md)
- [Sources and licensing](docs/LICENSE_POLICY.md)
- [Contribution guide](docs/KLAM_CONTRIBUTION.md)

Klam aims for broad coverage of currently available, rights-cleared Urdu sources. It does not claim to contain all Urdu text, and no record is marked human-reviewed without reviewer evidence.

