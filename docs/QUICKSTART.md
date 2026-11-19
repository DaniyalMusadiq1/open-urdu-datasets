# Klam quick start

Klam is the single, normalized Urdu dataset release in this project. Its build combines approved pinned sources, removes exact duplicate text, and keeps license, version, attribution, and review status on each record.

## Load the dataset

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
    print(row["text"])
    print(row["license"], row["source_id"])
```

Use `text` as the text field. For attribution or reuse, check `license`, `license_url`, `attribution`, `source_version`, and `source_locator` on each record. The generated Klam dataset card reports the current record count and source breakdown.

Records without documented human review are marked `unreviewed`.
