# Klam quick start

Klam is one Urdu dataset with a consistent format. The current release contains about **2.2 million records**.

## Load the data

Install Hugging Face Datasets:

```bash
python -m pip install "datasets>=3,<5"
```

Load and stream Klam:

```python
from datasets import load_dataset

data = load_dataset(
    "Daniyal643/open-urdu-datasets",
    split="train",
    streaming=True,
)

for row in data.take(3):
    print(row["text"])
    print(row["task"], row["script"])
```

Streaming reads a few rows at a time. Remove `streaming=True` to download the full release.

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

with open("klam-sample.jsonl", "w", encoding="utf-8") as output:
    for row in islice(data, 1000):
        output.write(json.dumps(row, ensure_ascii=False) + "\n")
```

## Reuse and review

- Use `text` for the content. `task` distinguishes general text, Roman Urdu sentiment, and romanization records.
- Each record includes `license`, `license_url`, and `attribution`. Klam includes different source licenses, so follow the license attached to each record you use.
- `source` and `source_version` preserve traceability. The release's `sources.json` stores full source manifests, so you only need to track the Klam release revision in your project.
- **Native-speaker review has not happened; records remain `unreviewed`.** Automated checks do not prove linguistic correctness or guarantee the absence of personal information.

See the [Klam dataset card](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets) for the field list and release details.
