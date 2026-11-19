---
language:
- ur
pretty_name: Klam (کلام)
configs:
- config_name: klam
  default: true
  data_files:
  - split: train
    path: "klam-original/data/*.jsonl.gz"
---

# Klam (کلام)

Klam is one simple Urdu dataset with a single record format. Its starter corpus contains 307 Ghalib poetry records from a CC0-dedicated digital transcription.

**Starter corpus: 307 records; native-speaker reviewed: 0.** All starter records are marked `unreviewed`. The poetry transcription's preface says it is based on the 1862 Nizami edition, with additional variants from other editions. Klam preserves per-record source links and the pinned source version. The earlier third-party NLP corpus releases are not inputs to Klam.

When records are available, load the single Klam dataset with:

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

The release uses one record format with title, text, genre label, source version, rights basis, license, attribution, and review status. Source manifests stay with the Klam release for people who need to audit them.

See the [Klam contribution guide](https://github.com/DaniyalMusadiq1/open-urdu-datasets/blob/main/docs/KLAM_CONTRIBUTION.md) for how original, permissioned, CC0, and verified public-domain text can be added.
