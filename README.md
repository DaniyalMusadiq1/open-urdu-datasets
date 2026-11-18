# Open Urdu Datasets

A source-aware collection of Urdu and Roman Urdu datasets with clear provenance, license notes, reusable files and validation tools.

**Published corpus:** 2,217,970 records and 1,006,902,795 whitespace-delimited tokens. This count is a text-size measure, not a model-token count. Native-speaker verified records: **0**. Records that have not received native-speaker review are labeled `unreviewed`.

[Browse the dataset on Hugging Face](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets) · [Browse the catalog](CATALOG.md) · [How the data is organized](docs/DATA_ARCHITECTURE.md) · [Contribute](CONTRIBUTING.md) · [Licensing and removal](docs/LICENSE_POLICY.md)

## What is here

The collection keeps each source separate so its schema, license, attribution and quality notes travel with the data.

| Collection | Records | Whitespace tokens | License | Record review |
| --- | ---: | ---: | --- | --- |
| Urdu Wikipedia articles | 543,011 | 96,417,163 | CC BY-SA 4.0 | Unreviewed |
| AI4Bharat Sangraha verified Urdu, data-0–7 | 1,491,487 | 905,720,516 | CC BY 4.0 declared upstream | Unreviewed |
| Dakshina Urdu native text (published subset) | 150,000 | 2,935,498 | CC BY-SA 4.0 | Unreviewed |
| UCI Roman Urdu sentiment sources | 27,106 | 528,943 | CC BY 4.0 | Pending review |
| Urdu Wikisource pages tagged PD-old | 6,366 | 1,300,675 | CC BY-SA 4.0 compilation | Unreviewed |

The aggregate is deduplicated using exact text identity checks. It does not mean the sources are semantically unique: quotations, alternate editions and near duplicates may remain. Read each dataset card before use. Licenses and attribution rules apply separately to each source.

## Load a dataset

Install the Hugging Face Datasets library:

```bash
python -m pip install "datasets>=3,<5"
```

Each published corpus has its own configuration because fields and labels differ by source. For example, stream the Sangraha corpus:

```python
from datasets import load_dataset

rows = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "sangraha-verified-urdu",
    split="train",
    streaming=True,
)

for row in rows.take(3):
    print(row["text"], row["review_status"])
```

Other configurations are `urdu-wikipedia`, `dakshina-urdu-native-text`, `roman-urdu-sentiment`, and `urwikisource-pd-old`. The [Hugging Face dataset card](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets) lists each configuration, its files and its license. Use a pinned Hugging Face revision when you need a reproducible snapshot.

Small local examples are available too: the [25-record Dakshina vocabulary sample](datasets/vocabulary/dakshina-urdu-sample/) and the [five-pair Belebele evaluation sample](datasets/translation/belebele-urdu-english-eval-sample/). The Belebele sample is evaluation-only; do not train or select models with it. These derived examples are not part of the published corpus total.

Run the local examples with:

```bash
python -m pip install -e ".[examples]"
python examples/plain_python.py
```

## In this repository

- `catalog/datasets.json` is the canonical machine-readable source inventory; `catalog/datasets.csv` is its typed, generated counterpart.
- `catalog/processed-corpora.json` records the published subsets and counts.
- `datasets/` holds dataset cards, source and license records, schemas, and small or locally hosted releases.
- `src/`, `scripts/`, and `tests/` contain reusable readers, importers, validators and checks.
- The large Wikipedia and Sangraha releases are hosted on Hugging Face. Their source pins, filters, manifests and checksums travel with the release.

See [data architecture](docs/DATA_ARCHITECTURE.md), [catalog definitions](CATALOG.md), [development guide](docs/DEVELOPMENT.md), and [coverage gaps](docs/COVERAGE.md).

## Data quality

The catalog distinguishes technical source/file checks from review of Urdu content. A `verified` catalog status means the stated source and files passed the listed technical checks; it does **not** mean the Urdu was reviewed by a native speaker. Upstream labels such as “verified” are not this project's human review.

Exact duplicate checks use SHA-256 over NFC-normalized text after whitespace collapse. This does not remove semantic or near-duplicate text. Automated language identification, script filters and contact-pattern screening have stated limits and are not guarantees of linguistic accuracy, safety or privacy.

## Contribute

Check [CONTRIBUTING.md](CONTRIBUTING.md) and the [dataset card template](docs/DATASET_CARD_TEMPLATE.md) before adding a source. Include its original license, immutable source reference, source hashes, record schema, transformation steps and validation evidence. Do not mark text as human reviewed without actual human review.

The English README is maintained as the primary guide. [The Urdu introduction](README.ur.md) is still marked unreviewed.
