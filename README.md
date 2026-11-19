# Open Urdu Dataset

A simple, source-traceable dataset for working with Urdu text.

## Start here

Use the **Sangraha Urdu text collection** as the main starting dataset. It contains **1,491,487 records** in one consistent text format and has one declared source license: **CC BY 4.0**.

- [Open the dataset on Hugging Face](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets)
- [Read the simple usage guide](docs/QUICKSTART.md)
- [See source, license, and quality details](CATALOG.md)

```bash
python -m pip install "datasets>=3,<5"
```

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
```

Streaming lets you read records without downloading the entire dataset into memory. Keep the dataset’s attribution and license information when sharing or publishing data derived from it.

## What “trusted” means here

The release is traceable to a pinned upstream source. Its published files have manifests, record counts, and checksums, and automated checks were used during processing.

**No records have been reviewed by a native Urdu speaker yet.** All records remain marked `unreviewed`. Automated checks and the upstream word “verified” do not establish that text is linguistically correct, safe, private, or human-verified. Check the dataset card and review the data for your intended use.

The Sangraha source declares **CC BY 4.0**. See the source card for attribution and reuse terms.

## Other collections

The project also indexes smaller task-specific datasets, such as Roman Urdu sentiment and evaluation data. They have different fields, purposes, and license terms, so they are kept separate. You can ignore them if you only need the main Urdu text collection.

Browse the [dataset catalog](CATALOG.md) or [all published files](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets/tree/main).

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding data. Every contribution should include its source, license, and validation evidence. Do not label Urdu text as human-reviewed unless a person has actually reviewed it.
