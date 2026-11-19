# Klam (کلام)

One simple, source-traceable Urdu dataset.

Klam brings the project's published Urdu and Roman Urdu collections together in **one consistent format** and one dataset you can load directly. The current release contains about **2.2 million records**.

## Start here

Install Hugging Face Datasets:

```bash
python -m pip install "datasets>=3,<5"
```

Load Klam and print a few records:

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

The main field is `text`. Each row also carries task, script, source, release version, license, attribution, and review status. You can ignore those fields for a quick start; they are there when you need them.

## Clear reuse information

Klam combines material with different source licenses, so the whole dataset does **not** have one license. Every record includes its own `license`, `license_url`, and ready-to-use `attribution`. The `sources.json` file explains the source records and versions in this Klam release. Users can cite one Klam release while the source details stay available in the data.

**Native-speaker verified records: 0.** Text remains marked `unreviewed` unless a record says otherwise. Automated checks do not establish linguistic correctness, privacy, or safety.

- [Open Klam on Hugging Face](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets)
- [Read the quick start](docs/QUICKSTART.md)
- [See source and reuse details](CATALOG.md)

## Contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding data. Each contribution needs a clear source, reuse terms, and validation evidence. Never mark text human-reviewed unless a person has reviewed it.
