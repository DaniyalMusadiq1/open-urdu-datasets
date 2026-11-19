# Klam quick start

Klam is being rebuilt as one original-source Urdu dataset with a consistent format.

**The new Klam data release is not ready to load yet.** Its source registry is empty, and records will be published only after rights and data checks pass. The previous mixed-source files are not part of this Klam release.

Once the release is available, the simple loading pattern will be:

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
```

For now, follow the [contribution guide](KLAM_CONTRIBUTION.md) to prepare original or explicitly permissioned text. Do not publish text from a book, OCR file, website, or dataset until its exact redistribution rights have been checked.
