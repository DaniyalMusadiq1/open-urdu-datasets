# Open Urdu Dataset

A simple, source-traceable Urdu text dataset.

## Start here

Use the **Sangraha Urdu text collection**, the default dataset for this project. It contains **1,491,487 records** in one consistent text format. Its source declares **CC BY 4.0**.

- [Open the dataset on Hugging Face](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets)
- [Read the quick start](docs/QUICKSTART.md)
- [Check the source, license, and quality details](CATALOG.md)

Install the Hugging Face Datasets library:

```bash
python -m pip install "datasets>=3,<5"
```

Load the default dataset and print a few rows:

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

Streaming lets you start without downloading the full collection into memory. Keep the source attribution and follow the license when reusing the data.

## What “trusted” means

The release is linked to a pinned source and includes manifests, record counts, checksums, and automated processing checks.

**The text has not been reviewed by native Urdu speakers.** Records are marked `unreviewed`. Automated checks and the source's word “verified” do not confirm linguistic correctness or establish that the data is safe, private, or human-reviewed. Review it for your intended use.

## More datasets

The project also lists optional task-specific datasets. Their formats and licenses differ, so they remain separate. You can ignore them if you only need the default Urdu text collection.

See the [dataset catalog](CATALOG.md) or [all published files](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets/tree/main).

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding data. Include the source, license, and validation evidence. Never label text as human-reviewed unless a person has reviewed it.
