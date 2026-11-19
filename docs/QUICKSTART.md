# Quick start

The simplest option is the default **Sangraha Urdu** collection: **1,491,487 records**.

## Load a few rows

Install Hugging Face Datasets:

```bash
python -m pip install "datasets>=3,<5"
```

Load and stream the default collection:

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

for row in data.take(3):
    print(row["text"])
    print(row["review_status"])  # "unreviewed"
```

Streaming reads a few rows at a time. Remove `streaming=True` if you want to download the full collection.

## Save a small JSONL sample

```python
import json
from itertools import islice
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

with open("urdu-sample.jsonl", "w", encoding="utf-8") as output:
    for row in islice(data, 1000):
        output.write(json.dumps(row, ensure_ascii=False) + "\n")
```

Change `1000` to save a different number of rows. Exporting the full collection takes more time and disk space.

## License and review status

- The source declares **CC BY 4.0**. Follow its attribution terms.
- Keep the source and review metadata when reusing records.
- **Native-speaker review has not happened; records are marked `unreviewed`.** Automated checks do not confirm linguistic correctness or guarantee that the data contains no personal information.
- For reproducible work, record the dataset revision you used.

See the [dataset card](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets) for source details and limitations. Other task-specific collections are optional and listed in the [catalog](../CATALOG.md).
