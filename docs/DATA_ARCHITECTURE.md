# Data architecture

The repository keeps a simple Klam release for users and source-specific reference material for auditing. Klam is built only from original, explicitly permissioned, or rights-verified public-domain text; previously published third-party corpus packages are not inputs.

## Responsibilities

| Location | Purpose |
| --- | --- |
| GitHub `catalog/` | Canonical source inventory, evidence, published-subset counts and link checks |
| GitHub `datasets/<category>/<slug>/` | Cards, source notes, licenses, schemas and small or locally hosted data packages |
| GitHub `scripts/`, `src/`, `tests/` | Pinned import and validation code, normalization utilities and examples |
| Hugging Face `corpora/<slug>/` | Published JSONL.GZ corpus files and their release metadata |
| Hugging Face `classification/<slug>/` | Published task datasets, keeping source labels and task semantics explicit |
| Hugging Face `github-sync/` | Versioned snapshots of the GitHub catalog and selected project documentation |
| Hugging Face root `README.md` | Dataset card with separate loadable configurations and per-source license notes |

GitHub is the source of truth for repository code, the discovery catalog and documented processing rules. Hugging Face is the download and streaming location for the large generated releases. A catalog entry is not proof that its data is hosted. Check its `hosted`, `local_path`, `download_url` and verification evidence fields.

## Dataset package layout

Use one directory per source or independently versioned subset:

```text
datasets/<category>/<dataset-id>/
├── DATASET_CARD.md
├── SOURCES.md
├── LICENSE
├── manifest.json
├── checksums.sha256
└── data/
    └── *.jsonl or *.jsonl.gz
```

The generated Wikipedia and Sangraha releases keep large data and generated manifests on Hugging Face; GitHub carries their cards, source notes, licenses, build code and catalog evidence. Do not commit large generated releases to GitHub. Keep file paths aligned between GitHub metadata and the Hugging Face release family.

## Hugging Face layout and loading

The Hugging Face repository groups files by corpus family. Its root card defines a separate Datasets configuration for each schema:

- `urdu-wikipedia`
- `sangraha-verified-urdu` (combines the eight source shards in one logical configuration)
- `dakshina-urdu-native-text`
- `roman-urdu-sentiment`
- `urwikisource-pd-old`

Load one configuration at a time. Do not concatenate different configurations without an explicit schema mapping: source fields, task labels, script and license can differ. JSONL.GZ records are UTF-8 JSON objects, one per line. Dataset-specific cards and manifests define the fields, splits, record counts, whitespace-token counts and SHA-256 hashes.

Example:

```python
from datasets import load_dataset

dataset = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "urdu-wikipedia",
    split="train",
    streaming=True,
)
print(next(iter(dataset)))
```

The word `streaming` avoids materializing all records in memory; it does not change the data or its license. Pin the Hugging Face repository revision when exact repeatability is required.

## Provenance and quality rules

- Preserve source IDs, URLs, revision IDs, timestamps, creator/attribution fields and license fields when supplied by the source.
- Record source revision and source-file SHA-256 in release manifests. Record output shard hashes, counts and transformation settings too.
- Keep original source text available when a transformation is applied; document transformations and do not silently “correct” Urdu.
- Use exact duplicate identity checks only as documented. NFC normalization and whitespace collapse are comparison keys; they do not by themselves authorize rewriting stored text.
- Keep every record's `review_status`. Machine filters and upstream “verified” labels do not count as local human review.
- Keep evaluation material in a separate evaluation-only package and warn users against training or model-selection contamination.
- Treat contact-pattern checks as triage; never claim a corpus is PII-free on that basis.
- Do not merge datasets with incompatible licenses or label systems into one downloadable configuration.

See [license policy](LICENSE_POLICY.md), [dataset card template](DATASET_CARD_TEMPLATE.md), and [Hugging Face sync details](HUGGINGFACE_SYNC.md).
