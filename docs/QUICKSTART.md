# Quick start

This repository publishes separate datasets for different tasks. Start with one configuration, read its card, and keep its source and license fields with your data.

## Choose a configuration

| Configuration | What it contains | Typical use |
| --- | --- | --- |
| `urdu-wikipedia` | Urdu Wikipedia articles | General Urdu text |
| `sangraha-verified-urdu` | Filtered Urdu web text from eight Sangraha source shards | General Urdu text |
| `dakshina-urdu-native-text` | Urdu text from the Dakshina project | Text and transliteration research |
| `roman-urdu-sentiment` | Roman Urdu text and source sentiment labels | Sentiment experiments |
| `urwikisource-pd-old` | Urdu Wikisource pages with an explicit public-domain-old tag | Historical and literary text |

“Verified” in the Sangraha source name is an upstream label. The project has not completed native-speaker review; the published records remain marked `unreviewed`. See the [catalog](../CATALOG.md) and each configuration's dataset card for license, provenance, fields, counts and limitations.

## Stream records

Streaming reads rows as needed and avoids loading a large configuration into memory.

```bash
python -m pip install "datasets>=3,<5"
```

```python
from datasets import load_dataset

rows = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "sangraha-verified-urdu",
    split="train",
    streaming=True,
)

for row in rows.take(3):
    print(row)
```

Change the configuration name to load another collection. Inspect a row before writing code that expects particular fields:

```python
print(rows.features)
```

For repeatable experiments, pass a commit ID with `revision="COMMIT_ID"` and save that ID with your experiment notes. The Hub page's Files and versions tab shows revisions.

## Save a streaming JSONL file

The published source files are UTF-8 JSON Lines compressed as `.jsonl.gz`. To export a sample without loading the full collection, stream rows to a local JSONL file:

```python
import json
from itertools import islice
from datasets import load_dataset

rows = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "urdu-wikipedia",
    split="train",
    streaming=True,
)

with open("urdu-wikipedia-sample.jsonl", "w", encoding="utf-8") as output:
    for row in islice(rows, 10_000):
        output.write(json.dumps(row, ensure_ascii=False) + "\\n")
```

Remove `islice(..., 10_000)` and iterate over `rows` to export the full configuration. The full exports are large and may take time and disk space.

## Use Parquet, Pandas or CSV

Hugging Face's Parquet converter has already created a Parquet view for this dataset. It is on the Hub's generated `refs/convert/parquet` branch and powers the dataset viewer. You can browse that [generated Parquet branch](https://huggingface.co/datasets/Daniyal643/open-urdu-datasets/tree/refs%2Fconvert%2Fparquet). It is a Hub-generated convenience view; the versioned JSONL.GZ releases and their manifests remain the project's published source files.

For a smaller configuration or a small filtered subset, Datasets can convert it locally:

```python
from datasets import load_dataset

dataset = load_dataset(
    "Daniyal643/open-urdu-datasets",
    "roman-urdu-sentiment",
    split="train",
)
dataset.to_parquet("roman-urdu-sentiment.parquet")
dataset.to_csv("roman-urdu-sentiment.csv")
```

This non-streaming example downloads the selected configuration into local memory. For the larger corpora, use streaming or the Hub-generated Parquet files instead. CSV does not carry a schema as reliably as Parquet; preserve the header and the source fields when sharing a CSV export.

## Reuse responsibly

The repository is mixed-license. A license for one configuration does not apply to the others. Keep source, attribution, license and `review_status` fields when filtering or exporting. Do not treat whitespace token counts as model-token counts, and do not treat automated filtering or duplicate checks as human review or a guarantee that the data has no personal information.

See [license policy](LICENSE_POLICY.md), [data architecture](DATA_ARCHITECTURE.md), and the [dataset cards](../CATALOG.md).
