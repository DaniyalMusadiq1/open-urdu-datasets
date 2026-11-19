# Quick start

For the simplest start, use the main Urdu text collection: **Sangraha Urdu**, with 1,491,487 records.

## Load and stream the data

Install the Hugging Face Datasets library:

```bash
python -m pip install "datasets>=3,<5"
```

Then load the dataset:

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "sangraha-verified-urdu",
    split="train",
    streaming=True,
)

for row in data.take(3):
    print(row["text"])
    print(row["review_status"])  # currently "unreviewed"
```

Streaming reads a few rows at a time, so you can start without downloading the whole collection. Remove `streaming=True` if you want Hugging Face Datasets to download and prepare the full collection locally.

## Save a small JSONL sample

```python
import json
from itertools import islice
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "sangraha-verified-urdu",
    split="train",
    streaming=True,
)

with open("urdu-sample.jsonl", "w", encoding="utf-8") as output:
    for row in islice(data, 1000):
        output.write(json.dumps(row, ensure_ascii=False) + "\n")
```

Change `1000` to a smaller or larger number. Remove the `islice` wrapper to export the full dataset; the full download takes more time and disk space.

## Trust, license, and limits

- The source declares **CC BY 4.0**. Follow its attribution terms.
- The release includes source and review metadata. Keep these fields with records you reuse.
- **Native-speaker review is pending; all records are marked `unreviewed`.** Automated checks do not confirm linguistic correctness or guarantee that data is free of personal information.
- For reproducible work, pin the Hugging Face dataset revision and record it with your project.

See the [dataset card](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets) for provenance, schema, and limitations. The repository has additional task-specific collections with separate licenses; see the [catalog](../CATALOG.md) if you need those.
